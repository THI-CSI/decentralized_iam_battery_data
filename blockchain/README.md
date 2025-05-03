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

*Note:* `quicktype example.json -l schema -o ./jsonschema/schemaname.json` can be used to generate json-schemas from json examples

**Install dependencies:**
```shell
make install
```

**Build the go library**:
This command also formats the sourcecode and generates the documentation (needed for to launch swagger).
```shell
make build
```

**Format the go sourcecode:**
```shell
make format
```

**Use the blockchain CLI**:

Start the Web API use the `-web` flag:
```shell
go run cmd/main.go -web
```

Create a demo blockchain and saves it to a file:
```shell
go run cmd/main.go -demo -save
```

Load the blockchain from a file and prints it to the console:
```shell
go run cmd/main.go -load -print-chain
```

Validate the blockchain:
```shell
go run cmd/main.go -load -validate
```

**Generate Documentation**:
```shell
make docs         # Generate full docs
make docs-go      # Generate go docs
make docs-did-vc  # Generate did & vc docs
make docs-swagger # Generate swagger docs
```

**Generate DID & VC structs**:

The generated code is safed in `./internal/core/types.go`.
```shell
make generate
```

**Cleanup**:

Removes any documentation, venv or node modules and the binary folder.
```shell
make clean
```

**Test**:

Run all unit tests
```shell
make test
```

**Run**:

Formats the sourcecode, runs the docs command for swagger and starts the Web API with the -web flag
```shell
make run
```

**All**:

Do everything: clean + install + generate + build + (format, docs) run + test
```shell
make all
```
