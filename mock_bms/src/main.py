import os
import json
import base64

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
    data = json.loads(cloud_did)
    public_cloud_key_str = data['verificationMethod']['publicKeyMultibase']

    # Decode the public key from base64
    public_cloud_key_bytes = base64.b64decode(public_cloud_key_str)

    # Load the public key
    try:
        public_cloud_key = ec.EllipticCurvePublicKey.from_encoded_point(ec.SECP256R1(), public_cloud_key_bytes)
        print("Public Cloud Key:", public_cloud_key)
    except ValueError as e:
        print(f"Error loading public key: {e}")
        return None

    return public_cloud_key

# Retrieves locally saved BMS DID and extracts ID
def get_bms_id():
    with open('bms.json', 'r', encoding='utf-8') as f:
        bms_did_str = f.read()

    json_data = json.loads(bms_did_str)
    bms_id = json_data['id']
    return bms_id

def main():
    flash()
    private_bms_key = init()
    #bms_id = "did:batterypass:896ad506-9843-48d3-b599-be45fca2bb3e"
    bms_id = get_bms_id()

    cloud_did_dict = get_data(bms_id)
    cloud_did_str = json.dumps(cloud_did_dict)
    public_cloud_key = extract_public_cloud_key(cloud_did_str)

    # Temporary implementation of cloud_did being stored locally
    #with open('cloud.json', 'r', encoding='utf-8') as f:
    #    cloud_did_str = f.read()
    #public_cloud_key = extract_public_cloud_key(cloud_did_str)

    json_data = process_json_gen_output()
    data = all_in_one_crypto(private_bms_key, public_cloud_key, json_data, bms_id)
    post_data(data)

def sign_vc():
    #Todo: implement
    pass

if __name__ == '__main__':
    '''
    # public and private key with the SECP256R1 curve
    private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())
    public_key = private_key.public_key()

    # Serialize the public key to bytes
    public_key_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.X962,
        format=serialization.PublicFormat.UncompressedPoint
    )

    # Encode the public key in base64 format
    base64_encoded_key = base64.b64encode(public_key_bytes).decode('utf-8')

    print("Base58 Encoded Public Key:", base64_encoded_key)
    '''
    main()
