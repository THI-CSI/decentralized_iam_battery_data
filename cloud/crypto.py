import pathlib
from Crypto.PublicKey import ECC

def decrypt_data(data):
    # TODO: Decide with other teams what encryption standard to use
    pass


def verify_credentials(request):
    # TODO: Verify the credentials by checking against the DID document
    pass


def determine_role(request):
    # TODO: Retrieve role from DID document
    pass


def generate_keys():
    # TODO: Generate key pair once and register with blockchain
    keys_dir = pathlib.Path(__file__).parent.joinpath("keys")
    keys_dir.mkdir(exist_ok=True)
    if not keys_dir.joinpath("private_key.pem").is_file():
        key = ECC.generate(curve='secp384r1')
        private_key_pem = key.export_key(format='PEM')
        public_key_pem = key.public_key().export_key(format='PEM')
        with open(keys_dir.joinpath("private_key.pem"), "w") as f:
            f.write(private_key_pem)
        with open(keys_dir.joinpath("public_key.pem"), "w") as f:
            f.write(public_key_pem)
        register_key(key.public_key())


def register_key(key):
    pass
