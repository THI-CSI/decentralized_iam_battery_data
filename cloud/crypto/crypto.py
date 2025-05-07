import pathlib
import logging
import base64
from Crypto.Protocol import HPKE
from Crypto.PublicKey import ECC


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
