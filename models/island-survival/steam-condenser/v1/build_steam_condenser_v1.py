#!/usr/bin/env python3
"""Native Tanks 3x3 Steam Condenser: source-only Blender build and four-way proof.

NOT a copy of the 2x2 Tech-Priests emergency condenser. Uses verified full-bore
Tanks fluid-interface fixtures, packed FMPL ferrocrete PBR from the approved V8
Solar Boiler, purpose-built visible geometry, one 45deg camera, 16-frame motion.
Build writes to a fresh output directory; NEVER edits a mod, source or workflow.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
CONTRACT = HERE / "contract.json"
FRAME_IDS = tuple(range(1, 92, 6))
YAW = (0, 90, 180, 270)
LOOP = 97

def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def preflight():
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    assert contract["prototype"] == "assembling-machine/steam-condenser"
    assert contract["footprint_tiles"] == [3, 3]
    assert len(contract["fixed_native_fluid_boxes"]) == 2
    assert tuple(contract["capture"]["working_frames"]) == FRAME_IDS
    assert tuple(contract["capture"]["fixed_yaws_deg"]) == YAW
    assert contract["capture"]["exact_loop_seam_frame"] == LOOP
    assert contract["capture"]["fps"] == 8
    assert contract["fluid_fixture"]["interface_id"] == "factorio-fluid-interface-v1"
    for spec, expected in zip(contract["fixed_native_fluid_boxes"], (
        ("steam-north", "input", (0,-1), (0,1.5,.36), "N"),
        ("water-south", "output", (0,1), (0,-1.5,.36), "S"),
    )):
        assert (spec["id"], spec["type"], tuple(spec["native_cell"]),
                tuple(spec["flange_blender_xyz"]), spec["fixture_facing"]) == expected
    for source in ("fluid_fixture", "packed_pbr_donor"):
        reference = ROOT / contract[source]["path"]
        if not reference.is_file():
            raise FileNotFoundError("Missing approved reference: " + str(reference))
        if digest(reference) != contract[source]["sha256"]:
            raise ValueError("Source identity changed: " + str(reference))
    return contract

def material(bpy, name, rgba, metal=0.0, rough=.65, transmission=0.0):
    mat = bpy.data.materials.new("TANKS CONDENSER | " + name)
    mat.diffuse_color = rgba
    mat.use_nodes = True
    p = mat.node_tree.nodes.get("Principled BSDF")
    p.inputs["Base Color"].default_value = rgba
    p.inputs["Metallic"].default_value = metal
    p.inputs["Roughness"].default_value = rough
    t = p.inputs.get("Transmission Weight")
    if t is not None:
        t.default_value = transmission
    if name in ("driftwood", "iron", "copper"):
        tex = mat.node_tree.nodes.new("ShaderNodeTexNoise")
        tex.inputs["Scale"].default_value = 31
        tex.inputs["Detail"].default_value = 3
        bump = mat.node_tree.nodes.new("ShaderNodeBump")
        bump.inputs["Strength"].default_value = .12
        bump.inputs["Distance"].default_value = .003
        mat.node_tree.links.new(tex.outputs["Fac"], bump.inputs["Height"])
        mat.node_tree.links.new(bump.outputs["Normal"], p.inputs["Normal"])
    return mat

def source_materials(bpy, contract):
    donor = ROOT / contract["packed_pbr_donor"]["path"]
    with bpy.data.libraries.load(str(donor), link=False) as (source, target):
        names = [n for n in source.materials if
                 contract["packed_pbr_donor"]["required_material_substring"].lower() in n.lower()]
        if not names:
            raise RuntimeError("Approved V8 packed FMPL ferrocrete materials not found")
        target.materials = names
    candidates = [m for m in target.materials if m is not None]
    if not candidates:
        raise RuntimeError("FMPL packed PBR material data failed to append")
    pbr = next((m for m in candidates if "ferrocrete" in m.name.lower()
                and "dark" not in m.name.lower()), candidates[0])
    return {
        "concrete": pbr,
        "driftwood": material(bpy, "driftwood", (.27,.165,.089,1), .08,.81),
        "iron": material(bpy, "iron", (.22,.25,.27,1), .78,.58),
        "copper": material(bpy, "copper", (.46,.24,.10,1), .76,.39),
        "brass": material(bpy, "brass", (.60,.42,.14,1), .80,.43),
        "glass": material(bpy, "cloudy condenser glass", (.18,.43,.45,1), .05,.16,.36),
        "water": material(bpy, "condensed water", (.065,.36,.48,1), .05,.19,.19),
        "cooling": material(bpy, "ribbed cooling metal", (.16,.22,.23,1), .54,.71),
        "steam": material(bpy, "pale steam jets", (.74,.80,.80,.45), .0,.90,.18),
        "dial": material(bpy, "aged dial", (.73,.67,.47,1), .13,.62)
    }, [m.name for m in candidates]

def collection(bpy, name):
    c = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(c)
    return c

def make_root(bpy, name, c=None, parent=None):
    obj = bpy.data.objects.new(name, None)
    if c is None:
        bpy.context.scene.collection.objects.link(obj)
    else:
        c.objects.link(obj)
    obj.parent = parent
    return obj

def reparent(bpy, obj, c, root):
    for old in tuple(obj.users_collection):
        old.objects.unlink(obj)
    c.objects.link(obj)
    obj.parent = root
    return obj

def cube(bpy, name, pos, dimensions, mat, c, root, bevel=.015):
    bpy.ops.mesh.primitive_cube_add(size=1, location=pos)
    o = reparent(bpy, bpy.context.object, c, root)
    o.name = name
    o.scale = dimensions
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    o.data.materials.append(mat)
    if bevel:
        m = o.modifiers.new("Soft edge", "BEVEL")
        m.width = min(bevel, min(dimensions)*.17)
        m.segments = 2
        o.modifiers.new("Stable normals", "WEIGHTED_NORMAL")
    return o

def cylinder(bpy, name, pos, radius, depth, mat, c, root,
             rotation=(0,0,0), vertices=32):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius,
                                        depth=depth, location=pos, rotation=rotation)
    o = reparent(bpy, bpy.context.object, c, root)
    o.name = name
    o.data.materials.append(mat)
    for f in o.data.polygons:
        if len(f.vertices) == 4:
            f.use_smooth = True
    return o

def rod(bpy, name, start, end, radius, mat, c, root):
    from mathutils import Vector
    v0, v1 = Vector(start), Vector(end)
    delta = v1-v0
    if delta.length < 1e-6:
        raise ValueError("Zero-length pipe section " + name)
    o = cylinder(bpy, name, (v0+v1)/2, radius, delta.length, mat, c, root)
    o.rotation_euler = delta.to_track_quat("Z","Y").to_euler()
    return o

def curve_tube(bpy, name, points, radius, mat, c, root):
    if len(points) < 2:
        raise ValueError("Pipe must have at least two control vertices")
    curve = bpy.data.curves.new(name, "CURVE")
    curve.dimensions = "3D"
    curve.resolution_u = 18
    curve.bevel_depth = radius
    curve.bevel_resolution = 4
    path = curve.splines.new("POLY")
    path.points.add(len(points)-1)
    for p, v in zip(path.points, points):
        p.co = (float(v[0]), float(v[1]), float(v[2]), 1)
    ob = bpy.data.objects.new(name, curve)
    c.objects.link(ob)
    ob.parent = root
    ob.data.materials.append(mat)
    return ob

def install_ports(bpy, contract, mats, root, port_collection):
    helper_path = ROOT / "models/reference/factorio-fluid-interface/append_reference.py"
    sys.path.insert(0, str(helper_path.parent))
    try:
        from append_reference import append_interface
    finally:
        sys.path.pop(0)
    reference_path = ROOT / contract["fluid_fixture"]["path"]
    imported = []
    for entry in contract["fixed_native_fluid_boxes"]:
        label = entry["id"]
        fixture, ref_root = append_interface(reference_path,
            joint_ground=(0,entry["flange_blender_xyz"][1],0),
            facing=entry["fixture_facing"],
            name="CONDENSER FIXTURE | " + label)
        bpy.context.view_layer.update()
        roles = {obj.get("interface_role"): obj for obj in fixture.all_objects}
        for role in ("machine_collar", "machine_throat"):
            src = roles[role]
            transform = src.matrix_world.copy()
            new = src.copy()
            new.data = src.data.copy()
            new.name = "PORT | " + label + " | " + role
            port_collection.objects.link(new)
            new.parent = root
            new.matrix_world = transform
            new["fixed_native_cell"] = entry["native_cell"]
            new["fixed_role"] = role
            new["joint_ground"] = [0,entry["flange_blender_xyz"][1],0]
            new["canonical_interface_sha256"] = contract["fluid_fixture"]["sha256"]
            new.data.materials.clear()
            new.data.materials.append(mats["iron"] if role=="machine_throat" else mats["brass"])
            if role == "machine_collar":
                imported.append(new)
        for obj in list(fixture.all_objects):
            bpy.data.objects.remove(obj, do_unlink=True)
        bpy.data.collections.remove(fixture)
    if len(imported)!=2:
        raise AssertionError("Both full-bore imported machine collars required")
    for p in imported:
        if len(p.data.vertices) != 256:
            raise AssertionError("Reference machine collar has invalid geometry")
    return imported

def setup_capture(bpy, contract):
    from mathutils import Vector
    scene = bpy.context.scene
    cam = bpy.data.cameras.new("Tanks fixed 45 degree ortho")
    camera = bpy.data.objects.new("FMPL_CAPTURE_CAMERA",cam)
    scene.collection.objects.link(camera)
    camera.location = tuple(contract["capture"]["fixed_camera"])
    camera.rotation_euler = tuple(math.radians(x) for x in
                                  contract["capture"]["camera_rotation_deg"])
    cam.type = "ORTHO"
    cam.ortho_scale = contract["capture"]["camera_ortho_scale"]
    scene.camera = camera
    for name,position,power,size in (
        ("Key area",(-3,-4,7),830,5),
        ("Fill area",(4,3,6),530,4),
    ):
        light = bpy.data.lights.new(name,"AREA")
        light.energy=power
        light.shape="DISK"
        light.size=size
        obj=bpy.data.objects.new(name,light)
        scene.collection.objects.link(obj)
        obj.location=position
        obj.rotation_euler=(Vector((0,0,1.0))-obj.location).to_track_quat("-Z","Y").to_euler()
    world = bpy.data.worlds.new("Nauvis neutral ambient")
    world.use_nodes=True
    world.node_tree.nodes.get("Background").inputs["Strength"].default_value=.47
    scene.world=world
    scene.render.engine="CYCLES"
    scene.cycles.device="CPU"
    scene.cycles.samples=16
    scene.render.resolution_x=scene.render.resolution_y=256
    scene.render.resolution_percentage=100
    scene.render.image_settings.file_format="PNG"
    scene.render.image_settings.color_mode="RGBA"
    scene.render.film_transparent=True
    scene.render.fps=8
    scene.frame_end=LOOP

def create_machine(bpy, contract):
    scene=bpy.context.scene
    mats, imported_names=source_materials(bpy,contract)
    base=collection(bpy,"01 | separate 3x3 concrete footings")
    body=collection(bpy,"02 | wooden copper condensation vessel")
    pipes=collection(bpy,"03 | fluid pipes, real north and south fittings")
    drive=collection(bpy,"04 | mechanical rotor and cooling")
    effects=collection(bpy,"05 | visible cycling moisture, water and steam")
    root=make_root(bpy,"EXPORT | rotate Tanks Steam Condenser, never camera")
    root["footprint_tiles"]=[3,3]
    root["source_name"]="tanks/steam-condenser-v1"
    for x in (-1.08,1.08):
        for y in (-1.04,1.04):
            cube(bpy,"FRAME | isolated ferrocrete support",(x,y,.10),
                 (.55,.52,.20),mats["concrete"],base,root,.017)
            cube(bpy,"FRAME | weathered timber bearer",(x,y,.26),
                 (.40,.37,.15),mats["driftwood"],base,root)
    for x in (-1.12,1.12):
        rod(bpy,"FRAME | copper upright",(x,0,.26),(x,0,1.79),
            .065,mats["copper"],body,root)
    for z in (.35,1.54):
        for x in (-1.10,1.10):
            rod(bpy,"FRAME | lateral brace",(x,-.92,z),(x,.92,z),
                .07,mats["driftwood"],body,root)
    # Original new 3x3 body, not imported 2x2 geometry.
    cylinder(bpy,"VESSEL | pressure drum",(0,0,.99),.68,1.35,
             mats["driftwood"],body,root,vertices=48)
    for theta in range(0,360,30):
        a=math.radians(theta)
        x,y=.682*math.cos(a),.682*math.sin(a)
        rod(bpy,"VESSEL | separate stave",(x,y,.35),(x,y,1.65),
            .045,mats["driftwood"],body,root)
    for z in (.43,1.56):
        cylinder(bpy,"VESSEL | bronze hoop",(0,0,z),.722,.065,
                 mats["brass"],body,root,vertices=64)
    cylinder(bpy,"VESSEL | closed copper crown",(0,0,1.70),.73,.17,
             mats["copper"],body,root)
    cylinder(bpy,"VESSEL | bottom cistern",(0,0,.30),.75,.21,
             mats["iron"],body,root)
    # Identically sized authored machine collars from verified reusable fixture.
    collars=install_ports(bpy,contract,mats,root,pipes)
    # Rigidity: these two pipe runs are rooted directly in the stationary body.
    curve_tube(bpy,"PIPE | incoming north steam elbow",
        [(0,1.47,.36),(0,.99,.36),(0,.99,1.39),(0,.66,1.39)],
        .265,mats["iron"],pipes,root)
    curve_tube(bpy,"PIPE | south liquid drain from sump",
        [(0,-.62,.35),(0,-1.47,.36)],.265,mats["copper"],pipes,root)
    for y in (-1.05,-.82,.82,1.05):
        cube(bpy,"FRAME | lateral bracing",(0,y,.26),
            (1.65,.10,.12),mats["driftwood"],base,root)
    # External heat-exchanger bank with actual tubing, not cosmetic rings.
    for k in range(6):
        z=.78+k*.21
        curve_tube(bpy,"COOLING | copper serpentine row "+str(k),
            [(-.91,-.60,z),(-1.10,-.37,z),
             (-1.10,.38,z),(-.90,.60,z)],.060,
            mats["copper"],body,root)
        for y in (-.42,-.18,.06,.30):
            cube(bpy,"COOLING | fin",(-1.15,y,z),
                (.18,.105,.13),mats["cooling"],body,root,.006)
    # Glass condensate readout: intentionally visible blue-green liquid.
    cylinder(bpy,"GLASS | inspectable sight tube",(.83,-.18,1.03),
             .122,.72,mats["glass"],effects,root)
    cylinder(bpy,"GLASS | visibly blue retained water",(.83,-.18,.89),
             .082,.36,mats["water"],effects,root)
    for z in (.67,1.39):
        cylinder(bpy,"GLASS | sealed brass cap",(.83,-.18,z),
            .145,.06,mats["brass"],effects,root)
    cylinder(bpy,"GAUGE | steam pressure bezel",(.64,-.75,1.70),
        .18,.085,mats["brass"],effects,root,rotation=(math.pi/2,0,0))
    cylinder(bpy,"GAUGE | paper dial",(.64,-.805,1.70),
        .137,.013,mats["dial"],effects,root,rotation=(math.pi/2,0,0))
    gauge=make_root(bpy,"GAUGE | pressure needle keyed",effects,root)
    gauge.location=(.64,-.83,1.70)
    rod(bpy,"GAUGE | thin needle",(-.09,0,0),(.10,0,0),
        .008,mats["iron"],effects,gauge)
    # An anchored vane assembly drives visible sequential circulation.
    rotor=make_root(bpy,"COOLING | rotating vane drive",drive,root)
    rotor.location=(0,0,1.92)
    cylinder(bpy,"COOLING | central bearing",(0,0,0),
        .18,.12,mats["iron"],drive,rotor)
    for k in range(4):
        a=math.radians(90*k)
        rod(bpy,"COOLING | fixed-length rotating paddle",
            (.12*math.cos(a),.12*math.sin(a),.01),
            (.42*math.cos(a),.42*math.sin(a),.01),
            .065,mats["copper"],drive,rotor)
    for k in range(4):
        a=2*math.pi*k/4
        # Droplets are separate 3D geometry with independent keyed descent.
        droplet=cylinder(bpy,"MOISTURE | condensed falling droplet "+str(k),
            (.34*math.cos(a),.34*math.sin(a),1.36),
            .036,.083,mats["water"],effects,root,vertices=12)
        for j,frame in enumerate((*FRAME_IDS,LOOP)):
            phase=(j+k*4)%16/16
            droplet.location.z=1.30-.80*phase
            droplet.keyframe_insert(data_path="location",frame=frame)
    steam=cylinder(bpy,"STEAM | visible intermittent north-intake mist",
        (0,.89,.98),.13,.24,mats["steam"],effects,root,vertices=16)
    # Only the small mist moves; fittings and all external pipe paths do not.
    for j,frame in enumerate((*FRAME_IDS,LOOP)):
        a=2*math.pi*j/16
        rotor.rotation_euler.z=a
        rotor.keyframe_insert(data_path="rotation_euler",frame=frame)
        gauge.rotation_euler.y=.16*math.sin(a)
        gauge.keyframe_insert(data_path="rotation_euler",frame=frame)
        steam.scale=(1+.08*math.sin(a),1+.07*math.sin(a),.73+.20*math.sin(a+1.1))
        steam.keyframe_insert(data_path="scale",frame=frame)
    rotor.rotation_euler.z=0
    gauge.rotation_euler.y=0
    steam.scale=(1,1,1)
    return root, collars, imported_names

def native_checks(bpy, contract, root, collars):
    from mathutils import Vector
    scene=bpy.context.scene
    assert len(collars)==2 and all(o.parent is root for o in collars)
    assert len([o for o in scene.objects if o.type=="CAMERA"])==1
    assert scene.camera.data.type=="ORTHO"
    assert abs(scene.camera.data.ortho_scale-contract["capture"]["camera_ortho_scale"])<1e-5
    assert list(root["footprint_tiles"])==[3,3]
    for collar,entry in zip(collars,contract["fixed_native_fluid_boxes"]):
        assert tuple(collar["fixed_native_cell"]) == tuple(entry["native_cell"])
        assert collar["canonical_interface_sha256"] == contract["fluid_fixture"]["sha256"]
        assert len(collar.data.vertices)==256
    scene.frame_set(1);bpy.context.view_layer.update()
    baseline=[o.matrix_world.copy() for o in collars]
    for frame in (7,25,49,73,91,LOOP):
        scene.frame_set(frame);bpy.context.view_layer.update()
        for o,first in zip(collars,baseline):
            if max(abs(v-w) for a,b in zip(o.matrix_world,first) for v,w in zip(a,b))>1e-6:
                raise RuntimeError("Moving fluid fitting, frame "+str(frame))
    scene.frame_set(0)
    return {"stable_full_bore_collars":2,"unchanged_port_motion_bu":0,
            "camera":list(scene.camera.location),"ortho_scale":scene.camera.data.ortho_scale}

def build(args):
    import bpy
    contract=preflight()
    out=args.output.resolve()
    if out.exists():
        raise FileExistsError("New source must not overwrite a previous directory: "+str(out))
    bpy.ops.wm.read_factory_settings(use_empty=True)
    setup_capture(bpy,contract)
    bpy.context.scene.cycles.samples=args.samples
    root,collars,material_names=create_machine(bpy,contract)
    checks=native_checks(bpy,contract,root,collars)
    out.mkdir(parents=True)
    master=out/"steam-condenser-v1.blend"
    bpy.ops.file.pack_all()
    bpy.ops.wm.save_as_mainfile(filepath=str(master),compress=True,check_existing=False)
    report={"schema":"tanks.steam-condenser.v1.native-proof",
            "native_sha256":digest(master),
            "fluid_fixture_sha256":contract["fluid_fixture"]["sha256"],
            "pbr_donor_sha256":contract["packed_pbr_donor"]["sha256"],
            "fmpl_materials_loaded":material_names,
            "footprint":[3,3],"fluid_ports":contract["fixed_native_fluid_boxes"],
            "proof_checks":checks,
            "camera":"single 45deg orthographic fixed camera",
            "fps":8,"directions":list(YAW),"frames":list(FRAME_IDS),
            "render_mode":args.render,"renders":[],
            "game_integrated":False,"owner_visual_approved":False}
    report_path=out/"build-report.json"
    report_path.write_text(json.dumps(report,indent=2)+"\n")
    if args.render!="none":
        frames=range(16) if args.render=="all" else (4,)
        for d,deg in enumerate(YAW):
            root.rotation_euler.z=math.radians(deg)
            for state,seq in (("idle",(-1,)),("working",frames)):
                for k in seq:
                    timeline=0 if k<0 else FRAME_IDS[k]
                    bpy.context.scene.frame_set(timeline)
                    bpy.context.view_layer.update()
                    name=("idle-d%02d.png"%d if k<0 else
                          "working-d%02d-f%03d.png"%(d,k))
                    bpy.context.scene.render.filepath=str(out/name)
                    bpy.ops.render.render(write_still=True)
                    report["renders"].append({"state":state,"direction":d,
                                              "index":k,"frame":timeline,
                                              "file":name,"sha256":digest(out/name)})
                    report_path.write_text(json.dumps(report,indent=2)+"\n")
    root.rotation_euler.z=0
    bpy.context.scene.frame_set(0)
    report["render_count"]=len(report["renders"])
    expected={"none":0,"proof":8,"all":68}[args.render]
    if report["render_count"]!=expected:
        raise RuntimeError("Missing native rendered frame")
    report_path.write_text(json.dumps(report,indent=2)+"\n")
    print("TANKS_STEAM_CONDENSER_NATIVE_SOURCE_PASS",report["render_count"],digest(master),flush=True)

def main():
    if "--self-check" in sys.argv:
        preflight()
        print("TANKS_STEAM_CONDENSER_3X3_SOURCE_CONTRACT_PASS",flush=True)
        return
    p=argparse.ArgumentParser()
    p.add_argument("--output",type=Path,required=True)
    p.add_argument("--samples",type=int,default=16)
    p.add_argument("--render",choices=("none","proof","all"),default="proof")
    a=p.parse_args(sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else sys.argv[1:])
    if not (4<=a.samples<=64):
        raise ValueError("Bounded Cycles sample count 4..64")
    build(a)

if __name__=="__main__":
    main()
