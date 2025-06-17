import functools
import pathlib
import logging
import base64
import json
from jwcrypto import jws, jwk
import os
import requests

from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Protocol import HPKE
from Crypto.Protocol.DH import key_agreement
from Crypto.Protocol.KDF import HKDF
from Crypto.Signature import DSS
from Crypto.PublicKey import ECC
from multiformats import multibase
from tinydb.table import Document


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
    verifier = DSS.new(sender_key, mode="fips-186-3", encoding="binary")
    message_to_verify = json.dumps(
        {key: value for key, value in message.items() if key != "signature"}, separators=(",", ":")
    ).encode()
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


def determine_role(doc: Document | None, sender_did: str) -> str | None:
    if doc and doc["did"] == sender_did:
        return "bms"
    did_response = requests.get(f"{os.getenv("BLOCKCHAIN_URL", "http://localhost:8443")}/api/v1/dids/{sender_did}")
    if not did_response.ok:
        return None
    controller = did_response.json()["verificationMethod"]["controller"]
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
    raw = multibase.decode(response.json()["verificationMethod"]["publicKeyMultibase"])
    if len(raw) == 67:
        raw = raw[len(b"\x12\x00"):]
        return ECC.EccKey(curve="P-256",
                          point=ECC.EccPoint(
                              int.from_bytes(raw[1:33], "big"), int.from_bytes(raw[33:65], "big"))
                          )
    if response.json()["revoked"]:
        raise ValueError("Public key revoked.")
    return ECC.import_key(multibase.decode(response.json()["verificationMethod"]["publicKeyMultibase"]))


def verify_vp(vp_json_object) -> str | None:
    """
    This function takes a Verifiable Presentation dictionary and sends it to the Blockchain for verification.
    """
    validator = jws.JWS()
    try:
        validator.deserialize(vp_json_object["proof"]["jws"])
        did = vp_json_object["proof"]["verificationMethod"].split("#")[0]
    except KeyError:
        return None
    key = jwk.JWK.from_pem(retrieve_public_key(did).export_key(format="PEM").encode())
    try:
        validator.verify(key)
    except jws.InvalidJWSSignature:
        return None

    # Then we send the Data to the Blockchain.
    response = requests.post(
        f"{os.getenv("BLOCKCHAIN_URL", "http://localhost:8443")}/api/v1/vc/verify",
        json=vp_json_object
    )
    if not response.ok:
        return None

    try:
        return "read" if (
                "read" in next(vp_json_object["verifiableCredential"])["credentialSubject"]["accessLevel"]
        ) else None
    except (KeyError, StopIteration):
        return None
