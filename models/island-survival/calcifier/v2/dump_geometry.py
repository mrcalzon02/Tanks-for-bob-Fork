import bpy,json,sys
from pathlib import Path
p=Path(sys.argv[sys.argv.index('--')+1]);bpy.ops.wm.open_mainfile(filepath=str(p/'calcifier-v2.blend'));bpy.context.scene.frame_set(25)
d={}
for o in bpy.context.scene.objects:
 if o.type!='MESH':continue
 pts=[o.matrix_world@v.co for v in o.data.vertices]
 d[o.name]={'location':list(o.location),'world':list(o.matrix_world.translation),'min':[min(v[a] for v in pts) for a in range(3)],'max':[max(v[a] for v in pts) for a in range(3)],'parent':o.parent.name if o.parent else None}
(p/'geometry-bounds.json').write_text(json.dumps(d,indent=2))
