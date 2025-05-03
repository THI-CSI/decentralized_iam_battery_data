// Code generated from JSON Schema using quicktype. DO NOT EDIT.
// To parse and unparse this JSON data, add this code to your project and do:
//
//    didSchema, err := UnmarshalDidSchema(bytes)
//    bytes, err = didSchema.Marshal()
//
//    vcRecordSchema, err := UnmarshalVcRecordSchema(bytes)
//    bytes, err = vcRecordSchema.Marshal()
//
//    vcSchema, err := UnmarshalVcSchema(bytes)
//    bytes, err = vcSchema.Marshal()

package core

import "encoding/json"

func UnmarshalDidSchema(data []byte) (DidSchema, error) {
	var r DidSchema
	err := json.Unmarshal(data, &r)
	return r, err
}

func (r *DidSchema) Marshal() ([]byte, error) {
	return json.Marshal(r)
}

func UnmarshalVcRecordSchema(data []byte) (VcRecordSchema, error) {
	var r VcRecordSchema
	err := json.Unmarshal(data, &r)
	return r, err
}

func (r *VcRecordSchema) Marshal() ([]byte, error) {
	return json.Marshal(r)
}

func UnmarshalVcSchema(data []byte) (VcSchema, error) {
	var r VcSchema
	err := json.Unmarshal(data, &r)
	return r, err
}

func (r *VcSchema) Marshal() ([]byte, error) {
	return json.Marshal(r)
}

type DidSchema struct {
	Schema      string              `json:"$schema"`
	ID          string              `json:"$id"`
	Title       string              `json:"title"`
	Description string              `json:"description"`
	Type        TypeElement         `json:"type"`
	Required    []string            `json:"required"`
	Properties  DidSchemaProperties `json:"properties"`
	Defs        DidSchemaDefs       `json:"$defs"`
}

type DidSchemaDefs struct {
	VerificationMethod VerificationMethod `json:"VerificationMethod"`
	ServiceEndpoint    ServiceEndpoint    `json:"ServiceEndpoint"`
}

type ServiceEndpoint struct {
	Type        TypeElement               `json:"type"`
	Required    []string                  `json:"required"`
	Description string                    `json:"description"`
	Properties  ServiceEndpointProperties `json:"properties"`
}

type ServiceEndpointProperties struct {
	ID              Revoked `json:"id"`
	Type            Revoked `json:"type"`
	ServiceEndpoint Issuer  `json:"serviceEndpoint"`
}

type Revoked struct {
	Type        TypeElement `json:"type"`
	Description string      `json:"description"`
}

type Issuer struct {
	Type        []TypeElement `json:"type"`
	Description string        `json:"description"`
}

type VerificationMethod struct {
	Type        TypeElement                  `json:"type"`
	Required    []string                     `json:"required"`
	Description string                       `json:"description"`
	Properties  VerificationMethodProperties `json:"properties"`
}

type VerificationMethodProperties struct {
	ID                 Revoked `json:"id"`
	Type               Revoked `json:"type"`
	Controller         Revoked `json:"controller"`
	PublicKeyMultibase Revoked `json:"publicKeyMultibase"`
}

type DidSchemaProperties struct {
	ID        ID        `json:"id"`
	Role      Role      `json:"role"`
	Owner     ID        `json:"owner"`
	PublicKey PublicKey `json:"publicKey"`
	Service   Service   `json:"service"`
	Created   Created   `json:"created"`
	Updated   Created   `json:"updated"`
	Revoked   Revoked   `json:"revoked"`
}

type Created struct {
	Type        TypeElement `json:"type"`
	Format      Format      `json:"format"`
	Description string      `json:"description"`
}

type ID struct {
	Type        TypeElement `json:"type"`
	Pattern     string      `json:"pattern"`
	Description string      `json:"description"`
}

type PublicKey struct {
	Ref         string `json:"$ref"`
	Description string `json:"description"`
}

type Role struct {
	Type        TypeElement `json:"type"`
	Enum        []string    `json:"enum"`
	Description string      `json:"description"`
}

type Service struct {
	Type        string       `json:"type"`
	Items       ItemsElement `json:"items"`
	Description string       `json:"description"`
}

type ItemsElement struct {
	Ref string `json:"$ref"`
}

type VcRecordSchema struct {
	Schema      string                   `json:"$schema"`
	ID          string                   `json:"$id"`
	Title       string                   `json:"title"`
	Description string                   `json:"description"`
	Type        TypeElement              `json:"type"`
	Required    []string                 `json:"required"`
	Properties  VcRecordSchemaProperties `json:"properties"`
}

type VcRecordSchemaProperties struct {
	ID        Created `json:"id"`
	VcHash    ID      `json:"vcHash"`
	Timestamp Created `json:"timestamp"`
	Revoked   Revoked `json:"revoked"`
}

type VcSchema struct {
	Schema      string             `json:"$schema"`
	ID          string             `json:"$id"`
	Title       string             `json:"title"`
	Description string             `json:"description"`
	Type        TypeElement        `json:"type"`
	Required    []string           `json:"required"`
	Properties  VcSchemaProperties `json:"properties"`
	Defs        VcSchemaDefs       `json:"$defs"`
	AllOf       []AllOf            `json:"allOf"`
}

type AllOf struct {
	If   If   `json:"if"`
	Then Then `json:"then"`
}

type If struct {
	Properties IfProperties `json:"properties"`
}

type IfProperties struct {
	CredentialSubject PurpleCredentialSubject `json:"credentialSubject"`
}

type PurpleCredentialSubject struct {
	Required []string `json:"required"`
}

type Then struct {
	Properties ThenProperties `json:"properties"`
}

type ThenProperties struct {
	Type FluffyType `json:"type"`
}

type FluffyType struct {
	Contains Contains `json:"contains"`
}

type Contains struct {
	Const string `json:"const"`
}

type VcSchemaDefs struct {
	BatteryPassRelationship BatteryPassRelationship `json:"BatteryPassRelationship"`
	BMSProduction           BMSProduction           `json:"BMSProduction"`
	ServiceAccess           ServiceAccess           `json:"ServiceAccess"`
}

type BMSProduction struct {
	Title      string                  `json:"title"`
	Type       TypeElement             `json:"type"`
	Required   []string                `json:"required"`
	Properties BMSProductionProperties `json:"properties"`
}

type BMSProductionProperties struct {
	ID         Created    `json:"id"`
	Type       PurpleType `json:"type"`
	BmsDid     ID         `json:"bmsDid"`
	ProducedOn Created    `json:"producedOn"`
	LotNumber  Revoked    `json:"lotNumber"`
}

type PurpleType struct {
	Const       string `json:"const"`
	Description string `json:"description"`
}

type BatteryPassRelationship struct {
	Title      string                            `json:"title"`
	Type       TypeElement                       `json:"type"`
	Required   []string                          `json:"required"`
	Properties BatteryPassRelationshipProperties `json:"properties"`
}

type BatteryPassRelationshipProperties struct {
	ID            Created    `json:"id"`
	Type          PurpleType `json:"type"`
	BatteryPassID Revoked    `json:"batteryPassId"`
}

type ServiceAccess struct {
	Title      string                  `json:"title"`
	Type       TypeElement             `json:"type"`
	Required   []string                `json:"required"`
	Properties ServiceAccessProperties `json:"properties"`
}

type ServiceAccessProperties struct {
	ID          Created    `json:"id"`
	Type        PurpleType `json:"type"`
	BmsDid      ID         `json:"bmsDid"`
	AccessLevel Role       `json:"accessLevel"`
	ValidFrom   Created    `json:"validFrom"`
	ValidUntil  Created    `json:"validUntil"`
}

type VcSchemaProperties struct {
	Context           Context                 `json:"@context"`
	ID                Created                 `json:"id"`
	Type              TentacledType           `json:"type"`
	Issuer            Issuer                  `json:"issuer"`
	Holder            Created                 `json:"holder"`
	IssuanceDate      Created                 `json:"issuanceDate"`
	ExpirationDate    Created                 `json:"expirationDate"`
	CredentialSubject FluffyCredentialSubject `json:"credentialSubject"`
	Proof             Revoked                 `json:"proof"`
}

type Context struct {
	OneOf       []OneOf `json:"oneOf"`
	Description string  `json:"description"`
}

type OneOf struct {
	Type   string      `json:"type"`
	Format *Format     `json:"format,omitempty"`
	Items  *OneOfItems `json:"items,omitempty"`
}

type OneOfItems struct {
	Type []TypeElement `json:"type"`
}

type FluffyCredentialSubject struct {
	OneOf       []ItemsElement `json:"oneOf"`
	Description string         `json:"description"`
}

type TentacledType struct {
	Type        string    `json:"type"`
	MinItems    int64     `json:"minItems"`
	Items       TypeItems `json:"items"`
	Contains    Contains  `json:"contains"`
	Description string    `json:"description"`
}

type TypeItems struct {
	Type TypeElement `json:"type"`
}

type TypeElement string

const (
	Boolean TypeElement = "boolean"
	Object  TypeElement = "object"
	String  TypeElement = "string"
)

type Format string

const (
	Date     Format = "date"
	DateTime Format = "date-time"
	URI      Format = "uri"
)
