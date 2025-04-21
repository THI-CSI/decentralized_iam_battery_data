package main

import (
	"blockchain/internal/core"
	"fmt"
)

func main() {
	var chain []core.Block

	// Generate one Genisis block and five blocks without transactions
	chain = append(chain, core.GenerateGenisisBlock())
	for i := 0; i <= 5; i++ {
		chain = append(chain, core.GenerateBlock(chain[len(chain)-1], nil))
	}

	// Print the blockchain example to the console
	for i := range chain {
		fmt.Println(chain[i])
	}
}
