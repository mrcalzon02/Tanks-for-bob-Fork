#!/usr/bin/env python3
"""Pit Kiln V6: move entire slab and four bricks inward and pitch toward the fire pit.

Input: published Pit Kiln V5 .blend. Replace yaw rocking with inward pitching, keep
the real imported Campfire V9 flames, V3b hand keys, V4 crackle and bank bricks.
This is a visual candidate: DO NOT update Factorio prototypes or Mod Portal.
"""
import argparse, hashlib, json, math, sys
from pathlib import Path
import bpy
from mathutils import Matrix, Vector, Quaternion
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
    if any(b.parent is None or b.parent.name!="V5 | WHOLE TRAY wobble (wood plank + all four bricks)" for b in bricks):
        raise RuntimeError("Must begin with verified five-part V5 tray, not independently keyed bricks")
    if any(not f.animation_data or not f.animation_data.action for f in flames):
        raise RuntimeError("Original campfire mesh actions missing")
    actions={o.name:o.animation_data.action.name for o in flames}
    original_light_action=firelight.data.animation_data.action.name
    # Use V5's EXISTING shared tray grouping but remove the wrong spinning
    # action. Neither the board nor any of its four children gets its own keys.
    rig=bpy.data.objects.get("V5 | WHOLE TRAY wobble (wood plank + all four bricks)")
    if not rig or board.parent != rig or any(b.parent != rig for b in bricks):
        raise RuntimeError("Wooden board and every brick must share the SAME parent")
    if any(b.animation_data for b in bricks):
        raise RuntimeError("Individual brick twitching is forbidden")
    root.rotation_euler.z=0
    scene.frame_set(1)
    bpy.context.view_layer.update()
    center=board.matrix_world.translation.copy()
    toward=Vector((-center.x,-center.y,0))
    if toward.length<.1:raise RuntimeError("Tray is not located beside the pit")
    toward.normalize()
    # Tangential horizontal axis causes the INWARD EDGE to DIP, rather than
    # spinning around Z. Yaw remains identically zero in the local rig.
    tangent=Vector((-toward.y,toward.x,0))
    rig.animation_data_clear()
    rig.name="V6 | INWARD LATERAL and DOWNWARD PITCH | whole board + four bricks"
    rig.rotation_mode="QUATERNION"
    rig.rotation_quaternion=Quaternion((1,0,0,0))
    base=rig.location.copy()
    bpy.context.view_layer.update()
    children=[board]+bricks
    child_rel={ob.name:rig.matrix_world.inverted()@ob.matrix_world for ob in children}
    for n,frame in enumerate(FRAMES+[97]):
        u=(1-math.cos(2*math.pi*(n%16)/16))/2
        rig.location=base+toward*(.165*u)+Vector((0,0,-.018*u))
        rig.rotation_quaternion=Quaternion(tangent,math.radians(6.4*u))
        rig.keyframe_insert(data_path="location",frame=frame,group="WHOLE TRAY inward slide")
        rig.keyframe_insert(data_path="rotation_quaternion",frame=frame,group="WHOLE TRAY forward pitch")
    for fc in rig.animation_data.action.fcurves:
        for key in fc.keyframe_points:
            key.interpolation="BEZIER"
            key.handle_left_type=key.handle_right_type="AUTO_CLAMPED"
    if len({int(k.co.x) for fc in rig.animation_data.action.fcurves for k in fc.keyframe_points})!=17:
        raise RuntimeError("Shared tray keyframes missing")
    measures={}
    for d,angle in enumerate((0,90,180,270)):
        root.rotation_euler.z=math.radians(angle)
        samples={}
        for f in (1,49,97):
            scene.frame_set(f);bpy.context.view_layer.update()
            pos=board.matrix_world.translation.copy()
            ss=world_to_camera_view(scene,scene.camera,pos)
            verts=[board.matrix_world@v.co for v in board.data.vertices]
            samples[f]=(pos,(ss.x*256,(1-ss.y)*256),verts,rig.rotation_quaternion.copy())
        p1,s1,v1,q1=samples[1]
        p9,s9,v9,q9=samples[49]
        pe,se,ve,qe=samples[97]
        inward_world=root.matrix_world.to_quaternion()@toward
        sideways=Vector((-inward_world.y,inward_world.x,0))
        inward=(p9-p1).dot(inward_world)
        sideways_motion=abs((p9-p1).dot(sideways))
        travel=math.dist(s1,s9)
        seam=math.dist(s1,se)
        top_z=max(v.z for v in v1)
        idx=[i for i,v in enumerate(v1) if v.z>=top_z-.035]
        if len(idx)<4:raise RuntimeError("Could not identify real wood slab top edge")
        inner=max(idx,key=lambda i:v1[i].dot(inward_world))
        outer=min(idx,key=lambda i:v1[i].dot(inward_world))
        dip=(v9[inner].z-v9[outer].z)-(v1[inner].z-v1[outer].z)
        if inward<.12 or travel<5.5:raise RuntimeError(f"Tray did not move INWARD at {angle} deg")
        if sideways_motion>.012 or abs(q9.z)>.0001:raise RuntimeError("Spinning/yaw detected")
        if dip>-.018:raise RuntimeError(f"Inward tray edge did not pitch DOWN at {angle} deg: {dip}")
        if seam>.03:raise RuntimeError("Loop seam not closed")
        for ob in children:
            rel=rig.matrix_world.inverted()@ob.matrix_world
            for ar,br in zip(rel,child_rel[ob.name]):
                if any(abs(float(a)-float(b))>.0005 for a,b in zip(ar,br)):
                    raise RuntimeError("Brick or board detached from whole-tray parent")
        measures[str(angle)]={"inward_slide_units":round(inward,4),
           "unwanted_transverse_units":round(sideways_motion,5),
           "inner_edge_pitch_dip_units":round(dip,4),
           "screen_travel_px_256":round(travel,3),
           "screen_travel_px_64":round(travel/4,3),
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
    master=out/"pit-kiln-v6-inward-pitch.blend"
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
                print("PIT_KILN_V6_INWARD_PITCH",state,angle,t,flush=True)
                bpy.ops.render.render(write_still=True)
                captured.append({"state":state,"direction":d,"index":index,
                                 "frame":t,"path":path.name,"sha256":sha(path)})
    root.rotation_euler.z=0
    scene.frame_set(0)
    report={"schema":6,"revision":"v6-final-inward-lateral-slide-with-forward-pitch",
            "source_blend":"pit-kiln-v5-whole-tray.blend",
            "tray_rig":rig.name,"tray_children":[o.name for o in children],
            "rocking_plank_count":1,"rocking_brick_count":4,
            "per_brick_actions_remaining":0,"static_firing_bank_bricks":len(bank),
            "original_campfire_flames":len(flames),
            "original_campfire_source_actions":actions,
            "original_campfire_light_action":original_light_action,
            "preserved_v4_crackle_controls":len(crackles),
            "motion":"inward lateral slide + inward-edge down pitch, no yaw",
            "max_inward_units":.165,"max_pitch_deg":6.4,
            "tray_pixel_motion":measures,
            "four_directions":[0,90,180,270],"fps":8,
            "source_frames":len(captured),"master_sha256":sha(master),
            "visual_approved":False,"factorio_prototype_changed":False,
            "captures":captured}
    (out/"build-report.json").write_text(json.dumps(report,indent=2)+"\n")
    print("PIT_KILN_V6_COMPLETE_68_FRAMES",json.dumps(measures),flush=True)
if __name__=="__main__": main()
