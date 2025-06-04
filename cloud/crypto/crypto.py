import os
import pathlib
import logging
import base64
import json
import requests

from Crypto.Protocol import HPKE
from Crypto.PublicKey import ECC
from typing import Dict, Any, Union, Tuple, Literal
from Crypto.Hash import SHA3_256


def decrypt_and_verify(receiver_key: ECC.EccKey, message_bundle: dict) -> bytes:
    enc = base64.b64decode(message_bundle["enc"])
    ciphertext = base64.b64decode(message_bundle["ciphertext"])
    decapsulator = HPKE.new(
        receiver_key=receiver_key,
        aead_id=HPKE.AEAD.AES256_GCM,
        enc=enc
    )
    try:
        return decapsulator.unseal(ciphertext)
    except ValueError:
        raise ValueError("Invalid signature")


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


def verify_credentials(request):
    # TODO: Verify the credentials by checking against the DID document
    pass


def determine_role(request):
    # TODO: Retrieve role from DID document
    pass


def generate_keys(password: str) -> None:
    # TODO: Generate key pair once and register with blockchain
    keys_dir = pathlib.Path(__file__).parent / "keys"
    keys_dir.mkdir(exist_ok=True)
    if not (keys_dir / "key.pem").is_file():
        key = ECC.generate(curve="P-384")
        export_private_key(key, password, keys_dir)
        logging.info(f"Generated {keys_dir / "key.pem"}")
        register_key(key.public_key())


def export_private_key(key: ECC.EccKey, passphrase: str, keys_dir: pathlib.Path) -> None:
    private_key_pem = key.export_key(
        format="PEM",
        passphrase=passphrase,
        protection="PBKDF2WithHMAC-SHA512AndAES256-CBC",
        prot_params={"iteration_count": 131072}
    )
    with open(keys_dir / "key.pem", "w") as f:
        f.write(private_key_pem)
    (keys_dir / "key.pem").chmod(0o600)


def load_private_key(passphrase: str) -> ECC.EccKey:
    pem_file = pathlib.Path(__file__).parent / "keys" / "key.pem"
    assert pem_file.is_file()
    with open(pem_file, "r") as f:
        return ECC.import_key(f.read(), passphrase=passphrase)


def register_key(key: ECC.EccKey):
    pass


def extract_vc_info(vc: Dict[str, Any]) -> tuple[str, str, str]:
    """
    Extract URI, issuer, and holder from a VC object.

    :param vc: The Verifiable Credential (VC) as a dictionary.
    :return: A tuple containing (URI, Issuer ID, Holder ID).
    """

    # Get all necessary data from the verifiable credential.
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

    # Check if all data is present, if not, raise a ValueError.
    if uri is None or issuer is None or holder is None:
        raise ValueError("Invalid Verifiable Credential")

    return uri, issuer, holder


def verify_vc(vc_json_object: json) -> Union[Tuple[Literal[True], dict], Tuple[Literal[False], str]]:
    """
    This function takes a Verifiable Credential dictionary, extracts the URI, issuer id, and holder id, and
    creates a 256-bit SHA-3 hash of the whole VC. The Data is then send to the blockchain to be verified.
    """

    # Extract the uri, issuer and holder.
    uri, issuer, holder = extract_vc_info(vc_json_object)

    # To generate the Hash, we must first serialize the Object.
    serialized_vc = json.dumps(vc_json_object, separators=(',', ':'), sort_keys=True).encode('utf-8')

    # Create the SHA3-256bit Hash
    vc_hash = SHA3_256.new(serialized_vc)

    # devbod: TODO: Should we use hexdigest()?
    # vc_digest = vc_hash.hexdigest()

    # Now we need to send the Data to the Blockchain.
    # First, we create the Datastructures we send.
    data = {
        "issuerDID": issuer,
        "holderDID": holder,
        "id": uri,
        "vcHash": vc_hash
    }

    # Then we send the Data to the Blockchain.
    response = requests.post(f"{os.getenv("BLOCKCHAIN_URL", "http://localhost:8443")}/api/v1/vc/verify", json=data)

    response_dict = response.json()
    response_status_code = response.status_code

    # If the response is 200, the VC is valid.
    if response_status_code == 200:
        return True, response_dict
    # Status code 404 means the VC has not been found or revoked.
    elif response_status_code == 404:
        return False, f"VC has been revoked or not found, status code {response_status_code}"
    # Status code 400 means the input was invalid/incorrect.
    elif response_status_code == 400:
        return False, f"Input is incorrect, status code {response_status_code}"
    # If we have a whole different status code, we have an unknown error.
    else:
        return False, f"Unknown status code {response.status_code}"