#!/usr/bin/env python3

import argparse
import json
import sys
import uuid
import pathlib
from datetime import datetime, timedelta, timezone

from crypto.crypto import load_private_key, get_public_key, generate_keys, encrypt_hpke, decrypt_hpke, verify_vc, sign_vc, sign_payload
from Crypto.PublicKey import ECC
from util.util import generate_vc, build_did_document, create_service_access_vc
from multiformats import multibase
from dotenv import load_dotenv
import logging
from pyld import jsonld
import requests

import random 


keys_dir = pathlib.Path(__file__).parent / "keys"
verbose = False

def log(message, level="info", override=False):
    if verbose or override:
        print(f"[{level.upper()}] {message}")


def main():
    parser = argparse.ArgumentParser(description="Generate keys for BMS and Service Station")
    parser.add_argument("--bms-password", required=True, help="Password to encrypt BMS private key")
    parser.add_argument("--service-password", required=True, help="Password to encrypt Service Station private key")
    parser.add_argument("--verbose", required=False, action='store_true', help="Enable verbose output")
    args = parser.parse_args()
    if args.verbose:
        global verbose
        verbose = True

    # Connectivity Test to Cloud
    log("[ServiceClient] Sending GET Request to Clound Endpoint to ensure connection...", override=True)
    requests_url = "http://localhost:8443/"
    cloud_public_key = None
    response = requests.get(requests_url)
    if response.status_code == 200:
        log(f"Successfully connected to {requests_url}", override=True)
        cloud_public_key_pem = response.json().get("public_key")
        log(f"Cloud Public Key: {cloud_public_key_pem}", override=True)  # PEM format

        # Decode PEM public key to ECC key object
        cloud_public_key = ECC.import_key(cloud_public_key_pem)
        log(f"Cloud Public Key ECC: {cloud_public_key}")  # ECC object
    else:
        log(f"Failed to connect to {requests_url}. Status code: {response.status_code}", level="error", override=True)
        sys.exit(1)


    # Generate BMS key pair
    log("Generating BMS key pair...")
    bms_name = "bms"
    generate_keys(args.bms_password, name=f"{bms_name}_key")
    bms_pub_pem = get_public_key(keys_dir, args.bms_password, f"{bms_name}_key")
    bms_pub_key = ECC.import_key(bms_pub_pem)
    bms_pub_der = bms_pub_key.export_key(format="DER")
    multibase_bms_key = multibase.encode(bms_pub_der, "base58btc")
    log(f"BMS Public Key (Multibase): {multibase_bms_key}")

    # Build BMS DID Document
    bms_did = f"did:batterypass:bms.sn-{uuid.uuid4().hex[:8]}"
    bms_did_doc = build_did_document(bms_did, multibase_bms_key, True)
    log("\nBMS DID Document:")
    log(json.dumps(bms_did_doc, indent=2))
    
    log("-"* 40)

    # Generate Service Station key pair
    log("Generating Service Station key pair...")
    service_name = "service"
    generate_keys(args.service_password, name=f"{service_name}_key")
    service_pub_pem = get_public_key(keys_dir, args.service_password, f"{service_name}_key")
    service_pub_key = ECC.import_key(service_pub_pem)
    service_pub_der = service_pub_key.export_key(format="DER")
    multibase_service_key = multibase.encode(service_pub_der, "base58btc")
    log(f"Service Station Public Key (Multibase): {multibase_service_key}")

    service_did = f"did:batterypass:service.sn-{uuid.uuid4().hex[:8]}"
    service_did_doc = build_did_document(service_did, multibase_service_key)
    log("\nService Station DID Document:")
    log(json.dumps(service_did_doc, indent=2))

    log("-" * 40)

    log("Successfully generated keys and DID documents for BMS and Service Station.", override=True)
    log("-" * 40, override=True)
    # Generate Verifiable Credential
    log("[ServiceClient] Generating Verifiable Credential...", override=True)
    access_levels = ["read", "write"]
    now = datetime.now(timezone.utc)
    valid_until = now + timedelta(days=365)  # 1 year validity

    service_access_vc = create_service_access_vc(
        issuer_did=service_did,
        holder_did=bms_did,
        bms_did=bms_did,
        access_levels=access_levels,
        valid_from=now,
        valid_until=valid_until,
    )

    # "Sending" Verifiable Credential to BMS for singing
    log("[BMS] Loading private key...", override=True)
    bms_priv_key = load_private_key(args.bms_password, name=f"{bms_name}_key")

    verification_method = f"{bms_did}#key-1"
    
    log("[BMS] Signing ServiceAccess Verifiable Credential...", override=True)
    signed_vc = sign_vc(service_access_vc, bms_priv_key, verification_method)
    log("Signed ServiceAccess Verifiable Credential:", override=True)
    log(json.dumps(signed_vc, indent=2), override=True)

    # Encrypt the signed VC
    log("[ServiceClient] Encrypting ServiceAccess Verifiable Credential...", override=True)
    
    # TODO Start

    signed_vc_bytes = json.dumps(signed_vc).encode('utf-8')
    enc_message = encrypt_hpke(
        cloud_public_key,
        signed_vc_bytes,
    )

    requestbody = {
        "did": service_did,
        "enc": enc_message["enc"],
        "ciphertext": enc_message["ciphertext"]
    }

    service_priv_key = load_private_key(args.service_password, name=f"{service_name}_key")

    requestbody = sign_payload(
        requestbody,
        service_priv_key
    )
    

    log("[ServiceClient] Body:")
    log(json.dumps(requestbody, indent=2))

    # Send the encrypted VC to the cloud
    log("[ServiceClient] Sending encrypted ServiceAccess Verifiable Credential to Cloud...", override=True)
    
    # TODO: Add actual cloud endpoint URL
    
    # TODO End
    
if __name__ == "__main__":
    main()