import functools
import json
import pathlib
import logging
import base64
import base58
import os
from typing import Union, Dict, Any

from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Protocol import HPKE
from Crypto.Protocol.DH import key_agreement
from Crypto.Protocol.KDF import HKDF
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS
from datetime import datetime, timezone

# --- jwcrypto imports for robust JWS signing ---
from jwcrypto import jwk, jws
from jwcrypto.common import json_encode

import requests
from multiformats import multibase


BLOCKCHAIN_URL = os.getenv("BLOCKCHAIN_URL", "http://localhost:8443")

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

def sign_vc_external(vc: dict,  verification_method: str) -> dict:
    """Signs a VC Document."""
    private_key = load_private_key_as_der("oem_key")
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
    private_key = load_private_key_as_der("oem_key")
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
        "did": did
    }
    return payload

def generate_keys(name: str  = "key") -> None:
    keys_dir = pathlib.Path(__file__).parent.parent / "keys"
    keys_dir.mkdir(exist_ok=True)
    if not (keys_dir /  f"{name}.pem").is_file():
        key = ECC.generate(curve="P-256")
        #export_private_key(key, password, keys_dir,  f"{name}.der")
        export_pem(key, keys_dir,  f"{name}.pem")

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

def load_private_key_as_der(name: str = "key") -> bytes:
    key_file = pathlib.Path(__file__).parent.parent / "keys" / f"{name}.pem"

    assert key_file.is_file(), f"Key file not found: {key_file}"
    key = None
    with open(key_file, "rt") as f:
        key = ECC.import_key(f.read())

    return key

def multibase_to_ecc_public_key(public_key_multibase):
    base58_string = public_key_multibase[1:]  # Remove 'z'

    decoded_bytes = base58.b58decode(base58_string)

    # Remove 2-byte multicodec prefix
    multicodec_prefix = decoded_bytes[:2]

    pubkey_bytes = decoded_bytes[2:]  # This is 65 bytes, expected uncompressed key format

    if pubkey_bytes[0] != 0x04:
        raise ValueError("Expected uncompressed public key to start with 0x04")

    x = pubkey_bytes[1:33]
    y = pubkey_bytes[33:65]

    x_int = int.from_bytes(x, 'big')
    y_int = int.from_bytes(y, 'big')
    return ECC.construct(curve='P-256', point_x=x_int, point_y=y_int)


def attach_proof_signature(obj: dict, signature: str) -> dict:
    """Adds the JWS signature to the object's proof.jws field."""
    if 'signature' not in obj:
        obj['signature'] = ""
    obj['signature'] = base64.b64encode(signature).decode('utf-8')
    return obj




def encrypt_data_from_did(bms_did: str, publicKeyMultibase: str, battery_data: str, private_key: ECC.EccKey):
    public_key = multibase_to_ecc_public_key(publicKeyMultibase) # ECC Key
    encrypted_data = encrypt_hpke(bms_did, public_key, battery_data.encode('utf-8'))
    message_to_verify = json.dumps(
        {key: value for key, value in encrypted_data.items() if key != "signature"}, separators=(",", ":")
    ).encode()
    hashed_data = SHA256.new(message_to_verify)
    signature = DSS.new(private_key, 'fips-186-3').sign(hashed_data)
    signed_payload = attach_proof_signature(encrypted_data, signature)

    return signed_payload

def retrieve_public_key(did: str) -> ECC.EccKey:
    response = requests.get(f"{BLOCKCHAIN_URL}/api/v1/dids/{did}")
    raw = multibase.decode(response.json()["verificationMethod"]["publicKeyMultibase"])
    if len(raw) == 67:
        raw = raw[len(b"\x12\x00"):]
        return ECC.EccKey(curve="P-256",
                          point=ECC.EccPoint(
                              int.from_bytes(raw[1:33], "big"), int.from_bytes(raw[33:65], "big"))
                          )
    if response.json()["revoked"]:
        raise ValueError("Public key revoked.")
    return ECC.import_key(multibase.decode(response.json()["verificationMethod"]["publicKeyMultibase"]))


def decrypt_and_verify(receiver_key: ECC.EccKey, message_str: str) -> bytes:
    message = json.loads(message_str)
    fields_to_decode = ["ciphertext", "aad", "salt", "signature", "eph_pub"]
    decoded_message = {key: base64.b64decode(value) for key, value in message.items() if key in fields_to_decode}
    eph_pub_der = decoded_message["eph_pub"]
    eph_pub = ECC.import_key(eph_pub_der)
    nonce = decoded_message["aad"]
    ciphertext = decoded_message["ciphertext"]
    salt = decoded_message["salt"]
    signature = decoded_message["signature"]
    ciphertext_data = ciphertext[:-16]
    tag = ciphertext[-16:]
    context = eph_pub_der + receiver_key.public_key().export_key(format="DER")
    did = message["did"]
    # Verify signature
    sender_key = retrieve_public_key(did)
    verifier = DSS.new(sender_key, mode="fips-186-3", encoding="binary")
    message_to_verify = json.dumps(
        {key: value for key, value in message.items() if key != "signature"}, separators=(",", ":")
    ).encode()
    try:
        verifier.verify(SHA256.new(message_to_verify), signature)
    except ValueError:
        print("Failed decryption due to invalid signature.")
        raise ValueError("Failed decryption due to invalid signature.")
    # Decrypt message
    hkdf = functools.partial(HKDF, key_len=32, hashmod=SHA256, salt=salt, context=context)
    aes_key = key_agreement(eph_pub=eph_pub, static_priv=receiver_key, kdf=hkdf)
    cipher = AES.new(aes_key, AES.MODE_GCM, nonce=nonce)
    cipher.update(nonce)
    try:
        plaintext = cipher.decrypt_and_verify(ciphertext_data, tag)
        return plaintext
    except ValueError:
        print("Failed decryption due to invalid MAC tag.")
        raise ValueError("Failed decryption due to invalid MAC tag.")