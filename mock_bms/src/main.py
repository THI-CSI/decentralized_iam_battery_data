import os

from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

from crypto import all_in_one_crypto
from api import get_data, post_data
from data_gen import process_json_gen_output

PRIVATE_KEY_PATH = 'private_key.pem'

# Creates and saves private key on first run.
def flash():
    if os.path.exists(PRIVATE_KEY_PATH):
        print(f"Private key already exists at {PRIVATE_KEY_PATH}.")
        return

    private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())
    try:
        with open(PRIVATE_KEY_PATH, "wb") as key_file:
            key_file.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            ))
        print(f"Private key created and saved to {PRIVATE_KEY_PATH}.")
    except Exception as e:
        print(f"Error saving private key: {e}")

def init():
    # Load the non-ephemeral private key from a file
    with open(PRIVATE_KEY_PATH, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
        )
    return private_key

# Used to extract public key from Cloud DID
def extract_public_cloud_key(cloud_did):
    # Todo: Implement key extraction
    # Placeholder Code:
    private_cloud_key = ec.generate_private_key(ec.SECP256R1())
    public_cloud_key = private_cloud_key.public_key()
    cloud_private_key_der = private_cloud_key.private_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    return public_cloud_key

def main():
    flash()
    private_bms_key = init()
    bms_did = "did:batterypass:896ad506-9843-48d3-b599-be45fca2bb3e"

    # Reimplement when to.do is completed:
    #cloud_did = get_data(bms_did)
    #public_cloud_key = extract_public_cloud_key(cloud_did)
    public_cloud_key = extract_public_cloud_key(1) # Temporary override

    json_data = process_json_gen_output()
    data = all_in_one_crypto(private_bms_key, public_cloud_key, json_data, bms_did)
    post_data(data)

if __name__ == '__main__':
    main()
