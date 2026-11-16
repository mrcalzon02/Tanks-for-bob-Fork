"""Independently reopen selected model sources and render actual GLB fidelity pairs."""
import argparse,json,sys
from pathlib import Path
import bpy
sys.path.insert(0,str(Path(__file__).resolve().parent))
from material_icon_registry import PILOTS,folder
from build_hydrogen_resource_models import sha
from blender_camera_guard import assert_clean,camera_record,install_canonical_camera
parser=argparse.ArgumentParser();parser.add_argument('--assets',nargs='+',choices=list(PILOTS),default=list(PILOTS))
args=parser.parse_args(sys.argv[sys.argv.index('--')+1:])
for id in args.assets:
 dest=folder(id);cfg=json.loads((dest/'capture-profile.json').read_text());review=dest/'export-review';review.mkdir(exist_ok=True)
 bpy.ops.wm.open_mainfile(filepath=str(dest/'authored.blend'));assert_clean(bpy.context.scene,cfg,bpy)
 assert all(im.packed_file and all(im.size) for im in bpy.data.images if im.source=='FILE')
 (dest/'source-reopen-qa.json').write_text(json.dumps(dict(passed=True,source_reopened=True,source_sha256=sha(dest/'authored.blend'),
  camera=camera_record(bpy.context.scene),persistent_camera_count=1,packed_images=True),indent=2)+'\n')
 cfg['source_size']=512
 for kind,file in [('source','authored.blend'),('export','runtime-reimport.blend')]:
  bpy.ops.wm.open_mainfile(filepath=str(dest/file));scene=bpy.context.scene;install_canonical_camera(scene,cfg,bpy)
  scene.render.film_transparent=True;scene.cycles.samples=32;scene.cycles.use_denoising=True
  scene.cycles.device='CPU'
  scene.render.resolution_x=512;scene.render.resolution_y=512;scene.render.resolution_percentage=100
  scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA'
  scene.render.filepath=str(review/(kind+'-beauty.png'));bpy.ops.render.render(write_still=True)
  for mat in {m for ob in scene.objects if ob.type=='MESH' for m in ob.data.materials}:
   nodes=mat.node_tree.nodes;links=mat.node_tree.links;bs=next(n for n in nodes if n.type=='BSDF_PRINCIPLED')
   output=next(n for n in nodes if n.type=='OUTPUT_MATERIAL');emit=nodes.new('ShaderNodeEmission');color=bs.inputs['Base Color']
   if color.is_linked:links.new(color.links[0].from_socket,emit.inputs['Color'])
   else:emit.inputs['Color'].default_value=color.default_value
   links.new(emit.outputs[0],output.inputs['Surface'])
  scene.render.filepath=str(review/(kind+'-basecolor.png'));bpy.ops.render.render(write_still=True)
 print('MATERIAL_EXPORT_REVIEW',id,flush=True)
