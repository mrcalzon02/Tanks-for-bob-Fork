#!/usr/bin/env python3
"""Pit Kiln V3: correct V2 by importing the REAL, pre-animated V9 campfire flames/light.

All six authored meshes, their animation actions and material graphs come from
the saved native Campfire V9 Blender model. Not newly drawn flame planes.
The V2 wet-brick firing bank and hand-made staging board remain unchanged.
"""
import argparse,hashlib,json,math,sys
from pathlib import Path
import bpy
from mathutils import Vector

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--out",required=True,type=Path)
    p.add_argument("--campfire",required=True,type=Path)
    p.add_argument("--samples",type=int,default=24)
    a=p.parse_args(sys.argv[sys.argv.index("--")+1:])
    out=a.out.resolve()
    if out.exists() and any(out.iterdir()):raise ValueError("V3 output must be empty/new")
    out.mkdir(parents=True,exist_ok=True)
    src=a.campfire.resolve()
    if not src.is_file():raise FileNotFoundError("Real authored campfire Blender source missing: "+str(src))
    scene=bpy.context.scene
    root=bpy.data.objects.get("EXPORT | rotate all clay and tools, never camera")
    staged=[o for o in scene.objects if o.name.startswith("V2 | WET BRICK on slab")]
    placed=[o for o in scene.objects if o.name.startswith("V2 | firing-bank WET BRICK")]
    plank=bpy.data.objects.get("V2 | rough support plank for unfired bricks")
    old_flames=[o for o in scene.objects if o.name.startswith("BURNING | flame tongue")]
    old_light=bpy.data.objects.get("BURNING | local kiln fire light")
    if not root or len(staged)!=4 or len(placed)!=10 or not plank:
        raise ValueError("Real V2 wet-brick kiln source missing or changed")
    if len(old_flames)!=8 or old_light is None:
        raise ValueError("Expected eight independently invented V1 flames to replace")
    if not scene.camera or scene.camera.data.type!="ORTHO" or abs(scene.camera.data.ortho_scale-3.55)>.001:
        raise ValueError("Expected preserved fixed 45-degree structure camera")
    # Delete the WRONG V1/V2 stand-in fire. Do not keep two overlapping effects.
    for o in old_flames+[old_light]:
        bpy.data.objects.remove(o,do_unlink=True)
    with bpy.data.libraries.load(str(src),link=False) as (available,loaded):
        flame_names=sorted(n for n in available.objects if n.startswith("flame_tongue"))
        if len(flame_names)!=6:raise ValueError("Real Campfire V9 must contain exactly six flame meshes")
        source_light="04 | animated fire light"
        if source_light not in available.objects:raise ValueError("Original keyed light missing")
        loaded.objects=flame_names+[source_light]
    objects={ob.name:ob for ob in loaded.objects if ob}
    if len(objects)!=7:raise RuntimeError("Failed to append all seven REAL campfire animation objects")
    flames=[objects[n] for n in flame_names]
    light=objects[source_light]
    if any(ob.type!="MESH" or not ob.animation_data or not ob.animation_data.action for ob in flames):
        raise ValueError("Imported original flame actions or geometry were not preserved")
    if light.type!="LIGHT" or not light.data.animation_data or not light.data.animation_data.action:
        raise ValueError("Imported original campfire light keys missing")
    # The old campfire scene also has six actual flame mesh shape/scale keyframes.
    # Their animation should be inherited, not procedurally approximated here.
    source_actions={ob.name:ob.animation_data.action.name for ob in flames}
    collection=bpy.data.collections.new("V3 | REUSED ACTUAL CAMPFIRE V9 keyframed fire")
    scene.collection.children.link(collection)
    for ob in flames+[light]:
        collection.objects.link(ob)
        if ob.parent is not None:
            raise ValueError("Original source fire requires unsupported parent hierarchy: "+ob.name)
    # One transform groups the authored original animation into the kiln. This
    # does not replace any of the source's individual keyframes or materials.
    assembly=bpy.data.objects.new("V3 | campfire animation retargeted to kiln hearth",None)
    collection.objects.link(assembly)
    assembly.location=(0,-.03,-.055)
    assembly.scale=(.90,.90,.87)
    scene.frame_set(1)
    bpy.context.view_layer.update()
    for ob in flames+[light]:
        ob.parent=assembly
        ob.matrix_parent_inverse.identity()
    assembly.parent=root
    # Light stays local to the flame; its original keyframed energy is retained.
    for ob in flames+[light]:
        ob.hide_render=True;ob.keyframe_insert(data_path="hide_render",frame=0)
        ob.hide_render=False;ob.keyframe_insert(data_path="hide_render",frame=1)
        ob.keyframe_insert(data_path="hide_render",frame=97)
        for fc in ob.animation_data.action.fcurves:
            if fc.data_path=="hide_render":
                for point in fc.keyframe_points:point.interpolation="CONSTANT"
    frames=list(range(1,92,6))
    # Original V9 already runs its 16-frame cycle on these timeline samples.
    # Validate that our saved scene genuinely changes the 6 flame geometries.
    scene.frame_set(1)
    start=[tuple(round(float(v),5) for v in ob.scale) for ob in flames]
    e1=light.data.energy
    scene.frame_set(49)
    middle=[tuple(round(float(v),5) for v in ob.scale) for ob in flames]
    e2=light.data.energy
    if start==middle or abs(e1-e2)<.005:
        raise ValueError("Imported campfire flame movement or authored light flicker not playing")
    if any(o.hide_render for o in flames):
        raise ValueError("Imported flames incorrectly hidden on active frame")
    scene.render.engine="CYCLES"
    scene.cycles.device="CPU"
    scene.cycles.samples=a.samples
    scene.render.film_transparent=True
    scene.render.resolution_x=scene.render.resolution_y=256
    scene.render.resolution_percentage=100
    scene.render.image_settings.file_format="PNG"
    scene.render.image_settings.color_mode="RGBA"
    scene.render.image_settings.color_depth="8"
    scene.render.fps=8
    root.rotation_euler.z=0
    scene.frame_set(0)
    scene.render.filepath="//renders/"
    bpy.context.view_layer.update()
    master=out/"pit-kiln-v3-real-campfire.blend"
    bpy.ops.wm.save_as_mainfile(filepath=str(master),check_existing=False)
    record=[]
    for state,samples in (("idle",[0]),("burning",frames)):
        for d,angle in enumerate([0,90,180,270]):
            root.rotation_euler.z=math.radians(angle)
            for idx,f in enumerate(samples):
                scene.frame_set(f)
                bpy.context.view_layer.update()
                target=out/(f"idle-d{d:02d}.png" if state=="idle"
                            else f"burning-d{d:02d}-f{idx:03d}.png")
                scene.render.filepath=str(target)
                print("REAL_CAMPFIRE_V3_RENDER",state,angle,idx,flush=True)
                bpy.ops.render.render(write_still=True)
                record.append(dict(state=state,direction=d,angle=angle,index=idx,
                                   frame=f,path=target.name,sha256=sha(target)))
    root.rotation_euler.z=0;scene.frame_set(0)
    (out/"build-report.json").write_text(json.dumps(dict(
        version=3,source_blend="pit-kiln-v2.blend",
        imported_campfire_blend=str(src.name),imported_campfire_sha256=sha(src),
        imported_flame_count=len(flames),removed_old_fake_flames=len(old_flames),
        imported_campfire_light=light.name,source_actions=source_actions,
        retained_staging_bricks=4,retained_bank_bricks=10,
        dimensions=[256,256],animation_frames=16,source_frames=68,fps=8,
        camera_elevation_deg=45,angle_directions=[0,90,180,270],
        master_sha256=sha(master),asset_approved=False,
        game_prototype_changed=False,captures=record
    ),indent=2)+"\n")
    print("PIT_KILN_V3_TRUE_CAMPFIRE_ANIMATION_CAPTURED",len(record),flush=True)

if __name__=="__main__":main()
