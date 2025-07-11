import uuid
import requests
import json
import os
from datetime import datetime, timedelta, timezone
import base58
from Crypto.PublicKey import ECC
import pathlib
from jwcrypto import jwk, jws
from jwcrypto.common import json_encode

MULTICODEC_PREFIXES = {
    'p256': b'\x12\x00',
}


def ecc_public_key_to_multibase(ecc_key):
    """
    Converts a PyCryptodome ECC public key to a multibase Base58BTC string
    with a multicodec prefix (P-256 only)
    """
    if not isinstance(ecc_key, ECC.EccKey):
        raise TypeError("Expected PyCryptodome EccKey")

    if ecc_key.curve not in ['P-256', 'NIST P-256']:
        raise ValueError("Only P-256 curve supported")

    # Get x and y bytes (32 bytes each)
    x_bytes = int(ecc_key.pointQ.x).to_bytes(32, byteorder='big')
    y_bytes = int(ecc_key.pointQ.y).to_bytes(32, byteorder='big')

    # Uncompressed point format: 0x04 + X + Y
    uncompressed_point = b'\x04' + x_bytes + y_bytes

    # Multicodec prefix + raw key bytes
    multicodec_bytes = MULTICODEC_PREFIXES['p256'] + uncompressed_point

    # Base58BTC multibase encode
    multibase = 'z' + base58.b58encode(multicodec_bytes).decode()

    return multibase


def _format_datetime(dt: datetime) -> str:
    """Formats a datetime object to ISO 8601 UTC format (YYYY-MM-DDTHH:MM:SSZ)."""
    # Ensure datetime is timezone-aware (assuming UTC if not) before formatting.
    if dt.tzinfo is None:
        dt = dt.astimezone(timezone.utc)
    return dt.replace(microsecond=0).isoformat().replace('+00:00', 'Z')


def create_service_access_vc(
        issuer_did: str,
        holder_did: str,
        bms_did: str,
        access_levels: list,
        valid_from: datetime,
        valid_until: datetime,
        proof: dict = None
) -> dict:
    issuance_date = _format_datetime(valid_from)
    expiration_date = _format_datetime(valid_until)

    vc_id = f"urn:uuid:{uuid.uuid4()}"
    credential_subject_id = holder_did

    vc = {
        "@context": [
            "https://www.w3.org/2018/credentials/v1",
            "http://localhost:8443/docs/vc.serviceAccess.schema.html"
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
            "validFrom": issuance_date,
            "validUntil": expiration_date
        },
        "proof": proof or {
            "type": "EcdsaSecp256r1Signature2019",
            "created": issuance_date,
            "verificationMethod": f"{issuer_did}#key-1",
            "proofPurpose": "authentication",
            "jws": ""  # Placeholder, replace with actual signature
        }
    }

    return vc


def make_vp_from_vc(vc: dict, holder_did: str, proof: dict = None) -> dict:
    """
    Creates a Verifiable Presentation (VP) from a Verifiable Credential (VC).
    """
    now_formatted = _format_datetime(datetime.now(timezone.utc))

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
            "created": now_formatted,
            "verificationMethod": f"{holder_did}#key-1",
            "challenge": "c82f7883-42a1-4b78-9c2e-d8d5321af9f8",  # Hardcoded for now
            "proofPurpose": "authentication",
            "jws": ""  # Placeholder, replace with actual signature
        }
    }

    return vp


def build_did_document(did: str, controller: str, public_key_multibase: str) -> dict:
    timestamp = _format_datetime(datetime.now(timezone.utc))
    verification_method = {
        "id": f"{did}#key-1",
        "type": "JsonWebKey2020",  # or Ed25519VerificationKey2020 if using Ed25519
        "controller": controller,
        "publicKeyMultibase": public_key_multibase
    }
    ServiceEndpoint = [
        {
            "id": f"{did}#Api-Endpoint",
            "type": "ApiEndpoint",
            "serviceEndpoint": f"http://api-service:8000" # API Service Endpoint URL
        }
    ]

    did_doc = {
        "proof": {
            "type": "EcdsaSecp256r1Signature2019",
            "created": timestamp,
            "challenge": str(uuid.uuid4()),  # Random challenge for proof
            "verificationMethod": f"{did}#key-1",  # This will be filled by the signing function
            "proofPurpose": "authentication",
            "jws": ""  # Placeholder
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
    response = requests.post(f"{os.getenv("BLOCKCHAIN_URL", "http://localhost:8443")}/api/v1/dids/createormodify",
                             headers={'Content-type': 'application/json'}, json=payload)
    return response.status_code == 200


def upload_vc_to_blockchain(vc: dict) -> bool:
    print(f"Uploading VC to Blockchain: {json.dumps(vc, indent=2)}")
    response = requests.post(f"{os.getenv('BLOCKCHAIN_URL', 'http://localhost:8443')}/api/v1/vcs/create",
                             headers={'Content-type': 'application/json'}, json=vc)
    return response.status_code == 200


# Crypto

def sign_json_payload(payload_dict, ecc_key):
    # Serialize payload to a compact JSON string
    payload = json.dumps(payload_dict, separators=(',', ':'))

    # Export the ECC key to PEM format
    pem_key = ecc_key.export_key(format='PEM')

    # Load the key into a jwcrypto JWK
    key = jwk.JWK.from_pem(pem_key.encode())

    # Create and sign the JWS
    signature = jws.JWS(payload.encode('utf-8'))
    signature.add_signature(key, alg='ES256', protected=json_encode({"alg": "ES256"}))

    # Return compact JWS format
    return signature.serialize(compact=True)

def attach_proof_jws(obj: dict, jws_token: str, verification_method: str) -> dict:
    """Adds the JWS signature to the object's proof.jws field."""
    if 'proof' not in obj:
        obj['proof'] = {}
    obj['proof']['jws'] = jws_token
    obj['proof']['verificationMethod'] = verification_method
    return obj

def sign_did(did: dict, private_key: ECC.EccKey, verification_method: str) -> dict:
    """Signs a DID Document."""
    jws_token = sign_json_payload(did, private_key)
    return attach_proof_jws(did, jws_token, verification_method)

def export_pem(key: ECC.EccKey, keys_dir: pathlib.Path, name: str = "key.pem") -> None:
    pem_key = key.export_key(format="PEM")
    key_file_path = keys_dir / name
    with open(key_file_path, "w") as f:
        f.write(pem_key)
    key_file_path.chmod(0o600)

def export_private_key(key: ECC.EccKey, passphrase: str, keys_dir: pathlib.Path, name: str = "key.der") -> None:
    private_key_der = key.export_key(
        format="DER",
        passphrase=passphrase,
        protection="scryptAndAES256-CBC"
    )
    key_file_path = keys_dir / name
    with open(key_file_path, "wb") as f:
        f.write(private_key_der)
    key_file_path.chmod(0o600)
