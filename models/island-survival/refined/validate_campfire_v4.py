#!/usr/bin/env python3
"""Verify procedural campfire v4 OBJ topology, visible layers and determinism."""
from pathlib import Path
from collections import Counter
import hashlib, math, subprocess, sys, tempfile
root=Path(__file__).resolve().parent
obj=root/'campfire-refined-v4.obj'; mtl=root/'campfire-refined-v4.mtl'
assert obj.exists() and mtl.exists(), 'run build_campfire_v4.py first'
vertices=[];faces=[];used=set();group='';material='';bygroup=Counter()
for line in obj.read_text().splitlines():
 p=line.split()
 if not p: continue
 if p[0]=='v':
  v=tuple(map(float,p[1:]));assert len(v)==3 and all(math.isfinite(x) for x in v)
  vertices.append(v)
 elif p[0]=='g':group=p[1]
 elif p[0]=='usemtl':material=p[1];used.add(material)
 elif p[0]=='f':
  a,b,c=map(int,p[1:]);assert a!=b and b!=c and a!=c
  assert all(1<=j<=len(vertices) for j in (a,b,c))
  assert material and group
  faces.append((a,b,c));bygroup[group]+=1
assert len(vertices)>2000 and len(faces)>3000
assert len([k for k in bygroup if k.startswith('stone_')])>=13
assert len([k for k in bygroup if k.startswith('cross_log_')])>=20
assert len([k for k in bygroup if k.startswith('flame_tongue_')])>=6
assert all(-1.8<v[0]<1.8 and -1.8<v[1]<1.8 and 0<=v[2]<1.8 for v in vertices)
materials={p.split()[1] for p in mtl.read_text().splitlines() if p.startswith('newmtl ')}
assert used <= materials, sorted(used-materials)
with tempfile.TemporaryDirectory() as d:
 subprocess.run([sys.executable,str(root/'build_campfire_v4.py'),d],check=True,capture_output=True)
 for name in ['campfire-refined-v4.obj','campfire-refined-v4.mtl']:
  assert (root/name).read_bytes()==(Path(d)/name).read_bytes(), f'nondeterministic {name}'
print('PASS campfire_v4 | vertices=%d triangles=%d groups=%d materials=%d OBJ_SHA256=%s'%(len(vertices),len(faces),len(bygroup),len(used),hashlib.sha256(obj.read_bytes()).hexdigest()))
