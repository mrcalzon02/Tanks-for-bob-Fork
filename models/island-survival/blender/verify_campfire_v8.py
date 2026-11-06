#!/usr/bin/env python3
"""Fail pipeline unless actual saved native .blend contains the V8 shader and animation work."""
from pathlib import Path
import json,sys
import bpy
argv=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
output=Path(argv[0])
sc=bpy.context.scene
assert sc.render.engine=='CYCLES' and sc.camera and sc.frame_end==96
stones=[o for o in sc.objects if o.name.startswith('stone_') and o.type=='MESH']
logs=[o for o in sc.objects if o.type=='MESH' and any(c.name=='02 | Firewood' for c in o.users_collection)]
flames=[o for o in sc.objects if o.name.startswith('flame_tongue') and o.type=='MESH']
assert len(stones)==15 and len(logs)>=25 and len(flames)==6
stone_mats={o.data.materials[0].name for o in stones}
assert len(stone_mats)==15 and all(x.startswith('CF8 | stone') for x in stone_mats)
assert all(all(m.name.startswith('CF8 | ') for m in o.data.materials) for o in logs+flames)
assert sum(len(o.data.polygons) for o in sc.objects if o.type=='MESH' and o.name!='Ground | shadow catcher')==12152
assert len([im for im in bpy.data.images if im.packed_file])>=15
normal_count=0
for o in stones+logs:
    for m in o.data.materials:
        nodes=m.node_tree.nodes
        if any(n.bl_idname=='ShaderNodeNormalMap' for n in nodes):
            normal_count+=1
assert normal_count>=50,(normal_count)
for flame in flames:
    assert len(flame.data.shape_keys.key_blocks)>=3
    assert flame.data.shape_keys.animation_data and flame.data.shape_keys.animation_data.action
    mat=flame.data.materials[0]
    nodes=mat.node_tree.nodes
    assert any(n.bl_idname=='ShaderNodeValToRGB' and n.label=='Pale-hot base to fading red tip' for n in nodes)
    assert any(n.bl_idname=='ShaderNodeValToRGB' and n.label=='Smooth opacity lead-off' for n in nodes)
    assert mat.node_tree.animation_data and mat.node_tree.animation_data.action
sc.frame_set(1)
shapes_start=[round(o.data.shape_keys.key_blocks['Wind sway'].value,4) for o in flames]
sc.frame_set(37)
shapes_later=[round(o.data.shape_keys.key_blocks['Wind sway'].value,4) for o in flames]
assert shapes_start!=shapes_later
assert bpy.data.objects.get('04 | animated fire light').data.animation_data
obj={'blend':bpy.data.filepath,'stone_objects':len(stones),'unique_stone_materials':len(stone_mats),'wood_objects':len(logs),'flame_objects':len(flames),'normal_mapped_material_slots':normal_count,'shape_keys_per_flame':3,'timeline':[1,96],'verified':True}
output.parent.mkdir(parents=True,exist_ok=True)
output.write_text(json.dumps(obj,indent=2)+'\n')
print('CF8_VERIFIED '+json.dumps(obj),flush=True)
