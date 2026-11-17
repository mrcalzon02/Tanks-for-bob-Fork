"""Genuine 32-timestamp four-facing captures with complementary shoreline layers."""
import bpy,json,sys,math,hashlib,importlib.util
from pathlib import Path
P=Path(sys.argv[sys.argv.index('--')+1]).resolve();R=Path(__file__).resolve().parents[4];sys.path.insert(0,str(R.parent/'model-production/tools/fmpl'))
from blender_camera_guard import assert_clean
spec=importlib.util.spec_from_file_location('wheel_base',Path(__file__).resolve().parents[1]/'v1/build_stone_water_wheel.py');base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)
source=P/'stone-water-wheel-v3.blend';runtime=P/'stone-water-wheel-v3.glb';bpy.ops.wm.open_mainfile(filepath=str(source));s=bpy.context.scene;profile=json.loads((P/'capture-profile.json').read_text());assert_clean(s,profile,bpy)
profile['states']={'idle':[1],'working':list(range(1,193,6))};(P/'capture-profile.json').write_text(json.dumps(profile,indent=2)+'\n')
root=bpy.data.objects['WHEEL | placement root'];projection=bpy.data.objects.new('Temporary square-ground projection',None);s.collection.objects.link(projection);projection.scale.y=math.sqrt(2);root.parent=projection;s.render.resolution_x=s.render.resolution_y=256;s.cycles.samples=24;s.render.film_transparent=True;s.render.image_settings.color_mode='RGBA';controls=base.install_layer_clips();images=[]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for facing,yaw in [('north',0),('east',270),('south',180),('west',90)]:
 root.rotation_euler.z=math.radians(yaw)
 for state,frames in [('idle',[1]),('working',list(range(1,193,6)))]:
  for index,f in enumerate(frames):
   s.frame_set(f);bpy.context.view_layer.update()
   for layer in ('full','above-water','underwater'):
    for compare,gate in controls:gate.inputs[1].default_value=0 if layer=='full' else 1;compare.operation='LESS_THAN' if layer=='above-water' else 'GREATER_THAN'
    file=P/(f'{facing}-{state}-{index:02d}-{layer}.png');s.render.filepath=str(file);bpy.ops.render.render(write_still=True);images.append(dict(file=file.name,sha256=sha(file),facing=facing,state=state,index=index,source_frame=f,layer=layer))
(P/'capture-manifest.json').write_text(json.dumps(dict(source_sha256=sha(source),runtime_sha256=sha(runtime),genuine_combined_camera_captures=132,genuine_rendered_passes=len(images),working_frames_per_facing=32,fps=8,idle_policy='Genuine stopped frame-one pose. The native offshore pump freezes its current mechanical pose rather than exposing a separate idle-animation prototype field.',images=images),indent=2)+'\n');print('WHEEL_CAPTURE_COMPLETE',len(images),flush=True)
