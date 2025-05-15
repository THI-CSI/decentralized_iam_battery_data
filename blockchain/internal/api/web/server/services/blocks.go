package services

import (
	"blockchain/internal/api/web/server/domain"
	"blockchain/internal/core"
	"context"
)

// BlockService defines the interface for returning blocks of the blockchain
type BlockService interface {
	// GetBlocks returns all blocks of the blockchain
	GetBlocks(ctx context.Context, chain *core.Blockchain) (*domain.BlockchainResponse, error)
}

// blockService is a concrete implementation of the BlockService interface.
type blockService struct{}

// NewBlockService creates and returns a new instance of the BlockService implementation.
func NewBlockService() BlockService {
	return &blockService{}
}

// GetBlocks gets all blocks
func (s *blockService) GetBlocks(ctx context.Context, chain *core.Blockchain) (*domain.BlockchainResponse, error) {
	var blockchainResponse domain.BlockchainResponse
	for _, block := range *chain {
		blockchainResponse = append(blockchainResponse, domain.ConvertBlockToResponse(block))
	}
	return &blockchainResponse, nil
}
