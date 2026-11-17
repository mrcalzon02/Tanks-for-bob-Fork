"""Genuine idle/working captures of the saved current source, not generated imagery."""
import bpy,json,sys,math,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[4];P=Path(sys.argv[sys.argv.index('--')+1]).resolve();sys.path.insert(0,str(R.parent/'model-production/tools/fmpl'))
from blender_camera_guard import assert_clean
source=P/'steam-condenser-v2.blend';runtime=P/'steam-condenser-v2.glb';bpy.ops.wm.open_mainfile(filepath=str(source));s=bpy.context.scene;profile=json.loads((P/'capture-profile.json').read_text());assert_clean(s,profile,bpy)
root=bpy.data.objects['EXPORT | Tanks wood steam treatment condenser'];projection=bpy.data.objects.new('Temporary square-ground projection',None);s.collection.objects.link(projection);projection.scale.y=math.sqrt(2);root.parent=projection;s.render.resolution_x=s.render.resolution_y=256;s.cycles.samples=32;s.render.film_transparent=True;s.render.image_settings.color_mode='RGBA';images=[];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for facing,yaw in [('north',0),('east',270),('south',180),('west',90)]:
 root.rotation_euler.z=math.radians(yaw)
 for state,frames in profile['states'].items():
  for index,f in enumerate(frames):
   s.frame_set(f);assert_clean(s,profile,bpy);file=P/f'{facing}-{state}-{index:02d}.png';s.render.filepath=str(file);bpy.ops.render.render(write_still=True);images.append(dict(file=file.name,sha256=sha(file),facing=facing,state=state,index=index,source_frame=f))
(P/'capture-manifest.json').write_text(json.dumps(dict(source_sha256=sha(source),runtime_sha256=sha(runtime),genuine_blender_frames=len(images),working_frames_per_facing=32,fps=8,frame_size=[256,256],images=images,native_projection={'global_ground_y_scale':math.sqrt(2),'runtime_geometry_changed':False},owner_visual_approved=False),indent=2)+'\n');print('CONDENSER_CAPTURE_COMPLETE',len(images),flush=True)
