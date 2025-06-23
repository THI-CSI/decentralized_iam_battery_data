#!/usr/bin/env python3

import argparse
import sys
import base64
import uuid
import pathlib
import requests
import os
import uvicorn

from dotenv import load_dotenv
from Crypto.PublicKey import ECC

from util.logging import log, sleep_countdown

import util.util as service_util
import util.oem_service as oem_service
import util.service_access as service_access
import crypto.crypto as crypto


load_dotenv()

KEYS_DIR = pathlib.Path(__file__).parent / "keys"


def setup_entity(entity_name, controller, controller_priv_key, is_bms=False, sn=(uuid.uuid4().hex[:8])):
    log.info(f"Setting up {entity_name.upper()} entity...")
    key_name = f"{entity_name}_key"
    
    log.info(f"Generating {entity_name} key pair...")
    crypto.generate_keys(name=key_name)
    private_key = crypto.load_private_key_as_der(key_name)
    public_key = private_key.public_key()

    public_key_multibase = service_util.ecc_public_key_to_multibase(public_key)

    did = f"did:batterypass:{entity_name}.sn-{sn}"
    did_doc = service_util.build_did_document(did, controller, public_key_multibase, is_bms)

    verification_method = f"{controller}#key-1"
    signed_did_doc = crypto.sign_did(did_doc, controller_priv_key, verification_method)
    log.info(f"{entity_name.upper()} DID document successfully signed")

    log.info(f"Registering {entity_name.upper()} DID in the Blockchain...")
    
    service_util.register_key_with_blockchain(signed_did_doc)
    
    return {
        "priv_key": private_key,
        "pub_key": public_key,
        "did": did,
        "did_doc": signed_did_doc
    }


def is_initialized():
    if not (KEYS_DIR / "oem_key.pem").is_file():
        return False
    if not (KEYS_DIR / "service_key.pem").is_file():
        return False
    return True


def is_service_running(port):
    retry_counter = 5
    while retry_counter > 0:
        try:
            response = requests.get(f"http://localhost:{port}/")
            return response.status_code == 200
        except requests.exceptions.ConnectionError:
            log.error(f"Service is not running closed the connection. Retrying in 1 second...")
        except Exception as e:
            log.error(f"Service is not running: {e}. Retrying in 1 second...")
        retry_counter -= 1
        sleep_countdown(1)
        continue
    return False

def initialize_entities():
    # Check connectivity to Cloud and blockchain
    if not is_service_running(port=8000):
        log.error("Cloud is not running. Please start the Cloud Service.")
        exit(0)
    if not is_service_running(port=8443):
        log.error("Blockchain is not running. Please start the Blockchain Service.")
        exit(0)

    for root, dirs, files in KEYS_DIR.walk(top_down=False):
        for name in files:
            (root / name).unlink()
    if is_initialized():
        KEYS_DIR.rmdir()

    # TODO: Use EU Private Key from testkeys directory
    # EU_PRIVATE_KEY is expected to be a Base64 encoded unencrypted DER private key
    eu_private_key_b64 = os.getenv('EU_PRIVATE_KEY')
    if not eu_private_key_b64:
        log.error("EU_PRIVATE_KEY not found.")
        sys.exit(1)
    eu_private_key = ECC.import_key(base64.b64decode(eu_private_key_b64))
    log.success(f"Imported EU Private Key as ECC object.")

    oem_data = setup_entity(
        entity_name="oem",
        controller="did:batterypass:eu",
        controller_priv_key=eu_private_key,
        sn="audi"
    )
    sleep_countdown(1)

    service_data = setup_entity(
        entity_name="service",
        controller="did:batterypass:eu",
        controller_priv_key=eu_private_key,
        sn="service"
    )
    sleep_countdown(1)
    log.success("Successfully initialized the Test Setup for the OEM and the Service.")


def main():
    parser = argparse.ArgumentParser(description="Generate keys for BMS and Service Station")
    parser.add_argument("--reinitialize", required=False, action='store_true', help="Initial Test Environment Setup of the EU, OEM and Service DIDs")
    parser.add_argument("--initialize", required=False, action='store_true', help="Initial Test Environment Setup of the EU, OEM and Service DIDs, if it does not exist")
    parser.add_argument("--oem-service", required=False, action='store_true', help="Starts the OEM Service")
    parser.add_argument("--service-access", required=False, action='store_true', help="Starts a Service Access Flow")
    parser.add_argument("--bms-did", type=str, required=False, help="Specify the BMS Did")
    parser.add_argument("--private", required=False, action='store_true', help="Returns private data of a BMS")
    args = parser.parse_args()


    if args.initialize:
        if not is_initialized():
            initialize_entities()
        exit(0)

    if not is_initialized() and not args.reinitialize:
        log.error("Environment not initialized. Please run with --initialize flag.")

        exit(1)

    if args.oem_service:
        uvicorn.run(oem_service.app, host="0.0.0.0", port=8123)
        exit(0)

    if args.reinitialize:
        initialize_entities()
        exit(0)

    if args.service_access:
        if not args.bms_did:
            log.error("BMS DID is required for service access.")
            exit(1)
        bms_did = args.bms_did
        service_access.start(bms_did, "did:batterypass:service.sn-service", args.private)

    sys.exit(0)
if __name__ == "__main__":
    main()