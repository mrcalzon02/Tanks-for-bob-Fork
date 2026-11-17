"""Fit the balance pivot and hang its upright pans from real suspension eyes."""
import bpy,bmesh,math,json,sys,hashlib,tempfile
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[4];P=R/'models/island-survival/thinking-hut/candidates/v1-study03';O=P.parent/'v1-production04'
if O.exists():raise FileExistsError(O)
O.mkdir(parents=True);tempfile.tempdir=str(R/'build/quarry-export-temp');sys.path.insert(0,str(R/'models/island-survival/primitive-steam-powered-pump/v3'))
from mesh_util import cylinder,tube
import surfaces
sys.path.insert(0,str(R.parent/'model-production/tools/fmpl'))
from blender_camera_guard import assert_clean,temporary_inspection_camera
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
bpy.ops.wm.open_mainfile(filepath=str(P/'thinking-hut-v1.blend'));s=bpy.context.scene;s.frame_set(1);root=bpy.data.objects['EXPORT | Thinking Hut authored shelter'];col=bpy.data.collections.new('HUT | fitted balance bearings');s.collection.children.link(col)
bronze=next(m for m in bpy.data.materials if m.name.endswith(' | worn-bronze-fittings'));obj=bpy.data.objects;balance=obj['HUT | research balance beam'];bar=obj['HUT | balance crossbar']
cut=cylinder('Temporary balance pivot bore',(0,0,0),.020,.15,bronze,col,balance,'Y',48);bpy.context.view_layer.update();bpy.context.view_layer.objects.active=bar;mod=bar.modifiers.new('True rotating trunnion bore','BOOLEAN');mod.object=cut;mod.operation='DIFFERENCE';mod.solver='EXACT';bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cut,do_unlink=True)
boss=tube('HUT | balance bored trunnion boss',[(Vector((0,-.02,0)),Vector((0,1,0)),.035,.020),(Vector((0,.02,0)),Vector((0,1,0)),.035,.020)],bronze,col,balance,48);surfaces.physical_box_uv(boss)
for eye in [o for o in balance.children if 'retained suspension eye' in o.name]:eye.location.z=-.025
origin=Vector((.70,-1.08,1.28))
for frame in range(0,194):
 s.frame_set(frame);angle=balance.rotation_euler.y
 for sign in (-1,1):
  pan=obj['HUT | upright suspended weighing pan '+str(sign)];local=Vector((sign*.28,0,-.041));point=origin+balance.rotation_euler.to_matrix()@local;pan.location=point-Vector((0,0,.22));pan.keyframe_insert(data_path='location',frame=frame)
for o in (bar,boss):
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.triangulate(bm,faces=list(bm.faces));bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-7);bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=1e-7);bm.to_mesh(o.data);bm.free()
for sign in (-1,1):
 pan=obj['HUT | upright suspended weighing pan '+str(sign)]
 for layer in pan.animation_data.action.layers:
  for strip in layer.strips:
   for bag in strip.channelbags:
    for curve in bag.fcurves:
     for key in curve.keyframe_points:key.interpolation='LINEAR'
profile=json.loads((P/'capture-profile.json').read_text());s.frame_set(1);assert_clean(s,profile,bpy);bpy.ops.file.pack_all();native=O/'thinking-hut-v1.blend';bpy.ops.wm.save_as_mainfile(filepath=str(native),compress=True)
bpy.ops.wm.open_mainfile(filepath=str(native));s=bpy.context.scene;root=bpy.data.objects['EXPORT | Thinking Hut authored shelter'];bpy.ops.object.select_all(action='DESELECT')
for o in [root,*root.children_recursive]:o.select_set(True)
bpy.ops.export_scene.gltf(filepath=str(O/'thinking-hut-v1.glb'),export_format='GLB',use_selection=True,export_cameras=False,export_lights=False,export_animations=True,export_animation_mode='SCENE',export_anim_scene_split_object=False,export_frame_range=True,export_force_sampling=True,export_frame_step=1,export_apply=True,export_extras=True)
(O/'capture-profile.json').write_text(json.dumps(profile,indent=2)+'\n');receipt=json.loads((P/'construction-receipt.json').read_text());receipt.update(parent_source_sha256=sha(P/'thinking-hut-v1.blend'),source_sha256=sha(native),glb_sha256=sha(O/'thinking-hut-v1.glb'),repairs=['Inward knee braces attach to actual beams','Rafters follow thatch underside and rear bearing seats','Bored bronze balance trunnion on fixed pin','Pans stay upright and hang at the bottoms of the retained beam eyes']);(O/'construction-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
projection=bpy.data.objects.new('SPRITE ONLY | square ground projection',None);s.collection.objects.link(projection);projection.scale.y=math.sqrt(2);root.parent=projection;s.render.resolution_x=s.render.resolution_y=512;s.render.filepath=str(O/'front-review512.png');bpy.ops.render.render(write_still=True)
with temporary_inspection_camera(s,bpy,'Fitted research balance') as camera:
 camera.data.type='ORTHO';camera.data.ortho_scale=2.2;camera.location=(2,-4,2.1);camera.rotation_euler=(Vector((.32,-.90,.95))-camera.location).to_track_quat('-Z','Y').to_euler();s.camera=camera;s.render.filepath=str(O/'bench-close512.png');bpy.ops.render.render(write_still=True)
print('HUT_BALANCE_FITTED_SOURCE_SAVED',native,flush=True)
