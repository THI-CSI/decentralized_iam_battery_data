import json
import os
import logging
import requests

from Crypto.Hash import SHA3_256
from Crypto.PublicKey import ECC
from functools import lru_cache
from fastapi import FastAPI, Depends, HTTPException, Path
from tinydb import TinyDB, where
from crypto.crypto import load_private_key, generate_keys, decrypt_and_verify, encrypt_and_sign
from dotenv import load_dotenv
from util.models import EncryptedPayload
from util.middleware import verify_request
from typing import Dict, Any

# devbod: TODO: Change this when having more info
BLOCKCHAIN_URL = "http://localhost:8000/FILLER/FOR/NOW"

app = FastAPI()
load_dotenv()
generate_keys(os.getenv("PASSPHRASE", "secret"))
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
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


@app.get("/")
def read_root():
    return {"message": "API is working"}


@app.get("/batterypass/{did}", summary="Get a battery pass entry by DID")
async def read_item(
        did: str = Path(description="Must be a properly formed DID"),
        db: TinyDB = Depends(get_db),
):
    return db.search(where("did") == did)


@app.put("/batterypass/{did}", summary="Create a new battery pass entry for a DID")
async def create_item(
        item: EncryptedPayload,
        did: str,
        db: TinyDB = Depends(get_db),
        private_key: ECC.EccKey = Depends(get_private_key),
):
    verify_request(item, private_key)
    if db.search(where("did") == did):
        raise HTTPException(status_code=400, detail="Entry already exists.")
    else:
        db.insert({"did": did, "encrypted_data": item.model_dump()})
        return {"ok": f"Entry for {did} added successfully."}


@app.post("/batterypass/{did}")
async def update_item(
        item: EncryptedPayload,
        did: int,
        db: TinyDB = Depends(get_db),
        private_key: ECC.EccKey = Depends(get_private_key),
):
    decrypted_item = verify_request(item, private_key)
    document = db.search(where("did") == did)
    if not document:
        raise HTTPException(status_code=404, detail="Entry doesn't exist.")
    decrypted_document = decrypt_and_verify(private_key, document[0]["encrypted_data"])
    for key, value in decrypted_item.items():
        set_nested_value(decrypted_document, key.split("."), value)
    encrypt_and_sign(private_key.public_key(), json.dumps(decrypted_document).encode("utf-8"))
    db.update(document[0], where("did") == did)
    return {"ok": f"Entry for {did} updated successfully."}

# Note: This function could be moved to crypto.py for consistency
def extract_vc_info(vc: Dict[str, Any]) -> tuple[str, str, str]:
    """
    Extract URI, issuer, and holder from a VC object.

    :param vc: The Verifiable Credential (VC) as a dictionary.
    :return: A tuple containing (URI, Issuer ID, Holder ID).
    """

    # Get all necessary data from the verifiable credential
    uri = vc.get("id")
    issuer = vc.get("issuer")
    subject = vc.get("credentialSubject")

    # Checking credentialSubjects form (If we have a uniform form, this is not necessary,
    # but will be left in for now)
    if isinstance(subject, dict):
        holder = subject.get("id")
    elif isinstance(subject, list) and len(subject) > 0:
        holder = subject[0].get("id")
    else:
        holder = None

    if uri is None or issuer is None or holder is None:
        raise ValueError("Invalid Verifiable Credential")

    return uri, issuer, holder


# Note: This function could be moved to crypto.py for consistency
def verify_vc(vc_json_object: json) -> bool:
    """
    This function takes a Verifiable Credential dictionary, extracts the URI, issuer id, and holder id, and
    creates a 256-bit SHA-3 hash of the whole VC. The Data is then send to the blockchain to be verified.
    """

    # Extract the uri, issuer and holder
    uri, issuer, holder = extract_vc_info(vc_json_object)

    # To generate the Hash, we must first serialize the Object
    serialized_vc = json.dumps(vc_json_object, separators=(',', ':'), sort_keys=True).encode('utf-8')

    # Create the SHA3-256bit Hash
    vc_hash = SHA3_256.new(serialized_vc)

    # devbod: TODO: Should we use hexdigest()?
    # vc_digest = vc_hash.hexdigest()

    # Now we need to send the Data to the Blockchain
    # First we create the Datastructures we send
    data = {
        "uri": uri,
        "issuer": issuer,
        "holder": holder,
        "hash": vc_hash
    }

    response = requests.post(BLOCKCHAIN_URL, json=data)

    if response.status_code == 200:
        return True
    else:
        return False
