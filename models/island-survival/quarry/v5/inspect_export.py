"""Reopen source and independently reimport and render the actual animated GLB."""
import bpy, hashlib, json, math, struct, sys
from pathlib import Path
import numpy as np
from mathutils import Vector
REPO=Path(__file__).resolve().parents[4]
OUT=REPO/'models/island-survival/quarry/candidates/v5-rooted04'
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
source=OUT/'quarry-v5.blend';runtime=OUT/'quarry-v5.glb'
bpy.ops.wm.open_mainfile(filepath=str(source));scene=bpy.context.scene
profile=json.loads((OUT/'capture-profile.json').read_text());assert_clean(scene,profile,bpy)
print('SOURCE_TIMING',scene.frame_start,scene.frame_end,scene.render.fps,scene.render.fps_base,flush=True)
source_fps=scene.render.fps/scene.render.fps_base
poses={}
for f in (1,25,49,97,145,193):
    scene.frame_set(f);poses[f]=snapshot()
packed=[dict(name=i.name,packed=bool(i.packed_file),size=list(i.size)) for i in bpy.data.images if i.users and i.type=='IMAGE']
# Measure actual attachment endpoints throughout the full working cycle.
obj=bpy.data.objects;root=obj['EXPORT | Quarry all authored parts'];bucket=obj['QUARRY | upright lifting bucket'];cable=obj['QUARRY | taut lifting cable'];rod=obj['QUARRY | rigid engine connecting rod'];pin=obj['QUARRY | retained engine crank pin'];slider=obj['QUARRY | crosshead slider'];piston=obj['QUARRY | guided working piston'];drum=obj['QUARRY | winding drum']
mechanism=dict(rod_endpoint_error=0.,piston_endpoint_error=0.,cable_endpoint_error=0.,bucket_upright_error=0.,paid_rope_error=0.)
for frame in range(1,194):
 scene.frame_set(frame);bpy.context.view_layer.update()
 ends=[rod.matrix_world@Vector((0,0,z)) for z in (-.13,.13)];targets=[pin.matrix_world.translation,slider.matrix_world.translation]
 mechanism['rod_endpoint_error']=max(mechanism['rod_endpoint_error'],min(max((ends[i]-targets[i]).length for i in (0,1)),max((ends[i]-targets[1-i]).length for i in (0,1))))
 mechanism['piston_endpoint_error']=max(mechanism['piston_endpoint_error'],((piston.matrix_world@Vector((0,0,.16)))-slider.matrix_world.translation).length)
 ends=[cable.matrix_world@Vector((0,0,z)) for z in (-.5,.5)];targets=[bucket.matrix_world@Vector((0,0,.715)),root.matrix_world@Vector((0,.402,2.1))]
 mechanism['cable_endpoint_error']=max(mechanism['cable_endpoint_error'],max((ends[i]-targets[i]).length for i in (0,1)))
 mechanism['bucket_upright_error']=max(mechanism['bucket_upright_error'],((bucket.matrix_world.to_3x3()@Vector((0,0,1))).normalized()-Vector((0,0,1))).length)
 mechanism['paid_rope_error']=max(mechanism['paid_rope_error'],abs(drum.rotation_euler.x*.188+bucket.location.z-.43))
(OUT/'mechanical-inspection.json').write_text(json.dumps(dict(source_sha256=sha(source),frames=193,errors=mechanism,passed=max(mechanism.values())<.001),indent=2)+'\n')
if max(mechanism.values())>=.001:raise RuntimeError('Attachment or rope relationship failed '+str(mechanism))
blob=runtime.read_bytes();length,kind=struct.unpack_from('<II',blob,12);assert kind==0x4e4f534a
gltf=json.loads(blob[20:20+length])
first=min(gltf['accessors'][s['input']]['min'][0] for a in gltf['animations'] for s in a['samplers'])
bpy.ops.wm.read_factory_settings(use_empty=True);bpy.context.scene.render.fps=24
bpy.ops.import_scene.gltf(filepath=str(runtime));scene=bpy.context.scene
print('IMPORT_TIMING',first,scene.render.fps,scene.render.fps_base,flush=True)
errors={};runtime_poses={}
for f in poses:
    t=(first+(f-1)/source_fps)*scene.render.fps/scene.render.fps_base;scene.frame_set(math.floor(t),subframe=t-math.floor(t));data=snapshot();runtime_poses[f]=data
    errors[f]=max(abs(poses[f][n][key][axis]-data[n][key][axis]) for n in poses[f] for key in ('min','max') for axis in range(3))
    if f==49:print('WORST',sorted([(max(abs(poses[f][n][k][a]-data[n][k][a]) for k in ('min','max') for a in range(3)),n) for n in poses[f]],reverse=True)[:4],flush=True)
summ=summarize(runtime_poses[1]);src=summarize(poses[1])
seam=max(abs(poses[1][n][k][a]-poses[193][n][k][a]) for n in poses[1] for k in ('min','max') for a in range(3))
moving=[n for n in poses[1] if max(abs(poses[1][n][k][a]-poses[49][n][k][a]) for k in ('min','max') for a in range(3))>.001]
socket_motion=max(abs(poses[1][n][k][a]-poses[f][n][k][a]) for n in poses[1] if 'REUSED quarry_base_stone' in n or 'windlass head tie' in n for f in poses for k in ('min','max') for a in range(3))
passed=not any((summ['missing_uv'],summ['nonfinite'],summ['degenerates'])) and max(errors.values())<.001 and seam<.001 and socket_motion<1e-6 and len(moving)>5 and all(i['packed'] for i in packed) and all('uri' not in i for i in gltf.get('images',[]))
receipt=dict(technical_checks_passed=passed,source_sha256=sha(source),glb_sha256=sha(runtime),source=src,runtime=summ,pose_bounds_errors=errors,cycle_seam_error=seam,fixed_socket_motion=socket_motion,moving_parts=moving,packed_images=packed,embedded_export_images=len(gltf.get('images',[])),animation_count=len(gltf.get('animations',[])),owner_visual_approved=False,native_game_verified=False)
(OUT/'runtime-inspection.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('QUARRY_RUNTIME',json.dumps({k:receipt[k] for k in ('technical_checks_passed','runtime','pose_bounds_errors','cycle_seam_error','fixed_socket_motion','embedded_export_images')}),flush=True)
if not passed:raise RuntimeError('Actual export failed inspection')
install_canonical_camera(scene,profile,bpy);scene.render.engine='CYCLES';scene.cycles.samples=32;scene.render.film_transparent=True
scene.world=bpy.data.worlds.new('Neutral export inspection');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.35,.35,.35,1)
for loc,power,size in [((3,-4,6),650,5),((-3,2,4),400,4)]:
    l=bpy.data.lights.new('Inspection area','AREA');l.energy=power;l.shape='DISK';l.size=size;o=bpy.data.objects.new('Inspection area',l);scene.collection.objects.link(o);o.location=loc;o.rotation_euler=(Vector((0,0,.5))-o.location).to_track_quat('-Z','Y').to_euler()
scene.render.resolution_x=scene.render.resolution_y=512
scene.frame_set(int(first*24+24))
scene.render.filepath=str(OUT/'actual-glb-front.png');bpy.ops.render.render(write_still=True)
root=bpy.data.objects['EXPORT | Quarry all authored parts']
review_parent=bpy.data.objects.new('Temporary export review rotation',None);scene.collection.objects.link(review_parent);root.parent=review_parent
review_parent.rotation_euler.z=math.pi
scene.render.filepath=str(OUT/'actual-glb-rear.png');bpy.ops.render.render(write_still=True)
review_parent.rotation_euler.z=0
clay=bpy.data.materials.new('Inspection neutral clay');clay.diffuse_color=(.18,.18,.18,1);clay.use_nodes=True;clay.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=(.18,.18,.18,1)
scene.view_layers[0].material_override=clay
scene.render.filepath=str(OUT/'actual-glb-clay.png');bpy.ops.render.render(write_still=True)
scene.view_layers[0].material_override=None
from blender_camera_guard import temporary_inspection_camera
scene.render.resolution_x=scene.render.resolution_y=512
with temporary_inspection_camera(scene,bpy,'actual exported drive attachments') as camera:
 camera.data.type='ORTHO';camera.data.ortho_scale=1.4;camera.location=(3,-3,2.2);camera.rotation_euler=(Vector((.92,-.42,.88))-camera.location).to_track_quat('-Z','Y').to_euler();scene.camera=camera
 scene.render.filepath=str(OUT/'actual-glb-drive-close.png');bpy.ops.render.render(write_still=True)
