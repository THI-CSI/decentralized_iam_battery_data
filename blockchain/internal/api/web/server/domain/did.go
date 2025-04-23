package domain

// CreateDid represents a request payload to create a new Decentralized Identifier (DID).
type CreateDid struct {
	// PublicKey is the public key associated with the DID. It is a required field.
	PublicKey string `json:"publicKey" validate:"required"`
}

// Did represents a Decentralized Identifier (DID).
// This struct is currently empty and may be used as a placeholder or extended later.
type Did struct{}

// AccessRight represents a permission or access right associated with a DID.
// This struct is currently empty and may be extended to include specific permissions or resource identifiers.
type AccessRight struct{}

// GrantAccessRights represents a request to assign a specific role to a DID.
type GrantAccessRights struct {
	// Did is the identifier to which the access role is granted. It is required.
	Did string `json:"did" validate:"required"`
	// Role is the name of the access role to be granted. It is required.
	Role string `json:"role" validate:"required"`
}

// AccessRightsResponse encapsulates a list of access rights.
type AccessRightsResponse struct {
	// AccessRights is a list of access rights associated with a DID.
	AccessRights []*AccessRight `json:"accessRights"`
}
