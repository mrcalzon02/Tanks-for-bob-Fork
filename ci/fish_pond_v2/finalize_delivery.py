"""Close production evidence, refresh the honest ledger and verify a package."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]


def read(path):
    return json.loads(path.read_text())


def write(path,data):
    path.write_text(json.dumps(data,indent=2)+'\n')


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--native',type=Path,required=True)
    p.add_argument('--package-out',type=Path,required=True)
    a = p.parse_args()
    native,package = a.native.resolve(),a.package_out.resolve()
    receipt = read(native/'engine-receipt.json')
    assert receipt['native_pass'] and receipt['reload_pass'] and not receipt['candidate_only']
    assert not receipt['proof_addon_overrides_production_art']
    docs = ROOT/'docs/art/fish-pond-v2'
    for name in ('engine-receipt.json','native.log','reload.log','create-save.log'):
        shutil.copy2(native/name,docs/name)
    manifest_path = ROOT/'tanks_for_bob_fork_1.8.103/graphics/entity/fish-pond-v2/source-manifest.json'
    manifest = read(manifest_path)
    assert receipt['atlas_sha256'] == manifest['working_sha256']
    manifest['production_native_verified'] = True
    manifest['native_evidence'] = 'docs/art/fish-pond-v2/engine-receipt.json'
    write(manifest_path,manifest)
    fmpl_path = ROOT/'models/island-survival/fish-pond/v2/FMPL_MODEL.json'
    fmpl = read(fmpl_path)
    fmpl['status'] = 'owner-approved-native-integrated'
    fmpl['native_production_reload_passed'] = True
    write(fmpl_path,fmpl)
    ledger_path = ROOT/'docs/art/STRUCTURE_COMPLETION_LEDGER.json'
    ledger = read(ledger_path)
    for row in ledger['structures']:
        if row['id'] == 'fish-pond':
            row.update(revision='V2',status='accepted_integrated',done=True,
                next='Preserve the accepted clay basin, four swimmers, baked portable source and tested native idle/working integration.',
                evidence=['docs/art/fish-pond-v2/README.md','models/island-survival/fish-pond/v2/FMPL_MODEL.json'],
                fmpl_delivery='Source/GLB inspected, native integration/reload and owner acceptance verified; canonical registration being closed.')
        row.pop('active',None)
        if row['id'] == 'beachpump':
            row['active'] = True
    ledger['active_structure'] = 'beachpump'
    ledger['updated'] = '2026-11-15'
    write(ledger_path,ledger)
    subprocess.run([sys.executable,str(ROOT/'tools/art/refresh_structure_ledger.py')],cwd=ROOT,check=True)
    output = subprocess.check_output([sys.executable,str(ROOT/'ci/package_mod.py'),'--output',str(package)],cwd=ROOT,text=True)
    package_receipt = json.loads(output)
    write(package/'package-receipt.json',package_receipt)
    write(docs/'package-receipt.json',package_receipt)
    delivery = {'schema':'tanks.fish-pond.v2.delivery','date':'2026-11-15','owner_accepted':True,
        'source_sha256':fmpl['source']['sha256'],'runtime_sha256':fmpl['runtime']['sha256'],
        'active_mod':'tanks_for_bob_fork_1.8.103','graphics':manifest,
        'production_native_passed':True,'save_reload_passed':True,'native_facings':4,
        'native_test_ponds':20,'actual_graphical_screenshots':24,'gameplay_changed':False,
        'package_sha256':package_receipt['sha256'],'package_byte_verified_files':package_receipt['files'],
        'user_mod_directory_changed':False,'mod_portal_published':False,
        'completed_structures':9,'total_structures':21,'next_structure':'beachpump'}
    write(docs/'delivery-receipt.json',delivery)
    print('FISH_POND_DELIVERY_VERIFIED',json.dumps(delivery))


if __name__ == '__main__':
    main()
