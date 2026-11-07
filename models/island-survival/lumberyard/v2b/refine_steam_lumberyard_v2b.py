#!/usr/bin/env python3
"""V2b focused mechanical readability from actual saved V2 Blender master.

Keep the Franklin firebox, boiler, raw and split-log piles, four-way camera and
16-frame cutting sequence. Add a keyed steam piston/connecting rod synchronized
to the existing spinning flywheel, clearer continuous leather belt and more
visible true toothed saw disk. No new invented machinery unrelated to operation.
"""
import argparse,hashlib,json,math,sys
from pathlib import Path
import bpy
from mathutils import Vector

FRAMES=list(range(1,17))
DRIVE=Vector((-.17,.84,.87))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def relink(ob,col):
    for c in list(ob.users_collection):c.objects.unlink(ob)
    col.objects.link(ob)
    return ob

def rod(name,p,q,r,mat,col):
    a,b=Vector(p),Vector(q)
    dif=b-a
    bpy.ops.mesh.primitive_cylinder_add(vertices=12,radius=r,depth=dif.length,
                                        location=(a+b)/2)
    obj=relink(bpy.context.object,col)
    obj.name=name
    obj.rotation_euler=dif.to_track_quat("Z","Y").to_euler()
    obj.data.materials.append(mat)
    return obj,dif.length

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--out",required=True,type=Path)
    p.add_argument("--samples",type=int,default=28)
    a=p.parse_args(sys.argv[sys.argv.index("--")+1:])
    out=a.out.resolve()
    if out.exists() and any(out.iterdir()):
        raise ValueError("New output required: do not overwrite existing V2")
    out.mkdir(parents=True,exist_ok=True)
    scene=bpy.context.scene
    source_report=json.loads((Path(bpy.data.filepath).parent/"build-report.json").read_text())
    root=bpy.data.objects.get("EXPORT | turn lumberyard under fixed 45-degree camera")
    fly=bpy.data.objects.get("ANIM | driven steam flywheel")
    saw=bpy.data.objects.get("SAW | primitive 20-tooth circular steel saw")
    belt=bpy.data.objects.get("DRIVE | one continuous oiled leather belt")
    wheel=bpy.data.objects.get("ENGINE | five-spoke power flywheel")
    original=bpy.data.objects.get("WORK | whole log feeding through turning saw")
    halves=[o for o in scene.objects if o.name.startswith("WORK | cut half to receiving stack")]
    if (not root or not fly or not saw or not belt or not wheel or not original or
        len(halves)!=2 or not scene.camera or scene.camera.data.type!="ORTHO"):
        raise RuntimeError("The verified V2 steam lumberyard is missing")
    if not fly.animation_data or not fly.animation_data.action:
        raise RuntimeError("V2 power wheel is not keyed")
    if belt.type!="CURVE":
        raise RuntimeError("Expected an actual continuous Blender leather belt path")
    # Make the loop read as a primitive wide, leather power-transmission belt.
    belt.data.bevel_depth=.031
    belt.data.bevel_resolution=2
    oldmat=belt.data.materials[0]
    if not oldmat.name.startswith("dark oily drive belt"):
        raise RuntimeError("Belt material has unexpectedly changed")
    mat=oldmat.copy()
    mat.name="V2b | visible oil-dark leather drive belt"
    belt.data.materials.clear()
    belt.data.materials.append(mat)
    ramps=[n for n in mat.node_tree.nodes if n.type=="VALTORGB"]
    if len(ramps)!=1:
        raise RuntimeError("Original primitive leather ramp missing")
    ramp=ramps[0]
    ramp.color_ramp.elements[0].color=(.145,.089,.037,1)
    ramp.color_ramp.elements[1].color=(.38,.255,.118,1)
    # Original actual saw is a closed 20-toothed plate. Enlarge the disk
    # slightly (not its rotating hub) to make the teeth legible at native sprite size.
    saw.scale.y*=1.19
    saw.scale.z*=1.19
    # Exposed, actually moving brass piston slider with a visible crank rod.
    engine=bpy.data.collections.new("V2b | reciprocating piston and visible crank linkage")
    scene.collection.children.link(engine)
    brass=bpy.data.materials.get("boiler bronzed brass")
    iron=bpy.data.materials.get("primitive iron saw and hub")
    if not brass or not iron:raise RuntimeError("Material family missing")
    bpy.ops.mesh.primitive_cube_add(size=1,location=(-.20,1.04,.665))
    piston=relink(bpy.context.object,engine)
    piston.name="V2b | ACTUAL reciprocating steam piston slider"
    piston.dimensions=(.21,.16,.17)
    piston.data.materials.append(brass)
    base_start=Vector((-.19,1.065,.665))
    base_end=DRIVE+Vector((.055,.20,0))
    conn,original_len=rod("V2b | keyframed steam-engine connecting rod",
                          base_start,base_end,.029,iron,engine)
    # Both live in the existing model root. No unnecessary moving scenery.
    for ob in (piston,conn):
        transform=ob.matrix_world.copy()
        ob.parent=root
        ob.matrix_world=transform
    for index,frame in enumerate(FRAMES+(17,)):
        u=(index%16)/16
        theta=4*math.pi*u
        crank=DRIVE+Vector((.055,.20*math.cos(theta),.20*math.sin(theta)))
        start=Vector((-.19,1.065+.070*math.cos(theta),.665))
        v=crank-start
        conn.location=(start+crank)/2
        conn.rotation_euler=v.to_track_quat("Z","Y").to_euler()
        conn.scale.z=v.length/original_len
        for path in ("location","rotation_euler","scale"):
            conn.keyframe_insert(data_path=path,frame=frame,group="steam power transmission")
        piston.location=(-.20,1.04+.070*math.cos(theta),.665)
        piston.keyframe_insert(data_path="location",frame=frame,group="steam piston strokes")
    scene.frame_set(0)
    for ob in (piston,conn):
        for fc in ob.animation_data.action.fcurves:
            for key in fc.keyframe_points:
                key.interpolation="BEZIER"
                key.handle_left_type=key.handle_right_type="AUTO_CLAMPED"
    # Validate the piston really changes position independently of the flame.
    coords=[]
    for frame in (1,5,9,13):
        scene.frame_set(frame)
        bpy.context.view_layer.update()
        coords.append(tuple(round(float(q),5) for q in piston.location))
    if len(set(coords))<2:
        raise RuntimeError("Reciprocating piston does not move")
    if len({int(k.co.x) for fc in piston.animation_data.action.fcurves
            for k in fc.keyframe_points})!=17:
        raise RuntimeError("Piston 16-frame loop is not authored")
    scene.cycles.samples=a.samples
    scene.cycles.use_denoising=False
    for layer in scene.view_layers:
        layer.cycles.use_denoising=False
    scene.render.resolution_x=scene.render.resolution_y=256
    scene.render.resolution_percentage=100
    scene.render.film_transparent=True
    scene.render.image_settings.file_format="PNG"
    scene.render.image_settings.color_mode="RGBA"
    scene.render.image_settings.color_depth="8"
    scene.render.fps=8
    root.rotation_euler.z=0
    scene.frame_set(0)
    scene.render.filepath="//renders/"
    master=out/"steam-lumberyard-v2b.blend"
    bpy.ops.wm.save_as_mainfile(filepath=str(master),check_existing=False)
    captures=[]
    for state,frames in (("idle",(0,)),("working",FRAMES)):
        for d,deg in enumerate((0,90,180,270)):
            root.rotation_euler.z=math.radians(deg)
            for index,t in enumerate(frames):
                scene.frame_set(t)
                bpy.context.view_layer.update()
                name=(f"idle-d{d:02d}.png" if state=="idle"
                      else f"working-d{d:02d}-f{index:03d}.png")
                file=out/name
                scene.render.filepath=str(file)
                print("LUMBERYARD_V2B_ACTUAL",state,deg,index,flush=True)
                bpy.ops.render.render(write_still=True)
                captures.append({"state":state,"direction":d,"index":index,
                    "angle":deg,"frame":t,"path":name,"sha256":sha(file)})
    root.rotation_euler.z=0
    scene.frame_set(0)
    prior=source_report
    prior.update(schema=3,revision="steam-lumberyard-v2b-visible-power-transmission",
                 source_blend="steam-lumberyard-v2.blend",
                 piston_animation_keys=17,connecting_rod_animation_keys=17,
                 piston_sample_positions=coords,
                 increased_belt_width=True,
                 increased_visible_tooth_silhouette=True,
                 counts={**prior["counts"],"reciprocating_steam_pistons":1,
                    "moving_crank_rods":1},
                 source_frames=68,captures=captures,master_sha256=sha(master),
                 visual_approved=False,game_prototype_unchanged=True)
    (out/"build-report.json").write_text(json.dumps(prior,indent=2)+"\n")
    print("STEAM_LUMBERYARD_V2B_CAPTURED",len(captures),flush=True)

if __name__=="__main__":main()
