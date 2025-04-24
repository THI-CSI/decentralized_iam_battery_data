package main

import "blockchain/internal/api/cli"

func main() {
	cli := cli.InitCli()
	cli.Parse()
}
