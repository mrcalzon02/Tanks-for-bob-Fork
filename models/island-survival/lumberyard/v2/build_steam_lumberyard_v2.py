#!/usr/bin/env python3
"""Lumberyard V2: primitive Franklin-stove boiler, piston/flywheel, belt driven saw.

Editable native meshes, not a concept sketch. The visible lumber operation is
whole bark-covered logs -> belt-driven longitudinal saw -> stacks of two halved
logs. No modern motor, no arbitrary wedge splitter. Four real model rotations.
"""
import argparse
import hashlib
import json
import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"v1"))
from build_lumberyard_v1 import (collection,into,material,box,beam,primitive_log,
                                split_half,earth_patch)

ANGLES=(0,90,180,270)
FRAMES=tuple(range(1,17))
WORK_CYCLE=(0,)+FRAMES+(17,)
BLADE_CENTER=Vector((.42,-.40,.72))
DRIVE_CENTER=Vector((-.17,.84,.87))
SAW_PULLEY_CENTER=Vector((-.17,-.40,.72))
SPOKE_COUNT=5

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def emit(name,color,power=1.5):
    m=bpy.data.materials.new(name)
    m.use_nodes=True
    bsdf=m.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value=(*color,1)
    bsdf.inputs["Roughness"].default_value=.85
    bsdf.inputs["Emission Color"].default_value=(*color,1)
    bsdf.inputs["Emission Strength"].default_value=power
    return m

def wheel(name,at,radius,material,col,spokes=True):
    """A real X-axis wooden/iron wheel in the Y/Z plane."""
    bpy.ops.mesh.primitive_cylinder_add(vertices=48,radius=radius,depth=.075,location=at)
    ob=into(bpy.context.object,col)
    ob.name=name
    ob.rotation_euler.y=math.pi/2
    ob.data.materials.append(material)
    if spokes:
        # Parent spokes to a common rotating hub, so the wheel visibly spins.
        ob.display_type="SOLID"
    return ob

def blade(name,at,radius,material,col):
    """Closed thick circular saw with 20 distinct physically modeled teeth."""
    n=40
    verts=[]
    # Local YZ plane, blade shaft passes through X.
    for x in (-.026,.026):
        verts.append((x,0,0))
        for j in range(n):
            theta=2*math.pi*j/n
            r=radius if j%2==0 else radius*.916
            verts.append((x,r*math.cos(theta),r*math.sin(theta)))
    faces=[]
    # front/back material surface; sides close the tooth profiles.
    for side in range(2):
        offset=side*(n+1)
        for j in range(n):
            a=offset+1+j
            b=offset+1+(j+1)%n
            if side==0:faces.append((offset,b,a))
            else:faces.append((offset,a,b))
    for j in range(n):
        a,b=1+j,1+(j+1)%n
        faces.append((a,b,b+n+1,a+n+1))
    mesh=bpy.data.meshes.new(name+" thick steel teeth")
    mesh.from_pydata(verts,[],faces)
    mesh.update()
    mesh.materials.append(material)
    for p in mesh.polygons:p.use_smooth=False
    ob=bpy.data.objects.new(name,mesh)
    col.objects.link(ob)
    ob.location=at
    return ob

def belt_path(y1,z1,r1,y2,z2,r2,x):
    """Visible closed oiled-leather loop: top tangent, saw arc, return, drive arc."""
    points=[]
    points.append((x,y1,z1+r1))
    points.append((x,y2,z2+r2))
    for i in range(1,17):
        a=math.pi*i/16
        points.append((x,y2-r2*math.sin(a),z2+r2*math.cos(a)))
    points.append((x,y1,z1-r1))
    for i in range(1,17):
        a=math.pi*i/16
        points.append((x,y1+r1*math.sin(a),z1-r1*math.cos(a)))
    return points

def belt_object(name,points,ma,col):
    curve=bpy.data.curves.new(name+" path","CURVE")
    curve.dimensions="3D"
    curve.resolution_u=16
    curve.bevel_depth=.017
    curve.bevel_resolution=2
    sp=curve.splines.new("POLY")
    sp.points.add(len(points)-1)
    for point,loc in zip(sp.points,points):
        point.co=(*loc,1)
    sp.use_cyclic_u=True
    ob=bpy.data.objects.new(name,curve)
    col.objects.link(ob)
    ob.data.materials.append(ma)
    return ob

def track_position(points,progress):
    segments=[]
    total=0
    for i,p in enumerate(points):
        q=points[(i+1)%len(points)]
        v=(Vector(q)-Vector(p)).length
        segments.append(v)
        total+=v
    distance=(progress%1)*total
    for i,seg in enumerate(segments):
        if distance<=seg:
            p=Vector(points[i])
            q=Vector(points[(i+1)%len(points)])
            return p+(q-p)*(distance/max(seg,.00001))
        distance-=seg
    return Vector(points[0])

def cyl(name,a,b,r,ma,col,verts=16):
    return beam(name,a,b,r,ma,col,verts)

def hide_state(ob,frame,visible):
    ob.hide_render=not visible
    ob.keyframe_insert(data_path="hide_render",frame=frame)
    if ob.animation_data:
        for fc in ob.animation_data.action.fcurves:
            if fc.data_path=="hide_render":
                for k in fc.keyframe_points:k.interpolation="CONSTANT"

def smooth_action(ob,linear=False):
    if not ob.animation_data or not ob.animation_data.action:return
    for fc in ob.animation_data.action.fcurves:
        for key in fc.keyframe_points:
            if fc.data_path=="hide_render":key.interpolation="CONSTANT"
            elif linear:key.interpolation="LINEAR"
            else:
                key.interpolation="BEZIER"
                key.handle_left_type=key.handle_right_type="AUTO_CLAMPED"

def setup_scene(samples):
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    scene=bpy.context.scene
    scene.render.engine="CYCLES"
    scene.cycles.samples=samples
    scene.cycles.device="CPU"
    scene.render.film_transparent=True
    scene.render.resolution_x=scene.render.resolution_y=256
    scene.render.resolution_percentage=100
    scene.render.image_settings.file_format="PNG"
    scene.render.image_settings.color_mode="RGBA"
    scene.render.image_settings.color_depth="8"
    scene.render.fps=8
    scene.view_settings.view_transform="Standard"
    scene.view_settings.look="Medium High Contrast"
    scene.world.use_nodes=True
    scene.world.node_tree.nodes["Background"].inputs["Color"].default_value=(.25,.24,.22,1)
    scene.world.node_tree.nodes["Background"].inputs["Strength"].default_value=.65
    return scene

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--out",type=Path,required=True)
    parser.add_argument("--samples",type=int,default=24)
    cfg=parser.parse_args(sys.argv[sys.argv.index("--")+1:])
    out=cfg.out.resolve()
    if out.exists() and any(out.iterdir()):
        raise FileExistsError("New empty output required; do not overwrite previous Blender assets")
    out.mkdir(parents=True,exist_ok=True)
    scene=setup_scene(cfg.samples)
    ground=collection("GROUND | rough timber yard")
    raw=collection("INPUT | whole tree trunks")
    boiler=collection("BOILER | primitive Franklin style enclosed stove firebox")
    engine=collection("ENGINE | steam piston flywheel and exposed crank")
    transmission=collection("DRIVE | continuous leather belt and two pulleys")
    saw=collection("SAW | rotating toothed circular blade and log carriage")
    stock=collection("OUTPUT | lengthwise-split log stack")
    active=collection("ANIMATION | log feed cut and eject")
    fixed=collection("FIXED | structure camera and daylight")
    soil=material("soil and woodchip covered worksite",(.15,.11,.065),(.34,.25,.13),.99,6)
    bark=material("dark rough unprocessed bark",(.083,.053,.026),(.29,.17,.07),.97,11)
    pale=material("pale wet exposed split log faces",(.48,.31,.12),(.79,.58,.31),.91,7)
    ends=material("warm concentric endgrain",(.32,.21,.10),(.64,.43,.21),.92,4)
    wood=material("rough tool and support timber",(.19,.10,.041),(.46,.27,.10),.96,8)
    blackiron=material("stove blackened cast iron",(.033,.037,.039),(.11,.108,.095),.81,12)
    steel=material("primitive iron saw and hub",(.19,.22,.21),(.54,.57,.55),.70,10)
    copper=material("boiler bronzed brass",(.28,.135,.045),(.64,.35,.11),.78,8)
    leather=material("dark oily drive belt",(.067,.040,.018),(.19,.125,.064),.95,16)
    orange=emit("orange embers inside stove",(.99,.29,.048),1.3)
    chips=material("pale fresh wood chips",(.38,.26,.12),(.81,.60,.32),.90,13)
    steam=material("small pale steam exhaust",(.55,.57,.54),(.87,.89,.85),.98,3)
    earth_patch(ground,soil)
    # LEFT: six tangible bark-covered whole trunks, not a forest tree.
    logs=[(-1.47,-.38,.005,1.25,.16),(-1.17,-.39,.005,1.43,.17),
          (-.92,-.34,-.01,1.15,.14),(-1.40,-.28,.28,1.25,.15),
          (-1.10,-.23,.30,1.22,.145),(-1.28,-.12,.55,1.02,.14)]
    for i,(x,y,z,L,r) in enumerate(logs):
        primitive_log(f"INPUT | full bark log {i+1:02d}",(x,y,z),L,r,bark,ends,raw,i+100)
    # A small Franklin-style enclosed iron stove with fire door, prominent cast
    # iron body, chimney and a strapped copper pressure cylinder above it.
    for x in (-.91,-.35):
        for y in (.47,1.06):
            box("BOILER | cast stove foot",(x,y,-.01),(.12,.13,.21),blackiron,boiler,.012)
    box("BOILER | solid enclosed Franklin firebox",(-.63,.76,.40),(.78,.69,.64),blackiron,boiler,.052)
    box("BOILER | thick stove door frame",(-.63,.402,.39),(.53,.052,.44),steel,boiler,.020)
    ember=box("BOILER | visible ember window",(-.63,.365,.37),(.41,.022,.23),orange,boiler,.025)
    grille=[]
    for x in (-.78,-.66,-.54,-.43):
        grille.append(box("BOILER | fire grate vertical bar",(x,.344,.36),(.020,.052,.28),
                           blackiron,boiler,.004))
    box("BOILER | stove top lid",(-.63,.76,.77),(.84,.77,.11),blackiron,boiler,.045)
    # Short smoke exhaust; external and visible, not hidden machinery.
    cyl("BOILER | cast iron chimney neck",(-.86,1.0,.77),(-.86,1.0,1.33),
        .09,blackiron,boiler,18)
    cyl("BOILER | raised chimney lip",(-.86,1.0,1.32),(-.86,1.0,1.38),
        .113,blackiron,boiler,18)
    # Primitive pressure vessel strapped down on the stove top.
    cyl("BOILER | horizontal copper pressure vessel",(-.62,.46,.90),
        (-.62,1.06,.90),.17,copper,boiler,24)
    for yy in (.54,1.0):
        cyl("BOILER | vessel retaining iron hoop",(-.62,yy,.90),(-.62,yy+.036,.90),
            .178,blackiron,boiler,24)
    cyl("BOILER | steam pipe to piston",(-.31,1.01,1.0),
        (-.10,1.09,.77),.026,copper,boiler,10)
    box("BOILER | crude pressure valve stem",(-.60,.76,1.18),
        (.055,.055,.17),blackiron,boiler,.01)
    # Steam engine in the open, not magically moving without a cylinder.
    cyl("ENGINE | exposed brass steam cylinder",(-.20,1.16,.66),
        (-.20,.83,.66),.13,copper,engine,20)
    flywheel=bpy.data.objects.new("ANIM | driven steam flywheel",None)
    engine.objects.link(flywheel)
    flywheel.location=DRIVE_CENTER
    fw=wheel("ENGINE | five-spoke power flywheel",DRIVE_CENTER,.28,steel,engine)
    # Five thick radial spokes and visible offset crank pin.
    spokes=[]
    for i in range(SPOKE_COUNT):
        t=2*math.pi*i/SPOKE_COUNT
        start=DRIVE_CENTER+Vector((.06,.035*math.cos(t),.035*math.sin(t)))
        finish=DRIVE_CENTER+Vector((.06,.245*math.cos(t),.245*math.sin(t)))
        spokes.append(cyl("ENGINE | real flywheel radial spoke",start,finish,.018,copper,engine,8))
    pin=box("ENGINE | offset bronze crankpin",
            tuple(DRIVE_CENTER+Vector((.09,.20,0))),(.085,.047,.047),copper,engine,.008)
    for ob in [fw]+spokes+[pin]:
        world=ob.matrix_world.copy()
        ob.parent=flywheel
        ob.matrix_world=world
    # Mechanical transmission: shaft along X, two X-axis pulleys, closed
    # leather belt and animated running stitch markers along the entire loop.
    drive_pulley=wheel("DRIVE | boiler power pulley",DRIVE_CENTER,.245,wood,transmission)
    saw_pulley=wheel("DRIVE | sawshaft receiving pulley",SAW_PULLEY_CENTER,.18,wood,transmission)
    # Shared hub rotate controls, pulley geometry children of their hubs.
    saw_hub=bpy.data.objects.new("ANIM | receiving pulley and saw spindle",None)
    transmission.objects.link(saw_hub)
    saw_hub.location=SAW_PULLEY_CENTER
    for ob,rig in ((drive_pulley,flywheel),(saw_pulley,saw_hub)):
        world=ob.matrix_world.copy()
        ob.parent=rig
        ob.matrix_world=world
    belt=belt_path(DRIVE_CENTER.y,DRIVE_CENTER.z,.252,
                   SAW_PULLEY_CENTER.y,SAW_PULLEY_CENTER.z,.186,-.17)
    belt_object("DRIVE | one continuous oiled leather belt",belt,leather,transmission)
    stitches=[]
    for i in range(7):
        ob=box("DRIVE | marching leather join / belt seam",tuple(track_position(belt,i/7)),
               (.029,.036,.026),copper,transmission,.005)
        stitches.append(ob)
    # Shaft, wood bearings, and a vertical toothed circular saw at right of pulley.
    cyl("SAW | continuous belt-to-blade shaft",(-.18,-.40,.72),
        (.52,-.40,.72),.055,steel,saw,20)
    for x in (-.14,.47):
        box("SAW | simple shaft bearing block",(x,-.40,.53),
            (.16,.20,.21),wood,saw,.023)
    saw_rig=bpy.data.objects.new("ANIM | keyed toothed saw rotation",None)
    saw.objects.link(saw_rig)
    saw_rig.location=BLADE_CENTER
    circular=blade("SAW | primitive 20-tooth circular steel saw",BLADE_CENTER,.325,steel,saw)
    # Include a clearly identifiable bright center hub and shaft rivets.
    hub=wheel("SAW | rotating central riveted hub",BLADE_CENTER,.075,copper,saw,False)
    for ob in (circular,hub):
        world=ob.matrix_world.copy()
        ob.parent=saw_rig
        ob.matrix_world=world
    # Feed bed uses longitudinal Y slide, away from raw input / into cut zone.
    for xx in (.18,.65):
        box("SAW | whole-trunk carriage guide",(xx,-.62,.21),
            (.12,1.76,.16),wood,saw,.016)
    for yy in (-1.27,.06):
        box("SAW | exposed carriage wooden cross tie",(.415,yy,.19),
            (.77,.17,.14),wood,saw,.016)
    # Do not obscure the upper part of the spinning blade.
    box("SAW | lower sawblade splash/guard timber",(.43,-.44,.27),
        (.78,.16,.16),wood,saw,.020)
    # Finished pile has REAL semicircular cross-section split timbers.
    finished=[(1.02,-.60,.12,1.25,.15),(1.35,-.59,.12,1.19,.15),
              (1.68,-.55,.11,1.11,.145),(1.10,-.49,.29,1.13,.14),
              (1.43,-.47,.29,1.11,.14),(1.26,-.39,.46,1.02,.13)]
    for i,(x,y,z,L,r) in enumerate(finished):
        split_half("OUTPUT | true flat-face longitudinal half-log %02d"%(i+1),
                   (x,y,z),L,r,bark,pale,ends,stock,i+200)
    for x in (1.05,1.62):
        box("OUTPUT | split logs resting on skid",(x,-.56,-.08),
            (.15,1.33,.15),wood,stock,.017)
    for i,(xx,yy) in enumerate([(-.25,-1.05),(.07,-1.22),(.86,-.83),
                                 (.74,-.16),(-.22,-.57),(1.00,.35)]):
        box("YARD | individual fresh woodchip", (xx,yy,-.10),
            (.08,.03,.023),chips,ground,.004,rotation=i*.67)
    # Working hero log: log moves into the spinning blade, becomes two
    # LENGTHWISE split half-trunks, then both eject to the finished stack.
    hero=primitive_log("WORK | whole log feeding through turning saw",
                       (.42,-1.0,.44),1.05,.165,bark,ends,active,712)
    left=split_half("WORK | cut half to receiving stack A",
                    (.30,-.38,.43),1.05,.148,bark,pale,ends,active,808)
    right=split_half("WORK | cut half to receiving stack B",
                     (.54,-.38,.43),1.05,.148,bark,pale,ends,active,809)
    eject=[left,right]
    splinters=[]
    for i in range(4):
        o=box("WORK | visible saw chips during cut %02d"%(i+1),
              (.42+(.12 if i%2 else -.12),-.46,.24),(.06,.025,.02),
              chips,active,.004)
        splinters.append(o)
    # Pressure-firing lamp is a very restrained hot point light.
    light_data=bpy.data.lights.new("BOILER | warm firebox glow","POINT")
    light_data.color=(1,.40,.14)
    light_data.shadow_soft_size=.25
    heatlight=bpy.data.objects.new("BOILER | keyed amber fire intensity",light_data)
    boiler.objects.link(heatlight)
    heatlight.location=(-.63,.30,.39)
    # Rotating shafts and belt markers are keyed independently.
    for n,frame in enumerate(FRAMES+(17,)):
        i=n%16
        u=i/16
        # Warm boiler remains lit through working cycle; flicker varies.
        factor=(.82,1.01,1.19,.92,1.13,.78,1.15,.99,
                1.21,.91,1.06,.77,1.14,.94,1.11,1.00)[i]
        light_data.energy=1.5*factor
        light_data.keyframe_insert(data_path="energy",frame=frame)
        ember_mat=orange.node_tree.nodes.get("Principled BSDF")
        ember_mat.inputs["Emission Strength"].default_value=1.1*factor
        ember_mat.inputs["Emission Strength"].keyframe_insert(data_path="default_value",frame=frame)
        flywheel.rotation_euler.x=4*math.pi*u
        saw_hub.rotation_euler.x=6*math.pi*u
        saw_rig.rotation_euler.x=6*math.pi*u
        for ctl in (flywheel,saw_hub,saw_rig):
            ctl.keyframe_insert(data_path="rotation_euler",frame=frame)
        # Moving join marks prove a taut, truly running drive belt.
        for k,stitch in enumerate(stitches):
            stitch.location=track_position(belt,(k/7+2*u)%1)
            stitch.keyframe_insert(data_path="location",frame=frame)
        # Full trunk goes from carriage entry to spinning blade.
        progression=(0,0,.04,.12,.22,.34,.46,.57,.68,.73,.73,.73,.73,.73,.73,.73)[i]
        hero.location.y=progression
        hero.keyframe_insert(data_path="location",frame=frame)
        hide_state(hero,frame,i<10)
        # At the cut point display two ACTUAL D-profile half logs and eject
        # both laterally onto the existing processed half-log pile.
        appear=i>=10
        travel=0 if i<10 else min(1,(i-10)/4)
        for j,h in enumerate(eject):
            hide_state(h,frame,appear)
            h.location=(.66*travel,.02+(.10 if j else -.10)*travel,.02*travel)
            h.keyframe_insert(data_path="location",frame=frame)
        for j,chip in enumerate(splinters):
            visible=6<=i<=12
            hide_state(chip,frame,visible)
            chip.location=(.03*math.sin(i+j),.0,.035*(i-5) if visible else 0)
            chip.keyframe_insert(data_path="location",frame=frame)
        hide_state(heatlight,frame,True)
    # Idle frame 0 is not burning or moving.
    scene.frame_set(0)
    for ob in [hero]+eject+splinters+[heatlight]:
        hide_state(ob,0,ob==hero)
    light_data.energy=0
    light_data.keyframe_insert(data_path="energy",frame=0)
    orange.node_tree.nodes.get("Principled BSDF").inputs["Emission Strength"].default_value=0
    orange.node_tree.nodes.get("Principled BSDF").inputs["Emission Strength"].keyframe_insert(
        data_path="default_value",frame=0)
    for ob in (flywheel,saw_hub,saw_rig,*stitches,hero,left,right,*splinters):
        smooth_action(ob,linear=ob in (flywheel,saw_hub,saw_rig))
    # Export root rotates ALL visible machine objects, never light or camera.
    pivot=bpy.data.objects.new("EXPORT | turn lumberyard under fixed 45-degree camera",None)
    scene.collection.objects.link(pivot)
    bpy.context.view_layer.update()
    moving_objects=[o for o in scene.objects if o.type in ("MESH","CURVE","EMPTY","LIGHT") and o != pivot]
    for ob in moving_objects:
        if ob.parent is not None:continue
        matrix=ob.matrix_world.copy()
        ob.parent=pivot
        ob.matrix_world=matrix
    camdata=bpy.data.cameras.new("Factorio 45-degree fixed structure projection")
    camdata.type="ORTHO"
    camdata.ortho_scale=5.75
    cam=bpy.data.objects.new("Factorio fixed structure camera",camdata)
    fixed.objects.link(cam)
    target=Vector((0,0,.59))
    cam.location=(0,-6,6.59)
    cam.rotation_euler=(target-cam.location).to_track_quat("-Z","Y").to_euler()
    scene.camera=cam
    for name,location,power,color,size in (
        ("Broad warm structure key",(-3,-4,7),520,(1,.94,.81),5),
        ("Cool skylight",(4,3,5),250,(.75,.85,1),5)):
        data=bpy.data.lights.new(name,"AREA")
        data.energy=power
        data.shape="DISK";data.size=size
        data.color=color
        ob=bpy.data.objects.new(name,data)
        fixed.objects.link(ob)
        ob.location=location
        ob.rotation_euler=(target-Vector(location)).to_track_quat("-Z","Y").to_euler()
    scene.frame_set(0)
    pivot.rotation_euler.z=0
    bpy.context.view_layer.update()
    master=out/"steam-lumberyard-v2.blend"
    scene.render.filepath="//renders/"
    bpy.ops.wm.save_as_mainfile(filepath=str(master),check_existing=False)
    captures=[]
    for state,frames in (("idle",(0,)),("working",FRAMES)):
        for d,angle in enumerate(ANGLES):
            pivot.rotation_euler.z=math.radians(angle)
            for i,frame in enumerate(frames):
                scene.frame_set(frame)
                bpy.context.view_layer.update()
                name=(f"idle-d{d:02d}.png" if state=="idle"
                      else f"working-d{d:02d}-f{i:03d}.png")
                path=out/name
                scene.render.filepath=str(path)
                print("STEAM_LUMBERYARD_RENDER",state,angle,frame,flush=True)
                bpy.ops.render.render(write_still=True)
                captures.append(dict(state=state,direction=d,index=i,frame=frame,
                                     angle=angle,path=name,sha256=sha(path)))
    pivot.rotation_euler.z=0
    scene.frame_set(0)
    build=dict(schema=2,revision="steam-lumberyard-v2-real-belt-driven-saw",
        source="authored native Blender from C-block lumberyard prototype slot",
        game_prototype_unchanged=True,
        mechanism="Franklin-style cast iron stove + copper boiler + steam piston + flywheel + continuous leather belt + vertical circular saw",
        counts=dict(raw_round_logs=len(logs),
                    output_true_lengthwise_split_halves=len(finished),
                    stove_firebox=1,pressure_boiler=1,steam_piston=1,
                    flywheel=1,leather_belt=1,drive_pulleys=2,
                    belt_join_markers=len(stitches),actual_saw_blades=1,
                    hero_round_logs=1,hero_split_halves=2),
        animation=["boiler fires","piston flywheel rotates","leather belt runs",
                   "saw blade spins","whole trunk feeds through",
                   "two lengthwise halves eject onto split-log stack"],
        camera_elevation=45,ortho_scale=5.75,
        directions=list(ANGLES),states={"idle":1,"working":16},
        source_frames=len(captures),fps=8,samples=cfg.samples,
        master_sha256=sha(master),visual_approved=False,
        factorio_client_tested=False,captures=captures)
    (out/"build-report.json").write_text(json.dumps(build,indent=2)+"\n")
    print("STEAM_LUMBERYARD_V2_NATIVE_68_CAPTURE_COMPLETE",flush=True)

if __name__=="__main__":main()
