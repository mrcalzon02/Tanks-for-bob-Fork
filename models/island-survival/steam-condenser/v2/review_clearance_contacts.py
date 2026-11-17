"""Bind explicit contact adjudication to the complete, unfiltered source/GLB sweep."""
import json,re,sys,hashlib
from pathlib import Path
H=Path(__file__).resolve().parent;P=Path(sys.argv[1]);sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
families=json.loads((H/'reviewed-contact-families.json').read_text())['families']
reports={};keys=[]
for state,artifact,raw in [('source','steam-condenser-v2.blend','clearance-raw.json'),('runtime','steam-condenser-v2.glb','clearance-runtime-raw.json')]:
 d=json.loads((P/raw).read_text());assert d['sha256']==sha(P/artifact) and d['sampled_poses']==385
 reviewed={};unknown={}
 for pair,observed in d['pairs'].items():
  base=' <> '.join(sorted(re.sub(r'\.\d+$','',n.replace('CONDENSER | ','')) for n in pair.split(' <> ')))
  if base not in families:unknown[pair]=observed;continue
  reviewed[pair]={'reason':families[base],'raw_observation':observed}
 reports[state]={'artifact_sha256':d['sha256'],'raw_pairs':len(d['pairs']),'moving_pairs':sum(v['moving'] for v in d['pairs'].values()),'unknown':unknown,'reviewed':reviewed};keys.append(set(d['pairs']))
passed=not any(r['unknown'] for r in reports.values()) and keys[0]==keys[1]
(P/'clearance-review.json').write_text(json.dumps({'passed':passed,'source_and_runtime_pair_sets_match':keys[0]==keys[1],'sampled_poses_per_artifact':385,'continuous_collision_simulation':False,'reviewed_family_record_sha256':sha(H/'reviewed-contact-families.json'),'reports':reports},indent=2)+'\n')
print('CONTACT_REVIEW',passed,{k:{n:v for n,v in r.items() if n!='reviewed'} for k,r in reports.items()})
assert passed
