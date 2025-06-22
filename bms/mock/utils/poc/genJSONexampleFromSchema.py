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
        return result.stdout
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Command failed: {e.stderr.strip()}") from e
    except json.JSONDecodeError as e:
        raise ValueError("Failed to parse JSON output") from e


# if __name__ == "__main__":
#     generate_fake_battery_data("cloud/BatteryPassDataModel/BatteryData-Root-schema.json")

