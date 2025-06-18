from fastapi import FastAPI, Body, Response
from typing import Any
from crypto.crypto import sign_did_external, sign_vc_external

import sys
import json

app = FastAPI()


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
    verification_method = data["verification_method"]

    try:
        signed_vc = sign_vc_external(vc, verification_method)
    except:
        return {"error": "Failed to sign VC"}

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
    verification_method = data["verification_method"]

    try:
        signed_did = sign_did_external(did, verification_method)
    except:
        return {"error": "Failed to sign DID"}

    response.status_code = 200
    return signed_did

# Run it with:
# ```shell
# uvicorn sign_service:app --port 8123
# ```
