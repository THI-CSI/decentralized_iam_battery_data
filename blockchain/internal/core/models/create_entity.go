// Code generated from JSON Schema using quicktype. DO NOT EDIT.
// To parse and unparse this JSON data, add this code to your project and do:
//
//    createEntity, err := UnmarshalCreateEntity(bytes)
//    bytes, err = createEntity.Marshal()

package models

import "encoding/json"

func UnmarshalCreateEntity(data []byte) (CreateEntity, error) {
	var r CreateEntity
	err := json.Unmarshal(data, &r)
	return r, err
}

func (r *CreateEntity) Marshal() ([]byte, error) {
	return json.Marshal(r)
}

type CreateEntity struct {
	Schema     string                 `json:"$schema"`
	ID         string                 `json:"$id"`
	Title      string                 `json:"title"`
	Type       string                 `json:"type"`
	Required   []string               `json:"required"`
	Properties CreateEntityProperties `json:"properties"`
}

type CreateEntityProperties struct {
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
	ID       IssuanceDate `json:"id"`
	Role     Items        `json:"role"`
	Metadata Proof        `json:"metadata"`
}

type IssuanceDate struct {
	Type   string `json:"type"`
	Format string `json:"format"`
}

type Proof = shared.Proof
	Type string `json:"type"`
}

type Items struct {
	Enum []string `json:"enum"`
}

type Type struct {
	Type  string `json:"type"`
	Items Items  `json:"items"`
}
