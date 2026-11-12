#!/usr/bin/env python3
"""Reconstruct exact native Blender/atlas artifacts from immutable Git binary parts.

All sources come from successful genuine Blender 5.2.3 Core30 #43293980849.
Never overwrites an existing output. Checks part sizes and complete SHA256.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import tempfile

HERE = Path(__file__).resolve().parent
CHUNK_BYTES = 180000
SPECS = {
    "blender": {"target": "beach-pump-v2.blend",
                "parts_dir": "source-parts/beach-pump-v2.blend",
                "bytes": 3399312,
                "sha256": "77e212ecd01df4e1795e19bb1bb81c207917b1ac248420c4777a86f5b3924bf9",
                "parts": 19},
    "working-128": {"target": "working-128.png",
                    "parts_dir": "atlas-parts/working-128.png",
                    "bytes": 345371,
                    "sha256": "6610fab65021c423d9bfd265435b40ea18639765a402ea6dc2b21ee0595d93fe",
                    "parts": 2},
    "working-256": {"target": "working-256.png",
                    "parts_dir": "atlas-parts/working-256.png",
                    "bytes": 1179754,
                    "sha256": "da22edade7abe0fb421bb47400954ead9e36a03a494f23bfdc3cefeea8fe3d65",
                    "parts": 7}
}


def reassemble(label: str, verify_only: bool = False):
    spec = SPECS[label]
    dest = HERE / spec["target"]
    if dest.exists():
        digest = hashlib.sha256(dest.read_bytes()).hexdigest()
        if verify_only and dest.stat().st_size == spec["bytes"] and digest == spec["sha256"]:
            print(f"VERIFIED_EXISTING {label} {digest}")
            return
        raise FileExistsError(f"Refusing to overwrite existing output: {dest}")
    if verify_only:
        raise FileNotFoundError(f"No assembled output to verify: {dest}")
    folder = HERE / spec["parts_dir"]
    parts = [folder / f"part-{i:02d}.bin" for i in range(spec["parts"])]
    found = sorted(folder.glob("part-*.bin"))
    if found != parts:
        raise ValueError(f"Binary part list mismatch for {label}: expected {len(parts)}, found {len(found)}")
    for index, part in enumerate(parts):
        required = min(CHUNK_BYTES, spec["bytes"] - CHUNK_BYTES * index)
        if not part.is_file() or part.stat().st_size != required:
            raise ValueError(f"Incorrect or missing {part.name}: expected {required} bytes")
    fd, temp = tempfile.mkstemp(prefix=f".{spec['target']}.", suffix=".verified-part", dir=HERE)
    total = 0
    checksum = hashlib.sha256()
    try:
        with os.fdopen(fd, "wb") as stream:
            for part in parts:
                data = part.read_bytes()
                stream.write(data)
                checksum.update(data)
                total += len(data)
            stream.flush()
            os.fsync(stream.fileno())
        if total != spec["bytes"] or checksum.hexdigest() != spec["sha256"]:
            raise ValueError(f"SHA256 source transfer mismatch for {label}, refusing output")
        if dest.exists():
            raise FileExistsError(f"Output appeared during assembly: {dest}")
        os.replace(temp, dest)
        print(f"ASSEMBLY_SHA256_PASS {label} bytes={total} sha256={checksum.hexdigest()}")
    finally:
        if os.path.exists(temp):
            os.remove(temp)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--asset", choices=("all", *SPECS.keys()), default="all")
    p.add_argument("--verify-only", action="store_true", help="Verify existing assembled outputs")
    args = p.parse_args()
    for name in (SPECS if args.asset == "all" else (args.asset,)):
        reassemble(name, args.verify_only)


if __name__ == "__main__":
    main()
