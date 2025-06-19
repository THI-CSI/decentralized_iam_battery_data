import json
import os
import logging
import pathlib

from datetime import datetime
from io import BytesIO
from json import JSONDecodeError

import multibase
import qrcode
from Crypto.PublicKey import ECC
from functools import lru_cache
from fastapi import FastAPI, Depends, Path, Body
from fastapi.params import Query
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import ValidationError, HttpUrl
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.colormasks import SolidFillColorMask
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from tinydb import TinyDB, where

from crypto.crypto import initialize, load_private_key, generate_keys, encrypt_hpke, determine_role, \
    decrypt_hpke, verify_vp
from dotenv import load_dotenv
from util.models import EncryptedPayload, SuccessfulResponse, DID, \
    BadRequestResponse, ForbiddenResponse, NotFoundResponse, VerifiablePresentation
from util.middleware import verify_request, retrieve_data
from util.validators import validate_battery_pass_payload

app = FastAPI(
    title="Battery Pass API",
    description="A detailed API description can be found "
                "**[here](https://github.com/THI-CSI/decentralized_iam_battery_data/tree/main/cloud/docs/api.md)**.",
    redoc_url=None,
)

load_dotenv()
initialize()
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
with open(pathlib.Path(__file__).parent / "docs" / "example" / "batterypass.json") as f:
    batterypass_json = json.load(f)


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
    db = TinyDB("data/db.json")
    try:
        yield db
    finally:
        db.close()


@lru_cache()
def get_private_key():
    return load_private_key(os.getenv("PASSPHRASE", "secret"))


pub_key_multibase = multibase.encode("base58btc", get_private_key().public_key().export_key(format="DER"))


def set_nested_value(doc, path_keys, new_value):
    current_level = doc
    for key in path_keys[:-1]:
        current_level = current_level.setdefault(key, {})
    if isinstance(current_level[path_keys[-1]], list):
        current_level[path_keys[-1]].append(new_value)
    else:
        current_level[path_keys[-1]] = new_value


def is_vp(b: bytes) -> VerifiablePresentation | None:
    try:
        model = json.loads(b)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None
    try:
        return VerifiablePresentation.model_validate(model)
    except ValidationError:
        raise ValueError("Invalid Verifiable Presentation.")


def generate_qr_code(base_url: HttpUrl, did: DID) -> BytesIO:
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=5,
        border=4,
    )
    qr.add_data(f"{base_url}?did={did}")
    qr.make(fit=True)
    img = qr.make_image(
        image_factory=StyledPilImage,
        module_drawer=RoundedModuleDrawer(),
        color_mask=SolidFillColorMask(front_color=(50, 100, 60), back_color=(255, 255, 255))
    )
    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf


@app.get("/",
         summary="API Health Check",
         tags=["General"],
         responses={
             200: {"content": {"application/json": {"example": {
                 "ok": "API is running.", "publicKeyMultibase": pub_key_multibase
             }}}},
         })
def read_root():
    """
    Handles the root endpoint of the API and provides a response indicating
    the operational status of the API.
    """
    return {"ok": "API is running.", "publicKeyMultibase": pub_key_multibase}


@app.get("/batterypass/",
         summary="List all stored DIDs",
         tags=["Battery Pass"],
         responses={
             200: {"model": list[DID]}
         })
async def list_dids(db: TinyDB = Depends(get_db)):
    entries = db.all()
    return [entry["did"] for entry in entries if "did" in entry]


@app.post("/batterypass/read/{did}",
          summary="Get a battery pass entry by DID",
          tags=["Battery Pass"],
          responses={
              200: {"model": dict, "content": {"application/json": {"example": batterypass_json}}},
              400: {"model": BadRequestResponse},
              404: {"model": NotFoundResponse},
          },
          description="A detailed description can be found "
                      "**[here](https://github.com/THI-CSI/decentralized_iam_battery_data"
                      "/blob/main/cloud/docs/api.md#get-batterypassreaddid)**. "
                      "If body is omitted, read public data."
          )
async def read_item(
        did: DID,
        payload: EncryptedPayload = None,
        db: TinyDB = Depends(get_db),
        private_key: ECC.EccKey = Depends(get_private_key),
):
    """
    Retrieve a battery pass entry by a specified Decentralized Identifier (DID).
    This endpoint fetches information from the TinyDB database corresponding
    to the given DID. The DID must be formatted correctly for the query to
    execute successfully.
    """
    document = db.search(where("did") == did)
    if not document:
        return error_response(404, "Entry doesn't exist.")
    if not payload:
        return retrieve_data(scope="public", did=did, doc=document[0], private_key=private_key)
    try:
        decrypted_payload = verify_request(payload, private_key)
        vp: VerifiablePresentation = is_vp(decrypted_payload)
        if not vp and len(decrypted_payload) != 128:
            raise ValueError("Invalid length for random value.")
    except ValueError as e:
        return error_response(400, str(e))
    if determine_role(document[0], payload.did) == "bms":
        return retrieve_data(scope="bms", did=did, doc=document[0], private_key=private_key)
    if vp and verify_vp(vp) == "read":
        return retrieve_data(scope="legitimate_interest", did=did, doc=document[0], private_key=private_key)
    return error_response(400, "Invalid request.")


@app.put("/batterypass/create/{did}",
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
                     "/blob/main/cloud/docs/api.md#put-batterypasscreatedid)**.")
async def create_item(
        payload: EncryptedPayload,
        did: DID,
        db: TinyDB = Depends(get_db),
        private_key: ECC.EccKey = Depends(get_private_key),
):
    """
    Create a new battery pass entry for a DID.

    This endpoint allows adding a new entry associated with the specified
    DID in the database. The item payload undergoes verification using the
    provided private key. If an entry for the DID already exists within the
    database, an HTTPException with status code 400 is raised.
    """
    try:
        decrypted_payload = verify_request(payload, private_key)
    except ValueError as e:
        return error_response(400, str(e))
    if db.search(where("did") == did):
        logging.warning(f"DID {did} already exists in DB")
        return error_response(400, "Entry already exists.")
    # TODO Fix Mock BMS Data Generator and implement OEM Endpoint to create Battery Pass
    #if not determine_role(None, payload.did) == "oem":
    #    return error_response(403, "Access denied.")
    results = validate_battery_pass_payload(json.loads(decrypted_payload))
    if not all(value == "Valid" for value in results.values()):
        return error_response(400, f"Invalid payload: {json.dumps(results)}")
    db.insert({
        "did": did,
        "encrypted_data": encrypt_hpke(private_key, decrypted_payload)
    })
    return {"ok": f"Entry for {did} added successfully."}


@app.post("/batterypass/update/{did}",
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
                      "/blob/main/cloud/docs/api.md#post-batterypassupdatedid)**.")
async def update_item(
        payload: EncryptedPayload,
        did: DID,
        db: TinyDB = Depends(get_db),
        private_key: ECC.EccKey = Depends(get_private_key),
):
    """
    Updates an existing entry in the database for a specified DID (decentralized identifier) by decrypting the
    provided encrypted payload, modifying the corresponding entry, and encrypting it again.

    Decodes the encrypted data provided in the request payload using the specified private key. Fetches the document
    associated with the given DID from the database, decrypts it, and applies the updates from the payload. The updated
    data is re-encrypted and stored back in the database.
    """
    try:
        decrypted_payload = json.loads(verify_request(payload, private_key))
    except JSONDecodeError:
        return error_response(400, "Error occurred while decoding JSON.")
    except ValueError as e:
        return error_response(400, str(e))

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


@app.post("/batterypass/delete/{did}",
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
                      "/blob/main/cloud/docs/api.md#delete-batterypassdeletedid)**.")
async def delete_item(
        did: DID,
        payload: EncryptedPayload,
        db: TinyDB = Depends(get_db),
        private_key: ECC.EccKey = Depends(get_private_key),
):
    """
    For a given DID, delete the entry from the database.
    """
    try:
        verify_request(payload, private_key)
    except ValueError as e:
        return error_response(400, str(e))

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


@app.get("/batterypass/qr/{did}",
         summary="Get a QR code for a battery pass entry by DID",
         tags=["Battery Pass"],
         responses={
             200: {"content": {"image/png": {"example": b""}}},
             400: {"model": BadRequestResponse},
         })
def read_qr(did: DID, url: HttpUrl = Query(description="The URL for the battery pass viewer.")):
    try:
        qr_code = generate_qr_code(url, did)
    except ValueError as e:
        return error_response(400, str(e))
    return StreamingResponse(qr_code, media_type="image/png")
