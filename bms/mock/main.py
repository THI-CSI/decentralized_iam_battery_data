import os
import requests

from utils.data_gen import run_battery_data_generator
from utils.message_creation import message_creation

BLOCKCHAIN_URL = "http://localhost:8443"
SIGN_SERVICE_URL = "http://localhost:8123"

# Environment Variables
# - CONTROLLER_DID
# - VERIFICATION_METHOD

if __name__ == "__main__":
    # TODO 1. Generate BMS Key Pair
    controller_did = os.getenv("CONTROLLER_DID", "did:batterypass:oem.audi")

    # TODO 2. Generate BMS DID
    did_bms = "did:batterypass:bms.abcd"

    did_document = {}
    # 3. Sign DID with Client's sign service
    response = requests.post(f"{SIGN_SERVICE_URL}/sign/", json={
        "did": did_bms,
        "verification_method": os.getenv("VERIFICATION_METHOD", "")
    })
    if response.status_code != 200:
        print("Error while signing DID.")
        exit(1)

    signed_did = response.json()

    # 4. Register BMS on Blockchain
    response = requests.post(f"{BLOCKCHAIN_URL}/api/v1/dids/createormodify", json=signed_did)

    if response.status_code != 200:
        print("Error while registering BMS on Blockchain.")
        exit(1)
    print("BMS registered successfully.")

    # TODO 5. Get DID from Controller (OEM)

    # TODO 6. Create VC

    # TODO 7. Sign VC

    # TODO 8. Register VC.



    vcs = ["did:batterypass:cloud.sn-central"]
    dids = []
    for vc in vcs:
        dids.append(requests.get(f"{BLOCKCHAIN_URL}/api/v1/dids/{vc}").json())


    # Generate Data
    battery_data = run_battery_data_generator()

    for did in dids:
        url = did["service"][0]["serviceEndpoint"]
        did_string = did["id"]
        public_key = did["verificationMethod"]["publicKeyMultibase"]

        # TODO Encrypt Data for Cloud
        #encrypted_data = message_creation(battery_data, public_key)
        encrypted_data = battery_data

        # Upload Data
        response = requests.post(f"{url}/batterypass/{did_bms}", json={"data": encrypted_data})
        if response.status_code == 200:
            print(f"Data for {did_string} sent successfully.")

