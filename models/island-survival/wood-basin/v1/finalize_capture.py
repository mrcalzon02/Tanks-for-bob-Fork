"""Package inspected storage source and capture body plus genuine fill-preview states."""
import bpy,json,math,sys,hashlib,tempfile,shutil
import numpy as np
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];P=R/'models/island-survival/wood-basin/candidates/v1-pilot03';O=R/'models/island-survival/wood-basin/candidates/v1-production02'
if O.exists():raise FileExistsError(O)
O.mkdir(parents=True)
for p in P.glob('*.png'):
 if '-albedo' in p.name or '-normal' in p.name or '-roughness' in p.name:shutil.copy2(p,O/p.name)
sys.path.insert(0,str(R/'models/island-survival/primitive-steam-powered-pump/v3'));import surfaces
sys.path.insert(0,str(R.parent/'model-production/tools/fmpl'));from blender_camera_guard import assert_clean
tempfile.tempdir=str(R/'build/basin-export-temp')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
bpy.ops.wm.open_mainfile(filepath=str(P/'wood-basin-v1.blend'));scene=bpy.context.scene
root=bpy.data.objects['EXPORT | Wood Basin all authored parts'];preview=[o for o in root.children_recursive if o.get('native_fluid_preview')]
rng=np.random.default_rng(171127);f=surfaces.field(rng,(512,512),.03)
color=np.stack([.10+.006*f,.24+.012*f,.28+.015*f],axis=-1)
mat=surfaces.material('basin-preview-liquid',color,.22+.008*f,.5+.008*f,0,O)
for o in preview:surfaces.apply(o,mat);o.hide_render=False
from mesh_util import box
glass=bpy.data.materials.new('BASIN | sealed clear mineral sight panels');glass.use_nodes=True
shader=glass.node_tree.nodes.get('Principled BSDF');shader.inputs['Base Color'].default_value=(.66,.76,.74,1);shader.inputs['Roughness'].default_value=.18;shader.inputs['Transmission Weight'].default_value=.75;shader.inputs['Alpha'].default_value=.25
glass.surface_render_method='DITHERED'
for facing in ('north','east','south','west'):
 parent=bpy.data.objects['BASIN | '+facing+' wall frame']
 panel=box('BASIN | sealed sight panel '+facing,(0,-1.208,.84),(.38,.008,.78),glass,bpy.context.scene.collection,parent,bevel=0)
 surfaces.physical_box_uv(panel);panel['native_window_holdout_in_body_capture']=True

bpy.ops.file.pack_all();scene.frame_set(1)
native=O/'wood-basin-v1.blend';bpy.ops.wm.save_as_mainfile(filepath=str(native),compress=True)
bpy.ops.wm.open_mainfile(filepath=str(native));scene=bpy.context.scene;root=bpy.data.objects['EXPORT | Wood Basin all authored parts'];preview=[o for o in root.children_recursive if o.get('native_fluid_preview')]
bpy.ops.object.select_all(action='DESELECT')
for o in [root,*root.children_recursive]:o.select_set(True)
bpy.ops.export_scene.gltf(filepath=str(O/'wood-basin-v1.glb'),export_format='GLB',use_selection=True,export_cameras=False,export_lights=False,export_animations=True,export_animation_mode='SCENE',export_anim_scene_split_object=False,export_frame_range=True,export_force_sampling=True,export_frame_step=1,export_apply=True,export_extras=True)
profile=json.loads((P/'capture-profile.json').read_text());(O/'capture-profile.json').write_text(json.dumps(profile,indent=2)+'\n')
shutil.copy2(P/'reuse-receipt.json',O/'starter-reuse-receipt.json')
projection=bpy.data.objects.new('SPRITE ONLY | square ground grid',None);scene.collection.objects.link(projection);projection.scale.y=math.sqrt(2);root.parent=projection
holdout=bpy.data.materials.new('SPRITE ONLY | native fluid window cutout');holdout.use_nodes=True
nodes=holdout.node_tree.nodes;nodes.clear();out=nodes.new('ShaderNodeOutputMaterial');node=nodes.new('ShaderNodeHoldout');holdout.node_tree.links.new(node.outputs[0],out.inputs['Surface'])
glass=bpy.data.materials['BASIN | sealed clear mineral sight panels']
panels=[o for o in root.children_recursive if o.get('native_window_holdout_in_body_capture')]
images=[]
for facing,yaw in [('north',0),('east',270),('south',180),('west',90)]:
 root.rotation_euler.z=math.radians(yaw)
 for state,frames in [('idle',[0]),('fill-preview',list(range(1,92,6)))]:
  for o in preview:o.hide_render=(state=='idle')
  for o in panels:o.data.materials.clear();o.data.materials.append(holdout if state=='idle' else glass)
  for i,frame in enumerate(frames):
   scene.frame_set(frame);assert_clean(scene,profile,bpy);path=O/(facing+'-'+state+'-'+str(i).zfill(2)+'.png')
   scene.render.filepath=str(path);bpy.ops.render.render(write_still=True);images.append(dict(file=path.name,facing=facing,state=state,index=i,source_frame=frame,sha256=sha(path)))
def pixels(path):
 im=bpy.data.images.load(str(path),check_existing=False);a=np.array(im.pixels[:]).reshape(256,256,4);bpy.data.images.remove(im);return a
body=np.zeros((256,1024,4),dtype=np.float32)
for i,d in enumerate(('north','east','south','west')):body[:,i*256:(i+1)*256]=pixels(O/(d+'-idle-00.png'))
im=bpy.data.images.new('wood-basin-body',width=1024,height=256,alpha=True);im.pixels.foreach_set(body.ravel());im.file_format='PNG';im.filepath_raw=str(O/'body-256.png');im.save()
im=bpy.data.images.load(str(O/'north-idle-00.png'));im.scale(64,64);im.file_format='PNG';im.filepath_raw=str(O/'icon-64.png');im.save()
# Native tint/level mask is deliberately neutral; no liquid is baked into body.
array=np.ones((18,12,4),dtype=np.float32);array[:,:,:3]=.55
im=bpy.data.images.new('Basin neutral native liquid mask',width=12,height=18,alpha=True);im.pixels.foreach_set(array.ravel());im.file_format='PNG';im.filepath_raw=str(O/'fluid-background.png');im.save()
array[:,:,:3]=(.025,.03,.025)
im=bpy.data.images.new('Basin dark empty native window',width=12,height=18,alpha=True);im.pixels.foreach_set(array.ravel());im.file_format='PNG';im.filepath_raw=str(O/'window-background.png');im.save()
receipt=dict(schema='tanks.wood-basin.v1.capture',source_sha256=sha(native),runtime_sha256=sha(O/'wood-basin-v1.glb'),genuine_blender_frames=len(images),images=images,frame_size=[256,256],source_preview_fps=8,native_body_frames_per_facing=1,native_fluid_animation='Actual tank fluid ratio, scrolling flow_sprite and gas_flow; source fill-preview frames are evidence, not a forced working animation.',native_projection={'global_ground_y_scale':math.sqrt(2),'runtime_geometry_changed':False},files={n:sha(O/n) for n in ('body-256.png','icon-64.png','fluid-background.png','window-background.png')},owner_visual_approved=False,native_game_verified=False)
(O/'capture-manifest.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('BASIN_GENUINE_FRAMES',len(images),flush=True)
