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
    accepted = counts['accepted_integrated']
    advanced = counts['repair_required'] + counts['advanced_candidate']
    production = counts['in_progress'] + counts['rebuild_required']
    focus = next(r['name'] for r in rows if r['id'] == data['active_structure'])
    out = ['# Ongoing structure completion ledger', '',
           'Updated '+data['updated']+' against `'+data['baseline_commit']+'`.', '',
           data['scope']+'.', '', data['completion_policy'], '',
           f'**{accepted} accepted/integrated; {advanced} advanced with open work; {production} requiring substantial production. Current focus: {focus}.**', '',
           '| Structure | Latest known revision | Status | Remaining action |',
           '| --- | --- | --- | --- |']
    for r in rows:
        out.append('| '+r['name']+' | '+r['revision']+' | '+r['status'].replace('_',' ')+' | '+r['next']+' |')
    out += ['', '## FMPL delivery and acceptance', '',
            'For each unfinished structure: lock native dimensions and ports; author supported geometry and its surface plan; unwrap/bake model-specific materials; animate real mechanisms and prove loop/clearance; save and independently reopen the editable master; export and independently inspect the FMPL runtime artifact; render and actually view front/rear/close/clay and four production facings; pack true RGBA states/layers and atlases; validate native Factorio placement/working/stop/restart/save-reload; record visual disposition before replacement; publish and read back hashes.', '',
            'FMPL uses the canonical pinned library in `fmpl-consumer.json`; validate the actual capture profile and matrix against its camera authority. Export/registry receipt audit is pending for historical accepted assets and does not authorize their rebuild. Candidate art may be saved and reviewed while approval remains pending.', '',
            '## Continuation', '',
            'The goal is paused. Resume from docs/art/REMAINING_STRUCTURES_HANDOFF.md and begin with the owner-designated existing compressor for Steam-Compressor. Preserve all ten accepted assets; Beach Pump V12 underwater polish is deferred. Keep the unfamiliar Tanks condenser candidate held and uninstalled; actual recipes, not names, define function. Tech-Priests atmospheric condenser V24 is a separate machine. Keep rejected wheel studies held and lifting buckets upright. Reconcile remote HEAD and preserve concurrent work.', '',
            'Follow docs/art/OPERATIONAL_FINISH_POLICY.md: prioritize working animated integration and necessary operational checks, using judgment for close-enough visuals. Do not request routine promotion permission again or add cosmetic production cycles. Never fabricate specific owner visual approval or missing source/export receipts. Do not create extra CI workflows, change progression/balance, duplicate the workbench, or add Tech-Priests turret/vehicle work.', '',
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
