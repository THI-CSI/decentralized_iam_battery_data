# BMS (Battery Management System)

## Mock BMS
### Usage

Run the Mock BMS:
```shell
python3 main.py
```

You can specify the interval of generating new data in minutes with the `INTERVAL_MIN` environment variable flag:
```shell
# This will generate every 6 seconds new data (default: 1 minute)
INTERVAL_MIN=0.1 python3 main.py
```


Run the Mock BMS in a docker container:
```shell
docker build -f build/dockerfiles/bms.Dockerfile -t bms .
docker run --rm -it --network host bms
```

