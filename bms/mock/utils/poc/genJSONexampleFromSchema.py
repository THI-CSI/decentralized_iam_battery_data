import subprocess
import json
import os


def generate_fake_battery_data(schema_path):
    schema_path = os.path.abspath(schema_path)
    schema_dir = os.path.dirname(schema_path)
    schema_file = os.path.basename(schema_path)

    try:
        result = subprocess.run(
            ["npx", "json-schema-faker", schema_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
            text=True,
            cwd=schema_dir
        )
        return delete_x_samm_aspect_model_urn(result.stdout)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Command failed: {e.stderr.strip()}") from e
    except json.JSONDecodeError as e:
        raise ValueError("Failed to parse JSON output") from e

def delete_x_samm_aspect_model_urn(data):
    """
    Recursively deletes all keys named 'x-samm-aspect-model-urn' from nested dictionaries or lists.
    """
    if isinstance(data, dict):
        # Use list to avoid RuntimeError from changing dict size during iteration
        keys_to_delete = [key for key in data if key == "x-samm-aspect-model-urn"]
        for key in keys_to_delete:
            del data[key]
        # Recursively process remaining items
        for value in data.values():
            delete_x_samm_aspect_model_urn(value)
    elif isinstance(data, list):
        for item in data:
            delete_x_samm_aspect_model_urn(item)
    # No-op for other types

    return data

if __name__ == "__main__":
    print(generate_fake_battery_data("cloud/BatteryPassDataModel/BatteryData-Root-schema.json"))

