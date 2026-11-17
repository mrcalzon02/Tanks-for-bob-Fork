import bpy
from pathlib import Path
p=Path(__file__).resolve().parents[4]/'models/island-survival/quarry/candidates/v5-rooted02/quarry-v5.blend';bpy.ops.wm.open_mainfile(filepath=str(p));o=bpy.data.objects['QUARRY | REUSED quarry_base_stone'];print('LAYERS',[(a.name,a.domain,a.data_type) for a in o.data.color_attributes]);print('ACTIVE',o.data.color_attributes.active_color_index,o.data.color_attributes.render_color_index)
for m in o.data.materials:
 print('MATERIAL',m.name)
 for node in m.node_tree.nodes:
  if node.type in ('VERTEX_COLOR','ATTRIBUTE'):print('ATTRNODE',node.name,getattr(node,'layer_name',None),getattr(node,'attribute_name',None),[(l.from_socket.name,l.to_socket.name) for l in m.node_tree.links if l.from_node==node])
