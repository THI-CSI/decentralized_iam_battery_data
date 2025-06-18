import os
import requests

from utils.data_gen import run_battery_data_generator
from utils.message_creation import message_creation

BLOCKCHAIN_URL = "http://localhost:8443"


# TODO 1. Key Generierenen
os.getenv("CONTROLLER_DID", "did:batterypass:oem.audi")

# TODO 2. DID generieren
did_bms = "did:batterypass:bms.abcd"

did_document = {}
# TODO 3. Client zum signieren des DIDs nutzen
## Client Endpoint to sign a DID

# TODO 4. Register BMS on Blockchain
requests.post(f"{BLOCKCHAIN_URL}/api/v1/dids/createormodify", json={"id": did_bms, "service": [{"type": "BMS", "serviceEndpoint": "http://localhost:8080/bms"}]})
print("BMS registered successfully.")

# TODO 5. Get DID from Controller (OEM)


vcs = ["did:batterypass:cloud.sn-central"]
dids = []
for vc in vcs:
    dids.append(requests.get(f"{BLOCKCHAIN_URL}/api/v1/dids/{vc}").json())


# 6. Daten generieren
battery_data = run_battery_data_generator()

for did in dids:
    url = did["service"][0]["serviceEndpoint"]
    did_string = did["id"]
    public_key = did["verificationMethod"]["publicKeyMultibase"]
    # TODO 7. Encrypt Data for Cloud
    #encrypted_data = message_creation(battery_data, public_key)
    encrypted_data = battery_data
    # 8. Upload Data
    response = requests.post(f"{url}/batterypass/{did_bms}", json={"data": encrypted_data})
    if response.status_code == 200:
        print(f"Data for {did_string} sent successfully.")