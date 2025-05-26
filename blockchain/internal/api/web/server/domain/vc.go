package domain

import "time"

// VCRequest represents a request for creating a Verifiable Credential with expiration date, id, and hash.
type VCRequest struct {
	// Expiration Date of the related Verifiable Credential
	ExpirationDate *time.Time `json:"expirationDate,omitempty" validate:"required"`

	// The identifier of the Verifiable Credential.
	ID string `json:"id" validate:"required"`

	// A SHA-256 hash of the complete VC in hexadecimal format.
	VcHash string `json:"vcHash" validate:"required"`
}
