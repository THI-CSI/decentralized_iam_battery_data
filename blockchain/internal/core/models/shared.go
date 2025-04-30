// Package models contains data structures for credential and verification handling
package models

// Context represents the JSON-LD context definition for credentials
type Context struct {
	Type []string `json:"type"`
}

// CredentialSubject defines the structure and requirements for a credential subject
type CredentialSubject struct {
	Type       string                      `json:"type"`
	Required   []string                    `json:"required"`
	Properties CredentialSubjectProperties `json:"properties"`
}

// CredentialSubjectProperties contains the specific properties for a credential subject
type CredentialSubjectProperties struct {
	Target        IssuanceDate `json:"target"`
	Modifications Proof        `json:"modifications"`
}

// Proof represents cryptographic proof information
type Proof struct {
	Type string `json:"type"`
}

// IssuanceDate defines the structure for credential issuance date information
type IssuanceDate struct {
	Type   string `json:"type"`
	Format string `json:"format"`
}

// Type represents a type definition with associated items
type Type struct {
	Type  string `json:"type"`
	Items Items  `json:"items"`
}

// Items contains enumeration values for a type
type Items struct {
	Enum []string `json:"enum"`
}
