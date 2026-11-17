import bpy,json,math
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
r=Path(__file__).resolve().parents[4];o=r/'models/island-survival/quarry/candidates/v5-rooted04'
bpy.ops.wm.open_mainfile(filepath=str(o/'quarry-v5.blend'));s=bpy.context.scene;root=bpy.data.objects['EXPORT | Quarry all authored parts']
p=bpy.data.objects.new('Temporary sprite projection',None);s.collection.objects.link(p);p.scale.y=math.sqrt(2);root.parent=p;bpy.context.view_layer.update()
ey=.59-math.sqrt((2*math.pi*.195)**2-.82**2);local=Vector((1.33,ey+.1,1.68));w=root.matrix_world@local
ndc=world_to_camera_view(s,s.camera,w);shift=-.63/math.sqrt(2)
record=dict(source_local=list(local),world=list(w),normalized_image=list(ndc),sprite_shift=[0,shift],emitter_position=[(ndc.x-.5)*5.6,(.5-ndc.y)*5.6+shift],derivation='Project the saved flue outlet through the actual canonical camera and sprite-only ground correction; apply native sprite scale and shift.')
(o/'smoke-anchor.json').write_text(json.dumps(record,indent=2)+'\n');print('SMOKE_ANCHOR',record)
