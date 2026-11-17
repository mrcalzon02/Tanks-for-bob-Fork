"""Reopen source and independently reimport and render the actual animated GLB."""
import bpy, hashlib, json, math, struct, sys
from pathlib import Path
import numpy as np
from mathutils import Vector
REPO=Path(__file__).resolve().parents[4]
OUT=REPO/'models/island-survival/steam-compressor/candidates/v2-barrel02'
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
source=OUT/'steam-compressor-v2.blend';runtime=OUT/'steam-compressor-v2.glb'
bpy.ops.wm.open_mainfile(filepath=str(source));scene=bpy.context.scene
profile=json.loads((OUT/'capture-profile.json').read_text());assert_clean(scene,profile,bpy)
print('SOURCE_TIMING',scene.frame_start,scene.frame_end,scene.render.fps,scene.render.fps_base,flush=True)
source_fps=scene.render.fps/scene.render.fps_base
poses={}
for f in (1,13,25,49,73,97):
    scene.frame_set(f);poses[f]=snapshot()
packed=[dict(name=i.name,packed=bool(i.packed_file),size=list(i.size)) for i in bpy.data.images if i.users and i.type=='IMAGE']
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
seam=max(abs(poses[1][n][k][a]-poses[97][n][k][a]) for n in poses[1] for k in ('min','max') for a in range(3))
moving=[n for n in poses[1] if max(abs(poses[1][n][k][a]-poses[49][n][k][a]) for k in ('min','max') for a in range(3))>.001]
socket_motion=max(abs(poses[1][n][k][a]-poses[f][n][k][a]) for n in poses[1] if 'fixed socket' in n or 'collar' in n for f in poses for k in ('min','max') for a in range(3))
passed=not any((summ['missing_uv'],summ['nonfinite'],summ['degenerates'])) and max(errors.values())<.001 and seam<.001 and socket_motion<1e-6 and len(moving)>5 and all(i['packed'] for i in packed) and all('uri' not in i for i in gltf.get('images',[]))
receipt=dict(technical_checks_passed=passed,source_sha256=sha(source),glb_sha256=sha(runtime),source=src,runtime=summ,pose_bounds_errors=errors,cycle_seam_error=seam,fixed_socket_motion=socket_motion,moving_parts=moving,packed_images=packed,embedded_export_images=len(gltf.get('images',[])),animation_count=len(gltf.get('animations',[])),owner_visual_approved=False,native_game_verified=False)
(OUT/'runtime-inspection.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('COMPRESSOR_RUNTIME',json.dumps({k:receipt[k] for k in ('technical_checks_passed','runtime','pose_bounds_errors','cycle_seam_error','fixed_socket_motion','embedded_export_images')}),flush=True)
if not passed:raise RuntimeError('Actual export failed inspection')
install_canonical_camera(scene,profile,bpy);scene.render.engine='CYCLES';scene.cycles.samples=32;scene.render.film_transparent=True
scene.world=bpy.data.worlds.new('Neutral export inspection');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.35,.35,.35,1)
for loc,power,size in [((3,-4,6),650,5),((-3,2,4),400,4)]:
    l=bpy.data.lights.new('Inspection area','AREA');l.energy=power;l.shape='DISK';l.size=size;o=bpy.data.objects.new('Inspection area',l);scene.collection.objects.link(o);o.location=loc;o.rotation_euler=(Vector((0,0,.5))-o.location).to_track_quat('-Z','Y').to_euler()
scene.frame_set(int(first*24+24))
scene.render.filepath=str(OUT/'actual-glb-front.png');bpy.ops.render.render(write_still=True)

