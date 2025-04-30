// Code generated from JSON Schema using quicktype. DO NOT EDIT.
// To parse and unparse this JSON data, add this code to your project and do:
//
//    produced, err := UnmarshalProduced(bytes)
//    bytes, err = produced.Marshal()

package models

import "encoding/json"

func UnmarshalProduced(data []byte) (Produced, error) {
	var r Produced
	err := json.Unmarshal(data, &r)
	return r, err
}

func (r *Produced) Marshal() ([]byte, error) {
	return json.Marshal(r)
}

type Produced struct {
	Schema     string             `json:"$schema"`
	ID         string             `json:"$id"`
	Title      string             `json:"title"`
	Type       string             `json:"type"`
	Required   []string           `json:"required"`
	Properties ProducedProperties `json:"properties"`
}

type ProducedProperties struct {
	Context           Context           `json:"@context"`
	Type              Type              `json:"type"`
	Issuer            IssuanceDate      `json:"issuer"`
	IssuanceDate      IssuanceDate      `json:"issuanceDate"`
	CredentialSubject CredentialSubject `json:"credentialSubject"`
	Proof             Proof             `json:"proof"`
}

type Context = shared.Context
	Type []string `json:"type"`
}

type CredentialSubject struct {
	Type       string                      `json:"type"`
	Required   []string                    `json:"required"`
	Properties CredentialSubjectProperties `json:"properties"`
}

type CredentialSubjectProperties struct {
	Owner IssuanceDate `json:"owner"`
	Owned Proof        `json:"owned"`
}

type Proof = shared.Proof
	Type string `json:"type"`
}

type IssuanceDate struct {
	Type   string `json:"type"`
	Format string `json:"format"`
}

type Type struct {
	Type  string `json:"type"`
	Items Items  `json:"items"`
}

type Items struct {
	Enum []string `json:"enum"`
}
