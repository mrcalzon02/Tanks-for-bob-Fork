#!/usr/bin/env python3
"""Original 3D shoreline Beach Pump V1, never a reskinned vanilla offshore pump.

Use actual Factorio 2.1 offshore-pump/beachpump: native water source north,
one south output at native (0,+0.25), shoreline selection box offset north.
Blender models north as +Y, moving only the intake paddle / lever / diaphragm.
No prototype edits, no full terrain slab, and no hidden machinery.
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
FRAMES=tuple(range(1,92,6))
DIRECTIONS=(0,90,180,270)
LOOP=97

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def preflight():
    c=json.loads((HERE/"contract.json").read_text(encoding="utf-8"))
    entity=c["entity"]
    assert (entity["type"],entity["name"])==("offshore-pump","beachpump")
    assert entity["selection_box_native"]==[[-.6,-1.49],[.6,.49]]
    assert entity["collision_box_native"]==[[-.6,-1.05],[.6,.3]]
    assert entity["tile_width"]==entity["tile_height"]==1
    assert entity["fluid_source_offset"]==[0,-1]
    assert entity["output_connection"]=={
        "position_native":[0,.25],"direction":"south","flow_direction":"output"}
    assert entity["energy_source"]=="void" and entity["pumping_speed"]==.01
    g=c["geometry"]
    assert g["visible_output_mouth_xyz"]==[0,-.49,.36]
    assert g["blender_selection_y"]==[-.49,1.49]
    assert g["no_concrete_floor"] and g["independent_stilt_supports"]==4
    f=c["fixture"]
    assert f["standard_id"]=="factorio-fluid-interface-v1"
    assert f["facing"]=="S" and f["center_height"]==.36
    a=c["animation"]
    assert a["working_frames"]==list(FRAMES)
    assert a["loop_return_frame"]==LOOP and a["fps"]==8
    assert c["camera"]["model_yaws_deg"]==list(DIRECTIONS)
    assert c["camera"]["single_camera"] and c["camera"]["elevation_deg"]==45
    for name in ("fixture","pbr_donor"):
        p=ROOT/c[name]["path"]
        if not p.is_file():raise FileNotFoundError("Pinned donor absent: "+str(p))
        if sha(p)!=c[name]["sha256"]:raise RuntimeError("Pinned donor changed: "+str(p))
    if not (ROOT/"models/reference/factorio-fluid-interface/append_reference.py").is_file():
        raise FileNotFoundError("Pinned FMPL fluid reference helper missing")
    return c

def group(bpy,name):
    c=bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(c)
    return c

def empty(bpy,name,c=None,parent=None):
    o=bpy.data.objects.new(name,None)
    if c is not None:c.objects.link(o)
    else:bpy.context.scene.collection.objects.link(o)
    o.parent=parent
    return o

def move(bpy,o,c,parent):
    for previous in tuple(o.users_collection):previous.objects.unlink(o)
    c.objects.link(o)
    o.parent=parent
    return o

def material(bpy,name,rgba,rough=.7,metal=0,transmission=0,noise=False):
    mat=bpy.data.materials.new("BEACH | "+name)
    mat.diffuse_color=rgba
    mat.use_nodes=True
    bs=mat.node_tree.nodes.get("Principled BSDF")
    bs.inputs["Base Color"].default_value=rgba
    bs.inputs["Roughness"].default_value=rough
    bs.inputs["Metallic"].default_value=metal
    t=bs.inputs.get("Transmission Weight")
    if t is not None:t.default_value=transmission
    if noise:
        n=mat.node_tree.nodes.new("ShaderNodeTexNoise")
        n.inputs["Scale"].default_value=37
        n.inputs["Detail"].default_value=3
        b=mat.node_tree.nodes.new("ShaderNodeBump")
        b.inputs["Strength"].default_value=.13
        b.inputs["Distance"].default_value=.004
        mat.node_tree.links.new(n.outputs["Fac"],b.inputs["Height"])
        mat.node_tree.links.new(b.outputs["Normal"],bs.inputs["Normal"])
    return mat

def approved_materials(bpy,c):
    donor=ROOT/c["pbr_donor"]["path"]
    with bpy.data.libraries.load(str(donor),link=False) as (source,dest):
        names=[n for n in source.materials if
               c["pbr_donor"]["material_name_contains"].lower() in n.lower()]
        if not names:raise ValueError("V8 Blender donor lacks approved packed ferrocrete")
        dest.materials=names
    provided=[m for m in dest.materials if m]
    if not provided:raise ValueError("FMPL material append produced no datablocks")
    stone=next((m for m in provided if "dark" not in m.name.lower()),provided[0])
    mats={
        "foot":stone,
        "wood":material(bpy,"pitted salt driftwood",(.32,.23,.13,1),.86,.04,noise=True),
        "darkwood":material(bpy,"wet salt-darkened timber",(.19,.14,.09,1),.89,.03,noise=True),
        "rope":material(bpy,"hemp tied lashings",(.53,.40,.23,1),.92),
        "copper":material(bpy,"dented copper",(.51,.28,.12,1),.46,.68,noise=True),
        "iron":material(bpy,"black wet forged iron",(.18,.22,.23,1),.7,.70,noise=True),
        "brass":material(bpy,"weathered brass",(.65,.46,.20,1),.49,.78),
        "leather":material(bpy,"oiled leather bellows",(.30,.16,.105,1),.92),
        "glass":material(bpy,"old green glass",(.13,.37,.36,1),.14,.10,.23),
        "water":material(bpy,"green-blue water",(.06,.34,.46,1),.19,.04,.18),
        "dial":material(bpy,"chalk dial",(.74,.69,.53,1),.84),
    }
    return mats,[m.name for m in provided]

def block(bpy,name,pos,scale,mat,c,parent,bevel=.015):
    bpy.ops.mesh.primitive_cube_add(size=1,location=pos)
    o=move(bpy,bpy.context.object,c,parent)
    o.name=name
    o.scale=scale
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    o.data.materials.append(mat)
    if bevel:
        m=o.modifiers.new("Hand-worn edges","BEVEL")
        m.width=min(bevel,min(scale)*.18)
        m.segments=2
        o.modifiers.new("Soft normals","WEIGHTED_NORMAL")
    return o

def cylinder(bpy,name,pos,radius,height,mat,c,parent,rotation=(0,0,0),n=32):
    bpy.ops.mesh.primitive_cylinder_add(vertices=n,radius=radius,depth=height,
                                       location=pos,rotation=rotation)
    o=move(bpy,bpy.context.object,c,parent)
    o.name=name
    o.data.materials.append(mat)
    for p in o.data.polygons:p.use_smooth=(len(p.vertices)==4)
    return o

def rod(bpy,name,a,b,r,mat,c,parent):
    from mathutils import Vector
    start=Vector(a);end=Vector(b)
    vector=end-start
    if vector.length<1e-5:raise RuntimeError("Invalid zero-length linkage: "+name)
    obj=cylinder(bpy,name,(start+end)/2,r,vector.length,mat,c,parent,n=16)
    obj.rotation_euler=vector.to_track_quat("Z","Y").to_euler()
    return obj

def pipe(bpy,name,points,r,mat,c,parent):
    curve=bpy.data.curves.new(name,"CURVE")
    curve.dimensions="3D"
    curve.resolution_u=18
    curve.bevel_depth=r
    curve.bevel_resolution=3
    spline=curve.splines.new("POLY")
    spline.points.add(len(points)-1)
    for pt,co in zip(spline.points,points):
        pt.co=(float(co[0]),float(co[1]),float(co[2]),1)
    o=bpy.data.objects.new(name,curve)
    c.objects.link(o)
    o.parent=parent
    o.data.materials.append(mat)
    return o

def socket(bpy,c,m,group_socket,root):
    sys.path.insert(0,str(ROOT/"models/reference/factorio-fluid-interface"))
    try:from append_reference import append_interface
    finally:sys.path.pop(0)
    src=ROOT/c["fixture"]["path"]
    position=c["geometry"]["visible_output_mouth_xyz"]
    lib,ref=append_interface(src,joint_ground=(position[0],position[1],0),
                         facing="S",name="BEACH TEMP FIXTURE | south outlet")
    bpy.context.view_layer.update()
    roles={o.get("interface_role"):o for o in lib.all_objects}
    retained=[]
    for role in c["geometry"]["fixed_socket_roles"]:
        original=roles[role]
        global_matrix=original.matrix_world.copy()
        o=original.copy()
        o.data=original.data.copy()
        o.name="PORT | south output | "+role
        group_socket.objects.link(o)
        o.parent=root
        o.matrix_world=global_matrix
        o.data.materials.clear()
        o.data.materials.append(m["iron" if role=="machine_throat" else "brass"])
        o["role"]="beachpump_output"
        o["native_cell"]=c["entity"]["output_connection"]["position_native"]
        o["native_direction"]="south"
        o["blender_joint"]=position
        o["reference_sha256"]=c["fixture"]["sha256"]
        retained.append(o)
    for o in list(lib.all_objects):
        bpy.data.objects.remove(o,do_unlink=True)
    bpy.data.collections.remove(lib)
    assert len(retained)==2 and all(len(o.data.vertices)==256 for o in retained)
    return retained

def camera(bpy,c):
    from mathutils import Vector
    scene=bpy.context.scene
    info=c["camera"]
    data=bpy.data.cameras.new("Wube fixed 45deg")
    cam=bpy.data.objects.new("FMPL_CAPTURE_CAMERA",data)
    scene.collection.objects.link(cam)
    cam.location=info["position"]
    cam.rotation_euler=(math.radians(info["elevation_deg"]),0,0)
    data.type="ORTHO"
    data.ortho_scale=info["orthographic_scale"]
    scene.camera=cam
    for name,p,power,sz in (
        ("Warm key",(-3,-4,7),800,4),
        ("Cool fill",(3,4,6),480,4)):
        ld=bpy.data.lights.new(name,"AREA")
        ld.energy=power
        ld.shape="DISK";ld.size=sz
        ob=bpy.data.objects.new(name,ld)
        scene.collection.objects.link(ob)
        ob.location=p
        ob.rotation_euler=(Vector((0,0,.7))-ob.location).to_track_quat("-Z","Y").to_euler()
    world=bpy.data.worlds.new("Nauvis saltwater light")
    world.use_nodes=True
    world.node_tree.nodes["Background"].inputs["Strength"].default_value=.52
    scene.world=world
    scene.render.engine="CYCLES"
    scene.cycles.device="CPU"
    scene.render.resolution_x=scene.render.resolution_y=info["resolution"][0]
    scene.render.resolution_percentage=100
    scene.render.image_settings.color_mode="RGBA"
    scene.render.image_settings.file_format="PNG"
    scene.render.film_transparent=True
    scene.render.fps=c["animation"]["fps"]
    scene.frame_end=LOOP

def model(bpy,c):
    from mathutils import Vector
    m,pbr=approved_materials(bpy,c)
    foot=group(bpy,"01 | four small rock anchors and loose boardwalk")
    inlet=group(bpy,"02 | waterward slotted cage and wet inlet riser")
    body=group(bpy,"03 | timber valve chamber and dock supports")
    outlet=group(bpy,"04 | single static full-bore landward outlet")
    mechanical=group(bpy,"05 | wave paddle, true rocker and active diaphragm")
    visible=group(bpy,"06 | water gauge, rope, moving droplets")
    root=empty(bpy,"EXPORT | rotate beachpump not camera")
    root["factorio_prototype"]="offshore-pump/beachpump"
    root["water_side_blender"]="+Y"
    root["native_selection_box"]=[[-.6,-1.49],[.6,.49]]
    # Separate hand-laid supports: NO contiguous concrete plinth or false terrain.
    for x in (-.33,.33):
        for y in (-.31,1.08):
            block(bpy,"ANCHOR | separate FMPL ferrocrete stone footing",
                (x,y,.065),(.22,.27,.13),m["foot"],foot,root,.014)
            cylinder(bpy,"DOCK | crooked wooden upright",
                (x,y,.31),.065,.60,m["darkwood"],foot,root,n=12)
        block(bpy,"DOCK | long warped skids",(x,.34,.38),
            (.13,1.49,.115),m["wood"],foot,root,.018)
    for i in range(8):
        y=-.24+i*.167
        block(bpy,"DOCK | narrow separated driftwood plank",
            (0,y,.47),(.87,.125,.052),
            m["wood"] if i%3 else m["darkwood"],foot,root,.012)
    for x in (-.41,.41):
        rod(bpy,"DOCK | tied longitudinal side rail",
            (x,-.33,.52),(x,1.25,.52),.037,m["wood"],foot,root)
    for y in (-.24,.92):
        for x in (-.37,.37):
            cylinder(bpy,"DOCK | rope post",(x,y,.58),.03,.22,
                     m["darkwood"],foot,root,n=10)
    # Visible submerged-looking water-side intake; no flat ocean sheet.
    pipe(bpy,"INTAKE | open slanted lower suction duct",
         [(0,1.31,.10),(0,1.14,.18),(0,.88,.36),(0,.68,.70)],
         .125,m["copper"],inlet,root)
    cylinder(bpy,"INTAKE | open iron grille nose",
             (0,1.28,.13),.21,.18,m["iron"],inlet,root,n=24)
    for i in range(7):
        x=-.18+i*.06
        block(bpy,"INTAKE | visible narrow filter grill bar",
              (x,1.388,.14),(.023,.027,.25),m["wood"],inlet,root,.003)
    for x in (-.19,.19):
        rod(bpy,"INTAKE | wooden strainer guard",
             (x,1.10,.14),(x,1.34,.34),.026,m["darkwood"],inlet,root)
    # Pumping box: timber sides, bronze straps, mechanical wet piston housing.
    block(bpy,"VALVE | solid timber pump block",
        (0,.43,.83),(.66,.63,.48),m["wood"],body,root,.047)
    for x in (-.35,.35):
        block(bpy,"VALVE | rough bolted timber cheek",
              (x,.43,.81),(.065,.68,.53),m["darkwood"],body,root)
    for y in (.16,.68):
        block(bpy,"VALVE | copper belt across chamber",
             (0,y,.83),(.70,.047,.16),m["copper"],body,root,.008)
    cylinder(bpy,"VALVE | vertical piston sleeve",
            (0,.37,1.15),.17,.30,m["iron"],body,root,n=32)
    cylinder(bpy,"VALVE | aged copper top collar",
            (0,.37,1.31),.19,.055,m["brass"],body,root)
    # Landward outlet is a standalone machine-side full-bore geometry clone.
    fixed=socket(bpy,c,m,outlet,root)
    pipe(bpy,"OUTPUT | continuous fixed copper lifter from pump chamber",
        [(0,.15,.72),(0,-.06,.72),(0,-.15,.47),(0,-.33,.36),(0,-.487,.36)],
        .238,m["copper"],outlet,root)
    for y in (-.19,-.36):
        rod(bpy,"OUTPUT | short timber support",
            (-.23,y,.42),(.23,y,.42),.033,m["wood"],outlet,root)
    # Wave paddle hangs north over water and swings, acting on an upper rocker.
    wave=empty(bpy,"MOTION | wave-actuated intake paddle pivot",mechanical,root)
    wave.location=(0,1.02,.72)
    rod(bpy,"WAVE | hinged long timber paddle shaft",
        (0,0,.03),(0,.29,-.32),.059,m["darkwood"],mechanical,wave)
    block(bpy,"WAVE | broad physical lifting blade",
        (0,.35,-.39),(.51,.13,.33),m["wood"],mechanical,wave,.027)
    cylinder(bpy,"WAVE | iron axle through paddle",
        (0,0,0),.098,.52,m["iron"],mechanical,wave,
        rotation=(0,math.pi/2,0),n=24)
    for x in (-.31,.31):
        rod(bpy,"WAVE | fixed supporting rocker bracket",
            (x,.96,.49),(x,1.06,.81),.031,m["iron"],mechanical,root)
    rocker=empty(bpy,"MOTION | hand-hewn twin-arm mechanical rocker",mechanical,root)
    rocker.location=(0,.55,1.50)
    rod(bpy,"ROCKER | long wood lever both sides",
        (0,-.44,0),(0,.40,0),.065,m["wood"],mechanical,rocker)
    for y in (-.32,.32):
        cylinder(bpy,"ROCKER | bronze link pin",
            (0,y,0),.088,.14,m["brass"],mechanical,rocker,
            rotation=(0,math.pi/2,0))
    cylinder(bpy,"ROCKER | stationary bearing socket",
        (0,.55,1.50),.13,.67,m["iron"],mechanical,root,
        rotation=(0,math.pi/2,0))
    for x in (-.31,.31):
        rod(bpy,"ROCKER | fixed timber A-frame",
            (x,.35,.53),(x,.55,1.49),.050,m["wood"],mechanical,root)
    bellows=empty(bpy,"MOTION | wet leather diaphragm actuator",mechanical,root)
    bellows.location=(0,.37,1.07)
    cylinder(bpy,"MOTION | leather water-lift diaphragm",
        (0,0,.03),.158,.19,m["leather"],mechanical,bellows,n=32)
    cylinder(bpy,"MOTION | exposed polished bronze piston",
        (0,0,.20),.052,.29,m["brass"],mechanical,bellows,n=20)
    # True moving connecting rod and visibly tied water paddle drive rope.
    linkage=cylinder(bpy,"MOTION | articulated rocker-to-diaphragm connecting rod",
            (0,0,0),.035,1,m["iron"],mechanical,root,n=16)
    rope=cylinder(bpy,"MOTION | taut rocker-to-paddle rope",
            (0,0,0),.021,1,m["rope"],visible,root,n=12)
    # Small visible operating sight. No unrealistically huge steam engine.
    cylinder(bpy,"SIGHT | old green glass tube",
        (.27,-.04,.95),.063,.38,m["glass"],visible,root)
    water=cylinder(bpy,"SIGHT | blue-green lifted water",
        (.27,-.04,.91),.042,.20,m["water"],visible,root,n=16)
    for z in (.76,1.16):
        cylinder(bpy,"SIGHT | crude metal retaining band",
            (.27,-.04,z),.078,.038,m["brass"],visible,root)
    cylinder(bpy,"GAUGE | circular brass frame",
            (-.25,.10,1.04),.115,.055,m["brass"],visible,root,
            rotation=(math.pi/2,0,0),n=24)
    cylinder(bpy,"GAUGE | worn white face",
            (-.25,.063,1.04),.088,.018,m["dial"],visible,root,
            rotation=(math.pi/2,0,0),n=24)
    needle=empty(bpy,"MOTION | low-pressure dial needle",visible,root)
    needle.location=(-.25,.047,1.04)
    rod(bpy,"GAUGE | black pin needle",
        (-.065,0,0),(.060,0,0),.009,m["iron"],visible,needle)
    droplets=[]
    for idx in range(3):
        d=cylinder(bpy,"MOISTURE | falling extracted water bead "+str(idx),
            (.14+.08*idx,.76,.56),.028,.064,m["water"],visible,root,n=10)
        d.hide_render=True
        d.keyframe_insert(data_path="hide_render",frame=0)
        d.hide_render=False
        d.keyframe_insert(data_path="hide_render",frame=1)
        d.keyframe_insert(data_path="hide_render",frame=LOOP)
        droplets.append(d)
    # Single deterministic loop, full 16 actual keyed poses, frame97 seam.
    for i,frame in enumerate((*FRAMES,LOOP)):
        phase=i*2*math.pi/16
        amplitude=.15*math.sin(phase)
        wave.rotation_euler.x=.13*math.sin(phase+.35)
        rocker.rotation_euler.x=amplitude
        bellows.location.z=1.07+.071*math.sin(phase)
        bellows.scale.z=1+.10*math.sin(phase)
        needle.rotation_euler.y=.11*math.sin(phase+.4)
        for ob,data_path in ((wave,"rotation_euler"),(rocker,"rotation_euler"),
                             (bellows,"location"),(bellows,"scale"),
                             (needle,"rotation_euler")):
            ob.keyframe_insert(data_path=data_path,frame=frame)
        # Geometry-length link actually joins the lever end and diaphragm top.
        pivot=Vector((0,.55,1.50))
        lever_end=pivot+Vector((0,-.34*math.cos(amplitude),-.34*math.sin(amplitude)))
        diaphragm=Vector((0,.37,1.25+.071*math.sin(phase)))
        d=lever_end-diaphragm
        linkage.location=(lever_end+diaphragm)/2
        linkage.rotation_euler=d.to_track_quat("Z","Y").to_euler()
        linkage.scale.z=d.length
        # Secondary rope couples paddle tip to the rocker water-side arm.
        wave_angle=wave.rotation_euler.x
        paddle=Vector((0,1.02+.22*math.cos(wave_angle)+.25*math.sin(wave_angle),
                       .72+.22*math.sin(wave_angle)-.25*math.cos(wave_angle)))
        rocker_end=pivot+Vector((0,.36*math.cos(amplitude),.36*math.sin(amplitude)))
        delta=rocker_end-paddle
        rope.location=(paddle+rocker_end)/2
        rope.rotation_euler=delta.to_track_quat("Z","Y").to_euler()
        rope.scale.z=delta.length
        for ob in (linkage,rope):
            for data_path in ("location","rotation_euler","scale"):
                ob.keyframe_insert(data_path=data_path,frame=frame)
        for idx,bead in enumerate(droplets):
            t=(i+idx*5)%16/16
            bead.location.z=.58-.40*t
            bead.keyframe_insert(data_path="location",frame=frame)
    wave.rotation_euler.x=0
    rocker.rotation_euler.x=0
    needle.rotation_euler.y=0
    bellows.location.z=1.07
    bellows.scale.z=1
    return root,fixed,pbr

def native_geometry_check(bpy,c,root,ports):
    scene=bpy.context.scene
    assert len(ports)==2 and all(o.parent is root and len(o.data.vertices)==256 for o in ports)
    assert {o.name for o in ports}=={
        "PORT | south output | machine_collar","PORT | south output | machine_throat"}
    assert len([o for o in scene.objects if o.type=="CAMERA"])==1
    assert scene.camera.data.type=="ORTHO" and scene.camera.parent is None
    assert abs(scene.camera.data.ortho_scale-3.75)<1e-6
    assert not any("TEMP FIXTURE" in o.name or "REF |" in o.name for o in scene.objects)
    assert sum(o.name.startswith("ANCHOR | separate") for o in scene.objects)==4
    assert sum(o.name.startswith("DOCK | narrow separated") for o in scene.objects)==8
    assert not any("slab" in o.name.lower() for o in scene.objects)
    assert {tuple(o["native_cell"]) for o in ports}=={(0,.25)}
    assert {tuple(o["blender_joint"]) for o in ports}=={(0,-.49,.36)}
    scene.frame_set(1)
    bpy.context.view_layer.update()
    ref=[o.matrix_world.copy() for o in ports]
    rocker=bpy.data.objects["MOTION | hand-hewn twin-arm mechanical rocker"]
    bellows=bpy.data.objects["MOTION | wet leather diaphragm actuator"]
    wave=bpy.data.objects["MOTION | wave-actuated intake paddle pivot"]
    first=(rocker.rotation_euler.x,bellows.location.z,wave.rotation_euler.x)
    travel=[]
    for frame in (1,7,13,25,49,73,91,97):
        scene.frame_set(frame);bpy.context.view_layer.update()
        travel.append(bellows.location.z)
        for o,mat in zip(ports,ref):
            diff=max(abs(a-b) for ra,rb in zip(o.matrix_world,mat) for a,b in zip(ra,rb))
            if diff>1e-6:raise RuntimeError("Native south output moved in Blender: "+str(frame))
    assert max(travel)-min(travel)>.13
    scene.frame_set(97)
    assert abs(rocker.rotation_euler.x-first[0])<1e-6
    assert abs(wave.rotation_euler.x-first[2])<1e-6
    assert abs(bellows.location.z-first[1])<1e-6
    scene.frame_set(0)
    return {"rigid_template_meshes":2,"vertices_per_mesh":256,
            "native_output_position":[0,.25],"visible_outlet_xyz":[0,-.49,.36],
            "intake_offset":[0,-1],"separate_stone_feet":4,
            "bellows_travel_bu":max(travel)-min(travel),"frame97_seam":True}

def build(args):
    import bpy
    c=preflight()
    out=args.out.resolve()
    if out.exists():raise FileExistsError("Refuse existing output directory: "+str(out))
    bpy.ops.wm.read_factory_settings(use_empty=True)
    camera(bpy,c)
    bpy.context.scene.cycles.samples=args.samples
    root,ports,materials=model(bpy,c)
    checks=native_geometry_check(bpy,c,root,ports)
    out.mkdir(parents=True,exist_ok=False)
    master=out/"beach-pump-v1.blend"
    bpy.ops.file.pack_all()
    bpy.ops.wm.save_as_mainfile(filepath=str(master),compress=True,check_existing=False)
    report={
        "schema":"tanks.beach-pump.v1.native-blender",
        "asset":"beachpump","factorio_prototype":"offshore-pump/beachpump",
        "master_sha256":sha(master),"fluid_fixture_sha256":c["fixture"]["sha256"],
        "pbr_material_donor_sha256":c["pbr_donor"]["sha256"],
        "fmpl_materials":materials,"prototype":c["entity"],
        "orientation_degrees":list(DIRECTIONS),"fps":8,"working_frames":list(FRAMES),
        "geometry_qa":checks,
        "render_mode":args.render,"renders":[],"render_count":0,
        "game_integrated":False,"human_approved":False}
    manifest=out/"build-report.json"
    manifest.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    if args.render!="none":
        frame_indices=range(16) if args.render=="all" else (4,)
        for direction,deg in enumerate(DIRECTIONS):
            root.rotation_euler.z=math.radians(deg)
            for state,indices in (("idle",(-1,)),("working",frame_indices)):
                for index in indices:
                    frame=0 if index<0 else FRAMES[index]
                    bpy.context.scene.frame_set(frame)
                    bpy.context.view_layer.update()
                    name=(f"idle-d{direction:02d}.png" if index<0 else
                          f"working-d{direction:02d}-f{index:03d}.png")
                    bpy.context.scene.render.filepath=str(out/name)
                    bpy.ops.render.render(write_still=True)
                    report["renders"].append({
                        "file":name,"sha256":sha(out/name),"state":state,
                        "direction":direction,"index":index,"frame":frame})
                    manifest.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    report["render_count"]=len(report["renders"])
    assert report["render_count"]=={"none":0,"proof":8,"all":68}[args.render]
    manifest.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print("TANKS_BEACH_PUMP_V1_REAL_BLENDER_BUILT",report["render_count"],
          "source="+report["master_sha256"],flush=True)

def main():
    if "--self-check" in sys.argv:
        preflight()
        print("TANKS_BEACH_PUMP_SOURCE_CONTRACT_PASS",flush=True)
        return
    p=argparse.ArgumentParser()
    p.add_argument("--out",type=Path,required=True)
    p.add_argument("--render",choices=("none","proof","all"),default="proof")
    p.add_argument("--samples",type=int,default=16)
    args=p.parse_args(sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else sys.argv[1:])
    if not 4<=args.samples<=64:raise ValueError("Cycles samples 4..64 only")
    build(args)
if __name__=="__main__":
    main()
