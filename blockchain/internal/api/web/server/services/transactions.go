package services

import (
	"blockchain/internal/core"
	"context"
	"encoding/json"
	"fmt"
)

// TransactionService defines the interface for returning transactions of a block of the blockchain
type TransactionService interface {
	GetTransactions(ctx context.Context, blockId int) (*[]json.RawMessage, error)
}

// transactionService is a concrete implementation of the TransactionService interface.
type transactionService struct {
	chain *core.Blockchain
}

// NewTransactionService creates and returns a new instance of the TransactionService implementation.
func NewTransactionService(chain *core.Blockchain) *transactionService {
	return &transactionService{chain: chain}
}

// GetTransactions gets all transactions of a block
func (s *transactionService) GetTransactions(ctx context.Context, blockId int) (*[]json.RawMessage, error) {
	block := s.chain.GetBlock(blockId)
	if block == nil {
		return nil, fmt.Errorf("block %d not found", blockId)
	}

	return &block.Transactions, nil
}
