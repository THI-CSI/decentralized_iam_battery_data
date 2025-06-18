import functools
import json
import pathlib
import logging
import base64
import os
from typing import Union, Dict, Any

from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Protocol import HPKE
from Crypto.Protocol.DH import key_agreement
from Crypto.Protocol.KDF import HKDF
from Crypto.PublicKey import ECC
from datetime import datetime, timezone

# --- jwcrypto imports for robust JWS signing ---
from jwcrypto import jwk, jws
from jwcrypto.common import json_encode


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

def sign_vc(vc: dict, private_key: ECC.EccKey, verification_method: str) -> dict:
    """Signs a Verifiable Credential."""
    jws_token = sign_json_payload(vc, private_key)
    return attach_proof_jws(vc, jws_token, verification_method)

def sign_vp(vp: dict, private_key: ECC.EccKey, verification_method: str) -> dict:
    """Signs a Verifiable Presentation."""
    jws_token = sign_json_payload(vp, private_key)
    return attach_proof_jws(vp, jws_token, verification_method)

def sign_did(did: dict, private_key: ECC.EccKey, verification_method: str) -> dict:
    """Signs a DID Document."""
    jws_token = sign_json_payload(did, private_key)
    return attach_proof_jws(did, jws_token, verification_method)

def sign_did_external(did: dict,  verification_method: str) -> dict:
    """Signs a DID Document."""
    private_key = load_private_key("123","oem_key")
    jws_token = sign_json_payload(did, private_key)
    return attach_proof_jws(did, jws_token, verification_method)


def decrypt_hpke(private_key: ECC.EccKey, bundle: dict) -> bytes:
    enc = base64.b64decode(bundle["enc"])
    ciphertext = base64.b64decode(bundle["ciphertext"])
    decapsulator = HPKE.new(enc=enc, aead_id=HPKE.AEAD.AES256_GCM, receiver_key=private_key)
    return decapsulator.unseal(ciphertext)


def encrypt_hpke(did, receiver_public_key: ECC.EccKey, message: bytes) -> dict:
    eph_key = ECC.generate(curve="P-256")
    salt = os.urandom(32)
    nonce = os.urandom(12)
    eph_pub = eph_key.public_key().export_key(format="DER")
    context = eph_pub + receiver_public_key.export_key(format="DER")
    hkdf = functools.partial(HKDF, key_len=32, hashmod=SHA256, salt=salt, context=context)
    aes_key = key_agreement(eph_priv=eph_key, static_pub=receiver_public_key, kdf=hkdf)
    cipher = AES.new(aes_key, AES.MODE_GCM, nonce=nonce)
    cipher.update(nonce)
    ciphertext, tag = cipher.encrypt_and_digest(message)
    payload = {
        "ciphertext": base64.b64encode(ciphertext + tag).decode(),
        "aad": base64.b64encode(nonce).decode(),
        "salt": base64.b64encode(salt).decode(),
        "eph_pub": base64.b64encode(eph_pub).decode(),
        "did": did,
    }
    return payload

def generate_keys(password: str, name: str  = "key") -> None:
    keys_dir = pathlib.Path(__file__).parent.parent / "keys"
    keys_dir.mkdir(exist_ok=True)
    if not (keys_dir /  f"{name}.der").is_file():
        key = ECC.generate(curve="P-256")
        export_private_key(key, password, keys_dir,  f"{name}.der")
        export_pem(key, keys_dir,  f"{name}.pem")
        logging.info(f"Generated {keys_dir /  f"{name}.der"}")

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
    

def get_public_key(keys_dir: pathlib.Path, passphrase: str, name: str = "key") -> bytes:
    private_key_path = keys_dir / f"{name}.der"

    if not private_key_path.is_file():
        raise FileNotFoundError(f"Private key {private_key_path} not found.")

    with open(private_key_path, "rb") as f:
        private_key_der = f.read()

    private_key = ECC.import_key(private_key_der, passphrase=passphrase)
    public_key = private_key.public_key()
    return public_key.export_key(format="DER")


def load_private_key(passphrase: str, name: str = "key") -> ECC.EccKey:
    key_file = pathlib.Path(__file__).parent.parent / "keys" / f"{name}.der"
    assert key_file.is_file()
    with open(key_file, "rb") as f:
        return ECC.import_key(f.read(), passphrase=passphrase)


