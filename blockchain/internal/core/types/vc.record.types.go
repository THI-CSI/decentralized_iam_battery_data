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
// timestamp, and revocation status.
type VCRecord struct {
	// Expiration Date of the related Verifiable Credential               
	ExpirationDate                                             *time.Time `json:"expirationDate,omitempty"`
	// The identifier of the Verifiable Credential.                       
	ID                                                         string     `json:"id"`
	// Timestamp when the record was created or updated.                  
	Timestamp                                                  time.Time  `json:"timestamp"`
	// A SHA-256 hash of the complete VC in hexadecimal format.           
	VcHash                                                     string     `json:"vcHash"`
}
