# `tools.py` Documentation

Make sure you are in the `decentralized_iam_battery_data/blockchain` directory.

Run commands using:

```shell
python3 tools.py [cmd] [options]
```

To see all available commands:

```shell
python3 tools.py -h
```

## Docker Setup

The Docker setup launches both the blockchain API and the frontend. Once the setup is running, the application will be accessible at [localhost:8443](http://localhost:8443).

- Swagger Documentation: Access the API documentation at [localhost:8443/swagger](localhost:8443/swagger).

**Starting the Docker Setup**

To build and start the Docker containers in detached mode:

```python
python3 tools.py dev up -d --build
```

**Stopping the Docker Setup**

To stop and remove the running Docker containers:

```python
python3 tools.py dev down
```

## Available Commands

| Command    | Description                                                                                                                     |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------- |
| `install`  | Installs all required dependencies for the project Blockchain. This includes node.js packages, python packages and go packages. |
| `run`      | Starts the blockchain application using the main Go entry point.                                                                |
| `build`    | Compiles the blockchain application and outputs the binary to `./bin/blockchain`.                                               |
| `format`   | Formats all Go source files in the project using `gofmt`.                                                                       |
| `test`     | Runs the unit tests defined in the `internal/core/` module with verbose output.                                                 |
| `generate` | Generates Go types from JSON Schema definitions located in `internal/jsonschema/`. Requires node.js and the `quicktype` tool.   |
| `docs`     | Generates project documentation. You can specify the type using `--type`.                                                       |
| `dev`      | Executes all docker commands and uses `docker-compose-dev.yml`.                                                                 |

_Note:_ `quicktype example.json -l schema -o ./internal/jsonschema/schemaname.json` can be used to generate json-schemas from json examples

## Documentation types

| Type            | Description                                                                                                                          |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| `all` (default) | Generate Swagger (OpenAPI) documentation, Go-specific technical documentation and documentation for DIDs and verifiable credentials. |
| `swagger`       | Generates Swagger (OpenApi) documentation from Go comments using `swag`.                                                             |
| `go`            | Creates Go-specific technical documentation using a custom shell script (`./scripts/generates-docs.sh`).                             |
| `did-vc`        | Generates documentation for DIDs and verifiable credentials (`./scripts/generate-did-vc-docs`).                                      |

## Blockchain Commands

**Help Command:**

```shell
python3 tools.py run help
```

| Type              | Description                                      |
| ----------------- | ------------------------------------------------ |
| `-demo`           | Generate a demo blockchain and validate it.      |
| `-genesis`        | Creates a new blockchain and saves it to a file. |
| `-print-chain`    | Print the entire blockchain.                     |
| `-file`           | Specify a different filename.                    |
| `-web`            | Starts the blockchain api.                       |
| `-help`           | Print the help page.                             |

## Example Commands
Generate a new empty blockchain with a genesis block:
```shell
python3 tools.py run -genesis
python3 tools.py run -print-chain
```

---
Generate a demo blockchain with some example DIDs and VCs:
```shell
python3 tools.py run -demo
cat blockchain-demo.json | jq # To check the contents of the blockchain demo in detail
python3 tools.py run -file=blockchain-demo.json -print-chain
```

---
Starts the blockchain and the web api:
```shell
python3 tools.py run -web
```

Starts the blockchain, the web api and automatically creates a demo transactions every three seconds:
```shell
python3 tools.py run -web -demo
```
