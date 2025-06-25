import json
import json5

from functools import lru_cache
from pathlib import Path
from typing import Literal, Any
from tinydb.table import Document
from crypto.crypto import decrypt_and_verify, decrypt_hpke
from Crypto.PublicKey import ECC
from util.models import EncryptedPayload


@lru_cache
def load_attributes() -> dict:
    with open(Path(__file__).parent / "attributes.jsonc") as f:
        return json5.load(f)


def verify_request(item: EncryptedPayload, private_key: ECC.EccKey) -> bytes:
    return decrypt_and_verify(private_key, json.dumps(item.model_dump()).encode())


def retrieve_data(scope: Literal["public", "bms", "legitimate_interest"], did: str, doc: Document,
                  private_key: ECC.EccKey):
    if scope not in ["public", "bms", "legitimate_interest"]:
        raise ValueError(f"Scope '{scope}' is not in ['public', 'bms', 'legitimate_interest'].")
    decrypted_data = decrypt_hpke(
        private_key=private_key,
        bundle=doc["encrypted_data"]
    )
    decrypted_dict = json.loads(decrypted_data)
    if scope == "bms":
        return decrypted_dict
    attributes = load_attributes()
    output_dict = filter_attributes(scope, attributes, decrypted_dict)
    return output_dict


def filter_attributes(
        scope: Literal["public", "legitimate_interest"],
        attributes: dict[str, Any],
        input_dict: dict[str, Any]
) -> dict[str, Any]:
    def merge_scopes(base_scope: dict, extra_scope: dict) -> dict:
        merged = dict(base_scope)
        for key, value in extra_scope.items():
            if key in merged:
                if isinstance(value, dict) and isinstance(merged[key], dict):
                    merged[key] = merge_scopes(merged[key], value)
                elif isinstance(value, list) and isinstance(merged[key], list):
                    merged[key] = list(set(merged[key]) | set(value))
            else:
                merged[key] = value
        return merged

    def recursive_filter(attr_structure: Any, data: Any, path: str = "") -> Any:
        result = {}
        if isinstance(attr_structure, dict):
            for key, sub_attrs in attr_structure.items():
                if key not in data:
                    continue
                filtered = recursive_filter(sub_attrs, data[key], path=f"{path}.{key}" if path else key)
                if filtered:
                    result[key] = filtered
        elif isinstance(attr_structure, list):
            for attr in attr_structure:
                if attr not in data:
                    continue
                if path == "materialComposition" and attr == "batteryMaterials" and scope == "public":
                    filtered_battery_materials = []
                    for item in data[attr]:
                        comp_name = item.get("batteryMaterialLocation", {}).get("componentName")
                        if comp_name in {"Anode", "Cathode", "Electrolyte"}:  # Exclude anode/cathode/electrolyte
                            continue
                        filtered_battery_materials.append(item)
                    if filtered_battery_materials:
                        result[attr] = filtered_battery_materials
                else:
                    result[attr] = data[attr]
        return result
    if scope == "legitimate_interest":
        merged_attrs = merge_scopes(attributes["public"], attributes["legitimate_interest"])
    else:
        merged_attrs = attributes["public"]

    return recursive_filter(merged_attrs, input_dict)
