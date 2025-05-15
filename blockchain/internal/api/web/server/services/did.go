package services

import (
	_ "blockchain/internal/api/web/server/domain"
	"blockchain/internal/core"
	core_type "blockchain/internal/core/types"
	"context"
	"encoding/json"
	"strings"
)

// DidService defines the interface for managing Decentralized Identifiers (DIDs)
// and their associated access rights.
type DidService interface {
	GetDIDs(ctx context.Context, chain *core.Blockchain) (*[]core_type.Did, error)
}

// didService is a concrete implementation of the DidService interface.
type didService struct{}

// NewDidService creates and returns a new instance of the DidService implementation.
func NewDidService() DidService {
	return &didService{}
}

// GetDIDs returns all DIDs in the blockchain
func (s *didService) GetDIDs(ctx context.Context, chain *core.Blockchain) (*[]core_type.Did, error) {
	var dids []core_type.Did
	var did core_type.Did
	var err error
	for _, block := range *chain {
		for _, transaction := range block.Transactions {
			err = json.Unmarshal(transaction, &did)
			if err != nil {
				return nil, err
			}
			if strings.HasPrefix(did.ID, "did:batterypass:") {
				dids = append(dids, did)
			}
		}
	}
	return &dids, nil
}
