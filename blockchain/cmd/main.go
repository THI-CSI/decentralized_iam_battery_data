package main

import (
	"blockchain/internal/api/cli"
	"blockchain/internal/core"
)

func main() {
	var chain core.Blockchain
	cli := cli.InitCli()
	cli.Parse(&chain)
}
