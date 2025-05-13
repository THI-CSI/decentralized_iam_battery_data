package cli

import (
	"blockchain/internal/api/web"
	"blockchain/internal/core"
	"blockchain/internal/storage"
	"encoding/json"
	"flag"
	"fmt"
	"os"
)

type Cli struct {
	printChain *bool
	validate   *bool
	web        *bool
	save       *bool
	load       *bool
	file       *string
	demo       *bool
}

// InitCli initializes CLI flags and returns a Cli instance
func InitCli() *Cli {
	cli := &Cli{
		printChain: flag.Bool("print-chain", false, "Print the entire blockchain"),
		validate:   flag.Bool("validate", false, "Validate the blockchain"),
		web:        flag.Bool("web", false, "Start the web server"),
		save:       flag.Bool("save", false, "Save the blockchain to a file"),
		load:       flag.Bool("load", false, "Load the blockchain from a file"),
		file:       flag.String("file", "", "Specify the file"),
		demo:       flag.Bool("demo", false, "Generate a demo blockchain and validate it"),
	}
	return cli
}

// Parse parses the CLI arguments and runs the corresponding command
func (cli *Cli) Parse(chain *core.Blockchain) {
	filename := "blockchain.json"
	flag.Parse()

	if len(*cli.file) > 0 {
		filename = *cli.file
	}

	if *cli.load {
		err := storage.Load(filename, chain)
		if err != nil {
			fmt.Printf("error: %v\n", err)
			return
		}
		if !chain.ValidateBlockchain() {
			fmt.Println("error: The loaded blockchain is not valid.")
			os.Exit(1)
		}
		fmt.Printf("Loaded blockchain from '%v'\n", filename)
	}

	if *cli.demo {
		fmt.Println("Creates a demo blockchain...")

		data, err := os.ReadFile("./docs/VC-DID-examples/bms.json")
		if err != nil {
			fmt.Println("Error: Could not read file:", err)
			return
		}
		var rawbms json.RawMessage = data

		data, err = os.ReadFile("./docs/VC-DID-examples/oem.json")
		if err != nil {
			fmt.Println("Error: Could not read file:", err)
			return
		}
		var rawoem json.RawMessage = data

		data, err = os.ReadFile("./docs/VC-DID-examples/cloud.json")
		if err != nil {
			fmt.Println("Error: Could not read file:", err)
			return
		}
		var rawcloud json.RawMessage = data

		data, err = os.ReadFile("./docs/VC-DID-examples/vcRecord.json")
		if err != nil {
			fmt.Println("Error: Could not read file:", err)
			return
		}
		var vcRecord json.RawMessage = data

		//Generate the genesis block and 3 additional blocks with above DIDs as Transactions
		chain = core.CreateChain()
		(*chain).AppendTransaction(rawoem)
		(*chain).AppendTransaction(rawbms)
		(*chain).AppendTransaction(rawcloud)
		(*chain).AppendBlock(core.GenerateBlock((*chain).GetLastBlock()))
		(*chain).AppendTransaction(rawcloud)
		(*chain).AppendTransaction(rawoem)
		(*chain).AppendBlock(core.GenerateBlock((*chain).GetLastBlock()))
		(*chain).AppendTransaction(vcRecord)
		(*chain).AppendBlock(core.GenerateBlock((*chain).GetLastBlock()))
		(*chain).AppendTransaction(vcRecord)
		(*chain).AppendBlock(core.GenerateBlock((*chain).GetLastBlock()))
		(*chain).AppendTransaction(rawcloud)
		(*chain).AppendTransaction(rawbms)
		(*chain).AppendTransaction(rawoem)
		(*chain).AppendBlock(core.GenerateBlock((*chain).GetLastBlock()))
	}

	if *cli.printChain {
		fmt.Println("Printing the entire blockchain...")
		core.PrintChain(chain)
	}

	if *cli.validate {
		fmt.Println("Validating the blockchain...")

		isValid := (*chain).ValidateBlockchain()
		if isValid {
			fmt.Printf("The blockchain is valid!\n")
		} else {
			fmt.Printf("The blockchain is not valid!\n")
		}
	}

	if *cli.web {
		fmt.Println("Starting the Web API...")
		web.CreateServer()
	}

	if *cli.save {
		err := storage.Save(filename, *chain)
		if err != nil {
			fmt.Printf("error: %v\n", err)
			return
		}
		fmt.Printf("Saved the blockchain to '%v'\n", filename)
	}

}
