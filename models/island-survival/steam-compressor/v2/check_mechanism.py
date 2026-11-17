"""Measure actual saved crank/piston joints and fixed sockets through the loop."""
import bpy,json,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[4];O=R/'models/island-survival/steam-compressor/candidates/v2-barrel02'
bpy.ops.wm.open_mainfile(filepath=str(O/'steam-compressor-v2.blend'))
scene=bpy.context.scene
rod=bpy.data.objects['COMPRESSOR | rigid connecting rod']
slider=bpy.data.objects['COMPRESSOR | guided crosshead']
pin=bpy.data.objects['COMPRESSOR | retained crank pin']
piston=bpy.data.objects['COMPRESSOR | working piston']
sockets=[o for o in scene.objects if o.name.startswith('PORT |')]
initial={o.name:o.matrix_world.copy() for o in sockets}
result={'rod_length_error':0.,'crank_joint_error':0.,'slider_joint_error':0.,'piston_joint_error':0.,'socket_motion':0.,'frames':97,'fixed_port_meshes':len(sockets)}
for f in range(1,98):
 scene.frame_set(f);bpy.context.view_layer.update()
 top=rod.matrix_world@Vector((0,0,.18));bottom=rod.matrix_world@Vector((0,0,-.18))
 result['rod_length_error']=max(result['rod_length_error'],abs((top-bottom).length-.36))
 result['crank_joint_error']=max(result['crank_joint_error'],(top-pin.matrix_world.translation).length)
 result['slider_joint_error']=max(result['slider_joint_error'],(bottom-slider.matrix_world.translation).length)
 result['piston_joint_error']=max(result['piston_joint_error'],(piston.matrix_world@Vector((0,0,.2))-slider.matrix_world.translation).length)
 for o in sockets:result['socket_motion']=max(result['socket_motion'],max(abs(o.matrix_world[i][j]-initial[o.name][i][j]) for i in range(4) for j in range(4)))
result['passed']=result['fixed_port_meshes']==4 and max(result[k] for k in ('rod_length_error','crank_joint_error','slider_joint_error','piston_joint_error','socket_motion'))<1e-6
(O/'mechanism-inspection.json').write_text(json.dumps(result,indent=2)+'\n')
print('BARREL_MECHANISM',result,flush=True)
assert result['passed']
