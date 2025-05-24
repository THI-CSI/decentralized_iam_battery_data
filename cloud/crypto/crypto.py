import pathlib
import logging
import base64
import json
import requests

import os

import requests
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Protocol import HPKE
from Crypto.Protocol.DH import key_agreement
from Crypto.Protocol.KDF import HKDF
from Crypto.Random import get_random_bytes
from Crypto.Signature import DSS
from Crypto.PublicKey import ECC
from typing import Dict, Any
from Crypto.Hash import SHA3_256
from multiformats import multibase
from tinydb import TinyDB, where


def hkdf(shared_secret):
    salt = get_random_bytes(16)
    return HKDF(master=shared_secret, key_len=256 // 8, salt=salt, hashmod=SHA256, context=None)


# devbod: TODO: Change this when having more info
BLOCKCHAIN_URL = "http://localhost:8000/FILLER/FOR/NOW"

def decrypt_and_verify(receiver_key: ECC.EccKey, message_bundle: dict) -> bytes:
    # TODO: @valljah Implement appropriate decryption and verification in accordance to BMS encryption
    ephemeral_pub_bytes = multibase.decode(message_bundle["pkE"])
    ephemeral_pub = ECC.import_key(ephemeral_pub_bytes)
    shared_secret = key_agreement(eph_pub=ephemeral_pub, static_priv=receiver_key, kdf=hkdf)
    signature = multibase.decode(message_bundle["sig"])
    ciphertext = multibase.decode(message_bundle["ciphertext"])
    did = message_bundle["did"]
    info = message_bundle["info"]
    sender_key = retrieve_public_key(did)
    verifier = DSS.new(sender_key, "fips-186-3")
    verifier.verify(SHA256.new(ephemeral_pub_bytes + info + did + ciphertext), signature)
    try:
        return (AES.new(key=shared_secret, mode=AES.MODE_GCM, nonce=ciphertext[:12])
                .decrypt_and_verify(ciphertext[28:], ciphertext[12:28]))
    except ValueError:
        raise ValueError("Failed decryption due to invalid MAC tag.")


def encrypt_and_sign(receiver_key: ECC.EccKey, message: bytes) -> dict:
    encapsulator = HPKE.new(
        receiver_key=receiver_key,
        aead_id=HPKE.AEAD.AES256_GCM,
    )
    ciphertext = encapsulator.seal(message)
    enc = encapsulator.enc
    return {
        "enc": base64.b64encode(enc).decode(),
        "ciphertext": base64.b64encode(ciphertext).decode()
    }


def verify_credentials(did, info) -> ECC.EccKey:
    # TODO: Verify the credentials by checking against the DID document
    pass


def determine_role(db: TinyDB, did: str) -> str | None:
    if db.search(where("id") == did):
        return "bms"
    did_response = requests.get(f"{os.getenv("BLOCKCHAIN_URL", "http://localhost:8443")}/api/v1/dids/{did}")
    if not did_response.ok:
        return None
    controller = did_response.json()["publicKey"]["controller"]
    return "oem" if controller == "did:batterypass:eu" else None


def generate_keys(password: str) -> None:
    # TODO: Generate key pair once and register with blockchain
    keys_dir = pathlib.Path(__file__).parent / "keys"
    keys_dir.mkdir(exist_ok=True)
    if not (keys_dir / "key.pem").is_file():
        key = ECC.generate(curve="P-256")
        export_private_key(key, password, keys_dir / "key.pem")
        logging.info(f"Generated {keys_dir / "key.pem"}")
        register_key(key.public_key())


def export_private_key(key: ECC.EccKey, passphrase: str, key_path: pathlib.Path) -> None:
    private_key_pem = key.export_key(
        format="PEM",
        passphrase=passphrase,
        protection="PBKDF2WithHMAC-SHA512AndAES256-CBC",
        prot_params={"iteration_count": 131072}
    )
    with open(key_path, "w") as f:
        f.write(private_key_pem)
    key_path.chmod(0o600)


def load_private_key(passphrase: str) -> ECC.EccKey:
    pem_file = pathlib.Path(__file__).parent / "keys" / "key.pem"
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
    return ECC.import_key(multibase.decode(response.json()["publicKey"]["publicKeyMultibase"]))


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