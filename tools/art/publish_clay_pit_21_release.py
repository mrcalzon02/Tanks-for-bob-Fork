#!/usr/bin/env python3
"""Upload only the exact Clay Pit V4c 1.8.97 package after official engine launch.

Guarded against missing source hashes, wrong version, or unverified runtime logs.
Uses repository-owned Mod Portal upload key from the protected GitHub secret.
"""
import hashlib
import json
import os
from pathlib import Path
import sys
import zipfile

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'ci'))
import publish_mod_portal as portal
from build_clay_pit_21_release import NEW_VERSION, MOD_NAME, PREFIX


def sha_bytes(blob): return hashlib.sha256(blob).hexdigest()


def main():
    if len(sys.argv)!=2:
        raise SystemExit('Usage: publish_clay_pit_21_release.py VERIFIED_OUTPUT_DIRECTORY')
    root=Path(sys.argv[1]).resolve()
    package=root/f'{MOD_NAME}_{NEW_VERSION}.zip'
    evidence=root/'clay-v4c-promotion-receipt.json'
    hashfile=root/(package.name+'.sha256')
    version=root/'engine-version.txt'
    create=root/'engine-create.log'
    benchmark=root/'engine-benchmark.log'
    required=(package,evidence,hashfile,version,create,benchmark)
    for path in required:
        if not path.is_file(): raise RuntimeError('Refusing portal upload; missing evidence '+path.name)
    if '2.1.23' not in version.read_text(errors='replace'):
        raise RuntimeError('Missing Factorio 2.1.23 engine evidence')
    if 'Loading mod tanks_for_bob_fork' not in create.read_text(errors='replace'):
        raise RuntimeError('Engine did not demonstrate loading Tanks for Bob')
    bench=benchmark.read_text(errors='replace')
    if not bench.strip() or ('Performed ' not in bench and 'ticks' not in bench):
        raise RuntimeError('Full game benchmark evidence absent')
    receipt=json.loads(evidence.read_text())
    sha=sha_bytes(package.read_bytes())
    if sha!=receipt.get('sha256') or sha!=hashfile.read_text().split()[0]:
        raise RuntimeError('Versioned package SHA mismatch')
    if (receipt.get('version')!=NEW_VERSION or receipt.get('factorio_version')!='2.1' or
            receipt.get('source_revision')!='v4c-readable-bucket-swing' or
            receipt.get('capture_frame_count')!=68 or
            receipt.get('directions')!=['north','east','south','west'] or
            not receipt.get('original_2_0_source_untouched')):
        raise RuntimeError('Different source/release; refusing to upload')
    rootdir=f'{MOD_NAME}_{NEW_VERSION}/'
    with zipfile.ZipFile(package) as z:
        if z.testzip() is not None: raise RuntimeError('Corrupt versioned mod ZIP')
        meta=json.loads(z.read(rootdir+'info.json'))
        if (meta.get('name')!=MOD_NAME or meta.get('version')!=NEW_VERSION or
                meta.get('factorio_version')!='2.1' or
                'base >= 2.1' not in meta.get('dependencies',[])):
            raise RuntimeError('Wrong engine dependency in production release')
        for rel,digest in receipt['new_art_hashes'].items():
            if sha_bytes(z.read(rootdir+rel))!=digest:
                raise RuntimeError('Accepted clay-pit atlas hash changed: '+rel)
        source=z.read(rootdir+'prototypes/entity/entities.lua').decode('utf-8')
        clay=source[source.index('  --claypit'):source.index('--pit-kiln')]
        if clay.count(PREFIX+'-working.png')!=4 or clay.count(PREFIX+'-idle.png')!=4:
            raise RuntimeError('Missing one or more four-way prototype directions')
    secret=os.getenv('FACTORIO_MOD_UPLOAD_KEY','').strip()
    if not secret: raise RuntimeError('Missing FACTORIO_MOD_UPLOAD_KEY; upload cannot proceed')
    print('CLAY_PIT_V4C_21_ENGINE_AND_ASSET_GATE_PASSED',sha,flush=True)
    portal.upload(package,NEW_VERSION,secret)
    indexed=NEW_VERSION in portal.portal_versions()
    state='publicly_indexed' if indexed else 'upload_accepted_index_pending'
    (root/'mod-portal-publication.json').write_text(json.dumps({
        'name':MOD_NAME,'version':NEW_VERSION,'factorio_version':'2.1','status':state,
        'sha256':sha,'url':f'https://mods.factorio.com/mod/{MOD_NAME}'
    },indent=2)+'\n')
    print('CLAY_PIT_V4C_PORTAL_'+state.upper(),flush=True)

if __name__=='__main__':main()
