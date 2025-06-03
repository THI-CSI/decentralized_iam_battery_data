import json
import os
import logging
import pathlib
from datetime import datetime
from json import JSONDecodeError
from typing import Literal, Annotated

from Crypto.PublicKey import ECC
from functools import lru_cache
from fastapi import FastAPI, Depends, Path, Body
from fastapi.openapi.models import Example
from fastapi.responses import JSONResponse
from tinydb import TinyDB, where
from tinydb.table import Document

from crypto.crypto import load_private_key, generate_keys, encrypt_hpke, determine_role, \
    decrypt_hpke, verify_vc
from dotenv import load_dotenv
from util.models import EncryptedPayload, SuccessfulResponse, EncryptedPayloadVC, DID, \
    BadRequestResponse, ForbiddenResponse, NotFoundResponse, VerifiableCredential
from util.middleware import verify_request

app = FastAPI(
    title="Battery Pass API",
    description="A detailed API description can be found "
                "**[here](https://github.com/THI-CSI/decentralized_iam_battery_data/tree/main/cloud/docs/api.md)**.",
    redoc_url=None,
)

load_dotenv()
generate_keys(os.getenv("PASSPHRASE", "secret"))
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
with open(pathlib.Path(__file__).parent / "docs" / "example" / "batterypass.json") as f:
    batterypass_json = json.load(f)
with open(pathlib.Path(__file__).parent / "docs" / "example" / "payload.json") as f:
    payload_json = json.load(f)
with open(pathlib.Path(__file__).parent.parent /
          "blockchain" / "docs" / "VC-DID-examples" / "VC-ServiceAccess.json") as f:
    vc_service_json = json.load(f)


def example_payload(did: DID, vc: VerifiableCredential):
    payload = payload_json.copy()
    payload["did"] = did
    payload["vc"] = vc
    return payload


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
         responses={
             200: {"model": SuccessfulResponse,
                   "content": {"application/json": {"example": {"ok": "API is running."}}}},
         })
def read_root():
    return {"ok": "API is running."}


@app.get("/batterypass/",
         summary="List all stored DIDs",
         tags=["Battery Pass"],
         responses={
             200: {"model": list[DID]}
         })
async def list_dids(db: TinyDB = Depends(get_db)):
    entries = db.all()
    return [entry["did"] for entry in entries if "did" in entry]


def retrieve_data(scope: Literal["public", "bms", "legitimate_interest"], did: str, doc: Document,
                  private_key: ECC.EccKey):
    if scope not in ["public", "bms", "legitimate_interest"]:
        raise ValueError(f"Scope '{scope}' is not in ['public', 'bms', 'legitimate_interest'].")
    decrypted_data = decrypt_hpke(
        private_key=private_key,
        bundle=doc["encrypted_data"]
    )


@app.get("/batterypass/{did}",
         summary="Get a battery pass entry by DID",
         tags=["Battery Pass"],
         responses={
             200: {"model": dict, "content": {"application/json": {"example": batterypass_json}}},
             400: {"model": BadRequestResponse},
             404: {"model": NotFoundResponse},
         })
async def read_item(
        did: DID,
        item: Annotated[EncryptedPayloadVC, Body(openapi_examples={
            "public": {
                "summary": "Public scope",
                "description": "Requires an empty body.",
                "value": {}
            },
            "bms": {
                "summary": "BMS scope",
                "description": "Requires a signature signed by the BMS.<br><br>"
                               "The payload inside the ciphertext must be a **128-byte random number**.",
                "value": example_payload(did="did:batterypass:bms.sn-987654321", vc=None)
            },
            "vc": {
                "summary": "VC-defined scope",
                "description": "Requires a verifiable credential signed by the BMS defining the access level.<br><br>"
                               "The payload inside the ciphertext must be a **128-byte random number**.",
                "value": example_payload(did="did:batterypass:bms.sn-987654321", vc=vc_service_json)
            }
        })],
        db: TinyDB = Depends(get_db),
        private_key: ECC.EccKey = Depends(get_private_key),
):
    document = db.search(where("did") == did)
    if not document:
        return error_response(404, "Entry doesn't exist.")
    if not item:
        return retrieve_data(scope="public", did=did, doc=document[0], private_key=private_key)
    try:
        random_number = verify_request(item, private_key)
        if len(random_number) != 128:
            raise ValueError("Invalid length for random value.")
    except ValueError as e:
        return error_response(400, e.args[0])
    if determine_role(db, did, item["did"]) == "bms":
        return retrieve_data(scope="bms", did=did, doc=document[0], private_key=private_key)
    if "vc" in item and verify_vc(item["vc"]):
        return retrieve_data(scope="legitimate_interest", did=did, doc=document[0], private_key=private_key)
    return error_response(400, "Invalid request.")


@app.put("/batterypass/{did}",
         summary="Create a new battery pass entry for a DID",
         tags=["Battery Pass"],
         responses={
             200: {"model": SuccessfulResponse,
                   "content": {
                       "application/json": {
                           "example": {"ok": "Entry for did:batterypass:bms.sn-987654321 added successfully."}
                       }
                   }},
             400: {"model": BadRequestResponse},
             403: {"model": ForbiddenResponse},
         })
async def create_item(
        item: Annotated[EncryptedPayload, Body(openapi_examples={
            "default": {
                "summary": "Default",
                "description": "A detailed description can be found "
                               "**[here](https://github.com/THI-CSI/decentralized_iam_battery_data/blob/main/cloud/docs/api.md#put-batterypassdid)**.",
                "value": example_payload(did="did:batterypass:bms.sn-987654321", vc=None)
            }
        })],
        did: str = Path(description="A properly formed DID"),
        db: TinyDB = Depends(get_db),
        private_key: ECC.EccKey = Depends(get_private_key),
):
    try:
        decrypted_item = verify_request(item, private_key)
    except ValueError as e:
        return error_response(400, e.args[0])

    if not determine_role(db, did, item["did"]) == "oem":
        return error_response(403, "Access denied.")
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
              200: {"model": SuccessfulResponse,
                    "content": {
                        "application/json": {
                            "example": {"ok": "Entry for did:batterypass:bms.sn-987654321 updated successfully."}
                        }
                    }},
              400: {"model": BadRequestResponse},
              403: {"model": ForbiddenResponse},
              404: {"model": NotFoundResponse},
          })
async def update_item(
        item: Annotated[EncryptedPayload, Body(openapi_examples={
            "default": {
                "summary": "Default",
                "description": "A detailed description can be found "
                               "**[here](https://github.com/THI-CSI/decentralized_iam_battery_data/blob/main/cloud/docs/api.md#post-batterypassdid)**.",
                "value": example_payload(did="did:batterypass:bms.sn-987654321", vc=None)
            }
        })],
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
        return error_response(403, "Access denied.")
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
                200: {"model": SuccessfulResponse,
                      "content": {
                          "application/json": {
                              "example": {"ok": "Entry for did:batterypass:bms.sn-987654321 deleted successfully."}
                          }
                      }},
                400: {"model": BadRequestResponse},
                403: {"model": ForbiddenResponse},
                404: {"model": NotFoundResponse},
            })
async def delete_item(
        item: Annotated[EncryptedPayload, Body(openapi_examples={
            "default": {
                "summary": "Default",
                "description": "A detailed description can be found "
                               "**[here](https://github.com/THI-CSI/decentralized_iam_battery_data/blob/main/cloud/docs/api.md#delete-batterypassdid)**.",
                "value": example_payload(did="did:batterypass:bms.sn-987654321", vc=None)
            }
        })],
        did: str = Path(description="A properly formed DID"),
        db: TinyDB = Depends(get_db),
        private_key: ECC.EccKey = Depends(get_private_key),
):
    try:
        verify_request(item, private_key)
    except ValueError as e:
        return error_response(400, e.args[0])

    if determine_role(db, did, item["did"]) != "bms":
        return error_response(403, "Access denied.")

    # Search for database entry with the given DID
    document = db.search(where("did") == did)

    # If no entry is found, raise an HTTP exception
    if not document:
        return error_response(404, "Entry doesn't exist.")

    # Delete the entry from the database
    db.remove(where("did") == did)

    # Return a success message indicating the deletion was successful
    return {"ok": f"Entry for {did} deleted successfully."}
