import docker
import argparse
import sys
import time
import json
import os


CONTAINER_STATE_FILE = "managed_containers.json"


def load_managed_containers():
    if os.path.exists(CONTAINER_STATE_FILE):
        with open(CONTAINER_STATE_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                print(f"Warning: Could not decode {CONTAINER_STATE_FILE}. Starting with an empty managed list.")
                return {}
    return {}


def save_managed_containers(containers_dict):
    with open(CONTAINER_STATE_FILE, 'w') as f:
        json.dump(containers_dict, f, indent=4)


def get_docker_client():
    try:
        client = docker.from_env()
        client.ping()
        return client
    except docker.errors.APIError as e:
        print(f"Error connecting to Docker daemon: {e}")
        print("Please ensure Docker is running and accessible.")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred while connecting to Docker: {e}")
        sys.exit(1)


def create_containers(client, amount, interval_min=None):
    managed_containers_data = load_managed_containers()
    print(f"Attempting to create {amount} Docker containers...")
    created_count = 0
    for i in range(amount):
        container_name = f"bms_script_container_{int(time.time())}_{i}"

        environment_vars = {}
        if interval_min is not None:
            environment_vars["INTERVAL_MIN"] = str(interval_min)

        try:
            container = client.containers.run(
                image="bms",
                name=container_name,
                detach=True,
                network="host",
                environment=environment_vars
            )
            managed_containers_data[container.id] = container.name
            print(f"  Container '{container.name}' ({container.id[:12]}) created.")
            created_count += 1
        except docker.errors.ImageNotFound:
            print(f"Error: Docker image 'bms' not found. Please ensure it exists.")
            continue
        except docker.errors.ContainerError as e:
            print(f"Error running container '{container_name}': {e}")
            continue
        except Exception as e:
            print(f"An unexpected error occurred creating container '{container_name}': {e}")
            continue
    save_managed_containers(managed_containers_data)
    if created_count > 0:
        print(f"\nSuccessfully created {created_count} containers.")
    else:
        print("\nNo containers were successfully created.")


def list_containers(client):
    managed_containers_data = load_managed_containers()
    if not managed_containers_data:
        print("No containers are currently managed by this script.")
        return

    print("Containers managed by this script:")
    all_docker_containers = {c.id: c for c in client.containers.list(all=True)}

    ids_to_remove_from_managed = []

    for container_id, container_name in list(managed_containers_data.items()):
        container = all_docker_containers.get(container_id)
        if container:
            try:
                container.reload()
                print(f"  ID: {container.id[:12]}, Name: {container.name}, Status: {container.status}")
            except docker.errors.NotFound:
                print(
                    f"  ID: {container_id[:12]}, Name: {container_name}, Status: Not Found (might have been removed externally).")
                ids_to_remove_from_managed.append(container_id)
            except Exception as e:
                print(f"  Error retrieving status for container {container_id[:12]}: {e}")
        else:
            print(f"  ID: {container_id[:12]}, Name: {container_name}, Status: Not Running (and not found by Docker).")
            ids_to_remove_from_managed.append(container_id)

    for container_id in ids_to_remove_from_managed:
        if container_id in managed_containers_data:
            del managed_containers_data[container_id]

    save_managed_containers(managed_containers_data)


def get_container_output(client, container_id_prefix):
    managed_containers_data = load_managed_containers()

    found_container_obj = None
    for container_id, container_name in list(managed_containers_data.items()):
        if container_id.startswith(container_id_prefix) or container_name == container_id_prefix:
            try:
                found_container_obj = client.containers.get(container_id)
                break
            except docker.errors.NotFound:
                print(
                    f"Warning: Managed container '{container_name}' ({container_id[:12]}) not found by Docker. Removing from managed list.")
                del managed_containers_data[container_id]
                continue
    save_managed_containers(managed_containers_data)

    if not found_container_obj:
        try:
            all_docker_containers = client.containers.list(all=True)
            for c in all_docker_containers:
                if c.id.startswith(container_id_prefix) or c.name == container_id_prefix:
                    found_container_obj = c
                    break
        except Exception as e:
            print(f"An error occurred while searching for container globally: {e}")

    if found_container_obj:
        try:
            print(
                f"\n--- Streaming logs for container '{found_container_obj.name}' ({found_container_obj.id[:12]}) ---")
            print("Press Ctrl+C to stop streaming.")

            for line in found_container_obj.logs(stream=True, follow=True, tail="all"):
                print(line.decode('utf-8').strip())
        except docker.errors.NotFound:
            print(f"Error: Container '{container_id_prefix}' not found (might have been removed).")
        except KeyboardInterrupt:
            print("\n--- Stopped streaming logs. ---")
        except Exception as e:
            print(f"An error occurred while fetching or streaming logs for '{container_id_prefix}': {e}")
    else:
        print(f"Error: Container with ID or name '{container_id_prefix}' not found.")


def kill_all_containers(client):
    managed_containers_data = load_managed_containers()
    if not managed_containers_data:
        print("No containers are currently managed by this script to kill.")
        return

    print("Attempting to stop and remove all managed containers...")
    killed_count = 0
    containers_to_remove_from_list = []

    for container_id, container_name in list(managed_containers_data.items()):
        try:
            container = client.containers.get(container_id)
            print(f"  Stopping container '{container.name}' ({container.id[:12]})...")
            container.stop(timeout=5)
            print(f"  Removing container '{container.name}' ({container.id[:12]})...")
            container.remove()
            killed_count += 1
            containers_to_remove_from_list.append(container_id)
            print(f"  Container '{container.name}' removed.")
        except docker.errors.NotFound:
            print(f"  Container '{container_name}' ({container_id[:12]}) already removed or not found by Docker.")
            containers_to_remove_from_list.append(container_id)
        except Exception as e:
            print(f"  Error stopping/removing container '{container_name}' ({container_id[:12]}): {e}")

    for container_id in containers_to_remove_from_list:
        if container_id in managed_containers_data:
            del managed_containers_data[container_id]

    save_managed_containers(managed_containers_data)

    print(f"\nSuccessfully stopped and removed {killed_count} containers.")
    if managed_containers_data:
        print(f"Warning: {len(managed_containers_data)} containers could not be removed "
              f"(see errors above or they might have been removed externally previously).")


def main():
    parser = argparse.ArgumentParser(
        description="Manage Docker containers for the 'bms' image. "
                    "This script maintains a list of managed containers in 'managed_containers.json'."
    )
    parser.add_argument(
        "-c", "--create",
        type=int,
        help="Specify the number of Docker containers to create (e.g., -c 3)."
    )
    parser.add_argument(
        "-l", "--list",
        action="store_true",
        help="List all Docker containers currently managed by this script."
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        help="Display the output (logs) of a specified container by its ID prefix or name "
             "(e.g., -o abc123def456 or -o my_container_name)."
    )
    parser.add_argument(
        "-k", "--kill-all",
        action="store_true",
        help="Stop and remove all Docker containers created by this script."
    )
    parser.add_argument(
        "--interval-min",
        type=float,
        help="Set the INTERVAL_MIN environment variable for created containers (e.g., --interval-min 60)."
    )

    args = parser.parse_args()
    client = get_docker_client()

    action_count = sum([bool(args.create), args.list, bool(args.output), args.kill_all])

    if action_count > 1:
        parser.error("Please specify only one main action at a time (--create, --list, --output, or --kill-all). "
                     "The --interval-min argument is only valid with --create.")
    elif action_count == 0:
        parser.print_help()
        print("\nNo action specified. Use -h or --help for usage instructions.")
        sys.exit(0)

    if args.create is not None:
        if args.create <= 0:
            print("Error: Amount to create must be a positive integer.")
            sys.exit(1)
        create_containers(client, args.create, args.interval_min)
    elif args.list:
        if args.interval_min is not None:
            print("Warning: --interval-min is only applicable with --create and will be ignored.")
        list_containers(client)
    elif args.output:
        if args.interval_min is not None:
            print("Warning: --interval-min is only applicable with --create and will be ignored.")
        get_container_output(client, args.output)
    elif args.kill_all:
        if args.interval_min is not None:
            print("Warning: --interval-min is only applicable with --create and will be ignored.")
        kill_all_containers(client)


if __name__ == "__main__":
    main()
