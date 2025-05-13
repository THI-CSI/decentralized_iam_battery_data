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
	web        *bool
	genesis    *bool
	file       *string
	demo       *bool
}

// InitCli initializes CLI flags and returns a Cli instance
func InitCli() *Cli {
	cli := &Cli{
		printChain: flag.Bool("print-chain", false, "Print the entire blockchain"),
		web:        flag.Bool("web", false, "Start the web server"),
		genesis:    flag.Bool("genesis", false, "Creates a new blockchain and saves it to a file"),
		file:       flag.String("file", "", "Specify the file"),
		demo:       flag.Bool("demo", false, "Generate a demo blockchain and validate it"),
	}
	return cli
}

// Parse parses the CLI arguments and runs the corresponding command
func (cli *Cli) Parse(chain *core.Blockchain) error {
	filename := "blockchain.json"
	var err error
	flag.Parse()

	if *cli.demo {
		filename = "blockchain-demo.json"
		fmt.Println("Creates a demo blockchain...")

		data, err := os.ReadFile("./docs/VC-DID-examples/bms.json")
		if err != nil {
			return fmt.Errorf("could not read file: %v", err)
		}
		var rawbms json.RawMessage = data

		data, err = os.ReadFile("./docs/VC-DID-examples/oem.json")
		if err != nil {
			return fmt.Errorf("could not read file: %v", err)
		}
		var rawoem json.RawMessage = data

		data, err = os.ReadFile("./docs/VC-DID-examples/cloud.json")
		if err != nil {
			return fmt.Errorf("could not read file: %v", err)
		}
		var rawcloud json.RawMessage = data

		data, err = os.ReadFile("./docs/VC-DID-examples/vcRecord.json")
		if err != nil {
			return fmt.Errorf("could not read file: %v", err)
		}
		var vcRecord json.RawMessage = data

		//Generate the genesis block and 3 additional blocks with above DIDs as Transactions
		chain = core.CreateChain()
		chain.AppendTransaction(rawoem)
		chain.AppendTransaction(rawbms)
		chain.AppendTransaction(rawcloud)
		chain.AppendBlock(core.GenerateBlock(chain.GetLastBlock()))
		chain.AppendTransaction(rawcloud)
		chain.AppendTransaction(rawoem)
		chain.AppendBlock(core.GenerateBlock(chain.GetLastBlock()))
		chain.AppendTransaction(vcRecord)
		chain.AppendBlock(core.GenerateBlock(chain.GetLastBlock()))
		chain.AppendTransaction(rawcloud)
		chain.AppendTransaction(rawoem)
		chain.AppendBlock(core.GenerateBlock(chain.GetLastBlock()))

		core.PrintChain(chain)

		err = storage.Save(filename, *chain)
		if err != nil {
			return err
		}
		fmt.Printf("Generated demo blockchain and saved it to '%v'!\n", filename)

		return nil
	}

	if len(*cli.file) > 0 {
		filename = *cli.file
	}

	if *cli.genesis {
		chain = core.CreateChain()
		err = storage.Save(filename, *chain)
		if err != nil {
			return err
		}
		fmt.Printf("Generated genesis block and saved the blockchain to '%v'!\n", filename)
		return nil
	}

	err = storage.Load(filename, chain)
	if err != nil {
		return fmt.Errorf("%v\nYou can use the argument '-genesis' to create a new blockchain.", err)
	}

	if !chain.ValidateBlockchain() {
		return fmt.Errorf("the loaded blockchain is not valid")
	}

	if *cli.printChain {
		core.PrintChain(chain)
	}

	if *cli.web {
		fmt.Println("Starting the Web API...")
		web.CreateServer()
	}

	err = storage.Save(filename, *chain)
	if err != nil {
		return err
	}

	return nil
}
