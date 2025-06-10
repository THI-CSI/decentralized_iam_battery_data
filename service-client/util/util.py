import uuid
import requests
import json
import os
from datetime import datetime, timedelta, timezone

def create_service_access_vc(
    issuer_did: str,
    holder_did: str,
    bms_did: str,
    access_levels: list,
    valid_from: datetime,
    valid_until: datetime,
    proof: dict = None
) -> dict:
    # Remove microseconds and format as ISO 8601 with 'Z'
    issuance_date = valid_from.replace(microsecond=0).strftime("%Y-%m-%dT%H:%M:%SZ")
    expiration_date = valid_until.replace(microsecond=0).strftime("%Y-%m-%dT%H:%M:%SZ")
   
    vc_id = f"urn:uuid:{uuid.uuid4()}"
    credential_subject_id = f"{vc_id}#serviceAccess"

    vc = {
        "@context": [
            "https://www.w3.org/2018/credentials/v1",
            "http://localhost:8443/docs/vc.schema.html"
        ],
        "id": vc_id,
        "type": ["VerifiableCredential", "ServiceAccess"],
        "issuer": issuer_did,
        "holder": holder_did,
        "issuanceDate": issuance_date,
        "expirationDate": expiration_date,
        "credentialSubject": {
            "id": credential_subject_id,
            "type": "ServiceAccess",
            "bmsDid": bms_did,
            "accessLevel": access_levels,
            "validFrom": valid_from,
            "validUntil": expiration_date
        },
        "proof": proof or {
            "type": "EcdsaSecp256r1Signature2019",
            "created": issuance_date,
            "verificationMethod": f"{issuer_did}#key-1",
            "proofPurpose": "authentication",
            "jws": "TODO"  # Placeholder, replace with actual signature
        }
    }

    return vc

def make_vp_from_vc(vc: dict, holder_did: str, proof: dict = None) -> dict:
    """
    Creates a Verifiable Presentation (VP) from a Verifiable Credential (VC).
    """
    vp_id = f"urn:uuid:{uuid.uuid4()}"
    now = datetime.now().replace(microsecond=0).strftime("%Y-%m-%dT%H:%M:%SZ")
    # TODO 
    vp = {
        "@context": [
            "https://www.w3.org/2018/credentials/v1",
            "http://localhost:8443/docs/vp.schema.html"
        ],
        "type": ["VerifiablePresentation"],
        "holder": holder_did,
        "verifiableCredential": [vc],
        "proof": proof or {
            "type": "EcdsaSecp256r1Signature2019",
            "created": now,
            "verificationMethod": f"{holder_did}#key-1",
            "challenge": "c82f7883-42a1-4b78-9c2e-d8d5321af9f8", # Hardcoded for now
            "proofPurpose": "authentication",
            "jws": "TODO"  # Placeholder, replace with actual signature
        }
    }

    return vp

def build_did_document(did: str, controller: str, multibase_key: str, bms: bool = False) -> dict:
    timestamp = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')
    verification_method = {
        "id": f"{did}#key-1",
        "type": "JsonWebKey2020",  # or Ed25519VerificationKey2020 if using Ed25519
        "controller": controller,
        "publicKeyMultibase": multibase_key
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
            "challenge": str(uuid.uuid4()),  # Random challenge for proof
            "verificationMethod": f"", # Assuming key identifier format
            "proofPurpose": "authentication",
            "jws": "eyJhbGciOiJFUzI1NiJ9..BASE64_SIG_PLACEHOLDER_NEEDS_REAL_SIGNATURE" # Placeholder
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

def upload_vc_to_blockchain(vc: dict) -> bool:
    print(f"Uploading VC to Blockchain: {json.dumps(vc, indent=2)}")
    response = requests.post(f"{os.getenv('BLOCKCHAIN_URL', 'http://localhost:8443')}/api/v1/vcs/create", headers={'Content-type': 'application/json'}, json=vc)
    return response.status_code == 200