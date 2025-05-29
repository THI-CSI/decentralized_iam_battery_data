package domain

import (
	"blockchain/internal/core"
	coreTypes "blockchain/internal/core/types"
	"fmt"
	"time"
)

// CreateDid defines the struct supplied by the users
type CreateDid struct {
	// Public key information used for verifying signatures and authentication.
	PublicKey PublicKey `json:"publicKey" validate:"required"`
	// Optional array of service endpoints related to the DID subject, such as APIs or metadata services.
	Service []DidSchema `json:"service,omitempty" validate:"required"`
}

// PublicKey Public key information used for verifying signatures and authentication.
type PublicKey struct {
	// DID that have the ability to make changes to this DID-Document.
	Controller string `json:"controller" validate:"required"`
	// The public key encoded in multibase format.
	PublicKeyMultibase string `json:"publicKeyMultibase" validate:"required"`
	// Type of the verification method, e.g., 'Ed25519VerificationKey2020'.
	Type string `json:"type" validate:"required"`
}

// DidSchema Represents a service associated with the DID subject,
// such as a metadata or data access point.
type DidSchema struct {
	// The actual service endpoint, which can be a URL.
	ServiceEndpoint string `json:"serviceEndpoint" validate:"required"`
	// Type or category of the service, e.g., 'BatteryDataService'.
	Type string `json:"type" validate:"required"`
}

// ConvertRequestToDid converts a supplied DID to a core type object
func ConvertRequestToDid(createDid *CreateDid) coreTypes.Did {
	didId := core.GenerateDid()

	var didServices []coreTypes.DidSchema
	for i, service := range createDid.Service {
		didServices = append(didServices, coreTypes.DidSchema{
			ServiceEndpoint: service.ServiceEndpoint,
			Type:            service.Type,
			ID:              fmt.Sprintf("%s#service-%v", didId, i),
		})
	}

	return coreTypes.Did{
		Context: []coreTypes.Context{
			coreTypes.HTTPLocalhost8443DocsDidSchemaHTML,
			coreTypes.HTTPSWWWW3Org2018CredentialsV1,
		},
		ID: didId,
		VerificationMethod: coreTypes.VerificationMethod{
			Controller:         createDid.PublicKey.Controller,
			ID:                 fmt.Sprintf("%s#key-1", didId),
			PublicKeyMultibase: createDid.PublicKey.PublicKeyMultibase,
			Type:               createDid.PublicKey.Type,
		},
		Revoked:   false,
		Service:   didServices,
		Timestamp: time.Now(),
	}
}
