import json
import base64

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec

from api import get_data, post_data
from message_creation import message_creation
from data_gen import retrieve_stored_battery_data, run_battery_data_generator

# Used to extract public key from Cloud DID
def extract_public_cloud_key(cloud_did):
    data = json.loads(cloud_did)
    public_cloud_key_str = data['verificationMethod']['publicKeyMultibase']

    # Decode the public key from base64
    if public_cloud_key_str.startswith('z'):
        public_cloud_key_str = public_cloud_key_str[1:]  # Remove the 'z' prefix

    public_cloud_key_bytes = base64.b64decode(public_cloud_key_str)

    # Load the public key
    try:
        public_cloud_key = ec.EllipticCurvePublicKey.from_encoded_point(ec.SECP256R1(), public_cloud_key_bytes)
        print("Public Cloud Key:", public_cloud_key)
    except ValueError as e:
        print(f"Error loading public key: {e}")
        return None

    return public_cloud_key

def data_exchange(blockchain_api_url, bms_did_id, cloud_api_url, regen):
    battery_data_str = retrieve_stored_battery_data()
    if battery_data_str is None or regen==True:
        battery_data_str = run_battery_data_generator()
    battery_data = battery_data_str.encode('utf-8')

    # Fetch the cloud DID from the API
    cloud_did_dict = get_data(blockchain_api_url + bms_did_id)
    cloud_did_str = json.dumps(cloud_did_dict)

    # Check if the DID is revoked
    if cloud_did_dict.get('revoked', False):
        print("The DID is revoked. Exiting.")
        return  # Exit or handle as needed

    public_cloud_key = extract_public_cloud_key(cloud_did_str)

    cloud_public_key_der_base64 = base64.b64encode(public_cloud_key.public_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )).decode('utf-8')

    message = message_creation(battery_data, cloud_public_key_der_base64)
    print(message)

    decoded_message = message.decode('utf-8')

    serialized_message = json.dumps(json.loads(decoded_message))

    post_data(cloud_api_url, serialized_message)
