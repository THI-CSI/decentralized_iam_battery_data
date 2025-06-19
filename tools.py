import argparse
import sys
import subprocess
import signal
import os

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

# TODO Clean Key file directories and blockchain.json

def signal_handler(_sig, _frame):
    print("received interrupt signal")
    sys.exit(1)


def check_return_code(code):
    if code != 0:
        print(f"Command failed with code {code}", file=sys.stderr)
        sys.exit(code)

def check_return_code(code):
    if code != 0:
        print(f"Command failed with code {code}", file=sys.stderr)
        sys.exit(code)


def blockchain_cmd(unknown_args):
    cwd = os.getcwd()
    os.chdir('blockchain')
    process = subprocess.run(["go", "run", "./cmd/main.go", *unknown_args])
    os.chdir(cwd)
    check_return_code(process.returncode)


def docker_compose(command: str, unknown_args):
    process = subprocess.run(["docker", "compose", command, *unknown_args])
    check_return_code(process.returncode)

def main():
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(dest="command")
    subparser.required = True

    if not os.path.exists("./blockchain/blockchain.json"):
        blockchain_cmd(["-genesis"])

    for c in DOCKER_COMMANDS:
        subparser.add_parser(c)

    args, unknown_args = parser.parse_known_args()

    signal.signal(signal.SIGINT, signal_handler)

    docker_compose(args.command, unknown_args)
    ## Service-client:
    ### Initialize Service Client
    # python3 service_access.py --initialize
    ### Start the Sign Service:
    # python3 service_access.py --sign-service

    ## Start BMS:
    # python3 main.py


if __name__ == "__main__":
    main()