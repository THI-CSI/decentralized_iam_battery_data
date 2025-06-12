import json
import sys
import os
from jwcrypto import jwk, jws
from jwcrypto.common import json_encode

def load_jwk_from_file(path):
    with open(path, 'r') as f:
        key_data = f.read()
        try:
            return jwk.JWK.from_json(key_data)
        except Exception:
            return jwk.JWK.from_pem(key_data.encode('utf-8'))

def sign_json_file(json_file_path, key_path, output_path='signed.jws'):
    # Remove the output file if it already exists
    if os.path.exists(output_path):
        print(f"Removing existing {output_path}...")
        os.remove(output_path)

    # Load the JSON payload
    with open(json_file_path, 'r') as f:
        payload = json.dumps(json.load(f))  # ensure it's compact JSON string

    # Load the JWK (or PEM)
    key = load_jwk_from_file(key_path)

    # Create and sign the JWS
    signature = jws.JWS(payload.encode('utf-8'))
    signature.add_signature(key, alg='ES256', protected=json_encode({"alg": "ES256"}))

    # Output compact JWS format
    jws_output = signature.serialize(compact=True)

    # Save the JWS to a file
    with open(output_path, 'w') as out_file:
        out_file.write(jws_output)

    print(f"JWS signature saved to {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python sign_json.py <path_to_json_file> <path_to_key_file>")
    else:
        sign_json_file(sys.argv[1], sys.argv[2])
        