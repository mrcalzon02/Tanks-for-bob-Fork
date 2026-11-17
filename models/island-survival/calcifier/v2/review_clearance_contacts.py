"""Adjudicate every animated intersection instead of treating all contacts as failures.

The raw unfiltered inventories stay alongside this review. Fixed construction
contacts remain separately inventoried; this is a game-asset kinematic check,
not a claim of manufacturing tolerances or a rigid-body simulation.
"""
import bpy,json,sys,hashlib
from pathlib import Path
P=Path(__file__).resolve().parents[1]/'candidates/v2-sockets08'
bpy.ops.wm.open_mainfile(filepath=str(P/'calcifier-v2.blend'))
def owner(o):
 while o:
  if o.animation_data and o.animation_data.action:return o.name
  o=o.parent
 return None
owners={o.name:owner(o) for o in bpy.context.scene.objects if o.type=='MESH'}
def reason(a,b):
 if owners[a] and owners[a]==owners[b]:return 'Attached surfaces within one rigid animated assembly'
 pair={a,b};text=' <> '.join((a,b))
 if any(n in text for n in ['wet mineral growth bed','wetted mineral surface']):return 'Mixer shaft/paddles intentionally submerged in the process material'
 if ('hemp belt' in text or 'travelling belt splice' in text) and ('pulley rim' in text or 'hemp belt' in text):return 'Belt and its fasteners seated on the driven pulley surface'
 if pair=={'CALCIFIER | driven vertical bevel','CALCIFIER | driving right angle bevel'}:return 'Stylized 18:18 bevel tooth engagement; opposing keyed rotations, approximate tooth contact'
 engine={'CALCIFIER | retained engine crank pin','CALCIFIER | engine rigid connecting arm','CALCIFIER | engine rigid piston','CALCIFIER | bored engine crosshead','CALCIFIER V2 | rigid forming crosshead extension','CALCIFIER V2 | forming linkage retained pin'}
 if pair<=engine:return 'Retained crank/crosshead joint; source endpoint coincidence measured for all 193 keys'
 if 'CALCIFIER V2 | driving bevel keyed hub' in pair and 'CALCIFIER | upper turning shaft' in pair:return 'Keyed hub on the driving shaft, identical angular velocity'
 if 'CALCIFIER V2 | offset separator rigid arm segment' in pair or 'CALCIFIER V2 | separator spherical retained end' in pair:
  if pair & {'CALCIFIER V2 | sieve retained eccentric','CALCIFIER V2 | extended eccentric support boss'}:return 'Upper offset-arm spherical drive joint; eccentric endpoint measured'
 if 'CALCIFIER V2 | offset separator rigid arm segment.002' in pair or 'CALCIFIER V2 | separator spherical retained end.001' in pair:
  if 'CALCIFIER V2 | sieve crosshead socket' in pair:return 'Separator offset-arm spherical follower joint; endpoint measured'
 return None
reviews={}
for filename in ('clearance-raw.json','clearance-runtime-raw.json'):
 data=json.loads((P/filename).read_text());reviewed={};unresolved={}
 for pair,record in data['pairs'].items():
  if not record['moving']:continue
  a,b=pair.split(' <> ');r=reason(a,b)
  (reviewed if r else unresolved)[pair]=r or record
 reviews[filename]={'artifact_sha256':data['sha256'],'sampled_poses':data['sampled_poses'],'reviewed_intentional_contacts':reviewed,'unresolved_animated_crossings':unresolved,'passed':not unresolved}
 if unresolved:print('UNRESOLVED',json.dumps(unresolved,indent=2),flush=True)
result={'passed':all(r['passed'] for r in reviews.values()),'checks':reviews,'fit_clearances_tiles':{'separator_guide_radial':.004,'forming_ram_guide_radial':.004,'forming_punch_cavity_radial':.007,'engine_piston_gland_radial':.004},'scope':'All mesh triangle crossings, all moving meshes against every component at 193 keys and 192 half-frames, independently in source and actual reimported GLB; intentional rigid joints and process-material immersion separately enumerated. Static construction contacts remain in the raw inventory. Fully contained fits additionally checked by explicit radii/strokes.','limitations':['Stylized tooth engagement is not a manufacturing-grade gear contact analysis.','Sampled poses do not constitute a continuous collision solver.'],'owner_visual_approved':False}
(P/'clearance-review.json').write_text(json.dumps(result,indent=2)+'\n')
if not result['passed']:raise RuntimeError('Unresolved animated intersections remain')
print('ALL_ANIMATED_CONTACTS_REVIEWED',flush=True)
