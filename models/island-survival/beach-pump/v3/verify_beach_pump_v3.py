#!/usr/bin/env python3
"""Independent native .blend reopen verification of the actual V2 screw-wheel pump."""
from __future__ import annotations
import hashlib,json,math,sys
from pathlib import Path
import bpy

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
FRAMES=tuple(range(1,92,6))
OUT=Path(sys.argv[sys.argv.index("--")+1]).resolve() if "--" in sys.argv else (ROOT/"models/island-survival/beach-pump/generated-v2")
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
report=json.loads((OUT/"build-report.json").read_text(encoding="utf-8"))
contract=json.loads((HERE.parent/"v2/contract.json").read_text(encoding="utf-8"))
native=OUT/"beach-pump-v3.blend"
assert native.is_file() and Path(bpy.data.filepath).resolve()==native.resolve()
assert sha(native)==report["native_sha256"]
assert report["schema"]=="tanks.beach-pump.v3.archimedes-native-blender"
assert report["donor_builder_blob_sha1"]==contract["v1_builder"]["git_blob_sha1"]
assert report["native_offshore"]==contract["lock"]
assert report["render_mode"] in ("none","proof","all")
assert report["render_count"]=={"none":0,"proof":8,"all":68}[report["render_mode"]]
assert tuple(report["four_facings"])==(0,90,180,270)
assert tuple(report["working_frames"])==FRAMES
assert not report["game_integrated"] and not report["human_visual_approved"]
scene=bpy.context.scene
assert scene.get("native_offshore_behavior")=="unchanged: direct water from adjacent shoreline"
assert scene.render.film_transparent and scene.render.image_settings.color_mode=="RGBA"
assert scene.camera and scene.camera.parent is None and scene.camera.data.type=="ORTHO"
assert abs(scene.camera.data.ortho_scale-3.75)<1e-5
assert abs(math.degrees(scene.camera.rotation_euler.x)-45)<1e-5
assert len([o for o in scene.objects if o.type=="CAMERA"])==1
root=bpy.data.objects.get("EXPORT | rotate beachpump not camera")
assert root and root.parent is None
assert root["factorio_prototype"]=="offshore-pump/beachpump"
assert sum(o.name.startswith("ANCHOR | separate") for o in scene.objects)==4
assert not any("slab" in o.name.lower() for o in scene.objects)
assert not any("BEACH TEMP FIXTURE" in o.name or "REF |" in o.name for o in scene.objects)
ports=[o for o in scene.objects if o.name.startswith("PORT | south output |")]
assert len(ports)==2 and all(o.parent is root for o in ports)
assert {o.name for o in ports}=={
    "PORT | south output | machine_collar","PORT | south output | machine_throat"}
assert all(len(o.data.vertices)==256 for o in ports)
assert {tuple(o["native_cell"]) for o in ports}=={(0,.25)}
assert {tuple(o["blender_joint"]) for o in ports}=={(0,-.49,.36)}
assert not any(o.name.startswith(("MOTION | hand-hewn","MOTION | wet leather",
                                 "MOTION | wave-actuated")) for o in scene.objects)
helix=bpy.data.objects.get("SCREW | exposed 3-turn bronze helical flight")
assert helix and helix.type=="MESH" and len(helix.data.vertices)>=500
assert helix.get("source_object_type")=="REAL_EDITABLE_HELIX"
assert helix.get("pitch_turns")==3
wheel=bpy.data.objects.get("MOTION | full bucket waterwheel shaft")
rotor=bpy.data.objects.get("MOTION | keyed Archimedes screw rotation")
assert wheel and rotor and wheel.parent is root
assert rotor.parent is bpy.data.objects.get("SCREW | diagonal shaft carrier (fixed)")
assert sum(o.name.startswith("WHEEL | cupped tapered paddle") for o in scene.objects)==8
assert sum(o.name.startswith("WHEEL | chunky bucket paddle") for o in scene.objects)==0
assert sum(o.name.startswith("DOCK | narrow separated driftwood plank") for o in scene.objects)==5
assert sum(o.name.startswith("WATER | running stream glint") for o in scene.objects)==4
assert bpy.data.objects.get("SCREW | smooth rolled outer flight rim")
assert sum(o.name.startswith("WHEEL | heavy wooden spoke") for o in scene.objects)==8
for name in ("CRANK | oversized side offset forged lever",
             "CRANK | large rotating external handle",
             "DRIVE | exposed rigid wheel-to-screw gearbox input",
             "TROUGH | continuous open wooden gutter bottom",
             "TROUGH | clearly visible blue-green water ribbon",
             "OUTPUT | permanent water run to native south pipe mouth",
             "SCREW | submerged open intake cage",
             "SUMP | blue-green collected flow"):
    assert bpy.data.objects.get(name) is not None,name
pockets=[o for o in scene.objects if o.name.startswith("WATER | visibly rising screw pocket")]
spill=[o for o in scene.objects if o.name.startswith("WATER | cascading trough-wheel spill")]
assert len(pockets)==6 and len(spill)==6
assert all(o.parent is rotor for o in pockets)
assert all(o.parent is root for o in spill)
scene.frame_set(1)
bpy.context.view_layer.update()
port_mats=[o.matrix_world.copy() for o in ports]
first_w=float(wheel.rotation_euler.x)
first_s=float(rotor.rotation_euler.z)
for fr in (7,13,25,43,49,73,85,91,97):
    scene.frame_set(fr);bpy.context.view_layer.update()
    for ob,ref in zip(ports,port_mats):
        difference=max(abs(a-b) for r,s in zip(ob.matrix_world,ref) for a,b in zip(r,s))
        assert difference<1e-6,(ob.name,fr,difference)
scene.frame_set(97)
assert abs(math.sin(wheel.rotation_euler.x-first_w))<1e-6
assert abs(math.sin(rotor.rotation_euler.z-first_s))<1e-6
scene.frame_set(1)
crank_first=bpy.data.objects["CRANK | large rotating external handle"].matrix_world.copy()
glint_first=bpy.data.objects["WATER | running stream glint 00"].matrix_world.copy()
scene.frame_set(7)
crank_second=bpy.data.objects["CRANK | large rotating external handle"].matrix_world.copy()
glint_second=bpy.data.objects["WATER | running stream glint 00"].matrix_world.copy()
def distance(a,b):
    return max(abs(x-y) for ra,rb in zip(a,b) for x,y in zip(ra,rb))
assert distance(crank_first,crank_second)>.01
assert distance(glint_first,glint_second)>.01
assert abs((wheel.rotation_euler.x-first_w)+math.pi/8)<1e-5
assert abs((rotor.rotation_euler.z-first_s)-math.pi/8)<1e-5
scene.frame_set(0)
for row in report["renders"]:
    p=OUT/row["file"]
    assert p.is_file() and sha(p)==row["sha256"],row["file"]
proof={
 "schema":"tanks.beach-pump.v3.independent-native-qa",
 "passed":True,
 "native_sha256":report["native_sha256"],
 "actual_blender_frames":len(report["renders"]),
 "real_helix_mesh_vertices":len(helix.data.vertices),
 "water_wheel_spokes":8,"water_wheel_paddles":8,
 "large_eccentric_side_crank":True,
 "linked_screw_and_wheel_rotation":True,
 "original_rocker_removed":True,
 "water_pockets":6,"wheel_cascade_droplets":6,
 "cupped_bucket_meshes":8,"exposed_dock_planks":5,
 "animated_trough_glints":4,"crank_and_water_moved_between_frames":True,
 "fixed_native_port_meshes":2,
 "fixed_port_vertices_each":256,
 "port_max_drift_bu":0,
 "native_south_output":[0,.25],
 "source_offset":[0,-1],
 "gameplay_original_rate_per_tick":0.01,
 "frame97_matches_frame1":True,
 "one_45_degree_ortho_camera":True,
 "game_integrated":False,"human_visual_approved":False
}
(OUT/"native-reopen-qa.json").write_text(json.dumps(proof,indent=2)+"\n",encoding="utf-8")
print("BEACH_PUMP_V3_ARCHIMEDES_NATIVE_REOPEN_PASS",json.dumps(proof),flush=True)
