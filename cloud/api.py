import json
import os
import logging
from datetime import datetime
from json import JSONDecodeError

from Crypto.PublicKey import ECC
from functools import lru_cache
from fastapi import FastAPI, Depends, HTTPException, Path
from fastapi.responses import JSONResponse
from tinydb import TinyDB, where
from crypto.crypto import load_private_key, generate_keys, decrypt_and_verify, encrypt_hpke, determine_role, \
    decrypt_hpke
from dotenv import load_dotenv
from util.models import EncryptedPayload, SuccessfulResponse, ErrorResponse
from util.middleware import verify_request

app = FastAPI(
    title="Battery Pass API",
    description="A detailed API description can be found under <code>cloud/docs/api.md</code>."
)

load_dotenv()
generate_keys(os.getenv("PASSPHRASE", "secret"))
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def error_response(status_code: int, message: str):
    return JSONResponse(
        status_code=status_code,
        content={
            "status": status_code,
            "message": message,
            "timestamp": datetime.now().isoformat()
        }
    )


def get_db():
    db = TinyDB("db.json")
    try:
        yield db
    finally:
        db.close()


@lru_cache()
def get_private_key():
    return load_private_key(os.getenv("PASSPHRASE", "secret"))


def set_nested_value(doc, path_keys, new_value):
    current_level = doc
    for key in path_keys[:-1]:
        current_level = current_level.setdefault(key, {})
    current_level[path_keys[-1]] = new_value


@app.get("/",
         summary="API Health Check",
         tags=["General"],
         response_model=SuccessfulResponse)
def read_root():
    return {"ok": "API is running"}


@app.get("/batterypass/",
         summary="List all stored DIDs",
         tags=["Battery Pass"],
         responses={
             200: {"model": list[str]}
         })
async def list_dids(db: TinyDB = Depends(get_db)):
    entries = db.all()
    return [entry["did"] for entry in entries if "did" in entry]


@app.get("/batterypass/{did}",
         summary="Get a battery pass entry by DID",
         tags=["Battery Pass"],
         responses={
             200: {"model": SuccessfulResponse},
             400: {"model": ErrorResponse},
             404: {"model": ErrorResponse},
         })
async def read_item(
        did: str = Path(description="A properly formed DID"),
        db: TinyDB = Depends(get_db),
):
    return db.search(where("did") == did)


@app.put("/batterypass/{did}",
         summary="Create a new battery pass entry for a DID",
         tags=["Battery Pass"],
         responses={
             200: {"model": SuccessfulResponse},
             400: {"model": ErrorResponse},
             403: {"model": ErrorResponse},
             404: {"model": ErrorResponse},
         })
async def create_item(
        item: EncryptedPayload,
        did: str = Path(description="A properly formed DID"),
        db: TinyDB = Depends(get_db),
        private_key: ECC.EccKey = Depends(get_private_key),
):
    try:
        decrypted_item = verify_request(item, private_key)
    except ValueError as e:
        return error_response(400, e.args[0])

    if not determine_role(db, did, item["did"]) == "oem":
        return error_response(403, "Unauthorized.")
    if db.search(where("did") == did):
        logging.warning(f"DID {did} already exists in DB")
        return error_response(400, "Entry already exists.")
    db.insert({
        "did": did,
        "encrypted_data": encrypt_hpke(private_key, decrypted_item)
    })
    return {"ok": f"Entry for {did} added successfully."}


@app.post("/batterypass/{did}",
          summary="Update a battery pass entry by DID",
          tags=["Battery Pass"],
          responses={
              200: {"model": SuccessfulResponse},
              400: {"model": ErrorResponse},
              403: {"model": ErrorResponse},
              404: {"model": ErrorResponse},
          })
async def update_item(
        item: EncryptedPayload,
        did: str = Path(description="A properly formed DID"),
        db: TinyDB = Depends(get_db),
        private_key: ECC.EccKey = Depends(get_private_key),
):
    try:
        decrypted_item = json.loads(verify_request(item, private_key))
    except JSONDecodeError:
        return error_response(400, "Error occurred while decoding JSON.")
    except ValueError as e:
        return error_response(400, e.args[0])

    document = db.search(where("did") == did)
    if determine_role(db, did, item["did"]) != "bms":
        return error_response(403, "Unauthorized.")
    if not document:
        return error_response(404, "Entry doesn't exist.")
    decrypted_document = json.loads(decrypt_hpke(private_key, document[0]["encrypted_data"]))
    for element in decrypted_item:  # Iterate over the list of JSON items
        if not isinstance(element, dict) or len(element) != 1:
            return error_response(400, "Invalid update format.")
        key, value = next(iter(element.items()))
        set_nested_value(decrypted_document, key.split("."), value)
    encrypted_data = encrypt_hpke(
        private_key.public_key(), json.dumps(decrypted_document).encode()
    )
    db.update({"encrypted_data": encrypted_data}, where("did") == did)
    return {"ok": f"Entry for {did} updated successfully."}


@app.delete("/batterypass/{did}",
            summary="Delete a battery pass entry by DID",
            tags=["Battery Pass"],
            responses={
                200: {"model": SuccessfulResponse},
                400: {"model": ErrorResponse},
                403: {"model": ErrorResponse},
                404: {"model": ErrorResponse},
            })
async def delete_item(
        item: EncryptedPayload,
        did: str = Path(description="A properly formed DID"),
        db: TinyDB = Depends(get_db),
        private_key: ECC.EccKey = Depends(get_private_key),
):
    try:
        verify_request(item, private_key)
    except ValueError as e:
        return error_response(400, e.args[0])

    if determine_role(db, did, item["did"]) != "bms":
        return error_response(403, "Unauthorized.")

    # Search for database entry with the given DID
    document = db.search(where("did") == did)

    # If no entry is found, raise an HTTP exception
    if not document:
        return error_response(404, "Entry doesn't exist.")

    # Delete the entry from the database
    db.remove(where("did") == did)

    # Return a success message indicating the deletion was successful
    return {"ok": f"Entry for {did} deleted successfully."}
