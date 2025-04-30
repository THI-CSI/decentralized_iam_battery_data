// Code generated from JSON Schema using quicktype. DO NOT EDIT.
// To parse and unparse this JSON data, add this code to your project and do:
//
//    modifyEntity, err := UnmarshalModifyEntity(bytes)
//    bytes, err = modifyEntity.Marshal()

package models

import "encoding/json"

func UnmarshalModifyEntity(data []byte) (ModifyEntity, error) {
	var r ModifyEntity
	err := json.Unmarshal(data, &r)
	return r, err
}

func (r *ModifyEntity) Marshal() ([]byte, error) {
	return json.Marshal(r)
}

type ModifyEntity struct {
	Schema     string                 `json:"$schema"`
	ID         string                 `json:"$id"`
	Title      string                 `json:"title"`
	Type       string                 `json:"type"`
	Required   []string               `json:"required"`
	Properties ModifyEntityProperties `json:"properties"`
}

type ModifyEntityProperties struct {
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
	Target        IssuanceDate `json:"target"`
	Modifications Proof        `json:"modifications"`
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
