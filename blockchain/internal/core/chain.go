package core

import (
	"fmt"
	"log/slog"
)

// ValidateBlockchain Validate a chain of blocks
func ValidateBlockchain(chain *[]Block) bool {
	for index := range *chain {
		currentBlock := (*chain)[index]

		// Check if the block hash is valid
		if CalculateBlockHash(currentBlock) != currentBlock.Hash {
			slog.Error(fmt.Sprintf("The hash of block %v is not valid!", index))
			return false
		}

		// Skip the other checks if it is the Genesis block
		if index == 0 {
			continue
		}

		previousBlock := (*chain)[index-1]

		// Check if the index is incrementing
		if previousBlock.Index+1 != currentBlock.Index {
			return false
		}

		// Checks if the PreviousBlockHash is the hash of the previous block
		if previousBlock.Hash != currentBlock.PreviousBlockHash {
			return false
		}

	}

	return true
}

// GetBlock Returns a block based on its id from the Blockchain
func GetBlock(chain *[]Block, id int) Block {
	for _, block := range *chain {
		if block.Index == id {
			return block
		}
	}
	return Block{}
}

// GetLastBlock Returns the last/newest block from the Blockchain
func GetLastBlock(chain *[]Block) Block {
	return (*chain)[len(*chain)-1]
}

// PrintChain Prints the complete Blockchain
func PrintChain(chain *[]Block) {
	for i, block := range *chain {
		fmt.Printf("Block %d: %+v\n", i, block)
	}
}

// CreateChain Creates a new Chain with the GenerateGenesisBlock method
func CreateChain() []Block {
	var chain *[]Block
	*chain = append(*chain, GenerateGenesisBlock())
	return *chain
}

// AppendBlock Appends a Block to a Chain
func AppendBlock(chain *[]Block, block Block) {
	*chain = append(*chain, block)
}
