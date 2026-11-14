import bpy,json,sys,math,bmesh
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
out=Path(sys.argv[sys.argv.index('--')+1]);s=bpy.context.scene
root=bpy.data.objects['EXPORT | rotate beachpump not camera'];root.rotation_euler.z=0
ports=[o for o in bpy.data.objects if o.name.startswith('PORT |')]
buckets=[o for o in bpy.data.objects if o.name.startswith(('WHEEL | V7 solid bucket','WHEEL | V7 closed bucket'))]
rings=[o for o in bpy.data.objects if o.name.startswith('WHEEL | thinner rounded timber rim')]
gutter=bpy.data.objects['TROUGH | continuous open wooden gutter bottom']
fills=[o for o in bpy.data.objects if o.name.startswith('WATER | V8 carried')]
drains=[o for o in bpy.data.objects if o.name.startswith('WATER | V8 moving')]
assert len(buckets)==24 and len(fills)==len(drains)==8

def points():
 bpy.context.view_layer.update();return [tuple(o.matrix_world@v.co) for o in ports for v in o.data.vertices]
def tree(o):
 deps=bpy.context.evaluated_depsgraph_get();eo=o.evaluated_get(deps);m=eo.to_mesh();bm=bmesh.new();bm.from_mesh(m);bm.transform(eo.matrix_world)
 t=BVHTree.FromBMesh(bm);bm.free();eo.to_mesh_clear();return t
s.frame_set(1);original=points();intersections=[];pool_scales=[];drain_sources=[];widths=[]
for fr in range(1,98):
 s.frame_set(fr);assert points()==original
 if True:
  obstacles=[tree(o) for o in rings]+[tree(gutter)]
  for ob in buckets:
   t=tree(ob)
   if any(t.overlap(x) for x in obstacles):intersections.append((fr,ob.name))
 pool_scales.append(fills[0].scale.y)
 drain_sources.append(tuple(drains[0].data.splines[0].points[0].co))
 widths.append(drains[0].data.bevel_depth)
assert not intersections,intersections
assert max(pool_scales)-min(pool_scales)>.9
assert max(widths)>.004 and min(widths)<1e-6
assert max((Vector(x)-Vector(drain_sources[0])).length for x in drain_sources)>.5
assert max(abs(a-b) for a,b in zip(drain_sources[0],drain_sources[-1]))<1e-5
assert abs(pool_scales[0]-pool_scales[-1])<1e-5
for pool,drain in zip(fills,drains):
 values=[];radii=[];endpoints=[]
 for fr in range(1,98):
  s.frame_set(fr);values.append(pool.scale.y);radii.append(drain.data.bevel_depth)
  if fr in (1,97):endpoints.append(tuple(drain.data.splines[0].points[0].co))
 assert max(values)-min(values)>.9
 assert max(radii)>.004 and min(radii)<1e-6
 assert max(abs(a-b) for a,b in zip(*endpoints))<1e-5
# All new effects and recovered splash switch off in the native idle frame.
effects=fills+drains+[o for o in bpy.data.objects if o.name.startswith('WATER | V7')]
s.frame_set(0);assert all(o.hide_render for o in effects)
s.frame_set(1);assert all(not o.hide_render for o in effects)
assert abs(s.camera.rotation_euler.x-math.pi/4)<1e-6
report={'passed':True,'native_reopened':True,'port_phases_checked':97,'bucket_clearance_phases_checked':97,'bucket_ring_or_gutter_intersections':0,'port_vertex_drift':0,'eight_pool_fill_and_empty_cycles':True,'eight_drains_move_with_buckets':True,'drain_loop_error':max(abs(a-b) for a,b in zip(drain_sources[0],drain_sources[-1])),'idle_effects_hidden':True,'camera_elevation':45,'game_integrated':False,'human_visual_approved':False}
(out/'independent-reopen.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
