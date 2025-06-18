import pathlib
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from Crypto.PublicKey import ECC
import pathlib
import base58


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


def get_public_key(keys_dir: pathlib.Path, name: str = "key.der") -> bytes:
    private_key_path = keys_dir / f"{name}"
    if not private_key_path.is_file():
        raise FileNotFoundError(f"Private key {private_key_path} not found.")

    with open(private_key_path, "rb") as f:
        private_key_der = f.read()

    private_key = ECC.import_key(private_key_der)
    public_key = private_key.public_key()
    return public_key.export_key(format="DER")


def load_private_key(name: str = "key.der") -> ECC.EccKey:
    key_file = pathlib.Path(__file__).parent / "keys" / f"{name}"
    assert key_file.is_file()
    with open(key_file, "rb") as f:
        return ECC.import_key(f.read())
