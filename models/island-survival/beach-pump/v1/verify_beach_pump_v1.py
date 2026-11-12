#!/usr/bin/env python3
"""Independent genuine Blender reopen for shoreline Beach Pump V1."""
from __future__ import annotations
import hashlib,json,math,sys
from pathlib import Path
import bpy

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
OUT=Path(sys.argv[sys.argv.index("--")+1]).resolve() if "--" in sys.argv else (
    ROOT/"models/island-survival/beach-pump/generated-v1")
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
contract=json.loads((HERE/"contract.json").read_text(encoding="utf-8"))
report=json.loads((OUT/"build-report.json").read_text(encoding="utf-8"))
native=OUT/"beach-pump-v1.blend"
assert native.is_file() and Path(bpy.data.filepath).resolve()==native
assert sha(native)==report["master_sha256"]
assert report["schema"]=="tanks.beach-pump.v1.native-blender"
assert report["asset"]=="beachpump"
assert report["factorio_prototype"]=="offshore-pump/beachpump"
assert report["prototype"]["selection_box_native"]==[[-.6,-1.49],[.6,.49]]
assert report["prototype"]["fluid_source_offset"]==[0,-1]
assert report["prototype"]["output_connection"]["position_native"]==[0,.25]
assert report["prototype"]["energy_source"]=="void"
assert report["render_count"]=={"none":0,"proof":8,"all":68}[report["render_mode"]]
assert sha(ROOT/contract["fixture"]["path"])==report["fluid_fixture_sha256"]
assert sha(ROOT/contract["pbr_donor"]["path"])==report["pbr_material_donor_sha256"]
assert any("ferrocrete" in n.lower() for n in report["fmpl_materials"])
scene=bpy.context.scene
root=bpy.data.objects.get("EXPORT | rotate beachpump not camera")
assert root is not None and root.parent is None
assert root["factorio_prototype"]=="offshore-pump/beachpump"
assert tuple(root["native_selection_box"][0])==(-.6,-1.49)
assert tuple(root["native_selection_box"][1])==(.6,.49)
assert len([o for o in scene.objects if o.type=="CAMERA"])==1
assert scene.camera.parent is None and scene.camera.data.type=="ORTHO"
assert abs(scene.camera.data.ortho_scale-3.75)<1e-6
assert abs(math.degrees(scene.camera.rotation_euler.x)-45)<1e-5
assert scene.render.film_transparent and scene.render.image_settings.color_mode=="RGBA"
assert len([o for o in scene.objects if o.name.startswith("ANCHOR | separate")])==4
assert len([o for o in scene.objects if o.name.startswith("DOCK | narrow separated")])==8
assert not any("slab" in o.name.lower() for o in scene.objects)
assert not any("TEMP FIXTURE" in o.name or "REF |" in o.name for o in scene.objects)
ports=[o for o in scene.objects if o.name.startswith("PORT | south output |")]
assert len(ports)==2
assert {o.name.rsplit(" | ",1)[-1] for o in ports}=={"machine_collar","machine_throat"}
assert all(o.parent is root and len(o.data.vertices)==256 for o in ports)
assert all(o["reference_sha256"]==report["fluid_fixture_sha256"] for o in ports)
assert {tuple(o["native_cell"]) for o in ports}=={(0,.25)}
assert {tuple(o["blender_joint"]) for o in ports}=={(0,-.49,.36)}
assert {o["native_direction"] for o in ports}=={"south"}
names=("MOTION | hand-hewn twin-arm mechanical rocker",
       "MOTION | wave-actuated intake paddle pivot",
       "MOTION | wet leather diaphragm actuator",
       "MOTION | articulated rocker-to-diaphragm connecting rod",
       "MOTION | taut rocker-to-paddle rope",
       "MOTION | low-pressure dial needle")
for name in names:assert bpy.data.objects.get(name) is not None, name
assert bpy.data.objects.get("INTAKE | open iron grille nose") is not None
assert bpy.data.objects.get("OUTPUT | continuous fixed copper lifter from pump chamber") is not None
scene.frame_set(1)
bpy.context.view_layer.update()
first=[p.matrix_world.copy() for p in ports]
rocker=bpy.data.objects[names[0]]
wave=bpy.data.objects[names[1]]
bellows=bpy.data.objects[names[2]]
start=(rocker.rotation_euler.x,wave.rotation_euler.x,bellows.location.z)
motion=[]
for frame in (1,7,13,25,49,73,91,97):
    scene.frame_set(frame);bpy.context.view_layer.update()
    motion.append(float(bellows.location.z))
    for p,ref in zip(ports,first):
        error=max(abs(x-y) for a,b in zip(p.matrix_world,ref) for x,y in zip(a,b))
        assert error<1e-6,(frame,p.name,error)
assert max(motion)-min(motion)>.13
scene.frame_set(97)
assert abs(rocker.rotation_euler.x-start[0])<1e-6
assert abs(wave.rotation_euler.x-start[1])<1e-6
assert abs(bellows.location.z-start[2])<1e-6
scene.frame_set(0)
for record in report["renders"]:
    p=OUT/record["file"]
    assert p.is_file() and sha(p)==record["sha256"]
assert not report["game_integrated"] and not report["human_approved"]
qa={"schema":"tanks.beach-pump.v1.native-reopen-qa","passed":True,
    "source_sha256":report["master_sha256"],
    "real_blender_frame_count":len(report["renders"]),
    "fixed_one_full_bore_output":True,"port_meshes":2,"port_vertices_each":256,
    "native_output_position":[0,.25],"blender_visible_output_joint":[0,-.49,.36],
    "water_intake_native":[0,-1],"shoreline_offset_selection":True,
    "four_separate_stone_feet":True,"no_filled_concrete_pad":True,
    "stroke_bu":max(motion)-min(motion),"animation_loop_closed":True,
    "single_45_degree_camera":True,"game_integrated":False,
    "human_art_approved":False}
(OUT/"native-reopen-qa.json").write_text(
    json.dumps(qa,indent=2)+"\n",encoding="utf-8")
print("BEACH_PUMP_V1_INDEPENDENT_NATIVE_REOPEN_PASS",
      json.dumps(qa),flush=True)
