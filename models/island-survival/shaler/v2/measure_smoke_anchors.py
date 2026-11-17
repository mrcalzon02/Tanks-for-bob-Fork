import bpy,json,math
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
r=Path(__file__).resolve().parents[4];o=r/'models/island-survival/shaler/candidates/v2-mechanisms02'
bpy.ops.wm.open_mainfile(filepath=str(o/'shaler-v2.blend'));s=bpy.context.scene;root=bpy.data.objects['EXPORT | Shaler all authored parts']
p=bpy.data.objects.new('Temporary sprite projection',None);s.collection.objects.link(p);p.scale.y=math.sqrt(2);root.parent=p
record={}
for name,yaw in [('north',0),('east',270),('south',180),('west',90)]:
 root.rotation_euler.z=math.radians(yaw);bpy.context.view_layer.update();local=Vector((-1.02,.76,2.055));w=root.matrix_world@local
 ndc=world_to_camera_view(s,s.camera,w);shift=-1/math.sqrt(2)
 record[name]=dict(source_local=list(local),sprite_shift=[0,shift],emitter_position=[(ndc.x-.5)*5.6,(.5-ndc.y)*5.6+shift])
(o/'smoke-anchors.json').write_text(json.dumps(dict(derivation='Saved flue outlet projected through canonical camera and native square-ground correction for each true facing',facings=record),indent=2)+'\n');print('SHALER_SMOKE_ANCHORS',record)
