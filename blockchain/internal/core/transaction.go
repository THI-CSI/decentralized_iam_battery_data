package core

import (
	"crypto/sha3"
	"encoding/hex"
	"fmt"
	"time"
)

// TransactionType defines the type of transaction in the system.
// It is a string-based type for better readability and type safety.
type TransactionType string

const (
	// Create represents a transaction that creates a new entity or record.
	Create TransactionType = "Create"
	// Modify represents a transaction that modifies an existing entity or record.
	Modify TransactionType = "Modify"
	// Grant represents a transaction that grants permissions or access.
	Grant TransactionType = "Grant"
	// Revoke represents a transaction that revokes permissions or access.
	Revoke TransactionType = "Revoke"
)

// Transaction represents the header of a single action recorded in the blockchain
type Transaction struct {
	// Index is the sequential number of the transaction.
	Index int
	// Timestamp records the exact time the transaction occurred.
	Timestamp string
	// Type indicates the kind of transaction, such as Create or Modify.
	Type TransactionType
	// Data holds additional information related to the transaction.
	Data string
}

var pendingTransactions []Transaction // Adequate as long as the blockchain stays in RAM

// CreateTransaction creates a new transaction and adds it to the pending list
func CreateTransaction(txType TransactionType, data string) Transaction {
	tx := Transaction{
		Index:     len(pendingTransactions), // Adequate as long as the blockchain stays in RAM
		Timestamp: time.Now().String(),
		Type:      txType,
		Data:      data,
	}
	pendingTransactions = append(pendingTransactions, tx)
	return tx
}

// CalculateTransactionHash computes the SHA-256 hash of a transaction
func CalculateTransactionHash(tx Transaction) string {
	record := fmt.Sprintf("%d%s%s", tx.Index, tx.Timestamp, string(tx.Type))
	hash := sha3.Sum256([]byte(record))
	return hex.EncodeToString(hash[:])
}

// BuildMerkleRoot computes the Merkle Root from a list of transactions
func BuildMerkleRoot(txs []Transaction) string {
	if len(txs) == 0 {
		return "0"
	}

	// Step 1: Hash each transaction
	hashes := make([]string, len(txs))
	for i, tx := range txs {
		hashes[i] = CalculateTransactionHash(tx)
	}

	// Step 2: Build the tree
	for len(hashes) > 1 {
		var newLevel []string

		for i := 0; i < len(hashes); i += 2 {
			// If odd number of hashes, duplicate the last
			var left = hashes[i]
			var right string
			if i+1 < len(hashes) {
				right = hashes[i+1]
			} else {
				// Duplicate the last hash
				right = left
			}
			// Concatenate and hash the pair
			combined := fmt.Sprintf("%s%s", left, right)
			hash := sha3.Sum256([]byte(combined))
			newLevel = append(newLevel, hex.EncodeToString(hash[:]))
		}

		hashes = newLevel
	}

	// Root hash is the only hash left
	return hashes[0]
}
