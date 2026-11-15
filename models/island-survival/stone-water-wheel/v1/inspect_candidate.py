"""Independently reopen the actual .blend and GLB and render export evidence."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import struct
import sys

import bpy
import numpy as np
from mathutils import Vector

def digest(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def geometry():
    vertices=[]
    triangles=0
    degenerate=0
    missing_uv=[]
    degenerate_objects=[]
    graph=bpy.context.evaluated_depsgraph_get()
    for obj in bpy.context.scene.objects:
        if obj.type!='MESH':
            continue
        evaluated=obj.evaluated_get(graph)
        mesh=evaluated.to_mesh()
        vertices += [evaluated.matrix_world@v.co for v in mesh.vertices]
        mesh.calc_loop_triangles()
        triangles += len(mesh.loop_triangles)
        bad=sum(t.area<1e-12 for t in mesh.loop_triangles)
        degenerate += bad
        if bad:degenerate_objects.append({'object':obj.name,'triangles':bad})
        if any(m and m.use_nodes and any(n.type=='TEX_IMAGE' for n in m.node_tree.nodes) for m in mesh.materials) and not mesh.uv_layers:
            missing_uv.append(obj.name)
        evaluated.to_mesh_clear()
    coords=np.array(vertices)
    assert coords.size and np.isfinite(coords).all()
    return {'min':coords.min(axis=0).tolist(),'max':coords.max(axis=0).tolist(),
            'triangles':triangles,'degenerate_triangles':degenerate,
            'textured_objects_without_uv':missing_uv,'degenerate_objects':degenerate_objects}

def image_array(path):
    im=bpy.data.images.load(str(path),check_existing=False)
    result=np.array(im.pixels[:],dtype=np.float32).reshape(im.size[1],im.size[0],4)
    bpy.data.images.remove(im)
    return result

def save_image(path,pixels):
    im=bpy.data.images.new(path.stem,width=pixels.shape[1],height=pixels.shape[0],alpha=True)
    im.pixels.foreach_set(pixels.ravel())
    im.filepath_raw=str(path)
    im.file_format='PNG'
    im.save()
    bpy.data.images.remove(im)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--candidate',type=Path,required=True)
    parser.add_argument('--fmpl-tools',type=Path,required=True)
    parser.add_argument('--stem',default='stone-water-wheel-v1')
    args=parser.parse_args(sys.argv[sys.argv.index('--')+1:])
    out=args.candidate.resolve()
    sys.path.insert(0,str(args.fmpl_tools.resolve()))
    from blender_camera_guard import assert_clean,install_canonical_camera
    profile=json.loads((out/'capture-profile.json').read_text())
    source=out/(args.stem+'.blend')
    export=out/(args.stem+'.glb')
    bpy.ops.wm.open_mainfile(filepath=str(source))
    scene=bpy.context.scene
    assert_clean(scene,profile,bpy)
    scene.frame_set(1)
    original=geometry()
    assert original['degenerate_triangles']==0 and not original['textured_objects_without_uv'], original
    packed=[im.name for im in bpy.data.images if im.packed_file]
    assert len(packed)>=6,packed
    sockets=[o for o in scene.objects if o.get('role')=='stationary_outlet']
    assert len(sockets)==2
    transforms={o.name:o.matrix_world.copy() for o in sockets}
    wheel=bpy.data.objects['WHEEL | rotating scoop assembly']
    initial=wheel.matrix_world.copy()
    max_socket_motion=0
    for frame in range(1,98,6):
        scene.frame_set(frame)
        bpy.context.view_layer.update()
        for o in sockets:
            max_socket_motion=max(max_socket_motion,max(abs(o.matrix_world[i][j]-transforms[o.name][i][j]) for i in range(4) for j in range(4)))
    seam=max(abs(wheel.matrix_world[i][j]-initial[i][j]) for i in range(4) for j in range(4))
    assert max_socket_motion<1e-7 and seam<1e-5
    scene.frame_set(1)
    blob=export.read_bytes()
    magic,version,total=struct.unpack_from('<III',blob)
    assert magic==0x46546c67 and version==2 and total==len(blob)
    length,kind=struct.unpack_from('<II',blob,12)
    assert kind==0x4e4f534a
    gltf=json.loads(blob[20:20+length])
    assert gltf.get('animations') and all('uri' not in im for im in gltf['images'])
    textured=[]
    for m in gltf['materials']:
        pbr=m.get('pbrMetallicRoughness',{})
        if 'baseColorTexture' in pbr:
            assert 'normalTexture' in m and 'metallicRoughnessTexture' in pbr,m['name']
            textured.append(m['name'])
    assert len(textured)>=2,textured
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=str(export))
    # glTF times are seconds; import into Blender's default 24 FPS can place
    # source frame 1 at a fractional frame. Compare the exact declared first
    # sample, rather than accidentally inspecting a later interpolated pose.
    first_time=min(gltf['accessors'][s['input']]['min'][0] for a in gltf['animations'] for s in a['samplers'])
    first_frame=first_time*bpy.context.scene.render.fps/bpy.context.scene.render.fps_base
    bpy.context.scene.frame_set(math.floor(first_frame),subframe=first_frame-math.floor(first_frame))
    assert not [o for o in bpy.data.objects if o.type=='CAMERA']
    imported=geometry()
    assert imported['degenerate_triangles']==0 and not imported['textured_objects_without_uv'], imported
    bounds_error=max(abs(a-b) for key in ('min','max') for a,b in zip(original[key],imported[key]))
    assert bounds_error<1e-5,{'error':bounds_error,'source':original,'export':imported,'imported_frame':bpy.context.scene.frame_current}
    scene=bpy.context.scene
    install_canonical_camera(scene,profile,bpy)
    scene.render.engine='CYCLES'
    scene.cycles.samples=32
    scene.cycles.use_denoising=False
    scene.render.threads_mode='FIXED'
    scene.render.threads=6
    scene.render.film_transparent=True
    scene.render.image_settings.file_format='PNG'
    scene.render.image_settings.color_mode='RGBA'
    scene.world=bpy.data.worlds.new('Inspection | neutral daylight')
    scene.world.use_nodes=True
    scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.35
    scene.view_settings.view_transform='AgX'
    for pos,energy in [((-3,-4,6),450),((3,2,4),180)]:
        data=bpy.data.lights.new('Inspection | area','AREA')
        data.energy,data.size=energy,4
        obj=bpy.data.objects.new(data.name,data)
        scene.collection.objects.link(obj)
        obj.location=pos
        obj.rotation_euler=(Vector((0,.3,.5))-obj.location).to_track_quat('-Z','Y').to_euler()
    root=bpy.data.objects['WHEEL | placement root']
    export_renders=[]
    for name,yaw in [('north',0),('east',270),('south',180),('west',90)]:
        root.rotation_euler.z=math.radians(yaw)
        bpy.context.view_layer.update()
        assert_clean(scene,profile,bpy)
        path=out/('export-reimport-'+name+'.png')
        scene.render.filepath=str(path)
        bpy.ops.render.render(write_still=True)
        export_renders.append({'file':path.name,'sha256':digest(path)})
    # Neutral clay exposes construction without the color/normal textures.
    clay=bpy.data.materials.new('Inspection | neutral clay')
    clay.use_nodes=True
    shader=clay.node_tree.nodes.get('Principled BSDF')
    shader.inputs['Base Color'].default_value=(.36,.36,.36,1)
    shader.inputs['Roughness'].default_value=.75
    scene.view_layers[0].material_override=clay
    for name,yaw in [('east',270),('west',90)]:
        root.rotation_euler.z=math.radians(yaw)
        scene.render.filepath=str(out/('export-clay-'+name+'.png'))
        bpy.ops.render.render(write_still=True)
    scene.view_layers[0].material_override=None
    manifest=json.loads((out/'render-manifest.json').read_text())
    layer_qa=[]
    motion=[]
    for name in ('north','east','south','west'):
        files=[r for r in manifest['images'] if r['facing']==name and r['state']=='working' and r['layer']=='full']
        arrays=[image_array(out/r['file']) for r in files]
        changes=[int(np.count_nonzero(np.max(np.abs(a-b),axis=2)>.025)) for a,b in zip(arrays,arrays[1:])]
        assert changes and min(changes)>8,(name,changes)
        motion.append({'facing':name,'frame_count':len(files),'min_changed_pixels_256':min(changes)})
        above=image_array(out/(name+'-working-001-above-water.png'))
        under=image_array(out/(name+'-working-001-underwater.png'))
        full=image_array(out/(name+'-working-001-full.png'))
        overlap=int(np.count_nonzero((above[:,:,3]>.9)&(under[:,:,3]>.9)))
        assert overlap==0,(name,overlap)
        assert np.count_nonzero(under[:,:,3]>.05)>8,name+' has no submerged geometry'
        union=np.maximum(above[:,:,3],under[:,:,3])
        missing=int(np.count_nonzero((full[:,:,3]>.95)&(union<.05)))
        assert missing==0,(name,missing)
        layer_qa.append({'facing':name,'opaque_layer_overlap_pixels':overlap,'missing_body_pixels':missing,
                         'underwater_pixels':int(np.count_nonzero(under[:,:,3]>.05))})
    sheet=np.zeros((768,1024,4),dtype=np.float32)
    for col,name in enumerate(('north','east','south','west')):
        for row,path in enumerate((out/(name+'-working-001-full.png'),out/('export-reimport-'+name+'.png'),out/(name+'-working-001-underwater.png'))):
            array=image_array(path)
            stride=array.shape[0]//256
            assert stride*256==array.shape[0]
            sheet[(2-row)*256:(3-row)*256,col*256:(col+1)*256]=array[::stride,::stride]
    save_image(out/'candidate-review-sheet.png',sheet)
    result={'schema':'tanks.stone-water-wheel.inspection.v1','technical_checks_passed':True,
        'visual_accepted':False,'game_integrated':False,'blender':bpy.app.version_string,
        'source_sha256':digest(source),'glb_sha256':digest(export),'packed_source_images':packed,
        'source_geometry':original,'runtime_geometry':imported,'bounds_error_tiles':bounds_error,
        'socket_motion_tiles':max_socket_motion,'wheel_loop_matrix_error':seam,
        'embedded_runtime_images':len(gltf['images']),'textured_pbr_materials':textured,
        'animation_count':len(gltf['animations']),'source_motion':motion,'layer_split':layer_qa,
        'runtime_renders':export_renders,'review_sheet_sha256':digest(out/'candidate-review-sheet.png'),
        'remaining':['Actual visual review and repair of any construction/flow defects',
                     '64/128/256 packing with measured native registration',
                     'Factorio placement/pipe/working/full-output/shoreline/landfill/stop/reload tests',
                     'Owner art acceptance and reviewed source promotion; FMPL registry receipt']}
    (out/'independent-inspection.json').write_text(json.dumps(result,indent=2)+'\n')
    print('INDEPENDENT_INSPECTION',json.dumps(result),flush=True)

if __name__=='__main__':
    main()
