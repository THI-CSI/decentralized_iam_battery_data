#!/usr/bin/env python3

import argparse
import json
import sys
import uuid
import pathlib
from datetime import datetime, timedelta, timezone

from crypto.crypto import load_private_key, get_public_key, generate_keys, encrypt_hpke, decrypt_hpke, sign_vc, sign_payload, sign_vp, sign_did, single_line_to_pem, pem_to_single_line
from Crypto.PublicKey import ECC, RSA 
from util.util import  build_did_document, create_service_access_vc, make_vp_from_vc, register_key_with_blockchain, upload_vc_to_blockchain
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
    public_key_pem = get_public_key(KEYS_DIR, password, name=key_name)
    public_key = ECC.import_key(public_key_pem)
    
    
    did = f"did:batterypass:{entity_name}.sn-{sn}"
    did_doc = build_did_document(did, controller, public_key_pem, is_bms)
    
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
        global verbose
        verbose = True

    # Connectivity Test to Cloud
    log("[ServiceClient] Sending GET Request to Clound Endpoint to ensure connection...", override=True)
    requests_url = os.getenv('CLOUD_URL')
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

    eu_private_key = ECC.import_key(single_line_to_pem(os.getenv('EU_PRIVATE_KEY')))
    
    oem_data = setup_entity(
        entity_name="oem",
        password=args.oem_password,
        controller="did:batterypass:eu",
        controller_priv_key=eu_private_key,
        sn="audi"
    )
    
    bms_data = setup_entity(
        entity_name="bms",
        password=args.bms_password,
        controller=oem_data['did'],
        controller_priv_key=oem_data['priv_key'],
        sn="544b51e7"
    )

    service_data = setup_entity(
        entity_name="service",
        password=args.service_password,
        controller="did:batterypass:eu",
        controller_priv_key=eu_private_key,
        sn="service1"
    )

    log("Successfully generated keys and DID documents for BMS and Service Station.", override=True)
    log("-" * 40, override=True)
    # Generate Verifiable Credential
    log("[ServiceClient] Generating Verifiable Credential...", override=True)
    
    now = datetime.now(timezone.utc).replace(microsecond=0)

    service_access_vc = create_service_access_vc(
        issuer_did=service_data['did'],
        holder_did=bms_data['did'],
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

    log("[ServiceClient] Uploading ServiceAccess Verifiable Credential to Blockchain...", override=True)
    if not upload_vc_to_blockchain(signed_vc):
        log("Failed to upload ServiceAccess Verifiable Credential to Blockchain.", level="error", override=True)
        sys.exit(1)
    log("ServiceAccess Verifiable Credential successfully uploaded to Blockchain.", override=True)


    log("[ServiceClient] Generating Verifiable Presentation from signed VC...", override=True)
    vp = make_vp_from_vc(signed_vc, holder_did=service_data['did'])

    signed_vp = sign_vp(vp, service_data["priv_key"], verification_method)
    
    log("Signed ServiceAccess Verifiable Presentation:", override=True)
    log(json.dumps(signed_vp, indent=2), override=True)


    # Encrypt the signed VC
    log("[ServiceClient] Encrypting ServiceAccess Verifiable Presentation...", override=True)
    
    signed_vp_bytes = json.dumps(signed_vp).encode('utf-8')
    enc_message = encrypt_hpke(
        cloud_public_key,
        signed_vp_bytes,
    )

    requestbody = {
        "did": service_data["did"],
        "enc": enc_message["enc"],
        "ciphertext": enc_message["ciphertext"]
    }

    requestbody = sign_payload(
        requestbody,
        service_data["priv_key"],
    )
   
    log("[ServiceClient] Body:")
    log(json.dumps(requestbody, indent=2))

    # Send the encrypted VC to the cloud
    log("[ServiceClient] Sending encrypted ServiceAccess Verifiable Credential to Cloud...", override=True)
if __name__ == "__main__":
    main()