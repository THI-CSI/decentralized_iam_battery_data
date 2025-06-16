#!/usr/bin/env python
import datetime
import sys
import requests
import click
import json
from pathlib import Path
from Crypto.PublicKey import ECC
from multiformats import multibase
from jwcrypto import jwk, jws


@click.command()
@click.argument("did", type=str)
@click.argument("sign_did", type=str)
@click.argument("registree_key_path", type=click.Path(exists=True, path_type=Path))
@click.argument("sign_key_path", type=click.Path(exists=True, path_type=Path))
def main(did: str, sign_did: str, sign_key_path: Path, registree_key_path: Path):
    with open(sign_key_path) as f:
        sign_key = ECC.import_key(f.read())
    with open(registree_key_path) as f:
        registree_key = ECC.import_key(f.read()).public_key()
    if not sign_key.has_private():
        print("Signing key is not private", file=sys.stderr)
        exit(1)
    did_document = {
        "@context": [
            "https://www.w3.org/2018/credentials/v1",
            "http://localhost:8443/docs/did.schema.html"
        ],
        "id": did,
        "revoked": False,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "verificationMethod": {
            "controller": sign_did,
            "id": f"{did}#key-1",
            "publicKeyMultibase": multibase.encode(registree_key.export_key(format="DER"), "base58btc"),
            "type": "Multikey"
        }
    }
    signature = jws.JWS(json.dumps(did_document))
    signature.add_signature(
        jwk.JWK.from_pem(sign_key.export_key(format="PEM").encode()), alg="ES256", protected={"alg": "ES256"}
    )
    request = {
        "proof": {
            "type": "EcdsaSecp256r1Signature2019",
            "created": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "verificationMethod": f"{sign_did}#key-1",
            "challenge": "c82f7883-42a1-4b78-9c2e-d8d5321af9f8",
            "proofPurpose": "authentication",
            "jws": signature.serialize(compact=True)
        },
        "payload": did_document
    }
    try:
        response = requests.post("http://localhost:8080/api/v1/dids/createormodify", json=request)
    except requests.exceptions.RequestException as e:
        print(f"Error: {e.args[0]}", file=sys.stderr)
        exit(1)
    if response.ok:
        print(response.text)
    else:
        print(f"Failed to register DID: {response.status_code} {response.text}")


if __name__ == "__main__":
    main()
