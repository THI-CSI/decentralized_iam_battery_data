package services

import (
	"blockchain/internal/core"
	"context"
	"fmt"
)

// BlockService defines the interface for returning blocks of the blockchain
type BlockService interface {
	GetBlocks(ctx context.Context) (*domain.BlockchainResponse, error)
	GetBlock(userContext context.Context, blockId int) (*domain.BlockResponse, error)
}

// blockService is a concrete implementation of the BlockService interface.
type blockService struct {
	chain *core.Blockchain
}

// NewBlockService creates and returns a new instance of the BlockService implementation.
func NewBlockService(chain *core.Blockchain) BlockService {
	return &blockService{chain: chain}
}

// GetBlocks gets all blocks
func (s *blockService) GetBlocks(ctx context.Context) (*domain.BlockchainResponse, error) {
	var blockchainResponse domain.BlockchainResponse
	for _, block := range *s.chain {
		blockchainResponse = append(blockchainResponse, domain.ConvertBlockToResponse(block))
	}
	return &blockchainResponse, nil
}

// GetBlock get a block by an id
func (s *blockService) GetBlock(ctx context.Context, blockId int) (*domain.BlockResponse, error) {
	block := s.chain.GetBlock(blockId)
	if block == nil {
		return nil, fmt.Errorf("block with id '%d' not found", blockId)
	}
	blockResponse := domain.ConvertBlockToResponse(*block)
	return &blockResponse, nil
}
