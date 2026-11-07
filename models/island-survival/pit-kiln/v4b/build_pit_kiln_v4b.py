#!/usr/bin/env python3
"""Pit Kiln V4: brick wobble plus visual fire crackle atop the real V9 campfire.

Input is the saved V3b .blend. Preserve every source flame mesh/action,
Clay Pit earthwork, and the wet-brick board and firing bank.
"""
import argparse,hashlib,json,math,sys
from pathlib import Path
import bpy
from mathutils import Matrix

FRAMES=list(range(1,92,6))
PULSE=(.12,.70,-.22,.48,.84,-.33,.31,-.58,.77,.26,-.41,.60,-.16,.89,-.35,.20)
BRIGHT=(.84,1.16,.76,1.22,.91,1.31,.70,1.13,.88,1.25,.75,1.15,.95,1.28,.79,1.03)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def keyed(ob):
    assert ob.animation_data and ob.animation_data.action,ob.name
    for f in ob.animation_data.action.fcurves:
        if f.data_path in ("rotation_euler","scale","location"):
            for k in f.keyframe_points:
                k.interpolation="BEZIER"
                k.handle_left_type=k.handle_right_type="AUTO_CLAMPED"
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--out",type=Path,required=True)
    ap.add_argument("--samples",type=int,default=28)
    a=ap.parse_args(sys.argv[sys.argv.index("--")+1:])
    out=a.out.resolve()
    if out.exists() and any(out.iterdir()):raise ValueError("Use new V4 output path")
    out.mkdir(parents=True,exist_ok=True)
    scene=bpy.context.scene
    root=bpy.data.objects.get("EXPORT | rotate all clay and tools, never camera")
    board=bpy.data.objects.get("V2 | rough support plank for unfired bricks")
    bricks=sorted((o for o in scene.objects if o.name.startswith("V2 | WET BRICK on slab")),key=lambda o:o.name)
    bank=[o for o in scene.objects if o.name.startswith("V2 | firing-bank WET BRICK")]
    flames=sorted((o for o in scene.objects if o.name.startswith("flame_tongue")),key=lambda o:o.name)
    helpers=sorted((o for o in scene.objects if o.name.startswith("V3b | HAND-KEYED original flame")),key=lambda o:o.name)
    source_light=bpy.data.objects.get("04 | animated fire light")
    if not(root and board and len(bricks)==4 and len(bank)==10 and
           len(flames)==len(helpers)==6 and source_light and source_light.type=="LIGHT"):
        raise RuntimeError("Real V3b campfire/board/brick source not present")
    if not scene.camera or scene.camera.data.type!="ORTHO" or abs(scene.camera.data.ortho_scale-3.55)>.001:
        raise RuntimeError("Structure camera mismatch")
    for f in flames:
        if f.parent not in helpers or not f.animation_data or not f.animation_data.action:
            raise RuntimeError("Original imported campfire animation not intact")
    if not source_light.data.animation_data or not source_light.data.animation_data.action:
        raise RuntimeError("Original Campfire V9 light animation missing")
    original_actions={f.name:f.animation_data.action.name for f in flames}
    # ENTIRE staged tray is ONE coherent rigid assembly. The wood support plank
    # and ALL four wet bricks share a single pivot. The previous four unrelated
    # brick animations are eliminated rather than layered underneath.
    scene.frame_set(1)
    root.rotation_euler.z=0
    bpy.context.view_layer.update()
    center=board.matrix_world.translation.copy()
    tray=bpy.data.objects.new("V4b | COMPLETE TRAY AND FOUR BRICKS | rock together",None)
    scene.collection.objects.link(tray)
    tray.matrix_world=Matrix.Translation(center)
    bpy.context.view_layer.update()
    world=tray.matrix_world.copy()
    tray.parent=root
    tray.matrix_world=world
    bpy.context.view_layer.update()
    tray_parts=[board]+bricks
    for ob in tray_parts:
        saved=ob.matrix_world.copy()
        # No individual wobble actions inherited from an older version.
        if ob.animation_data:
            ob.animation_data_clear()
        ob.parent=tray
        ob.matrix_world=saved
        bpy.context.view_layer.update()
    for j,t in enumerate(FRAMES+[97]):
        phase=2*math.pi*(j%16)/16
        tray.location=(center.x+.040*math.cos(phase),
                       center.y+.018*math.cos(phase+.30),
                       center.z+.009*math.sin(phase))
        tray.rotation_euler=(math.radians(4.4)*math.cos(phase+.2),
                             math.radians(5.3)*math.cos(phase),
                             math.radians(3.2)*math.cos(phase+.4))
        tray.keyframe_insert(data_path="location",frame=t,group="Entire wooden tray rock")
        tray.keyframe_insert(data_path="rotation_euler",frame=t,group="Entire wooden tray rock")
    keyed(tray)
    # Blender-space proof is independent of changing firelight: measure the
    # positions of a real corner of the plank and EACH wet brick in all four
    # orientations, between opposite swing extremes. Firing-bank stays fixed.
    from bpy_extras.object_utils import world_to_camera_view
    geometry_motion={}
    for d,orientation in enumerate((0,90,180,270)):
        root.rotation_euler.z=math.radians(orientation)
        positions={}
        for frame in (1,49):
            scene.frame_set(frame)
            bpy.context.view_layer.update()
            values=[]
            for ob in tray_parts:
                point=ob.matrix_world @ ob.data.vertices[0].co
                camera_point=world_to_camera_view(scene,scene.camera,point)
                values.append((camera_point.x*256,(1-camera_point.y)*256))
            positions[frame]=values
        travels=[round(math.hypot(a[0]-z[0],a[1]-z[1]),3)
                 for a,z in zip(positions[1],positions[49])]
        if min(travels)<2.0:
            raise RuntimeError(f"Whole tray motion unreadable in direction {orientation}: {travels}")
        geometry_motion[str(orientation)]={"wooden_tray_px_256":travels[0],
            "four_bricks_px_256":travels[1:],"lowest_px_256":min(travels)}
        # Inner-bank brick geometry is never parented to the tray.
        if any(ob.parent==tray for ob in bank):
            raise RuntimeError("Firing-bank bricks incorrectly connected to tray")
    root.rotation_euler.z=0
    scene.frame_set(1)
    bpy.context.view_layer.update()
    # Extra identity-parent layer changes the six already-animated native flames,
    # without replacing their mesh, materials, source actions, or V3b actions.
    col=bpy.data.collections.new("V4 | crackle layers on original campfire")
    scene.collection.children.link(col)
    crackles=[]
    scene.frame_set(1);bpy.context.view_layer.update()
    for i,f in enumerate(flames):
        parent=f.parent
        old_world=f.matrix_world.copy()
        ctl=bpy.data.objects.new("V4 | original flame crackle %02d"%(i+1),None)
        col.objects.link(ctl)
        ctl.parent=parent
        ctl.matrix_parent_inverse.identity()
        ctl.location=(0,0,0);ctl.rotation_euler=(0,0,0);ctl.scale=(1,1,1)
        bpy.context.view_layer.update()
        f.parent=ctl
        f.matrix_parent_inverse.identity()
        bpy.context.view_layer.update()
        if (f.matrix_world.translation-old_world.translation).length>.001:
            raise RuntimeError("Crackle parent changed source flame baseline transform")
        for j,t in enumerate(FRAMES+[97]):
            k=(j%16+3*i)%16
            change=PULSE[k]
            ctl.scale=(1+.06*change,1+.045*PULSE[(k+5)%16],1+.30*change)
            ctl.rotation_euler.z=math.radians(3.2*change)
            ctl.keyframe_insert(data_path="scale",frame=t,group="Kiln fire crackle")
            ctl.keyframe_insert(data_path="rotation_euler",frame=t,group="Kiln fire crackle")
        keyed(ctl)
        crackles.append(ctl)
    # Short, irregular glow pulses complement the ORIGINAL, still-keyed fire light.
    data=bpy.data.lights.new("V4 | crackling ember illumination","POINT")
    data.color=(1,.43,.17);data.shadow_soft_size=.25
    light=bpy.data.objects.new("V4 | additional small crackle light",data)
    col.objects.link(light)
    light.parent=root
    light.location=(0,-.08,.20)
    light.hide_render=True;light.keyframe_insert(data_path="hide_render",frame=0)
    light.hide_render=False;light.keyframe_insert(data_path="hide_render",frame=1)
    light.keyframe_insert(data_path="hide_render",frame=97)
    for j,t in enumerate(FRAMES+[97]):
        data.energy=.8*BRIGHT[j%16]
        data.keyframe_insert(data_path="energy",frame=t)
    # Two small popping amber embers, not new flame meshes.
    ember_mat=bpy.data.materials.new("V4 | small crackling amber ember")
    ember_mat.use_nodes=True
    p=ember_mat.node_tree.nodes.get("Principled BSDF")
    p.inputs["Base Color"].default_value=(1,.28,.045,1)
    p.inputs["Emission Color"].default_value=(1,.45,.09,1)
    p.inputs["Emission Strength"].default_value=1.1
    embers=[]
    for i in range(2):
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1,radius=.021,location=(0,0,.15))
        ob=bpy.context.object
        for original in list(ob.users_collection):original.objects.unlink(ob)
        col.objects.link(ob)
        ob.name="V4 | pop ember %02d"%(i+1)
        ob.data.materials.append(ember_mat)
        ob.parent=root
        ob.hide_render=True;ob.keyframe_insert(data_path="hide_render",frame=0)
        for j,t in enumerate(FRAMES+[97]):
            phase=(j%16+3*i)%8
            ob.location=(-.08+.065*i+.012*phase,-.06+.04*i,.13+.033*phase)
            ob.scale=(.75,.75,.75)
            ob.hide_render=phase<2 or phase>5
            ob.keyframe_insert(data_path="location",frame=t)
            ob.keyframe_insert(data_path="hide_render",frame=t)
        keyed(ob);embers.append(ob)
    # Ensure no individual brick wobble survived, and one keyed control owns all
    # five objects. The existing six imported campfire animations are untouched.
    if any(ob.parent!=tray or ob.animation_data for ob in tray_parts):
        raise RuntimeError("Whole tray must be a single control without independent brick keys")
    if not tray.animation_data or not tray.animation_data.action:
        raise RuntimeError("Tray rocking action not saved")

    scene.render.engine="CYCLES";scene.cycles.device="CPU";scene.cycles.samples=a.samples
    scene.render.film_transparent=True
    scene.render.resolution_x=scene.render.resolution_y=256
    scene.render.resolution_percentage=100
    scene.render.image_settings.file_format="PNG"
    scene.render.image_settings.color_mode="RGBA"
    scene.render.image_settings.color_depth="8"
    scene.render.fps=8
    root.rotation_euler.z=0;scene.frame_set(0)
    scene.render.filepath="//renders/"
    master=out/"pit-kiln-v4b-whole-tray.blend"
    bpy.ops.wm.save_as_mainfile(filepath=str(master),check_existing=False)
    entries=[]
    for state,frames in (("idle",[0]),("burning",FRAMES)):
        for d,angle in enumerate((0,90,180,270)):
            root.rotation_euler.z=math.radians(angle)
            for j,t in enumerate(frames):
                scene.frame_set(t);bpy.context.view_layer.update()
                target=out/(f"idle-d{d:02d}.png" if state=="idle" else f"burning-d{d:02d}-f{j:03d}.png")
                scene.render.filepath=str(target)
                print("PIT_KILN_V4B_RENDER",state,angle,t,flush=True)
                bpy.ops.render.render(write_still=True)
                entries.append({"state":state,"direction":d,"index":j,"frame":t,"path":target.name,"sha256":sha(target)})
    root.rotation_euler.z=0;scene.frame_set(0)
    receipt={"schema":4,"revision":"v4b-whole-tray-rocks-with-four-wet-bricks",
        "original_campfire_flames":len(flames),"original_campfire_actions":original_actions,
        "original_animated_campfire_light":source_light.name,
        "v3b_existing_flame_helpers":len(helpers),
        "new_crackle_controls":len(crackles),"staged_bricks_wobbling":len(bricks),
        "complete_tray_control":tray.name,"tray_parts":len(tray_parts),
        "tray_motion_screen_pixels":geometry_motion,
        "bank_bricks_stationary":len(bank),"staging_board_stationary":False,"crackle_ember_count":len(embers),
        "camera_elevation_deg":45,"directions":[0,90,180,270],
        "fps":8,"source_frames":len(entries),"master_sha256":sha(master),
        "brick_motion_samples":geometry_motion,"art_approved":False,
        "factorio_prototype_changed":False,"captures":entries}
    (out/"build-report.json").write_text(json.dumps(receipt,indent=2)+"\n")
    print("PIT_KILN_V4B_68_RENDER_COMPLETE",flush=True)
if __name__=="__main__":main()
