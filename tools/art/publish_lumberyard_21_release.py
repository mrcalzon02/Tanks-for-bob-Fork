#!/usr/bin/env python3
"""Upload only accepted Steam Lumberyard V2b 1.8.99 package after official engine launch.

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
from build_lumberyard_21_release import NEW_VERSION, MOD_NAME, PREFIX


def sha_bytes(blob): return hashlib.sha256(blob).hexdigest()


def main():
    if len(sys.argv)!=2:
        raise SystemExit('Usage: publish_lumberyard_21_release.py VERIFIED_OUTPUT_DIRECTORY')
    root=Path(sys.argv[1]).resolve()
    package=root/f'{MOD_NAME}_{NEW_VERSION}.zip'
    evidence=root/'lumberyard-v2b-release-receipt.json'
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
            receipt.get('source_revision')!='steam-lumberyard-v2b-visible-power-transmission' or
            receipt.get('capture_frame_count')!=68 or
            receipt.get('directions')!=['north','east','south','west'] or
            not receipt.get('previous_art_preserved')):
        raise RuntimeError('Different source/release; refusing to upload')
    rootdir=f'{MOD_NAME}_{NEW_VERSION}/'
    with zipfile.ZipFile(package) as z:
        if z.testzip() is not None: raise RuntimeError('Corrupt versioned mod ZIP')
        meta=json.loads(z.read(rootdir+'info.json'))
        if (meta.get('name')!=MOD_NAME or meta.get('version')!=NEW_VERSION or
                meta.get('factorio_version')!='2.1' or
                'base >= 2.1' not in meta.get('dependencies',[])):
            raise RuntimeError('Wrong engine dependency in production release')
        if len(receipt.get('new_art_hashes',{}))!=7 or not receipt.get('pulley_alignment_verified'):
        raise RuntimeError('Corrected saw-side pulley provenance missing')
    for rel,digest in receipt['new_art_hashes'].items():
            if sha_bytes(z.read(rootdir+rel))!=digest:
                raise RuntimeError('Accepted lumberyard atlas hash changed: '+rel)
        source=z.read(rootdir+'prototypes/entity/entities.lua').decode('utf-8')
        lumber=source[source.index('  --Growing plot'):source.index('--quarry')]
        if lumber.count(PREFIX+'-working.png')!=4 or lumber.count(PREFIX+'-idle.png')!=4:
            raise RuntimeError('Missing one or more lumberyard sprite directions')
    secret=os.getenv('FACTORIO_MOD_UPLOAD_KEY','').strip()
    if not secret: raise RuntimeError('Missing FACTORIO_MOD_UPLOAD_KEY; upload cannot proceed')
    print('LUMBERYARD_V2B_21_ENGINE_AND_ASSET_GATE_PASSED',sha,flush=True)
    portal.upload(package,NEW_VERSION,secret)
    indexed=NEW_VERSION in portal.portal_versions()
    state='publicly_indexed' if indexed else 'upload_accepted_index_pending'
    (root/'mod-portal-publication.json').write_text(json.dumps({
        'name':MOD_NAME,'version':NEW_VERSION,'factorio_version':'2.1','status':state,
        'sha256':sha,'url':f'https://mods.factorio.com/mod/{MOD_NAME}'
    },indent=2)+'\n')
    print('LUMBERYARD_V2B_PORTAL_'+state.upper(),flush=True)

if __name__=='__main__':main()
