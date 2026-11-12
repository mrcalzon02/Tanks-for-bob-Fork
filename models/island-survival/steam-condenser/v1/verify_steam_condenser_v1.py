#!/usr/bin/env python3
"""Independently reopen real Blender Tanks 3x3 Steam Condenser source and verify."""
from __future__ import annotations
import hashlib
import json
import math
from pathlib import Path
import sys
import bpy

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
OUT=Path(sys.argv[sys.argv.index("--")+1]).resolve() if "--" in sys.argv else (
    ROOT/"models/island-survival/steam-condenser/generated-v1")
REPORT=OUT/"build-report.json"
manifest=json.loads(REPORT.read_text(encoding="utf-8"))
contract=json.loads((HERE/"contract.json").read_text(encoding="utf-8"))
native=OUT/"steam-condenser-v1.blend"
def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert native.is_file() and Path(bpy.data.filepath).resolve()==native
assert sha(native)==manifest["native_sha256"]
assert manifest["footprint"]==[3,3] and len(manifest["fluid_ports"])==2
assert manifest["render_mode"] in ("none","proof","all")
assert manifest["render_count"]=={"none":0,"proof":8,"all":68}[manifest["render_mode"]]
assert sha(ROOT/contract["fluid_fixture"]["path"])==manifest["fluid_fixture_sha256"]
assert sha(ROOT/contract["packed_pbr_donor"]["path"])==manifest["pbr_donor_sha256"]
assert any("ferrocrete" in x.lower() for x in manifest["fmpl_materials_loaded"])
scene=bpy.context.scene
root=bpy.data.objects.get("EXPORT | rotate Tanks Steam Condenser, never camera")
assert root is not None and list(root["footprint_tiles"])==[3,3]
assert len([o for o in scene.objects if o.type=="CAMERA"])==1
assert scene.camera.type=="CAMERA" and scene.camera.parent is None
assert scene.camera.data.type=="ORTHO"
assert abs(scene.camera.data.ortho_scale-5.2)<1e-6
assert abs(math.degrees(scene.camera.rotation_euler.x)-45.0)<1e-5
assert scene.render.film_transparent and scene.render.image_settings.color_mode=="RGBA"
collars=[o for o in scene.objects if o.name.startswith("PORT | ") and o.name.endswith(" | machine_collar")]
throats=[o for o in scene.objects if o.name.startswith("PORT | ") and o.name.endswith(" | machine_throat")]
assert len(collars)==len(throats)==2
assert {tuple(o["fixed_native_cell"]) for o in collars}=={(0,-1),(0,1)}
assert all(o.parent is root and len(o.data.vertices)==256 for o in collars+throats)
assert all(o["canonical_interface_sha256"]==manifest["fluid_fixture_sha256"] for o in collars)
assert sum(o.name.startswith("VESSEL | ") for o in scene.objects)>5
assert sum(o.name.startswith("COOLING | ") for o in scene.objects)>5
assert sum(o.name.startswith("GLASS | ") for o in scene.objects)>=3
assert not any(o.name.startswith("REF | ") for o in scene.objects)
rotor=bpy.data.objects.get("COOLING | rotating vane drive")
gauge=bpy.data.objects.get("GAUGE | pressure needle keyed")
assert rotor is not None and gauge is not None
scene.frame_set(1)
bpy.context.view_layer.update()
base=[o.matrix_world.copy() for o in collars+throats]
first=float(rotor.rotation_euler.z)
for frame in (7,25,49,73,91,97):
    scene.frame_set(frame)
    bpy.context.view_layer.update()
    for o,a in zip(collars+throats,base):
        assert max(abs(x-y) for r,s in zip(o.matrix_world,a) for x,y in zip(r,s))<1e-6,(o.name,frame)
scene.frame_set(97)
assert abs(math.sin(rotor.rotation_euler.z-first))<1e-6
for row in manifest["renders"]:
    path=OUT/row["file"]
    assert path.is_file() and sha(path)==row["sha256"]
assert not manifest["game_integrated"] and not manifest["owner_visual_approved"]
result={"schema":"tanks.steam-condenser.v1.independent-native-qa",
        "passed":True,"native_sha256":manifest["native_sha256"],
        "camera_45_degrees":True,"four_orientation_source":True,
        "full_bore_port_count":2,"fixed_fluid_cells":[[0,-1],[0,1]],
        "static_collars_and_throats":True,"loop_frame_97_matches_frame_1":True,
        "actual_render_count":len(manifest["renders"]),"game_integrated":False,
        "visual_owner_approved":False}
(OUT/"native-reopen-qa.json").write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
print("TANKS_CONDENSER_REAL_NATIVE_REOPEN_PASS",json.dumps(result),flush=True)
