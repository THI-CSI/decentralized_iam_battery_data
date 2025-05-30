from fastapi import HTTPException
from crypto.crypto import decrypt_and_verify
from Crypto.PublicKey import ECC
from util.models import EncryptedPayload


def verify_request(item: EncryptedPayload, private_key: ECC.EccKey) -> bytes:
    return decrypt_and_verify(private_key, item.model_dump())
