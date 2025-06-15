import json
import os
import logging
import pathlib
from datetime import datetime
from json import JSONDecodeError
from typing import Literal, Annotated, Optional

from Crypto.PublicKey import ECC
from functools import lru_cache
from fastapi import FastAPI, Depends, Path, Body
from fastapi.params import Query
from fastapi.responses import JSONResponse
from tinydb import TinyDB, where
from tinydb.table import Document

from crypto.crypto import load_private_key, generate_keys, encrypt_hpke, determine_role, \
    decrypt_hpke, verify_vc
from dotenv import load_dotenv
from util.models import EncryptedPayload, SuccessfulResponse, DID, \
    BadRequestResponse, ForbiddenResponse, NotFoundResponse, VerifiablePresentation, get_encrypted_payload
from util.middleware import verify_request
from util.validators import validate_battery_pass_payload

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


def example_payload(did: DID, vp: VerifiablePresentation):
    payload = payload_json.copy()
    payload["did"] = did
    payload["vp"] = vp
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
    if isinstance(current_level[path_keys[-1]], list):
        current_level[path_keys[-1]].append(new_value)
    else:
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
    if scope == "bms":
        return json.loads(decrypted_data)
    return None


@app.get("/batterypass/{did}",
         summary="Get a battery pass entry by DID",
         tags=["Battery Pass"],
         responses={
             200: {"model": dict, "content": {"application/json": {"example": batterypass_json}}},
             400: {"model": BadRequestResponse},
             404: {"model": NotFoundResponse},
         })
async def read_item(
        did: str,
        payload: str = Query(
            default=None,
            description="An [encrypted JSON payload](https://github.com/THI-CSI/decentralized_iam_battery_data"
                        "/blob/main/cloud/docs/api.md#request-body) as a serialized string.\n\n"
                        "The payload inside the ciphertext must contain a 128-byte random number."
        ),
        public: bool = Query(default=True, description="Whether to retrieve only public battery pass data.\n\n"
                                                       "If set to `false`, either `payload` or `vp` must be provided."),
        vp: str = Query(default=None,
                        description="A verifiable presentation signed by the BMS defining the access level as a "
                                    "serialized JSON string."),
        db: TinyDB = Depends(get_db),
        private_key: ECC.EccKey = Depends(get_private_key),
):
    document = db.search(where("did") == did)
    if not document:
        return error_response(404, "Entry doesn't exist.")
    if public:
        return retrieve_data(scope="public", did=did, doc=document[0], private_key=private_key)
    vp: VerifiablePresentation = VerifiablePresentation.model_validate_json(vp) if vp else None
    payload: EncryptedPayload = EncryptedPayload.model_validate_json(payload) if payload else None
    try:
        random_number = verify_request(payload, private_key)
        if len(random_number) != 128:
            raise ValueError("Invalid length for random value.")
    except ValueError as e:
        return error_response(400, e.args[0])
    if determine_role(document[0], payload.did) == "bms":
        return retrieve_data(scope="bms", did=did, doc=document[0], private_key=private_key)
    if vp and verify_vc(vp):
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
         },
         description="A detailed description can be found "
                     "**[here](https://github.com/THI-CSI/decentralized_iam_battery_data"
                     "/blob/main/cloud/docs/api.md#put-batterypassdid)**.")
async def create_item(
        payload: EncryptedPayload,
        did: str,
        db: TinyDB = Depends(get_db),
        private_key: ECC.EccKey = Depends(get_private_key),
):
    logging.info("Test")
    try:
        decrypted_payload = verify_request(payload, private_key)
    except ValueError as e:
        return error_response(400, e.args[0])
    if db.search(where("did") == did):
        logging.warning(f"DID {did} already exists in DB")
        return error_response(400, "Entry already exists.")
    if not determine_role(None, payload.did) == "oem":
        return error_response(403, "Access denied.")
    results = validate_battery_pass_payload(json.loads(decrypted_payload))
    if not all(value == "Valid" for value in results.values()):
        return error_response(400, f"Invalid payload: {json.dumps(results)}")
    db.insert({
        "did": did,
        "encrypted_data": encrypt_hpke(private_key, decrypted_payload)
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
          },
          description="A detailed description can be found "
                      "**[here](https://github.com/THI-CSI/decentralized_iam_battery_data"
                      "/blob/main/cloud/docs/api.md#post-batterypassdid)**.")
async def update_item(
        payload: EncryptedPayload,
        did: str,
        db: TinyDB = Depends(get_db),
        private_key: ECC.EccKey = Depends(get_private_key),
):
    try:
        decrypted_payload = json.loads(verify_request(payload, private_key))
    except JSONDecodeError:
        return error_response(400, "Error occurred while decoding JSON.")
    except ValueError as e:
        return error_response(400, e.args[0])

    document = db.search(where("did") == did)
    if not document:
        return error_response(404, "Entry doesn't exist.")
    if determine_role(document[0], payload.did) != "bms":
        return error_response(403, "Access denied.")
    decrypted_document = json.loads(decrypt_hpke(private_key, document[0]["encrypted_data"]))
    for element in decrypted_payload:  # Iterate over the list of JSON items
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
            },
            description="A detailed description can be found "
                        "**[here](https://github.com/THI-CSI/decentralized_iam_battery_data"
                        "/blob/main/cloud/docs/api.md#delete-batterypassdid)**.")
async def delete_item(
        did: str,
        payload: str = Query(
            description="An [encrypted JSON payload](https://github.com/THI-CSI/decentralized_iam_battery_data"
                        "/blob/main/cloud/docs/api.md#request-body) as a serialized string.\n\n"
                        "The payload inside the ciphertext must contain a 128-byte random number."
        ),
        db: TinyDB = Depends(get_db),
        private_key: ECC.EccKey = Depends(get_private_key),
):
    payload = EncryptedPayload.model_validate_json(payload)
    try:
        verify_request(payload, private_key)
    except ValueError as e:
        return error_response(400, e.args[0])

    # Search for database entry with the given DID
    document = db.search(where("did") == did)

    # If no entry is found, raise an HTTP exception
    if not document:
        return error_response(404, "Entry doesn't exist.")

    if determine_role(document[0], payload.did) != "bms":
        return error_response(403, "Access denied.")


    # Delete the entry from the database
    db.remove(where("did") == did)

    # Return a success message indicating the deletion was successful
    return {"ok": f"Entry for {did} deleted successfully."}
