// Code generated from JSON Schema using quicktype. DO NOT EDIT.
// To parse and unparse this JSON data, add this code to your project and do:
//
//    bmsLinkedSchema, err := UnmarshalBmsLinkedSchema(bytes)
//    bytes, err = bmsLinkedSchema.Marshal()
//
//    createEntitySchema, err := UnmarshalCreateEntitySchema(bytes)
//    bytes, err = createEntitySchema.Marshal()
//
//    didDocumentSchema, err := UnmarshalDidDocumentSchema(bytes)
//    bytes, err = didDocumentSchema.Marshal()
//
//    grantAccessSchema, err := UnmarshalGrantAccessSchema(bytes)
//    bytes, err = grantAccessSchema.Marshal()
//
//    modifyEntitySchema, err := UnmarshalModifyEntitySchema(bytes)
//    bytes, err = modifyEntitySchema.Marshal()
//
//    producedSchema, err := UnmarshalProducedSchema(bytes)
//    bytes, err = producedSchema.Marshal()
//
//    revokeAccessSchema, err := UnmarshalRevokeAccessSchema(bytes)
//    bytes, err = revokeAccessSchema.Marshal()

package core

import "encoding/json"

func UnmarshalBmsLinkedSchema(data []byte) (BmsLinkedSchema, error) {
	var r BmsLinkedSchema
	err := json.Unmarshal(data, &r)
	return r, err
}

func (r *BmsLinkedSchema) Marshal() ([]byte, error) {
	return json.Marshal(r)
}

func UnmarshalCreateEntitySchema(data []byte) (CreateEntitySchema, error) {
	var r CreateEntitySchema
	err := json.Unmarshal(data, &r)
	return r, err
}

func (r *CreateEntitySchema) Marshal() ([]byte, error) {
	return json.Marshal(r)
}

func UnmarshalDidDocumentSchema(data []byte) (DidDocumentSchema, error) {
	var r DidDocumentSchema
	err := json.Unmarshal(data, &r)
	return r, err
}

func (r *DidDocumentSchema) Marshal() ([]byte, error) {
	return json.Marshal(r)
}

func UnmarshalGrantAccessSchema(data []byte) (GrantAccessSchema, error) {
	var r GrantAccessSchema
	err := json.Unmarshal(data, &r)
	return r, err
}

func (r *GrantAccessSchema) Marshal() ([]byte, error) {
	return json.Marshal(r)
}

func UnmarshalModifyEntitySchema(data []byte) (ModifyEntitySchema, error) {
	var r ModifyEntitySchema
	err := json.Unmarshal(data, &r)
	return r, err
}

func (r *ModifyEntitySchema) Marshal() ([]byte, error) {
	return json.Marshal(r)
}

func UnmarshalProducedSchema(data []byte) (ProducedSchema, error) {
	var r ProducedSchema
	err := json.Unmarshal(data, &r)
	return r, err
}

func (r *ProducedSchema) Marshal() ([]byte, error) {
	return json.Marshal(r)
}

func UnmarshalRevokeAccessSchema(data []byte) (RevokeAccessSchema, error) {
	var r RevokeAccessSchema
	err := json.Unmarshal(data, &r)
	return r, err
}

func (r *RevokeAccessSchema) Marshal() ([]byte, error) {
	return json.Marshal(r)
}

type BmsLinkedSchema struct {
	Schema     string                    `json:"$schema"`
	ID         string                    `json:"$id"`
	Title      string                    `json:"title"`
	Type       TypeElement               `json:"type"`
	Required   []string                  `json:"required"`
	Properties BmsLinkedSchemaProperties `json:"properties"`
}

type BmsLinkedSchemaProperties struct {
	Context           Context                 `json:"@context"`
	Type              TypeClass               `json:"type"`
	Issuer            IssuanceDate            `json:"issuer"`
	IssuanceDate      IssuanceDate            `json:"issuanceDate"`
	CredentialSubject PurpleCredentialSubject `json:"credentialSubject"`
	Proof             Proof                   `json:"proof"`
}

type Context struct {
	Type []TypeElement `json:"type"`
}

type PurpleCredentialSubject struct {
	Type       TypeElement      `json:"type"`
	Required   []string         `json:"required"`
	Properties PurpleProperties `json:"properties"`
}

type PurpleProperties struct {
	BmsID         Proof `json:"bmsId"`
	BatteryPassID Proof `json:"batteryPassId"`
}

type Proof struct {
	Type TypeElement `json:"type"`
}

type IssuanceDate struct {
	Type   TypeElement `json:"type"`
	Format Format      `json:"format"`
}

type TypeClass struct {
	Type  TypeElement `json:"type"`
	Items RoleClass   `json:"items"`
}

type RoleClass struct {
	Enum []string `json:"enum"`
}

type CreateEntitySchema struct {
	Schema     string                       `json:"$schema"`
	ID         string                       `json:"$id"`
	Title      string                       `json:"title"`
	Type       TypeElement                  `json:"type"`
	Required   []string                     `json:"required"`
	Properties CreateEntitySchemaProperties `json:"properties"`
}

type CreateEntitySchemaProperties struct {
	Context           Context                 `json:"@context"`
	Type              TypeClass               `json:"type"`
	Issuer            IssuanceDate            `json:"issuer"`
	IssuanceDate      IssuanceDate            `json:"issuanceDate"`
	CredentialSubject FluffyCredentialSubject `json:"credentialSubject"`
	Proof             Proof                   `json:"proof"`
}

type FluffyCredentialSubject struct {
	Type       TypeElement      `json:"type"`
	Required   []string         `json:"required"`
	Properties FluffyProperties `json:"properties"`
}

type FluffyProperties struct {
	ID       IssuanceDate `json:"id"`
	Role     RoleClass    `json:"role"`
	Metadata Proof        `json:"metadata"`
}

type DidDocumentSchema struct {
	Schema      string                      `json:"$schema"`
	ID          string                      `json:"$id"`
	Title       string                      `json:"title"`
	Description string                      `json:"description"`
	Type        TypeElement                 `json:"type"`
	Required    []string                    `json:"required"`
	Properties  DidDocumentSchemaProperties `json:"properties"`
}

type DidDocumentSchemaProperties struct {
	Context            AuthenticationClass `json:"@context"`
	ID                 IssuanceDate        `json:"id"`
	VerificationMethod VerificationMethod  `json:"verificationMethod"`
	Authentication     AuthenticationClass `json:"authentication"`
	Service            Service             `json:"service"`
}

type AuthenticationClass struct {
	OneOf []Proof `json:"oneOf"`
}

type Service struct {
	Type  TypeElement `json:"type"`
	Items Proof       `json:"items"`
}

type VerificationMethod struct {
	Type  TypeElement             `json:"type"`
	Items VerificationMethodItems `json:"items"`
}

type VerificationMethodItems struct {
	Type       TypeElement     `json:"type"`
	Required   []string        `json:"required"`
	Properties ItemsProperties `json:"properties"`
}

type ItemsProperties struct {
	ID                 Proof `json:"id"`
	Type               Proof `json:"type"`
	Controller         Proof `json:"controller"`
	PublicKeyMultibase Proof `json:"publicKeyMultibase"`
}

type GrantAccessSchema struct {
	Schema     string                      `json:"$schema"`
	ID         string                      `json:"$id"`
	Title      string                      `json:"title"`
	Type       TypeElement                 `json:"type"`
	Required   []string                    `json:"required"`
	Properties GrantAccessSchemaProperties `json:"properties"`
}

type GrantAccessSchemaProperties struct {
	Context           Context                    `json:"@context"`
	Type              TypeClass                  `json:"type"`
	Issuer            IssuanceDate               `json:"issuer"`
	IssuanceDate      IssuanceDate               `json:"issuanceDate"`
	CredentialSubject TentacledCredentialSubject `json:"credentialSubject"`
	Proof             Proof                      `json:"proof"`
}

type TentacledCredentialSubject struct {
	Type       TypeElement         `json:"type"`
	Required   []string            `json:"required"`
	Properties TentacledProperties `json:"properties"`
}

type TentacledProperties struct {
	Grantee     IssuanceDate `json:"grantee"`
	Resource    Proof        `json:"resource"`
	AccessLevel RoleClass    `json:"accessLevel"`
}

type ModifyEntitySchema struct {
	Schema     string                       `json:"$schema"`
	ID         string                       `json:"$id"`
	Title      string                       `json:"title"`
	Type       TypeElement                  `json:"type"`
	Required   []string                     `json:"required"`
	Properties ModifyEntitySchemaProperties `json:"properties"`
}

type ModifyEntitySchemaProperties struct {
	Context           Context                 `json:"@context"`
	Type              TypeClass               `json:"type"`
	Issuer            IssuanceDate            `json:"issuer"`
	IssuanceDate      IssuanceDate            `json:"issuanceDate"`
	CredentialSubject StickyCredentialSubject `json:"credentialSubject"`
	Proof             Proof                   `json:"proof"`
}

type StickyCredentialSubject struct {
	Type       TypeElement      `json:"type"`
	Required   []string         `json:"required"`
	Properties StickyProperties `json:"properties"`
}

type StickyProperties struct {
	Target        IssuanceDate `json:"target"`
	Modifications Proof        `json:"modifications"`
}

type ProducedSchema struct {
	Schema     string                   `json:"$schema"`
	ID         string                   `json:"$id"`
	Title      string                   `json:"title"`
	Type       TypeElement              `json:"type"`
	Required   []string                 `json:"required"`
	Properties ProducedSchemaProperties `json:"properties"`
}

type ProducedSchemaProperties struct {
	Context           Context                 `json:"@context"`
	Type              TypeClass               `json:"type"`
	Issuer            IssuanceDate            `json:"issuer"`
	IssuanceDate      IssuanceDate            `json:"issuanceDate"`
	CredentialSubject IndigoCredentialSubject `json:"credentialSubject"`
	Proof             Proof                   `json:"proof"`
}

type IndigoCredentialSubject struct {
	Type       TypeElement      `json:"type"`
	Required   []string         `json:"required"`
	Properties IndigoProperties `json:"properties"`
}

type IndigoProperties struct {
	Owner IssuanceDate `json:"owner"`
	Owned Proof        `json:"owned"`
}

type RevokeAccessSchema struct {
	Schema     string                       `json:"$schema"`
	ID         string                       `json:"$id"`
	Title      string                       `json:"title"`
	Type       TypeElement                  `json:"type"`
	Required   []string                     `json:"required"`
	Properties RevokeAccessSchemaProperties `json:"properties"`
}

type RevokeAccessSchemaProperties struct {
	Context           Context                   `json:"@context"`
	Type              TypeClass                 `json:"type"`
	Issuer            IssuanceDate              `json:"issuer"`
	IssuanceDate      IssuanceDate              `json:"issuanceDate"`
	CredentialSubject IndecentCredentialSubject `json:"credentialSubject"`
	Proof             Proof                     `json:"proof"`
}

type IndecentCredentialSubject struct {
	Type       TypeElement        `json:"type"`
	Required   []string           `json:"required"`
	Properties IndecentProperties `json:"properties"`
}

type IndecentProperties struct {
	RevokedVC Proof `json:"revokedVC"`
}

type TypeElement string

const (
	Array  TypeElement = "array"
	Object TypeElement = "object"
	String TypeElement = "string"
)

type Format string

const (
	DateTime Format = "date-time"
	URI      Format = "uri"
)
