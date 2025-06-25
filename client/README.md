# Client

## Setup

Be sure to start the blockchain and the cloud before starting any client scripts. (Important: Start the Blockchain first.)

```bash
python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

## Usage
You can initialize the client with the `--initialize` flag:
```shell
python3 main.py --initialize
```

To start the OEM-Service, you can use the `--oem-service` flag:
```shell
python3 main.py --oem-service
```

You can also reinitialize the keys with the `--reinitialize` flag:
```shell
python3 main.py --reinitialize
```

To execute the service access flow, you can use the `--service-access` flag.

To get the private batterypass data of a BMS, you can use the `--private` flag:
```shell
python3 main.py --service-access --bms-did <bms-did> --private | grep -E "numberOfFullCycles|remainingCapacity|roundTripEfficiencyat50PerCentCycleLife|expectedNumberOfCycles"
```

To get the public data of the batterypass, you can just use  the `--service-access` and `--bms-did <bms-did>` flag without the `--private` flag:
```shell
python3 main.py --service-access --bms-did <bms-did> | grep -E "roundTripEfficiencyat50PerCentCycleLife|expectedNumberOfCycles"
```
