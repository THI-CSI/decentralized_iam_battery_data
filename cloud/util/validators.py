import os
from pathlib import Path
import json
import re
from jsonschema import validate, Draft4Validator, ValidationError

# Define relevant paths
# TODO Probably wrong PROJECT ROOT in the docker-compose container
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
SCHEMA_DIR = PROJECT_ROOT / 'cloud' / 'BatteryPassDataModel'

# ------------------------------- Shared ------------------------------- #
def load_schema(submodel: str) -> dict:
    """Load a schema from the BatteryPassDataModel"""
    submodel = submodel[0].upper() + submodel[1:]
    path = SCHEMA_DIR / f"{submodel}-schema.json"
    if not path.exists():
        raise FileNotFoundError(f"Schema not found for {submodel}")
    with path.open("r", encoding="utf-16") as f:
        return json.load(f)

# ------------------------------- Full Payload Validation ------------------------------- #
def validate_battery_pass_payload(data: dict):
    """Validate a complete given battery pass payload"""
    results = {}
    for submodel_name, payload in data.items():
        try:
            schema = load_schema(submodel_name)
            #validate(instance=payload, schema=schema)
            Draft4Validator(schema).validate(payload)
            results[submodel_name] = "Valid"
        except FileNotFoundError as e:
            results[submodel_name] = f"Missing schema: {e}"
        except ValidationError as e:
            results[submodel_name] = f"Validation error: {e.message}"
    return results

# ------------------------------- Field-Level Update Validation ------------------------------- #
def parse_path(path_str: str):
    """Parse a given path and return all steps"""
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
    """Get subschema from a given schema"""
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


def resolve_ref(schema, ref):
    """Resolves a local $ref within a schema"""
    if not ref.startswith("#/"):
        raise ValueError(f"Only local refs supported: {ref}")
    parts = ref.lstrip("#/").split("/")
    sub = schema
    for part in parts:
        sub = sub[part]
    return sub

def dereference_subschema(schema, subschema):
    """Resolve $ref in the subschema (single level only)"""
    if "$ref" in subschema:
        return resolve_ref(schema, subschema["$ref"])
    return subschema


def validate_updates(update_list: list):
    """Validate updates from the PUT-request"""
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

            # Resolve $ref if present
            resolved_subschema = dereference_subschema(schema, subschema)

            # Validate just the value
            Draft4Validator(resolved_subschema).validate(value)
            results.append({"path": full_path, "valid": True})
        except (ValidationError, FileNotFoundError, ValueError) as e:
            results.append({"path": full_path, "valid": False, "error": str(e)})
    return results
