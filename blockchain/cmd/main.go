package main

import (
	"blockchain/internal/core"
	"fmt"
)

func main() {
	var chain []core.Block

	// Generate one Genesis block and three blocks without transactions
	chain = append(chain, core.GenerateGenesisBlock())
	for i := 0; i <= 3; i++ {
		chain = append(chain, core.GenerateBlock(chain[len(chain)-1], nil))
	}

	// Print the blockchain example to the console
	for i := range chain {
		fmt.Println(chain[i])
	}

	// Outputs whether the blockchain is valid
	fmt.Printf("Is the blockchain valid: %v\n", core.ValidateBlockchain(chain))
}
