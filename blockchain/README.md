# IAM Blockchain

The IAM blockchain is the database for our decentralized identity and access management platform for battery data. It will store decentralized identities (DIDs) and verifiable credentials (VCs) to store the different identities and access rights of other network entities.

## Project Structure

| Directory         | Description                                            |
| ----------------- | ------------------------------------------------------ |
| cmd/              | Contains the entry point of the program                |
| internal/core/    | Contains the primary implementation of the blockchain  |
| internal/api/     | Contains the external interfaces for the application   |
| internal/api/web/ | Contains the web api for the application               |
| internal/api/cli/ | Contains the CLI for the application                   |
| internal/storage/ | Contains functionality to load and save the blockchain |

## Modules

### Core

The core module (`internal/core/`) contains the primary functionality of the blockchain.
It includes the data structures that define the blocks and transactions, as well as the functions to create and validate them.

### API

The api module (`/internal/api/`) contains the external interfaces for the blockchain.
It is planned to provide a web interface (`/internal/api/web/`) that can be used to make HTTP requests to create new transactions or retrieve information from the blockchain.

To generate new swagger documentation use the command:

It is also planned to provide a simple CLI (`/internal/api/cli`) to interact with the blockchain for testing and development purposes.

### Storage

The storage module (`/internal/storage/`) will provide an interface to load and store data from different sources.
Since this project is only a proof of concept, we will only store the blockchain in a file for now.

## Usage

Make sure you are in the `decentralized_iam_battery_data/blockchain` directory.

Run commands using:

```shell
python3 tools.py [cmd] [options]
```

To see all available commands:

```shell
python3 tools.py -h
```

### Run Docker Setup

The Docker setup launches both the blockchain API and the frontend. Once the setup is running, the application will be accessible at [localhost:8443](http://localhost:8443).

- Swagger Documentation: Access the API documentation at [localhost:8443/swagger](localhost:8443/swagger).

**Starting the Docker Setup**

To build and start the Docker containers in detached mode:

```python
python3 tools.py docker up -d --build
```

**Stopping the Docker Setup**

To stop and remove the running Docker containers:

```python
python3 tools.py docker down
```

### Available Commands

| Command    | Description                                                                                                                     |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------- |
| `install`  | Installs all required dependencies for the project Blockchain. This includes node.js packages, python packages and go packages. |
| `run`      | Starts the blockchain application using the main Go entry point.                                                                |
| `build`    | Compiles the blockchain application and outputs the binary to `./bin/blockchain`.                                               |
| `format`   | Formats all Go source files in the project using `gofmt`.                                                                       |
| `test`     | Runs the unit tests defined in the `internal/core/` module with verbose output.                                                 |
| `generate` | Generates Go types from JSON Schema definitions located in `internal/jsonschema/`. Requires node.js and the `quicktype` tool.   |
| `docs`     | Generates project documentation. You can specify the type using `--type`.                                                       |

_Note:_ `quicktype example.json -l schema -o ./jsonschema/schemaname.json` can be used to generate json-schemas from json examples

### Documentation types

| Type            | Description                                                                                                                          |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| `all` (default) | Generate Swagger (OpenAPI) documentation, Go-specific technical documentation and documentation for DIDs and verifiable credentials. |
| `swagger`       | Generates Swagger (OpenApi) documentation from Go comments using `swag`.                                                             |
| `go`            | Creates Go-specific technical documentation using a custom shell script (`./scripts/generates-docs.sh`).                             |
| `did-vc`        | Generates documentation for DIDs and verifiable credentials (`./scripts/generate-did-vc-docs`).                                      |

### Blockchain Commands

**Help Command:**

```shell
python3 tools.py run help
```

| Type              | Description                                 |
| ----------------- | ------------------------------------------- |
| `-demo` (default) | Generate a demo blockchain and validate it. |
| `-file`           | Specify the file.                           |
| `-load`           | Load the blockchain from a file.            |
| `-print-chain`    | Print the entire blockchain.                |
| `-save`           | Save the blockchain to a file.              |
| `-validate`       | Validate the blockchain.                    |
| `-web`            | Starts the blockchain api.                  |

**Example Command:**

```shell
python3 tools.py run -demo -save -load -print-chain
```
