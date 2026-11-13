#!/usr/bin/env python3
"""Byte-preserving reconstruction of genuine Blender 5.2 V4 master from Git parts."""
import argparse
import hashlib
import json
import os
from pathlib import Path
from tempfile import NamedTemporaryFile

def assemble(root: Path, verify_only: bool = False):
    manifest = json.loads((root / "source_manifest.json").read_text(encoding="utf-8"))
    assert manifest["schema"] == "tanks.beach-pump.v4.exact-native-blender-git-parts"
    dest = root / manifest["source_filename"]
    if dest.exists():
        data = dest.read_bytes()
        if len(data) != manifest["source_bytes"] or hashlib.sha256(data).hexdigest() != manifest["source_sha256"]:
            raise FileExistsError(f"Conflicting native model exists: {dest}")
        print("BEACH_V4_NATIVE_ALREADY_VERIFIED", dest)
        return
    temp = None
    total = 0
    digest = hashlib.sha256()
    try:
        if not verify_only:
            temp = NamedTemporaryFile(mode="wb", prefix=".beach-pump-v4-", dir=root, delete=False)
        for part in manifest["parts"]:
            partpath = root / part["name"]
            body = partpath.read_bytes()
            if len(body) != part["bytes"]:
                raise ValueError(f"Git part truncated or altered: {partpath}")
            # Confirm each part's Git SHA-1 blob identity, independently.
            githash = hashlib.sha1(b"blob " + str(len(body)).encode("ascii") + b"\0" + body).hexdigest()
            if githash != part["git_blob_sha1"]:
                raise ValueError(f"Git part content identity mismatch: {partpath}")
            digest.update(body)
            total += len(body)
            if temp:
                temp.write(body)
        actual = digest.hexdigest()
        if total != manifest["source_bytes"] or actual != manifest["source_sha256"]:
            raise ValueError(f"Native Blender byte checksum failed: {actual} ({total} bytes)")
        if temp:
            temp.flush()
            os.fsync(temp.fileno())
            temp.close()
            os.replace(temp.name, dest)
            temp = None
        print("BEACH_V4_GENUINE_NATIVE_BLEND_VERIFIED", actual, total, "verify_only=",verify_only)
    finally:
        if temp:
            name = temp.name
            temp.close()
            Path(name).unlink(missing_ok=True)

if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--verify-only", action="store_true")
    args=parser.parse_args()
    assemble(Path(__file__).resolve().parent, args.verify_only)
