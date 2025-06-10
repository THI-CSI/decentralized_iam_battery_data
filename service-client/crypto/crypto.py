import functools
import json
import pathlib
import logging
import base64
import json
from typing import Union
import os

import requests
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Protocol import HPKE
from Crypto.Protocol.DH import key_agreement
from Crypto.Protocol.KDF import HKDF
from Crypto.Signature import DSS, pkcs1_15 
from Crypto.PublicKey import ECC
from typing import Dict, Any
from Crypto.Hash import SHA3_256
from multiformats import multibase


def base64url_encode(data: bytes) -> str:
    """Encodes data using the base64url URL-safe alphabet."""
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode('ascii')

import json
import base64
from Crypto.Hash import SHA256
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS

# Helper function for base64url encoding, assuming it's not available elsewhere
def base64url_encode(data: bytes) -> str:
    """Encodes data in base64url format."""
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode('ascii')

def _sign_json_ld(obj: dict, private_key: ECC.EccKey, verification_method: str) -> dict:
    """
    Signs a JSON-LD object and produces a full, three-part JWS compact serialization.

    The payload of the JWS is the canonicalized input object, including the 'proof'
    block but with the 'jws' field removed. This is the standard for suites like
    JsonWebSignature2020. The signature is then placed inside the 'proof.jws' field.

    Args:
        obj (dict): The JSON-LD object, must include a 'proof' object shell.
        private_key (ECC.EccKey): The private key for signing.
        verification_method (str): DID URI for the verification method. It will be
                                   used for the 'kid' in the JWS header and the
                                   'verificationMethod' in the final proof.

    Returns:
        dict: The signed JSON-LD object with 'proof.jws' and 'verificationMethod'.
    """
    # 1. Create a deep copy of the object to prepare the payload.
    # This copy will include the proof metadata but not the signature itself.
    obj_to_sign = json.loads(json.dumps(obj))

    # 2. Prepare the proof block for signing. It must include all metadata
    # that needs to be integrity-protected.
    if 'proof' not in obj_to_sign:
        # Ensure a proof block exists if it was omitted.
        obj_to_sign['proof'] = {}
    
    # Add the verificationMethod to the proof to be signed. This ensures
    # the link to the key is also part of the signed data.
    obj_to_sign['proof']['verificationMethod'] = verification_method

    # The 'jws' field is where the signature will go, so it must be
    # removed from the data being signed.
    if 'jws' in obj_to_sign['proof']:
        del obj_to_sign['proof']['jws']

    # 3. Determine the JWS algorithm and create the JWS Header
    header = {
        "alg": "ES256",
        "kid": verification_method
    }
    signer = DSS.new(private_key, 'fips-186-3', 'binary')
   
    # 4. Create the JWS parts: Header and Payload
    encoded_header = base64url_encode(
        json.dumps(header, separators=(',', ':'), sort_keys=True).encode('utf-8')
    )
    
    # The payload is the canonicalized version of the object *with* the
    # proof metadata but *without* the jws field.
    canonical_payload = json.dumps(
        obj_to_sign, separators=(',', ':'), sort_keys=True
    ).encode('utf-8')
    
    encoded_payload = base64url_encode(canonical_payload)

    # 5. Create the signing input and sign it
    # The signing input is ASCII(BASE64URL(UTF8(JWS Protected Header)) || '.' || BASE64URL(JWS Payload))
    signing_input = f"{encoded_header}.{encoded_payload}".encode('ascii')
    hash_obj = SHA256.new(signing_input)
    signature = signer.sign(hash_obj)
    
    # 6. Encode the signature
    encoded_signature = base64url_encode(signature)

    # 7. Assemble the final JWS
    jws = f"{encoded_header}.{encoded_payload}.{encoded_signature}"
    
    # 8. Add the JWS and verificationMethod to the *original* object's proof.
    # We modify the original object, which is a common pattern for this operation.
    obj['proof']['jws'] = jws
    obj['proof']['verificationMethod'] = verification_method

    return obj

def sign_vc(vc: dict, private_key: ECC.EccKey, verification_method: str) -> dict:
    """Signs a Verifiable Credential."""
    return _sign_json_ld(vc, private_key, verification_method)

def sign_vp(vp: dict, private_key: ECC.EccKey, verification_method: str) -> dict:
    """Signs a Verifiable Presentation."""
    return _sign_json_ld(vp, private_key, verification_method)

def sign_did(did: dict, private_key: ECC.EccKey, verification_method: str) -> dict:
    """Signs a DID Document."""
    return _sign_json_ld(did, private_key, verification_method)

def sign_payload(payload: dict, private_key: ECC.EccKey) -> bytes:

    # Prepare a copy of payload to sign, excluding the proof.jws field
    payload_copy = json.loads(json.dumps(payload))  # Deep copy
    if 'signature' in payload_copy.get('signature', {}):
        del payload_copy['payload']

    # Serialize with sorted keys, no whitespace (canonical-like)
    serialized_payload = json.dumps(payload_copy, separators=(',', ':'), sort_keys=True).encode('utf-8')

    # Create hash of the serialized payload
    hash_obj = SHA256.new(serialized_payload)

    # Create signer with FIPS 186-3 DER encoding (matches your verifier)
    signer = DSS.new(private_key, 'fips-186-3')

    # Generate signature (DER encoded)
    signature_der = signer.sign(hash_obj)

    # Base64 encode signature (standard base64)
    signature_b64 = base64.b64encode(signature_der).decode('ascii')

    # Update payload proof with signature and verification method
    payload['signature'] = signature_b64
    

    return payload


def decrypt_hpke(private_key: ECC.EccKey, bundle: dict) -> bytes:
    enc = base64.b64decode(bundle["enc"])
    ciphertext = base64.b64decode(bundle["ciphertext"])
    decapsulator = HPKE.new(enc=enc, aead_id=HPKE.AEAD.AES256_GCM, receiver_key=private_key)
    return decapsulator.unseal(ciphertext)


def encrypt_hpke(private_key: ECC.EccKey, message: bytes) -> dict:
    encapsulator = HPKE.new(receiver_key=private_key.public_key(), aead_id=HPKE.AEAD.AES256_GCM)
    ciphertext = encapsulator.seal(message)
    enc = encapsulator.enc
    return {
        "enc": base64.b64encode(enc).decode(),
        "ciphertext": base64.b64encode(ciphertext).decode()
    }

def generate_keys(password: str, name: str  = "key") -> None:
    # TODO: Generate key pair once and register with blockchain
    keys_dir = pathlib.Path(__file__).parent.parent / "keys"
    key_name = f"{name}.pem"
    #print(f"Generating keys in {keys_dir}")
    keys_dir.mkdir(exist_ok=True)
    if not (keys_dir / key_name).is_file():
        key = ECC.generate(curve="P-256")
        export_private_key(key, password, keys_dir, key_name)
        logging.info(f"Generated {keys_dir / key_name}")


def export_private_key(key: ECC.EccKey, passphrase: str, keys_dir: pathlib.Path, name: str = "key.pem") -> None:
    private_key_pem = key.export_key(
        format="PEM",
        passphrase=passphrase,
        protection="PBKDF2WithHMAC-SHA512AndAES256-CBC",
        prot_params={"iteration_count": 131072}
    )
    key_file_path = keys_dir / f"{name}"
    with open(key_file_path, "w") as f:
        f.write(private_key_pem)
    key_file_path.chmod(0o600)

def get_public_key(keys_dir: pathlib.Path, passphrase: str,name: str = "key.pem") -> str:
    private_key_path = keys_dir / f"{name}.pem"

    if not private_key_path.is_file():
        raise FileNotFoundError(f"Private key {private_key_path} not found.")

    with open(private_key_path, "rt") as f:
        private_key_pem = f.read()

    private_key = ECC.import_key(private_key_pem, passphrase=passphrase)
    public_key = private_key.public_key()
    return public_key.export_key(format="PEM")


def load_private_key(passphrase: str, name: str = "key") -> ECC.EccKey:
    pem_file = pathlib.Path(__file__).parent.parent / "keys" / f"{name}.pem"
    assert pem_file.is_file()
    with open(pem_file, "r") as f:
        return ECC.import_key(f.read(), passphrase=passphrase)


def extract_vc_info(vc: Dict[str, Any]) -> tuple[str, str, str]:
    """
    Extract URI, issuer, and holder from a VC object.

    :param vc: The Verifiable Credential (VC) as a dictionary.
    :return: A tuple containing (URI, Issuer ID, Holder ID).
    """

    # Get all necessary data from the verifiable credential
    uri = vc.get("id")
    issuer = vc.get("issuer")
    subject = vc.get("credentialSubject")

    # Checking credentialSubjects form (If we have a uniform form, this is not necessary,
    # but will be left in for now)
    if isinstance(subject, dict):
        holder = subject.get("id")
    elif isinstance(subject, list) and len(subject) > 0:
        holder = subject[0].get("id")
    else:
        holder = None

    # Check if all data is present, if not raise a ValueError
    if uri is None or issuer is None or holder is None:
        raise ValueError("Invalid Verifiable Credential")

    return uri, issuer, holder


def verify_vc(vc_json_object: json) -> bool:
    """
    This function takes a Verifiable Credential dictionary, extracts the URI, issuer id, and holder id, and
    creates a 256-bit SHA-3 hash of the whole VC. The Data is then send to the blockchain to be verified.
    """

    # Extract the uri, issuer and holder
    uri, issuer, holder = extract_vc_info(vc_json_object)

    # To generate the Hash, we must first serialize the Object
    serialized_vc = json.dumps(vc_json_object, separators=(',', ':'), sort_keys=True).encode('utf-8')

    # Create the SHA3-256bit Hash
    vc_hash = SHA3_256.new(serialized_vc)

    # devbod: TODO: Should we use hexdigest()?
    # vc_digest = vc_hash.hexdigest()

    # Now we need to send the Data to the Blockchain
    # First we create the Datastructures we send
    data = {
        "uri": uri,
        "issuer": issuer,
        "holder": holder,
        "hash": vc_hash
    }

    # Then we send the Data to the Blockchain
    response = requests.post(BLOCKCHAIN_URL, json=data)

    # If the response is 200, we can assume the VC is valid
    if response.status_code == 200:
        return True
    # If not, we can assume the VC is invalid. We should check for reasons in the future
    # devbod: TODO: Check for Reasons
    else:
        return False

def single_line_to_pem(single_line_key, key_type="PRIVATE KEY"):
    """Converts a single-line Base64 string back to a standard PEM format."""
    pem_lines = [single_line_key[i:i+64] for i in range(0, len(single_line_key), 64)]
    reconstructed_pem = (
        f"-----BEGIN {key_type}-----\n"
        + "\n".join(pem_lines) + "\n"
        + f"-----END {key_type}-----\n"
    )
    return reconstructed_pem

def pem_to_single_line(pem_string):
    """
    Converts a standard multi-line PEM string to a single-line Base64 string.
    """
    print("--- 2. Converting PEM to Single Line ---")
    lines = pem_string.strip().split('\n')
    # Filter out the header and footer lines
    b64_lines = [line for line in lines if not line.startswith('-----')]
    single_line_key = "".join(b64_lines)
    
    print("Resulting single-line key:")
    print(single_line_key)
    print("\nThis format is ideal for environment variables or JSON configs.\n")
    return single_line_key