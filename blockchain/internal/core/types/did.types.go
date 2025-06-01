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
	Context                                                   []Context          `json:"@context"`
	ID                                                        string             `json:"id"`
	// A revoked flag indicating if an DID is no longer valid.                   
	Revoked                                                   bool               `json:"revoked"`
	Service                                                   []Service          `json:"service,omitempty"`
	Timestamp                                                 time.Time          `json:"timestamp"`
	VerificationMethod                                        VerificationMethod `json:"verificationMethod"`
}

type Service struct {
	ID              string `json:"id"`
	ServiceEndpoint string `json:"serviceEndpoint"`
	Type            Type   `json:"type"`
}

type VerificationMethod struct {
	Controller         string `json:"controller"`
	ID                 string `json:"id"`
	PublicKeyMultibase string `json:"publicKeyMultibase"`
	Type               string `json:"type"`
}

type Context string

const (
	HTTPLocalhost8443DocsDidSchemaHTML Context = "http://localhost:8443/docs/did.schema.html"
	HTTPSWWWW3Org2018CredentialsV1     Context = "https://www.w3.org/2018/credentials/v1"
)

type Type string

const (
	BatteryPassAPI Type = "BatteryPassAPI"
	HandleDID      Type = "HandleDID"
)
