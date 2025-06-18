from datetime import datetime, timezone
from uuid import uuid4

def _format_datetime(dt: datetime) -> str:
    """Formats a datetime object to ISO 8601 UTC format (YYYY-MM-DDTHH:MM:SSZ)."""
    # Ensure datetime is timezone-aware (assuming UTC if not) before formatting.
    if dt.tzinfo is None:
        dt = dt.astimezone(timezone.utc)
    return dt.replace(microsecond=0).isoformat().replace('+00:00', 'Z')

def build_did_document(did: str, controller: str, public_key_multibase: str, bms: bool = False) -> dict:
    timestamp = _format_datetime(datetime.now(timezone.utc))
    verification_method = {
        "id": f"{did}#key-1",
        "type": "JsonWebKey2020",  # or Ed25519VerificationKey2020 if using Ed25519
        "controller": controller,
        "publicKeyMultibase": public_key_multibase
    }
    ServiceEndpoint = None
    if bms:
        ServiceEndpoint = [
            {
                "id": f"{did}#batterypassApi-test1",
                "type": "BatteryPassAPI",
                "serviceEndpoint": f"http://localhost:8443"
            }
        ]


    did_doc = {
        "proof": {
            "type": "EcdsaSecp256r1Signature2019",
            "created": timestamp,
            "challenge": str(uuid4()),  # Random challenge for proof
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
            "service": ServiceEndpoint,
            "timestamp": timestamp,
            "revoked": False
        }
    }


    return did_doc

def register_key_with_blockchain(payload: dict = None) -> bool:
    response = requests.post(f"{os.getenv("BLOCKCHAIN_URL", "http://localhost:8443")}/api/v1/dids/createormodify", headers={'Content-type': 'application/json'}, json=payload)
    return response.status_code == 200
