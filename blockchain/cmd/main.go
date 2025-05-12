package main

import (
	"blockchain/internal/api/cli"
	"blockchain/internal/core"
)

func main() {
	var chain core.Blockchain
	mycli := cli.InitCli()
	mycli.Parse(&chain)
}
