package services

import (
	"blockchain/internal/core"
	coreTypes "blockchain/internal/core/types"
	"context"
	"encoding/json"
	"strings"
)

// DidService defines the interface for managing Decentralized Identifiers (DIDs)
// and their associated access rights.
type DidService interface {
	GetDIDs(ctx context.Context) (*[]coreTypes.Did, error)
	GetDID(userContext context.Context, did string) (*coreTypes.Did, error)
	CreateOrModifyDID(userContext context.Context, create *domain.CreateDid) (*coreTypes.Did, error)
	RevokeDid(userContext context.Context, did string) error
}

// didService is a concrete implementation of the DidService interface.
type didService struct {
	chain *core.Blockchain
}

// NewDidService creates and returns a new instance of the DidService implementation.
func NewDidService(chain *core.Blockchain) DidService {
	return &didService{chain: chain}
}

// GetDIDs returns all DIDs in the blockchain
func (s *didService) GetDIDs(ctx context.Context) (*[]coreTypes.Did, error) {
	var dids []coreTypes.Did
	var did coreTypes.Did
	var err error
	for i := len(*s.chain) - 1; i >= 0; i-- {
		block := *s.chain.GetBlock(i)
		for _, transaction := range block.Transactions {
			err = json.Unmarshal(transaction, &did)
			if err != nil {
				return nil, err
			}
			if strings.HasPrefix(did.ID, "did:batterypass:") && !containsDid(dids, did.ID) {
				dids = append(dids, did)
			}
		}
	}
	return &dids, nil
}

// GetDID returns a single DID
func (s *didService) GetDID(userContext context.Context, did string) (*coreTypes.Did, error) {
	return s.chain.FindDID(did)
}

// CreateDID appends a new DID to the blockcahin
func (s *didService) CreateDID(userContext context.Context, createDid *domain.CreateDid) (*coreTypes.Did, error) {
	did := domain.ConvertRequestToDid(createDid)

	// Create Transaction
	if err := s.chain.AppendDid(&did); err != nil {
		return nil, err
	}

	return &did, nil
}

// RevokeDid revokes an existing DID on the blockchain
func (s *didService) RevokeDid(userContext context.Context, didId string) error {
	did, err := s.chain.FindDID(didId)
	if err != nil {
		return domain.NotFoundError(err.Error())
	}

	did.Revoked = true
	if err := s.chain.AppendDid(did); err != nil {
		return domain.BadRequestError(err.Error())
	}

	return nil
}

// containsDid checks if a DID is in a list of DIDs
//
// true if the list contains this DID already
// false if the list does not contain this DID
func containsDid(didList []coreTypes.Did, didId string) bool {
	for _, did := range didList {
		if did.ID == didId {
			return true
		}
	}
	return false
}
