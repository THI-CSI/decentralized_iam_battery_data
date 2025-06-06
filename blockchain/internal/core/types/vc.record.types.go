// Code generated from JSON Schema using quicktype. DO NOT EDIT.
// To parse and unparse this JSON data, add this code to your project and do:
//
//    vCRecord, err := UnmarshalVCRecord(bytes)
//    bytes, err = vCRecord.Marshal()

package core

import "time"

import "encoding/json"

func UnmarshalVCRecord(data []byte) (VCRecord, error) {
	var r VCRecord
	err := json.Unmarshal(data, &r)
	return r, err
}

func (r *VCRecord) Marshal() ([]byte, error) {
	return json.Marshal(r)
}

// Minimal record of a Verifiable Credential containing only its ID, a hash of the VC, a
// timestamp, and expiration date.
type VCRecord struct {
	ExpirationDate *time.Time `json:"expirationDate,omitempty"`
	ID             string     `json:"id"`
	Proof          Proof      `json:"proof"`
	Timestamp      time.Time  `json:"timestamp"`
	VcHash         string     `json:"vcHash"`
}

// Cryptographic proof that makes the subject verifiable.
type Proof struct {
	// Optional challenge to prevent replay attacks.                 
	Challenge                                           *string      `json:"challenge,omitempty"`
	Created                                             time.Time    `json:"created"`
	// The actual signature in JSON Web Signature format             
	Jws                                                 string       `json:"jws"`
	ProofPurpose                                        ProofPurpose `json:"proofPurpose"`
	Type                                                Type         `json:"type"`
	// Reference to the key used to create the proof.                
	VerificationMethod                                  string       `json:"verificationMethod"`
}

type ProofPurpose string

const (
	Authentication ProofPurpose = "authentication"
)

type Type string

const (
	EcdsaSecp256R1Signature2019 Type = "EcdsaSecp256r1Signature2019"
)
