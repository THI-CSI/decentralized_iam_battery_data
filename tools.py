import argparse
import random
import shutil
import sys
import subprocess
import signal
import os
import time

import requests

DEBUG = os.getenv("DEBUG", "false") == "true"
BMS_DATA_GENERATION_INTERVAL = os.getenv("BMS_DATA_GENERATION_INTERVAL", "1")
NEW_DATA_GEN = os.getenv("NEW_DATA_GEN", "false") == "true"


CLI_COMMANDS = [
    "up",
    "down",
    "clean",
    "tmux"
]

CLEANUP_FILES = [
    "./blockchain/blockchain.json",
    "./bms/mock/utils/keys/",
    "./bms/mock/.venv/",
    "./cloud/.env",
    "./cloud/docs/example/keys/",
    "./client/keys/",
    "./client/.venv/"
]

REQUIREMENTS = [
    "docker",
    "tmux"
]


class Log:
    class color:
        HEADER = '\033[95m'
        DEBUG = '\33[90m'
        INFO = '\033[96m'
        SUCCESS = '\033[92m'
        WARNING = '\033[93m'
        ERROR = '\033[91m'
        RESET = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'

    def error(self, msg):
        symbol = f"{self.color.BOLD}[{self.color.ERROR}-{self.color.RESET + self.color.BOLD}]{self.color.RESET}"
        print(f"{symbol} {msg}")

    def warning(self, msg):
        symbol = f"{self.color.BOLD}[{self.color.WARNING}!{self.color.RESET + self.color.BOLD}]{self.color.RESET}"
        print(f"{symbol} {msg}")

    def success(self, msg):
        symbol = f"{self.color.BOLD}[{self.color.SUCCESS}+{self.color.RESET + self.color.BOLD}]{self.color.RESET}"
        print(f"{symbol} {msg}")

    def info(self, msg):
        symbol = f"{self.color.BOLD}[{self.color.INFO}i{self.color.RESET + self.color.BOLD}]{self.color.RESET}"
        print(f"{symbol} {msg}")

    def debug(self, msg):
        symbol = f"{self.color.BOLD + self.color.DEBUG}[#]{self.color.RESET}"
        print(f"{symbol} {msg}")

log = Log()


class Tmux:
    def __init__(self, session_name: str, user_pane_id: str = "pane0"):
        self.tmux_session = session_name
        self.pane_map = {}
        self._create_tmux_session(user_pane_id=user_pane_id)

    def _exec_tmux_command(self, cmd: list) -> str:
        full_cmd = ["tmux"] + cmd
        try:
            result = subprocess.run(
                full_cmd,
                capture_output=True,
                check=True,
                text=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            raise
        except Exception as e:
            raise


    def _create_tmux_session(self, user_pane_id: str = "pane0"):
        try:
            self._exec_tmux_command(["has-session", "-t", self.tmux_session])
        except:
            self._exec_tmux_command(['new-session', '-d', '-s', self.tmux_session])

            initial_pane_id = self._exec_tmux_command(['list-panes', '-t', f"{self.tmux_session}:0", "-F", "#{pane_id}"])
            self.pane_map[user_pane_id] = initial_pane_id


    def attach_to_tmux_session(self):
        self._exec_tmux_command(['attach-session', '-t', self.tmux_session])

    def kill_tmux_session(self):
        for user_pane_id in self.pane_map:
            try:
                self.kill_pane(user_pane_id)
            except:
                pass
        try:
            self._exec_tmux_command(['kill-session', '-t', self.tmux_session])
        except:
            pass


    def get_tmux_pane_id(self, user_pane_id: str) -> str:
        if user_pane_id not in self.pane_map:
            raise ValueError(f"Pane with user ID '{user_pane_id}' not found.")
        return self.pane_map[user_pane_id]

    def split_pane(self, user_pane_id: str, direction: str = "right") -> str:
        if user_pane_id in self.pane_map:
            raise ValueError(f"Pane with user ID '{user_pane_id}' already exists.")

        if direction not in ["right", "bottom"]:
            raise ValueError("Invalid split direction. Must be 'right' or 'bottom'.")

        target_window = f"{self.tmux_session}:0"

        cmd_args = ["split-window", "-t", target_window, "-P", "-F", "#{pane_id}"]
        if direction == "right":
            cmd_args.append("-h") # Horizontal split (right)
        else:
            cmd_args.append("-v") # Vertical split (bottom)

        tmux_pane_id = self._exec_tmux_command(cmd_args)
        self.pane_map[user_pane_id] = tmux_pane_id
        return tmux_pane_id

    def send_command(self, user_pane_id: str, command: str):
        tmux_pane_id = self.get_tmux_pane_id(user_pane_id)
        # Use C-m to simulate pressing Enter after the command
        self._exec_tmux_command(["send-keys", "-t", tmux_pane_id, command, "C-m"])

    def switch_pane(self, user_pane_id: str):
        tmux_pane_id = self.get_tmux_pane_id(user_pane_id)
        self._exec_tmux_command(["select-pane", "-t", tmux_pane_id])

    def kill_pane(self, user_pane_id: str):
        tmux_pane_id = self.get_tmux_pane_id(user_pane_id)
        self._exec_tmux_command(["kill-pane", "-t", tmux_pane_id])
        del self.pane_map[user_pane_id]


def is_service_running(port):
    try:
        response = requests.get(f"http://localhost:{port}/")
    except requests.exceptions.ConnectionError:
        return False
    return response.status_code == 200


tmux = None

def sleep_countdown(seconds):
    spinner = "|\\-/"
    for i in range(seconds*4, 0, -1):
        print(f'\r[{spinner[i%len(spinner)]}] Waiting {i//4} Seconds...', end=' ')
        time.sleep(0.25)
    print("\r", end="")

def service_monitor_on_steroids():
    log.info("Starting Tmux Utility On Steroids")
    global tmux
    tmux = Tmux(f"diam_bat_tmux_{random.randint(100,999)}", user_pane_id="blockchain_cloud")
    # Create Panes
    tmux.split_pane("bms_1", "right")
    tmux.split_pane("bms_2", "bottom")
    tmux.split_pane("console", "bottom")
    tmux.switch_pane("blockchain_cloud")
    tmux.split_pane("oem_service", "bottom")
    tmux.switch_pane("console")

    # Start Docker-Compose
    log.info("Starting the Blockchain and the Cloud with Docker-Compose")
    tmux.send_command("blockchain_cloud", "docker compose up --build")
    sleep_countdown(4)
    while not is_service_running(port=8000) and not is_service_running(port=8443):
        print("Waiting for Docker to start...")
        time.sleep(1)
        input("Press Enter to continue...")
    # Start OEM Service
    log.info("Initializing the Client Service")
    tmux.send_command("oem_service", "cd client")
    tmux.send_command("oem_service", "source .venv/bin/activate")

    # TODO Do not initialize on every run
    tmux.send_command("oem_service", "python3 main.py --initialize")
    log.info("Starting the OEM Service")
    tmux.send_command("oem_service", "python3 main.py --oem-service")
    sleep_countdown(4)
    while not is_service_running(port=8123):
        print("Waiting for OEM Service to start...")
        time.sleep(1)
        input("Press Enter to continue...")

    # Start BMS
    for bms in ["bms_1", "bms_2"]:
        log.info(f"Starting BMS {bms}")
        tmux.send_command(bms, "cd bms/mock")
        tmux.send_command(bms, "source .venv/bin/activate")
        tmux.send_command(bms, f'INTERVAL_MIN="{BMS_DATA_GENERATION_INTERVAL}" python3 main.py')

    # Source Client for Maintenance Access
    tmux.send_command("console", "cd client")
    tmux.send_command("console", "source .venv/bin/activate")

    tmux.attach_to_tmux_session()

    tmux.kill_tmux_session()
    exec_cmd(["docker", "compose", "down"])


def signal_handler(_sig, _frame):
    print("\rreceived interrupt signal")
    global tmux
    if isinstance(tmux, Tmux):
        tmux.kill_tmux_session()
    sys.exit(1)


def check_return_code(code):
    if code != 0:
        print(f"Command failed with code {code}", file=sys.stderr)
        sys.exit(code)


def create_and_install_venv(dir):
    if not os.path.isdir(dir):
        log.error(f"Error: Directory '{dir}' does not exist.")
        return

    venv_path = os.path.join(dir, '.venv')
    requirements_path = os.path.join(dir, 'requirements.txt')


    if os.path.exists(venv_path):
        log.info(f"Virtual environment already exists at '{venv_path}'. Skipping creation.")
    else:
        log.info(f"Creating virtual environment at '{venv_path}'...")
        try:
            cwd = os.getcwd()
            os.chdir(dir)

            subprocess.run([sys.executable, '-m', 'venv', '.venv'], check=True, capture_output=True, text=True)

            os.chdir(cwd)
            log.info("Virtual environment created successfully.")
        except subprocess.CalledProcessError as e:
            os.chdir(cwd)
            log.error(f"Error creating virtual environment: {e}")
            print(f"Stdout: {e.stdout}")
            print(f"Stderr: {e.stderr}")
            return
        except Exception as e:
            os.chdir(cwd)
            log.error(f"An unexpected error occurred during venv creation: {e}")
            return

    venv_python_executable = os.path.join(venv_path, 'bin', 'python')

    if os.path.exists(requirements_path):
        log.info(f"Found '{requirements_path}'. Installing packages...")
        try:
            subprocess.run([venv_python_executable, '-m', 'pip', 'install', '-r', requirements_path],
                           check=True, capture_output=True, text=True)
            log.info("Packages from requirements.txt installed successfully.")
        except subprocess.CalledProcessError as e:
            log.error(f"Error installing packages from requirements.txt: {e}")
            print(f"Stdout: {e.stdout}")
            print(f"Stderr: {e.stderr}")
        except Exception as e:
            log.error(f"An unexpected error occurred during package installation: {e}")
    else:
        log.warning(f"No 'requirements.txt' found at '{requirements_path}'. Skipping package installation.")




def exec_cmd(unknown_args, dir='./'):
    cwd = os.getcwd()
    os.chdir(dir)
    process = subprocess.run(unknown_args, capture_output=True, text=DEBUG)
    os.chdir(cwd)
    check_return_code(process.returncode)
    os.chdir(cwd)
    check_return_code(process.returncode)


def client_cmd(unknown_args):
    cwd = os.getcwd()
    os.chdir('client')
    process = subprocess.run(["python3", "main.py", *unknown_args])
    os.chdir(cwd)
    check_return_code(process.returncode)



def cleanup_project():
    log.info("Cleaning up project...")
    for path in CLEANUP_FILES:
        try:
            if os.path.isfile(path):
                os.remove(path)  # Delete a file
                log.success(f"Deleted file: {path}")
            elif os.path.isdir(path):
                shutil.rmtree(path)  # Delete a directory and its contents
                log.success(f"Deleted directory: {path}")
            else:
                log.warning(f"Path does not exist: {path}")
        except Exception as e:
            log.error(f"Error deleting {path}: {e}")


def is_installed(cmd_util, manual = False):
    if manual:
        process = subprocess.run(cmd_util, capture_output=True, text=False)
    else:
        process = subprocess.run(["which", cmd_util], capture_output=True, text=False)
    return process.returncode == 0


def check_requirements():
    for req in REQUIREMENTS:
        if not is_installed(req):
            log.error(f"{req} is not installed. Please install {req} and try again.")
            exit(1)


def project_initialization():
    log.info("Initializing project...")

    if not os.path.exists("./blockchain/blockchain.json"):
        log.info("Creating blockchain.json file")
        exec_cmd(["go", "run", "./cmd/main.go","-genesis"], dir='./blockchain')

    if not os.path.exists("./cloud/.env"):
        log.info("Creating .env file for Cloud")
        with open('./cloud/.env', 'w') as file: file.write('PASSPHRASE=bad-password')


    create_and_install_venv("client")
    create_and_install_venv("bms/mock")

    # TODO Install dependencies for the Mock BMS Data Generator
    ## npm install json-schema-faker
    ## npm install json-schema-faker@0.5.9
    ## npx json-schema-faker cloud/BatteryData/BatteryData-Root-schema.json


def main():
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(dest="command")
    subparser.required = True
    for c in CLI_COMMANDS:
        subparser.add_parser(c)

    args, unknown_args = parser.parse_known_args()

    signal.signal(signal.SIGINT, signal_handler)

    if args.command == "clean":
        cleanup_project()
        exit(0)

    check_requirements()
    project_initialization()

    if args.command == "tmux":
        if not is_installed("tmux"):
            log.error("Tmux is not installed. Please install tmux and try again.")
            exit(1)
        service_monitor_on_steroids()
        exit(0)

    if args.command in ["up", "down"]:
        if not is_installed(["docker", "compose", "-h"], manual=True):
            log.error("Docker Compose is not installed. Please install Docker Compose and try again.")
            exit(1)
        exec_cmd(["docker", "compose", args.command, *unknown_args])




if __name__ == "__main__":
    main()