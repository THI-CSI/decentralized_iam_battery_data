from typing import NamedTuple
from Crypto.PublicKey import ECC
from multiformats import multibase
import pathlib
import requests


class ECCKeyPair(NamedTuple):
    private_key: ECC.EccKey
    public_key: ECC.EccKey


def generate_keys() -> ECCKeyPair | None:
    key = ECC.generate(curve='P-256')
    keys_dir = pathlib.Path(__file__).parent / "keys"
    keys_dir.mkdir(exist_ok=True)
    if (keys_dir / "key.pem").is_file():
        print(f"Key file already exists at {keys_dir / 'key.pem'}")
        return None
    with open(keys_dir / "key.pem", "w") as f:
        f.write(key.export_key(format="PEM"))
    with open(keys_dir / "public.pem", 'w') as f:
        f.write(key.public_key().export_key(format='PEM'))
    register_public_key(key.public_key())
    return ECCKeyPair(key, key.public_key())


def register_public_key(public_key: ECC.EccKey, did: str) -> bool:
    try:
        endpoint = "http://localhost:8443/api/v1/did/"
        response = requests.post(
            endpoint,
            json={
                "publicKey": multibase.encode(public_key.export_key(format="DER"), "base64url"),
                # "did": did
            }
        )
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False


if __name__ == "__main__":
    key_pair = generate_keys()
    if key_pair is None:
        exit()
    if register_public_key(key_pair.public_key, ""):
        print("Public key registered successfully")
    else:
        print("Failed to register public key")
