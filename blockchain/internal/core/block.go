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
const TransactionThreshold = 1

// Block represents a unit in the blockchain containing a set of Transactions.
// Each block is cryptographically linked to the previous one.
type Block struct {
	Index             int               `json:"Index"`
	Timestamp         string            `json:"Timestamp"`
	Hash              string            `json:"Hash"`
	PreviousBlockHash string            `json:"PreviousBlockHash"`
	Transactions      []json.RawMessage `json:"Transactions"`
	MerkleRoot        string            `json:"MerkleRoot"`
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
	_, err := hasher.Write([]byte(record))
	if err != nil {
		print("Error: Could not write to hasher: %v\n", err)
		return "" // TODO: This is an insecure fallback
	}
	hash := hasher.Sum(nil)
	return hex.EncodeToString(hash)
}

// GenerateGenesisBlock Generate the Genesis Block
func GenerateGenesisBlock() Block {
	var block Block

	if err := CreateTrustAnchor(); err != nil {
		fmt.Println("CreateTrustAnchor method failed: ", err)
	}

	block.Index = 0
	block.Timestamp = time.Now().Format(time.RFC3339)
	// Since this is the first block in the chain, the PreviousBlockHash is hardcoded
	block.PreviousBlockHash = "0000000000000000000000000000000000000000000000000000000000000000"
	block.Transactions = PendingTransactions
	block.MerkleRoot = "0000000000000000000000000000000000000000000000000000000000000000"
	block.Hash = CalculateBlockHash(block)

	PendingTransactions = nil

	return block
}

// GenerateBlock Generate a Block with the data of the previous block and a list of transactions
func GenerateBlock(currentBlock *Block) Block {
	var block Block

	block.Index = currentBlock.Index + 1
	block.Timestamp = time.Now().Format(time.RFC3339)
	block.PreviousBlockHash = currentBlock.Hash
	block.Transactions = PendingTransactions
	block.MerkleRoot = BuildMerkleRoot(PendingTransactions)
	block.Hash = CalculateBlockHash(block)

	PendingTransactions = nil

	return block
}
