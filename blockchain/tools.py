#!/usr/bin/env python3

import argparse
import os
import sys
import subprocess
import signal

DOCKER_COMMANDS = [
    "up",
    "down",
    "pull",
    "push",
    "build",
    "logs",
    "run",
    "exec",
    "ls",
]

DELETE_FOLDER = [
    "bin",
    ".venv",
    "node_modules",
    "./docs/schema",
    "./docs/sourcecode",
    "./docs/openapi.html",
    "package.json",
    "package-lock.json",
    "schema_doc.css",
    "schema_doc.min.js",
    "package.json",
    "./internal/api/web/openapi.bundled.yamlopenapitools.json",
]

SCHEMA_DIR = "./internal/jsonschema"
QUICKTYPE = "./node_modules/.bin/quicktype"
REDOCLY = "./node_modules/.bin/redocly"
TYPEDOC = "./node_modules/.bin/typedoc"
SCHEMA_RESOLVER = "./node_modules/.bin/json-schema-resolver"
DOCS = "./docs"
CORETYPES = "./internal/core/types"
APITYPES = "./internal/api/types"


def signal_handler(_sig, _frame):
    print("received interrupt signal")
    sys.exit(1)


def check_return_code(code):
    if code != 0:
        print(f"Command failed with code {code}", file=sys.stderr)
        sys.exit(code)


def blockchain_cmd(unknown_args):
    process = subprocess.run(["go", "run", "./cmd/main.go", *unknown_args])
    check_return_code(process.returncode)


def docker_compose_dev(command: str, unknown_args):
    process = subprocess.run(
        ["docker", "compose", "-f", "docker-compose-dev.yml", command, *unknown_args]
    )
    check_return_code(process.returncode)


def run_command(command: list[str]):
    process = subprocess.run(command)
    check_return_code(process.returncode)


def main():
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(dest="command")
    subparser.required = True

    # commands for docker
    docker_parser = subparser.add_parser(
        "dev",
        help='Docker related commands, executes docker-compose-dev.yml, for more info "docker -h" ',
    )
    docker_subparser = docker_parser.add_subparsers(dest="docker_command")
    docker_subparser.required = True

    for c in DOCKER_COMMANDS:
        docker_subparser.add_parser(c, help=f"docker {c} command")

    # special subcommands
    blockchain_parser = subparser.add_parser(
        "run", help="run the blockchain application"
    )
    blockchain_subparser = blockchain_parser.add_subparsers(dest="blockchain_parser")
    blockchain_subparser.add_parser("h")
    blockchain_subparser.add_parser("help")

    subparser.add_parser("install", help="install all dependencies")
    subparser.add_parser("format", help="format the sourcecode")
    subparser.add_parser("build", help="build the blockchain application")
    subparser.add_parser("clean", help="clean build artifacts and generated docs")
    subparser.add_parser("test", help="test the blockchain application")
    subparser.add_parser("generate", help="generate go types from jsonschemas")

    docs_parser = subparser.add_parser(
        "docs", help='build documentation, for more info "docs -h"'
    )
    docs_parser.add_argument(
        "--type",
        choices=["go", "swagger", "did-vc", "all"],
        default="all",
        help="Type of docs to generate (default: all)",
    )

    args, unknown_args = parser.parse_known_args()

    signal.signal(signal.SIGINT, signal_handler)

    if args.command == "run":
        if args.blockchain_parser == "h" or args.blockchain_parser == "help":
            blockchain_cmd(["-h"])
        else:
            if "-web" in unknown_args:
                if os.path.exists(f"{DOCS}/swagger"):
                    blockchain_cmd(unknown_args)
                else:
                    print(
                        "You need to generate the swagger documentation before you can start the webserver"
                    )
            else:
                blockchain_cmd(unknown_args)

    elif args.command == "install":
        run_command(["bash", "./scripts/install-dependencies.sh"])

    elif args.command == "format":
        run_command(["gofmt", "-l", "-s", "-w", "."])
        print("Successfully formatted sourcecode")

    elif args.command == "build":
        run_command(["go", "build", "-o", "bin/blockchain", "./cmd/main.go"])
        print("Successfully built, binary is in ./bin/blockchain")

    elif args.command == "docs":
        run_command(["mkdir", "-p", DOCS])
        run_command(
            [
                REDOCLY,
                "build-docs",
                "./internal/api/web/openapi.yaml",
                "--output",
                f"{DOCS}/openapi.html",
            ]
        )
        run_command(["gomarkdoc", "./...", "-o", DOCS + "/sourcecode/go/md/go.md"])
        run_command([
            "golds",
            "-nouses",
            "-only-list-exporteds",
            "-gen",
            f"-dir={DOCS}/sourcecode/go/html",
            "./..."
        ])
        run_command([TYPEDOC, "--options", "typedoc.md.json"])
        run_command([TYPEDOC, "--options", "typedoc.html.json"])
        run_command(["bash", "./scripts/generate-did-vc-docs-md.sh"])
        run_command(["bash", "./scripts/generate-did-vc-docs-html.sh"])

    elif args.command == "clean":
        for folder in DELETE_FOLDER:
            print(f"delete: {folder}")
            if os.path.exists(folder):
                if os.path.isdir(folder):
                    run_command(["rm", "-rf", folder])
                else:
                    run_command(["rm", "-f", folder])

    elif args.command == "test":
        run_command(["go", "test", "-v", "./internal/core"])

    elif args.command == "generate":
        if os.path.exists("./node_modules"):
            run_command(["bash", "./scripts/generate-api-go.sh"])
            run_command(
                [
                    QUICKTYPE,
                    "-s",
                    "schema",
                    SCHEMA_DIR + "/did.schema.json",
                    "--top-level",
                    "DID",
                    "--package",
                    "core",
                    "-o",
                    CORETYPES + "/did.types.go",
                ]
            )
            run_command(
                [
                    QUICKTYPE,
                    "-s",
                    "schema",
                    SCHEMA_DIR + "/vc.record.schema.json",
                    "--top-level",
                    "VCRecord",
                    "--package",
                    "core",
                    "-o",
                    CORETYPES + "/vc.record.types.go",
                ]
            )
        else:
            print(
                'Install dependencies, before generating types: "python3 tools.py install"'
            )

    elif args.command == "dev":
        if os.path.exists("./blockchain.json/"):
            run_command(["rm", "-rf", "./blockchain.json/"])
        if not os.path.exists("./blockchain.json"):
            blockchain_cmd(["-genesis"])
        docker_compose_dev(args.docker_command, unknown_args)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
