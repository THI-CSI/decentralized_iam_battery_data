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

from crypto.crypto import load_private_key, generate_keys, encrypt_hpke, determine_role, \
    decrypt_hpke, verify_vc
from dotenv import load_dotenv
from util.models import EncryptedPayload, SuccessfulResponse, DID, \
    BadRequestResponse, ForbiddenResponse, NotFoundResponse, VerifiablePresentation, get_encrypted_payload
from util.middleware import verify_request, retrieve_data
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


@app.get("/batterypass/{did}",
         summary="Get a battery pass entry by DID",
         tags=["Battery Pass"],
         responses={
             200: {"model": dict, "content": {"application/json": {"example": batterypass_json}}},
             400: {"model": BadRequestResponse},
             404: {"model": NotFoundResponse},
         },
         description="A detailed description can be found "
                     "**[here](https://github.com/THI-CSI/decentralized_iam_battery_data"
                     "/blob/main/cloud/docs/api.md#get-batterypassdid)**."
         )
async def read_item(
        did: DID,
        payload: str = Query(
            default=None,
            description="An [encrypted JSON payload](https://github.com/THI-CSI/decentralized_iam_battery_data"
                        "/blob/main/cloud/docs/api.md#request-body) as a serialized string.\n\n"
                        "The payload inside the ciphertext can contain a 128-byte random number "
                        "**or** a [Verifiable Presentation](https://www.w3.org/TR/vc-data-model-2.0/) granting access."
        ),
        public: bool = Query(default=True, description="Whether to retrieve only public battery pass data.\n\n"
                                                       "If set to `false`, `payload` must be provided."),
        db: TinyDB = Depends(get_db),
        private_key: ECC.EccKey = Depends(get_private_key),
):
    document = db.search(where("did") == did)
    if not document:
        return error_response(404, "Entry doesn't exist.")
    if public:
        return retrieve_data(scope="public", did=did, doc=document[0], private_key=private_key)
    if not payload:
        return error_response(400, "Payload must be provided.")
    try:
        payload: EncryptedPayload = EncryptedPayload.model_validate_json(payload) if payload else None
        decrypted_payload = verify_request(payload, private_key)
        vp: VerifiablePresentation = is_vp(decrypted_payload)
        if not vp and len(decrypted_payload) != 128:
            raise ValueError("Invalid length for random value.")
    except ValueError as e:
        return error_response(400, str(e))
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
        did: DID,
        db: TinyDB = Depends(get_db),
        private_key: ECC.EccKey = Depends(get_private_key),
):
    try:
        decrypted_payload = verify_request(payload, private_key)
    except ValueError as e:
        return error_response(400, str(e))
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
        did: DID,
        db: TinyDB = Depends(get_db),
        private_key: ECC.EccKey = Depends(get_private_key),
):
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
        did: DID,
        payload: str = Query(
            description="An [encrypted JSON payload](https://github.com/THI-CSI/decentralized_iam_battery_data"
                        "/blob/main/cloud/docs/api.md#request-body) as a serialized string.\n\n"
                        "The payload inside the ciphertext must contain a 128-byte random number."
        ),
        db: TinyDB = Depends(get_db),
        private_key: ECC.EccKey = Depends(get_private_key),
):
    try:
        payload = EncryptedPayload.model_validate_json(payload)
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


@app.get("/batterypass/{did}/qr",
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
