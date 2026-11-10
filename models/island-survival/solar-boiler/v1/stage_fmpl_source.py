#!/usr/bin/env python3
"""Stage ONLY committed FMPL material maps and camera/import code at a pinned ref.

Files are copied into an ephemeral runner directory; source maps are never
vendored into Tanks. Packed PBR textures in the .blend are the deliverable.
Git blob SHA-1 values from the authoritative catalog protect every map.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import time
from urllib.request import Request, urlopen

PIN = '939ff2d0fea5d236d7092b907c5f08961d5a7560'
BASE = f'https://raw.githubusercontent.com/mrcalzon02/Tech-Priests/{PIN}/'
CATALOG = 'art/source-to-3d/shared-parts/industrial-asset-library/catalog.json'
IMPORTER = 'art/source-to-3d/shared-parts/industrial-asset-library/import_materials.py'
CAMERA = ('tools/fmpl/capture_policy.py', 'tools/fmpl/blender_camera_guard.py')
MATERIALS = ('ferrocrete', 'ferrocrete_light', 'ferrocrete_dark')


def git_blob_sha(data):
    return hashlib.sha1(f'blob {len(data)}\0'.encode()+data).hexdigest()


def fetch(path, root):
    out = root / path
    if out.exists():
        raise FileExistsError('No staged source file overwrite: ' + str(out))
    out.parent.mkdir(parents=True, exist_ok=True)
    last = None
    for attempt in range(3):
        try:
            req = Request(BASE+path, headers={'User-Agent': 'tanks-solar-boiler-fmpl-reference/1'})
            with urlopen(req, timeout=45) as res:
                data = res.read()
            if not data:
                raise ValueError('Empty FMPL source file: ' + path)
            out.write_bytes(data)
            return {'path': path, 'bytes': len(data), 'git_blob_sha': git_blob_sha(data),
                    'sha256': hashlib.sha256(data).hexdigest()}
        except (OSError, ValueError) as e:
            last = e
            if attempt < 2: time.sleep(2**attempt)
    raise RuntimeError(f'Unable to stage pinned FMPL source {path}: {last}')


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--output',type=Path,required=True)
    args=p.parse_args()
    out=args.output.resolve()
    if out.exists() and any(out.iterdir()):
        raise FileExistsError('FMPL staging destination must be empty')
    out.mkdir(parents=True,exist_ok=True)
    entries=[fetch(CATALOG,out)]
    catalog=json.loads((out/CATALOG).read_text())
    if catalog.get('schema') != 'tp-industrial-asset-catalog.v1' or len(catalog.get('materials',[]))<23:
        raise ValueError('Unrecognized authoritative FMPL PBR catalog')
    entries.append(fetch(IMPORTER,out))
    for path in CAMERA:
        entries.append(fetch(path,out))
    ids={m['material_id']:m for m in catalog['materials']}
    for key in MATERIALS:
        spec=ids[key]
        for kind,record in sorted(spec['maps'].items()):
            e=fetch(record['source_path'],out)
            if e['git_blob_sha']!=record['git_blob_sha'] or e['bytes']!=record['size_bytes']:
                raise ValueError(f'{key}/{kind}: FMPL source blob hash or size mismatch')
            e['material_id']=key;e['kind']=kind
            entries.append(e)
    receipt={'schema':'tanks.solar.fmpl-reference.v1','source_repo':'mrcalzon02/Tech-Priests',
        'source_commit':PIN,'material_ids':list(MATERIALS),'files':entries,
        'no_external_models':True, 'source_textures_copied_to_tanks':False}
    (out/'fmpl-stage-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print('FMPL_REFERENCE_PBR_STAGED_VERIFIED',len(entries),PIN,flush=True)

if __name__=='__main__':main()
