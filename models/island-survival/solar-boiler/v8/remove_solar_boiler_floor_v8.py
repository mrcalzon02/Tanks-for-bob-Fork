#!/usr/bin/env python3
"""Solar Boiler V8: remove ONLY V7's visible FMPL concrete floor slab and pavers.

Retain 3x2 Factorio footprint, all load-bearing support meshes, and the exact
verified V7 rig, keyed material effects, camera, valves and fluid sockets.
Native V7 source and renders remain immutable.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
SOLAR=HERE.parent
SOURCE=SOLAR/"generated-v7"/"solar-boiler-v7.blend"
SOURCE_REPORT=SOLAR/"generated-v7"/"build-report.json"
FRAMES=tuple(range(1,92,6))
SEAM=97
YAW=(0,90,180,270)
PORTS=("water-west","water-east","steam-north")
PAD="FMPL | 3x2 ferrocrete continuous equipment pad"
PAVER_PREFIX="FMPL | laid exterior concrete paver"

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def is_floor_name(name):
    return name==PAD or name.startswith(PAVER_PREFIX)

def self_check():
    assert len(FRAMES)==16 and FRAMES[0]==1 and FRAMES[-1]==91
    assert SOURCE.is_file() and SOURCE_REPORT.is_file()
    prior=json.loads(SOURCE_REPORT.read_text())
    assert sha(SOURCE)==prior["native_sha256"],"V7 donor has changed"
    assert prior["render_count"]==68 and prior["footprint"]==[3,2]
    assert prior["fixed_ground_count"]==31
    assert not prior["visual_approved"] and not prior["game_integrated"]
    targets=[n for n in prior["grounded_objects"] if is_floor_name(n)]
    assert len([n for n in targets if n==PAD])==1
    assert len([n for n in targets if n.startswith(PAVER_PREFIX)])==10
    assert len(targets)==11 and len(prior["grounded_objects"])-len(targets)==20
    print("SOLAR_V8_FLOOR_REMOVAL_CONTRACT_PASS",len(targets),flush=True)
    return prior,targets

def camera_record(scene):
    cam=scene.camera
    return {"name":cam.name,"matrix_world":[list(row) for row in cam.matrix_world],
            "type":cam.data.type,"ortho_scale":cam.data.ortho_scale,
            "shift_x":cam.data.shift_x,"shift_y":cam.data.shift_y,
            "resolution":[scene.render.resolution_x,scene.render.resolution_y]}

def edit(bpy,prior,targets):
    scene=bpy.context.scene
    root=bpy.data.objects["EXPORT | rotate Solar Boiler model, never camera"]
    rig=bpy.data.objects[prior["rumble_rig"]]
    scene.frame_set(0);root.rotation_euler.z=0
    bpy.context.view_layer.update()
    assert rig.parent is root and camera_record(scene)==prior["camera"]
    before={obj.name for obj in bpy.data.objects}
    for name in targets:
        ob=bpy.data.objects[name]
        assert ob.type=="MESH" and ob.parent is root and ob.get("v7_ground_locked")
        bpy.data.objects.remove(ob,do_unlink=True)
    after={obj.name for obj in bpy.data.objects}
    assert before-after==set(targets),"V8 changed an object outside the approved pad and pavers"
    assert not any(is_floor_name(obj.name) for obj in bpy.data.objects)
    supports=[n for n in prior["grounded_objects"] if n not in targets]
    assert len(supports)==20
    assert all(bpy.data.objects[n].parent is root and bpy.data.objects[n].get("v7_ground_locked")
               for n in supports)
    assert len(prior["flexed_wood_pipe_planks"])==33
    assert all(bpy.data.objects[n].parent is root for n in prior["flexed_wood_pipe_planks"])
    assert all(bpy.data.objects[n].parent is rig for n in prior["glass_receiver_names"])
    for key in PORTS:
        assert bpy.data.objects[f"PORT | {key} | full machine collar"].parent is root
        assert bpy.data.objects[f"REF | {key} | near matching collar"].parent is root
    assert bpy.data.objects["SOLAR | west | adjustable trough pivot"].parent is rig
    assert bpy.data.objects["SOLAR | east | adjustable trough pivot"].parent is rig
    assert list(root["footprint_tiles"])==[3,2]
    scene["solar_boiler_revision"]="V8 floorless V7: remove ONLY ferrocrete pad and ten pavers"
    scene["v8_v7_sha256"]=sha(SOURCE)
    scene["game_integration"]=False
    scene.frame_set(0);root.rotation_euler.z=0
    bpy.context.view_layer.update()
    assert camera_record(scene)==prior["camera"]
    return root,rig,supports

def render(bpy,scene,out,filename,frame):
    scene.frame_set(frame)
    bpy.context.view_layer.update()
    scene.render.filepath=str(out/filename)
    print("SOLAR_V8_CYCLES",filename,frame,flush=True)
    bpy.ops.render.render(write_still=True)
    return {"file":filename,"frame":frame,"sha256":sha(out/filename)}

def build(args):
    import bpy
    prior,targets=self_check()
    if args.output.exists() and any(args.output.iterdir()):
        raise FileExistsError("V8 will not overwrite existing render proof")
    bpy.ops.wm.open_mainfile(filepath=str(SOURCE))
    scene=bpy.context.scene
    root,rig,supports=edit(bpy,prior,targets)
    scene.render.film_transparent=True
    scene.render.image_settings.color_mode="RGBA"
    scene.render.fps=8
    scene.frame_start=0;scene.frame_end=SEAM
    scene.cycles.samples=args.samples
    args.output.mkdir(parents=True,exist_ok=True)
    native=args.output/"solar-boiler-v8.blend"
    bpy.ops.file.pack_all()
    bpy.ops.wm.save_as_mainfile(filepath=str(native),compress=True,check_existing=False)
    report={
        "schema":"tanks.solar-boiler.v8.floorless-grounded",
        "native_sha256":sha(native),"v7_source_sha256":sha(SOURCE),
        "footprint":[3,2],"camera":prior["camera"],"fps":8,
        "directions":list(YAW),"frames":list(FRAMES),"seam":SEAM,
        "removed_floor_objects":targets,"removed_floor_count":len(targets),
        "retained_grounded_supports":supports,"retained_support_count":len(supports),
        "rumble_rig":rig.name,"flexed_wood_pipe_planks":prior["flexed_wood_pipe_planks"],
        "glass_receiver_names":prior["glass_receiver_names"],
        "steam_objects":prior["steam_objects"],
        "native_port_interfaces_fixed":list(PORTS),
        "visual_approved":False,"game_integrated":False,"renders":[]}
    manifest=args.output/"build-report.json"
    manifest.write_text(json.dumps(report,indent=2)+"\n")
    if args.render=="none":return
    for state in ("idle","working"):
        for d,yaw in enumerate(YAW):
            root.rotation_euler.z=math.radians(yaw)
            seq=(-1,) if state=="idle" else range(16)
            for k in seq:
                frame=0 if k<0 else FRAMES[k]
                filename=(f"idle-d{d:02d}.png" if k<0 else
                          f"working-d{d:02d}-f{k:03d}.png")
                item=render(bpy,scene,args.output,filename,frame)
                item.update({"direction":d,"state":state,"index":k})
                report["renders"].append(item)
                manifest.write_text(json.dumps(report,indent=2)+"\n")
    root.rotation_euler.z=0;scene.frame_set(0)
    bpy.context.view_layer.update()
    report["render_count"]=len(report["renders"])
    assert report["render_count"]==68
    manifest.write_text(json.dumps(report,indent=2)+"\n")
    assert sha(SOURCE)==prior["native_sha256"]
    print("SOLAR_V8_FLOORLESS_68_CYCLES_RENDERS_PASS",flush=True)

def main():
    if "--self-check" in sys.argv:
        self_check();return
    p=argparse.ArgumentParser()
    p.add_argument("--output",type=Path,required=True)
    p.add_argument("--render",choices=("none","all"),default="all")
    p.add_argument("--samples",type=int,default=24)
    a=p.parse_args(sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else sys.argv[1:])
    if not 4<=a.samples<=48:raise ValueError("Bounded Cycles samples 4-48 only")
    build(a)
if __name__=="__main__":main()
