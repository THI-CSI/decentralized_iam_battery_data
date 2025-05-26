from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import base64
import json
from datetime import datetime
import os

did = "did:example:123456789abcdefgh"

# Generate signing key pair
private_signing_key = ec.generate_private_key(ec.SECP256R1())
public_signing_key = private_signing_key.public_key()

# Genertate Ephermal key pair for key agreement
private_ephermal_key = ec.generate_private_key(ec.SECP256R1())
public_ephermal_key = private_ephermal_key.public_key()

# Generate Key Pair for Cloud
private_cloud_key = ec.generate_private_key(ec.SECP256R1())
public_cloud_key = private_cloud_key.public_key()

# Define dynamic battery data
dynamic_battery_data = {
    "state_of_health": 97,
    "state_of_charge": 78,
    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
}
dynamic_battery_data_json = json.dumps(dynamic_battery_data)
dynamic_battery_data_bytes = dynamic_battery_data_json.encode("utf-8")

# Key aggreement with ECDH
shared_secret = private_ephermal_key.exchange(ec.ECDH(), public_cloud_key)

# Key derivation with HKDF(SHA-256)
ephermal_public_key_der = public_ephermal_key.public_bytes(
    encoding=serialization.Encoding.DER,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)
cloud_public_key_der = public_ephermal_key.public_bytes(
    encoding=serialization.Encoding.DER,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)
info = ephermal_public_key_der + cloud_public_key_der
salt = os.urandom(32)
aes_derived_key = HKDF(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    info=info
).derive(shared_secret)

# AES-GCM 256
nonce = os.urandom(12)
aesgcm = AESGCM(aes_derived_key)
ciphertext = aesgcm.encrypt(nonce, dynamic_battery_data_bytes, nonce)

# Create message 
message = f'"ciphertext": {ciphertext}, "aad": {nonce}, "salt": {salt}, "ephermal_public_key": {ephermal_public_key_der}, "did": {did}'
message_bytes = message.encode("utf-8")

# Sign messsage with ECDSA and add to message
signature = private_signing_key.sign(
    message_bytes,
    ec.ECDSA(hashes.SHA256())
)
message = f'"ciphertext": {ciphertext}, "aad": {nonce}, "salt": {salt}, "ephermal_public_key": {ephermal_public_key_der}, "did": {did}, "signature": {signature}'
message_bytes = message.encode("utf-8")
print(message_bytes)