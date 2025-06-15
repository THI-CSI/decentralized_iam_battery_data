#!/usr/bin/env python

import functools
import json
import click
from base64 import b64encode
from datetime import datetime
from functools import lru_cache
from urllib.parse import quote
from pathlib import Path
from os import urandom, getenv
from dotenv import load_dotenv
from Crypto.Protocol.DH import key_agreement
from Crypto.PublicKey import ECC
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Signature import DSS
from Crypto.Protocol.KDF import HKDF

cloud_path = Path(__file__).parent.parent.parent
payloads_path = Path(__file__).parent / "payloads"
payloads_path.mkdir(exist_ok=True)
bms_did: str
oem_did: str
bms_key: ECC.EccKey
oem_key: ECC.EccKey


@lru_cache()
def load_cloud_public_key() -> ECC.EccKey:
    with open(cloud_path / "crypto" / "keys" / "key.pem", 'rb') as f:
        return ECC.import_key(f.read(), passphrase=getenv("PASSPHRASE")).public_key()


def gen_payload(path: Path, sign_key: ECC.EccKey, sender_did: str, b: bytes, query: str = None) -> None:
    eph_key = ECC.generate(curve="P-256")
    cloud_pub = load_cloud_public_key()
    salt = urandom(32)
    nonce = urandom(12)
    eph_pub = eph_key.public_key().export_key(format="DER")
    context = eph_pub + cloud_pub.export_key(format="DER")
    hkdf = functools.partial(HKDF, key_len=32, hashmod=SHA256, salt=salt, context=context)
    aes_key = key_agreement(eph_priv=eph_key, static_pub=cloud_pub, kdf=hkdf)
    cipher = AES.new(aes_key, AES.MODE_GCM, nonce=nonce)
    cipher.update(nonce)
    ciphertext, tag = cipher.encrypt_and_digest(b)
    payload = {
        "ciphertext": b64encode(ciphertext + tag).decode(),
        "aad": b64encode(nonce).decode(),
        "salt": b64encode(salt).decode(),
        "eph_pub": b64encode(eph_pub).decode(),
        "did": sender_did,
    }
    signature = DSS.new(sign_key, mode="fips-186-3", encoding="binary").sign(SHA256.new(
        json.dumps(payload, separators=(",", ":")).encode()
    ))
    payload["signature"] = b64encode(signature).decode()
    with open(path, "w") as f:
        if query is None:
            json.dump(payload, f, indent=4)
        else:
            f.write(f"{query}payload={quote(json.dumps(payload, separators=(",", ":")))}")
    print(f"Generated {path}")


def gen_get_payload() -> None:
    gen_payload(payloads_path / "get_payload.txt", bms_key, bms_did, urandom(128), "public=false&")


def gen_post_payload() -> None:
    update = [{
        "performance.batteryCondition.numberOfFullCycles": {
            "numberOfFullCyclesValue": 1e100,
            "lastUpdate": datetime.now().isoformat()
        }
    }]
    gen_payload(payloads_path / "post_payload.json", bms_key, bms_did, json.dumps(update).encode())


def gen_put_payload() -> None:
    with open(Path(__file__).parent / "batterypass.json", "r") as f:
        batterypass = json.load(f)
    gen_payload(payloads_path / "put_payload.json", oem_key, oem_did, json.dumps(batterypass).encode())


def gen_delete_payload() -> None:
    gen_payload(payloads_path / "delete_payload.txt", bms_key, bms_did, urandom(128), "")


@click.command()
@click.argument("did_bms", type=str)
@click.argument("did_oem", type=str)
@click.argument("bms_key_path", type=click.Path(exists=True, path_type=Path))
@click.argument("oem_key_path", type=click.Path(exists=True, path_type=Path))
def main(did_bms, did_oem, bms_key_path, oem_key_path):
    global bms_key, oem_key, bms_did, oem_did
    load_dotenv(cloud_path / ".env")
    with open(bms_key_path, "r") as f:
        bms_key = ECC.import_key(f.read())
    with open(oem_key_path, "r") as f:
        oem_key = ECC.import_key(f.read())
    bms_did = did_bms
    oem_did = did_oem
    gen_get_payload()
    gen_post_payload()
    gen_put_payload()
    gen_delete_payload()
    print("All payloads were generated successfully!")


if __name__ == '__main__':
    main()
