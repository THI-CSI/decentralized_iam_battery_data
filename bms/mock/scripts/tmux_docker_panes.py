import subprocess
import sys
import argparse



def create_tmux_panes(num_panes):
    subprocess.run(['tmux', 'new-session', '-d', '-s', 'docker_session'])

    for i in range(num_panes):
        if i == 0:
            subprocess.run(['tmux', 'send-keys', '-t', 'docker_session:0', 'docker run -it --network host bms', 'C-m'])
        else:
            subprocess.run(['tmux', 'split-window', '-v', '-t', 'docker_session:0'])
            subprocess.run(['tmux', 'send-keys', '-t', f'docker_session:0.{i}', 'docker run -it --network host bms', 'C-m'])

    # Attach to the tmux session
    subprocess.run(['tmux', 'attach-session', '-t', 'docker_session'])

def kill_docker_containers():
    # Get the list of running Docker containers with the image name "bms"
    result = subprocess.run(['docker', 'ps', '--filter', 'ancestor=bms', '-q'], stdout=subprocess.PIPE, text=True)
    container_ids = result.stdout.strip().split('\n')

    # Kill each container
    for container_id in container_ids:
        if container_id:  # Check if the container_id is not empty
            subprocess.run(['docker', 'kill', container_id])

def main():
    parser = argparse.ArgumentParser(description='Create tmux panes to run Docker containers.')
    parser.add_argument('num_panes', type=int, help='Number of tmux panes to create')
    args = parser.parse_args()

    if args.num_panes < 1:
        print("Error: Number of panes must be at least 1.")
        sys.exit(1)

    create_tmux_panes(args.num_panes)
    kill_docker_containers()

if __name__ == "__main__":
    main()
