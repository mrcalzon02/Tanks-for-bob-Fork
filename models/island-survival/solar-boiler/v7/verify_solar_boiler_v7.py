#!/usr/bin/env python3
"""Independent reopened native .blend QA for V7 grounded Solar Boiler."""
from __future__ import annotations
import argparse, hashlib, json, math, sys
from pathlib import Path
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from refine_solar_boiler_v7 import (SOURCE,SOURCE_REPORT,FRAMES,SEAM,PORTS,
    restrained_rumble,camera_record,sha,REQUIRED_GROUND)

def check(out):
    out=out.resolve()
    receipt=json.loads((out/"build-report.json").read_text())
    native=out/"solar-boiler-v7.blend"
    assert Path(bpy.data.filepath).resolve()==native
    assert receipt["native_sha256"]==sha(native)
    assert sha(SOURCE)==receipt["v6_source_sha256"]
    assert sha(SOURCE)==json.loads(SOURCE_REPORT.read_text())["native_sha256"]
    assert not receipt["visual_approved"] and not receipt["game_integrated"]
    scene=bpy.context.scene
    root=bpy.data.objects["EXPORT | rotate Solar Boiler model, never camera"]
    rig=bpy.data.objects[receipt["rumble_rig"]]
    scene.frame_set(0);root.rotation_euler.z=0
    bpy.context.view_layer.update()
    assert rig.parent is root and root.animation_data is None
    assert camera_record(scene)==receipt["camera"]
    assert scene.camera.parent is None and scene.camera.data.type=="ORTHO"
    assert len([o for o in bpy.data.objects if o.type=="CAMERA"])==1
    assert scene.render.fps==8 and scene.render.image_settings.color_mode=="RGBA"
    assert list(root["footprint_tiles"])==[3,2]
    anchored=[bpy.data.objects[n] for n in receipt["grounded_objects"]]
    assert len(anchored)==receipt["fixed_ground_count"]>=19
    for prefix in REQUIRED_GROUND:
        assert any(o.name.startswith(prefix) for o in anchored),prefix
    assert all(o.parent is root and o.get("v7_ground_locked") for o in anchored)
    assert bpy.data.objects["FMPL | 3x2 ferrocrete continuous equipment pad"] in anchored
    # Independent evaluated world matrices AND actual vertex coordinates.
    def world_verts(obj):
        eval_ob=obj.evaluated_get(bpy.context.evaluated_depsgraph_get())
        return [eval_ob.matrix_world@v.co for v in eval_ob.data.vertices]
    stable={o.name:world_verts(o) for o in anchored}
    # Baseline for exact attached native Factorio port rings.
    ports={p:world_verts(bpy.data.objects[f"PORT | {p} | full machine collar"])
           for p in PORTS}
    fixed_socket={}
    for name in receipt["flexed_wood_pipe_planks"]:
        ob=bpy.data.objects[name]
        sections=len(ob.data.vertices)//4
        idx=(0,1,2*sections,2*sections+1)
        fixed_socket[name]=(idx,[world_verts(ob)[i] for i in idx])
    assert len(fixed_socket)==33
    samples=(0,1,4,7,13,19,25,31,37,43,49,55,61,67,73,79,85,91,94,97)
    max_ground=0.0;max_socket=0.0
    for frame in samples:
        scene.frame_set(frame)
        bpy.context.view_layer.update()
        for o in anchored:
            actual=world_verts(o);baseline=stable[o.name]
            assert len(actual)==len(baseline)
            drift=max((a-b).length for a,b in zip(actual,baseline))
            max_ground=max(drift,max_ground)
            assert drift<1e-6,(o.name,frame,drift)
        for p,baseline in ports.items():
            actual=world_verts(bpy.data.objects[f"PORT | {p} | full machine collar"])
            assert max((a-b).length for a,b in zip(actual,baseline))<1e-6,(p,frame)
        for name,(indices,baseline) in fixed_socket.items():
            actual=world_verts(bpy.data.objects[name])
            drift=max((actual[i]-b).length for i,b in zip(indices,baseline))
            max_socket=max(drift,max_socket)
            assert drift<1e-6,(name,frame,drift)
    motion=[]
    for k,frame in enumerate(FRAMES):
        scene.frame_set(frame)
        actual=tuple(rig.location)
        expected=restrained_rumble(k)
        assert math.dist(actual,expected)<1e-5,(frame,actual,expected)
        motion.append(math.dist(actual,(0,0,0)))
    assert 0.003<max(motion)<0.012
    scene.frame_set(1);a=tuple(rig.location)
    scene.frame_set(SEAM);b=tuple(rig.location)
    assert math.dist(a,b)<1e-6
    assert len(receipt["glass_receiver_names"])==2
    assert all(bpy.data.objects[n].parent is rig for n in receipt["glass_receiver_names"])
    assert len([o for o in scene.objects if o.get("v6_boiling_bubble")])==24
    assert len(receipt["steam_objects"])==12
    assert all(bpy.data.objects[n].get("v6_no_closed_pipe_leaks")
               for n in receipt["steam_objects"])
    assert bpy.data.objects["SOLAR | west | adjustable trough pivot"].parent is rig
    assert bpy.data.objects["SOLAR | east | adjustable trough pivot"].parent is rig
    root.rotation_euler.z=0
    scene.frame_set(0)
    assert camera_record(scene)==receipt["camera"]
    for yaw in (0,90,180,270):
        root.rotation_euler.z=math.radians(yaw)
        scene.frame_set(25)
        assert camera_record(scene)==receipt["camera"]
    root.rotation_euler.z=0;scene.frame_set(0)
    assert len(receipt["renders"])==receipt["render_count"]==68
    for item in receipt["renders"]:
        assert sha(out/item["file"])==item["sha256"],item["file"]
    result={"schema":"tanks.solar.v7.native-reopen-qa","passed":True,
            "v6_source_sha256":sha(SOURCE),"v7_native_sha256":sha(native),
            "grounded_mesh_count":len(anchored),
            "max_ground_vertex_drift_bu":max_ground,
            "max_socket_vertex_drift_bu":max_socket,
            "max_upper_motion_bu":max(motion),
            "locked_native_ports":list(PORTS),
            "focal_glass_receivers":2,"real_boiling_bubbles":24,
            "steam_lobes":12,"flexed_pipe_staves":33,
            "real_blender_frames":68,"render_complete":True,
            "visual_approved":False,"game_integrated":False}
    (out/"native-reopen-qa.json").write_text(json.dumps(result,indent=2)+"\n")
    print("SOLAR_V7_68_FRAMES_GROUNDED_ZERO_WORLD_DRIFT_PASS",len(anchored),flush=True)

def main():
    p=argparse.ArgumentParser();p.add_argument("--output",type=Path,required=True)
    a=p.parse_args(sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else sys.argv[1:])
    check(a.output)
if __name__=="__main__":
    main()
