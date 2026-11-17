"""Resume saved derivative, export through FMPL guard, then capture genuine frames."""
import bpy
import hashlib
import json
import math
from pathlib import Path
import sys
import tempfile

REPO=Path(__file__).resolve().parents[4]
OUT=REPO/'models/island-survival/thinking-hut/candidates/v1-lantern08'
SHARED=REPO.parent/'model-production'
temp=REPO/'build/compressor-export-temp';temp.mkdir(exist_ok=True)
tempfile.tempdir=str(temp)
sys.path.insert(0,str(SHARED/'tools/fmpl'))
from blender_camera_guard import install_canonical_camera,assert_clean
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
source=OUT/'thinking-hut-v1.blend'
bpy.ops.wm.open_mainfile(filepath=str(source));scene=bpy.context.scene
root=bpy.data.objects['EXPORT | Thinking Hut authored shelter']
profile=json.loads((OUT/'capture-profile.json').read_text())
assert_clean(scene,profile,bpy)
(OUT/'capture-profile.json').write_text(json.dumps(profile,indent=2)+'\n')
if '--capture' not in sys.argv:
    bpy.ops.object.select_all(action='DESELECT')
    for o in [root,*root.children_recursive]:o.select_set(True)
    bpy.ops.export_scene.gltf(filepath=str(OUT/'thinking-hut-v1.glb'),export_format='GLB',use_selection=True,export_cameras=False,export_lights=False,export_animations=True,export_animation_mode='SCENE',export_anim_scene_split_object=False,export_frame_range=True,export_force_sampling=True,export_frame_step=1,export_apply=True,export_extras=True)
projection=bpy.data.objects.new('SPRITE ONLY | square ground grid',None);scene.collection.objects.link(projection);projection.scale.y=math.sqrt(2);root.parent=projection
images=[]
for facing,yaw in [('north',0)]:
    root.rotation_euler.z=math.radians(yaw)
    states=profile['states'] if '--capture' in sys.argv else {'pilot':[25]}
    for state,frames in states.items():
        for index,frame in enumerate(frames):
            scene.frame_set(frame);assert_clean(scene,profile,bpy)
            path=OUT/(f'{facing}-{state}-{index:02d}.png')
            if not path.exists():
                scene.render.filepath=str(path);bpy.ops.render.render(write_still=True)
            images.append(dict(file=path.name,facing=facing,state=state,index=index,source_frame=frame,sha256=sha(path)))
if '--capture' in sys.argv:
    (OUT/'capture-manifest.json').write_text(json.dumps(dict(schema='tanks.thinking-hut.v1.capture',source_sha256=sha(source),runtime_sha256=sha(OUT/'thinking-hut-v1.glb'),genuine_blender_frames=len(images),frame_size=[256,256],fps=4,images=images,native_projection={'global_ground_y_scale':math.sqrt(2),'runtime_geometry_changed':False},owner_visual_approved=False,native_game_verified=False),indent=2)+'\n')
print('COMPRESSOR_EXPORTED_CAPTURED',len(images),flush=True)
