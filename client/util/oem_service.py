from fastapi import FastAPI, Body, Response
from typing import Any
from crypto.crypto import sign_did_external, sign_vc_external

import crypto.crypto as crypto

import sys
import os
import json
import requests

app = FastAPI()

OEM_DID = os.getenv("OEM_DID", "did:batterypass:oem.sn-audi")

BLOCKCHAIN_URL = os.getenv("BLOCKCHAIN_URL", "http://localhost:8443")
TESTING_SETUP = os.getenv("TESTING_SETUP", "true").lower() == "true"

@app.post("/sign/vc")
def sign_vc_service(response: Response, request: Any = Body(None)):
    response.status_code = 400

    try:
        data = json.loads(request)
    except:
        return {"error": "Invalid JSON"}

    if "vc" not in data:
        return {"error": "vc is required"}
    if "verification_method" not in data:
        return {"error": "verification_method is required"}
    vc = data["vc"]
    verification_method = f"{data["verification_method"]}#key-1"

    try:
        signed_vc = sign_vc_external(vc, verification_method)
    except Exception as e:
        return {"error": "Failed to sign VC", "message": e}

    response.status_code = 200
    return signed_vc

@app.post("/sign/did")
def sign_did_service(response: Response, request: Any = Body(None)):
    response.status_code = 400

    try:
        data = json.loads(request)
    except:
        return {"error": "Invalid JSON"}

    if "did" not in data:
        return {"error": "did is required"}
    if "verification_method" not in data:
        return {"error": "verification_method is required"}
    did = data["did"]
    verification_method = f"{data["verification_method"]}#key-1"

    try:
        signed_did = sign_did_external(did, verification_method)
    except:
        return {"error": "Failed to sign DID"}

    response.status_code = 200
    return signed_did



@app.post("/batterypass/{bms_did}")
def create_batterypass(bms_did: str, response: Response, request: Any = Body(None)):
    response.status_code = 400

    if "cloudDid" not in request:
        return {"error": "cloudDid is required"}
    if "encryptedData" not in request:
        return {"error": "encryptedData is required"}
    cloud_did = request["cloudDid"]
    encrypted_data = request["encryptedData"]

    # TODO 1. Decrypt Data from BMS
    oem_private_key = crypto.load_private_key_as_der("oem_key")
    decrypted_data = "{}"
    try:
        decrypted_data = crypto.decrypt_and_verify(oem_private_key, json.dumps(encrypted_data))
    except:
        response.status_code = 400
        return {"error": "Failed to decrypt data from BMS"}

    # 2. Get Cloud DID from Blockchain
    resp = requests.get(f"{BLOCKCHAIN_URL}/api/v1/dids/{cloud_did}")
    if resp.status_code != 200:
        response.status_code = 404
        print(resp.text)
        print(f"Error while getting Cloud DID '{cloud_did}'.")
        return {"error": "Cloud DID not found" }

    cloud_did_document = resp.json()
    print(json.dumps(cloud_did_document, indent=2))

    # 3. Encrypt Data for Cloud
    decrypted_data_string = decrypted_data.decode("utf-8")
    print(decrypted_data_string)
    encrypted_data = crypto.encrypt_data_from_did(OEM_DID, cloud_did_document["verificationMethod"]["publicKeyMultibase"], decrypted_data_string, oem_private_key)

    # 4. Create Battery pass
    url = cloud_did_document["service"][0]["serviceEndpoint"]
    if TESTING_SETUP:
        url = url.replace("api-service", "localhost")

    resp = requests.put(f"{url}/batterypass/create/{bms_did}", json=encrypted_data)
    if resp.status_code != 200:
        response.status_code = 400
        print(resp.text)
        print(f"Error while creating Batterypass for {bms_did} on cloud {cloud_did}.")
        return {"error": "Failed to create Batterypass"}

    response.status_code = 200
    return {"success": "Batterypass created successfully"}



# Run it with:
# ```shell
# uvicorn sign_service:app --port 8123
# ```
