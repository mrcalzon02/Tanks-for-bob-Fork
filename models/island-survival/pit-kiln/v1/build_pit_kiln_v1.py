#!/usr/bin/env python3
"""Pit Kiln V1: source-grounded primitive kiln, reusing the editable Clay Pit V3 basin.

Only visible in-world geometry is built. No hidden mechanism, building, chimney,
or unapproved modification of live Factorio prototypes.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import random
import sys

import bpy
from mathutils import Vector


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def args():
    p=argparse.ArgumentParser()
    p.add_argument("--out",type=Path,required=True)
    p.add_argument("--samples",type=int,default=24)
    return p.parse_args(sys.argv[sys.argv.index("--")+1:])


def material(name,color,roughness=0.98,emission=0):
    m=bpy.data.materials.new(name);m.use_nodes=True
    shader=m.node_tree.nodes.get("Principled BSDF")
    shader.inputs["Base Color"].default_value=(*color,1)
    shader.inputs["Roughness"].default_value=roughness
    shader.inputs["Metallic"].default_value=0
    if shader.inputs.get("Specular IOR Level"):
        shader.inputs["Specular IOR Level"].default_value=.08
    if emission:
        shader.inputs["Emission Color"].default_value=(*color,1)
        shader.inputs["Emission Strength"].default_value=emission
    return m


def move(ob,collection):
    for previous in list(ob.users_collection):
        previous.objects.unlink(ob)
    collection.objects.link(ob)
    return ob


def stone(name,where,scale,ma,col,rng):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2,radius=1,location=where)
    ob=move(bpy.context.object,col)
    ob.name=name
    ob.scale=scale
    ob.rotation_euler=(rng.uniform(-.16,.16),rng.uniform(-.22,.22),rng.uniform(0,6.28))
    ob.data.materials.append(ma)
    return ob


def log(name,p1,p2,width,ma,col):
    a,b=Vector(p1),Vector(p2);v=b-a
    bpy.ops.mesh.primitive_cylinder_add(vertices=10,radius=width,depth=v.length,location=(a+b)/2)
    ob=move(bpy.context.object,col)
    ob.name=name
    ob.rotation_euler=v.to_track_quat("Z","Y").to_euler()
    ob.data.materials.append(ma)
    return ob


def tongue(name,xy,base,height,width,ma,col,orientation):
    x,y=xy
    # Solid double-face flame silhouette, with pointed top; no billboard image planes.
    # Two diagonally crossed mesh surfaces read from all four camera orientations.
    vertices=[];faces=[]
    for offset in (orientation,orientation+math.pi/2):
        along=(math.cos(offset),math.sin(offset))
        across=(-math.sin(offset),math.cos(offset))
        center=(x,y)
        k=len(vertices)
        for t,depth in ((-.6*width,base),(0,base+.055),(.6*width,base)):
            vertices.append((center[0]+across[0]*t,center[1]+across[1]*t,depth))
        vertices.append((center[0]+along[0]*width*.28,
                         center[1]+along[1]*width*.28,base+height))
        faces.extend(((k,k+1,k+3),(k+1,k+2,k+3)))
    mesh=bpy.data.meshes.new(name+" mesh")
    mesh.from_pydata(vertices,[],faces);mesh.update()
    ob=bpy.data.objects.new(name,mesh);col.objects.link(ob);ob.data.materials.append(ma)
    return ob


def setup_animation(ob,phase,frames):
    ob.hide_render=True; ob.keyframe_insert(data_path="hide_render",frame=0)
    ob.hide_render=False; ob.keyframe_insert(data_path="hide_render",frame=1)
    ob.hide_render=False; ob.keyframe_insert(data_path="hide_render",frame=97)
    for index,frame in enumerate(frames+[97]):
        x=2*math.pi*(index%16)/16
        ob.scale=(1+.09*math.sin(x+phase),1+.07*math.sin(x*.9+phase),
                  1+.18*math.sin(x+phase)+.075*math.sin(2*x+phase/2))
        ob.keyframe_insert(data_path="scale",frame=frame)
        ob.rotation_euler.z=.07*math.sin(x+phase*.7)
        ob.keyframe_insert(data_path="rotation_euler",frame=frame)
    if ob.animation_data:
        for curve in ob.animation_data.action.fcurves:
            for k in curve.keyframe_points:
                if curve.data_path=="hide_render":
                    k.interpolation="CONSTANT"
                else:
                    k.interpolation="BEZIER"
                    k.handle_left_type=k.handle_right_type="AUTO_CLAMPED"


def main():
    opt=args();out=opt.out.resolve()
    if out.exists() and any(out.iterdir()):
        raise ValueError("Output must be empty/new; never overwrite previous models")
    out.mkdir(parents=True,exist_ok=True)
    scene=bpy.context.scene
    if scene.render.engine!="CYCLES" or not scene.camera or scene.camera.data.type!="ORTHO":
        raise ValueError("Expected editable native Clay Pit V3 Cycles orthographic scene")
    root=bpy.data.objects.get("EXPORT | rotate all clay and tools, never camera")
    basin=next((o for o in scene.objects if "one broad excavated clay bowl" in o.name),None)
    if root is None or basin is None or len(basin.data.materials)!=1:
        raise ValueError("Missing source Clay Pit V3 basin and model rotation root")
    # The original clay-pit primitive work implements do NOT belong in the kiln.
    old_tools=[o for o in list(scene.objects) if o.name.startswith("WORK |")]
    for ob in old_tools:
        bpy.data.objects.remove(ob,do_unlink=True)
    kiln=bpy.data.collections.new("PIT KILN | reused clay-earthwork and handmade fuel")
    scene.collection.children.link(kiln)
    active=bpy.data.collections.new("BURNING | authored 16-frame primitive fire")
    scene.collection.children.link(active)
    chalk=material("KILN | chalk and ash-white heat stones",(.53,.50,.45),.98)
    ash=material("KILN | grey ash-speckled stones",(.35,.34,.33),.99)
    dark=material("KILN | charcoal-black stones",(.12,.105,.088),1)
    wood=material("KILN | rough crossed fuel logs",(.21,.11,.053),.97)
    char=material("KILN | burned fuel tips",(.07,.052,.038),.99)
    flare=material("FIRE | bright yellow orange core",(1.0,.51,.052),.86,1.05)
    glow=material("FIRE | warm orange tongues",(.98,.20,.035),.92,.75)
    yellow=material("FIRE | yellow center",(1.0,.77,.13),.89,1.15)
    rng=random.Random(6321)
    # Use the single editable excavated clay bowl from V3, not additional pits.
    # Only the visible top of the interior is populated; no fabricated hidden oven.
    rocks=[
      ((-.47,-.36,-.10),(.32,.27,.21),chalk),((.38,-.38,-.09),(.32,.24,.22),ash),
      ((-.45,.20,-.09),(.30,.25,.20),chalk),((.36,.22,-.10),(.28,.25,.20),chalk),
      ((-.06,-.55,-.10),(.25,.23,.18),ash),((.00,.48,-.10),(.24,.20,.17),ash),
      ((-.20,-.08,-.16),(.19,.17,.16),dark),((.22,-.05,-.16),(.19,.16,.14),dark),
      ((.08,-.22,-.15),(.17,.14,.12),dark)
    ]
    made=[]
    for i,(pos,scale,mat) in enumerate(rocks):
        made.append(stone("KILN | exposed rock and ash %02d"%(i+1),pos,scale,mat,kiln,rng))
    for i,(a,b,rad) in enumerate([
      ((-.66,-.06,.11),(.56,.11,.10),.075),
      ((-.45,.38,.12),(.47,-.34,.11),.07),
      ((-.34,-.39,.085),(.30,.49,.085),.054)
    ]):
        made.append(log("KILN | crossed primitive fuel %02d"%(i+1),a,b,rad,wood,kiln))
    # Small loose short billets near the rim only when burning, matching 2-frame overlay.
    billets=[]
    for i,(a,b) in enumerate([
      ((.69,.44,.16),(1.00,.45,.17)),
      ((-.89,-.54,.15),(-.66,-.56,.17))
    ]):
        ob=log("BURNING | feeding wood billet %02d"%(i+1),a,b,.045,wood,active)
        billets.append(ob)
        ob.hide_render=True;ob.keyframe_insert(data_path="hide_render",frame=0)
        ob.hide_render=False;ob.keyframe_insert(data_path="hide_render",frame=1)
        ob.hide_render=False;ob.keyframe_insert(data_path="hide_render",frame=97)
    frames=list(range(1,92,6))
    flames=[]
    for i,(x,y,h,w) in enumerate([
        (-.24,-.04,.42,.16),(.12,.06,.54,.18),(.33,-.23,.45,.14),
        (-.02,-.34,.47,.17),(.01,.32,.40,.13),(-.38,.17,.37,.11),
        (.28,.22,.34,.12),(-.23,-.28,.32,.12)
    ]):
        material_choice=[flare,glow,yellow,flare,glow,flare,yellow,glow][i]
        ob=tongue("BURNING | flame tongue %02d"%(i+1),(x,y),.045,h,w,
                  material_choice,active,orientation=i*.77)
        setup_animation(ob,i*.72,frames)
        flames.append(ob)
    light_data=bpy.data.lights.new("PIT KILN | animated low orange illumination","POINT")
    light_data.color=(1.0,.49,.20);light_data.shadow_soft_size=.44
    light=bpy.data.objects.new("BURNING | local kiln fire light",light_data)
    active.objects.link(light);light.location=(0,-.05,.29)
    light.hide_render=True;light.keyframe_insert(data_path="hide_render",frame=0)
    light.hide_render=False;light.keyframe_insert(data_path="hide_render",frame=1)
    light.hide_render=False;light.keyframe_insert(data_path="hide_render",frame=97)
    for i,frame in enumerate(frames+[97]):
        t=2*math.pi*(i%16)/16
        light_data.energy=3.5*(1+.1*math.sin(t+.7)+.04*math.sin(3*t+.3))
        light_data.keyframe_insert(data_path="energy",frame=frame)
    # All visible kiln objects rotate, camera and fixed daylight do not.
    for ob in made+billets+flames+[light]:
        mw=ob.matrix_world.copy();ob.parent=root;ob.matrix_world=mw
    scene.camera.data.ortho_scale=3.15
    scene.cycles.samples=opt.samples
    scene.cycles.use_denoising=False
    scene.cycles.device="CPU"
    scene.render.film_transparent=True
    scene.render.resolution_x=scene.render.resolution_y=256
    scene.render.resolution_percentage=100
    scene.render.image_settings.file_format="PNG"
    scene.render.image_settings.color_mode="RGBA"
    scene.render.image_settings.color_depth="8"
    scene.render.fps=8
    scene.frame_set(0);root.rotation_euler.z=0
    bpy.context.view_layer.update()
    master=out/"pit-kiln-v1.blend"
    scene.render.filepath="//captures/"
    bpy.ops.wm.save_as_mainfile(filepath=str(master),check_existing=False)
    cam_before=[[float(v) for v in row] for row in scene.camera.matrix_world]
    records=[]
    for state,samples in (("idle",[0]),("burning",frames)):
        for d,angle in enumerate((0,90,180,270)):
            root.rotation_euler.z=math.radians(angle)
            for index,frame in enumerate(samples):
                scene.frame_set(frame)
                bpy.context.view_layer.update()
                path=out/(f"idle-d{d:02d}.png" if state=="idle"
                          else f"burning-d{d:02d}-f{index:03d}.png")
                scene.render.filepath=str(path)
                print("PIT_KILN_RENDER",state,angle,frame,flush=True)
                bpy.ops.render.render(write_still=True)
                records.append(dict(state=state,direction=d,angle=angle,index=index,
                                    timeline_frame=frame,path=path.name,sha256=sha(path)))
    root.rotation_euler.z=0
    scene.frame_set(0)
    report=dict(schema=1,revision="pit-kiln-native-v1",engine="Factorio 2.1",
                blender=bpy.app.version_string,source_blend="clay-pit-v3.blend",
                reused_basin=True,removed_clay_pit_tools=len(old_tools),
                basin_count=1,rock_count=len(rocks),fuel_count=len(made)-len(rocks)+len(billets),
                flame_count=len(flames),camera_elevation_deg=45,ortho_scale=3.15,
                fps=8,directions=[0,90,180,270],states={"idle":1,"burning":16},
                samples=frames,frames_count=len(records),master_sha256=sha(master),
                original_sprites_modified=False,art_accepted=False,game_tested=False,
                captures=records)
    (out/"build-report.json").write_text(json.dumps(report,indent=2)+"\n")
    print("PIT_KILN_V1_BLENDER_CAPTURED",len(records),flush=True)


if __name__=="__main__":
    main()
