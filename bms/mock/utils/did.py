import uuid
from datetime import datetime, timezone

def _format_datetime(dt: datetime) -> str:
    """Formats a datetime object to ISO 8601 UTC format (YYYY-MM-DDTHH:MM:SSZ)."""
    # Ensure datetime is timezone-aware (assuming UTC if not) before formatting.
    if dt.tzinfo is None:
        dt = dt.astimezone(timezone.utc)
    return dt.replace(microsecond=0).isoformat().replace('+00:00', 'Z')

def create_cloud_instance_vc(
    issuer_did: str,
    holder_did: str,
    cloud_did: str,
    valid_from: datetime,
    valid_until: datetime,
    proof: dict = None
) -> dict:
    issuance_date = _format_datetime(valid_from)
    expiration_date = _format_datetime(valid_until)

    vc_id = f"urn:uuid:{uuid.uuid4()}"

    vc = {
        "@context": [
            "https://www.w3.org/2018/credentials/v1",
            "http://localhost:8443/docs/vc.cloudInstance.schema.html"
        ],
        "id": vc_id,
        "type": [
            "VerifiableCredential",
            "CloudInstance"
        ],
        "issuer": issuer_did,
        "holder": holder_did,
        "issuanceDate": issuance_date,
        "expirationDate": expiration_date,
        "credentialSubject": {
            "id": holder_did,
            "type": "CloudInstance",
            "cloudDid": cloud_did,
            "timestamp": issuance_date
        },
        "proof": proof or {
            "type": "EcdsaSecp256r1Signature2019",
            "created": issuance_date,
            "verificationMethod": f"{issuer_did}#key-1",
            "proofPurpose": "authentication",
            "jws": ""
        }
    }
    return vc

def build_did_document(did: str, controller: str, public_key_multibase: str) -> dict:
    timestamp = _format_datetime(datetime.now(timezone.utc))
    verification_method = {
        "id": f"{did}#key-1",
        "type": "JsonWebKey2020",  # or Ed25519VerificationKey2020 if using Ed25519
        "controller": controller,
        "publicKeyMultibase": public_key_multibase
    }


    did_doc = {
        "proof": {
            "type": "EcdsaSecp256r1Signature2019",
            "created": timestamp,
            "challenge": str(uuid.uuid4()),  # Random challenge for proof
            "verificationMethod": f"{did}#key-1", # This will be filled by the signing function
            "proofPurpose": "authentication",
            "jws": "" # Placeholder
        },
        "payload": {
            "@context": [
                "https://www.w3.org/2018/credentials/v1",
                "http://localhost:8443/docs/did.schema.html"
            ],
            "id": did,
            "verificationMethod": verification_method,
            "timestamp": timestamp,
            "revoked": False
        }
    }


    return did_doc