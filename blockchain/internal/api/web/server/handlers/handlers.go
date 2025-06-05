package handlers

import (
	"blockchain/internal/api/web/server/models"
	"blockchain/internal/api/web/server/services"
	"fmt"
	"github.com/labstack/echo/v4"
	"log"
	"net/http"
	"os"
	"path/filepath"
	"runtime"

	"github.com/xeipuuv/gojsonschema"
)

// MyServer holds all application services and pre-compiled JSON schemas.
// This struct will be instantiated once at application startup.
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
	responseVcVerifySchema     *gojsonschema.Schema

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
	// Determine the base path for your application to build absolute paths
	_, currentFile, _, ok := runtime.Caller(0)
	if !ok {
		return nil, fmt.Errorf("could not get current file path for schema loading")
	}
	// Path from handlers.go (internal/api/web/server/handlers) to project root (blockchain)
	projectRoot := filepath.Join(filepath.Dir(currentFile), "../../../../")

	// Define specific schema base directories
	apiWebSchemasPath := filepath.Join(projectRoot, "internal/api/web/jsonschemas")
	coreSchemasPath := filepath.Join(projectRoot, "internal/jsonschema")

	// Create a global SchemaLoader. This is crucial for resolving
	// internal references ($ref) between different schema files, especially across different root paths.
	globalSchemaLoader := gojsonschema.NewSchemaLoader()

	// Load common.defs.schema.json first, as it's likely referenced by others.
	commonDefsFullPath := filepath.Join(coreSchemasPath, "common.defs.schema.json")
	if _, err := os.Stat(commonDefsFullPath); err == nil {
		if err := globalSchemaLoader.AddSchemas(gojsonschema.NewReferenceLoader("file://" + commonDefsFullPath)); err != nil {
			return nil, fmt.Errorf("failed to add common definitions schema from %s: %w", commonDefsFullPath, err)
		}
		log.Printf("Successfully added common definitions schema: %s", commonDefsFullPath)
	} else {
		log.Printf("Warning: common.defs.schema.json not found at %s. Ensure it's not referenced or its path is correct if it is.", commonDefsFullPath)
	}

	// Helper function to load and compile a single schema from a given base path.
	// It will use the pre-configured globalSchemaLoader for reference resolution.
	loadSchema := func(basePath, relativePath string) (*gojsonschema.Schema, error) {
		fullPath := filepath.Join(basePath, relativePath)
		schemaLoader := gojsonschema.NewReferenceLoader("file://" + fullPath)

		// Before compiling, add the specific schema's loader to the global one.
		// This allows the compiler to find this schema by its $id or relative path for future references.
		if err := globalSchemaLoader.AddSchemas(schemaLoader); err != nil {
			return nil, fmt.Errorf("failed to add schema from %s to global loader: %w", fullPath, err)
		}

		compiled, err := globalSchemaLoader.Compile(schemaLoader)
		if err != nil {
			return nil, fmt.Errorf("failed to compile schema from %s: %w", fullPath, err)
		}
		log.Printf("Successfully compiled schema: %s (from %s)", relativePath, basePath)
		return compiled, nil
	}

	var err error

	// --- Load Response Schemas (from apiWebSchemasPath) ---
	s.responseTransactionsSchema, err = loadSchema(apiWebSchemasPath, "responses/response.transactions.schema.json")
	if err != nil {
		return nil, fmt.Errorf("failed to load responseTransactionsSchema: %w", err)
	}

	s.responseBlockSchema, err = loadSchema(apiWebSchemasPath, "responses/response.block.schema.json")
	if err != nil {
		return nil, fmt.Errorf("failed to load responseBlockSchema: %w", err)
	}

	s.responseBlocksSchema, err = loadSchema(apiWebSchemasPath, "responses/response.blocks.schema.json")
	if err != nil {
		return nil, fmt.Errorf("failed to load responseBlocksSchema: %w", err)
	}

	s.responseDidSchema, err = loadSchema(apiWebSchemasPath, "responses/response.did.schema.json")
	if err != nil {
		return nil, fmt.Errorf("failed to load responseDidSchema: %w", err)
	}

	s.responseDidsSchema, err = loadSchema(apiWebSchemasPath, "responses/response.dids.schema.json")
	if err != nil {
		return nil, fmt.Errorf("failed to load responseDidsSchema: %w", err)
	}

	s.responseVcSchema, err = loadSchema(apiWebSchemasPath, "responses/response.vc.schema.json")
	if err != nil {
		return nil, fmt.Errorf("failed to load responseVcSchema: %w", err)
	}

	s.responseVcsSchema, err = loadSchema(apiWebSchemasPath, "responses/response.vcs.schema.json")
	if err != nil {
		return nil, fmt.Errorf("failed to load responseVcsSchema: %w", err)
	}

	s.responseVcVerifySchema, err = loadSchema(apiWebSchemasPath, "responses/request.vp.verify.schema.json")
	if err != nil {
		return nil, fmt.Errorf("failed to load responseVcVerifySchema: %w", err)
	}

	// --- Load Request Schemas (from apiWebSchemasPath) ---
	s.requestDidCreateormodifySchema, err = loadSchema(apiWebSchemasPath, "requests/request.did.createormodify.schema.json")
	if err != nil {
		return nil, fmt.Errorf("failed to load requestDidCreateormodifySchema: %w", err)
	}

	s.requestDidRevokeSchema, err = loadSchema(apiWebSchemasPath, "requests/request.did.revoke.schema.json")
	if err != nil {
		return nil, fmt.Errorf("failed to load requestDidRevokeSchema: %w", err)
	}

	s.requestVcCreateSchema, err = loadSchema(apiWebSchemasPath, "requests/request.vc.create.schema.json")
	if err != nil {
		return nil, fmt.Errorf("failed to load requestVcCreateSchema: %w", err)
	}

	s.requestVcRevokeSchema, err = loadSchema(apiWebSchemasPath, "requests/request.vc.revoke.schema.json")
	if err != nil {
		return nil, fmt.Errorf("failed to load requestVcRevokeSchema: %w", err)
	}

	s.requestVpVerifySchema, err = loadSchema(apiWebSchemasPath, "requests/request.vp.verify.schema.json")
	if err != nil {
		return nil, fmt.Errorf("failed to load requestVpVerifySchema: %w", err)
	}

	log.Println("All JSON schemas loaded and compiled successfully.")
	return s, nil
}

// validateIncomingRequest handles schema validation for incoming request bodies.
// It returns an error if validation fails or an internal error occurs.
// If validation fails, it writes a 400 Bad Request response.
func (s *MyServer) validateIncomingRequest(ctx echo.Context, data interface{}, schema *gojsonschema.Schema) error {
	documentLoader := gojsonschema.NewGoLoader(data)

	validationResult, validateErr := schema.Validate(documentLoader)
	if validateErr != nil {
		log.Printf(`Internal error during schema validation: %v`, validateErr)
		msg := "Internal server error during request validation process"
		return ctx.JSON(http.StatusInternalServerError, models.ResponseErrorSchema{Message: msg}) // Message is string
	}

	if !validationResult.Valid() {
		validationDetails := make([]struct {
			Context     *string `json:"context,omitempty"`
			Description string  `json:"description"`
			Field       string  `json:"field"`
			Type        *string `json:"type,omitempty"`
			Value       *string `json:"value,omitempty"`
		}, 0) // Explicitly use the anonymous struct type here

		for _, desc := range validationResult.Errors() {
			// Handle pointer fields by taking the address of a temporary variable
			context := fmt.Sprintf("%v", desc.Context())
			typ := desc.Type() // desc.Type() is already string
			value := fmt.Sprintf("%v", desc.Value())

			detail := struct {
				Context     *string `json:"context,omitempty"`
				Description string  `json:"description"`
				Field       string  `json:"field"`
				Type        *string `json:"type,omitempty"`
				Value       *string `json:"value,omitempty"`
			}{
				Field:       desc.Field(),       // Field is string, assign directly
				Description: desc.Description(), // Description is string, assign directly
				Context:     &context,           // Context is *string, assign address
				Type:        &typ,               // Type is *string, assign address
				Value:       &value,             // Value is *string, assign address
			}
			validationDetails = append(validationDetails, detail)
		}
		log.Printf("Bad Request: NOT conform to schema! Errors: %v", validationDetails)

		msg := "Invalid request payload"
		return ctx.JSON(http.StatusBadRequest, models.ResponseErrorSchema{
			Message: msg,                // Message is string
			Details: &validationDetails, // Details is *[]struct, assign address of slice
		})
	}

	return nil // Validation successful
}

// validateOutgoingResponse handles schema validation for outgoing response bodies.
// It returns an error if validation fails or an internal error occurs.
// If validation fails, it writes a 500 Internal Server Error response.
func (s *MyServer) validateOutgoingResponse(ctx echo.Context, data interface{}, schema *gojsonschema.Schema) error {
	documentLoader := gojsonschema.NewGoLoader(data)

	validationResult, validateErr := schema.Validate(documentLoader)
	if validateErr != nil {
		log.Printf("Internal error during schema validation: %v", validateErr)
		msg := "Internal server error during response validation process"
		return ctx.JSON(http.StatusInternalServerError, models.ResponseErrorSchema{Message: msg}) // Message is string
	}

	if !validationResult.Valid() {
		validationDetails := make([]struct {
			Context     *string `json:"context,omitempty"`
			Description string  `json:"description"`
			Field       string  `json:"field"`
			Type        *string `json:"type,omitempty"`
			Value       *string `json:"value,omitempty"`
		}, 0) // Explicitly use the anonymous struct type here

		for _, desc := range validationResult.Errors() {
			// Handle pointer fields by taking the address of a temporary variable
			context := fmt.Sprintf("%v", desc.Context())
			typ := desc.Type() // desc.Type() is already string
			value := fmt.Sprintf("%v", desc.Value())

			detail := struct {
				Context     *string `json:"context,omitempty"`
				Description string  `json:"description"`
				Field       string  `json:"field"`
				Type        *string `json:"type,omitempty"`
				Value       *string `json:"value,omitempty"`
			}{
				Field:       desc.Field(),       // Field is string, assign directly
				Description: desc.Description(), // Description is string, assign directly
				Context:     &context,           // Context is *string, assign address
				Type:        &typ,               // Type is *string, assign address
				Value:       &value,             // Value is *string, assign address
			}
			validationDetails = append(validationDetails, detail)
		}
		// Log the detailed errors internally
		log.Printf("Not conform to schema! Errors: %v", validationDetails)

		msg := fmt.Sprintf("Internal server error: Malformed data generated by server")
		return ctx.JSON(http.StatusInternalServerError, models.ResponseErrorSchema{
			Message: msg,                // Message is string
			Details: &validationDetails, // Details is *[]struct, assign address of slice
		})
	}

	return nil // Validation successful
}
