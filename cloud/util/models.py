from datetime import datetime
from typing import Annotated

from fastapi.params import Query
from pydantic import BaseModel, Field, StringConstraints

DID_PATTERN = r"^did:batterypass:(oem|cloud|bms|service|user)\.[a-zA-Z0-9][a-zA-Z0-9-]+$"
URN_PATTERN = (
    r"^urn:uuid:("
    r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"
    r"|"
    r"[0-9A-F]{8}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{12}"
    r")$"
)
BASE64_PATTERN = r"^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?$"

DID = Annotated[
    str,
    StringConstraints(pattern=DID_PATTERN)
]
URN = Annotated[
    str,
    StringConstraints(pattern=URN_PATTERN)
]


def Base64String(length=None):
    return Annotated[
        str,
        StringConstraints(pattern=BASE64_PATTERN, min_length=length, max_length=length)
    ]


bms_example = "did:batterypass:bms.sn-987654321"
service_example = "did:batterypass:service.tuv-sued-42"


def get_encrypted_payload(
        ciphertext: Annotated[Base64String, Query(description="The payload inside the ciphertext must be a "
                                                              "**128-byte random number**.")] = None,
        aad: Annotated[Base64String, Query()] = None,
        salt: Annotated[Base64String, Query()] = None,
        eph_pub: Annotated[Base64String, Query()] = None,
        sender_did: Annotated[DID, Query()] = None,
        signature: Annotated[Base64String, Query()] = None,
):
    if not (
            ciphertext and aad and salt and eph_pub and sender_did and signature
    ):
        return None
    return EncryptedPayload(
        ciphertext=ciphertext,
        aad=aad,
        salt=salt,
        eph_pub=eph_pub,
        sender_did=sender_did,
        signature=signature
    )


class CredentialSubject(BaseModel):
    id: DID
    type: str
    bmsDid: DID
    accessLevel: list[str]
    validFrom: str
    validUntil: str


class Proof(BaseModel):
    type: str
    created: str
    verificationMethod: str
    proofPurpose: str
    jws: str


class VerifiableCredential(BaseModel):
    at_context: list[str] = Field(alias="@context")
    id: URN
    type: list[str]
    issuer: DID
    holder: DID
    issuanceDate: str
    expirationDate: str
    credentialSubject: CredentialSubject


class VerifiablePresentation(BaseModel):
    at_context: list[str] = Field(alias="@context")
    type: list[str]
    vc: list[VerifiableCredential] = Field(alias="verifiableCredential")
    holder: DID
    proof: Proof


class EncryptedPayload(BaseModel):
    ciphertext: Base64String()
    aad: Base64String(length=16)
    salt: Base64String(length=44)
    eph_pub: Base64String(length=124)
    did: DID
    signature: Base64String()


class SuccessfulResponse(BaseModel):
    ok: str


class ErrorResponse(BaseModel):
    status: int
    message: str
    timestamp: str = Field(examples=[datetime.now().isoformat()])


class BadRequestResponse(ErrorResponse):
    status: int = 400
    message: str = "Invalid request."


class ForbiddenResponse(ErrorResponse):
    status: int = 403
    message: str = "Access denied."


class NotFoundResponse(ErrorResponse):
    status: int = 404
    message: str = "Entry doesn't exist."
