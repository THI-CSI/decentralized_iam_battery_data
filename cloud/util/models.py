from pydantic import BaseModel


# Pydantic models
class EncryptedPayload(BaseModel):
    enc: str
    ciphertext: str
