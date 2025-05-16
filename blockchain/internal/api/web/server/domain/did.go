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
	PublicKey PublicKey `json:"publicKey" required:"true"`
	// Optional array of service endpoints related to the DID subject, such as APIs or metadata
	// services.
	Service []DidSchema `json:"service,omitempty" required:"true"`
}

// PublicKey Public key information used for verifying signatures and authentication.
type PublicKey struct {
	// DID that have the ability to make changes to this DID-Document.
	Controller string `json:"controller" required:"true"`
	// The public key encoded in multibase format.
	PublicKeyMultibase string `json:"publicKeyMultibase" required:"true"`
	// Type of the verification method, e.g., 'Ed25519VerificationKey2020'.
	Type string `json:"type" required:"true"`
}

// DidSchema Represents a service associated with the DID subject,
// such as a metadata or data access point.
type DidSchema struct {
	// The actual service endpoint, which can be a URL.
	ServiceEndpoint string `json:"serviceEndpoint" required:"true"`
	// Type or category of the service, e.g., 'BatteryDataService'.
	Type string `json:"type" required:"true"`
}

// ConvertRequestToDid converts a supplied DID to a core type object
func ConvertRequestToDid(createDid *CreateDid) coreTypes.Did {
	now := time.Now()
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
		ID: didId,
		PublicKey: coreTypes.PublicKey{
			Controller:         createDid.PublicKey.Controller,
			ID:                 fmt.Sprintf("%s#key-1", didId),
			PublicKeyMultibase: createDid.PublicKey.PublicKeyMultibase,
			Type:               createDid.PublicKey.Type,
		},
		Revoked:   false,
		Service:   didServices,
		Timestamp: &now,
	}
}
