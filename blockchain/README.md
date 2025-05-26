# IAM Blockchain

The IAM blockchain is the database for our decentralized identity and access management platform for battery data. It
will store decentralized identities (DIDs) and verifiable credentials (VCs) to store the different identities and access
rights of other network entities.

Here you can read more about:

- [Project Structure](docs/modules.md#project-structure)
- [Blockchain Modules](docs/modules.md#modules)
- [Getting Started](#getting-started)
- [`tools.py` Documentation](docs/tools.md)
-
    - [Docker Setup](docs/tools.md#docker-setup)
-
    - [Available Commands](docs/tools.md#available-commands)
-
    - [Example Commands](docs/tools.md#example-commands)
- [API Documentation](docs/api.md)

## Getting Started

You can use the 'install' command from the 'tools.py' script to install all required dependencies:

```shell
python3 tools.py install
```

You can then build the documentation using the 'docs' command:

```shell
python3 tools.py docs
```

If you do not have a `blockchain.json` file with a valid blockchain you can create a new one using the `-genesis` flag:

```shell
python3 tools.py run -genesis
```

The final step is to start the Docker containers with the `dev` command to start up the blockchain, the web API and the
frontend:

```shell
python3 tools.py dev --build
```

Once everything has started, you can access the Swagger API documentation at the following address:
`http://127.0.0.1:8443/swagger/index.html`

[Here you can see how to interact with the API](docs/api.md#api-interaction)

