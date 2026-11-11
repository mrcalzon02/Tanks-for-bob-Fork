#!/usr/bin/env python3
"""Solar Boiler V7: ground-lock foundation and attenuate V6 upper-body rumble.

Reads immutable, independently verified V6 Blender native source. No geometry,
camera, Factorio prototype, live sprites or V6 proof artifacts are overwritten.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
SOLAR = HERE.parent
SOURCE = SOLAR / "generated-v6" / "solar-boiler-v6.blend"
SOURCE_REPORT = SOLAR / "generated-v6" / "build-report.json"
FRAMES = tuple(range(1, 92, 6))
SEAM = 97
YAW = (0, 90, 180, 270)
PORTS = ("water-west", "water-east", "steam-north")

# V6: max X ~.0175, Y .010, Z .008 tiles; V7 is gentler especially in Z.
# Ground plate, pavers, seating plinths, saddle shoes and upright supports are
# NOT animated. Only the supported upper machinery and optical assembly shudder.
def restrained_rumble(k):
    q = math.tau * (k % 16) / 16
    return (
        .0075 * math.sin(3*q) + .0016 * math.sin(7*q + .25),
        .0040 * math.sin(5*q + .55),
        .0015 * math.sin(4*q + 1.2),
    )

# Explicit categories from V1, V2 and V4 source, not guessed from a render.
GROUND_PREFIXES = (
    "FMPL | 3x2 ferrocrete continuous equipment pad",
    "FMPL | laid exterior concrete paver",
    "SUPPORT | boiler cast seating plinth",
    "SUPPORT | rusted steel saddle shoe",
    "SOLAR | load-bearing angled steel array support",
    "SOLAR | diagonal collector cage brace",
    "CONCENTRATOR | west | load-bearing collector saddle extension",
    "CONCENTRATOR | east | load-bearing collector saddle extension",
    "WOOD V4 | shaped barrel seating cradle",
)
REQUIRED_GROUND = GROUND_PREFIXES[:4]

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def self_check():
    assert len(FRAMES) == 16 and FRAMES[0] == 1 and FRAMES[-1] == 91
    assert all(abs(a-b) < 1e-12 for a,b in zip(restrained_rumble(0), restrained_rumble(16)))
    old_max = max(math.dist((0,0,0), (
        .014*math.sin(3*math.tau*k/16)+.0035*math.sin(7*math.tau*k/16+.25),
        .010*math.sin(5*math.tau*k/16+.55),
        .008*math.sin(4*math.tau*k/16+1.2)))
        for k in range(16))
    new_max = max(math.dist((0,0,0), restrained_rumble(k)) for k in range(16))
    assert 0.003 < new_max < 0.012 and new_max < old_max*.65, (new_max, old_max)
    assert max(abs(restrained_rumble(k)[2]) for k in range(16)) <= .0015
    assert SOURCE.is_file() and SOURCE_REPORT.is_file()
    original = json.loads(SOURCE_REPORT.read_text())
    assert original["native_sha256"] == sha(SOURCE)
    assert original["render_count"] == 68 and original["footprint"] == [3,2]
    assert not original["visual_approved"] and not original["game_integrated"]
    print("SOLAR_V7_GROUNDED_MOTION_MATH_PASS", round(new_max,6), round(old_max,6), flush=True)
    return original

def is_grounded(obj):
    return obj.type == "MESH" and obj.name.startswith(GROUND_PREFIXES)

def camera_record(scene):
    cam=scene.camera
    return {"name":cam.name,"matrix_world":[list(row) for row in cam.matrix_world],
            "type":cam.data.type,"ortho_scale":cam.data.ortho_scale,
            "shift_x":cam.data.shift_x,"shift_y":cam.data.shift_y,
            "resolution":[scene.render.resolution_x,scene.render.resolution_y]}

def modify_native(bpy, original):
    scene=bpy.context.scene
    root=bpy.data.objects["EXPORT | rotate Solar Boiler model, never camera"]
    rig=bpy.data.objects[original["rumble_rig"]]
    scene.frame_set(0)
    root.rotation_euler.z=0
    bpy.context.view_layer.update()
    assert rig.parent is root
    assert camera_record(scene) == original["camera"]
    grounded=[]
    for obj in list(bpy.data.objects):
        if obj.parent is not rig or not is_grounded(obj):
            continue
        world=obj.matrix_world.copy()
        obj.animation_data_clear()
        obj.parent=root
        obj.matrix_world=world
        obj["v7_ground_locked"]=True
        grounded.append(obj.name)
    for prefix in REQUIRED_GROUND:
        assert any(x.startswith(prefix) for x in grounded), ("Required grounded fixture missing",prefix)
    assert len(grounded) >= 19, ("Insufficient base/support objects", grounded)
    assert bpy.data.objects["FMPL | 3x2 ferrocrete continuous equipment pad"].parent is root

    rig.name="SHAKE V7 | upper wooden machine and focal glass, base static"
    rig.animation_data_clear()
    rig["v7_motion_bounds_tiles"]=[.0091,.004,.0015]
    rig["v7_foundation_static"]=True
    for frame,k in [(0,None)] + list(zip(FRAMES,range(16))) + [(SEAM,16)]:
        rig.location=(0.,0.,0.) if k is None else restrained_rumble(k)
        rig.keyframe_insert(data_path="location",frame=frame)

    # Rescale all 33 anchored wooden pipe skins to match the softer movement.
    # Their four socket-ring vertices remain exactly unchanged in local space.
    flexed=[]
    for name in original["flexed_wood_pipe_planks"]:
        ob=bpy.data.objects[name]
        assert ob.parent is root
        keys=ob.data.shape_keys
        assert keys is not None
        ky=keys.key_blocks["V6 local flex lateral"]
        kz=keys.key_blocks["V6 local flex vertical"]
        basis=keys.key_blocks["V6 original fixed socket"]
        n=len(basis.data);sections=n//4
        assert n%4==0 and sections>=4
        for index in (0,1,2*sections,2*sections+1):
            assert (ky.data[index].co-basis.data[index].co).length<1e-7
            assert (kz.data[index].co-basis.data[index].co).length<1e-7
        keys.animation_data_clear()
        north="north steam outlet" in name
        for frame,k in [(0,None)] + list(zip(FRAMES,range(16))) + [(SEAM,16)]:
            dx,dy,dz=(0.,0.,0.) if k is None else restrained_rumble(k)
            ky.value=(dx if north else dy)/.014
            kz.value=dz/.010
            ky.keyframe_insert(data_path="value",frame=frame)
            kz.keyframe_insert(data_path="value",frame=frame)
        ob["v7_socket_restraint"]="fixed 4-vertex ring, reduced interior flex"
        flexed.append(name)
    assert len(flexed)==33
    for port in PORTS:
        machine=bpy.data.objects["PORT | "+port+" | full machine collar"]
        ref=bpy.data.objects["REF | "+port+" | near matching collar"]
        assert machine.parent is root and ref.parent is root
    assert bpy.data.objects["SOLAR | west | adjustable trough pivot"].parent is rig
    assert bpy.data.objects["SOLAR | east | adjustable trough pivot"].parent is rig
    assert all(bpy.data.objects[n].parent is rig for n in original["glass_receiver_names"])
    scene["solar_boiler_revision"]="V7 fixed ferrocrete and supports; restrained upper-machine rumble"
    scene["v7_v6_sha256"]=sha(SOURCE)
    scene["game_integration"]=False
    scene.frame_set(0)
    root.rotation_euler.z=0
    bpy.context.view_layer.update()
    assert camera_record(scene)==original["camera"]
    return root,rig,grounded,flexed

def render(bpy,scene,out,filename,frame):
    scene.frame_set(frame)
    bpy.context.view_layer.update()
    scene.render.filepath=str(out/filename)
    print("SOLAR_V7_CYCLES",filename,frame,flush=True)
    bpy.ops.render.render(write_still=True)
    return {"file":filename,"frame":frame,"sha256":sha(out/filename)}

def build(args):
    import bpy
    original=self_check()
    if args.output.exists() and any(args.output.iterdir()):
        raise FileExistsError("V7 refuses to overwrite existing art evidence")
    bpy.ops.wm.open_mainfile(filepath=str(SOURCE))
    scene=bpy.context.scene
    root,rig,grounded,flexed=modify_native(bpy,original)
    scene.cycles.samples=args.samples
    scene.frame_start=0;scene.frame_end=SEAM
    scene.render.fps=8
    scene.render.image_settings.color_mode="RGBA"
    scene.render.film_transparent=True
    args.output.mkdir(parents=True,exist_ok=True)
    native=args.output/"solar-boiler-v7.blend"
    bpy.ops.file.pack_all()
    bpy.ops.wm.save_as_mainfile(filepath=str(native),compress=True,check_existing=False)
    report={"schema":"tanks.solar-boiler.v7.ground-locked-restrained-rumble",
            "native_sha256":sha(native),"v6_source_sha256":sha(SOURCE),
            "camera":original["camera"],"footprint":[3,2],"fps":8,
            "directions":list(YAW),"frames":list(FRAMES),"seam":SEAM,
            "rumble_rig":rig.name,"grounded_objects":grounded,
            "fixed_ground_count":len(grounded),"flexed_wood_pipe_planks":flexed,
            "glass_receiver_names":original["glass_receiver_names"],
            "steam_objects":original["steam_objects"],
            "native_port_interfaces_fixed":list(PORTS),
            "preserved_visual_design":"V6 glass, steam, reflectors, barrel, pipe locations",
            "visual_approved":False,"game_integrated":False,"renders":[]}
    manifest=args.output/"build-report.json"
    manifest.write_text(json.dumps(report,indent=2)+"\n")
    if args.render=="none":
        return
    for state in ("idle","working"):
        seq=[-1] if state=="idle" else range(16)
        for d,yaw in enumerate(YAW):
            root.rotation_euler.z=math.radians(yaw)
            for k in seq:
                frame=0 if k<0 else FRAMES[k]
                filename=(f"idle-d{d:02d}.png" if k<0 else
                          f"working-d{d:02d}-f{k:03d}.png")
                item=render(bpy,scene,args.output,filename,frame)
                item.update({"direction":d,"state":state,"index":k})
                report["renders"].append(item)
                manifest.write_text(json.dumps(report,indent=2)+"\n")
    root.rotation_euler.z=0
    scene.frame_set(0)
    bpy.context.view_layer.update()
    report["render_count"]=len(report["renders"])
    assert report["render_count"]==68
    manifest.write_text(json.dumps(report,indent=2)+"\n")
    print("SOLAR_V7_GROUND_LOCKED_68_REAL_BLENDER_RENDERS",flush=True)

def main():
    if "--self-check" in sys.argv:
        self_check();return
    p=argparse.ArgumentParser()
    p.add_argument("--output",type=Path,required=True)
    p.add_argument("--samples",type=int,default=24)
    p.add_argument("--render",choices=("none","all"),default="all")
    a=p.parse_args(sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else sys.argv[1:])
    if not 4<=a.samples<=48:
        raise ValueError("Cycles samples must be between 4 and 48")
    build(a)

if __name__=="__main__":
    main()
