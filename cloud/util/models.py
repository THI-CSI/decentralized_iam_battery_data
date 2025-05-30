from pydantic import BaseModel


# Pydantic models
class EncryptedPayload(BaseModel):
    enc: str
    ciphertext: str


class SuccessfulResponse(BaseModel):
    ok: str


class ErrorResponse(BaseModel):
    status: int
    message: str
    timestamp: str
