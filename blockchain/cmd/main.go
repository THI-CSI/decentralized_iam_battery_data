package main

import (
	"blockchain/internal/api/cli"
	"blockchain/internal/core"
	"fmt"
	"os"
)

// main is the entry point of the application, initializing the CLI and processing the blockchain.
func main() {
	var chain core.Blockchain

	mycli := cli.InitCli()
	if err := mycli.Parse(&chain); err != nil {
		fmt.Fprintf(os.Stderr, "error: %v\n", err)
		os.Exit(1)
	}
}
