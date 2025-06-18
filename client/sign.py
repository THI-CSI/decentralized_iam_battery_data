from crypto.crypto import sign_did_external

import sys
import json

with open(sys.argv[1], 'r') as f:
    payload = json.load(f)

verification_method = sys.argv[2] 

signed = sign_did_external(payload, verification_method)

# Return the modified payload as a JSON string via stdout
print(json.dumps(signed))