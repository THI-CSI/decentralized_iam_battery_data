import argparse
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


def signal_handler(_sig, _frame):
    print("received interrupt signal")
    sys.exit(1)


def check_return_code(code):
    if code != 0:
        print(f"Command failed with code {code}", file=sys.stderr)
        sys.exit(code)


def docker_compose(command: str, unknown_args):
    process = subprocess.run(["docker", "compose", command, *unknown_args])
    check_return_code(process.returncode)

def main():
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(dest="command")
    subparser.required = True

    for c in DOCKER_COMMANDS:
        subparser.add_parser(c)

    args, unknown_args = parser.parse_known_args()

    signal.signal(signal.SIGINT, signal_handler)

    docker_compose(args.command, unknown_args)


if __name__ == "__main__":
    main()