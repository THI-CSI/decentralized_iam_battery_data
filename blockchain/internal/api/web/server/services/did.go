package services

import (
	"blockchain/internal/api/web/server/domain"
	_ "blockchain/internal/api/web/server/domain"
	"blockchain/internal/core"
	coreTypes "blockchain/internal/core/types"
	"context"
	"encoding/json"
	"strings"
)

// DidService defines the interface for managing Decentralized Identifiers (DIDs)
// and their associated access rights.
type DidService interface {
	GetDIDs(ctx context.Context, chain *core.Blockchain) (*[]coreTypes.Did, error)
	GetDID(userContext context.Context, chain *core.Blockchain, did string) (*coreTypes.Did, error)
	CreateDID(userContext context.Context, chain *core.Blockchain, create *domain.CreateDid) (*coreTypes.Did, error)
	RevokeDid(userContext context.Context, chain *core.Blockchain, did string) error
}

// didService is a concrete implementation of the DidService interface.
type didService struct{}

// NewDidService creates and returns a new instance of the DidService implementation.
func NewDidService() DidService {
	return &didService{}
}

// GetDIDs returns all DIDs in the blockchain
func (s *didService) GetDIDs(ctx context.Context, chain *core.Blockchain) (*[]coreTypes.Did, error) {
	var dids []coreTypes.Did
	var did coreTypes.Did
	var err error
	for i := len(*chain) - 1; i >= 0; i-- {
		block := chain.GetBlock(i)
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

// GetDID returns
func (s *didService) GetDID(userContext context.Context, chain *core.Blockchain, did string) (*coreTypes.Did, error) {
	return chain.FindDID(did)
}

func (s *didService) CreateDID(userContext context.Context, chain *core.Blockchain, createDid *domain.CreateDid) (*coreTypes.Did, error) {
	did := domain.ConvertRequestToDid(createDid)

	// Create Transaction
	if err := chain.AppendDid(&did); err != nil {
		return nil, err
	}

	return &did, nil
}

func (s *didService) RevokeDid(userContext context.Context, chain *core.Blockchain, didId string) error {
	did, err := chain.FindDID(didId)
	if err != nil {
		return domain.NotFoundError(err.Error())
	}

	did.Revoked = true
	if err := chain.AppendDid(did); err != nil {
		return err
	}

	return nil
}

func containsDid(didList []coreTypes.Did, didId string) bool {
	for _, did := range didList {
		if did.ID == didId {
			return true
		}
	}
	return false
}
