import json
import jwt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend


# === Load RSA Private Key from PEM file ===
def load_private_key(pem_path: str):
    with open(pem_path, "rb") as key_file:
        return serialization.load_pem_private_key(
            key_file.read(), password=None, backend=default_backend()
        )


# === Create JWS Signature ===
def create_jws(payload: dict, private_key) -> str:
    return jwt.encode(payload, private_key, algorithm="RS256")


# === Read Json File ===
def read_file(path: str):
    with open(path) as jf:
        data = json.load(jf)
        data["proof"]["jws"] = ""
        return data


# === Main ===
if __name__ == "__main__":
    # Example JSON payload
    payload_oem_did = read_file("./docs/test-examples/oem-did.json")["payload"]
    payload_oem_vc = read_file("./docs/test-examples/oem-vc.json")
    payload_bms_did = read_file("./docs/test-examples/bms-did.json")["payload"]
    # payload_bms_vc = read_file("./docs/test-examples/bms-did.json")

    # Paths to your PEM-encoded keys
    private_key_path_eu = "./internal/api/web/testkeys/rsa_private_key.pem"
    private_key_path_oem = "./docs/test-examples/oem_private_key.pem"
    private_key_path_bms = "./docs/test-examples/bms_private_key.pem"

    # Load keys
    private_key_eu = load_private_key(private_key_path_eu)
    private_key_oem = load_private_key(private_key_path_oem)
    private_key_bms = load_private_key(private_key_path_bms)

    # Create and print JWS token
    jws_token = create_jws(payload_oem_vc, private_key_oem)
    print(jws_token)
