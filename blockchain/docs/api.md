# API Documentation
You can build the swagger documentation with the [`tools.py`script](tools.md):
```shell
python3 tools.py docs
```

Then you can start the webserver:
```shell
python3 tools.py run -web
```

And then you can view the swagger documentation under the following domain: `http://localhost:8443/swagger/index.html`

## API Interaction
We will use [`httpie`](https://httpie.io/docs/cli/linux) to interact with the API via the console, but you can also use `curl`. 
For a user interface, you can use [Postman](https://www.postman.com/).

### Blocks
#### Get all Blocks
The endpoint `/blocks` can be used to retrieve all the blocks in the blockchain via the API:
```shell
http GET http://localhost:8443/api/v1/blocks
```

#### Get a Block by ID
The endpoint `/blocks/<blockid>` can be used to retrieve the block with the specified ID:
```shell
http GET http://localhost:8443/api/v1/blocks/0
```

#### Get all Transactions of a Block
The endpoint `/blocks/<blockid>/transactions` can be used to retrieve all transactions of a block:
```shell
http GET http://localhost:8443/api/v1/blocks/0/transactions
```

---
### DIDs
#### Get all DIDs
The endpoint `/dids` can be used to retrieve all DIDs on the blockchain:
```shell
http GET http://localhost:8443/api/v1/dids
```

#### Get a single DID
The endpoint `/dids/<did>` can be used to retrieve the specified DID:
```shell
http GET http://localhost:8443/api/v1/dids/did:batterypass:896ad506-9843-48d3-b599-be45fca2bb3e
```

#### Create a new DID
The `POST` endpoint `/dids` can be used to create a new DID on the blockchain:
```shell
http POST localhost:8443/api/v1/dids < docs/api-examples/bms-example.json 
```

#### Revoke a DID
The `DELETE` endpoint `/dids/<did>` can be used to revoke a new DID on the blockchain:
```shell
http DELETE http://localhost:8443/api/v1/dids/did:batterypass:896ad506-9843-48d3-b599-be45fca2bb3e
```

---
### VCs
#### Create a new VC
The `POST` endpoint `/dids/<did>/vc` can be used to create a new VC record on the blockchain:
```shell
http POST localhost:8443/api/v1/dids/did:batterypass:896ad506-9843-48d3-b599-be45fca2bb3e/vc < docs/api-examples/vc-example.json
```
The DID specified in the API URL must be the same as the Issuer DID in the verifiable credential.

#### Get a VC Record
The endpoint `/dids/<did>/vc/<urn>` can be used to retrieve the specified VC record on the blockchain:
```shell
http GET localhost:8443/api/v1/vc/urn:uuid:cc4e69d7-b7f7-4155-ac8b-5af63df4472a
```
