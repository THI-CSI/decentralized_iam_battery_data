import functools
import pathlib
import base64
import pathlib
import base58
import json
import os


from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Protocol.DH import key_agreement
from Crypto.Protocol.KDF import HKDF
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS
from Crypto.Hash import SHA256
from Crypto.Math.Numbers import Integer
from jwcrypto import jwk, jws
from jwcrypto.common import json_encode


def sign_payload(payload, ecc_key):
    # Export the ECC key to PEM format
    pem_key = ecc_key.export_key(format='PEM')

    # Load the key into a jwcrypto JWK
    key = jwk.JWK.from_pem(pem_key.encode())

    # Create and sign the JWS
    signature = jws.JWS(payload)
    signature.add_signature(key, alg='ES256', protected=json_encode({"alg": "ES256"}))

    # Return compact JWS format
    return signature.serialize(compact=True)

def attach_proof_signature(obj: dict, signature: str) -> dict:
    """Adds the JWS signature to the object's proof.jws field."""
    if 'signature' not in obj:
        obj['signature'] = ""
    obj['signature'] = base64.b64encode(signature).decode('utf-8')
    return obj

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

def multibase_to_ecc_public_key(public_key_multibase):
    base58_string = public_key_multibase[1:]
    decoded_bytes = base58.b58decode(base58_string)
    multicodec_prefix = decoded_bytes[:2]
    pubkey_bytes = decoded_bytes[2:]
    if pubkey_bytes[0] != 0x04:
        raise ValueError("Expected uncompressed public key to start with 0x04")
    x = pubkey_bytes[1:33]
    y = pubkey_bytes[33:65]
    x_int = int.from_bytes(x, 'big')
    y_int = int.from_bytes(y, 'big')
    return ECC.construct(curve='P-256', point_x=x_int, point_y=y_int)

def generate_keys(name: str = "key") -> None:
    keys_dir = pathlib.Path(__file__).parent / "keys"
    keys_dir.mkdir(exist_ok=True)
    if not (keys_dir / f"{name}.pem").is_file():
        key = ECC.generate(curve="P-256")
        export_pem(key, keys_dir, f"{name}.pem")

def export_pem(key: ECC.EccKey, keys_dir: pathlib.Path, name: str = "key.pem") -> None:
    pem_key = key.export_key(format="PEM")
    key_file_path = keys_dir / name
    with open(key_file_path, "w") as f:
        f.write(pem_key)
    key_file_path.chmod(0o600)


def load_private_key_as_der(name: str = "key") -> ECC.EccKey:
    key_file = pathlib.Path(__file__).parent / "keys" / f"{name}.pem"

    assert key_file.is_file(), f"Key file not found: {key_file}"
    key = None
    with open(key_file, "rt") as f:
        key = ECC.import_key(f.read())

    return key

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