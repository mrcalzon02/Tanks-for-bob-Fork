#!/usr/bin/env python3
"""Original 1x2 Tanks primitive steam pump — real editable Blender V1.
No Factorio prototype/runner mutation. Two native engine ports retain +/-0.75.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
CONTRACT=HERE/"contract.json"
FRAMES=tuple(range(1,92,6))
ORIENTATIONS=(0,90,180,270)
END=97

def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def preflight():
    spec=json.loads(CONTRACT.read_text(encoding="utf-8"))
    assert spec["entity_type"]=="pump" and spec["entity_name"]=="primitive-steam-powered-pump"
    assert spec["footprint_tiles"]==[1,2] and spec["tile_scale_bu"]==1
    assert spec["gameplay_locked"] and len(spec["native_connections"])==2
    expected=(("outlet-north","output",(0,-.75),"north",(0,1,.36),"N"),
              ("inlet-south","input",(0,.75),"south",(0,-1,.36),"S"))
    for item,check in zip(spec["native_connections"],expected):
        assert (item["id"],item["flow_direction"],tuple(item["native_position"]),
                item["native_direction"],tuple(item["blender_joint"]),
                item["fixture_facing"])==check
    capture=spec["capture"]
    assert tuple(capture["frames"])==FRAMES and tuple(capture["fixed_yaws"])==ORIENTATIONS
    assert capture["fps"]==8 and capture["seam"]==END
    assert capture["ortho_scale"]==3.85 and capture["elevation_degrees"]==45
    for key in ("fixture","fmpl_pbr_donor"):
        path=ROOT/spec[key]["path"]
        if not path.is_file():
            raise FileNotFoundError("Immutable donor missing: "+str(path))
        if sha(path)!=spec[key]["sha256"]:
            raise RuntimeError("Immutable donor hash mismatch: "+str(path))
    assert (ROOT/"models/reference/factorio-fluid-interface/append_reference.py").is_file()
    return spec

def coll(bpy,name):
    c=bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(c)
    return c

def root_obj(bpy,name,collection=None,parent=None):
    o=bpy.data.objects.new(name,None)
    if collection: collection.objects.link(o)
    else: bpy.context.scene.collection.objects.link(o)
    o.parent=parent
    return o

def reparent(bpy,obj,collection,parent):
    for c in list(obj.users_collection):c.objects.unlink(obj)
    collection.objects.link(obj)
    obj.parent=parent
    return obj

def mat(bpy,name,color,metal=.0,rough=.72,transmission=0):
    m=bpy.data.materials.new("PUMP | "+name)
    m.diffuse_color=color
    m.use_nodes=True
    node=m.node_tree.nodes.get("Principled BSDF")
    node.inputs["Base Color"].default_value=color
    node.inputs["Metallic"].default_value=metal
    node.inputs["Roughness"].default_value=rough
    inp=node.inputs.get("Transmission Weight")
    if inp is not None:inp.default_value=transmission
    if name in ("driftwood","oxidized copper","forged iron"):
        tex=m.node_tree.nodes.new("ShaderNodeTexNoise")
        tex.inputs["Scale"].default_value=29
        tex.inputs["Detail"].default_value=3
        bump=m.node_tree.nodes.new("ShaderNodeBump")
        bump.inputs["Strength"].default_value=.15
        bump.inputs["Distance"].default_value=.003
        m.node_tree.links.new(tex.outputs["Fac"],bump.inputs["Height"])
        m.node_tree.links.new(bump.outputs["Normal"],node.inputs["Normal"])
    return m

def materials(bpy,spec):
    donor=ROOT/spec["fmpl_pbr_donor"]["path"]
    with bpy.data.libraries.load(str(donor),link=False) as (src,dst):
        options=[n for n in src.materials if "ferrocrete" in n.lower()]
        if not options:raise RuntimeError("Approved FMPL ferrocrete PBR source missing")
        dst.materials=options
    approved=[m for m in dst.materials if m]
    if not approved:raise RuntimeError("Packed FMPL PBR import failed")
    pbr=next((m for m in approved if "dark" not in m.name.lower()),approved[0])
    return {
        "stone":pbr,
        "wood":mat(bpy,"driftwood",(.30,.175,.084,1),.05,.87),
        "iron":mat(bpy,"forged iron",(.19,.22,.23,1),.82,.60),
        "copper":mat(bpy,"oxidized copper",(.43,.22,.115,1),.76,.48),
        "brass":mat(bpy,"brass collar",(.56,.39,.13,1),.83,.36),
        "glass":mat(bpy,"murky sight glass",(.14,.38,.40,1),.03,.12,.33),
        "water":mat(bpy,"water",(.04,.34,.51,1),.07,.24,.16),
        "dial":mat(bpy,"aged dial",(.77,.70,.51,1),.03,.75),
        "steam":mat(bpy,"small relief steam",(.76,.79,.77,.6),.0,.91,.18),
    },[m.name for m in approved]

def cube(bpy,name,pos,size,material,c,parent,bevel=.01):
    bpy.ops.mesh.primitive_cube_add(size=1,location=pos)
    obj=reparent(bpy,bpy.context.object,c,parent)
    obj.name=name
    obj.scale=size
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    obj.data.materials.append(material)
    if bevel:
        modifier=obj.modifiers.new("Worn edges","BEVEL")
        modifier.width=min(bevel,min(size)*.18)
        modifier.segments=2
        obj.modifiers.new("Weighted faceted normals","WEIGHTED_NORMAL")
    return obj

def cylinder(bpy,name,pos,r,depth,material,c,parent,rotation=(0,0,0),segments=32):
    bpy.ops.mesh.primitive_cylinder_add(vertices=segments,radius=r,depth=depth,
                                        location=pos,rotation=rotation)
    obj=reparent(bpy,bpy.context.object,c,parent)
    obj.name=name
    obj.data.materials.append(material)
    for p in obj.data.polygons:
        p.use_smooth=len(p.vertices)==4
    return obj

def rod(bpy,name,a,b,r,material,c,parent):
    from mathutils import Vector
    lo,hi=Vector(a),Vector(b)
    d=hi-lo
    if d.length<1e-5:raise ValueError("Zero-length shaft "+name)
    obj=cylinder(bpy,name,(lo+hi)/2,r,d.length,material,c,parent,segments=16)
    obj.rotation_euler=d.to_track_quat("Z","Y").to_euler()
    return obj

def bent_pipe(bpy,name,points,r,material,c,parent):
    cu=bpy.data.curves.new(name,"CURVE")
    cu.dimensions="3D"
    cu.resolution_u=16
    cu.bevel_depth=r
    cu.bevel_resolution=4
    spline=cu.splines.new("POLY")
    spline.points.add(len(points)-1)
    for pt,co in zip(spline.points,points):
        pt.co=tuple(co)+(1.0,)
    obj=bpy.data.objects.new(name,cu)
    c.objects.link(obj)
    obj.parent=parent
    cu.materials.append(material)
    return obj

def machine_sockets(bpy,spec,materials,frame,model):
    reference=ROOT/spec["fixture"]["path"]
    sys.path.insert(0,str(ROOT/"models/reference/factorio-fluid-interface"))
    try:from append_reference import append_interface
    finally:sys.path.pop(0)
    out=[]
    for item in spec["native_connections"]:
        jy=item["blender_joint"][1]
        added,helper=append_interface(reference,joint_ground=(0,jy,0),
            facing=item["fixture_facing"],name="GUIDE | "+item["id"])
        bpy.context.view_layer.update()
        pieces={obj.get("interface_role"):obj for obj in added.all_objects}
        for role in ("machine_collar","machine_throat"):
            src=pieces[role]
            matrix=src.matrix_world.copy()
            clone=src.copy()
            clone.data=src.data.copy()
            clone.name="PORT | "+item["id"]+" | "+role
            frame.objects.link(clone)
            clone.parent=model
            clone.matrix_world=matrix
            clone.data.materials.clear()
            clone.data.materials.append(materials["brass" if role=="machine_collar" else "iron"])
            clone["native_position"]=item["native_position"]
            clone["native_direction"]=item["native_direction"]
            clone["port_id"]=item["id"]
            clone["standard_sha256"]=spec["fixture"]["sha256"]
            clone["nominal_joint"]=item["blender_joint"]
            out.append(clone)
        for o in list(added.all_objects):
            bpy.data.objects.remove(o,do_unlink=True)
        bpy.data.collections.remove(added)
    assert len(out)==4
    return out

def camera_setup(bpy,spec):
    from mathutils import Vector
    scene=bpy.context.scene
    config=spec["capture"]
    camera_data=bpy.data.cameras.new("Fixed Wube 45 degree orthographic")
    camera=bpy.data.objects.new("FMPL_CAPTURE_CAMERA",camera_data)
    scene.collection.objects.link(camera)
    camera.location=config["camera"]
    camera.rotation_euler=(math.radians(45),0,0)
    camera_data.type="ORTHO"
    camera_data.ortho_scale=config["ortho_scale"]
    scene.camera=camera
    for name,loc,power,size in (("Key",(-3,-4,7),700,5),("Fill",(3,3,6),420,4)):
        light=bpy.data.lights.new(name,"AREA")
        light.energy=power
        light.shape="DISK"
        light.size=size
        obj=bpy.data.objects.new(name,light)
        scene.collection.objects.link(obj)
        obj.location=loc
        obj.rotation_euler=(Vector((0,0,.9))-obj.location).to_track_quat("-Z","Y").to_euler()
    world=bpy.data.worlds.new("Nauvis neutral ambient")
    world.use_nodes=True
    world.node_tree.nodes.get("Background").inputs["Strength"].default_value=.50
    scene.world=world
    scene.render.engine="CYCLES"
    scene.cycles.device="CPU"
    scene.render.resolution_x=scene.render.resolution_y=256
    scene.render.resolution_percentage=100
    scene.render.image_settings.file_format="PNG"
    scene.render.image_settings.color_mode="RGBA"
    scene.render.film_transparent=True
    scene.render.fps=8
    scene.frame_end=END

def construct(bpy,spec):
    from mathutils import Vector
    mats,pbr=materials(bpy,spec)
    base=coll(bpy,"01 | minimal loose footings and wood bed")
    pipes=coll(bpy,"02 | stationary full bore north and south liquid pipes")
    mechanical=coll(bpy,"03 | crude cast drive cylinder and boiler")
    motion=coll(bpy,"04 | rotating flywheel and true reciprocating piston")
    detail=coll(bpy,"05 | inspection instruments and steam relief")
    model=root_obj(bpy,"EXPORT | rotate primitive steam-powered pump, never camera")
    model["footprint_tiles"]=[1,2]
    model["prototype_type"]="pump"
    # Four little feet, no blanket floor slab; two irregular timber skids.
    for x in (-.32,.32):
        for y in (-.64,.64):
            cube(bpy,"FOOT | separate small FMPL stone footing",
                 (x,y,.082),(.20,.23,.165),mats["stone"],base,model,.014)
        cube(bpy,"FRAME | rough lengthwise timber runner",
             (x,0,.22),(.16,1.60,.18),mats["wood"],base,model)
    for y in (-.57,.56):
        cube(bpy,"FRAME | notched lower cross tie",
             (0,y,.29),(.70,.12,.13),mats["wood"],base,model)
    # Centered wood frame and squat brass-copper steam jacket.
    for x in (-.31,.31):
        rod(bpy,"FRAME | independent blackened steel riser",
            (x,-.29,.25),(x,-.29,1.43),.043,mats["iron"],mechanical,model)
    cylinder(bpy,"PUMP | forged upright pressure barrel",(0,-.16,.73),
             .215,.70,mats["iron"],mechanical,model,segments=48)
    cylinder(bpy,"PUMP | bronze retaining band",(0,-.16,.49),
             .243,.09,mats["brass"],mechanical,model)
    cylinder(bpy,"PUMP | upper sealing band",(0,-.16,1.05),
             .243,.08,mats["brass"],mechanical,model)
    cube(bpy,"FIREBOX | battered driftwood and metal combustion case",
         (0,.41,.49),(.56,.46,.51),mats["wood"],mechanical,model,.035)
    for i in range(4):
        cube(bpy,"FIREBOX | exposed heat slit",( -.18+i*.12,.164,.50),
             (.035,.028,.32),mats["iron"],mechanical,model,.005)
    cylinder(bpy,"STEAM | humble copper pressure dome",
             (0,.36,1.04),.215,.28,mats["copper"],mechanical,model)
    rod(bpy,"STEAM | small copper riser",
        (0,.39,1.11),(0,.39,1.42),.062,mats["copper"],mechanical,model)
    cylinder(bpy,"STEAM | boiler relief cap",(0,.39,1.45),
             .105,.095,mats["brass"],detail,model)
    # The official native pipe fittings are stationary and full-sized.
    sockets=machine_sockets(bpy,spec,mats,pipes,model)
    bent_pipe(bpy,"PIPE | south inlet from native port",
              [(0,-.99,.36),(0,-.73,.36),(0,-.48,.36),(0,-.42,.62)],
              .245,mats["iron"],pipes,model)
    bent_pipe(bpy,"PIPE | north high-pressure discharge to native port",
              [(0,-.08,.76),(0,.08,.76),(0,.28,.36),(0,.73,.36),(0,.99,.36)],
              .245,mats["copper"],pipes,model)
    # Visible fixed supports clamp the two heavy through-lines.
    for y in (-.70,.70):
        rod(bpy,"BRACE | pipe saddle crossing frame",
            (-.30,y,.30),(.30,y,.30),.036,mats["brass"],pipes,model)
    # One exposed vertical piston slides inside its immutable cylinder.
    piston=root_obj(bpy,"MOTION | vertically reciprocating piston",motion,model)
    cylinder(bpy,"MOTION | polished plunger head",(0,-.16,1.14),
             .175,.15,mats["copper"],motion,piston)
    cylinder(bpy,"MOTION | hardened sliding piston shaft",(0,-.16,1.36),
             .06,.40,mats["iron"],motion,piston)
    cube(bpy,"MOTION | crosshead on straight guides",(0,-.16,1.53),
         (.49,.18,.105),mats["wood"],motion,piston)
    for x in (-.30,.30):
        rod(bpy,"FRAME | narrow crosshead guide",
            (x,-.16,1.07),(x,-.16,1.68),.023,mats["brass"],motion,model)
    # Side crank and flywheel: real 3D wheel, not a flat rotating billboard.
    wheel=root_obj(bpy,"MOTION | keyed lateral 3D drive flywheel",motion,model)
    wheel.location=(.27,-.15,.94)
    bpy.ops.mesh.primitive_torus_add(major_segments=48,minor_segments=8,
        location=(0,0,0),rotation=(0,math.pi/2,0),
        major_radius=.235,minor_radius=.025)
    ring=reparent(bpy,bpy.context.object,motion,wheel)
    ring.name="MOTION | cast bronze wheel rim"
    ring.data.materials.append(mats["brass"])
    cylinder(bpy,"MOTION | flywheel axle bearing",(0,0,0),
             .086,.11,mats["iron"],motion,wheel,rotation=(0,math.pi/2,0))
    for k in range(6):
        a=k*2*math.pi/6
        rod(bpy,"MOTION | six real wheel spokes",
            (0,0,0), (0,.23*math.sin(a),.23*math.cos(a)),
            .021,mats["wood"],motion,wheel)
    cylinder(bpy,"MOTION | crank eccentric pin",
        (.065,0,.145),.044,.095,mats["iron"],motion,wheel,
        rotation=(0,math.pi/2,0),segments=16)
    # Connecting rod is sized/oriented every pose between eccentric pin & head.
    link=cylinder(bpy,"MOTION | hinged connecting rod",
                  (0,0,0),.031,1,mats["iron"],motion,model,segments=12)
    # Inspectable liquid sight and small gauge, not giant icon-space labels.
    cylinder(bpy,"SIGHT | clouded cylindrical glass",
             (-.30,-.28,.86),.060,.36,mats["glass"],detail,model)
    cylinder(bpy,"SIGHT | colored fluid volume",
             (-.30,-.28,.77),.039,.175,mats["water"],detail,model)
    for z in (.67,1.05):
        cylinder(bpy,"SIGHT | brass compression collar",
            (-.30,-.28,z),.076,.041,mats["brass"],detail,model)
    cylinder(bpy,"GAUGE | circular tiny body",
        (-.26,.23,1.23),.126,.045,mats["brass"],detail,model,
        rotation=(math.pi/2,0,0),segments=24)
    gauge=root_obj(bpy,"MOTION | analog pressure needle",detail,model)
    gauge.location=(-.26,.19,1.23)
    rod(bpy,"GAUGE | slender true pointer",
        (-.09,0,0),(.075,0,0),.009,mats["iron"],detail,gauge)
    puff=cylinder(bpy,"STEAM | intermittent tiny safety valve discharge",
             (0,.38,1.56),.074,.13,mats["steam"],detail,model,segments=16)
    # A full 16-pose rotation and seam, with connected rod keyframed to
    # actual piston/flywheel endpoints. Importantly, *NO* port object moves.
    for j,frame in enumerate((*FRAMES,END)):
        phase=j*math.pi*2/16
        piston.location.z=.103*math.cos(phase)
        wheel.rotation_euler.x=phase
        gauge.rotation_euler.y=.12*math.sin(phase)
        puff.scale.z=.70+.32*max(0,math.sin(phase+.3))
        for obj,field in ((piston,"location"),(wheel,"rotation_euler"),
                          (gauge,"rotation_euler"),(puff,"scale")):
            obj.keyframe_insert(data_path=field,frame=frame)
        # The flywheel crank offset rotates in the YZ plane of the wheel.
        crank=Vector((.335,-.15-.145*math.sin(phase),.94+.145*math.cos(phase)))
        head=Vector((0,-.16,1.54+.103*math.cos(phase)))
        vector=head-crank
        link.location=(head+crank)/2
        link.rotation_euler=vector.to_track_quat("Z","Y").to_euler()
        link.scale.z=vector.length
        for field in ("location","rotation_euler","scale"):
            link.keyframe_insert(data_path=field,frame=frame)
    piston.location.z=0
    wheel.rotation_euler.x=0
    gauge.rotation_euler.y=0
    link.scale.z=1
    puff.scale.z=1
    return model,sockets,pbr

def integrity(bpy,spec,model,sockets):
    from mathutils import Vector
    scene=bpy.context.scene
    assert len(sockets)==4
    assert len([x for x in scene.objects if x.type=="CAMERA"])==1
    assert scene.camera.parent is None and scene.camera.data.type=="ORTHO"
    assert abs(scene.camera.data.ortho_scale-3.85)<1e-6
    assert tuple(model["footprint_tiles"])==(1,2)
    for obj in sockets:
        assert obj.parent is model and len(obj.data.vertices)==256
        assert obj["standard_sha256"]==spec["fixture"]["sha256"]
    assert sorted({tuple(x["native_position"]) for x in sockets})==[(0,-.75),(0,.75)]
    scene.frame_set(1)
    bpy.context.view_layer.update()
    stationary=[o.matrix_world.copy() for o in sockets]
    piston=bpy.data.objects["MOTION | vertically reciprocating piston"]
    wheel=bpy.data.objects["MOTION | keyed lateral 3D drive flywheel"]
    initial=(float(piston.location.z),float(wheel.rotation_euler.x))
    high=initial[0]
    low=initial[0]
    for frame in (7,13,25,49,73,91,97):
        scene.frame_set(frame)
        bpy.context.view_layer.update()
        high=max(high,float(piston.location.z))
        low=min(low,float(piston.location.z))
        for obj,orig in zip(sockets,stationary):
            if max(abs(a-b) for rowA,rowB in zip(obj.matrix_world,orig)
                   for a,b in zip(rowA,rowB))>1e-6:
                raise RuntimeError("Fixed full-bore socket moved: "+obj.name)
    assert high-low>.15
    scene.frame_set(97)
    assert abs(piston.location.z-initial[0])<1e-6
    assert abs(math.sin(wheel.rotation_euler.x-initial[1]))<1e-6
    scene.frame_set(0)
    return {"rigid_port_meshes":4,"port_vertex_count_each":256,
            "north_output":[0,-.75],"south_input":[0,.75],
            "measured_piston_travel_bu":high-low,"verified_seam":True}

def build(args):
    import bpy
    spec=preflight()
    out=args.out.resolve()
    if out.exists():raise FileExistsError("Refuse existing render directory: "+str(out))
    bpy.ops.wm.read_factory_settings(use_empty=True)
    camera_setup(bpy,spec)
    bpy.context.scene.cycles.samples=args.samples
    model,sockets,source_mats=construct(bpy,spec)
    qa=integrity(bpy,spec,model,sockets)
    out.mkdir(parents=True)
    master=out/"pump-v1.blend"
    bpy.ops.file.pack_all()
    bpy.ops.wm.save_as_mainfile(filepath=str(master),compress=True,check_existing=False)
    report={"schema":"tanks.primitive-steam-pump.v1.native-source",
        "native_sha256":sha(master),
        "fixture_sha256":spec["fixture"]["sha256"],
        "pbr_donor_sha256":spec["fmpl_pbr_donor"]["sha256"],
        "fmpl_materials":source_mats,
        "dimensions":[1,2],"type":"pump","name":"primitive-steam-powered-pump",
        "ports":spec["native_connections"],
        "camera":{"name":"FMPL_CAPTURE_CAMERA","ortho_scale":3.85,"fixed":True,
                  "elevation_degrees":45},
        "qa":qa,"directions":list(ORIENTATIONS),"fps":8,
        "frames":list(FRAMES),"seam":END,
        "render_mode":args.render,"renders":[],
        "game_integrated":False,"owner_visual_approved":False}
    manifest=out/"build-report.json"
    manifest.write_text(json.dumps(report,indent=2)+"\n")
    if args.render!="none":
        frame_ids=range(16) if args.render=="all" else (4,)
        for d,degrees in enumerate(ORIENTATIONS):
            model.rotation_euler.z=math.radians(degrees)
            for state,sequence in (("idle",(-1,)),("working",frame_ids)):
                for k in sequence:
                    frame=0 if k<0 else FRAMES[k]
                    bpy.context.scene.frame_set(frame)
                    bpy.context.view_layer.update()
                    name=("idle-d%02d.png"%d if k<0 else
                          "working-d%02d-f%03d.png"%(d,k))
                    bpy.context.scene.render.filepath=str(out/name)
                    bpy.ops.render.render(write_still=True)
                    report["renders"].append({"file":name,"state":state,
                        "direction":d,"index":k,"frame":frame,"sha256":sha(out/name)})
                    manifest.write_text(json.dumps(report,indent=2)+"\n")
    report["render_count"]=len(report["renders"])
    assert report["render_count"]=={"none":0,"proof":8,"all":68}[args.render]
    manifest.write_text(json.dumps(report,indent=2)+"\n")
    print("TANKS_PRIMITIVE_STEAM_PUMP_NATIVE_BUILT",report["render_count"],sha(master),flush=True)

def main():
    if "--self-check" in sys.argv:
        preflight()
        print("TANKS_PRIMITIVE_STEAM_PUMP_SOURCE_PREFLIGHT_PASS",flush=True)
        return
    p=argparse.ArgumentParser()
    p.add_argument("--out",type=Path,required=True)
    p.add_argument("--render",choices=("none","proof","all"),default="proof")
    p.add_argument("--samples",type=int,default=16)
    args=p.parse_args(sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else sys.argv[1:])
    if not (4<=args.samples<=64):raise ValueError("Samples bounded 4..64")
    build(args)
if __name__=="__main__":main()
