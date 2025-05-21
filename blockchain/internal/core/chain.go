package core

import (
	core "blockchain/internal/core/types"
	"blockchain/internal/storage"
	"encoding/json"
	"errors"
	"fmt"
	"log/slog"
	"os"
	"strings"
	"time"
)

type Blockchain []Block

// ValidateBlockchain Validate a chain of blocks
func (chain *Blockchain) ValidateBlockchain() bool {
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
func (chain *Blockchain) GetBlock(id int) *Block {
	for _, block := range *chain {
		if block.Index == id {
			return &block
		}
	}
	return nil
}

// GetLastBlock Returns the last/newest block from the Blockchain
func (chain *Blockchain) GetLastBlock() *Block {
	return &(*chain)[len(*chain)-1]
}

// Print Prints the complete Blockchain
func (chain *Blockchain) Print() {
	for i, block := range *chain {
		fmt.Printf("Block %d: %+v\n", i, block)
	}
}

// CreateChain Creates a new Chain with the GenerateGenesisBlock method
func CreateChain() *Blockchain {
	var chain Blockchain
	chain = append(chain, GenerateGenesisBlock())
	return &chain
}

// AppendBlock Appends a Block to a Chain
func (chain *Blockchain) AppendBlock(block Block) {
	if block.Transactions != nil {
		*chain = append(*chain, block)
	}
}

// VerifyDID Verify that the blockchain contains the DID and the revocation flag is false
func (chain *Blockchain) VerifyDID(did string) DidState {
	for _, tx := range PendingTransactions {
		didPending, _ := core.UnmarshalDid(tx)
		if didPending.ID == did {
			return DidPending
		}
	}

	var block *Block
	for i := len(*chain) - 1; i >= 0; i-- {
		block = chain.GetBlock(i)
		if block == nil {
			return DidAbsent
		}
		for _, tx := range block.Transactions {
			if diddoc, _ := core.UnmarshalDid(tx); strings.HasPrefix(diddoc.ID, "did:") {
				if diddoc.ID == did {
					if diddoc.Revoked {
						return DidRevoked
					} else {
						return DidValid
					}
				}
			}
		}
	}
	return DidAbsent
}

// VerifyVCRecord Verify that the blockchain contains a VCRecord which is still valid
func (chain *Blockchain) VerifyVCRecord(uri string, vcHash string) VCState {
	for _, tx := range PendingTransactions {
		vcPending, _ := core.UnmarshalVCRecord(tx)
		if vcPending.ID == uri {
			return VCPending
		}
	}
	var block *Block
	for i := len(*chain) - 1; i >= 0; i-- {
		block = chain.GetBlock(i)
		if block == nil {
			return VCAbsent
		}
		for _, tx := range block.Transactions {
			if onChainRecord, _ := core.UnmarshalVCRecord(tx); strings.HasPrefix(onChainRecord.ID, "urn:") {
				if onChainRecord.ID == uri || onChainRecord.VcHash == vcHash {
					if onChainRecord.VcHash != vcHash || onChainRecord.ID != uri {
						return VCTampered
					} else if onChainRecord.ExpirationDate.Before(time.Now()) {
						return VCExpired
					} else {
						return VCValid
					}
				}
			}
		}
	}
	return VCAbsent
}

func (chain *Blockchain) FindDID(did string) (*core.Did, error) {
	var didResponse core.Did
	for i := len(*chain) - 1; i >= 0; i-- {
		block := chain.GetBlock(i)
		for _, transaction := range block.Transactions {
			err := json.Unmarshal(transaction, &didResponse)
			if err != nil {
				// TODO Check if the way of unmarshal only DIDs works as expected
				continue
			}
			if didResponse.ID == did {
				return &didResponse, nil
			}
		}
	}
	return nil, errors.New("did not found")
}

func (chain *Blockchain) FindVCRecord(urn string) (*core.VCRecord, error) {
	var vcRecordResponse core.VCRecord
	for i := len(*chain) - 1; i >= 0; i-- {
		block := chain.GetBlock(i)
		for _, transaction := range block.Transactions {
			err := json.Unmarshal(transaction, &vcRecordResponse)
			if err != nil {
				// TODO Check if the way of unmarshal only VCs works as expected
				continue
			}
			if vcRecordResponse.ID == urn {
				return &vcRecordResponse, nil
			}
		}
	}
	return nil, errors.New("VC record not found")
}

// Consensus Basic consensus mechanism, which checks, if enough transactions are pending
func (chain *Blockchain) Consensus() bool {
	return len(PendingTransactions) >= TransactionThreshold
}

// Automate Automates the block generation and will check every second if the consensus is given
func (chain *Blockchain) Automate(filename string) {
	for {
		// Checks every second if the TransactionThreshold has been reached
		time.Sleep(time.Second)
		if chain.Consensus() {
			chain.AppendBlock(GenerateBlock(chain.GetLastBlock()))
			fmt.Printf("[+] Generated new block!\n%v\n", chain.GetLastBlock())
			if err := storage.Save(filename, *chain); err != nil {
				fmt.Fprintf(os.Stderr, "error: %v\n", err)
				os.Exit(1)
			}
			fmt.Printf("[i] Saved the new block to the '%v' file!\n", filename)
		}
		//fmt.Printf("[i] Pending Transactions: %v\n", len(PendingTransactions))
	}
}
