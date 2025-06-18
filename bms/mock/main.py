import os
import requests
import uuid

import utils.data_gen as data_gen
import utils.message_creation as message_creation
import utils.crypto as crypto
import utils.did as did_utils


BMS_FILE_NAME = "bms_key"

BLOCKCHAIN_URL = "http://localhost:8443"
SIGN_SERVICE_URL = "http://localhost:8123"

# Environment Variables
CONTROLLER_DID = os.getenv("CONTROLLER_DID", "did:batterypass:oem.audi")
VERIFICATION_METHOD = os.getenv("VERIFICATION_METHOD", "")

if __name__ == "__main__":
    # 1. Generate BMS Key Pair

    crypto.generate_keys(name=BMS_FILE_NAME)
    private_key = crypto.load_private_key(f"{BMS_FILE_NAME}.der")
    public_key = private_key.public_key()

    public_key_multibase = crypto.ecc_public_key_to_multibase(public_key)

    # 2. Generate BMS DID
    did_bms = f"did:batterypass:bms.sn-{(uuid.uuid4().hex[:8])}"

    did_document = did_utils.build_did_document(did_bms, VERIFICATION_METHOD, public_key_multibase)
    # 3. Sign DID with Client's sign service
    response = requests.post(f"{SIGN_SERVICE_URL}/sign/did", json={
        "did": did_bms,
        "verification_method": VERIFICATION_METHOD
    })
    if response.status_code != 200:
        print("Error while signing DID.")
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
    print("BMS registered successfully.")

    # 5. Get DID from Controller (OEM)
    response = requests.get(f"{BLOCKCHAIN_URL}/api/v1/dids/{CONTROLLER_DID}")
    if response.status_code != 200:
        print("Error while getting Controller DID from the blockchain.")
        exit(1)

    controller_did = response.json()



    # TODO 6. Create VC
    # Create CloudInstanceVC
    vc_document = {}

    # TODO 7. Sign VC
    # Sign CloudInstanceVC with OEM (Use clients sign service)
    #response = requests.post(f"{SIGN_SERVICE_URL}/sign/vc", json={})
    #if response.status_code != 200:
    #    print("Error while signing VC.")
    #    exit(1)

    # TODO 8. Register VC.
    response = requests.post(
        f"{BLOCKCHAIN_URL}/api/v1/vcs/create",
        headers={'Content-type': 'application/json'},
        json=vc_document
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
        #encrypted_data = message_creation.message_creation(battery_data, public_key)
        encrypted_data = battery_data

        # Upload Data
        response = requests.post(f"{url}/batterypass/{did_bms}", json={"data": encrypted_data})
        if response.status_code == 200:
            print(f"Data for {did_string} sent successfully.")

