// Code generated from JSON Schema using quicktype. DO NOT EDIT.
// To parse and unparse this JSON data, add this code to your project and do:
//
//    bmsLinked, err := UnmarshalBmsLinked(bytes)
//    bytes, err = bmsLinked.Marshal()

package models

import "encoding/json"

func UnmarshalBmsLinked(data []byte) (BmsLinked, error) {
	var r BmsLinked
	err := json.Unmarshal(data, &r)
	return r, err
}

func (r *BmsLinked) Marshal() ([]byte, error) {
	return json.Marshal(r)
}

type BmsLinked struct {
	Schema     string              `json:"$schema"`
	ID         string              `json:"$id"`
	Title      string              `json:"title"`
	Type       string              `json:"type"`
	Required   []string            `json:"required"`
	Properties BmsLinkedProperties `json:"properties"`
}

type BmsLinkedProperties struct {
	Context           Context           `json:"@context"`
	Type              Type              `json:"type"`
	Issuer            Issu              `json:"issuer"`
	IssuanceDate      Issu              `json:"issuanceDate"`
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
	BmsID         Proof `json:"bmsId"`
	BatteryPassID Proof `json:"batteryPassId"`
}

type Proof = shared.Proof
	Type string `json:"type"`
}

type Issu struct {
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
