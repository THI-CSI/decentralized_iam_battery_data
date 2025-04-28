# Cloud

The Cloud API serves as an endpoint for battery data ingestion 
and management of that data inside a Battery Pass database.

## Usage

The API is written in Python and can be run with Docker.

### Requirements

| Package      | Version                  |
|--------------|--------------------------|
| Docker       | *Any*                    |
| Python       | 3.12                     |
| PIP packages | *See `requirements.txt`* |

### Initialization

Run `docker build` to build the container:

```shell
docker build -t cloud-api .
```

Run `docker run` to start it:

```shell
docker run --name cloud -p 8000:8000 -d cloud-api
```

Run `docker logs` to inspect the logs (CTRL + C to exit):

```shell
docker logs -f cloud
```