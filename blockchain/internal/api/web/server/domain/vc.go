package domain

import "time"

type VCRequest struct {
	// Expiration Date of the related Verifiable Credential
	ExpirationDate *time.Time `json:"expirationDate,omitempty" validate:"required"`

	// The identifier of the Verifiable Credential.
	ID string `json:"id" validate:"required"`

	// A SHA-256 hash of the complete VC in hexadecimal format.
	VcHash string `json:"vcHash" validate:"required"`
}
