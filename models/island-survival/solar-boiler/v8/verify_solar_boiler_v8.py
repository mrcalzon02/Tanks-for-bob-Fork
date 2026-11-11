#!/usr/bin/env python3
"""Reopen V8 Blender file and prove floor is physically absent, supports unmoved."""
from __future__ import annotations
import argparse,json,math,sys
from pathlib import Path
import bpy
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
sys.path.insert(0,str(HERE.parent/"v7"))
from remove_solar_boiler_floor_v8 import (SOURCE,SOURCE_REPORT,FRAMES,SEAM,PORTS,
    PAD,PAVER_PREFIX,sha,camera_record,is_floor_name)
from refine_solar_boiler_v7 import restrained_rumble

def check(out):
    out=out.resolve()
    receipt=json.loads((out/"build-report.json").read_text())
    native=out/"solar-boiler-v8.blend"
    assert Path(bpy.data.filepath).resolve()==native.resolve()
    assert sha(native)==receipt["native_sha256"]
    assert sha(SOURCE)==receipt["v7_source_sha256"]
    previous=json.loads(SOURCE_REPORT.read_text())
    assert previous["native_sha256"]==receipt["v7_source_sha256"]
    assert receipt["removed_floor_count"]==11
    assert receipt["retained_support_count"]==20
    assert not receipt["visual_approved"] and not receipt["game_integrated"]
    scene=bpy.context.scene
    root=bpy.data.objects["EXPORT | rotate Solar Boiler model, never camera"]
    rig=bpy.data.objects[receipt["rumble_rig"]]
    scene.frame_set(0);root.rotation_euler.z=0
    bpy.context.view_layer.update()
    assert rig.parent is root and root.animation_data is None
    assert camera_record(scene)==receipt["camera"]
    assert scene.camera.parent is None and scene.camera.data.type=="ORTHO"
    assert len([x for x in scene.objects if x.type=="CAMERA"])==1
    assert scene.render.film_transparent and scene.render.image_settings.color_mode=="RGBA"
    assert list(root["footprint_tiles"])==receipt["footprint"]==[3,2]
    # Verify not merely hidden: the Blender object datablocks no longer exist.
    assert not any(is_floor_name(obj.name) for obj in bpy.data.objects)
    assert set(receipt["removed_floor_objects"]) == {
        n for n in previous["grounded_objects"] if is_floor_name(n)}
    assert receipt["removed_floor_objects"].count(PAD)==1
    assert len([n for n in receipt["removed_floor_objects"] if n.startswith(PAVER_PREFIX)])==10
    grounded=[bpy.data.objects[n] for n in receipt["retained_grounded_supports"]]
    assert len(grounded)==20
    assert all(o.type=="MESH" and o.parent is root and o.get("v7_ground_locked") for o in grounded)
    assert set(receipt["retained_grounded_supports"]).isdisjoint(receipt["removed_floor_objects"])

    def world_verts(obj):
        ev=obj.evaluated_get(bpy.context.evaluated_depsgraph_get())
        return [ev.matrix_world@v.co for v in ev.data.vertices]
    support_basis={o.name:world_verts(o) for o in grounded}
    port_basis={p:world_verts(bpy.data.objects[f"PORT | {p} | full machine collar"])
                for p in PORTS}
    flex={}
    for n in receipt["flexed_wood_pipe_planks"]:
        ob=bpy.data.objects[n]
        assert ob.parent is root
        s=len(ob.data.vertices)//4
        ix=(0,1,2*s,2*s+1)
        flex[n]=(ix,[world_verts(ob)[i] for i in ix])
    assert len(flex)==33
    max_support=0.;max_port=0.;max_socket=0.
    for frame in (0,1,4,7,13,19,25,31,37,43,49,55,61,67,73,79,85,91,94,97):
        scene.frame_set(frame)
        bpy.context.view_layer.update()
        for ob in grounded:
            actual=world_verts(ob);baseline=support_basis[ob.name]
            drift=max((a-b).length for a,b in zip(actual,baseline))
            max_support=max(max_support,drift)
            assert drift<1e-6,(ob.name,frame,drift)
        for p,baseline in port_basis.items():
            actual=world_verts(bpy.data.objects[f"PORT | {p} | full machine collar"])
            drift=max((a-b).length for a,b in zip(actual,baseline))
            max_port=max(max_port,drift)
            assert drift<1e-6,(p,frame,drift)
        for name,(idx,baseline) in flex.items():
            actual=world_verts(bpy.data.objects[name])
            drift=max((actual[i]-b).length for i,b in zip(idx,baseline))
            max_socket=max(max_socket,drift)
            assert drift<1e-6,(name,frame,drift)
    magnitudes=[]
    for k,frame in enumerate(FRAMES):
        scene.frame_set(frame)
        actual=tuple(rig.location);expected=restrained_rumble(k)
        assert math.dist(actual,expected)<1e-5,(frame,actual,expected)
        magnitudes.append(math.dist(actual,(0,0,0)))
    assert .003<max(magnitudes)<.012
    scene.frame_set(1);start=tuple(rig.location)
    scene.frame_set(SEAM);end=tuple(rig.location)
    assert math.dist(start,end)<1e-6
    assert len(receipt["glass_receiver_names"])==2
    assert all(bpy.data.objects[n].parent is rig for n in receipt["glass_receiver_names"])
    assert len([ob for ob in scene.objects if ob.get("v6_boiling_bubble")])==24
    assert len(receipt["steam_objects"])==12
    assert all(bpy.data.objects[n].get("v6_no_closed_pipe_leaks")
               for n in receipt["steam_objects"])
    assert bpy.data.objects["SOLAR | west | adjustable trough pivot"].parent is rig
    assert bpy.data.objects["SOLAR | east | adjustable trough pivot"].parent is rig
    root.rotation_euler.z=0;scene.frame_set(0)
    assert camera_record(scene)==receipt["camera"]
    for yaw in (0,90,180,270):
        root.rotation_euler.z=math.radians(yaw)
        scene.frame_set(25)
        assert camera_record(scene)==receipt["camera"]
    root.rotation_euler.z=0;scene.frame_set(0)
    assert len(receipt["renders"])==receipt["render_count"]==68
    for r in receipt["renders"]:
        assert sha(out/r["file"])==r["sha256"],r["file"]
    qa={
        "schema":"tanks.solar.v8.floorless-native-qa","passed":True,
        "v7_native_sha256":sha(SOURCE),"v8_native_sha256":sha(native),
        "absent_floor_mesh_count":len(receipt["removed_floor_objects"]),
        "retained_stationary_supports":len(grounded),
        "max_support_vertex_drift_bu":max_support,
        "max_native_port_vertex_drift_bu":max_port,
        "max_timber_socket_vertex_drift_bu":max_socket,
        "max_upper_motion_bu":max(magnitudes),
        "focal_glass_receivers":2,"boiling_bubbles":24,
        "steam_lobes":12,"flexed_pipe_staves":33,
        "real_blender_frames":68,"render_complete":True,
        "visual_approved":False,"game_integrated":False}
    (out/"native-reopen-qa.json").write_text(json.dumps(qa,indent=2)+"\n")
    print("SOLAR_V8_FLOORLESS_4_DIRECTION_NATIVE_VERIFIED",len(grounded),flush=True)

def main():
    p=argparse.ArgumentParser();p.add_argument("--output",type=Path,required=True)
    a=p.parse_args(sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else sys.argv[1:])
    check(a.output)
if __name__=="__main__":main()
