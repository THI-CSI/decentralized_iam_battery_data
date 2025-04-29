// Code generated from JSON Schema using quicktype. DO NOT EDIT.
// To parse and unparse this JSON data, add this code to your project and do:
//
//    vc, err := UnmarshalVc(bytes)
//    bytes, err = vc.Marshal()

package core

import "encoding/json"

func UnmarshalVc(data []byte) (Vc, error) {
	var r Vc
	err := json.Unmarshal(data, &r)
	return r, err
}

func (r *Vc) Marshal() ([]byte, error) {
	return json.Marshal(r)
}

type Vc struct {
	Schema     string       `json:"$schema"`
	Title      string       `json:"title"`
	Type       string       `json:"type"`
	Properties VCProperties `json:"properties"`
	Required   []string     `json:"required"`
}

type VCProperties struct {
	Context           Context           `json:"@context"`
	ID                ID                `json:"id"`
	Type              Type              `json:"type"`
	Issuer            ID                `json:"issuer"`
	IssuanceDate      IssuanceDate      `json:"issuanceDate"`
	CredentialSubject CredentialSubject `json:"credentialSubject"`
	Proof             Proof             `json:"proof"`
}

type Context struct {
	Type     string       `json:"type"`
	Items    IssuanceDate `json:"items"`
	MinItems int64        `json:"minItems"`
}

type IssuanceDate struct {
	Type   string `json:"type"`
	Format string `json:"format"`
}

type CredentialSubject struct {
	Type       string                      `json:"type"`
	Properties CredentialSubjectProperties `json:"properties"`
	Required   []string                    `json:"required"`
}

type CredentialSubjectProperties struct {
	ID              ID              `json:"id"`
	BatteryIdentity BatteryIdentity `json:"batteryIdentity"`
}

type BatteryIdentity struct {
	Type       string                    `json:"type"`
	Properties BatteryIdentityProperties `json:"properties"`
	Required   []string                  `json:"required"`
}

type BatteryIdentityProperties struct {
	Manufacturer     Items        `json:"manufacturer"`
	Model            Items        `json:"model"`
	BatteryType      Items        `json:"batteryType"`
	PassportEndpoint IssuanceDate `json:"passportEndpoint"`
}

type Items struct {
	Type string `json:"type"`
}

type ID struct {
	Type    string `json:"type"`
	Pattern string `json:"pattern"`
}

type Proof struct {
	Type       string          `json:"type"`
	Properties ProofProperties `json:"properties"`
	Required   []string        `json:"required"`
}

type ProofProperties struct {
	Type               Contains     `json:"type"`
	Created            IssuanceDate `json:"created"`
	VerificationMethod ID           `json:"verificationMethod"`
	ProofPurpose       Contains     `json:"proofPurpose"`
	ProofValue         Items        `json:"proofValue"`
}

type Contains struct {
	Type string   `json:"type"`
	Enum []string `json:"enum"`
}

type Type struct {
	Type     string   `json:"type"`
	Items    Items    `json:"items"`
	Contains Contains `json:"contains"`
}
