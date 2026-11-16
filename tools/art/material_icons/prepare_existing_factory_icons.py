"""Make item capture masters from the actual, unchanged, already-authored factory GLBs."""
import json,math,shutil,sys
from pathlib import Path
import bpy
sys.path.insert(0,str(Path(__file__).resolve().parent))
from material_icon_registry import ROOT,PILOTS,folder
import build_hydrogen_resource_models as p
from build_material_icon_pilots import lighting
from blender_camera_guard import install_canonical_camera,assert_clean
for id,spec in PILOTS.items():
 if spec['shape']!='reuse-building':continue
 dest=folder(id)
 if dest.exists():raise FileExistsError('Preserve factory icon revisions '+str(dest))
 dest.mkdir(parents=True);shutil.copy2(spec['source_glb'],dest/'model.glb')
 bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(dest/'model.glb'));p.preserve_glb_images(dest)
 meshes=[o for o in bpy.context.scene.objects if o.type=='MESH'];bpy.context.view_layer.update();bounds=p.measure(meshes)
 cfg=json.loads((ROOT/'tools/fmpl/profiles/item-icon.example.json').read_text())
 cfg.update(asset=id,source='runtime-reimport.blend',source_size=256,sizes=[64,128,256],samples=32,threads=4)
 cfg['camera_override'].update(target=[(bounds[0][i]+bounds[1][i])/2 for i in range(3)],
  ortho_scale=max(bounds[1][0]-bounds[0][0],((bounds[1][1]-bounds[0][1])+(bounds[1][2]-bounds[0][2]))/math.sqrt(2))*1.16)
 for ob in list(bpy.context.scene.objects):
  if ob.type in ['LIGHT','CAMERA']:bpy.data.objects.remove(ob,do_unlink=True)
 lighting(bpy.context.scene);install_canonical_camera(bpy.context.scene,cfg,bpy);assert_clean(bpy.context.scene,cfg,bpy)
 for image in bpy.data.images:
  if image.source=='FILE':assert image.packed_file and all(image.size)
 bpy.ops.wm.save_as_mainfile(filepath=str(dest/'authored.blend'))
 bpy.ops.wm.save_as_mainfile(filepath=str(dest/'runtime-reimport.blend'))
 (dest/'capture-profile.json').write_text(json.dumps(cfg,indent=2)+'\n')
 triangles=invalid=0
 for ob in meshes:
  ob.data.calc_loop_triangles();triangles+=len(ob.data.loop_triangles);invalid+=sum(t.area<1e-12 for t in ob.data.loop_triangles)
 assert invalid==0
 record=dict(passed=True,asset=id,source_method='unchanged authored factory GLB reused as item icon',
  original_glb=str(spec['source_glb']),original_glb_sha256=p.sha(spec['source_glb']),
  original_editable_master=str(spec['editable_master']),original_editable_sha256=p.sha(spec['editable_master']),
  glb_sha256=p.sha(dest/'model.glb'),authored_sha256=p.sha(dest/'authored.blend'),triangles=triangles,
  degenerate_triangles=invalid,pose='upright building; canonical FMPL 45-degree orthographic optics',new_texture_bake=False)
 (dest/'runtime-inspection.json').write_text(json.dumps(record,indent=2)+'\n')
 (dest/'surface-plan.json').write_text(json.dumps(dict(construction=spec['construction'],source_regions='Retain original building-specific authored PBR surfaces',
  editable_master=str(spec['editable_master']),reused_glb_unchanged=True),indent=2)+'\n')
 print('EXISTING_FACTORY_ICON_SOURCE',id,flush=True)
