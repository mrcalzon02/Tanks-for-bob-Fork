"""Validate all 21 structure identities and render the ongoing completion ledger."""
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LEDGER = ROOT / 'docs/art/STRUCTURE_COMPLETION_LEDGER.json'

def main():
    data = json.loads(LEDGER.read_text(encoding='utf-8'))
    designs = json.loads((ROOT/'models/island-survival/designs.json').read_text(encoding='utf-8'))
    rows = data['structures']
    ids = [r['id'] for r in rows]
    expected = {r.get('name', r.get('id')) for r in designs['models']}
    assert len(ids) == len(set(ids)) == 21 and set(ids) == expected, 'Missing/duplicate structure IDs'
    allowed = {'accepted_integrated','repair_required','advanced_candidate','in_progress','rebuild_required'}
    for r in rows:
        assert r['status'] in allowed and r['next'] and r['evidence'] and r['fmpl_delivery']
        assert r['done'] == (r['status'] == 'accepted_integrated'), r['id']
    counts = Counter(r['status'] for r in rows)
    out = ['# Ongoing structure completion ledger', '',
           'Updated '+data['updated']+' against `'+data['baseline_commit']+'`.', '',
           data['scope']+'.', '', data['completion_policy'], '',
           '**7 accepted/integrated; 4 advanced with open work; 10 requiring substantial production. Current focus: Primitive Steam-Powered Pump.**', '',
           '| Structure | Latest known revision | Status | Remaining action |',
           '| --- | --- | --- | --- |']
    for r in rows:
        out.append('| '+r['name']+' | '+r['revision']+' | '+r['status'].replace('_',' ')+' | '+r['next']+' |')
    out += ['', '## FMPL delivery and acceptance', '',
            'For each unfinished structure: lock native dimensions and ports; author supported geometry and its surface plan; unwrap/bake model-specific materials; animate real mechanisms and prove loop/clearance; save and independently reopen the editable master; export and independently inspect the FMPL runtime artifact; render and actually view front/rear/close/clay and four production facings; pack true RGBA states/layers and atlases; validate native Factorio placement/working/stop/restart/save-reload; record visual disposition before replacement; publish and read back hashes.', '',
            'FMPL uses the canonical pinned library in `fmpl-consumer.json`; validate the actual capture profile and matrix against its camera authority. Export/registry receipt audit is pending for historical accepted assets and does not authorize their rebuild. Candidate art may be saved and reviewed while approval remains pending.', '',
            '## Continuation', '',
            'Resume the existing Primitive Steam-Powered Pump artifact first: this is the pipe-to-pipe pump the owner identified. Keep the rejected wheel studies held; its separate shoreline intake remains in progression and any retained lifting buckets must stay upright. Recover exact Condenser V24 source/artifacts rather than duplicating them. Repair Beach Pump underwater occlusion while preserving owner-accepted placement. Finish Fish Pond export after reviewing its existing pilot, then continue through the remaining production targets. Reconcile the remote HEAD before publication and preserve concurrent work.', '',
            'Owner review gates replacement of art; it does not block independent modeling, candidate capture or other structures. Never mark missing review or uninspected output PASS. Do not create a new CI workflow per structure, change progression/balance, duplicate the workbench, or add Tech-Priests turret/vehicle work.', '',
            '## Evidence', '']
    for r in rows:
        links = []
        for p in r['evidence']:
            url = p if p.startswith('https:') else '../../'+p
            links.append('['+p.split('/')[-1]+']('+url+')')
        out.append('- '+r['name']+': '+', '.join(links))
    (ROOT/'docs/art/STRUCTURE_COMPLETION_LEDGER.md').write_text('\n'.join(out)+'\n',encoding='utf-8')
    print(json.dumps({'validated_structures':len(rows),'counts':dict(counts)},indent=2))

if __name__ == '__main__':
    main()
