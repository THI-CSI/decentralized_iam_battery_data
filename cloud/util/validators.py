import os
import json
import re
from jsonschema import validate, ValidationError

CLOUD_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SCHEMA_DIR = os.path.join(CLOUD_ROOT, 'Batterypass')

# ------------------------------- Shared ------------------------------- +
def load_schema(submodel: str) -> dict:
    path = os.path.join(SCHEMA_DIR, f"{submodel}-schema.json")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Schema not found for {submodel}")
    with open(path, "r") as f:
        return json.load(f)

# ------------------------------- Full Payload Validation ------------------------------- #
def validate_battery_pass_payload(data: dict):
    results = {}
    for submodel_name, payload in data.items():
        try:
            schema = load_schema(submodel_name)
            validate(instance=payload, schema=schema)
            results[submodel_name] = "Valid"
        except FileNotFoundError as e:
            results[submodel_name] = f"Missing schema: {e}"
        except ValidationError as e:
            results[submodel_name] = f"Validation error: {e.message}"
    return results

# ------------------------------- Field-Level Update Validation ------------------------------- #
def parse_path(path_str: str):
    steps = []
    parts = path_str.split(".")
    for part in parts:
        match = re.match(r"(\w+)(\[(\d+)\])?", part)
        if match:
            steps.append(match.group(1))
            if match.group(3):
                steps.append(int(match.group(3)))
    return steps


def get_subschema(schema: dict, path_steps: list):
    current = schema
    for step in path_steps:
        if isinstance(step, int):  # array index
            if "items" in current:
                current = current["items"]
            else:
                raise ValueError("Array index but no 'items' in schema")
        else:
            if "properties" in current and step in current["properties"]:
                current = current["properties"][step]
            else:
                raise ValueError(f"Property '{step}' not found in schema")
    return current


def validate_updates(update_list: list):
    results = []
    for update in update_list:
        if len(update) != 1:
            results.append({"error": "Each update must have one key-value pair."})
            continue

        full_path, value = list(update.items())[0]
        path_parts = full_path.split(".")
        submodel = path_parts[0]
        relative_path = ".".join(path_parts[1:])

        try:
            schema = load_schema(submodel)
            path_steps = parse_path(relative_path)
            subschema = get_subschema(schema, path_steps)
            validate(instance=value, schema=subschema)
            results.append({"path": full_path, "valid": True})
        except (ValidationError, FileNotFoundError, ValueError) as e:
            results.append({"path": full_path, "valid": False, "error": str(e)})
    return results