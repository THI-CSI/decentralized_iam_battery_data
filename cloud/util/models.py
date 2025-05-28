from pydantic import BaseModel


# Pydantic models
class EncryptedPayload(BaseModel):
    ciphertext: str
    aad: str
    salt: str
    eph_pub: str
    did: str
    signature: str
