#!/usr/bin/env python3
"""Primitive Lumberyard V1: real editable Factorio-angled Blender model and four-way animation.

Asset replaces conceptually the old growing-plot artwork, but does NOT change
any live prototypes. Grounded purpose: whole round logs -> crude splitter ->
stacks of lengthwise HALF logs, not sawn end-grain discs.
"""
import argparse
import hashlib
import json
import math
import random
import sys
from pathlib import Path

import bpy
from mathutils import Vector

DIRECTIONS=(0,90,180,270)
FRAMES=tuple(range(1,17))
SEAM_FRAME=17
RNG=random.Random(40261107)

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def collection(name):
    col=bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(col)
    return col

def into(obj,col):
    for c in list(obj.users_collection):c.objects.unlink(obj)
    col.objects.link(obj)
    return obj

def material(name,dark,light,rough=.92,scale=6.0):
    m=bpy.data.materials.new(name)
    m.use_nodes=True
    nodes=m.node_tree.nodes
    bsdf=nodes.get("Principled BSDF")
    bsdf.inputs["Roughness"].default_value=rough
    if bsdf.inputs.get("Specular IOR Level"):
        bsdf.inputs["Specular IOR Level"].default_value=.1
    noise=nodes.new("ShaderNodeTexNoise")
    noise.inputs["Scale"].default_value=scale
    noise.inputs["Detail"].default_value=3.0
    ramp=nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].position=.18
    ramp.color_ramp.elements[0].color=(*dark,1)
    ramp.color_ramp.elements[1].position=.82
    ramp.color_ramp.elements[1].color=(*light,1)
    m.node_tree.links.new(noise.outputs["Fac"],ramp.inputs["Fac"])
    m.node_tree.links.new(ramp.outputs["Color"],bsdf.inputs["Base Color"])
    return m

def box(name,loc,size,mat,col,bevel=.016,rotation=0):
    bpy.ops.mesh.primitive_cube_add(size=1,location=loc)
    ob=into(bpy.context.object,col)
    ob.name=name
    ob.dimensions=size
    ob.rotation_euler.z=rotation
    bpy.context.view_layer.objects.active=ob
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    if bevel:
        mod=ob.modifiers.new("rough relieved edges","BEVEL")
        mod.width=bevel
        mod.segments=2
        ob.modifiers.new("smoothed face normals","WEIGHTED_NORMAL")
        for p in ob.data.polygons:p.use_smooth=True
    ob.data.materials.append(mat)
    return ob

def beam(name,a,b,r,material,col,verts=8):
    a,b=Vector(a),Vector(b)
    vec=b-a
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts,radius=r,depth=vec.length,
                                        location=(a+b)*.5)
    ob=into(bpy.context.object,col)
    ob.name=name
    ob.rotation_euler=vec.to_track_quat("Z","Y").to_euler()
    ob.data.materials.append(material)
    return ob

def primitive_log(name,center,length,r,bark,endgrain,col,seed=0):
    """One real trunk oriented along Y, with bark side and two exposed end-grain caps."""
    rng=random.Random(47+seed)
    n=16
    verts=[]
    x,y,z=center
    for side in (-1,1):
        yy=y+side*length*.5
        for i in range(n):
            angle=2*math.pi*i/n
            jitter=r*(1+rng.uniform(-.028,.028))
            verts.append((x+jitter*math.cos(angle),yy,z+jitter*math.sin(angle)))
    faces=[];inds=[]
    for i in range(n):
        j=(i+1)%n
        faces.append((i,j,j+n,i+n));inds.append(0)
    faces.append(tuple(range(n-1,-1,-1)));inds.append(1)
    faces.append(tuple(range(n,n*2)));inds.append(1)
    mesh=bpy.data.meshes.new(name+" mesh")
    mesh.from_pydata(verts,[],faces)
    mesh.materials.append(bark)
    mesh.materials.append(endgrain)
    mesh.update()
    for p,i in zip(mesh.polygons,inds):
        p.material_index=i
        p.use_smooth=i==0
    ob=bpy.data.objects.new(name,mesh)
    col.objects.link(ob)
    return ob

def split_half(name,center,length,r,bark,cut,endgrain,col,seed=0):
    """A split trunk half, flat pale inner face UP, curved bark below.

    True D-shaped cross section, no full cylinder hidden under a paint stripe.
    """
    x,y,z=center
    n=12
    verts=[]
    for side in (-1,1):
        yy=y+side*length*.5
        for i in range(n+1):
            theta=math.pi*i/n
            verts.append((x+r*math.cos(theta),yy,z-r*math.sin(theta)))
    count=n+1
    faces=[];mids=[]
    for i in range(n):
        faces.append((i,i+1,i+1+count,i+count));mids.append(0)
    faces.append((0,count,count+n,n));mids.append(1)
    faces.append(tuple(range(count-1,-1,-1)));mids.append(2)
    faces.append(tuple(range(count,count*2)));mids.append(2)
    mesh=bpy.data.meshes.new(name+" mesh")
    mesh.from_pydata(verts,[],faces)
    mesh.update()
    for m in (bark,cut,endgrain):mesh.materials.append(m)
    for p,idx in zip(mesh.polygons,mids):
        p.material_index=idx
        p.use_smooth=(idx==0)
    ob=bpy.data.objects.new(name,mesh)
    col.objects.link(ob)
    return ob

def wedge(name,base_z,col,stone):
    """Visible thick, crude splitting blade: wide at top, narrow edge at bottom."""
    half_y=.55
    verts=[
        (-.19,-half_y,base_z+.34),(.19,-half_y,base_z+.34),
        (.19,half_y,base_z+.34),(-.19,half_y,base_z+.34),
        (-.012,-half_y,base_z),(.012,-half_y,base_z),
        (.012,half_y,base_z),(-.012,half_y,base_z)]
    faces=[(0,1,2,3),(4,7,6,5),(0,4,5,1),
           (3,2,6,7),(0,3,7,4),(1,5,6,2)]
    me=bpy.data.meshes.new(name+" blade mesh")
    me.from_pydata(verts,[],faces);me.update()
    ob=bpy.data.objects.new(name,me)
    col.objects.link(ob);ob.data.materials.append(stone)
    return ob

def earth_patch(col,mat):
    """Slightly irregular low patch. No tile-square or invisible underside."""
    edges=20
    verts=[(0,0,-.17)]
    for i in range(edges):
        t=2*math.pi*i/edges
        swell=1+.06*math.sin(3*t+.3)+.035*math.cos(7*t)
        verts.append((1.94*math.cos(t)*swell,
                      1.82*math.sin(t)*swell,-.16+.015*math.sin(5*t)))
    faces=[(0,i+1,(i+1)%edges+1) for i in range(edges)]
    me=bpy.data.meshes.new("primitive yard disturbed soil mesh")
    me.from_pydata(verts,[],faces);me.update()
    ob=bpy.data.objects.new("GROUND | compacted worksite soil outline",me)
    col.objects.link(ob);me.materials.append(mat)
    return ob

def key_discrete(ob,t,visible):
    ob.hide_render=not visible
    ob.keyframe_insert(data_path="hide_render",frame=t)
    for fc in ob.animation_data.action.fcurves:
        if fc.data_path=="hide_render":
            for k in fc.keyframe_points:k.interpolation="CONSTANT"

def animate(machine,full,halves,chip,col):
    """Sixteen-frame crude press action; log splits lengthwise, two halves shift apart."""
    for idx,frame in enumerate(list(FRAMES)+[SEAM_FRAME]):
        phase=idx%16
        # Raised -> descends -> strikes -> lifts, with a hard reset at next cycle.
        plunge=(0,.05,.10,.19,.33,.48,.52,.52,.45,.30,.16,.07,0,0,0,0)[phase]
        machine.location.z=-plunge
        machine.keyframe_insert(data_path="location",frame=frame)
        showing=(phase<7)
        key_discrete(full,frame,showing)
        key_discrete(halves[0],frame,not showing)
        key_discrete(halves[1],frame,not showing)
        spread=(0,0,0,0,0,0,0,.06,.12,.18,.24,.29,.31,.31,.31,.31)[phase]
        for i,h in enumerate(halves):
            h.location.x=(-1 if i==0 else 1)*spread
            h.keyframe_insert(data_path="location",frame=frame)
        # Small visible wood chips burst at the splitting moment.
        for j,c in enumerate(chip):
            alive=7<=phase<=10
            key_discrete(c,frame,alive)
            c.location.z=(.13+.07*j)+(phase-7)*.065 if alive else .10+.07*j
            c.keyframe_insert(data_path="location",frame=frame)
    for ob in [machine]+list(halves)+list(chip):
        if not ob.animation_data:continue
        for fc in ob.animation_data.action.fcurves:
            if fc.data_path=="hide_render":continue
            for k in fc.keyframe_points:
                k.interpolation="BEZIER"
                k.handle_left_type=k.handle_right_type="AUTO_CLAMPED"

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--out",type=Path,required=True)
    parser.add_argument("--samples",type=int,default=20)
    args=parser.parse_args(sys.argv[sys.argv.index("--")+1:])
    out=args.out.resolve()
    if out.exists() and any(out.iterdir()):
        raise ValueError("New/empty output directory required; preserve previous asset revisions")
    out.mkdir(parents=True,exist_ok=True)
    scene=bpy.context.scene
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    scene.render.engine="CYCLES"
    scene.cycles.device="CPU"
    scene.cycles.samples=args.samples
    scene.render.film_transparent=True
    scene.render.resolution_x=256
    scene.render.resolution_y=256
    scene.render.resolution_percentage=100
    scene.render.image_settings.file_format="PNG"
    scene.render.image_settings.color_mode="RGBA"
    scene.render.image_settings.color_depth="8"
    scene.render.fps=8
    scene.view_settings.view_transform="Standard"
    scene.view_settings.look="Medium High Contrast"
    scene.world.use_nodes=True
    scene.world.node_tree.nodes["Background"].inputs["Color"].default_value=(.27,.26,.23,1)
    scene.world.node_tree.nodes["Background"].inputs["Strength"].default_value=.65

    soil=collection("GROUND | primitive lumberyard surface")
    input_col=collection("INPUT | intact bark-covered round logs")
    processor=collection("PROCESSOR | rough wooden lever splitter and rails")
    output_col=collection("OUTPUT | stacks of lengthwise-split D-shape half logs")
    active_col=collection("WORK | wedge travel, active trunk, chips")
    fixtures=collection("CAMERA AND LIGHT | never rotate")

    bark=material("BARK | thick rough unprocessed bark",(.095,.060,.035),(.27,.15,.075),.98,11)
    endgrain=material("LOG ENDS | pale concentric end grain",(.35,.22,.11),(.64,.42,.20),.90,4)
    cut=material("SPLIT FACES | bright exposed wet timber",(.49,.34,.17),(.78,.60,.34),.90,6)
    frame=material("WOOD FRAME | heavy hewn timber",(.22,.115,.052),(.46,.28,.12),.98,7)
    dark=material("PEG AND ROPE | aged lashings",(.10,.068,.039),(.24,.17,.095),.98,12)
    metal=material("WEDGE | chipped dark stone or crude iron",(.10,.11,.105),(.28,.30,.285),.96,8)
    earth=material("SOIL | uneven dusty work ground",(.23,.17,.10),(.42,.29,.16),.99,5)
    chips=material("FRESH WOOD CHIPS | small pale splinters",(.46,.31,.17),(.81,.62,.35),.91,14)

    made=[]
    made.append(earth_patch(soil,earth))
    # LEFT INPUT: several FULL round trunks with bark, varied length and diameter.
    input_specs=[(-1.51,-.37,.02,1.48,.16),
                 (-1.20,-.40,.02,1.65,.17),
                 (-.93,-.32,.00,1.38,.145),
                 (-1.40,-.22,.30,1.42,.15),
                 (-1.10,-.22,.30,1.49,.15),
                 (-1.28,-.12,.56,1.18,.14)]
    for i,(x,y,z,L,r) in enumerate(input_specs):
        made.append(primitive_log(f"INPUT | intact full log {i+1:02d}",
                                  (x,y,z),L,r,bark,endgrain,input_col,i))
    # CENTER MACHINE: visible wooden cradle, hard posts, crossbar, braces,
    # lever and primitive blade guide. Unlike a modern saw, no drive motor.
    for x in (-.50,.50):
        made.append(box("PROCESSOR | upright square hewn post",
                        (x,.20,.66),(.19,.22,1.56),frame,processor,.035))
        made.append(box("PROCESSOR | y-axis cradle runner",
                        (x*.65,.09,.21),(.15,1.60,.20),frame,processor,.025))
    made.append(box("PROCESSOR | upper load-bearing crossbeam",
                    (0,.20,1.42),(1.22,.24,.20),frame,processor,.035))
    for x in (-.50,.50):
        made.append(beam("PROCESSOR | diagonal timber brace",(x,-.38,.10),
                         (x,.20,1.23),.060,frame,processor,8))
    # Crosspieces under the active log.
    for y in (-.49,.46):
        made.append(box("PROCESSOR | log cradle cross rail",(0,y,.19),
                        (1.12,.13,.14),frame,processor,.02))
    head=bpy.data.objects.new("ANIMATION | entire lifting splitter head",None)
    active_col.objects.link(head)
    blade=wedge("PROCESSOR | REAL lengthwise splitting wedge",.55,active_col,metal)
    blade.parent=head
    lifting=box("PROCESSOR | wood wedge carrier",(0,.02,.99),
                (.41,.33,.24),frame,active_col,.025)
    lifting.parent=head
    for x in (-.16,.16):
        guide=box("PROCESSOR | wedge moving wooden guide",
                  (x,.02,1.13),(.055,.28,.35),frame,active_col,.01)
        guide.parent=head
    # Lever is a visible mechanical handle, attached to the moving head.
    lever=beam("PROCESSOR | long hand-operated lever",
               (-.20,.15,1.27),(.80,-.46,1.60),.052,frame,active_col,10)
    lever.parent=head
    # Active round log becomes two actual longitudinal halves under the blade.
    full=primitive_log("WORK | hero trunk under splitting wedge",
                       (0,.02,.44),1.12,.18,bark,endgrain,active_col,999)
    half_left=split_half("WORK | left half of split hero trunk",
                         (-.10,.02,.46),1.12,.145,bark,cut,endgrain,active_col,13)
    half_right=split_half("WORK | right half of split hero trunk",
                          (.10,.02,.46),1.12,.145,bark,cut,endgrain,active_col,14)
    # RIGHT OUTPUT: half-log stacks, each has a TRUE light flat cut face.
    stacks=[
        (.98,-.56,.11,1.22,.16),(1.32,-.57,.11,1.26,.16),
        (1.66,-.51,.11,1.13,.14),(1.10,-.45,.30,1.18,.155),
        (1.48,-.44,.30,1.12,.145),(1.25,-.40,.48,1.04,.145)]
    for i,(x,y,z,L,r) in enumerate(stacks):
        made.append(split_half(f"OUTPUT | split D-face half log {i+1:02d}",
                         (x,y,z),L,r,bark,cut,endgrain,output_col,i))
    # Rough skids under finished stock and loose small chip scatter.
    for x in (.98,1.56):
        made.append(box("OUTPUT | simple ground timber skid",
                        (x,-.48,-.055),(.14,1.36,.13),frame,output_col,.018))
    chip_particles=[]
    for j,(x,y) in enumerate([(-.30,-.61),(.28,-.42),(.54,-.14),
                               (-.21,.51),(.18,.58),(.60,-.67)]):
        ob=box(f"GROUND | bark sliver {j+1:02d}",(x,y,-.08),
               (.09+.02*(j%3),.037,.026),chips,soil,.005,
               rotation=.3*j)
        made.append(ob)
    for j in range(3):
        c=box(f"WORK | keyed splinter burst {j+1:02d}",
              (.02+.13*(j-1),.06,.13+j*.07),
              (.08,.027,.02),chips,active_col,.004)
        chip_particles.append(c)
    animate(head,full,(half_left,half_right),chip_particles,active_col)

    # Same fixed-camera philosophy as approved Factorio campfire/clay/pit kiln.
    pivot=bpy.data.objects.new("EXPORT | rotate entire lumberyard under one fixed camera",None)
    scene.collection.objects.link(pivot)
    bpy.context.view_layer.update()
    for ob in list(scene.objects):
        if ob.type in {"MESH","EMPTY"} and ob != pivot and ob.parent is None:
            world=ob.matrix_world.copy()
            ob.parent=pivot
            ob.matrix_world=world
    cam_data=bpy.data.cameras.new("Factorio 45 degree structure camera")
    cam_data.type="ORTHO"
    cam_data.ortho_scale=5.35
    cam=bpy.data.objects.new("Factorio fixed ortho camera",cam_data)
    fixtures.objects.link(cam)
    target=Vector((0,0,.56))
    cam.location=(0,-6,6.56)
    cam.rotation_euler=(target-cam.location).to_track_quat("-Z","Y").to_euler()
    scene.camera=cam
    for name,loc,power,color,size in [
        ("Warm large daylight",(-3,-4,7),470,(1,.93,.83),5),
        ("Cool fill",(4,3,5),320,(.74,.85,1),5)
    ]:
        data=bpy.data.lights.new(name,"AREA")
        data.energy=power
        data.shape="DISK"
        data.size=size
        light=bpy.data.objects.new(name,data)
        fixtures.objects.link(light)
        light.location=loc
        light.rotation_euler=(target-Vector(loc)).to_track_quat("-Z","Y").to_euler()
        data.color=color

    # Save editable master and exact first render before emitting preview frames.
    pivot.rotation_euler.z=0
    scene.frame_set(0)
    bpy.context.view_layer.update()
    blend=out/"primitive-lumberyard-v1.blend"
    scene.render.filepath="//frames/"
    bpy.ops.wm.save_as_mainfile(filepath=str(blend),check_existing=False)
    records=[]
    for state,frames in (("idle",(0,)),("working",FRAMES)):
        for d,angle in enumerate(DIRECTIONS):
            pivot.rotation_euler.z=math.radians(angle)
            for i,t in enumerate(frames):
                scene.frame_set(t)
                bpy.context.view_layer.update()
                path=out/(f"idle-d{d:02d}.png" if state=="idle"
                          else f"working-d{d:02d}-f{i:03d}.png")
                scene.render.filepath=str(path)
                print("LUMBERYARD_V1_RENDER",state,angle,t,flush=True)
                bpy.ops.render.render(write_still=True)
                records.append({"state":state,"direction":d,"frame_index":i,
                                "timeline":t,"angle":angle,
                                "path":path.name,"sha256":sha(path)})
    pivot.rotation_euler.z=0
    scene.frame_set(0)
    report={
        "schema":1,"revision":"primitive-lumberyard-native-v1",
        "source":"new editable Blender geometry authored from C-block lumber processing brief",
        "intended_prototype":"assembling-machine/growing-plot (review only)",
        "original_game_prototype_modified":False,
        "geometry":{"raw_full_logs":len(input_specs),"output_true_split_halves":len(stacks),
           "rough_processor":True,"one_hero_trunk":True,
           "two_separating_active_halves":True,
           "wedge_slider":True,"visible_cut_face_material":True,
           "wood_chip_specks":len(chip_particles)},
        "camera_elevation":45,"ortho_scale":5.35,"source_render_size":[256,256],
        "rotations":list(DIRECTIONS),"states":{"idle":1,"working":16},
        "original_cblock_art_replaced":False,
        "source_frames":len(records),"fps":8,
        "editable_blend":blend.name,"master_sha256":sha(blend),
        "render_samples":args.samples,"blender":bpy.app.version_string,
        "visual_approved":False,"game_tested":False,"frames":records}
    (out/"build-report.json").write_text(json.dumps(report,indent=2)+"\n")
    print("LUMBERYARD_NATIVE_68_FRAMES_COMPLETE",len(records),flush=True)

if __name__=="__main__":main()
