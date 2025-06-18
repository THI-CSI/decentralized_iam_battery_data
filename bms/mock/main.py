import os
import requests
import uuid
import json
from datetime import datetime, timedelta, timezone

import utils.data_gen as data_gen
import utils.crypto as crypto
import utils.did as did_utils


BMS_FILE_NAME = "bms_key"

BLOCKCHAIN_URL = "http://localhost:8443"
OEM_SIGN_SERVICE_URL = os.getenv("OEM_SIGN_SERVICE_URL", "http://localhost:8123")

# Environment Variables
CONTROLLER_DID = os.getenv("CONTROLLER_DID", "did:batterypass:oem.audi")
SN = os.getenv("SN", (uuid.uuid4().hex[:8]))
CLOUD_DID = os.getenv("CLOUD_DID", "did:batterypass:cloud.centralcloud")

if __name__ == "__main__":
    # 1. Generate BMS Key Pair

    crypto.generate_keys(name=BMS_FILE_NAME)
    private_key = crypto.load_private_key(f"{BMS_FILE_NAME}.der")
    public_key = private_key.public_key()

    public_key_multibase = crypto.ecc_public_key_to_multibase(public_key)

    # 2. Generate BMS DID
    did_bms = f"did:batterypass:bms.sn-{(uuid.uuid4().hex[:8])}"

    did_document = did_utils.build_did_document(did_bms, CONTROLLER_DID, public_key_multibase)
    # 3. Sign DID with Client's sign service
    response = requests.post(f"{OEM_SIGN_SERVICE_URL}/sign/did", json=json.dumps({
        "did": did_document,
        "verification_method": CONTROLLER_DID
    }))
    if response.status_code != 200:
        print("Error while signing DID.")
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
        print("Error while registering BMS on Blockchain.")
        exit(1)
    print(f"BMS {SN} registered successfully.")

    # 5. Get DID from Controller (OEM)
    response = requests.get(f"{BLOCKCHAIN_URL}/api/v1/dids/{CONTROLLER_DID}")
    if response.status_code != 200:
        print("Error while getting Controller DID from the blockchain.")
        exit(1)

    controller_did = response.json()



    # 6. Create VC
    # Create CloudInstanceVC

    now = datetime.now(timezone.utc)

    vc_document = did_utils.create_cloud_instance_vc(
        CONTROLLER_DID, # OEM DID (Controller DID)
        did_bms, # BMS DID
        CLOUD_DID, # Cloud DID
        now, #Today
        (now + timedelta(days=365)) # Valid for 1 year
    )

    # 7. Sign VC
    # Sign CloudInstanceVC with OEM (Use clients sign service)
    response = requests.post(f"{OEM_SIGN_SERVICE_URL}/sign/vc", json=json.dumps({
        "vc": vc_document,
        "verification_method": CONTROLLER_DID
    }))
    if response.status_code != 200:
        print("Error while signing VC.")
        exit(1)
    signed_vc = response.json()
    
    # TODO 8. Register VC.
    response = requests.post(
        f"{BLOCKCHAIN_URL}/api/v1/vcs/create/cloud",
        headers={'Content-type': 'application/json'},
        json=signed_vc
    )

    if response.status_code != 200:
        print("Error while registering VC on Blockchain.")
        exit(1)


    vcs = ["did:batterypass:cloud.sn-central"]
    dids = []
    for vc in vcs:
        response = requests.get(f"{BLOCKCHAIN_URL}/api/v1/dids/{vc}").json()
        dids.append(response)


    # Generate Data
    # TODO use updated version from 'feat/mbms-data-gen'
    battery_data = data_gen.run_battery_data_generator()

    for did in dids:
        url = did["service"][0]["serviceEndpoint"]
        did_string = did["id"]
        public_key = did["verificationMethod"]["publicKeyMultibase"]

        # TODO Encrypt Data for Cloud
        encrypted_data = crypto.encrypt_hpke(did_string, public_key, battery_data)

        # Upload Data
        response = requests.post(f"{url}/batterypass/read/{did_bms}", json={"data": encrypted_data})
        if response.status_code == 200:
            print(f"Data for {did_string} sent successfully.")

