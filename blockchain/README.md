# IAM Blockchain
The IAM blockchain is the database for our decentralized identity and access management platform for battery data. It will store decentralized identities (DIDs) and verifiable credentials (VCs) to store the different identities and access rights of other network entities.

## Project Structure

| Directory | Description | 
|  - | - | 
| cmd/ | Contains the entry point of the program |
| internal/core/ | Contains the primary implementation of the blockchain |
| internal/api/ | Contains the external interfaces for the application |
| internal/api/web/ | Contains the web api for the application |
| internal/api/cli/ | Contains the CLI for the application |
| internal/storage/ | Contains functionality to load and save the blockchain |

## Modules
### Core
The core module (`internal/core/`) contains the primary functionality of the blockchain. 
It includes the data structures that define the blocks and transactions, as well as the functions to create and validate them.

### API
The api module (`/internal/api/`) contains the external interfaces for the blockchain. 
It is planned to provide a web interface (`/internal/api/web/`) that can be used to make HTTP requests to create new transactions or retrieve information from the blockchain.
It is also planned to provide a simple CLI (`/internal/api/cli`) to interact with the blockchain for testing and development purposes.

### Storage
The storage module (`/internal/storage/`) will provide an interface to load and store data from different sources. 
Since this project is only a proof of concept, we will only store the blockchain in a file for now.

