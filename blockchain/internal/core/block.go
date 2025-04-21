package core

import (
	"crypto/sha3"
	"encoding/hex"
	"time"
)

// Block represents a unit in the blockchain containing a set of Transactions.
// Each block is cryptographically linked to the previous one.
type Block struct {
	// Index is the position of the block in the chain.
	Index int
	// Timestamp is when the block was created.
	Timestamp time.Time
	// Hash is the cryptographic hash of this block.
	Hash string
	// PreviousBlockHash is the hash of the prior block.
	PreviousBlockHash string
	// Transactions holds all transactions in this block.
	Transactions []Transaction
}

// Calculates the SHA-256 hash of a block
func CalculateBlockHash(block Block) string {
	sha256 := sha3.New256()
	// TODO: We have to calculate a Merkle Tree Hash and add it to the record
	record := string(block.Index) + block.Timestamp.String() + block.PreviousBlockHash
	sha256.Write([]byte(record))
	hash := sha256.Sum(nil)
	return hex.EncodeToString(hash)
}

// Generate a Genisis Block
func GenerateGenisisBlock() Block {
	var block Block

	block.Index = 0
	block.Timestamp = time.Now()
	// Since this is the first block in the chain, the PreviousBlockHash is hardcoded
	block.PreviousBlockHash = "0000000000000000000000000000000000000000000000000000000000000000"
	block.Transactions = nil
	block.Hash = CalculateBlockHash(block)

	return block
}

// Generate a Block with the data of the previous block and a list of transactions
func GenerateBlock(currentBlock Block, transactions []Transaction) Block {
	var block Block

	block.Index = currentBlock.Index + 1
	block.Timestamp = time.Now()
	block.PreviousBlockHash = currentBlock.Hash
	block.Transactions = transactions
	block.Hash = CalculateBlockHash(block)

	return block
}
