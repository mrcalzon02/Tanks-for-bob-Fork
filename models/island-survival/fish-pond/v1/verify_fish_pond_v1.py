#!/usr/bin/env python3
"""Blender native reopen verifier for Fish Pond V1 (not a log-only test)."""
from pathlib import Path
import hashlib
import json
import sys
import bpy
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
sys.path.insert(0,str(HERE))
from build_fish_pond_v1 import validate
output=ROOT/'models/island-survival/fish-pond/generated-v1'
report=json.loads((output/'build-report.json').read_text())
native=output/'fish-pond-v1.blend'
assert Path(bpy.data.filepath).resolve()==native.resolve()
assert hashlib.sha256(native.read_bytes()).hexdigest()==report['master_sha256']
source=ROOT/'models/island-survival/clay-pit/generated-v4c/clay-pit-v4c.blend'
assert hashlib.sha256(source.read_bytes()).hexdigest()==report['source_sha256']
assert validate(bpy)>=1
scene=bpy.context.scene
assert scene.render.film_transparent and scene.render.image_settings.color_mode=='RGBA'
assert scene.camera.data.type=='ORTHO'
assert abs(scene.camera.data.ortho_scale-3.30)<.01
fish=[o for o in scene.objects if o.name.startswith('POND | fish') and o.name.endswith('body')]
assert len(fish)==4
for body in fish:
    keys=body.data.shape_keys
    assert keys is not None and len(keys.key_blocks)==3
    stroke=keys.key_blocks['Tail stroke left']
    values=[]
    for frame in (1,7,13,19,97):
        scene.frame_set(frame)
        values.append(float(stroke.value))
    assert abs(values[0]-values[-1])<1e-4, values
    assert max(values)>0.95, values
print('FISH_POND_NATIVE_SAVE_REOPEN_PASS',report['master_sha256'],flush=True)
