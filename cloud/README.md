# Cloud

The Cloud API serves as an endpoint for battery data ingestion 
and management of that data inside a Battery Pass database.

Per default the API is available at [http://localhost:8000](http://localhost:8000)
with the UI being available at [http://localhost:8501](http://localhost:8501).

## Usage

The API is written in Python and can be run with Docker Compose.

### Requirements

| Package               | Version                  |
|-----------------------|--------------------------|
| Docker                | *Any*                    |
| Docker Compose Plugin | *Any*                    |
| Python                | 3.12                     |
| PIP packages          | *See `requirements.txt`* |

### Initialization

Create a `.env` file containing `PASSPHRASE` and, if wanted, `BLOCKCHAIN_URL` to specify the blockchain endpoint.

```shell
echo "PASSPHRASE=$(python -c 'import uuid; print(uuid.uuid4())')" > .env
```

Run `docker compose build` to build the containers:

```shell
docker compose build
```

Run `docker compose up -d` to start it:

```shell
docker compose up -d
```

Run `docker logs` to inspect the logs (CTRL + C to exit):

```shell
docker logs -f cloud
```

Run `docker compose down` to stop the cloud stack:
```shell
docker compose down
```