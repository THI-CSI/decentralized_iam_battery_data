from util.logging import log
import util.util as service_util
import crypto.crypto as crypto

import sys
import time
import json
import datetime


# TODO Fix maintanence Service
# - It should be possible to fetch the batterypass data from the cloud
def start(bms_did: str):
    # TODO Write Function to fetch this data
    ## We have to provide the did of the Mock BMS via command line argument
    ## 1. fetch did document of the BMS from the blockchain
    ## 2. read bms private key from the bms/mock/utils/keys directory (We have to change the mock_bms keyname to store keys of all BMS's)
    ## 3. fetch did document of the Service Client from the blockchain
    ## 4. Load the private key from client/keys

    service_data = None
    bms_data = None

    # Generate Verifiable Credential
    log.info("[ServiceClient] Generating Verifiable Credential for Service Access...")

    now = datetime.datetime.now(datetime.timezone.utc)

    service_access_vc = service_util.create_service_access_vc(
        issuer_did=bms_data['did'],
        holder_did=service_data['did'],
        bms_did=bms_data['did'],
        access_levels=["read", "write"],
        valid_from=now,
        valid_until=(now + datetime.timedelta(days=365))
    )


    verification_method = f"{bms_data['did']}#key-1"

    log.info("[BMS] Signing ServiceAccess Verifiable Credential...")
    signed_vc = crypto.sign_vc(service_access_vc, bms_data['priv_key'], verification_method)
    log.info("Signed ServiceAccess Verifiable Credential:")
    log(json.dumps(signed_vc, indent=2), override=True)
    time.sleep(2)  # Adding a small delay
    log.info("[ServiceClient] Uploading ServiceAccess Verifiable Credential to Blockchain...")

    if not service_util.upload_vc_to_blockchain(signed_vc):
        log.error("Failed to upload ServiceAccess Verifiable Credential to Blockchain.")
        sys.exit(1)
    log.success("ServiceAccess Verifiable Credential successfully uploaded to Blockchain.")


    log.info("[ServiceClient] Generating Verifiable Presentation from signed VC...")
    vp = service_util.make_vp_from_vc(signed_vc, holder_did=service_data['did'])

    # The verification method for the VP proof must correspond to the holder's key
    vp_verification_method = f"{service_data['did']}#key-1"
    signed_vp = crypto.sign_vp(vp, service_data["priv_key"], vp_verification_method)

    log.info("Signed ServiceAccess Verifiable Presentation:")
    log.info(json.dumps(signed_vp, indent=2))
    exit(0)

    # Encrypt the signed VP
    log.info("[ServiceClient] Encrypting ServiceAccess Verifiable Presentation...")

    signed_vp_bytes = json.dumps(signed_vp).encode('utf-8')
    enc_message = encrypt_hpke(
        service_data['did'],
        cloud_public_key,
        signed_vp_bytes,
    )


    log.info("[ServiceClient] Body:")
    log.info(json.dumps(enc_message, indent=2))


    # Send the encrypted VC to the cloud
    log.info("[ServiceClient] Sending encrypted ServiceAccess Verifiable Credential to Cloud...")

    battery_pass_data = requests.post(f"{os.getenv('BATTERYPASS_URL', 'http://localhost:8000/battery')}/{bms_data['did']}/read",
                                      json=enc_message,
                                      )

    # Check if the request was successful
    if battery_pass_data.status_code == 200:
        log.info("[ServiceClient] Successfully retrieved BatteryPass data from the cloud.")
        log.info(battery_pass_data.json())
    else:
        log.error(f"[ServiceClient] Failed to retrieve BatteryPass data. Status code: {battery_pass_data.status_code}")
        sys.exit(1)