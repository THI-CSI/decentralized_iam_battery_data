import uuid
from datetime import datetime, timedelta, timezone

def generate_vc(issuer_did, holder_did, bms_did, access_levels, duration_years):
    """
    Generates a Verifiable Credential based on the provided template and arguments.
    """
    now = datetime.now(timezone.utc)
    issuance_date = now.strftime('%Y-%m-%dT%H:%M:%SZ')
    expiration_date_dt = now + timedelta(days=duration_years * 365.25) # Using 365.25 for better year accuracy
    expiration_date = expiration_date_dt.strftime('%Y-%m-%dT%H:%M:%SZ')
    # Proof creation time can be slightly after issuance
    proof_created_date = (now + timedelta(seconds=5)).strftime('%Y-%m-%dT%H:%M:%SZ')

    vc_id = f"urn:uuid:{uuid.uuid4()}"

    vc = {
      "@context": [
        "https://www.w3.org/2018/credentials/v1",
        "https://batterypass.com/contexts/service-access/v1"
      ],
      "id": vc_id,
      "type": [
        "VerifiableCredential",
        "ServiceAccess"
      ],
      "issuer": issuer_did,
      "holder": holder_did,
      "issuanceDate": issuance_date,
      "expirationDate": expiration_date,
      "credentialSubject": {
        "id": holder_did,
        "type": "ServiceAccess",
        "bmsDid": bms_did,
        "accessLevel": access_levels,
        "validFrom": issuance_date,
        "validUntil": expiration_date
      },
      "proof": {
        "type": "EcdsaSecp256r1Signature2019",
        "created": proof_created_date,
        "verificationMethod": f"{bms_did}#device-key", # Assuming key identifier format
        "proofPurpose": "assertionMethod",
        "jws": "eyJhbGciOiJFUzI1NiJ9..BASE64_SIG_PLACEHOLDER_NEEDS_REAL_SIGNATURE" # Placeholder
      }
    }
    return vc

def create_service_access_vc(
    issuer_did: str,
    holder_did: str,
    bms_did: str,
    access_levels: list,
    valid_from: datetime,
    valid_until: datetime,
    proof: dict = None
) -> dict:
    issuance_date = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    expiration_date = valid_until.replace(microsecond=0).isoformat()

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
            "validFrom": valid_from.replace(microsecond=0).isoformat(),
            "validUntil": expiration_date
        },
        "proof": proof or {
            "type": "EcdsaSecp256r1Signature2019",
            "created": issuance_date,
            "verificationMethod": f"{issuer_did}#key-1",
            "proofPurpose": "assertionMethod",
            "jws": "TODO"  # Placeholder, replace with actual signature
        }
    }

    return vc

def build_did_document(did: str, multibase_key: str, bms: bool = False) -> dict:
    timestamp = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    verification_method = {
        "id": f"{did}#key-1",
        "type": "EcdsaSecp256r1VerificationKey2019",  # or Ed25519VerificationKey2020 if using Ed25519
        "controller": did,
        "publicKeyMultibase": multibase_key.decode() if isinstance(multibase_key, bytes) else multibase_key
    }
    ServiceEndpoint = None
    if bms:
        ServiceEndpoint = {
            "id": f"{did}#service",
            "type": "BMSService",
            "serviceEndpoint": f"http://localhost:8443/bms/{did.split(':')[-1]}"
        }
    
        
    did_doc = {
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
    

    return did_doc