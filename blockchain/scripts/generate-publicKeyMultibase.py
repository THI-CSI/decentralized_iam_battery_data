from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import base58
import sys

# Multicodec prefixes
MULTICODEC_PREFIXES = {
    'ed25519': b'\xed',
    'p256': b'\x12\x00',  # aka secp256r1
}

def pem_to_publickeymultibase(pem_path, key_type):
    # Load PEM
    with open(pem_path, 'rb') as f:
        pem_data = f.read()

    # Load public key object
    pubkey = serialization.load_pem_public_key(pem_data, backend=default_backend())

    # Get raw public key bytes depending on key type
    if key_type == 'ed25519':
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
        if not isinstance(pubkey, Ed25519PublicKey):
            raise TypeError("Expected Ed25519 public key")
        raw = pubkey.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        )
        prefix = MULTICODEC_PREFIXES['ed25519']

    elif key_type == 'p256':
        from cryptography.hazmat.primitives.asymmetric.ec import EllipticCurvePublicKey, SECP256R1
        if not isinstance(pubkey, EllipticCurvePublicKey):
            raise TypeError("Expected ECDSA public key")
        if not isinstance(pubkey.curve, SECP256R1):
            raise TypeError("Expected SECP256R1 (P-256) curve")
        raw = pubkey.public_bytes(
            encoding=serialization.Encoding.X962,
            format=serialization.PublicFormat.UncompressedPoint
        )
        prefix = MULTICODEC_PREFIXES['p256']

    else:
        raise ValueError("Unsupported key type: choose from 'ed25519' or 'p256'")

    # Combine prefix and raw key
    multicodec_bytes = prefix + raw

    # Multibase (Base58BTC, prefix with 'z')
    multibase = 'z' + base58.b58encode(multicodec_bytes).decode()
    return multibase


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python pem_to_multibase.py <public_key.pem> <key_type: ed25519|p256>")
        sys.exit(1)

    pem_file = sys.argv[1]
    key_type = sys.argv[2]

    try:
        result = pem_to_publickeymultibase(pem_file, key_type)
        print(result)
    except Exception as e:
        print("Error:", e)
