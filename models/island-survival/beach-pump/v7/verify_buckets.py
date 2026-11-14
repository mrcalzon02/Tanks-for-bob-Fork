"""Reopen and measure the actual bucket/wheel and bucket/gutter intersections."""
import bpy,bmesh,json,math,sys
from pathlib import Path
from mathutils.bvhtree import BVHTree

out=Path(sys.argv[sys.argv.index('--')+1])
s=bpy.context.scene
root=bpy.data.objects['EXPORT | rotate beachpump not camera'];root.rotation_euler.z=0
ports=[o for o in bpy.data.objects if o.name.startswith('PORT |')]
buckets=[o for o in bpy.data.objects if o.name.startswith(('WHEEL | V7 solid bucket','WHEEL | V7 closed bucket'))]
rings=[o for o in bpy.data.objects if o.name.startswith('WHEEL | thinner rounded timber rim')]
gutter=bpy.data.objects['TROUGH | continuous open wooden gutter bottom']
assert len(buckets)==24 and len(rings)==2 and len(ports)==2
def points():
    bpy.context.view_layer.update()
    return [tuple(o.matrix_world@v.co) for o in ports for v in o.data.vertices]
def tree(o):
    deps=bpy.context.evaluated_depsgraph_get();eo=o.evaluated_get(deps);m=eo.to_mesh()
    bm=bmesh.new();bm.from_mesh(m);bm.transform(eo.matrix_world)
    result=BVHTree.FromBMesh(bm);bm.free();eo.to_mesh_clear();return result
states=[];intersections=[]
s.frame_set(1);original=points()
for fr in range(1,98,6):
    s.frame_set(fr);assert points()==original
    rb=[tree(o) for o in rings];gt=tree(gutter)
    for o in buckets:
        bt=tree(o)
        if any(bt.overlap(t) for t in rb):intersections.append([fr,o.name,'ring'])
        if bt.overlap(gt):intersections.append([fr,o.name,'gutter'])
    states.append([bpy.data.objects[n].rotation_euler[i] for n,i in (
        ('MOTION | full bucket waterwheel shaft',0),('MOTION | keyed Archimedes screw rotation',2))])
assert not intersections,intersections
assert abs(states[4][0]-states[0][0])>1 and abs(states[4][1]-states[0][1])>1
assert max(abs(math.sin(a-b)) for a,b in zip(states[0],states[-1]))<1e-6
effects=[o for o in bpy.data.objects if o.name.startswith('WATER | V7')]
s.frame_set(0);assert all(o.hide_render for o in effects)
s.frame_set(1);assert all(not o.hide_render for o in effects)
result={'passed':True,'native_reopened':True,'phases_checked':17,
        'bucket_wall_meshes':24,'bucket_ring_surface_intersections':0,
        'bucket_gutter_surface_intersections':0,'stationary_port_vertex_drift':0,
        'wheel_and_screw_move':True,'wheel_and_screw_loop':True,
        'idle_splash_hidden':True,'game_integrated':False,'human_visual_approved':False}
(out/'independent-reopen.json').write_text(json.dumps(result,indent=2)+'\n')
print('V7_NATIVE_INTERSECTION_CHECK_PASS',json.dumps(result))
