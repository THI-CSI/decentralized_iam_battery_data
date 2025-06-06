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

## API Development
The API was build with a "schema-first" approach. (When calling any `python3 tools.py ...` command make sure you are in the `blockchain` directory.)
### Structure
```bash
internal/api/web
|-- jsonexample
|   |-- requests
|   `-- responses
|-- jsonschema
|   |-- requests
|   `-- responses
|-- openapi.bundled.yaml
|-- openapi.yaml
|-- server
|   |-- config.go
|   |-- extra_routes.go
|   |-- handlers
|   |-- models
|   |   `-- api.gen.go
|   |-- services
|   `-- utils
`-- web.go
```
- `./internal/api/web/openapi.yaml` defines all endpoints and references schemas for requests/responses that communicate application/json (Also references example files)
- `./internal/api/web/jsonschema` contains jsonschemas for requests & response which themselves reference our core schemas as much as possible to ensure consistency across the project
- `./internal/api/web/jsonexample` contains referenced example files for requests & responses
- `./internal/core/jsonschema` contains our core, W3C-compliant data structures that define the data types used in the blockchain implementation and are referenced by the endpoint schemas.
- `./scripts/generate-api-go.sh` takes the the defining yaml file and generates datatypes and interfaces for an echo server (Is triggered like this `python3 tools.py generate`)
- `./internal/api/web/openapi.bundled.yaml` is a sideproduct of `./scripts/generate-api-go.sh` containing a completely dereferenced api configuration.
- `./internal/api/web/server/models/api.gen.go` is the product of `./scripts/generate-api-go.sh` containing type and inteface definitions
- `./internal/api/web/server/handlers/handlers.go` Contains the central `MyService` struct required for the handlers as well as methods to check incoming and outgoing data against the respected schemas.
- `./internal/api/web/server/handlers` contains handler definitions per specified endpoint (Any extensive logic triggered here is defined in `./internal/api/web/server/services`)
- `./internal/api/web/server/services` contains all necessary logic that is specific to an endpoint
- `./internal/api/web/web.go` is the entry point to the Echo webserver
- `./internal/api/web/server/extra_routes.go` contains extra routes e.g. for status checks and various documentation.
### openapi.yaml
Each endpoint defintion in this yaml file looks like this:
```yaml
/api/v1/dids/createormodify:  
  post:  
    tags: [ DIDs ]  
    summary: Create or modify a DID document  
    operationId: createOrModifyDid  
    requestBody:  
      required: true  
      content:  
        application/json:  
          schema:  
            $ref: './jsonschema/requests/request.did.createormodify.schema.json'  
    responses:  
      '200':  
        description: DID created or modified successfully  
        content:  
          application/json:  
            schema:  
              { $ref: './jsonschema/responses/response.ok.schema.json' }  
      '400':  
        description: Client Errors  
        content:  
          application/json:  
            schema: { $ref: './jsonschema/responses/response.error.schema.json' }  
      '500':  
        description: Server Errors  
        content:  
          application/json:  
            schema: { $ref: './jsonschema/responses/response.error.schema.json' }
```
**Remark:**
- `operationId: createOrModifyDid` this ties in with the naming of the handlers (they need to match - first letter is capital in go)
- The echo server will not start if you are missing a handler defined in the yaml.
- One can comment out endpoints and regenerate `api.gen.go` to remove an endpoint
### request.did.createormodify.schema.json
Each referenced schema looks like this. Using the core schemas as building blocks
```json
{  
  "$schema": "http://json-schema.org/draft-07/schema#",  
  "$id": "request.did.createormodify",  
  "type": "object",  
  "required": ["proof", "payload"],  
  "additionalProperties": false,  
  "properties": {  
    "proof": { "$ref": "../../../../jsonschema/common.defs.schema.json#/definitions/Proof"},  
    "payload": { "$ref": "../../../../jsonschema/did.schema.json"}  
  }  
}
```
### handlers/did.go
Each endpoint must implement a handler (naming convention defined in yaml: `operationId: createOrModifyDid`; requries a function called `CreateOrModifyDid`)
```go
// CreateOrModifyDid handles POST /api/v1/dids/createormodify
func (s *MyServer) CreateOrModifyDid(ctx echo.Context) error {  
    var requestBody models.CreateOrModifyDidJSONRequestBody  
  
    if err := ctx.Bind(&requestBody); err != nil {  
       return echo.NewHTTPError(http.StatusBadRequest, models.ResponseErrorSchema{Message: err.Error()})  
    }  
  
    if err := s.validateIncomingRequest(ctx, &requestBody, s.requestDidCreateormodifySchema); err != nil {  
       return err  
    }  
  
    err := s.DidService.VerifyRequestCreateOrModify(requestBody)  
    if err != nil {  
       return echo.NewHTTPError(http.StatusBadRequest, models.ResponseErrorSchema{Message: err.Error()})  
    }  
  
    err = s.DidService.CreateOrModifyDID(ctx.Request().Context(), &requestBody.Payload)  
    if err != nil {  
       return echo.NewHTTPError(http.StatusInternalServerError, models.ResponseErrorSchema{Message: err.Error()})  
    }  
  
    return ctx.JSON(http.StatusOK, models.ResponseOkSchema{Message: "DID created"})  
}
```
**Remark:**
- `err := s.validateIncomingRequest(ctx, &requestBody, s.requestDidCreateormodifySchema)` here the request validation from `handlers/handlers.go` is called (similar in all POST endpoints)
- `err = s.DidService.CreateOrModifyDID(ctx.Request().Context(), &requestBody.Payload)` Corresponding interface `DidService` contains the method `CreateOrModifyDID` which handles logic to actually ass the recieved did to the blockchain
- All short responses are handled by the generated types: `models.ResponseOkSchema` and `models.ResponseErrorSchema`
- All complicated responses have their own schema and generated types and should also utilize `s.validateOutgoingResponse`
### services/did.go
Most endpoints require logic to perform any meaningful tasks. That is outsourced to the services directory.
```go
// DidService defines the interface for managing Decentralized Identifiers (DIDs)
// and their associated access rights.  
type DidService interface {  
    GetDIDs(ctx context.Context) (*[]coreTypes.Did, error)  
    GetDID(userContext context.Context, did string) (*coreTypes.Did, error) 
    CreateOrModifyDID(userContext context.Context, create *models.DidSchema) error  
    RevokeDid(userContext context.Context, did string) error  
    GetPublicKey(did string) (string, error)  
    VerifyRequestCreateOrModify(requestBody models.RequestDidCreateormodifySchema) error  
    VerifyRequestRevoke(requestBody models.RequestDidRevokeSchema) error  
}
 
// didService is a concrete implementation of the DidService interface.
type didService struct {  
    chain *core.Blockchain  
}  
  
// NewDidService creates and returns a new instance of the DidService implementation.
func NewDidService(chain *core.Blockchain) DidService {  
    return &didService{chain: chain}  
}
...
// CreateOrModifyDID appends a new DID or a modification to the blockchain
func (s *didService) CreateOrModifyDID(userContext context.Context, createDid *models.DidSchema) error {  
    // Transform from api types to core types - Works because of equal JSON tags  
    var err error  
    jsonBytes, err := json.Marshal(createDid)  
    if err != nil {  
       log.Printf("Internal Server Error: %s", err)  
       return err  
    }  
    did, err := coreTypes.UnmarshalDid(jsonBytes)  
    if err != nil {  
       log.Printf("Internal Server Error: %s", err)  
       return err  
    }  
  
    // Create Transaction  
    if err := s.chain.AppendDid(&did); err != nil {  
       log.Printf("Internal Server Error: %s", err)  
       return err  
    }  
    return nil  
}
```
**Remark:**
- The interface, type and func above '...' is needed for any service file
- The functions headers declared in the interface need to match the declared function
### handlers/handlers.go
```go
// MyServer holds all application services and pre-compiled JSON schemas.// This struct will be instantiated once at application startup.  
type MyServer struct {  
    DidService         services.DidService  
    BlockService       services.BlockService  
    TransactionService services.TransactionService  
    VCService          services.VCService  
    VPService          services.VPService  
  
    // Compiled JSON Schemas (loaded once at startup)  
    responseTransactionsSchema *gojsonschema.Schema  
    responseBlockSchema        *gojsonschema.Schema  
    responseBlocksSchema       *gojsonschema.Schema  
    responseDidSchema          *gojsonschema.Schema  
    responseDidsSchema         *gojsonschema.Schema  
    responseVcSchema           *gojsonschema.Schema  
    responseVcsSchema          *gojsonschema.Schema  
  
    requestDidCreateormodifySchema *gojsonschema.Schema  
    requestDidRevokeSchema         *gojsonschema.Schema  
    requestVcCreateSchema          *gojsonschema.Schema  
    requestVcRevokeSchema          *gojsonschema.Schema  
    requestVpVerifySchema          *gojsonschema.Schema  
}  
  
// NewMyServer is the constructor for MyServer.  
// It initializes all services and compiles all necessary JSON schemas.  
func NewMyServer(  
    didSvc services.DidService,  
    blockSvc services.BlockService,  
    txSvc services.TransactionService,  
    vcSvc services.VCService,  
    vpSvc services.VPService,  
) (*MyServer, error) {  
    s := &MyServer{  
       DidService:         didSvc,  
       BlockService:       blockSvc,  
       TransactionService: txSvc,  
       VCService:          vcSvc,  
       VPService:          vpSvc,  
    }  
  
    // --- Schema Loading and Compilation ---  
    // Define specific schema base directories    
    apiWebSchemasPath := "./internal/api/web/jsonschema"  
    coreSchemasPath := "./internal/jsonschema"  
  
...
  
    // --- Load Response Schemas (from apiWebSchemasPath) ---  
...
    s.responseDidSchema, err = loadSchema(apiWebSchemasPath, "responses/response.did.schema.json")  
    if err != nil {  
       return nil, fmt.Errorf("failed to load responseDidSchema: %w", err)  
    }  
  
    s.responseDidsSchema, err = loadSchema(apiWebSchemasPath, "responses/response.dids.schema.json")  
    if err != nil {  
       return nil, fmt.Errorf("failed to load responseDidsSchema: %w", err)  
    }  
  
 ...
  
    // --- Load Request Schemas (from apiWebSchemasPath) ---  
    s.requestDidCreateormodifySchema, err = loadSchema(apiWebSchemasPath, "requests/request.did.createormodify.schema.json")  
    if err != nil {  
       return nil, fmt.Errorf("failed to load requestDidCreateormodifySchema: %w", err)  
    }  
  
    s.requestDidRevokeSchema, err = loadSchema(apiWebSchemasPath, "requests/request.did.revoke.schema.json")  
    if err != nil {  
       return nil, fmt.Errorf("failed to load requestDidRevokeSchema: %w", err)  
    }  
  
 ...
}
```
**Remark**:
- All service interfaces need to be declared in the `type MyServer` as well as passed to `func NewMyServer`
- Also all request and response schemas have to be loaded for the validation methods to work properly
### web.go
Entry point of the webserver
```go
// CreateServer initializes the Echo server, starts it, and ensures graceful shutdown handling.
// The server runs in a goroutine to allow for concurrent shutdown handling via `gracefulShutdown`.  
func CreateServer(chain *core.Blockchain) {  
    e := echo.New()  
  
    // Add Echo middleware (e.g., Logger, Recover)  
    e.Use(middleware.Logger())  
    e.Use(middleware.Recover())  
  
    e.HTTPErrorHandler = utils.CustomErrorHandler  
  
    // Initialize all your services  
    didService := services.NewDidService(chain)  
    blockService := services.NewBlockService(chain)  
    transactionService := services.NewTransactionService(chain)  
    vcService := services.NewVCService(chain)  
    vpService := services.NewVPService(chain)  
  
    // Create an instance of your server implementation  
    myServer, err := handlers.NewMyServer(  
       didService,  
       blockService,  
       transactionService,  
       vcService,  
       vpService,  
    )  
    if err != nil {  
       // If schema loading or any other server initialization fails, log and exit.  
       log.Fatalf("Failed to initialize server handlers with schemas: %v", err)  
    }  
  
    // Register the handlers generated by oapi-codegen  
    models.RegisterHandlers(e, myServer)  
  
    // Register any extra routes (status, swagger, static files)  
    server.RegisterExtraRoutes(e)  
  
    // Get server configuration, including the port  
    config := server.NewConfiguration()  
  
    done := make(chan bool, 1)  
  
    go func() {  
       err := e.Start(fmt.Sprintf(":%s", config.Port))  
       if err != nil && err != http.ErrServerClosed {  
          e.Logger.Fatal("shutting down the server", err)  
       }  
    }()  
  
    go gracefulShutdown(e, done)  
  
    <-done  
    log.Println("Graceful shutdown complete.")  
}
```
**Remark:**
- A new service interface also requires initialization in the `CreateServer` method

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
http POST localhost:8443/jsonschema/v1/dids < docs/jsonschema-examples/bms-example.json 
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
http POST localhost:8443/jsonschema/v1/dids/did:batterypass:896ad506-9843-48d3-b599-be45fca2bb3e/vc < docs/jsonschema-examples/vc-example.json
```
The DID specified in the API URL must be the same as the Issuer DID in the verifiable credential.

#### Get a VC Record
The endpoint `/dids/<did>/vc/<urn>` can be used to retrieve the specified VC record on the blockchain:
```shell
http GET localhost:8443/jsonschema/v1/vc/urn:uuid:cc4e69d7-b7f7-4155-ac8b-5af63df4472a
```
