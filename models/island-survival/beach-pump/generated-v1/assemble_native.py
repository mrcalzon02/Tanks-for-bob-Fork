#!/usr/bin/env python3
"""Reconstruct the EXACT independently reopened 3D Beach Pump native Blender master.

Safe: reads only the versioned binary part files, refuses to overwrite output,
checks each part length and FINAL SHA256, then renames atomically. No Blender,
game prototype or network needed.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import tempfile

HERE = Path(__file__).resolve().parent
EXPECTED_SHA256 = "aed52dad68e16f40d626e713c525081ce77eb93210fc622e8cfa55ddecb5428d"
EXPECTED_BYTES = 3360030
PARTS = 12
PART_BYTES = 300000

def rebuild(target):
    target = Path(target).expanduser().resolve()
    if target.exists():
        raise FileExistsError("Refuse to overwrite any existing native Blender master: " + str(target))
    parts = [HERE/"native-blend-parts"/f"part-{i:02d}.bin" for i in range(PARTS)]
    if not all(p.is_file() for p in parts):
        raise FileNotFoundError("One or more source-preserving Blender part files are missing")
    for i,p in enumerate(parts):
        expected = PART_BYTES if i < PARTS-1 else EXPECTED_BYTES - (PARTS-1)*PART_BYTES
        if p.stat().st_size != expected:
            raise ValueError(f"Incorrect binary part length {p.name}: {p.stat().st_size} != {expected}")
    target.parent.mkdir(parents=True,exist_ok=True)
    fd,tmp = tempfile.mkstemp(prefix="beach-pump-v1.",suffix=".part",dir=target.parent)
    from os import fdopen, replace, unlink
    digest = hashlib.sha256()
    total = 0
    try:
        with fdopen(fd,"wb") as handle:
            for p in parts:
                content=p.read_bytes()
                digest.update(content)
                handle.write(content)
                total += len(content)
        if total != EXPECTED_BYTES or digest.hexdigest() != EXPECTED_SHA256:
            raise ValueError("Native Blender reconstruction SHA256 mismatch; refuse publication")
        if target.exists():raise FileExistsError("Output collision during reconstruction")
        replace(tmp,target)
    finally:
        if Path(tmp).exists():unlink(tmp)
    print("BEACH_PUMP_NATIVE_BLENDER_REASSEMBLED_SHA256_PASS",str(target),digest.hexdigest())

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--out",default=str(HERE/"beach-pump-v1.blend"))
    args=parser.parse_args()
    rebuild(args.out)

if __name__=="__main__":main()
