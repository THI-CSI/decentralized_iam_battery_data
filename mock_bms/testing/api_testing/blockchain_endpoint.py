from flask import Flask, jsonify
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
import base64

app = Flask(__name__)

@app.route('/api/v1/dids/did:batterypass:896ad506-9843-48d3-b599-be45fca2bb3e', methods=['GET'])
def get_did():
    # Generate a private key for use in the cloud
    private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())
    public_key = private_key.public_key()

    # Serialize the public key to bytes in the correct format
    public_key_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.X962,
        format=serialization.PublicFormat.UncompressedPoint
    )

    # Encode the public key in base64
    public_key_base64 = base64.b64encode(public_key_bytes).decode('utf-8')

    # Create the DID document
    cloud_did = {
        "@context": [
            "https://www.w3.org/2018/credentials/v1",
            "http://localhost:8443/docs/did.schema.html"
        ],
        "id": "did:batterypass:cloud.vw-node-eu-central",
        "verificationMethod": {
            "id": "did:batterypass:cloud.vw-node-eu-central#key-1",
            "type": "JsonWebKey2020",
            "controller": "did:batterypass:oem.VW",
            "publicKeyMultibase": "z" + public_key_base64
        },
        "service": [
            {
                "id": "did:batterypass:cloud.vw-node-eu-central",
                "type": "BatteryPassAPI",
                "serviceEndpoint": "https://<cloud-endpoint>"
            }
        ],
        "timestamp": "2025-04-02T09:00:00Z",
        "revoked": False
    }

    return jsonify(cloud_did)

if __name__ == '__main__':
    app.run(host='localhost', port=8080)
