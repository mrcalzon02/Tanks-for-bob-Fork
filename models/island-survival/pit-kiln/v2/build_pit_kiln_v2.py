#!/usr/bin/env python3
"""Pit Kiln V2: reuse native V1 kiln; add hand-formed raw bricks on wooden staging slab,
and an intentionally spaced inner-wall firing ring. Original Factorio art unchanged.
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

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def parse():
    p=argparse.ArgumentParser()
    p.add_argument("--out",required=True,type=Path)
    p.add_argument("--samples",type=int,default=24)
    return p.parse_args(sys.argv[sys.argv.index("--")+1:])

def material(name,base,roughness=.96):
    m=bpy.data.materials.new(name);m.use_nodes=True
    n=m.node_tree.nodes.get("Principled BSDF")
    n.inputs["Base Color"].default_value=(*base,1)
    n.inputs["Roughness"].default_value=roughness
    n.inputs["Metallic"].default_value=0
    socket=n.inputs.get("Specular IOR Level")
    if socket: socket.default_value=.07
    nodes=m.node_tree.nodes
    noise=nodes.new("ShaderNodeTexNoise")
    noise.inputs["Scale"].default_value=16
    noise.inputs["Detail"].default_value=2.2
    ramp=nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].position=.25
    ramp.color_ramp.elements[0].color=(*[c*.85 for c in base],1)
    ramp.color_ramp.elements[1].position=.77
    ramp.color_ramp.elements[1].color=(*[min(1,c*1.17) for c in base],1)
    m.node_tree.links.new(noise.outputs["Fac"],ramp.inputs["Fac"])
    m.node_tree.links.new(ramp.outputs["Color"],n.inputs["Base Color"])
    return m

def relink(obj,col):
    for old in list(obj.users_collection):
        old.objects.unlink(obj)
    col.objects.link(obj)
    return obj

def mesh_box(name,location,dimensions,ma,col,angle=0,edge=.015,seed=0):
    bpy.ops.mesh.primitive_cube_add(size=1,location=location)
    ob=relink(bpy.context.object,col)
    ob.name=name
    ob.dimensions=dimensions
    ob.rotation_euler.z=angle
    bpy.context.view_layer.objects.active=ob
    ob.select_set(True)
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    ob.select_set(False)
    # Hand-molded silhouette: localized uneven pressure on top and ends.
    rng=random.Random(seed)
    for v in ob.data.vertices:
        if v.co.z>0:
            v.co.z+=rng.uniform(-.007,.008)
            v.co.x+=rng.uniform(-.005,.005)
            v.co.y+=rng.uniform(-.006,.006)
    mod=ob.modifiers.new("Soft imperfect handmade edges","BEVEL")
    mod.width=edge
    mod.segments=2
    ob.modifiers.new("Weighted face normals","WEIGHTED_NORMAL")
    ob.data.materials.append(ma)
    return ob

def parent_world(child,root):
    matrix=child.matrix_world.copy()
    child.parent=root
    child.matrix_world=matrix

def hide_when_idle(ob):
    ob.hide_render=True
    ob.keyframe_insert(data_path="hide_render",frame=0)
    ob.hide_render=False
    ob.keyframe_insert(data_path="hide_render",frame=1)
    ob.keyframe_insert(data_path="hide_render",frame=97)
    if ob.animation_data:
        for f in ob.animation_data.action.fcurves:
            for k in f.keyframe_points:k.interpolation="CONSTANT"

def main():
    args=parse()
    out=args.out.resolve()
    if out.exists() and any(out.iterdir()):
        raise ValueError("Do not overwrite previous evidence")
    out.mkdir(parents=True,exist_ok=True)
    scene=bpy.context.scene
    root=bpy.data.objects.get("EXPORT | rotate all clay and tools, never camera")
    basin=next((ob for ob in scene.objects if "one broad excavated clay bowl" in ob.name),None)
    flames=[ob for ob in scene.objects if ob.name.startswith("BURNING | flame tongue")]
    if not root or not basin or len(flames)!=8 or not scene.camera or scene.camera.data.type!="ORTHO":
        raise RuntimeError("Missing native pit kiln V1 source or correct camera")
    if abs(scene.camera.data.ortho_scale-3.55)>.001:
        raise RuntimeError("V1 camera scale changed")
    prev_objects=len([o for o in scene.objects if o.type=="MESH"])
    k=bpy.data.collections.new("KILN V2 | wood board with staged hand-molded wet bricks")
    scene.collection.children.link(k)
    firing=bpy.data.collections.new("KILN V2 | unfired bricks on sloped inner heat-reflecting bank")
    scene.collection.children.link(firing)
    boardmat=material("V2 | split wood slab, rough cut",(.24,.125,.049),.99)
    clay_a=material("V2 | unbaked damp clay brick, reddish ochre",(.45,.185,.095),.98)
    clay_b=material("V2 | unbaked damp brick, shaded umber",(.31,.125,.07),.96)
    clay_c=material("V2 | unbaked brick, clay slip",(.39,.16,.085),.98)
    palette=[clay_a,clay_b,clay_c]
    props=[]
    # Short hand-split wooden plank on the high outer-right lip: a resting/work
    # surface for raw bricks, not a platform in the fire.
    props.append(mesh_box("V2 | rough support plank for unfired bricks",
        (.92,.54,.245),(.59,.36,.055),boardmat,k,
        angle=math.radians(-14),edge=.022,seed=401))
    # Shallow uneven board cuts, all real mesh (not hidden internal geometry).
    # Four damp handmade bricks, three loose on the board with one resting on top.
    staged=[
        (.76,.48,.335,-9),(.94,.49,.335,4),(1.07,.63,.335,-13),
        (.87,.56,.430,9)
    ]
    for i,(x,y,z,a) in enumerate(staged):
        props.append(mesh_box("V2 | WET BRICK on slab %02d"%(i+1),
            (x,y,z),(.235,.145,.095),palette[i%3],k,
            angle=math.radians(a),edge=.017,seed=520+i))
    # The actual firing arrangement: place hand-molded bricks on the inward
    # facing clay bank, OUTSIDE the 0.6-unit firewood/flame core. The ring is
    # deliberately incomplete so flames remain visible. Front + side arc.
    arc=[(-155,-.015),(-132,.015),(-105,-.02),(-73,.012),(-41,.020),
         (-14,-.016),(22,.013),(66,-.018),(109,.016),(145,-.009)]
    placed=[]
    for i,(deg,jitter) in enumerate(arc):
        th=math.radians(deg)
        radial=.88+jitter
        x=radial*math.cos(th)
        y=1.02*radial*math.sin(th)
        z=.075+(.02 if abs(deg)>100 else 0)
        # Tangential orientation of the long face; hand-set with uneven angles
        # to receive concentrated heat, not simply thrown on flames.
        ob=mesh_box("V2 | firing-bank WET BRICK %02d"%(i+1),
            (x,y,z),(.255,.16,.105),palette[(i+1)%3],firing,
            angle=th+math.pi/2+math.radians((i%3-1)*6),
            edge=.017,seed=650+i)
        hide_when_idle(ob)
        placed.append(ob)
    for ob in props+placed:
        parent_world(ob,root)
    scene.cycles.samples=args.samples
    scene.cycles.device="CPU"
    scene.render.film_transparent=True
    scene.render.resolution_x=scene.render.resolution_y=256
    scene.render.resolution_percentage=100
    scene.render.image_settings.file_format="PNG"
    scene.render.image_settings.color_mode="RGBA"
    scene.render.image_settings.color_depth="8"
    scene.render.fps=8
    frames=list(range(1,92,6))
    root.rotation_euler.z=0
    scene.frame_set(0)
    bpy.context.view_layer.update()
    master=out/"pit-kiln-v2.blend"
    scene.render.filepath="//renders/"
    bpy.ops.wm.save_as_mainfile(filepath=str(master),check_existing=False)
    records=[]
    for state,samples in (("idle",[0]),("burning",frames)):
        for d,angle in enumerate((0,90,180,270)):
            root.rotation_euler.z=math.radians(angle)
            for i,fr in enumerate(samples):
                scene.frame_set(fr)
                bpy.context.view_layer.update()
                path=out/(f"idle-d{d:02d}.png" if state=="idle"
                          else f"burning-d{d:02d}-f{i:03d}.png")
                scene.render.filepath=str(path)
                print("PIT_KILN_V2_RENDER",state,angle,i,flush=True)
                bpy.ops.render.render(write_still=True)
                records.append(dict(state=state,direction=d,angle=angle,index=i,
                                    frame=fr,path=path.name,sha256=sha(path)))
    root.rotation_euler.z=0
    scene.frame_set(0)
    report=dict(schema=2,asset="pit-kiln",revision="v2-wood-brick-staging",
        source_blend="pit-kiln-v1.blend",blender=bpy.app.version_string,
        source_mesh_count=prev_objects,
        reused_clay_pit_basin=True,reused_campfire_style_core=True,
        real_hand_formed_bricks=len(staged)+len(placed),
        staged_bricks=len(staged),staging_wooden_slab_count=1,
        inner_bank_bricks=len(placed),
        firing_bank_is_outside_flame_core=True,
        flame_count=len(flames),camera_elevation_deg=45,
        camera_ortho_scale=3.55,directions=[0,90,180,270],
        states={"idle":1,"burning":16},frame_count=len(records),
        samples=frames,master_sha256=sha(master),game_prototype_unchanged=True,
        user_accepted=False,captures=records)
    (out/"build-report.json").write_text(json.dumps(report,indent=2)+"\n")
    print("PIT_KILN_V2_CAPTURED",len(records),flush=True)

if __name__=="__main__":
    main()
