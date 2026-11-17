"""Reopen source and independently reimport and render the actual animated GLB."""
import bpy, hashlib, json, math, struct, sys
from pathlib import Path
import numpy as np
from mathutils import Vector
REPO=Path(__file__).resolve().parents[4]
OUT=REPO/'models/island-survival/calcifier/candidates/v2-sockets08'
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
source=OUT/'calcifier-v2.blend';runtime=OUT/'calcifier-v2.glb'
bpy.ops.wm.open_mainfile(filepath=str(source));scene=bpy.context.scene
profile=json.loads((OUT/'capture-profile.json').read_text());assert_clean(scene,profile,bpy)
print('SOURCE_TIMING',scene.frame_start,scene.frame_end,scene.render.fps,scene.render.fps_base,flush=True)
source_fps=scene.render.fps/scene.render.fps_base
poses={}
for f in (1,25,49,97,145,193):
    scene.frame_set(f);poses[f]=snapshot()
packed=[dict(name=i.name,packed=bool(i.packed_file),size=list(i.size)) for i in bpy.data.images if i.users and i.type=='IMAGE']
# Check the engine attachments, 18:18 right-angle drive and 31:62 mixer ratio.
obj=bpy.data.objects;rod=obj['CALCIFIER | engine rigid connecting arm'];pin=obj['CALCIFIER | retained engine crank pin'];slider=obj['CALCIFIER | guided engine crosshead'];piston=obj['CALCIFIER | engine rigid piston'];my=obj['CALCIFIER | driving 18 tooth miter'];mz=obj['CALCIFIER | driven 18 tooth miter'];pinion=obj['CALCIFIER | vertical 31 tooth pinion'];mix=obj['CALCIFIER | mineral paddle gear and shaft']
from mathutils.bvhtree import BVHTree
def world_bvh(o):
 graph=bpy.context.evaluated_depsgraph_get();ev=o.evaluated_get(graph);data=ev.to_mesh();data.calc_loop_triangles();tree=BVHTree.FromPolygons([ev.matrix_world@v.co for v in data.vertices],[tuple(t.vertices) for t in data.loop_triangles],all_triangles=True);ev.to_mesh_clear();return tree
guide=next(o for o in obj if o.name.startswith('CALCIFIER | engine guide crossmember') and abs(o.location.z-.98)<.0001);static_guide=world_bvh(guide)
mechanism=dict(offset_arm_endpoint_error=0.,forming_crosshead_offset_error=0.,die_pad_gap=0.,ram_shaft_die_clearance_error=0.,rod_guide_triangle_intersections=0,mixer_thrust_seat_gap=0.,pinion_thrust_seat_gap=0.,rod_endpoint_error=0.,piston_endpoint_error=0.,miter_ratio_error=0.,mixer_ratio_error=0.,crosshead_off_axis=0.)
for frame in range(1,194):
 scene.frame_set(frame);bpy.context.view_layer.update()
 mechanism['rod_guide_triangle_intersections']=max(mechanism['rod_guide_triangle_intersections'],len(static_guide.overlap(world_bvh(rod))))
 for key,collar,bush in [('mixer_thrust_seat_gap','CALCIFIER | mixer load carrying thrust collar','CALCIFIER | upper vertical shaft bronze bush'),('pinion_thrust_seat_gap','CALCIFIER | pinion lower thrust collar','CALCIFIER | lower pinion shaft journal')]:
  c=obj[collar];b=obj[bush];low=min((c.matrix_world@v.co).z for v in c.data.vertices);high=max((b.matrix_world@v.co).z for v in b.data.vertices);mechanism[key]=max(mechanism[key],abs(low-high))

 ends=[rod.matrix_world@Vector((0,0,z)) for z in (-.145,.145)];targets=[pin.matrix_world.translation,slider.matrix_world.translation]
 mechanism['rod_endpoint_error']=max(mechanism['rod_endpoint_error'],min(max((ends[i]-targets[i]).length for i in (0,1)),max((ends[i]-targets[1-i]).length for i in (0,1))))
 mechanism['piston_endpoint_error']=max(mechanism['piston_endpoint_error'],((piston.matrix_world@Vector((0,0,.175)))-slider.matrix_world.translation).length)
 mechanism['miter_ratio_error']=max(mechanism['miter_ratio_error'],abs(my.rotation_euler.y+mz.rotation_euler.z-math.pi/18),abs(mz.rotation_euler.z-pinion.rotation_euler.z))
 mechanism['mixer_ratio_error']=max(mechanism['mixer_ratio_error'],abs(mix.rotation_euler.z+pinion.rotation_euler.z/2))
 mechanism['crosshead_off_axis']=max(mechanism['crosshead_off_axis'],abs(slider.location.x-1),abs(slider.location.y+.635))
 arm=obj['CALCIFIER V2 | rigid offset separator arm'];sieve=obj['CALCIFIER V2 | guided scum sediment sieve carriage'];upperpin=obj['CALCIFIER V2 | sieve retained eccentric']
 # Recover actual rigid arm endpoints from frame-one geometry construction.
 LR=math.sqrt(1.29**2+.51**2+1.18**2)
 for local_z,target in [(-LR/2,sieve.matrix_world@Vector((0,-.27,-.06))),(LR/2,upperpin.matrix_world.translation)]:
  mechanism['offset_arm_endpoint_error']=max(mechanism['offset_arm_endpoint_error'],((arm.matrix_world@Vector((0,0,local_z)))-target).length)
 forming=obj['CALCIFIER V2 | forming ram coupled to engine']
 mechanism['forming_crosshead_offset_error']=max(mechanism['forming_crosshead_offset_error'],(forming.matrix_world.translation-slider.matrix_world@Vector((-.71,-.405,0))).length)
 pad=obj['CALCIFIER V2 | load bearing die pad'];die=obj['CALCIFIER V2 | two cavity bioceramic forming die']
 mechanism['die_pad_gap']=max(mechanism['die_pad_gap'],abs(max((pad.matrix_world@v.co).z for v in pad.data.vertices)-min((die.matrix_world@v.co).z for v in die.data.vertices)))
 shaft=obj['CALCIFIER V2 | forming guided piston shaft'];low=min((shaft.matrix_world@v.co).z for v in shaft.data.vertices)
 mechanism['ram_shaft_die_clearance_error']=max(mechanism['ram_shaft_die_clearance_error'],max(0.,.56-low))

(OUT/'mechanical-inspection.json').write_text(json.dumps(dict(source_sha256=sha(source),frames=193,errors=mechanism,passed=max(mechanism.values())<.001),indent=2)+'\n')
if max(mechanism.values())>=.001:raise RuntimeError('Actual attachment check failed '+str(mechanism))
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
socket_motion=max(abs(poses[1][n][k][a]-poses[f][n][k][a]) for n in poses[1] if 'fixed player pipe flange' in n or 'REUSED calcifier_base' in n or 'full size' in n or 'full bore' in n for f in poses for k in ('min','max') for a in range(3))
passed=not any((summ['missing_uv'],summ['nonfinite'],summ['degenerates'])) and max(errors.values())<.001 and seam<.001 and socket_motion<1e-6 and len(moving)>5 and all(i['packed'] for i in packed) and all('uri' not in i for i in gltf.get('images',[]))
receipt=dict(technical_checks_passed=passed,source_sha256=sha(source),glb_sha256=sha(runtime),source=src,runtime=summ,pose_bounds_errors=errors,cycle_seam_error=seam,fixed_socket_motion=socket_motion,moving_parts=moving,packed_images=packed,embedded_export_images=len(gltf.get('images',[])),animation_count=len(gltf.get('animations',[])),owner_visual_approved=False,native_game_verified=False)
(OUT/'runtime-inspection.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('CALCIFIER_RUNTIME',json.dumps({k:receipt[k] for k in ('technical_checks_passed','runtime','pose_bounds_errors','cycle_seam_error','fixed_socket_motion','embedded_export_images')}),flush=True)
if not passed:raise RuntimeError('Actual export failed inspection')
install_canonical_camera(scene,profile,bpy);scene.render.engine='CYCLES';scene.cycles.samples=32;scene.render.film_transparent=True
scene.world=bpy.data.worlds.new('Neutral export inspection');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.35,.35,.35,1)
for loc,power,size in [((3,-4,6),650,5),((-3,2,4),400,4)]:
    l=bpy.data.lights.new('Inspection area','AREA');l.energy=power;l.shape='DISK';l.size=size;o=bpy.data.objects.new('Inspection area',l);scene.collection.objects.link(o);o.location=loc;o.rotation_euler=(Vector((0,0,.5))-o.location).to_track_quat('-Z','Y').to_euler()
scene.render.resolution_x=scene.render.resolution_y=512
scene.frame_set(int(first*24+24))
scene.render.filepath=str(OUT/'actual-glb-front.png');bpy.ops.render.render(write_still=True)
root=bpy.data.objects['EXPORT | Calcifier all authored parts']
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
 camera.data.type='ORTHO';camera.data.ortho_scale=2.8;camera.location=(3,-4,3);camera.rotation_euler=(Vector((.16,.02,1.35))-camera.location).to_track_quat('-Z','Y').to_euler();scene.camera=camera
 scene.render.filepath=str(OUT/'actual-glb-drive-close.png');bpy.ops.render.render(write_still=True)
