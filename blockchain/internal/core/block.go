package core

import (
	"crypto/sha3"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"strings"
	"time"
)

// TransactionThreshold is the number of PendingTransactions required to create a new block.
const TransactionThreshold = 10

// Block represents a unit in the blockchain containing a set of Transactions.
// Each block is cryptographically linked to the previous one.
type Block struct {
	// Index is the position of the block in the chain.
	Index int
	// Timestamp is when the block was created.
	Timestamp string
	// Hash is the cryptographic hash of this block.
	Hash string
	// PreviousBlockHash is the hash of the prior block.
	PreviousBlockHash string
	// Transactions hold all transactions in this block.
	Transactions []json.RawMessage
	// MerkleRoot holds the fingerprint of the whole merkle tree
	MerkleRoot string
}

// Returns a more readable string representation of the block structure
func (b Block) String() string {
	var block string

	block = strings.Repeat("-", 85) + "\n"
	block += fmt.Sprintf("Index: %v\n", b.Index)
	block += fmt.Sprintf("Timestamp: %v\n", b.Timestamp)
	block += fmt.Sprintf("Hash: %v\n", b.Hash)
	block += fmt.Sprintf("PreviousBlockHash: %v\n", b.PreviousBlockHash)
	block += fmt.Sprintf("Transactions: %v\n", len(b.Transactions))
	block += strings.Repeat("-", 85)

	return block
}

// CalculateBlockHash computes the SHA-256 hash of a block
func CalculateBlockHash(block Block) string {
	hasher := sha3.New256()
	record := fmt.Sprintf("%d%s%s%s", block.Index, block.Timestamp, block.PreviousBlockHash, block.MerkleRoot)
	hasher.Write([]byte(record))
	hash := hasher.Sum(nil)
	return hex.EncodeToString(hash)
}

// GenerateGenesisBlock Generate a Genesis Block
func GenerateGenesisBlock() Block {
	var block Block

	CreateTrustAnchor()

	block.Index = 0
	block.Timestamp = time.Now().Format("2006-01-02 15:04:05")
	// Since this is the first block in the chain, the PreviousBlockHash is hardcoded
	block.PreviousBlockHash = "0000000000000000000000000000000000000000000000000000000000000000"
	block.Transactions = PendingTransactions
	block.Hash = CalculateBlockHash(block)

	PendingTransactions = PendingTransactions[:0]

	return block
}

// GenerateBlock Generate a Block with the data of the previous block and a list of transactions
func GenerateBlock(currentBlock Block) Block {
	var block Block

	block.Index = currentBlock.Index + 1
	block.Timestamp = time.Now().Format("2006-01-02 15:04:05")
	block.PreviousBlockHash = currentBlock.Hash
	block.Transactions = PendingTransactions
	block.MerkleRoot = BuildMerkleRoot(PendingTransactions)
	block.Hash = CalculateBlockHash(block)

	PendingTransactions = PendingTransactions[:0]

	return block
}
