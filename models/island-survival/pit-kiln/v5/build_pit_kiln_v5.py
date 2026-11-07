#!/usr/bin/env python3
"""Pit Kiln V5: rock the WHOLE wooden tray + all four wet bricks as one assembly.

Input: published Pit Kiln V4 .blend. Remove old individual brick motion, keep
the real imported Campfire V9 flames, V3b hand keys, V4 crackle and bank bricks.
This is a visual candidate: DO NOT update Factorio prototypes or Mod Portal.
"""
import argparse, hashlib, json, math, sys
from pathlib import Path
import bpy
from mathutils import Matrix, Vector
from bpy_extras.object_utils import world_to_camera_view

FRAMES=list(range(1,92,6))
def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--out",type=Path,required=True)
    p.add_argument("--samples",type=int,default=28)
    opt=p.parse_args(sys.argv[sys.argv.index("--")+1:])
    out=opt.out.resolve()
    if out.exists() and any(out.iterdir()):
        raise ValueError("New empty output directory required: do not overwrite V4")
    out.mkdir(parents=True,exist_ok=True)
    scene=bpy.context.scene
    root=bpy.data.objects.get("EXPORT | rotate all clay and tools, never camera")
    board=bpy.data.objects.get("V2 | rough support plank for unfired bricks")
    bricks=sorted((o for o in scene.objects if o.name.startswith("V2 | WET BRICK on slab")),key=lambda o:o.name)
    bank=[o for o in scene.objects if o.name.startswith("V2 | firing-bank WET BRICK")]
    flames=[o for o in scene.objects if o.name.startswith("flame_tongue")]
    crackles=[o for o in scene.objects if o.name.startswith("V4 | original flame crackle")]
    firelight=bpy.data.objects.get("04 | animated fire light")
    if not root or not board or len(bricks)!=4 or len(bank)!=10 or len(flames)!=6 or len(crackles)!=6 or not firelight:
        raise RuntimeError("Required V4 kiln/real campfire/whole tray model is missing")
    if not scene.camera or scene.camera.data.type!="ORTHO" or abs(scene.camera.data.ortho_scale-3.55)>.001:
        raise RuntimeError("Incorrect existing 45-degree structure camera")
    if any(not b.animation_data or not b.animation_data.action for b in bricks):
        raise RuntimeError("Expected independent V4 brick keys to REMOVE")
    if any(not f.animation_data or not f.animation_data.action for f in flames):
        raise RuntimeError("Original campfire mesh actions missing")
    actions={o.name:o.animation_data.action.name for o in flames}
    original_light_action=firelight.data.animation_data.action.name
    # Work from first working frame, including the authored original placements.
    root.rotation_euler.z=0
    scene.frame_set(1)
    bpy.context.view_layer.update()
    original_world={o.name:o.matrix_world.copy() for o in [board]+bricks}
    # Eliminate individual wobble completely. No per-brick actions remain.
    for brick in bricks:
        brick.animation_data_clear()
    rig=bpy.data.objects.new("V5 | WHOLE TRAY wobble (wood plank + all four bricks)",None)
    scene.collection.objects.link(rig)
    rig.matrix_world=Matrix.Translation(original_world[board.name].translation)
    bpy.context.view_layer.update()
    rig_world=rig.matrix_world.copy()
    rig.parent=root
    rig.matrix_world=rig_world
    bpy.context.view_layer.update()
    for ob in [board]+bricks:
        ob.parent=rig
        ob.matrix_world=original_world[ob.name]
    bpy.context.view_layer.update()
    if any((ob.matrix_world.translation-original_world[ob.name].translation).length>.0001
           for ob in [board]+bricks):
        raise RuntimeError("Parenting altered board/brick positions")
    # Shared pendulum-like rock: +7 degrees around tray center with very small
    # transverse movement. The plank and ALL FOUR bricks move together, rigidly.
    loc=rig.location.copy()
    for n,t in enumerate(FRAMES+[97]):
        phase=2*math.pi*(n%16)/16
        rig.rotation_euler=(math.radians(1.3*math.sin(phase+.5)-.62),
                            math.radians(1.4*math.sin(phase-.7)+.9),
                            math.radians(7.0*math.sin(phase)))
        rig.location=(loc.x+.040*math.sin(phase),loc.y+.020*math.sin(phase),loc.z)
        rig.keyframe_insert(data_path="rotation_euler",frame=t,group="ENTIRE wooden tray rocking")
        rig.keyframe_insert(data_path="location",frame=t,group="ENTIRE wooden tray rocking")
    for fc in rig.animation_data.action.fcurves:
        for key in fc.keyframe_points:
            key.interpolation="BEZIER"
            key.handle_left_type=key.handle_right_type="AUTO_CLAMPED"
    if any(brick.animation_data for brick in bricks):
        raise RuntimeError("Per-brick wobble was not cleared")
    if len({int(key.co.x) for fc in rig.animation_data.action.fcurves for key in fc.keyframe_points})!=17:
        raise RuntimeError("Whole-tray loop must have 16 samples plus seam key")
    # Separate the actual moving slab from fire flicker: measure the same four
    # slab mesh corners directly in camera space across opposing positions.
    measures={}
    for d,angle in enumerate((0,90,180,270)):
        root.rotation_euler.z=math.radians(angle)
        coords={}
        for frame in (1,25,49,73,97):
            scene.frame_set(frame)
            bpy.context.view_layer.update()
            coords[frame]=[]
            for vert in board.data.vertices:
                pos=board.matrix_world@vert.co
                screen=world_to_camera_view(scene,scene.camera,pos)
                coords[frame].append((float(screen.x)*256,float(1-screen.y)*256))
        distance=max(math.dist(coords[25][i],coords[73][i]) for i in range(len(coords[25])))
        seam=max(math.dist(coords[1][i],coords[97][i]) for i in range(len(coords[1])))
        if distance<3.5:
            raise RuntimeError(f"Whole tray is not moving visibly at {angle} deg: {distance:.2f} px")
        if seam>.15:
            raise RuntimeError(f"Whole tray loop seam is not closed at {angle} deg: {seam:.3f} px")
        measures[str(angle)]={"tray_corner_motion_px_256":round(distance,3),
                              "equivalent_px_64":round(distance/4,3),
                              "seam_px_256":round(seam,4)}
    root.rotation_euler.z=0
    scene.cycles.samples=opt.samples
    scene.cycles.device="CPU"
    scene.render.engine="CYCLES"
    scene.render.film_transparent=True
    scene.render.resolution_x=256
    scene.render.resolution_y=256
    scene.render.resolution_percentage=100
    scene.render.image_settings.file_format="PNG"
    scene.render.image_settings.color_mode="RGBA"
    scene.render.image_settings.color_depth="8"
    scene.render.fps=8
    scene.frame_set(0)
    scene.render.filepath="//rendered/"
    master=out/"pit-kiln-v5-whole-tray.blend"
    bpy.ops.wm.save_as_mainfile(filepath=str(master),check_existing=False)
    captured=[]
    for state,frames in (("idle",[0]),("burning",FRAMES)):
        for d,angle in enumerate((0,90,180,270)):
            root.rotation_euler.z=math.radians(angle)
            for index,t in enumerate(frames):
                scene.frame_set(t)
                bpy.context.view_layer.update()
                path=out/(f"idle-d{d:02d}.png" if state=="idle" else f"burning-d{d:02d}-f{index:03d}.png")
                scene.render.filepath=str(path)
                print("PIT_KILN_V5_WHOLE_TRAY",state,angle,t,flush=True)
                bpy.ops.render.render(write_still=True)
                captured.append({"state":state,"direction":d,"index":index,
                                 "frame":t,"path":path.name,"sha256":sha(path)})
    root.rotation_euler.z=0
    scene.frame_set(0)
    report={"schema":5,"revision":"v5-whole-tray-rock-and-preserved-campfire-crackle",
            "source_blend":"pit-kiln-v4-animated.blend",
            "tray_rig":rig.name,
            "tray_children":[o.name for o in [board]+bricks],
            "rocking_plank_count":1,"rocking_brick_count":4,
            "per_brick_actions_remaining":sum(bool(b.animation_data) for b in bricks),
            "static_firing_bank_bricks":len(bank),
            "original_campfire_flames":6,
            "original_campfire_source_actions":actions,
            "original_campfire_light_action":original_light_action,
            "preserved_v4_crackle_controls":len(crackles),
            "shared_wobble_angle_deg":7.0,
            "tray_pixel_motion":measures,
            "four_directions":[0,90,180,270],"fps":8,
            "source_frames":len(captured),"master_sha256":sha(master),
            "visual_approved":False,"factorio_prototype_changed":False,
            "captures":captured}
    (out/"build-report.json").write_text(json.dumps(report,indent=2)+"\n")
    print("PIT_KILN_V5_COMPLETE_68_FRAMES",json.dumps(measures),flush=True)
if __name__=="__main__": main()
