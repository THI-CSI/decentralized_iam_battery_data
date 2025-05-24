import json
import os
import logging
from datetime import datetime

from Crypto.PublicKey import ECC
from functools import lru_cache
from fastapi import FastAPI, Depends, HTTPException, Path
from fastapi.responses import JSONResponse
from tinydb import TinyDB, where
from crypto.crypto import load_private_key, generate_keys, decrypt_and_verify, encrypt_and_sign, determine_role
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
    verify_request(item, private_key)
    if db.search(where("did") == did):
        logging.warning(f"DID {did} already exists in DB")
        return error_response(400, "Entry already exists.")
    else:
        if determine_role(db, did) == "oem":
            db.insert({"did": did, "encrypted_data": item.model_dump()})
            return {"ok": f"Entry for {did} added successfully."}
        else:
            raise HTTPException(status_code=403, detail="Unauthorized.")


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
    decrypted_item = verify_request(item, private_key)
    document = db.search(where("did") == did)
    if not document:
        return error_response(404, "Entry doesn't exist.")
    decrypted_document = decrypt_and_verify(private_key, document[0]["encrypted_data"])
    for key, value in decrypted_item.items():
        set_nested_value(decrypted_document, key.split("."), value)
    encrypt_and_sign(private_key.public_key(), json.dumps(decrypted_document).encode("utf-8"))
    db.update(document[0], where("did") == did)
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
):
    # Search for database entry with the given DID
    document = db.search(where("did") == did)

    # If no entry is found, raise an HTTP exception
    if not document:
        raise HTTPException(status_code=404, detail="Entry doesn't exist.")

    # Delete the entry from the database
    db.remove(where("did") == did)

    # Return a success message indicating the deletion was successful
    return {"ok": f"Entry for {did} deleted successfully."}
