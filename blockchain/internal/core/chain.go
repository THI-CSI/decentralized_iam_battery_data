package core

import (
	core "blockchain/internal/core/types"
	"fmt"
	"log/slog"
	"time"
)

type Blockchain []Block

// ValidateBlockchain Validate a chain of blocks
func ValidateBlockchain(chain *Blockchain) bool {
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
func GetBlock(chain *Blockchain, id int) Block {
	for _, block := range *chain {
		if block.Index == id {
			return block
		}
	}
	return Block{}
}

// GetLastBlock Returns the last/newest block from the Blockchain
func GetLastBlock(chain *Blockchain) Block {
	return (*chain)[len(*chain)-1]
}

// PrintChain Prints the complete Blockchain
func PrintChain(chain *Blockchain) {
	for i, block := range *chain {
		fmt.Printf("Block %d: %+v\n", i, block)
	}
}

// CreateChain Creates a new Chain with the GenerateGenesisBlock method
func CreateChain() *Blockchain {
	var chain *Blockchain
	*chain = append(*chain, GenerateGenesisBlock())
	return chain
}

// AppendBlock Appends a Block to a Chain
func AppendBlock(chain *Blockchain, block Block) {
	*chain = append(*chain, block)
}

// VerifyDID Verify that the blockchain contains the DID and the revocation flag is false
func (chain *Blockchain) VerifyDID(did string) string {
	var block Block
	for i := len(*chain) - 1; i >= 0; i-- {
		block = GetBlock(chain, i)
		for _, tx := range block.Transactions {
			if diddoc, err := core.UnmarshalDid(tx); err == nil {
				if diddoc.ID == did && !diddoc.Revoked {
					return "revoked"
				} else {
					return "valid"
				}
			}
		}
	}
	return "absent"
}

// VerifyVCRecord Verify that the blockchain contains a VCRecord which is still valid
func (chain *Blockchain) VerifyVCRecord(vcRecord core.VCRecord) string {
	if vcRecord.ExpirationDate != nil && vcRecord.Timestamp.Before(*vcRecord.ExpirationDate) {
		var block Block
		for i := len(*chain) - 1; i >= 0; i-- {
			block = GetBlock(chain, i)
			for _, tx := range block.Transactions {
				if onChainRecord, err := core.UnmarshalVCRecord(tx); err == nil {
					if onChainRecord.ID == vcRecord.ID {
						if onChainRecord.VcHash != vcRecord.VcHash {
							return "tampered"
						} else if onChainRecord.ExpirationDate.Before(time.Now()) {
							return "expired"
						} else {
							return "valid"
						}
					}
				}
			}
		}
	}
	return "absent"
}
