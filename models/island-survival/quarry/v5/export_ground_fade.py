import bpy,json,hashlib,sys,tempfile,shutil
from pathlib import Path
r=Path(__file__).resolve().parents[4];p=r/'models/island-survival/quarry/candidates/v5-rooted02';o=p.parent/'v5-rooted04';o.mkdir();tempfile.tempdir=str(r/'build/quarry-export-temp')
bpy.ops.wm.open_mainfile(filepath=str(p/'quarry-v5.blend'));terrain=bpy.data.objects['QUARRY | REUSED quarry_base_stone']
for mat in terrain.data.materials:
 nodes=mat.node_tree.nodes;links=mat.node_tree.links;bsdf=nodes.get('Principled BSDF');vertex=next(n for n in nodes if n.type=='VERTEX_COLOR');old=bsdf.inputs['Base Color'].links[0].from_socket
 multiply=nodes.new('ShaderNodeMix');multiply.data_type='RGBA';multiply.blend_type='MULTIPLY';multiply.inputs[0].default_value=1
 links.new(old,multiply.inputs[6]);links.new(vertex.outputs['Color'],multiply.inputs[7]);links.new(multiply.outputs[2],bsdf.inputs['Base Color'])
 # White vertex RGB leaves source appearance unchanged; shared RGBA becomes GLTF COLOR_0.
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(o/'quarry-v5.blend'),compress=True);bpy.ops.wm.open_mainfile(filepath=str(o/'quarry-v5.blend'))
root=bpy.data.objects['EXPORT | Quarry all authored parts'];bpy.ops.object.select_all(action='DESELECT')
for item in [root,*root.children_recursive]:item.select_set(True)
bpy.ops.export_scene.gltf(filepath=str(o/'quarry-v5.glb'),export_format='GLB',use_selection=True,export_cameras=False,export_lights=False,export_animations=True,export_animation_mode='SCENE',export_anim_scene_split_object=False,export_frame_range=True,export_force_sampling=True,export_frame_step=1,export_apply=True,export_extras=True)
shutil.copy2(p/'capture-profile.json',o/'capture-profile.json');shutil.copy2(p/'smoke-anchor.json',o/'smoke-anchor.json')
sha=lambda x:hashlib.sha256(x.read_bytes()).hexdigest()
(o/'terrain-receipt.json').write_text(json.dumps(dict(parent_source_sha256=sha(p/'quarry-v5.blend'),source_sha256=sha(o/'quarry-v5.blend'),runtime_sha256=sha(o/'quarry-v5.glb'),correction='Bind white RGB and fade alpha to the same glTF COLOR_0 stream through supported texture x vertex-color multiplication; source appearance and geometry unchanged.',owner_visual_approved=False,native_integrated=False),indent=2)+'\n')
