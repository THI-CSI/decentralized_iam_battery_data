package cli

import (
	"blockchain/internal/api/web"
	"blockchain/internal/core"
	"blockchain/internal/storage"
	"flag"
	"fmt"
)

type Cli struct {
	printChain *bool
	validate   *bool
	web        *bool
	save       *string
	load       *string
	demo       *bool
}

// InitCli initializes CLI flags and returns a Cli instance
func InitCli() *Cli {
	cli := &Cli{
		printChain: flag.Bool("print-chain", false, "Print the entire blockchain"),
		validate:   flag.Bool("validate", false, "Validate the blockchain"),
		web:        flag.Bool("web", false, "Start the web server"),
		save:       flag.String("save", "", "Save the blockchain to disk"),
		load:       flag.String("load", "", "Load the blockchain from disk"),
		demo:       flag.Bool("demo", false, "Generate a demo blockchain and validate it"),
	}
	return cli
}

// Parse parses the CLI arguments and runs the corresponding command
func (cli *Cli) Parse(chain *[]core.Block) {
	flag.Parse()

	if len(*cli.load) > 0 {
		filename := *cli.load
		err := storage.Load(filename, chain)
		if err != nil {
			fmt.Printf("error: %v\n", err)
			return
		}
		fmt.Printf("Loaded blockchain from '%v'\n", filename)
	}

	if *cli.demo {
		fmt.Println("Creates a demo blockchain...")

		// Generate genesis block and 3 additional blocks with no transactions
		*chain = append(*chain, core.GenerateGenesisBlock())
		for i := 0; i < 3; i++ {
			*chain = append(*chain, core.GenerateBlock((*chain)[len(*chain)-1], nil))
		}
	}

	if *cli.printChain {
		fmt.Println("Printing the entire blockchain...")

		for i, block := range *chain {
			fmt.Printf("Block %d: %+v\n", i, block)
		}
	}

	if *cli.validate {
		fmt.Println("Validating the blockchain...")

		isValid := core.ValidateBlockchain(*chain)
		if isValid {
			fmt.Printf("The blockchain is valid!\n")
		}else {
			fmt.Printf("The blockchain is not valid!\n")
		}
	}

	if *cli.web {
		fmt.Println("Starting the Web API...")
		web.CreateServer()
	}


	if len(*cli.save) > 0 {
		filename := *cli.save
		err := storage.Save(filename, *chain)
		if err != nil {
			fmt.Printf("error: %v\n", err)
			return
		}
		fmt.Printf("Saved the blockchain to '%v'\n", filename)
	}

}
