import functools
import json
import pathlib
import logging
import base64
import json

import os

import requests
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Protocol import HPKE
from Crypto.Protocol.DH import key_agreement
from Crypto.Protocol.KDF import HKDF
from Crypto.Signature import DSS
from Crypto.PublicKey import ECC
from typing import Dict, Any
from Crypto.Hash import SHA3_256
from multiformats import multibase

def sign_vc(vc: dict, private_key: ECC.EccKey, verification_method: str) -> dict:
    """
    Signs the Verifiable Credential dictionary using ECDSA secp256r1 with SHA-256.

    Args:
        vc (dict): The VC JSON object, must include a 'proof' object without 'jws' yet.
        private_key (ECC.EccKey): ECC private key for signing.
        verification_method (str): DID URI for the verification method to add in proof.

    Returns:
        dict: The VC with 'proof.jws' added containing the base64-encoded signature.
    """
    # Prepare a copy of VC to sign, excluding the proof.jws field
    vc_copy = json.loads(json.dumps(vc))  # Deep copy
    if 'jws' in vc_copy.get('proof', {}):
        del vc_copy['proof']['jws']

    # Serialize with sorted keys, no whitespace (canonical-like)
    serialized_vc = json.dumps(vc_copy, separators=(',', ':'), sort_keys=True).encode('utf-8')

    # Create hash of the serialized VC
    hash_obj = SHA256.new(serialized_vc)

    # Create signer with FIPS 186-3 DER encoding (matches your verifier)
    signer = DSS.new(private_key, 'fips-186-3')

    # Generate signature (DER encoded)
    signature_der = signer.sign(hash_obj)

    # Base64 encode signature (standard base64)
    signature_b64 = base64.b64encode(signature_der).decode('ascii')

    # Update VC proof with signature and verification method
    vc['proof']['jws'] = signature_b64
    vc['proof']['verificationMethod'] = verification_method

    return vc

def sign_payload(payload: dict, private_key: ECC.EccKey) -> bytes:

    # Prepare a copy of payload to sign, excluding the proof.jws field
    payload_copy = json.loads(json.dumps(payload))  # Deep copy
    if 'signature' in payload_copy.get('signature', {}):
        del payload_copy['payload']

    # Serialize with sorted keys, no whitespace (canonical-like)
    serialized_payload = json.dumps(payload_copy, separators=(',', ':'), sort_keys=True).encode('utf-8')

    # Create hash of the serialized payload
    hash_obj = SHA256.new(serialized_payload)

    # Create signer with FIPS 186-3 DER encoding (matches your verifier)
    signer = DSS.new(private_key, 'fips-186-3')

    # Generate signature (DER encoded)
    signature_der = signer.sign(hash_obj)

    # Base64 encode signature (standard base64)
    signature_b64 = base64.b64encode(signature_der).decode('ascii')

    # Update payload proof with signature and verification method
    payload['signature'] = signature_b64
    

    return payload

def decrypt_and_verify(receiver_key: ECC.EccKey, message_bytes: bytes) -> bytes:
    message = json.loads(message_bytes)
    fields_to_decode = ["ciphertext", "aad", "salt", "signature", "eph_pub"]
    decoded_message = {key: base64.b64decode(value) for key, value in message.items() if key in fields_to_decode}
    eph_pub_der = decoded_message["eph_pub"]
    eph_pub = ECC.import_key(eph_pub_der)
    nonce = decoded_message["aad"]
    ciphertext = decoded_message["ciphertext"]
    salt = decoded_message["salt"]
    signature = decoded_message["signature"]
    ciphertext_data = ciphertext[:-16]
    tag = ciphertext[-16:]
    context = eph_pub_der + receiver_key.public_key().export_key(format="DER")
    did = message["did"]

    # Verify signature
    sender_key = retrieve_public_key(did)
    verifier = DSS.new(sender_key, mode="fips-186-3", encoding="der")
    message_to_verify = json.dumps({key: value for key, value in message.items() if key != "signature"}).encode()
    try:
        verifier.verify(SHA256.new(message_to_verify), signature)
    except ValueError:
        raise ValueError("Failed decryption due to invalid signature.")

    # Decrypt message
    hkdf = functools.partial(HKDF, key_len=32, hashmod=SHA256, salt=salt, context=context)
    aes_key = key_agreement(eph_pub=eph_pub, static_priv=receiver_key, kdf=hkdf)
    cipher = AES.new(aes_key, AES.MODE_GCM, nonce=nonce)
    cipher.update(nonce)
    try:
        plaintext = cipher.decrypt_and_verify(ciphertext_data, tag)
        return plaintext
    except ValueError:
        raise ValueError("Failed decryption due to invalid MAC tag.")


def decrypt_hpke(private_key: ECC.EccKey, bundle: dict) -> bytes:
    enc = base64.b64decode(bundle["enc"])
    ciphertext = base64.b64decode(bundle["ciphertext"])
    decapsulator = HPKE.new(enc=enc, aead_id=HPKE.AEAD.AES256_GCM, receiver_key=private_key)
    return decapsulator.unseal(ciphertext)


def encrypt_hpke(private_key: ECC.EccKey, message: bytes) -> dict:
    encapsulator = HPKE.new(receiver_key=private_key.public_key(), aead_id=HPKE.AEAD.AES256_GCM)
    ciphertext = encapsulator.seal(message)
    enc = encapsulator.enc
    return {
        "enc": base64.b64encode(enc).decode(),
        "ciphertext": base64.b64encode(ciphertext).decode()
    }


def verify_credentials(did, info) -> ECC.EccKey:
    # TODO: Verify the credentials by checking against the DID document
    pass


def generate_keys(password: str, name: str  = "key") -> None:
    # TODO: Generate key pair once and register with blockchain
    keys_dir = pathlib.Path(__file__).parent.parent / "keys"
    key_name = f"{name}.pem"
    #print(f"Generating keys in {keys_dir}")
    keys_dir.mkdir(exist_ok=True)
    if not (keys_dir / key_name).is_file():
        key = ECC.generate(curve="P-256")
        export_private_key(key, password, keys_dir, key_name)
        logging.info(f"Generated {keys_dir / key_name}")
        register_key(key.public_key())


def export_private_key(key: ECC.EccKey, passphrase: str, keys_dir: pathlib.Path, name: str = "key.pem") -> None:
    private_key_pem = key.export_key(
        format="PEM",
        passphrase=passphrase,
        protection="PBKDF2WithHMAC-SHA512AndAES256-CBC",
        prot_params={"iteration_count": 131072}
    )
    key_file_path = keys_dir / f"{name}"
    with open(key_file_path, "w") as f:
        f.write(private_key_pem)
    key_file_path.chmod(0o600)

def get_public_key(keys_dir: pathlib.Path, passphrase: str,name: str = "key.pem") -> str:
    private_key_path = keys_dir / f"{name}.pem"

    if not private_key_path.is_file():
        raise FileNotFoundError(f"Private key {private_key_path} not found.")

    with open(private_key_path, "rt") as f:
        private_key_pem = f.read()

    private_key = ECC.import_key(private_key_pem, passphrase=passphrase)
    public_key = private_key.public_key()
    return public_key.export_key(format="PEM")


def load_private_key(passphrase: str, name: str = "key") -> ECC.EccKey:
    pem_file = pathlib.Path(__file__).parent.parent / "keys" / f"{name}.pem"
    assert pem_file.is_file()
    with open(pem_file, "r") as f:
        return ECC.import_key(f.read(), passphrase=passphrase)


def register_key(public_key: ECC.EccKey):
    response = requests.post(f"{os.getenv("BLOCKCHAIN_URL", "http://localhost:8443")}/api/v1/dids", json={
        "publicKey": {
            "type": "Multikey",
            "publicKeyMultibase": multibase.encode(public_key.export_key(format="DER"), "base58btc"),
        },
        "service": {
            "type": "BatteryPassAPI",
            "serviceEndpoint": os.getenv("BASE_URL", "http://localhost:8567"),
        }
    })
    return response.status_code == 200


def retrieve_public_key(did: str) -> ECC.EccKey:
    response = requests.get(f"{os.getenv("BLOCKCHAIN_URL", "http://localhost:8443")}/api/v1/dids/{did}")
    # TODO: Add revoked check
    return ECC.import_key(multibase.decode(response.json()["verificationMethod"]["publicKeyMultibase"]))


def extract_vc_info(vc: Dict[str, Any]) -> tuple[str, str, str]:
    """
    Extract URI, issuer, and holder from a VC object.

    :param vc: The Verifiable Credential (VC) as a dictionary.
    :return: A tuple containing (URI, Issuer ID, Holder ID).
    """

    # Get all necessary data from the verifiable credential
    uri = vc.get("id")
    issuer = vc.get("issuer")
    subject = vc.get("credentialSubject")

    # Checking credentialSubjects form (If we have a uniform form, this is not necessary,
    # but will be left in for now)
    if isinstance(subject, dict):
        holder = subject.get("id")
    elif isinstance(subject, list) and len(subject) > 0:
        holder = subject[0].get("id")
    else:
        holder = None

    # Check if all data is present, if not raise a ValueError
    if uri is None or issuer is None or holder is None:
        raise ValueError("Invalid Verifiable Credential")

    return uri, issuer, holder


def verify_vc(vc_json_object: json) -> bool:
    """
    This function takes a Verifiable Credential dictionary, extracts the URI, issuer id, and holder id, and
    creates a 256-bit SHA-3 hash of the whole VC. The Data is then send to the blockchain to be verified.
    """

    # Extract the uri, issuer and holder
    uri, issuer, holder = extract_vc_info(vc_json_object)

    # To generate the Hash, we must first serialize the Object
    serialized_vc = json.dumps(vc_json_object, separators=(',', ':'), sort_keys=True).encode('utf-8')

    # Create the SHA3-256bit Hash
    vc_hash = SHA3_256.new(serialized_vc)

    # devbod: TODO: Should we use hexdigest()?
    # vc_digest = vc_hash.hexdigest()

    # Now we need to send the Data to the Blockchain
    # First we create the Datastructures we send
    data = {
        "uri": uri,
        "issuer": issuer,
        "holder": holder,
        "hash": vc_hash
    }

    # Then we send the Data to the Blockchain
    response = requests.post(BLOCKCHAIN_URL, json=data)

    # If the response is 200, we can assume the VC is valid
    if response.status_code == 200:
        return True
    # If not, we can assume the VC is invalid. We should check for reasons in the future
    # devbod: TODO: Check for Reasons
    else:
        return False