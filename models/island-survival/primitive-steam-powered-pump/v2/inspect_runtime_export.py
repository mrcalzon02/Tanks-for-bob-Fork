"""Inspect the actual pipe-pump GLB in a new Blender process, including motion."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import struct
import sys

import bpy
from mathutils import Vector

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def geometry():
    dg=bpy.context.evaluated_depsgraph_get()
    positions=[]
    triangles=0
    bad=[]
    for obj in bpy.context.scene.objects:
        if obj.type!='MESH':continue
        evaluated=obj.evaluated_get(dg)
        mesh=evaluated.to_mesh()
        positions += [evaluated.matrix_world@v.co for v in mesh.vertices]
        mesh.calc_loop_triangles()
        triangles+=len(mesh.loop_triangles)
        count=sum(t.area<1e-12 for t in mesh.loop_triangles)
        if count:bad.append({'object':obj.name,'count':count})
        evaluated.to_mesh_clear()
    assert positions and all(math.isfinite(v[i]) for v in positions for i in range(3))
    return {'min':[min(v[i] for v in positions) for i in range(3)],
            'max':[max(v[i] for v in positions) for i in range(3)],
            'triangles':triangles,'degenerate_objects':bad}

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--candidate',type=Path,required=True)
    p.add_argument('--fmpl-tools',type=Path,required=True)
    p.add_argument('--stem',default='pipe-pump-v2')
    args=p.parse_args(sys.argv[sys.argv.index('--')+1:])
    out=args.candidate.resolve()
    sys.path.insert(0,str(args.fmpl_tools.resolve()))
    from blender_camera_guard import install_canonical_camera,assert_clean
    native=out/(args.stem+'.blend')
    runtime=out/(args.stem+'.glb')
    bpy.ops.wm.open_mainfile(filepath=str(native))
    bpy.context.scene.frame_set(1)
    original=geometry()
    blob=runtime.read_bytes()
    length,kind=struct.unpack_from('<II',blob,12)
    assert kind==0x4e4f534a
    gltf=json.loads(blob[20:20+length])
    assert gltf.get('animations') and not gltf.get('cameras')
    assert all('uri' not in image for image in gltf.get('images',[]))
    first=min(gltf['accessors'][sampler['input']]['min'][0] for anim in gltf['animations'] for sampler in anim['samplers'])
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.context.scene.render.fps=48
    bpy.ops.import_scene.gltf(filepath=str(runtime))
    scene=bpy.context.scene
    def source_frame(frame):
        target=(first+(frame-1)/48)*scene.render.fps/scene.render.fps_base
        scene.frame_set(math.floor(target),subframe=target-math.floor(target))
        bpy.context.view_layer.update()
    source_frame(1)
    imported=geometry()
    assert not original['degenerate_objects'] and not imported['degenerate_objects'],(original,imported)
    bounds_error=max(abs(a-b) for key in ('min','max') for a,b in zip(original[key],imported[key]))
    assert bounds_error<1e-5,(original,imported)
    ports=[o for o in scene.objects if o.name.startswith('PORT | ')]
    assert len(ports)==4
    reference={o.name:o.matrix_world.copy() for o in ports}
    pin=bpy.data.objects['MOTION | crank eccentric pin']
    head=bpy.data.objects['V2 JOINT | real crosshead pivot']
    eyes=[o for o in scene.objects if o.name.startswith('V2 JOINT | connecting rod eye')]
    assert len(eyes)==2
    max_joint=max_rod=max_port=0.
    for frame in range(1,98):
        source_frame(frame)
        a,b=[o.matrix_world.translation for o in eyes]
        cr,hd=pin.matrix_world.translation,head.matrix_world.translation
        max_joint=max(max_joint,min((a-cr).length,(b-cr).length),min((a-hd).length,(b-hd).length))
        max_rod=max(max_rod,abs((a-b).length-.6))
        for port in ports:
            max_port=max(max_port,max(abs(port.matrix_world[i][j]-reference[port.name][i][j]) for i in range(4) for j in range(4)))
    assert max_joint<1e-5 and max_rod<1e-6 and max_port<1e-7,(max_joint,max_rod,max_port)
    source_frame(1)
    profile=json.loads((out/'capture-profile.json').read_text())
    install_canonical_camera(scene,profile,bpy)
    scene.render.engine='CYCLES'
    scene.cycles.samples=48
    scene.cycles.use_denoising=False
    scene.render.film_transparent=True
    scene.render.image_settings.file_format='PNG'
    scene.render.image_settings.color_mode='RGBA'
    scene.view_settings.view_transform='AgX'
    scene.world=bpy.data.worlds.new('Actual export | neutral inspection')
    scene.world.use_nodes=True
    scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.35
    for position,power in [((-3,-4,6),450),((3,2,4),180)]:
        light=bpy.data.lights.new('Actual export | area','AREA')
        light.energy,light.size=power,4
        obj=bpy.data.objects.new(light.name,light)
        scene.collection.objects.link(obj)
        obj.location=position
        obj.rotation_euler=(Vector((0,0,.8))-obj.location).to_track_quat('-Z','Y').to_euler()
    # Imported nodes can have quaternion animation. Use a separate, unanimated
    # inspection pivot rather than writing Euler angles into an animated node.
    root=bpy.data.objects.new('INSPECT | rotate imported assembly',None)
    scene.collection.objects.link(root)
    for obj in list(scene.objects):
        if obj is not root and obj.parent is None and obj.type not in {'CAMERA','LIGHT'}:
            world=obj.matrix_world.copy()
            obj.parent=root
            obj.matrix_world=world
    images=[]
    for name,yaw in [('north',0),('east',270),('south',180),('west',90)]:
        root.rotation_euler.z=math.radians(yaw)
        source_frame(1)
        assert_clean(scene,profile,bpy)
        path=out/('actual-glb-'+name+'.png')
        scene.render.filepath=str(path)
        bpy.ops.render.render(write_still=True)
        images.append({'file':path.name,'sha256':sha(path)})
    texture_channels=[]
    for material in gltf.get('materials',[]):
        pbr=material.get('pbrMetallicRoughness',{})
        if 'baseColorTexture' in pbr:
            assert 'normalTexture' in material and 'metallicRoughnessTexture' in pbr,material.get('name')
            texture_channels.append(material.get('name'))
    approved=(out/'owner-disposition.json').is_file()
    result={'schema':'tanks.pipe-pump.runtime-inspection','geometry_and_motion_checks_passed':True,
        'overall_visual_accepted':approved,'game_integrated':False,'source_sha256':sha(native),'glb_sha256':sha(runtime),
        'source_geometry':original,'runtime_geometry':imported,'bounds_error_tiles':bounds_error,
        'sampled_source_frames':97,'max_joint_error_tiles':max_joint,'max_rigid_length_error_tiles':max_rod,
        'max_socket_motion_tiles':max_port,'embedded_images':len(gltf.get('images',[])),
        'textured_materials_with_exported_albedo_normal_metallic_roughness':texture_channels,
        'runtime_renders':images,'remaining':['Native Factorio integration/transfer/registration evidence'] if approved else ['Owner visual disposition and native integration']}
    (out/'runtime-inspection.json').write_text(json.dumps(result,indent=2)+'\n')
    print('ACTUAL_PIPE_PUMP_EXPORT_INSPECTED',json.dumps(result),flush=True)

if __name__=='__main__':main()
