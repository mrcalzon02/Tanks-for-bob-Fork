"""Enumerate intentional fitted joints and water/cam contacts; preserve raw inventory."""
from pathlib import Path
import json,sys
P=Path(sys.argv[1]);s=json.loads((P/'clearance-raw.json').read_text());t=json.loads((P/'clearance-runtime-raw.json').read_text());assert set(s['pairs'])==set(t['pairs'])
reasons={};bad={}
for pair,record in s['pairs'].items():
 if not record['moving']:continue
 a,b=pair.split(' <> ');owners=s['motion_owners']
 if owners[a] and owners[a]==owners[b]:reasons[pair]='Fixed surfaces within one rigid bucket, gate, or wheel assembly, including seated pin/rim and keyed spoke joints.'
 elif 'cam follower roller' in pair and 'fixed drain cam contact rail' in pair:reasons[pair]='Follower engages the fixed shaped cam to lift its side drain gate at the top of the lift.'
 elif any(word in pair for word in ('falling drain water','short draining water')):reasons[pair]='Controlled efflux joins the water jet/drop or meets the solid receiving race; intentional fluid/wall contact, not interpenetrating rigid machinery.'
 else:bad[pair]=record
result=dict(passed=not bad,source_sha256=s['sha256'],runtime_sha256=t['sha256'],poses_per_artifact=385,source_and_actual_glb_pair_sets_agree=True,reviewed_intentional_animated_contacts=reasons,unresolved_animated_crossings=bad,scope='All static pairs inventoried once. Every moving mesh against the entire assembly at 193 keys and 192 half-frames in source and independently reimported GLB.',limitations=['Sampled clearance, not continuous rigid-body simulation.','Water/wall contacts and rigid fitted joints are retained and individually enumerated.'],owner_visual_approved=False)
(P/'clearance-review.json').write_text(json.dumps(result,indent=2)+'\n');assert result['passed'],bad;print('WHEEL SOURCE/EXPORT CLEARANCE PASS',len(reasons),'intentional moving pairs')
