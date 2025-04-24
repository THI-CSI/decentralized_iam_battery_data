package cli

import (
	"blockchain/internal/api/web"
	"blockchain/internal/core"
	"flag"
	"fmt"
)

type Cli struct {
	printChain *bool
	printBlock *bool
	validate   *bool
	web        *bool
	save       *bool
	load       *bool
	test       *bool
}

// InitCli initializes CLI flags and returns a Cli instance
func InitCli() *Cli {
	cli := &Cli{
		printChain: flag.Bool("print-chain", false, "Print the entire blockchain"),
		printBlock: flag.Bool("print-block", false, "Print a specific block"),
		validate:   flag.Bool("validate", false, "Validate the blockchain"),
		web:        flag.Bool("web", false, "Start the web server"),
		save:       flag.Bool("save", false, "Save the blockchain to disk"),
		load:       flag.Bool("load", false, "Load the blockchain from disk"),
		test:       flag.Bool("test", false, "Generate a test blockchain and validate it"),
	}
	return cli
}

// Parse parses the CLI arguments and runs the corresponding command
func (cli *Cli) Parse() {
	flag.Parse()

	switch {
	case *cli.printChain:
		fmt.Println("Printing the entire blockchain...")

	case *cli.printBlock:
		fmt.Println("Printing a specific block...")

	case *cli.validate:
		fmt.Println("Validating the blockchain...")

	case *cli.web:
		web.CreateServer()

	case *cli.save:
		fmt.Println("Saving the blockchain...")

	case *cli.load:
		fmt.Println("Loading the blockchain...")

	case *cli.test:
		fmt.Println("Running blockchain test...")
		var chain []core.Block

		// Generate genesis block and 3 additional blocks with no transactions
		chain = append(chain, core.GenerateGenesisBlock())
		for i := 0; i < 3; i++ {
			chain = append(chain, core.GenerateBlock(chain[len(chain)-1], nil))
		}

		// Print all blocks
		for i, block := range chain {
			fmt.Printf("Block %d: %+v\n", i, block)
		}

		// Validate and print result
		fmt.Printf("Is the blockchain valid? %v\n", core.ValidateBlockchain(chain))

	default:
		fmt.Println("No valid flag provided. Use -h for help.")
	}
}
