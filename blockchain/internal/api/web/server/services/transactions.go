package services

import (
	"blockchain/internal/api/web/server/models"
	"blockchain/internal/core"
	"context"
	"encoding/json"
	"fmt"
)

// TransactionService defines the interface for returning transactions of a block of the blockchain
type TransactionService interface {
	GetTransactions(ctx context.Context, blockId int) (*models.ResponseTransactionsSchema, error)
}

// transactionService is a concrete implementation of the TransactionService interface.
type transactionService struct {
	chain *core.Blockchain
}

// NewTransactionService creates and returns a new instance of the TransactionService implementation.
func NewTransactionService(chain *core.Blockchain) TransactionService {
	return &transactionService{chain: chain}
}

// GetTransactions gets all transactions of a block
func (s *transactionService) GetTransactions(ctx context.Context, blockId int) (*models.ResponseTransactionsSchema, error) {
	block := s.chain.GetBlock(blockId)
	if block == nil {
		return nil, fmt.Errorf("block %d not found", blockId)
	}

	var transactionResponse models.ResponseTransactionsSchema
	for _, transaction := range block.Transactions {
		marshalledTransaction, err := json.Marshal(transaction) // Assuming 'transaction' from block.Transactions is directly marshalable
		if err != nil {
			return nil, fmt.Errorf("failed to marshal transaction from blockchain: %w", err)
		}

		var item models.ResponseTransactionsSchema_Item
		err = item.UnmarshalJSON(marshalledTransaction)
		if err != nil {
			return nil, fmt.Errorf("failed to unmarshal transaction into ResponseTransactionsSchema_Item: %w", err)
		}

		transactionResponse = append(transactionResponse, item)
	}

	return &transactionResponse, nil
}
