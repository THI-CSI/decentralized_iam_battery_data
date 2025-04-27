package main

import (
	"blockchain/internal/api/cli"
	"blockchain/internal/core"
)

func main() {
	var chain []core.Block
	cli := cli.InitCli()
	cli.Parse(&chain)
}
