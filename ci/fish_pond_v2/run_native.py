"""Install candidate art only in an isolated disposable Factorio profile."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--binary', type=Path, required=True)
    parser.add_argument('--atlas', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--production', action='store_true')
    args = parser.parse_args()
    binary, atlas, out = args.binary.resolve(), args.atlas.resolve(), args.out.resolve()
    if out.exists():
        raise FileExistsError(out)
    receipt = json.loads((atlas/'atlas-manifest.json').read_text())
    assert receipt['verified'] and receipt['genuine_frames'] == 68
    version = subprocess.check_output([str(binary),'--version'], text=True).strip()
    assert '2.1.24' in version
    out.mkdir(parents=True)
    mods = out/'mods'
    mods.mkdir()
    shutil.copytree(ROOT/'tanks_for_bob_fork_1.8.103', mods/'tanks_for_bob_fork_1.8.103')
    addon = mods/'fish-pond-v2-proof_0.0.1'
    addon.mkdir()
    (addon/'info.json').write_text(json.dumps({'name':'fish-pond-v2-proof', 'version':'0.0.1',
        'title':'Temporary Fish Pond V2 proof', 'author':'local test', 'factorio_version':'2.1',
        'dependencies':['base','tanks_for_bob_fork']}))
    graphics = addon/'graphics'
    graphics.mkdir()
    for state in ('idle','working'):
        source = atlas/(state+'-256.png')
        assert hashlib.sha256(source.read_bytes()).hexdigest() == receipt['files'][source.name]['sha256']
        shutil.copy2(source, graphics/source.name)
    adapter = (ROOT/'models/island-survival/fish-pond/v2/graphics.lua').read_text()
    # Snapshot the fully normalized legacy prototype before the candidate
    # adapter, solely for an exact in-client before/after art comparison.
    baseline = 'local legacy=table.deepcopy(data.raw["assembling-machine"]["fish-pond"]); legacy.name="fish-pond-v2-legacy-reference"; data:extend({legacy})\n'
    if args.production:
        installed = ROOT/'tanks_for_bob_fork_1.8.103/graphics/entity/fish-pond-v2'
        for state in ('idle','working'):
            assert hashlib.sha256((installed/(state+'-256.png')).read_bytes()).hexdigest() == receipt['files'][state+'-256.png']['sha256']
        (addon/'data-final-fixes.lua').write_text('-- Production proof uses the active mod adapter without overriding it.\n')
    else:
        (addon/'data-final-fixes.lua').write_text(baseline+adapter)
    (addon/'data.lua').write_text('data:extend({{type="recipe",name="fish-pond-v2-fluid-proof",categories={"fishery"},enabled=true,energy_required=.5,ingredients={{type="fluid",name="water",amount=2}},results={{type="fluid",name="water",amount=2}}}})\n')
    shutil.copy2(HERE/'control.lua', addon/'control.lua')
    scenario = addon/'scenarios/proof'
    scenario.mkdir(parents=True)
    (scenario/'control.lua').write_text('-- Logic in proof addon.\n')
    (mods/'mod-list.json').write_text(json.dumps({'mods':[{'name':name,'enabled':name in ('base','tanks_for_bob_fork','fish-pond-v2-proof')} for name in ('base','elevated-rails','quality','recycler','space-age','tanks_for_bob_fork','fish-pond-v2-proof')]}))
    runtime = out/'runtime'
    runtime.mkdir()
    config = out/'config.ini'
    config.write_text('[path]\nread-data='+str(binary.parents[2]/'data')+'\nwrite-data='+str(runtime)+'\n')
    common = [str(binary),'--config',str(config),'--mod-directory',str(mods)]
    with (out/'native.log').open('w') as handle:
        result = subprocess.run(common+['--test-scenario','fish-pond-v2-proof/proof','--test-ticks','6060'], stdout=handle,stderr=subprocess.STDOUT,timeout=180)
    log = (out/'native.log').read_text(errors='replace')
    passed = result.returncode == 0 and 'FISH_POND_V2_NATIVE_PASS' in log
    report = {'engine':version,'exit_code':result.returncode,'native_pass':passed,'reload_pass':False,
        'candidate_only':not args.production,'production_source_art_changed':args.production,
        'proof_addon_overrides_production_art':not args.production,
        'atlas_sha256':receipt['files']['working-256.png']['sha256']}
    if passed:
        save = out/'fish-pond-v2-proof.zip'
        with (out/'create-save.log').open('w') as handle:
            created = subprocess.run(common+['--create',str(save)],stdout=handle,stderr=subprocess.STDOUT,timeout=180)
        if created.returncode == 0 and save.is_file():
            with (out/'reload.log').open('w') as handle:
                reloaded = subprocess.run(common+['--test-save',str(save),'--test-ticks','120'],stdout=handle,stderr=subprocess.STDOUT,timeout=180)
            report['reload_pass'] = reloaded.returncode == 0 and 'FISH_POND_V2_RELOAD_PASS' in (out/'reload.log').read_text(errors='replace')
    (out/'engine-receipt.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
    if not passed:
        print(log[-6000:])
        raise SystemExit(1)
    if not report['reload_pass']:
        raise SystemExit('Production states passed; save/reload incomplete')


if __name__ == '__main__':
    main()
