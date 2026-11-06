#!/usr/bin/env python3
"""Verify that V9 saved Blender objects and char shader drivers really exist."""
import json,sys
from pathlib import Path
import bpy
argv=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
out=Path(argv[0]);s=bpy.context.scene
ctrl=bpy.data.objects["CAMPFIRE CONTROLS | collection 03 toggle fire"]
assert float(ctrl["Fire Active"])==1
assert s.frame_start==0 and s.frame_end==96
wood=[o for o in bpy.data.collections["02 | Firewood"].objects if o.type=="MESH"]
flames=[o for o in s.objects if o.name.startswith("flame_tongue")]
light=bpy.data.objects["04 | animated fire light"]
checked=set()
for o in wood:
 for m in o.data.materials:
    if m.name in checked:continue
    checked.add(m.name)
    assert any(n.label=="CF9 wood char / original wood switch" for n in m.node_tree.nodes)
    assert any(n.bl_idname=="ShaderNodeNormalMap" for n in m.node_tree.nodes)
    assert m.node_tree.animation_data and m.node_tree.animation_data.action,m.name
    assert any(n.label=="FIRE ACTIVE control, 0 cold / 1 burning" for n in m.node_tree.nodes)
assert len(wood)>=25 and len(checked)>=42 and len(flames)==6
for obj in flames+[light]:
    assert obj.animation_data and obj.animation_data.action
    assert any("hide_render" in f.data_path for f in obj.animation_data.action.fcurves),obj.name
s.frame_set(0)
val=next(n for n in wood[0].data.materials[0].node_tree.nodes if n.label=="FIRE ACTIVE control, 0 cold / 1 burning")
assert abs(val.outputs[0].default_value)<.01,"Cold wood charcoal still enabled"
s.frame_set(13)
assert val.outputs[0].default_value>.99,"Burning wood not charred"
s.frame_set(0)
assert all(o.hide_render for o in flames+[light]),"Cold state still has fire geometry"
s.frame_set(13)
assert all(not o.hide_render for o in flames+[light]),"Burning state hides fire"
assert len([o for o in s.objects if o.name.startswith("stone_")])==15
assert sum(len(o.data.polygons) for o in s.objects if o.type=="MESH" and o.name!="Ground | shadow catcher")==12152
assert s.render.engine=="CYCLES"
result={"verified":True,"native_blend":bpy.data.filepath,"wood_objects":len(wood),"char_materials":len(checked),
        "stone_objects":15,"animated_flames":len(flames),"one_timeline_state":True,
        "idle_uncharred":True,"burning_charred_core":True,"preserves_normal_maps":True}
out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(result,indent=2)+"\n")
print("V9_VERIFIED",json.dumps(result))
