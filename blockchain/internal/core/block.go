package core

import "time"

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
