#!/usr/bin/env python3
"""Reassemble exact 3D Blender V2 from Core30-verified immutable Git source parts.

The 2026-11-12 native model was independently reopened by Blender 5.2.3.
No image generation or approximation: only bytewise concatenation and SHA256.
"""
from __future__ import annotations
import argparse
import hashlib
import os
from pathlib import Path
import tempfile

HERE=Path(__file__).resolve().parent
EXPECTED_SHA256="ee9c9ba560f8b28a580c7307e642f1f6c420627a3165131a0c4f6b53987d0646"
EXPECTED_BYTES=3399311
PART_COUNT=12
PART_BYTES=300000

def assemble(target:Path):
    target=target.expanduser().resolve()
    if target.exists():
        raise FileExistsError(f"Refusing to overwrite previous source: {target}")
    sources=[HERE/"native-blend-parts"/f"part-{i:02d}.bin" for i in range(PART_COUNT)]
    for i,path in enumerate(sources):
        needed=min(PART_BYTES,EXPECTED_BYTES-PART_BYTES*i)
        if not path.is_file() or path.stat().st_size!=needed:
            raise ValueError(f"Missing or incorrect source part {path.name}: expected {needed} bytes")
    target.parent.mkdir(parents=True,exist_ok=True)
    fd,temp=tempfile.mkstemp(prefix=".beach-pump-v2-",suffix=".part",dir=target.parent)
    digest=hashlib.sha256()
    length=0
    try:
        with os.fdopen(fd,"wb") as writer:
            for file in sources:
                part=file.read_bytes()
                digest.update(part)
                writer.write(part)
                length+=len(part)
        if length!=EXPECTED_BYTES or digest.hexdigest()!=EXPECTED_SHA256:
            raise ValueError("Refusing to publish unverified Blender source bytes")
        if target.exists():
            raise FileExistsError("Output appeared while assembling source")
        os.replace(temp,target)
    finally:
        if os.path.exists(temp):os.unlink(temp)
    print("BEACH_V2_BYTE_IDENTICAL_NATIVE_BLENDER_REASSEMBLED",
          target,EXPECTED_SHA256,flush=True)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--out",type=Path,default=HERE/"beach-pump-v2.blend")
    args=p.parse_args()
    assemble(args.out)

if __name__=="__main__":
    main()
