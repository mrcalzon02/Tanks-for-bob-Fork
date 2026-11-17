"""Reopen source and independently reimport and render the actual animated GLB."""
import bpy, hashlib, json, math, struct, sys
from pathlib import Path
import numpy as np
from mathutils import Vector
REPO=Path(__file__).resolve().parents[4]
OUT=Path(sys.argv[sys.argv.index('--')+1]).resolve()
sys.path.insert(0,str(REPO.parent/'model-production/tools/fmpl'))
from blender_camera_guard import assert_clean,install_canonical_camera
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def snapshot():
    graph=bpy.context.evaluated_depsgraph_get();result={}
    for o in bpy.context.scene.objects:
        if o.type!='MESH':continue
        ev=o.evaluated_get(graph);m=ev.to_mesh();m.calc_loop_triangles()
        pts=np.array([tuple(ev.matrix_world@v.co) for v in m.vertices])
        result[o.name]={'min':pts.min(axis=0).tolist(),'max':pts.max(axis=0).tolist(),'finite':bool(np.isfinite(pts).all()),'uv':bool(m.uv_layers),'triangles':len(m.loop_triangles),'degenerates':sum(t.area<1e-12 for t in m.loop_triangles)}
        ev.to_mesh_clear()
    return result
def summarize(d):
    return dict(mesh_count=len(d),triangles=sum(o['triangles'] for o in d.values()),min=np.min([o['min'] for o in d.values()],axis=0).tolist(),max=np.max([o['max'] for o in d.values()],axis=0).tolist(),missing_uv=[n for n,o in d.items() if not o['uv']],nonfinite=[n for n,o in d.items() if not o['finite']],degenerates={n:o['degenerates'] for n,o in d.items() if o['degenerates']})
source=OUT/'tank-assembler-v1.blend';runtime=OUT/'tank-assembler-v1.glb'
bpy.ops.wm.open_mainfile(filepath=str(source));scene=bpy.context.scene;profile=json.loads((OUT/'capture-profile.json').read_text());assert_clean(scene,profile,bpy);source_fps=scene.render.fps/scene.render.fps_base
poses={}
for f in (1,25,49,97,145,193):scene.frame_set(f);poses[f]=snapshot()
packed=[dict(name=i.name,packed=bool(i.packed_file),size=list(i.size)) for i in bpy.data.images if i.users and i.type=='IMAGE']
def mechanics(frame_set):
 from mathutils import Quaternion
 obj=bpy.data.objects;load=obj['VEHICLE | upright suspended engine module'];drum=obj['VEHICLE | reversing supported hoist drum'];motor=obj['VEHICLE | reversing hoist electric armature'];tool=obj['VEHICLE | guided joining head'];bus1=obj['VEHICLE | first rigid insulated electrical arm'];bus2=obj['VEHICLE | second rigid insulated electrical arm'];ropes=[o for o in obj if o.name.startswith('VEHICLE | variable hanging rope')];assert len(ropes)==2
 errors=dict(upright_load=0.,rope_attachment=0.,rigid_arm_length=0.,electrical_joint_attachment=0.,winch_winding_ratio=0.,tool_guide_alignment=0.)
 for f in (1+i/2 for i in range(385)):
  frame_set(f);pos=load.matrix_world.translation;angle=(pos.z-1.32)/.081;expected=Quaternion((1,0,0),angle)@Vector((0,0,1))
  errors['upright_load']=max(errors['upright_load'],((load.matrix_world.to_quaternion()@Vector((0,0,1)))-Vector((0,0,1))).length)
  for o in (drum,motor):errors['winch_winding_ratio']=max(errors['winch_winding_ratio'],((o.matrix_world.to_quaternion()@Vector((0,0,1)))-expected).length)
  for rope in ropes:
   lower=rope.matrix_world@Vector((0,0,-.5));upper=rope.matrix_world@Vector((0,0,.5));errors['rope_attachment']=max(errors['rope_attachment'],abs(lower.z-(pos.z+.66)),abs(upper.z-2.779),abs(lower.y-.42),abs(upper.y-.42))
  points=[(o.matrix_world@Vector((0,offset,-.185)),o.matrix_world@Vector((0,offset,.185))) for o,offset in ((bus1,0),(bus2,.04))]
  errors['rigid_arm_length']=max(errors['rigid_arm_length'],*[abs((hi-lo).length-.37) for lo,hi in points])
  errors['electrical_joint_attachment']=max(errors['electrical_joint_attachment'],(points[0][0]-Vector((1.13,-.12,1.57))).length,(points[0][1]+Vector((0,0,.04))-points[1][0]).length,(points[1][1]-Vector((.65,tool.matrix_world.translation.y,1.61))).length)
  errors['tool_guide_alignment']=max(errors['tool_guide_alignment'],abs(tool.matrix_world.translation.x-.65),abs(tool.matrix_world.translation.z-1.37))
 return errors
set_source=lambda f:(scene.frame_set(math.floor(f),subframe=f-math.floor(f)),bpy.context.view_layer.update())
source_mechanics=mechanics(set_source)
assert max(source_mechanics.values())<.0001,source_mechanics
blob=runtime.read_bytes();length,kind=struct.unpack_from('<II',blob,12);gltf=json.loads(blob[20:20+length]);first=min(gltf['accessors'][x['input']]['min'][0] for a in gltf['animations'] for x in a['samplers']);assert len(gltf['animations'])==1
for m in gltf['materials']:
 pbr=m.get('pbrMetallicRoughness',{})
 if 'baseColorTexture' in pbr:assert 'normalTexture' in m and 'metallicRoughnessTexture' in pbr,m['name']
bpy.ops.wm.read_factory_settings(use_empty=True);bpy.context.scene.render.fps=24;bpy.ops.import_scene.gltf(filepath=str(runtime));scene=bpy.context.scene
assert not [o for o in scene.objects if o.type in ('CAMERA','LIGHT')]
def set_runtime(f):
 t=(first+(f-1)/source_fps)*24;scene.frame_set(math.floor(t),subframe=t-math.floor(t));bpy.context.view_layer.update()
runtime_mechanics=mechanics(set_runtime);assert max(runtime_mechanics.values())<1e-4,runtime_mechanics
errors={};runtime_poses={}
for f in poses:
 set_runtime(f);data=snapshot();runtime_poses[f]=data;assert set(data)==set(poses[f]);errors[f]=max(abs(poses[f][n][key][axis]-data[n][key][axis]) for n in data for key in ('min','max') for axis in range(3))
src=summarize(poses[1]);summ=summarize(runtime_poses[1]);seam=max(abs(poses[1][n][k][axis]-poses[193][n][k][axis]) for n in poses[1] for k in ('min','max') for axis in range(3));passed=not any((src['missing_uv'],src['nonfinite'],src['degenerates'],summ['missing_uv'],summ['nonfinite'],summ['degenerates'])) and max(errors.values())<.001 and seam<1e-5 and all(i['packed'] for i in packed) and all('uri' not in i for i in gltf['images'])
receipt=dict(technical_checks_passed=passed,source_sha256=sha(source),glb_sha256=sha(runtime),source=src,runtime=summ,pose_bounds_errors=errors,cycle_seam_error=seam,source_mechanics=source_mechanics,runtime_mechanics=runtime_mechanics,mechanism_sampled_poses=385,mechanical_fit_policy='385 authored and interpolated samples: upright engine load, attached rope ends/fairleads, 0.37-tile rigid electrical arms in parallel hinge planes 0.04 tile apart, joined by axial pins, guided tool, winding drum/motor lift ratio. Full raw triangle sweep reviewed separately.',packed_images=packed,embedded_export_images=len(gltf['images']),animation_count=len(gltf['animations']),owner_visual_approved=False,native_game_verified=False)
(OUT/'runtime-inspection.json').write_text(json.dumps(receipt,indent=2)+'\n');print('TANK_RUNTIME_CHECK',json.dumps({k:v for k,v in receipt.items() if k!='packed_images'}),flush=True);assert passed
install_canonical_camera(scene,profile,bpy);scene.render.engine='CYCLES';scene.cycles.samples=32;scene.render.film_transparent=True;scene.render.image_settings.color_mode='RGBA';scene.render.resolution_x=scene.render.resolution_y=512;scene.view_settings.view_transform='AgX'
scene.world=bpy.data.worlds.new('Neutral exported ammunition inspection');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.35,.35,.35,1)
for loc,power in [((3,-4,6),500),((-3,2,4),300)]:
 l=bpy.data.lights.new('Inspection area','AREA');l.energy=power;l.size=4;o=bpy.data.objects.new(l.name,l);scene.collection.objects.link(o);o.location=loc;o.rotation_euler=(Vector((0,.3,.6))-o.location).to_track_quat('-Z','Y').to_euler()
root=bpy.data.objects['EXPORT | Tanks vehicle conversion gantry'];projection=bpy.data.objects.new('Temporary square-ground projection',None);scene.collection.objects.link(projection);projection.scale.y=math.sqrt(2);yawwrap=bpy.data.objects.new('Temporary physical review yaw',None);scene.collection.objects.link(yawwrap);yawwrap.parent=projection;root.parent=yawwrap;set_runtime(1)
for name,yaw in [('front',0),('rear',180),('side',90)]:
 yawwrap.rotation_euler.z=math.radians(yaw);scene.render.filepath=str(OUT/('actual-glb-'+name+'.png'));bpy.ops.render.render(write_still=True)
yawwrap.rotation_euler.z=90*math.pi/180;clay=bpy.data.materials.new('Neutral clay');clay.use_nodes=True;clay.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=(.28,.28,.28,1);scene.view_layers[0].material_override=clay;scene.render.filepath=str(OUT/'actual-glb-clay.png');bpy.ops.render.render(write_still=True);scene.view_layers[0].material_override=None;yawwrap.rotation_euler.z=0
from blender_camera_guard import temporary_inspection_camera
with temporary_inspection_camera(scene,bpy,'Actual upright engine lift and guided joining mechanism') as camera:
 target=Vector((0,.3*math.sqrt(2),1.70));camera.data.type='ORTHO';camera.data.ortho_scale=3.5;camera.location=target+Vector((-2,-2,1.3));camera.rotation_euler=(target-camera.location).to_track_quat('-Z','Y').to_euler();scene.camera=camera;scene.render.filepath=str(OUT/'actual-glb-mechanism-close.png');bpy.ops.render.render(write_still=True)
