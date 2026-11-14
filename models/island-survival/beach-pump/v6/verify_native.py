"""Independent reopen checks and four review angles; these are not game atlases."""
import bpy, json, math, sys
from pathlib import Path
from mathutils import Vector

out=Path(sys.argv[sys.argv.index('--')+1]).resolve()
s=bpy.context.scene
root=bpy.data.objects['EXPORT | rotate beachpump not camera']
ports=[o for o in bpy.data.objects if o.name.startswith('PORT |')]
assert len(ports)==2
root.rotation_euler.z=0
def points():
    bpy.context.view_layer.update()
    return [tuple(o.matrix_world@v.co) for o in ports for v in o.data.vertices]
s.frame_set(1)
original=points()
drift=0
states=[]
for fr in range(1,98,6):
    s.frame_set(fr)
    drift=max(drift,max((Vector(a)-Vector(b)).length for a,b in zip(points(),original)))
    states.append([bpy.data.objects[n].rotation_euler[i] for n,i in (
        ('MOTION | full bucket waterwheel shaft',0),
        ('MOTION | keyed Archimedes screw rotation',2))])
assert drift<1e-8
assert abs(states[4][0]-states[0][0])>1
assert abs(states[4][1]-states[0][1])>1
assert all(abs(math.sin(a-b))<1e-6 for a,b in zip(states[0],states[-1]))
fluid=bpy.data.objects['WATER | continuous shallow volume with traveling free surface']
assert len(fluid.data.shape_keys.key_blocks)==4
collars=[bpy.data.objects[f'HOUSING | narrow brass retaining collar {i:02d}'] for i in range(2)]
assert abs(collars[1].location.z-collars[0].location.z)>.8
assert abs(s.camera.rotation_euler.x-math.pi/4)<1e-6
assert s.camera.data.type=='ORTHO'
assert s['game_integrated']==False and s['human_visual_approved']==False
spill=bpy.data.objects['WATER | uninterrupted trough-to-wheel falling sheet']
s.frame_set(0)
assert spill.hide_render
s.frame_set(25)
assert not spill.hide_render
s.render.resolution_x=s.render.resolution_y=512
s.cycles.samples=24
for i,yaw in enumerate((-45,45,135,225)):
    root.rotation_euler.z=math.radians(yaw)
    s.render.filepath=str(out/f'angle-{i}.png')
    bpy.ops.render.render(write_still=True)
result={'passed':True,'blender':bpy.app.version_string,'independent_reopen':True,
        'port_max_drift':drift,'wheel_and_screw_animate':True,'loop_matches':True,
        'idle_falling_water_hidden':True,'collars_separated':True,
        'review_camera_elevation':45,'four_review_angles':[-45,45,135,225],
        'game_integrated':False,'human_visual_approved':False}
(out/'independent-reopen.json').write_text(json.dumps(result,indent=2)+'\n')
print('INDEPENDENT_REOPEN_PASS',json.dumps(result))
