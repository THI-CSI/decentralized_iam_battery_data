package cli

import (
	"blockchain/internal/api/web"
	"blockchain/internal/core"
	"blockchain/internal/storage"
	"encoding/json"
	"flag"
	"fmt"
	"log"
	"os"
	"os/signal"
	"time"
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

	interrupt := make(chan os.Signal, 1)
	signal.Notify(interrupt, os.Interrupt)

	if *cli.demo && !*cli.web {
		return generateDemoBlockchain(chain, filename)
	}

	if len(*cli.file) > 0 {
		filename = *cli.file
	}

	if *cli.genesis {
		return generateGenesisBlockchain(chain, filename)
	}

	if err = storage.Load(filename, chain); err != nil {
		return fmt.Errorf("%v\nYou can use the argument '-genesis' to create a new blockchain.", err)
	}

	if !chain.ValidateBlockchain() {
		return fmt.Errorf("the loaded blockchain is not valid")
	}

	if *cli.web {
		startWebApi(chain, filename, *cli.demo)
	}

	if *cli.printChain {
		chain.Print()
	}

	if err = storage.Save(filename, *chain); err != nil {
		return err
	}

	select {
	case <-interrupt:
		log.Println("Interrupt received! Stopping blockchain...")
		if err = storage.Save(filename, *chain); err != nil {
			return err
		}
	}

	return nil
}

// generateDemoBlockchain Extracts the demo blockchain generation from the CLI
func generateDemoBlockchain(chain *core.Blockchain, filename string) error {
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

	chain.Print()

	err = storage.Save(filename, *chain)
	if err != nil {
		return err
	}
	fmt.Printf("Generated demo blockchain and saved it to '%v'!\n", filename)

	return nil
}

// generateGenesisBlockchain Extracts the initial creation of the blockchain with the genesis from the CLI
func generateGenesisBlockchain(chain *core.Blockchain, filename string) error {
	chain = core.CreateChain()
	err := storage.Save(filename, *chain)
	if err != nil {
		return err
	}
	fmt.Printf("Generated genesis block and saved the blockchain to '%v'!\n", filename)
	return nil
}

// startWebApi Extracts the web api and blockchain automation from the CLI
func startWebApi(chain *core.Blockchain, filename string, createDemoTransactions bool) {
	fmt.Println("Starting the Blockchain...")
	go chain.Automate(filename)

	if createDemoTransactions {
		go func() {
			data, _ := os.ReadFile("./docs/VC-DID-examples/oem.json")
			var rawoem json.RawMessage = data

			for {
				time.Sleep(3 * time.Second)
				chain.AppendTransaction(rawoem)
				fmt.Println("[+] Added Transaction")
			}
		}()
	}

	fmt.Println("Starting the Web API...")
	web.CreateServer()
}
