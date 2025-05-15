package domain

import "blockchain/internal/core"

// BlockResponse represents a block in the blockchain
type BlockResponse struct {
	// Index is the position of the block in the chain.
	Index int `json:"id"`
	// Timestamp is when the block was created.
	Timestamp string `json:"timestamp"`
	// Hash is the cryptographic hash of this block.
	Hash string `json:"hash"`
	// PreviousBlockHash is the hash of the prior block.
	PreviousBlockHash string `json:"previousBlockHash"`
	// MerkleRoot holds the fingerprint of the whole merkle tree
	MerkleRoot string `json:"merkleRoot"`
}

// BlockchainResponse represents the blockchain
type BlockchainResponse []BlockResponse

func ConvertBlockToResponse(b core.Block) BlockResponse {
	return BlockResponse{
		Index:             b.Index,
		Timestamp:         b.Timestamp,
		Hash:              b.Hash,
		PreviousBlockHash: b.PreviousBlockHash,
		MerkleRoot:        b.MerkleRoot,
	}
}
