#!/usr/bin/env python3
"""Minimal OBJ and material checks for the campfire refinement."""
from pathlib import Path
import hashlib, math
root=Path(__file__).resolve().parent
obj=root/'campfire-refined.obj'
mtl=root/'campfire-refined.mtl'
verts=[]; faces=[]; used=set(); groups=set(); m=None;g=None
for line in obj.read_text().splitlines():
    p=line.strip().split()
    if not p:continue
    if p[0]=='v':
        xyz=tuple(map(float,p[1:]));assert len(xyz)==3 and all(math.isfinite(k) for k in xyz);verts.append(xyz)
    elif p[0]=='usemtl': m=p[1];used.add(m)
    elif p[0]=='g':g=p[1];groups.add(g)
    elif p[0]=='f':
        idx=[int(i.split('/')[0]) for i in p[1:]]
        assert len(idx)==3 and len(set(idx))==3 and all(1<=i<=len(verts) for i in idx)
        assert m and g
        faces.append(idx)
mats={p.split()[1] for p in mtl.read_text().splitlines() if p.startswith('newmtl ')}
assert used<=mats,sorted(used-mats)
assert len(verts)>500 and len(faces)>500
assert len(groups)>20
assert all(-1.6<=v[i]<=1.6 for v in verts for i in [0,1])
assert all(0<=v[2]<=1.8 for v in verts)
assert any(x.startswith('stone_') for x in groups)
assert any(x.startswith('cross_log_') for x in groups)
assert any(x.startswith('flame_tongue_') for x in groups)
print(f'PASS | vertices={len(verts)} faces={len(faces)} groups={len(groups)} materials={len(used)} | sha256={hashlib.sha256(obj.read_bytes()).hexdigest()}')
