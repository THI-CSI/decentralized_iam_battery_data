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
	ExpirationDate time.Time `json:"expirationDate"`
	ID             string    `json:"id"`
	Timestamp      time.Time `json:"timestamp"`
	VcHash         string    `json:"vcHash"`
}
