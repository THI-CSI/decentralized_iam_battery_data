package services

import (
	"blockchain/internal/core"
	"context"
	"fmt"
)

// BlockService defines the interface for returning blocks of the blockchain
type BlockService interface {
	GetBlocks(ctx context.Context) (*[]core.Block, error)
	GetBlock(ctx context.Context, blockId int) (*core.Block, error)
}

// blockService is a concrete implementation of the BlockService interface.
type blockService struct {
	chain *core.Blockchain // This is a pointer to your Blockchain type
}

// NewBlockService creates and returns a new instance of the BlockService implementation.
func NewBlockService(chain *core.Blockchain) BlockService {
	return &blockService{chain: chain}
}

// GetBlocks gets all blocks
func (s *blockService) GetBlocks(ctx context.Context) (*[]core.Block, error) {
	return (*[]core.Block)(s.chain), nil
}

// GetBlock get a block by an id
func (s *blockService) GetBlock(ctx context.Context, blockId int) (*core.Block, error) {
	block := s.chain.GetBlock(blockId)
	if block == nil {
		return nil, fmt.Errorf("block with id '%d' not found", blockId)
	}
	return block, nil
}
