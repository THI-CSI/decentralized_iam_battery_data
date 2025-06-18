# Client

## Setup

Be sure to start the blockchain and the cloud before starting any client scripts. (Important: Start the Blockchain first.)

```bash
python3 -m venv .venv
source .venv/bin/activate
(In .venv) pip install -r requirements.txt
```

## Service Access 

To simulate a Maintenance access of a Service to a BMS, execute the following, where the passwords can be chosen arbitrarily.

```bash
python3 service_access.py --bms-password 123 --cloud-password 123 --service-password 123 --oem-password 123 --verbose
```