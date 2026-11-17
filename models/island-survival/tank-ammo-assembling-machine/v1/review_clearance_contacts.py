"""Adjudicate only actual fitted drive contacts; preserve every raw pair."""
from pathlib import Path
import json,sys
P=Path(sys.argv[1]);s=json.loads((P/'clearance-raw.json').read_text());t=json.loads((P/'clearance-runtime-raw.json').read_text());assert set(s['pairs'])==set(t['pairs'])
allowed={'AMMO | motor to press leather belt':{'AMMO | motor drive pulley leather contact','AMMO | press reduction pulley leather contact'},'AMMO | upper cross-shaft leather belt':{'AMMO | press transfer pulley leather contact','AMMO | mixing upper transfer pulley leather contact'},'AMMO | rear agitator leather belt':{'AMMO | mixing upper drop pulley leather contact','AMMO | agitator driven pulley leather contact'}}
reasons={};bad={}
for pair,record in s['pairs'].items():
 if not record['moving']:continue
 a,b=pair.split(' <> ');owners=s['motion_owners']
 if owners[a] and owners[a]==owners[b]:reasons[pair]='Seated fixed surfaces inside a single rigid rotor/crank/ram/link/agitator assembly. Individual moving joints and clearances checked independently.'
 elif b in allowed.get(a,set()) or a in allowed.get(b,set()):reasons[pair]='Leather band meets its actual rotating pulley running surface. Separate flanges, bearings, frame and neighbouring mechanisms remain clear.'
 else:bad[pair]=record
result=dict(passed=not bad,source_sha256=s['sha256'],runtime_sha256=t['sha256'],poses_per_artifact=385,source_and_actual_glb_pair_sets_agree=True,reviewed_intentional_animated_contacts=reasons,unresolved_animated_crossings=bad,scope='All fixed mesh pairs once, every moving mesh against the full machine at 193 keys plus 192 half-frames independently in source and GLB.',limitations=['Sampled clearance, not continuous rigid-body simulation.','Belt surfaces are fixed running paths; pulleys and rigid shafts are animated. Grain travel on the leather is not simulated.'],owner_visual_approved=False)
(P/'clearance-review.json').write_text(json.dumps(result,indent=2)+'\n');assert result['passed'],bad;print('AMMO SOURCE/EXPORT CLEARANCE PASS',len(reasons),'intentional moving contact pairs')
