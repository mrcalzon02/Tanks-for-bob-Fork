#!/usr/bin/env python3
"""Add 16 hand-authored kiln-specific keys to each real imported campfire flame."""
import argparse,json,hashlib,math,sys
from pathlib import Path
import bpy

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def run():
    ap=argparse.ArgumentParser()
    ap.add_argument("--out",required=True,type=Path)
    args=ap.parse_args(sys.argv[sys.argv.index("--")+1:])
    out=args.out.resolve()
    if out.exists() and any(out.iterdir()):raise ValueError("New output required")
    out.mkdir(parents=True,exist_ok=True)
    scene=bpy.context.scene
    original=Path(bpy.data.filepath)
    old=json.loads((original.parent/"build-report.json").read_text())
    flames=sorted((o for o in scene.objects if o.name.startswith("flame_tongue")),key=lambda o:o.name)
    group=bpy.data.objects.get("V3 | campfire animation retargeted to kiln hearth")
    root=bpy.data.objects.get("EXPORT | rotate all clay and tools, never camera")
    if len(flames)!=6 or not group or not root:
        raise ValueError("Missing original V9 flame objects/retarget root")
    if not all(o.parent==group and o.animation_data and o.animation_data.action for o in flames):
        raise ValueError("Missing existing campfire source animation")
    x=(0,.011,.029,.021,-.006,-.020,-.014,.014,.031,.006,-.022,-.029,-.004,.017,.022,.011)
    y=(0,-.011,-.009,.015,.018,-.008,-.020,-.005,.019,.023,-.006,-.025,-.009,.012,.015,.006)
    z=(0,.030,.069,.040,-.008,.048,.098,.026,-.014,.035,.080,.050,-.020,.018,.074,.034)
    twist=(-.04,.04,.11,.05,-.06,-.10,.03,.12,.05,-.07,-.11,-.03,.08,.12,.025,-.035)
    samples=list(range(1,92,6))
    scene.frame_set(1);bpy.context.view_layer.update()
    controls=[]
    for index,flame in enumerate(flames):
        helper=bpy.data.objects.new("V3b | HAND-KEYED original flame %02d"%(index+1),None)
        scene.collection.objects.link(helper)
        original_world=flame.matrix_world.copy()
        helper.matrix_world=original_world
        bpy.context.view_layer.update()
        helper.parent=group
        helper.matrix_world=original_world
        bpy.context.view_layer.update()
        flame.parent=helper
        flame.matrix_world=original_world
        bpy.context.view_layer.update()
        origin=helper.location.copy()
        original_rot=helper.rotation_euler.z
        phase=(index*3)%16
        amplitude=.7+(index%3)*.2
        for t,frame in enumerate(samples+[97]):
            k=(t+phase)%16 if t<16 else phase
            helper.location=(origin.x+x[k]*amplitude,
                             origin.y+y[(k+2*index)%16]*amplitude,
                             origin.z+z[k]*(.78+.07*index))
            helper.rotation_euler.z=original_rot+twist[(k+index)%16]*(.55+.08*index)
            helper.keyframe_insert(data_path="location",frame=frame)
            helper.keyframe_insert(data_path="rotation_euler",frame=frame)
        for curve in helper.animation_data.action.fcurves:
            for key in curve.keyframe_points:
                key.interpolation="BEZIER"
                key.handle_left_type=key.handle_right_type="AUTO_CLAMPED"
        controls.append(helper)
    scene.frame_set(1);bpy.context.view_layer.update()
    first=[tuple(round(v,4) for v in obj.location) for obj in controls]
    scene.frame_set(49);bpy.context.view_layer.update()
    second=[tuple(round(v,4) for v in obj.location) for obj in controls]
    if first==second:raise ValueError("Hand-keyed parent movement does not evaluate")
    if len(old.get("source_actions",{}))!=6:raise ValueError("Original V9 action hashes missing")
    scene.render.engine="CYCLES"
    scene.cycles.samples=24
    scene.cycles.device="CPU"
    scene.render.resolution_x=scene.render.resolution_y=256
    scene.render.resolution_percentage=100
    scene.render.image_settings.file_format="PNG"
    scene.render.image_settings.color_mode="RGBA"
    scene.render.image_settings.color_depth="8"
    scene.render.film_transparent=True
    scene.render.fps=8
    root.rotation_euler.z=0;scene.frame_set(0)
    master=out/"pit-kiln-v3-real-campfire.blend"
    scene.render.filepath="//renders/"
    bpy.ops.wm.save_as_mainfile(filepath=str(master),check_existing=False)
    records=[]
    for state,frames in (("idle",[0]),("burning",samples)):
        for d,angle in enumerate((0,90,180,270)):
            root.rotation_euler.z=math.radians(angle)
            for idx,frame in enumerate(frames):
                scene.frame_set(frame);bpy.context.view_layer.update()
                target=out/(f"idle-d{d:02d}.png" if state=="idle" else f"burning-d{d:02d}-f{idx:03d}.png")
                scene.render.filepath=str(target)
                print("KILN_HAND_ANIMATED",state,angle,idx,flush=True)
                bpy.ops.render.render(write_still=True)
                records.append(dict(state=state,direction=d,angle=angle,index=idx,
                                    frame=frame,path=target.name,sha256=sha(target)))
    root.rotation_euler.z=0;scene.frame_set(0)
    old.update(source_frames=68,captures=records,master_sha256=sha(master),
               kiln_revision="v3b-hand-authored-six-original-flames",
               hand_keyed_original_flames=6,hand_keyed_per_flame=17,
               user_visual_accepted=False,game_prototype_changed=False)
    (out/"build-report.json").write_text(json.dumps(old,indent=2)+"\n")
    print("KILN_V3B_HAND_AUTHORED_68_REAL_RENDER_FRAMES",flush=True)
if __name__=="__main__":run()
