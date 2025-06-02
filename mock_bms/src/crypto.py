from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import base64
import json
from datetime import datetime
import os
import pathlib

def bms_signing_key_pair_generation():
    bms_private_signing_key = ec.generate_private_key(ec.SECP256R1())
    bms_private_signing_key_der = bms_private_signing_key.private_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()  
    )
    keys_dir = pathlib.Path(__file__).parent / "keys"
    keys_dir.mkdir(exist_ok=True)
    key_path = (keys_dir / "bms_private_signing_key.der")
    if not key_path.is_file(): 
        with open(key_path, "wb") as f:
            f.write(bms_private_signing_key_der)
        key_path.chmod(0o600)
    
def writing_did():
    bms_did = "did:example:123456789abcdefgh"
    did_path = (pathlib.Path(__file__).parent / "bms_did")
    if not did_path.is_file(): 
        with open(did_path, "w", encoding="utf-8") as f:
            f.write(bms_did)

def read_key(filename: str):
    keys_dir = pathlib.Path(__file__).parent / "keys"
    key_path = keys_dir / filename
    if key_path.is_file():
        with open(key_path, "rb") as f:
            bms_private_signing_key_der = f.read()
            private_key = serialization.load_der_private_key(
                bms_private_signing_key_der,
                password=None,
            )
            return private_key
    else:
        raise FileNotFoundError("Privater Schlüssel nicht gefunden.")

def read_bms_did():
    did_path = pathlib.Path(__file__).parent / "bms_did"
    if did_path.is_file():
        with open(did_path, "r", encoding="utf-8") as f:
            bms_did = f.read().strip()
            return bms_did
    else:
        raise FileNotFoundError("DID-Datei nicht gefunden.")

def message_creation(dynamic_battery_data: str, cloud_public_key):
    bms_did = read_bms_did()
    bms_private_signing_key = read_key("bms_private_signing_key.der")
    cloud_public_key_der = cloud_public_key.public_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # Generate ECC ephermal key pair and export public key
    private_ephermal_key = ec.generate_private_key(ec.SECP256R1())
    public_ephermal_key = private_ephermal_key.public_key()
    ephermal_public_key_der = public_ephermal_key.public_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # Key aggreement with ECDH
    shared_secret = private_ephermal_key.exchange(ec.ECDH(), cloud_public_key)

    # Key derivation with HKDF(SHA-256)
    info = ephermal_public_key_der + cloud_public_key_der
    salt = os.urandom(32)
    aes_derived_key = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        info=info
    ).derive(shared_secret)

    # AES-GCM 256
    nonce = os.urandom(12)
    associated_data = nonce
    aesgcm = AESGCM(aes_derived_key)
    ciphertext = aesgcm.encrypt(nonce, dynamic_battery_data, associated_data)

    # Get timestamp
    timestamp_bytes = datetime.now().strftime("%Y-%m-%d %H:%M:%S").encode("utf-8")

    # Create message
    ciphertext_b64 = base64.b64encode(ciphertext).decode('utf-8')
    associated_data_b64 = base64.b64encode(associated_data).decode('utf-8')
    salt_b64 = base64.b64encode(salt).decode('utf-8')
    ephermal_public_key_b64 = base64.b64encode(ephermal_public_key_der).decode('utf-8')
    did_b64 = base64.b64encode(bms_did).decode('utf-8')
    timestamp_b64 = base64.b64encode(timestamp_bytes).decode("utf-8")
    message = {
        "ciphertext": ciphertext_b64,
        "aad": associated_data_b64,
        "salt": salt_b64,
        "ephermal_public_key": ephermal_public_key_b64,
        "did": did_b64,
        "timestamp": timestamp_b64
    }
    message_json = json.dumps(message)
    message_bytes = message_json.encode("utf-8")

    # Sign messsage with ECDSA and add to message
    signature = bms_private_signing_key.sign(
        message_bytes,
        ec.ECDSA(hashes.SHA256())
    )
    signature_b64 = base64.b64encode(signature).decode('utf-8')
    message["signature"] = signature_b64
    signed_json_message = json.dumps(message)
    signed_json_message_bytes = signed_json_message.encode("utf-8")
    print(signed_json_message_bytes)

    return signed_json_message_bytes