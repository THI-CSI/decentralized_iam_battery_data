# BMS (Battery Management System)

## Mock BMS
### Usage

Run the Mock BMS:
```shell
python3 main.py
```

Run the Mock BMS with the new data generator (WIP):
```shell
NEW_DATA_GEN="true" python3 main.py
```


Run the Mock BMS in a docker container:
```shell
docker build -f build/dockerfiles/bms.Dockerfile -t bms .
docker run --rm -it --network host bms
```