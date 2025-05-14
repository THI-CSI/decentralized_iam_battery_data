import json
import os
import logging


from Crypto.PublicKey import ECC
from functools import lru_cache
from fastapi import FastAPI, Depends, HTTPException, Path
from tinydb import TinyDB, where
from crypto.crypto import load_private_key, generate_keys, decrypt_and_verify, encrypt_and_sign
from dotenv import load_dotenv
from util.models import EncryptedPayload
from util.middleware import verify_request


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


@app.delete("/batterypass/{did}")
async def delete_item(
        did: int,
        db: TinyDB = Depends(get_db),
):
    """
    For a given DID, delete the entry from the database.
    :param did: The DID of the entry to delete.
    :param db: Dependency for the database.
    :return: None
    """

    # Search for database entry with the given DID
    document = db.search(where("did") == did)

    # If no entry is found, raise an HTTP exception
    if not document:
        raise HTTPException(status_code=404, detail="Entry doesn't exist.")

    # Delete the entry from the database
    db.remove(where("did") == did)

    # Return a success message indicating the deletion was successful
    return {"ok": f"Entry for {did} deleted successfully."}
