package services

import (
	"blockchain/internal/api/web/server/domain"
	"context"
)

// DidService defines the interface for managing Decentralized Identifiers (DIDs)
// and their associated access rights.
type DidService interface {
	// CreateDid registers a new DID using the provided public key.
	// Returns the created DID object or an error.
	CreateDid(ctx context.Context, createDid *domain.CreateDid) (*domain.Did, error)

	// GrantAccessRight assigns an access role to a DID.
	// Returns an error if the operation fails.
	GrantAccessRight(ctx context.Context, grantAccessRights *domain.GrantAccessRights) error

	// GetAccessRightsForDid fetches all access rights assigned to a specific DID.
	// Returns a slice of AccessRight or an error.
	GetAccessRightsForDid(ctx context.Context, didId string) ([]*domain.AccessRight, error)
}

// didService is a concrete implementation of the DidService interface.
type didService struct{}

// NewDidService creates and returns a new instance of the DidService implementation.
func NewDidService() DidService {
	return &didService{}
}

// CreateDid creates a new DID based on the provided input.
// Currently returns a placeholder response.
func (s *didService) CreateDid(ctx context.Context, createDid *domain.CreateDid) (*domain.Did, error) {
	return &domain.Did{}, nil
}

// GrantAccessRight grants the specified access role to the given DID.
// Currently a placeholder with no operation.
func (s *didService) GrantAccessRight(ctx context.Context, grantAccessRights *domain.GrantAccessRights) error {
	return nil
}

// GetAccessRightsForDid returns a list of access rights assigned to a DID.
// Currently returns an empty list as a placeholder.
func (s *didService) GetAccessRightsForDid(ctx context.Context, didId string) ([]*domain.AccessRight, error) {
	return []*domain.AccessRight{}, nil
}
