import json
from fastapi import HTTPException

from crypto.crypto import decrypt_and_verify
from Crypto.PublicKey import ECC
from util.models import EncryptedPayload


def verify_request(item: EncryptedPayload, private_key: ECC.EccKey) -> dict:
    try:
        decrypted_bytes = decrypt_and_verify(
            private_key,
            item.model_dump()
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Failed decryption or signature verification.")
    try:
        return json.loads(decrypted_bytes.decode("utf-8"))
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Failed decoding decrypted data to JSON.")
