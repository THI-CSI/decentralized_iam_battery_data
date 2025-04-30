// Code generated from JSON Schema using quicktype. DO NOT EDIT.
// To parse and unparse this JSON data, add this code to your project and do:
//
//    did, err := UnmarshalDid(bytes)
//    bytes, err = did.Marshal()

package models

import "encoding/json"

func UnmarshalDid(data []byte) (Did, error) {
	var r Did
	err := json.Unmarshal(data, &r)
	return r, err
}

func (r *Did) Marshal() ([]byte, error) {
	return json.Marshal(r)
}

type Did struct {
	Schema      string        `json:"$schema"`
	ID          string        `json:"$id"`
	Title       string        `json:"title"`
	Description string        `json:"description"`
	Type        string        `json:"type"`
	Required    []string      `json:"required"`
	Properties  DIDProperties `json:"properties"`
}

type DIDProperties struct {
	Context            Context            `json:"@context"`
	ID                 ID                 `json:"id"`
	VerificationMethod VerificationMethod `json:"verificationMethod"`
	Authentication     Context            `json:"authentication"`
	Service            Service            `json:"service"`
}

type Context = shared.Context
	OneOf []ItemsElement `json:"oneOf"`
}

type ItemsElement struct {
	Type string `json:"type"`
}

type ID struct {
	Type   string `json:"type"`
	Format string `json:"format"`
}

type Service struct {
	Type  string       `json:"type"`
	Items ItemsElement `json:"items"`
}

type VerificationMethod struct {
	Type  string                  `json:"type"`
	Items VerificationMethodItems `json:"items"`
}

type VerificationMethodItems struct {
	Type       string          `json:"type"`
	Required   []string        `json:"required"`
	Properties ItemsProperties `json:"properties"`
}

type ItemsProperties struct {
	ID                 ItemsElement `json:"id"`
	Type               ItemsElement `json:"type"`
	Controller         ItemsElement `json:"controller"`
	PublicKeyMultibase ItemsElement `json:"publicKeyMultibase"`
}
