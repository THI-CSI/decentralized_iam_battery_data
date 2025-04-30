// Code generated from JSON Schema using quicktype. DO NOT EDIT.
// To parse and unparse this JSON data, add this code to your project and do:
//
//    revokeAccess, err := UnmarshalRevokeAccess(bytes)
//    bytes, err = revokeAccess.Marshal()

package models

import "encoding/json"

func UnmarshalRevokeAccess(data []byte) (RevokeAccess, error) {
	var r RevokeAccess
	err := json.Unmarshal(data, &r)
	return r, err
}

func (r *RevokeAccess) Marshal() ([]byte, error) {
	return json.Marshal(r)
}

type RevokeAccess struct {
	Schema     string                 `json:"$schema"`
	ID         string                 `json:"$id"`
	Title      string                 `json:"title"`
	Type       string                 `json:"type"`
	Required   []string               `json:"required"`
	Properties RevokeAccessProperties `json:"properties"`
}

type RevokeAccessProperties struct {
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
	RevokedVC Proof `json:"revokedVC"`
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
