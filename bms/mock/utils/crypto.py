import functools
import pathlib
import base64
import pathlib
import base58
import os


from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Protocol.DH import key_agreement
from Crypto.Protocol.KDF import HKDF
from Crypto.PublicKey import ECC

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

def generate_keys(name: str = "key") -> None:
    keys_dir = pathlib.Path(__file__).parent / "keys"
    keys_dir.mkdir(exist_ok=True)
    if not (keys_dir / f"{name}.der").is_file():
        key = ECC.generate(curve="P-256")
        export_private_key(key, keys_dir, f"{name}.der")
        export_pem(key, keys_dir, f"{name}.pem")

def export_pem(key: ECC.EccKey, keys_dir: pathlib.Path, name: str = "key.pem") -> None:
    pem_key = key.export_key(format="PEM")
    key_file_path = keys_dir / name
    with open(key_file_path, "w") as f:
        f.write(pem_key)
    key_file_path.chmod(0o600)


def export_private_key(key: ECC.EccKey, keys_dir: pathlib.Path, name: str = "key.der") -> None:
    private_key_der = key.export_key(format="DER")
    key_file_path = keys_dir / name
    with open(key_file_path, "wb") as f:
        f.write(private_key_der)
    key_file_path.chmod(0o600)

def load_private_key(name: str = "key.der") -> ECC.EccKey:
    key_file = pathlib.Path(__file__).parent / "keys" / f"{name}"
    assert key_file.is_file()
    with open(key_file, "rb") as f:
        return ECC.import_key(f.read())
    
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