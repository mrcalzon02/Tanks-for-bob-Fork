#!/usr/bin/env python3
"""Reassemble the exact full-68-frame Beach Pump Blender 5.2 source.

12 immutable Git parts, independently source-SHA checked. No network,
re-render, modeling, gameplay or workflow mutation. Refuses overwriting.
"""
from __future__ import annotations
import argparse,hashlib,os,tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent
EXPECTED_SHA="022ff8b827f326bb351515b5180be06527a6c7daf5028d9b24fb3fdcab084ee0"
EXPECTED_BYTES=3360006
COUNT=12
CHUNK_BYTES=300000

def reconstruct(target):
    out=Path(target).expanduser().resolve()
    if out.exists():raise FileExistsError("Refuse to replace an editable master: "+str(out))
    parts=[HERE/"native-blend-parts"/f"part-{i:02d}.bin" for i in range(COUNT)]
    for i,p in enumerate(parts):
        expected=CHUNK_BYTES if i<COUNT-1 else EXPECTED_BYTES-(COUNT-1)*CHUNK_BYTES
        if not p.is_file() or p.stat().st_size!=expected:
            raise ValueError("Missing or altered Blender source part: "+str(p))
    out.parent.mkdir(parents=True,exist_ok=True)
    fd,tmp=tempfile.mkstemp(prefix="beach-master-",suffix=".partial",dir=out.parent)
    h=hashlib.sha256();n=0
    try:
        with os.fdopen(fd,"wb") as stream:
            for p in parts:
                data=p.read_bytes()
                h.update(data);stream.write(data);n+=len(data)
        if n!=EXPECTED_BYTES or h.hexdigest()!=EXPECTED_SHA:
            raise ValueError("Exact native Blender SHA256 mismatch")
        if out.exists():raise FileExistsError("Refuse output collision")
        os.replace(tmp,out)
    finally:
        if Path(tmp).exists():Path(tmp).unlink()
    print("BEACH_PUMP_FULL_NATIVE_BLENDER_REASSEMBLY_PASS",str(out),h.hexdigest())

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--out",default=str(HERE/"beach-pump-v1.blend"))
    a=p.parse_args()
    reconstruct(a.out)
if __name__=="__main__":
    main()
