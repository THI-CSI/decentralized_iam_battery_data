#!/usr/bin/env python3

import argparse
import json
import sys
import base64
import uuid
import pathlib
import time
from datetime import datetime, timedelta, timezone

from crypto.crypto import load_private_key, get_public_key, generate_keys, encrypt_hpke, decrypt_hpke, sign_vc, sign_vp, sign_did
from Crypto.PublicKey import ECC, RSA 
from util.util import  ecc_public_key_to_multibase, build_did_document, create_service_access_vc, make_vp_from_vc, register_key_with_blockchain, upload_vc_to_blockchain
from multiformats import multibase
from dotenv import load_dotenv
load_dotenv()

import logging
from pyld import jsonld
import requests
import os
import random 


KEYS_DIR = pathlib.Path(__file__).parent / "keys"
verbose = False

def log(message, level="info", override=False):
    if verbose or override:
        print(f"[{level.upper()}] {message}")


def setup_entity(entity_name, password, controller, controller_priv_key, is_bms=False, sn=(uuid.uuid4().hex[:8])):
    """
    Generates keys, creates a DID, signs the DID Document, and registers it.

    Args:
        entity_name (str): The name for the entity (e.g., "bms", "service").
        password (str): The password to encrypt the private key.
        controller (str): The DID of the controller (e.g., "did:batterypass:oem").
        controller_priv_key (ECC.EccKey): The private key of the controller.
        is_bms (bool): Flag to indicate if the entity is a BMS.

    Returns:
        dict: Contains the entity's keys, DID, and signed DID document.
    """
    log(f"--- Setting up entity: {entity_name.upper()} ---", override=True)
    key_name = f"{entity_name}_key"
    
    log(f"Generating {entity_name} key pair...")
    generate_keys(password, name=key_name)
    private_key = load_private_key(password, name=key_name)
    public_key = private_key.public_key()

    # Convert to multibase
    public_key_multibase = ecc_public_key_to_multibase(public_key)

    print(public_key_multibase)


    did = f"did:batterypass:{entity_name}.sn-{sn}"
    did_doc = build_did_document(did, controller, public_key_multibase, is_bms)
    log(json.dumps(did_doc, indent=2))
  
    verification_method = f"{controller}#key-1"
    signed_did_doc = sign_did(did_doc, controller_priv_key, verification_method)
    log(f"\n{entity_name.upper()} Signed DID Document:")
    log(json.dumps(signed_did_doc, indent=2))
    
    log(f"Registering {entity_name.upper()} DID with Blockchain...")
    
    register_key_with_blockchain(signed_did_doc)
    
    return {
        "priv_key": private_key,
        "pub_key": public_key,
        "did": did,
        "did_doc": signed_did_doc
    }



def main():

  
    parser = argparse.ArgumentParser(description="Generate keys for BMS and Service Station")
    parser.add_argument("--bms-password", required=True, help="Password to encrypt BMS private key")
    parser.add_argument("--service-password", required=True, help="Password to encrypt Service Station private key")
    parser.add_argument("--oem-password", required=True, help="Password to encrypt OEM private key")
    parser.add_argument("--verbose", required=False, action='store_true', help="Enable verbose output")
    args = parser.parse_args()
    if args.verbose:
        log("[ServiceClient] Verbose mode enabled.", override=True)
        global verbose
        verbose = True

    # Connectivity Test to Cloud
    log("[ServiceClient] Sending GET Request to Clound Endpoint to ensure connection...", override=True)
    requests_url = os.getenv('CLOUD_URL', 'http://localhost:8000') # Added a default for testing
    cloud_public_key = None
    response = requests.get(requests_url)

    if response.status_code == 200:
        log(f"Successfully connected to {requests_url}", override=True)
    
        # This is a Base64 encoded string of a DER key
        base64_der_key = response.json().get("publicKeyMultibase", None)
        log(f"Cloud Public Key (Base64-DER): {base64_der_key}", override=True)

        # Decode the Base64 string to get the raw DER bytes
        der_key = base64.b64decode(base64_der_key)
    
        # Now, import the DER-formatted key (which is in bytes)
        cloud_public_key = ECC.import_key(der_key)
    
        log(f"Successfully imported Cloud Public Key as ECC object.", override=True)
    else:
        log(f"Failed to connect to {requests_url}. Status code: {response.status_code}", level="error", override=True)
        sys.exit(1)

    # EU_PRIVATE_KEY is expected to be a Base64 encoded unencrypted DER private key
    eu_private_key_b64 = os.getenv('EU_PRIVATE_KEY')
    if not eu_private_key_b64:
        log("EU_PRIVATE_KEY environment variable not set.", level="error", override=True)
        sys.exit(1)
    eu_private_key = ECC.import_key(base64.b64decode(eu_private_key_b64))
    log(f"Successfully imported EU Private Key as ECC object.", override=True)
    
    oem_data = setup_entity(
        entity_name="oem",
        password=args.oem_password,
        controller="did:batterypass:eu",
        controller_priv_key=eu_private_key,
        sn="audi"
    )
    time.sleep(1)  # Adding a small delay
    
    bms_data = setup_entity(
        entity_name="bms",
        password=args.bms_password,
        controller=oem_data['did'],
        controller_priv_key=oem_data['priv_key'],
        sn="544b51e7"
    )
    time.sleep(1)  # Adding a small delay
    
    service_data = setup_entity(
        entity_name="service",
        password=args.service_password,
        controller="did:batterypass:eu",
        controller_priv_key=eu_private_key,
        sn="service"
    )
    
    log("Successfully generated keys and DID documents for BMS and Service Station.", override=True)
    log("-" * 40, override=True)
    # Generate Verifiable Credential
    log("[ServiceClient] Generating Verifiable Credential...", override=True)
    
    now = datetime.now(timezone.utc)

    service_access_vc = create_service_access_vc(
        issuer_did=bms_data['did'],
        holder_did=service_data['did'],
        bms_did=bms_data['did'],
        access_levels=["read", "write"],
        valid_from=now,
        valid_until=(now + timedelta(days=365))
    )
    

    verification_method = f"{bms_data['did']}#key-1"
    
    log("[BMS] Signing ServiceAccess Verifiable Credential...", override=True)
    signed_vc = sign_vc(service_access_vc, bms_data['priv_key'], verification_method)
    log("Signed ServiceAccess Verifiable Credential:", override=True)
    log(json.dumps(signed_vc, indent=2), override=True)
    time.sleep(2)  # Adding a small delay
    log("[ServiceClient] Uploading ServiceAccess Verifiable Credential to Blockchain...", override=True)
    
    if not upload_vc_to_blockchain(signed_vc):
        log("Failed to upload ServiceAccess Verifiable Credential to Blockchain.", level="error", override=True)
        sys.exit(1)
    log("ServiceAccess Verifiable Credential successfully uploaded to Blockchain.", override=True)


    log("[ServiceClient] Generating Verifiable Presentation from signed VC...", override=True)
    vp = make_vp_from_vc(signed_vc, holder_did=service_data['did'])

    # The verification method for the VP proof must correspond to the holder's key
    vp_verification_method = f"{service_data['did']}#key-1"
    signed_vp = sign_vp(vp, service_data["priv_key"], vp_verification_method)
    
    log("Signed ServiceAccess Verifiable Presentation:", override=True)
    log(json.dumps(signed_vp, indent=2), override=True)
    exit(0)

    # Encrypt the signed VP
    log("[ServiceClient] Encrypting ServiceAccess Verifiable Presentation...", override=True)
    
    signed_vp_bytes = json.dumps(signed_vp).encode('utf-8')
    enc_message = encrypt_hpke(
        service_data['did'],
        cloud_public_key,
        signed_vp_bytes,
    )


    log("[ServiceClient] Body:")
    log(json.dumps(enc_message, indent=2))


    # Send the encrypted VC to the cloud
    log("[ServiceClient] Sending encrypted ServiceAccess Verifiable Credential to Cloud...", override=True)

    battery_pass_data = requests.post(f"{os.getenv('BATTERYPASS_URL', 'http://localhost:8000/battery')}/{bms_data['did']}/read", 
                                      json=enc_message,
                                      )
    
    # Check if the request was successful
    if battery_pass_data.status_code == 200:
        log("[ServiceClient] Successfully retrieved BatteryPass data from the cloud.", override=True)
        log(battery_pass_data.json(), override=True)
    else:
        log(f"[ServiceClient] Failed to retrieve BatteryPass data. Status code: {battery_pass_data.status_code}", level="error", override=True)
        sys.exit(1)

    
    sys.exit(0)
if __name__ == "__main__":
    main()