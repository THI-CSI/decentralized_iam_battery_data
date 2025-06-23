from util.logging import log
import util.util as service_util
import crypto.crypto as crypto
from Crypto.PublicKey import ECC
import sys, os
import time
import json
import datetime
import pathlib
import requests


BLOCKCHAIN_URL = os.getenv("BLOCKCHAIN_URL", "http://localhost:8443")
TESTING_SETUP = os.getenv("TESTING_SETUP", "true").lower() == "true"

def retrieve_cloud_data():
    cloud_did = "did:batterypass:cloud.sn-central"
    response = requests.get(f"{BLOCKCHAIN_URL}/api/v1/dids/{cloud_did}")

    if response.status_code != 200:
        log.error("Error while getting Cloud DID from the blockchain.")
        print(response.text)
        exit(1)

    cloud_did_document = response.json()
    cloud_public_key = cloud_did_document["verificationMethod"]["publicKeyMultibase"]
    cloud_url = cloud_did_document["service"][0]["serviceEndpoint"]

    if TESTING_SETUP:
        cloud_url = cloud_url.replace("api-service", "localhost")

    return cloud_url, cloud_public_key


def read_bms_data(bms_did: str, enc_message: bytes or None, cloud_url: str):
    battery_pass_data = requests.post(f"{cloud_url}/batterypass/read/{bms_did}", json=enc_message)
    # Check if the request was successful
    if battery_pass_data.status_code != 200:
        log.error(f"[ServiceClient] Failed to retrieve BatteryPass data. Status code: {battery_pass_data.status_code}")
        log.debug(battery_pass_data.text)
        sys.exit(1)
    log.info("[ServiceClient] Successfully retrieved BatteryPass data from the cloud.")
    return battery_pass_data.json()


def load_bms_private_key_as_der(name: str = "key") -> ECC.EccKey:
    key_file = pathlib.Path(__file__).parent.parent.parent / "bms" / "mock" / "utils" / "keys" / f"{name}.pem"
    assert key_file.is_file(), f"Key file not found: {key_file}"
    key = None
    with open(key_file, "rt") as f:
        key = ECC.import_key(f.read())
    return key


def start(bms_did: str, service_did: str, private_data: bool = False):
    cloud_url, cloud_public_key = retrieve_cloud_data()

    if not private_data:
        log.info("[ServiceClient] Requesting Public Data from Cloud...")
        print(json.dumps(read_bms_data(bms_did, None, cloud_url), indent=2))
        exit(0)

    # Generate Verifiable Credential
    log.info("[ServiceClient] Generating Verifiable Credential for Service Access...")

    now = datetime.datetime.now(datetime.timezone.utc)

    service_access_vc = service_util.create_service_access_vc(
        issuer_did=bms_did,
        holder_did=service_did,
        bms_did=bms_did,
        access_levels=["read", "write"],
        valid_from=now,
        valid_until=(now + datetime.timedelta(days=365))
    )


    verification_method = f"{bms_did}#key-1"

    log.info("[BMS] Signing ServiceAccess Verifiable Credential...")
    bms_sn = f"bms_{bms_did.split("sn-")[1]}"

    signed_vc = crypto.sign_vc(service_access_vc, load_bms_private_key_as_der(bms_sn), verification_method)
    log.debug("Signed ServiceAccess Verifiable Credential:")
    log.debug(json.dumps(signed_vc, indent=2))
    time.sleep(2)
    log.info("[ServiceClient] Uploading ServiceAccess Verifiable Credential to Blockchain...")

    if not service_util.upload_vc_to_blockchain(signed_vc):
        log.error("Failed to upload ServiceAccess Verifiable Credential to Blockchain.")
        exit(1)
    log.success("ServiceAccess Verifiable Credential successfully uploaded to Blockchain.")


    log.info("[ServiceClient] Generating Verifiable Presentation from signed VC...")
    vp = service_util.make_vp_from_vc(signed_vc, holder_did=service_did)

    # The verification method for the VP proof must correspond to the holder's key
    vp_verification_method = f"{service_did}#key-1"
    # Service Private Key
    service_priv_key = crypto.load_private_key_as_der("service_key")
    signed_vp = crypto.sign_vp(vp, service_priv_key, vp_verification_method)

    log.debug("Signed ServiceAccess Verifiable Presentation.")
    log.debug(json.dumps(signed_vp, indent=2))

    # Encrypt the signed VP
    log.info("[ServiceClient] Encrypting ServiceAccess Verifiable Presentation...")

    signed_vp_bytes = json.dumps(signed_vp).encode('utf-8')
    enc_message = crypto.encrypt_hpke(
        service_did,
        cloud_public_key,
        signed_vp_bytes,
    )

    log.debug("[ServiceClient] Body:")
    log.debug(json.dumps(enc_message, indent=2))

    # Send the encrypted VC to the cloud
    log.info("[ServiceClient] Sending encrypted ServiceAccess Verifiable Credential to Cloud...")
    battery_pass_data = json.dumps(read_bms_data(bms_did, enc_message, cloud_url), indent=2)

    log.debug("[ServiceClient] BatteryPass Data:")
    log.debug(battery_pass_data)