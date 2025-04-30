// Code generated from JSON Schema using quicktype. DO NOT EDIT.
// To parse and unparse this JSON data, add this code to your project and do:
//
//    grantAccess, err := UnmarshalGrantAccess(bytes)
//    bytes, err = grantAccess.Marshal()

package models

import "encoding/json"

func UnmarshalGrantAccess(data []byte) (GrantAccess, error) {
	var r GrantAccess
	err := json.Unmarshal(data, &r)
	return r, err
}

func (r *GrantAccess) Marshal() ([]byte, error) {
	return json.Marshal(r)
}

type GrantAccess struct {
	Schema     string                `json:"$schema"`
	ID         string                `json:"$id"`
	Title      string                `json:"title"`
	Type       string                `json:"type"`
	Required   []string              `json:"required"`
	Properties GrantAccessProperties `json:"properties"`
}

type GrantAccessProperties struct {
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
	Grantee     IssuanceDate `json:"grantee"`
	Resource    Proof        `json:"resource"`
	AccessLevel Items        `json:"accessLevel"`
}

type Items struct {
	Enum []string `json:"enum"`
}

type IssuanceDate struct {
	Type   string `json:"type"`
	Format string `json:"format"`
}

type Proof = shared.Proof
	Type string `json:"type"`
}

type Type struct {
	Type  string `json:"type"`
	Items Items  `json:"items"`
}
