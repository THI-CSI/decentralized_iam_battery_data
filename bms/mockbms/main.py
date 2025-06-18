import argparse, sys, json, subprocess
from dotenv import load_dotenv
from uuid import uuid4
import tempfile


# Load environment variables from .env file
load_dotenv()

from crypto import generate_keys, load_private_key, ecc_public_key_to_multibase
from util import build_did_document, register_key_with_blockchain


def main():
    # Create the parser
    parser = argparse.ArgumentParser(description="Mock a Battery Management System")


    parser.add_argument("--initialize", required=True, help="Password to encrypt BMS private key")

    # Parsing arguments
    args = parser.parse_args()
    # Generates the BMS Signing Key Pair and prints it on screen
    if args.initialize:
        generate_keys(name="bms_key")
        private_key = load_private_key("bms_key.der")
        public_key = private_key.public_key()

        # Convert to multibase
        public_key_multibase = ecc_public_key_to_multibase(public_key)

        did = f"did:batterypass:bms.sn-{(uuid4().hex[:8])}"
        did_doc = build_did_document(did, args.initialize, public_key_multibase, True)
        did_str = json.dumps(did_doc)
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as tmpfile:
            tmpfile.write(did_str)
            tmpfile_path = tmpfile.name
        result = subprocess.run(
                ["python3", "../../client/sign.py", tmpfile_path, args.initialize],
                capture_output=True,
                text=True
        )
        # Get the output string from the subprocess
        output_str = result.stdout.strip()

        # Convert output string back to a Python object (assuming it's JSON)
        signed_did = json.loads(output_str)

        print(json.dumps(signed_did, indent=2))
        
        register_key_with_blockchain(signed_did)

        #controller_did = retrieve_did_from_blockchain(args.initialize)


    # Wrong or no argument provided
    if not any(vars(args).values()):
        print(f"Error")
        sys.exit(1)
    exit(0)

if __name__ == '__main__':
    main()

