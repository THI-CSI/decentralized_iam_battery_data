import requests

def fill_dids(vc_list, blockchain_url = "http://localhost:8443"):
    dids = []
    for vc in vc_list:
        vc_cloud_did = vc["credentialSubject"]["cloudDid"]
        response = requests.get(f"{blockchain_url}/api/v1/dids/{vc_cloud_did}").json()
        dids.append(response)
    return dids