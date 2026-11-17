"""Read-only inventory of the owner-designated shared compressor master."""
import bpy
import json
from pathlib import Path
from mathutils import Vector

out = Path(__file__).resolve().parents[4] / 'build/compressor-source-inventory.json'
objects = []
for o in bpy.context.scene.objects:
    bounds = [o.matrix_world @ Vector(c) for c in o.bound_box] if o.type == 'MESH' else []
    objects.append(dict(name=o.name, type=o.type, parent=o.parent.name if o.parent else None,
        animated=bool(o.animation_data), hidden=o.hide_render,
        bounds=[[min(v[i] for v in bounds) for i in range(3)], [max(v[i] for v in bounds) for i in range(3)]] if bounds else None,
        materials=[m.name for m in o.data.materials if m] if o.type=='MESH' else [], props=dict(o.items())))
out.write_text(json.dumps(dict(objects=objects, fps=bpy.context.scene.render.fps,
    end=bpy.context.scene.frame_end, images=[dict(name=i.name, packed=bool(i.packed_file), path=i.filepath) for i in bpy.data.images]),indent=2,default=str))
print('INVENTORY', out, len(objects))
