"""Save the current structure-production state without running new modeling."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/art/checkpoint-2026-11-16'
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def write(path,data): path.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
def main():
    OUT.mkdir(parents=True,exist_ok=True)
    source=ROOT/'tanks_for_bob_fork_1.8.104'
    native=ROOT/'build/tanks-alignment-final104'
    assert json.loads((source/'info.json').read_text())['version']=='1.8.104'
    differences=[]
    for file in source.rglob('*'):
        if not file.is_file():continue
        copy=native/'mods'/source.name/file.relative_to(source)
        if not copy.is_file() or sha(copy)!=sha(file):differences.append(file.relative_to(source).as_posix())
    native_receipt=json.loads((native/'receipt.json').read_text())
    assert native_receipt['native_grid_connections_passed'] and native_receipt['source_version']=='1.8.104'
    write(OUT/'alignment-receipt.json',native_receipt)
    verification={'active_source':source.name,'source_matches_existing_native_test_copy':not differences,
      'differences_from_test_copy':differences,'native_grid_connections':native_receipt['player_grid_connections'],
      'genuine_graphical_capture_available':native_receipt['graphical_captured'],
      'visual_review_not_inferred':True,'goal_status':'paused','new_modeling_performed_for_checkpoint':False}
    for directory,name in [('local-art-full-pack-check01','verification-receipt.json'),
                           ('local-art-full-pack-check01','actual-user-launch-receipt.json'),
                           ('local-art-install-20261115-01','installation-receipt.json')]:
        receipt=ROOT/'build'/directory/name
        if receipt.is_file():shutil.copy2(receipt,OUT/name)
    write(OUT/'verification.json',verification)
    groups={
      'models/island-survival/stone-water-wheel/candidates':'Retained rejected/held studies; upright buckets required; not installed.',
      'models/island-survival/primitive-steam-powered-pump/candidates':'V3-production02/atlases02 accepted; earlier pilot/production01/atlases01 preserved as superseded.',
      'models/island-survival/fish-pond/candidates':'V2-production01/atlases01 accepted; pilot02/03/04 preserved as development history.',
      'models/island-survival/steam-condenser/candidates':'Unapproved V1 development source/export/atlases; not installed or owner accepted.',
      'tanks_for_bob_fork_1.8.104':'Current versioned source; preserve operational art and alignment corrections.'}
    inventory=[]
    for group,status in groups.items():
        base=ROOT/group
        for file in sorted(base.rglob('*')):
            if file.is_file():inventory.append({'path':file.relative_to(ROOT).as_posix(),
                'bytes':file.stat().st_size,'sha256':sha(file),'status':status})
    write(OUT/'asset-inventory.json',{'schema':'tanks.structure-checkpoint.v1','files':inventory})
    ledger_path=ROOT/'docs/art/STRUCTURE_COMPLETION_LEDGER.json'
    ledger=json.loads(ledger_path.read_text())
    ledger['updated']='2026-11-16';ledger['active_source']=source.name
    ledger['active_structure']='Steam-Compressor';ledger['production_state']='paused; handoff prepared'
    for row in ledger['structures']:
        row.pop('active',None)
        if row['id']=='Steam-Compressor':
            row['active']=True
            row['next']='FIRST on resume: reuse the owner-designated half-finished compressor for the existing Steam-Compressor. Locate its editable master, preserve useful mechanism, and finish primitive low-tech construction and canister charging/release integration. See REMAINING_STRUCTURES_HANDOFF.md.'
            row['evidence'].append('docs/art/REMAINING_STRUCTURES_HANDOFF.md') if 'docs/art/REMAINING_STRUCTURES_HANDOFF.md' not in row['evidence'] else None
        if row['id']=='steam-condenser':
            row['revision']='Tanks V1 unapproved candidate held; native entity exists'
            row['next']='Keep the unfamiliar V1 candidate unapproved and uninstalled. The actual placeable steam-condenser exists; Steam-condenserA consumes wood and steam and returns stone/industrial waste. Do not infer water output or borrow Tech-Priests atmospheric-condenser V24. Resume only from actual function and the owner’s construction brief.'
        if row['id'] in ('fish-pond','solar-boiler','primitive-steam-powered-pump'):
            evidence='docs/art/checkpoint-2026-11-16/verification.json'
            if evidence not in row['evidence']:row['evidence'].append(evidence)
    write(ledger_path,ledger)
    subprocess.run(['python',str(ROOT/'tools/art/refresh_structure_ledger.py')],cwd=ROOT,check=True)
    print(json.dumps({'saved_files':len(inventory),'saved_MB':round(sum(x['bytes'] for x in inventory)/1e6,1),
        'verification':verification,'open_structures':[r['id'] for r in ledger['structures'] if not r['done']]},indent=2))
if __name__=='__main__':main()
