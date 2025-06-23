import os
import requests
import uuid
import json
import time
import urllib.parse as urllib
from datetime import datetime, timedelta, timezone

import utils.battery_data as battery_data_generator
import utils.crypto as crypto
import utils.w3c as w3c_util
import utils.util as mock_util
from utils.logging import log, sleep_countdown



BLOCKCHAIN_URL = os.getenv("BLOCKCHAIN_URL", "http://localhost:8443")
OEM_SIGN_SERVICE_URL = os.getenv("OEM_SIGN_SERVICE_URL", "http://localhost:8123")

# Environment Variables
CONTROLLER_DID = os.getenv("CONTROLLER_DID", "did:batterypass:oem.sn-audi")
CLOUD_DIDS = os.getenv("CLOUD_DIDS", "did:batterypass:cloud.sn-central")
INTERVAL_MIN = os.getenv("INTERVAL_MIN", "1")
TESTING_SETUP = os.getenv("TESTING_SETUP", "true").lower() == "true"

VCs = []

SN = os.getenv("SN", (uuid.uuid4().hex[:8]))
BMS_FILE_NAME = f"bms_{SN}"


if __name__ == "__main__":
    # 1. Generate BMS Key Pair

    crypto.generate_keys(name=BMS_FILE_NAME)
    private_key = crypto.load_private_key_as_der(BMS_FILE_NAME)
    public_key = private_key.public_key()

    public_key_multibase = crypto.ecc_public_key_to_multibase(public_key)

    # 2. Generate BMS DID
    did_bms = f"did:batterypass:bms.sn-{SN}"
    log.info(f"BMS: {log.color.BOLD+log.color.UNDERLINE}{did_bms}{log.color.RESET}")

    did_document = w3c_util.build_did_document(did_bms, CONTROLLER_DID, public_key_multibase)
    # 3. Sign DID with Client's sign service
    response = requests.post(f"{OEM_SIGN_SERVICE_URL}/sign/did", json=json.dumps({
        "did": did_document,
        "verification_method": CONTROLLER_DID
    }))
    if response.status_code != 200:
        log.error("Error while signing DID.")
        print(response.text)
        exit(1)

    signed_did = response.json()
    # 4. Register BMS on Blockchain
    response = requests.post(
        f"{BLOCKCHAIN_URL}/api/v1/dids/createormodify",
        headers={'Content-type': 'application/json'},
        json=signed_did
    )

    if response.status_code != 200:
        log.error("Error while registering BMS on Blockchain.")
        print(response.text)
        exit(1)

    # 5. Get DID from Controller (OEM)
    response = requests.get(f"{BLOCKCHAIN_URL}/api/v1/dids/{CONTROLLER_DID}")
    if response.status_code != 200:
        log.error("Error while getting Controller DID from the blockchain.")
        exit(1)

    controller_did = response.json()


    log.success(f"Registering BMS DID '{did_bms}' in the Blockchain...")
    time.sleep(1)

    # 6. Create VC
    # Create CloudInstanceVC

    now = datetime.now(timezone.utc)

    # Split CLOUD_DIDs by ','
    CLOUD_DIDS_SPLIT = CLOUD_DIDS.split(',')
    for CLOUD_DID in CLOUD_DIDS_SPLIT:
        vc_document = w3c_util.create_cloud_instance_vc(
            CONTROLLER_DID,  # OEM DID (Controller DID)
            did_bms,  # BMS DID
            CLOUD_DID,  # Cloud DID
            now,  # Today
            (now + timedelta(days=365))  # Valid for 1 year
        )

        # 7. Sign VC
        # Sign CloudInstanceVC with OEM (Use clients sign service)
        response = requests.post(f"{OEM_SIGN_SERVICE_URL}/sign/vc", json=json.dumps({
            "vc": vc_document,
            "verification_method": CONTROLLER_DID
        }))
        if response.status_code != 200:
            log.error("Error while signing VC.")
            print(response.text)
            exit(1)
        signed_vc = response.json()
        # 8. Register VC.
        response = requests.post(
            f"{BLOCKCHAIN_URL}/api/v1/vcs/create/cloud",
            headers={'Content-type': 'application/json'},
            json=signed_vc
        )

        if response.status_code != 200:
            log.error("Error while registering VC on Blockchain.")
            print(response.text)
            exit(1)

        VCs.append(signed_vc)

        log.success(f"Registering VC for '{CLOUD_DID}' in the Blockchain...")
        time.sleep(1)

    dids = mock_util.fill_dids(VCs, BLOCKCHAIN_URL)

    # Data Generator
    battery_data = battery_data_generator.get_battery_data()

    for did in dids:
        url = did["service"][0]["serviceEndpoint"]
        oem_public_key = controller_did["verificationMethod"]["publicKeyMultibase"]

        if TESTING_SETUP:
            url = url.replace("api-service", "localhost")

        response = requests.get(f"{url}/batterypass/{did_bms}")
        if response.status_code != 200:

            log.success("Creating Batterypass at the cloud through the OEM Service...")
            encrypted_data = crypto.encrypt_data_from_did(did_bms, oem_public_key, battery_data, private_key)

            response = requests.post(
                f"{OEM_SIGN_SERVICE_URL}/batterypass/{did_bms}",
                json={
                "cloudDid": did["id"],
                "encryptedData": encrypted_data
            })
            if response.status_code != 200:
                log.error("Batterypass not created.")
                print(response.text)
                exit(1)

    print('-'*32)
    log.info(f"QR-Code: http://localhost:8000/batterypass/qr/{urllib.quote_plus(did_bms)}?url={urllib.quote_plus(f'http://localhost:8501')}")
    log.info(f"Blockchain Explorer: http://localhost:8443/dids/{urllib.quote_plus(did_bms)}")
    log.info(f"BatteryPass Data Viewer: http://localhost:8501/?did={urllib.quote_plus(did_bms)}")
    print('-'*32)

    try:
        while True:
            dids = mock_util.fill_dids(VCs, BLOCKCHAIN_URL)

            # Data Generator
            battery_data = battery_data_generator.get_battery_data_update()

            for did in dids:
                url = did["service"][0]["serviceEndpoint"]
                service_public_key = did["verificationMethod"]["publicKeyMultibase"]
                if TESTING_SETUP:
                    url = url.replace("api-service", "localhost")

                encrypted_data = crypto.encrypt_data_from_did(did_bms, service_public_key, battery_data, private_key)

                # Upload Data
                response = requests.post(f"{url}/batterypass/update/{did_bms}", json=encrypted_data)

                if response.status_code != 200:
                    log.error(f"Error while uploading data for {did['id']}.")
                    print(response.text)
                    exit(1)
                else:
                    log.flow(f"Data for {did['id']} sent successfully.")

            sleep_countdown(int(float(INTERVAL_MIN) * 60))

    except KeyboardInterrupt:
        log.info("Stopping BMS Mock...")
        exit(0)

