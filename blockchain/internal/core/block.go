package core

import (
	"crypto/sha256"
	"encoding/hex"
	"fmt"
	"log/slog"
	"strings"
	"time"
)

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
	// Transactions holds all transactions in this block.
	Transactions []Transaction
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
	sha256 := sha256.New()
	record := fmt.Sprintf("%d%s%s%s", block.Index, block.Timestamp, block.PreviousBlockHash, block.MerkleRoot)
	sha256.Write([]byte(record))
	hash := sha256.Sum(nil)
	return hex.EncodeToString(hash)
}

// Generate a Genesis Block
func GenerateGenesisBlock() Block {
	var block Block

	t := time.Now()

	block.Index = 0
	block.Timestamp = t.Format("2006-01-02 15:04:05")
	// Since this is the first block in the chain, the PreviousBlockHash is hardcoded
	block.PreviousBlockHash = "0000000000000000000000000000000000000000000000000000000000000000"
	block.Transactions = nil
	block.Hash = CalculateBlockHash(block)

	return block
}

// Generate a Block with the data of the previous block and a list of transactions
func GenerateBlock(currentBlock Block, transactions []Transaction) Block {
	var block Block

	t := time.Now()

	block.Index = currentBlock.Index + 1
	block.Timestamp = t.Format("2006-01-02 15:04:05")
	block.PreviousBlockHash = currentBlock.Hash
	block.Transactions = transactions
	block.MerkleRoot = BuildMerkleRoot(transactions)
	block.Hash = CalculateBlockHash(block)

	return block
}

// Validate a chain of blocks
func ValidateBlockchain(chain []Block) bool {
	for index := range chain {
		currentBlock := chain[index]

		// Check if the block hash is valid
		if CalculateBlockHash(currentBlock) != currentBlock.Hash {
			slog.Error(fmt.Sprintf("The hash of block %v is not valid!", index))
			return false
		}

		// Skip the other checks if it is the Genesis block
		if index == 0 {
			continue
		}

		previousBlock := chain[index-1]

		// Check if the index is incrementing
		if previousBlock.Index+1 != currentBlock.Index {
			return false
		}

		// Checks if the PreviousBlockHash is the hash of the previous block
		if previousBlock.Hash != currentBlock.PreviousBlockHash {
			return false
		}

		// TODO: Add check to validate the Transactions
	}

	return true
}
