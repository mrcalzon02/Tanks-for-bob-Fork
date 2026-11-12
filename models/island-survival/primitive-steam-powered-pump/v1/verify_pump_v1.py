#!/usr/bin/env python3
"""Independently reopen the genuine Tanks 1x2 Steam Pump Blender master."""
from __future__ import annotations
import hashlib
import json
import math
from pathlib import Path
import sys
import bpy

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
out=Path(sys.argv[sys.argv.index("--")+1]).resolve() if "--" in sys.argv else (
    ROOT/"models/island-survival/primitive-steam-powered-pump/generated-v1")
spec=json.loads((HERE/"contract.json").read_text(encoding="utf-8"))
report=json.loads((out/"build-report.json").read_text(encoding="utf-8"))
native=out/"pump-v1.blend"
def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
assert native.is_file() and Path(bpy.data.filepath).resolve()==native.resolve()
assert sha(native)==report["native_sha256"]
assert sha(ROOT/spec["fixture"]["path"])==report["fixture_sha256"]
assert sha(ROOT/spec["fmpl_pbr_donor"]["path"])==report["pbr_donor_sha256"]
assert report["schema"]=="tanks.primitive-steam-pump.v1.native-source"
assert report["dimensions"]==[1,2] and report["type"]=="pump"
assert report["name"]=="primitive-steam-powered-pump"
assert len(report["ports"])==2
assert report["render_count"]=={"none":0,"proof":8,"all":68}[report["render_mode"]]
scene=bpy.context.scene
model=bpy.data.objects.get("EXPORT | rotate primitive steam-powered pump, never camera")
assert model is not None and tuple(model["footprint_tiles"])==(1,2)
assert len([o for o in scene.objects if o.type=="CAMERA"])==1
assert scene.camera is not None and scene.camera.data.type=="ORTHO"
assert scene.camera.parent is None
assert abs(scene.camera.data.ortho_scale-3.85)<1e-6
assert abs(math.degrees(scene.camera.rotation_euler.x)-45)<1e-5
assert scene.render.film_transparent and scene.render.image_settings.color_mode=="RGBA"
ports=[o for o in scene.objects if o.name.startswith("PORT | ")]
assert len(ports)==4
assert len([o for o in ports if o.name.endswith(" | machine_collar")])==2
assert len([o for o in ports if o.name.endswith(" | machine_throat")])==2
assert all(o.parent is model and len(o.data.vertices)==256 for o in ports)
assert all(o["standard_sha256"]==report["fixture_sha256"] for o in ports)
assert {tuple(o["native_position"]) for o in ports}=={(0,-.75),(0,.75)}
assert {o["native_direction"] for o in ports}=={"north","south"}
assert {tuple(o["nominal_joint"]) for o in ports}=={(0,1,.36),(0,-1,.36)}
assert not any(o.name.startswith("GUIDE | ") or o.name.startswith("REF | ") for o in scene.objects)
assert any("ferrocrete" in n.lower() for n in report["fmpl_materials"])
wheel=bpy.data.objects.get("MOTION | keyed lateral 3D drive flywheel")
piston=bpy.data.objects.get("MOTION | vertically reciprocating piston")
link=bpy.data.objects.get("MOTION | hinged connecting rod")
assert wheel and piston and link
assert len([o for o in scene.objects if o.name.startswith("PIPE | ")])==2
assert any(o.name=="MOTION | cast bronze wheel rim" and o.type=="MESH" for o in scene.objects)
assert any(o.name=="GAUGE | slender true pointer" for o in scene.objects)
assert any(o.name=="SIGHT | clouded cylindrical glass" for o in scene.objects)
scene.frame_set(1)
bpy.context.view_layer.update()
base=[ob.matrix_world.copy() for ob in ports]
first=(float(wheel.rotation_euler.x),float(piston.location.z))
heights=[]
for frame in (1,7,13,25,49,73,91,97):
    scene.frame_set(frame)
    bpy.context.view_layer.update()
    heights.append(float(piston.location.z))
    for ob,ref in zip(ports,base):
        delta=max(abs(a-b) for rowA,rowB in zip(ob.matrix_world,ref)
                  for a,b in zip(rowA,rowB))
        assert delta<1e-6,(frame,ob.name,delta)
assert max(heights)-min(heights)>.15
scene.frame_set(97)
assert abs(math.sin(wheel.rotation_euler.x-first[0]))<1e-6
assert abs(piston.location.z-first[1])<1e-6
scene.frame_set(0)
for entry in report["renders"]:
    file=out/entry["file"]
    assert file.is_file() and sha(file)==entry["sha256"]
assert report["game_integrated"] is False and report["owner_visual_approved"] is False
receipt={
 "schema":"tanks.primitive-steam-pump.v1.native-reopen-qa",
 "passed":True,
 "native_sha256":sha(native),
 "full_bore_rigid_mesh_count":4,
 "mating_vertices_each":256,
 "native_positions":[[0,-.75],[0,.75]],
 "mating_ground_joints":[[0,1,.36],[0,-1,.36]],
 "piston_movement_bu":max(heights)-min(heights),
 "loop_97_matches_1":True,
 "single_45_degree_ortho":True,
 "actual_blender_frame_count":len(report["renders"]),
 "game_integrated":False,"owner_visual_approved":False
}
(out/"native-reopen-qa.json").write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
print("TANKS_PUMP_NATIVE_REOPEN_PASS",json.dumps(receipt),flush=True)
