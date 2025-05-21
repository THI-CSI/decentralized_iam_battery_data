// Code generated from JSON Schema using quicktype. DO NOT EDIT.
// To parse and unparse this JSON data, add this code to your project and do:
//
//    did, err := UnmarshalDid(bytes)
//    bytes, err = did.Marshal()

package core

import "time"

import "encoding/json"

func UnmarshalDid(data []byte) (Did, error) {
	var r Did
	err := json.Unmarshal(data, &r)
	return r, err
}

func (r *Did) Marshal() ([]byte, error) {
	return json.Marshal(r)
}

// Minimal on-chain DID record with a revocation tag.
type Did struct {
	// Defines the JSON-LD context, providing meaning to terms used in the did.                                   
	Context                                                                                    []Context          `json:"@context"`
	// Decentralized Identifier (DID) for the entity, following the DID syntax.                                   
	ID                                                                                         string             `json:"id"`
	// Boolean flag indicating whether this DID has been revoked.                                                 
	Revoked                                                                                    bool               `json:"revoked"`
	// Optional array of service endpoints related to the DID subject, such as APIs or metadata                   
	// services.                                                                                                  
	Service                                                                                    []DidSchema        `json:"service,omitempty"`
	// Timestamp indicating when the DID document was created/modified.                                           
	Timestamp                                                                                  time.Time          `json:"timestamp"`
	// Public key information used for verifying signatures and authentication.                                   
	VerificationMethod                                                                         VerificationMethod `json:"verificationMethod"`
}

// Represents a service associated with the DID subject, such as a metadata or data access
// point.
type DidSchema struct {
	// Identifier for the service endpoint, typically a DID fragment.       
	ID                                                               string `json:"id"`
	// The actual service endpoint, which can be a URL.                     
	ServiceEndpoint                                                  string `json:"serviceEndpoint"`
	// Type or category of the service, e.g., 'BatteryDataService'.         
	Type                                                             string `json:"type"`
}

// Public key information used for verifying signatures and authentication.
//
// A method by which a DID subject can be authenticated, typically using cryptographic keys.
type VerificationMethod struct {
	// DID that has the ability to make changes to this DID-Document.             
	Controller                                                             string `json:"controller"`
	// Identifier for the verification method, typically a DID fragment.          
	ID                                                                     string `json:"id"`
	// The public key encoded in multibase format.                                
	PublicKeyMultibase                                                     string `json:"publicKeyMultibase"`
	// Type of the verification method, e.g., 'Ed25519VerificationKey2020'.       
	Type                                                                   string `json:"type"`
}

type Context string

const (
	HTTPLocalhost8443DocsDidSchemaHTML Context = "http://localhost:8443/docs/did.schema.html"
	HTTPSWWWW3Org2018CredentialsV1     Context = "https://www.w3.org/2018/credentials/v1"
)
