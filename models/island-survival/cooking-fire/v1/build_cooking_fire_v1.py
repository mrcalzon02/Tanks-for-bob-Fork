"""Derive the Cooking Fire directly from the accepted V12 campfire.

blender -b -t 4 --python-exit-code 1 --python build_cooking_fire_v1.py -- \
    --source-blend /path/to/production-v12-structure-45/master.blend \
    --output-dir /path/to/output --render pilot
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import struct
import sys

import bpy
from mathutils import Vector

SOURCE_SHA256 = '7cf8e35b27a670f00bc5b4a5b55c2dbe4ce448edb3ad8bf1b3ff9fd316493632'
SOURCE_COMMIT = 'ce3ef9720298807e3036962bde094341643c237f'
SOURCE_PATH = 'models/island-survival/blender/production-v12-structure-45/master.blend'


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def mesh_fingerprint(obj):
    h = hashlib.sha256()
    for v in obj.data.vertices:
        h.update(struct.pack('<3f', *v.co))
    for poly in obj.data.polygons:
        h.update(struct.pack('<I', len(poly.vertices)))
        h.update(struct.pack('<' + 'I' * len(poly.vertices), *poly.vertices))
        h.update(struct.pack('<I', poly.material_index))
    return {'mesh_sha256': h.hexdigest(),
            'materials': [m.name if m else None for m in obj.data.materials],
            'location': list(obj.location), 'rotation': list(obj.rotation_euler),
            'scale': list(obj.scale), 'parent': obj.parent.name if obj.parent else None}


def iron_material(name, dark=False):
    material = bpy.data.materials.new(name)
    material.use_nodes = True
    nodes, links = material.node_tree.nodes, material.node_tree.links
    shader = nodes.get('Principled BSDF')
    shader.inputs['Metallic'].default_value = .72
    shader.inputs['Roughness'].default_value = .73
    noise = nodes.new('ShaderNodeTexNoise')
    noise.inputs['Scale'].default_value = 64
    noise.inputs['Detail'].default_value = 3
    ramp = nodes.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].position = .22
    ramp.color_ramp.elements[0].color = (.022, .025, .028, 1) if dark else (.045, .050, .057, 1)
    ramp.color_ramp.elements[1].position = .80
    ramp.color_ramp.elements[1].color = (.075, .075, .071, 1) if dark else (.15, .16, .17, 1)
    links.new(noise.outputs['Fac'], ramp.inputs['Fac'])
    links.new(ramp.outputs['Color'], shader.inputs['Base Color'])
    bump = nodes.new('ShaderNodeBump')
    bump.inputs['Strength'].default_value = .25
    bump.inputs['Distance'].default_value = .008
    links.new(noise.outputs['Fac'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], shader.inputs['Normal'])
    return material


def link_object(name, data, collection, pivot, material=None):
    obj = bpy.data.objects.new(name, data)
    collection.objects.link(obj)
    obj.parent = pivot
    if material:
        data.materials.append(material)
    obj['Cooking Fire component'] = True
    return obj


def lathe(name, profile, collection, pivot, material, segments=96):
    verts, faces = [], []
    for radius, z in profile:
        for i in range(segments):
            theta = 2 * math.pi * i / segments
            dent = 1 + .005 * math.sin(7*theta + z*3) + .003 * math.sin(13*theta-z*5)
            verts.append((radius * dent * math.cos(theta), radius * dent * math.sin(theta), z))
    for j in range(len(profile)-1):
        for i in range(segments):
            ni=(i+1)%segments
            faces.append((j*segments+i,j*segments+ni,(j+1)*segments+ni,(j+1)*segments+i))
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = link_object(name, mesh, collection, pivot, material)
    for poly in mesh.polygons:
        poly.use_smooth = True
    return obj


def tube(name, points, radius, collection, pivot, material):
    curve = bpy.data.curves.new(name, 'CURVE')
    curve.dimensions = '3D'
    curve.resolution_u = 12
    curve.bevel_depth = radius
    curve.bevel_resolution = 4
    curve.use_fill_caps = True
    spline = curve.splines.new('BEZIER')
    spline.bezier_points.add(len(points)-1)
    for bp, point in zip(spline.bezier_points, points):
        bp.co = point
        bp.handle_left_type = bp.handle_right_type = 'AUTO'
    return link_object(name, curve, collection, pivot, material)


def annulus(name, center, normal, radius, tube_radius, collection, pivot, material):
    normal = Vector(normal).normalized()
    tangent = normal.cross(Vector((0,0,1)))
    if tangent.length < .01:
        tangent = normal.cross(Vector((0,1,0)))
    tangent.normalize()
    bitangent = normal.cross(tangent).normalized()
    points = [Vector(center)+radius*(math.cos(i*2*math.pi/24)*tangent+math.sin(i*2*math.pi/24)*bitangent) for i in range(25)]
    return tube(name, points, tube_radius, collection, pivot, material)


def stone_height(scene, x, y):
    hits=[]
    for obj in scene.objects:
        if not obj.name.startswith('stone_'):
            continue
        inv = obj.matrix_world.inverted()
        origin = inv @ Vector((x,y,3))
        direction = (inv.to_3x3() @ Vector((0,0,-1))).normalized()
        hit, loc, _, _ = obj.ray_cast(origin, direction)
        if hit:
            hits.append((obj.matrix_world @ loc).z)
    if not hits:
        raise ValueError(f'No source stone beneath support at {x},{y}')
    return max(hits)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--source-blend', type=Path, required=True)
    parser.add_argument('--output-dir', type=Path, required=True)
    parser.add_argument('--render', choices=('none','pilot','proof'), default='proof')
    args=parser.parse_args(sys.argv[sys.argv.index('--')+1:])
    if digest(args.source_blend) != SOURCE_SHA256:
        raise ValueError('Source must be the exact accepted V12 master')
    out=args.output_dir.resolve()
    out.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.open_mainfile(filepath=str(args.source_blend.resolve()))
    scene=bpy.data.scenes['RENDER']
    bpy.context.window.scene=scene
    scene.frame_set(0)
    bpy.context.view_layer.update()
    pivot=bpy.data.objects['EXPORT | direction pivot']
    source_meshes={o.name:mesh_fingerprint(o) for o in scene.objects if o.type=='MESH'}
    source_actions=sorted(a.name for a in bpy.data.actions)
    daylight={o.name: {'matrix': [list(row) for row in o.matrix_world], 'power':o.data.energy, 'color':list(o.data.color)} for o in scene.objects if o.type=='LIGHT' and o.name!='04 | animated fire light'}
    collection=bpy.data.collections.new('05 | Cooking Fire additions')
    scene.collection.children.link(collection)
    bpy.data.scenes['MODEL'].collection.children.link(collection)
    iron=iron_material('Cooking Fire | hammered cast iron')
    soot=iron_material('Cooking Fire | soot-dark iron', dark=True)
    profile=[(.001,.805),(.22,.805),(.32,.83),(.43,.89),(.51,.99),(.565,1.12),(.58,1.24),(.57,1.34),(.54,1.45),(.525,1.53),(.525,1.565),(.515,1.585),(.485,1.585),(.475,1.565),(.48,1.53),(.492,1.46),(.52,1.34),(.53,1.24),(.515,1.13),(.465,1.01),(.39,.93),(.29,.885),(.20,.87),(.001,.87),(.001,.805)]
    pot=lathe('Cooking Fire | thick-walled cauldron', profile, collection, pivot, iron)
    pot['Design'] = 'Added onto the original unscaled V12 stone/log/fire assembly'
    annulus('Cooking Fire | rolled rim',(0,0,1.575),(0,0,1),.505,.031,collection,pivot,iron)
    for sign in (-1,1):
        tube('Cooking Fire | left handle' if sign<0 else 'Cooking Fire | right handle',[(sign*.55,-.10,1.36),(sign*.73,-.10,1.43),(sign*.79,0,1.46),(sign*.73,.10,1.43),(sign*.55,.10,1.36)],.030,collection,pivot,iron)
    supports=[]
    for index,theta in enumerate((-math.pi/2,math.pi/6,5*math.pi/6)):
        cx,cy=math.cos(theta),math.sin(theta)
        x,y=.73*cx,.73*cy
        h=stone_height(scene,x,y)
        points=[(x,y,h-.005),(.69*cx,.69*cy,h+.09),(.58*cx,.58*cy,.68),(.43*cx,.43*cy,.925)]
        tube(f'Cooking Fire | supported trivet leg {index+1}',points,.041,collection,pivot,soot)
        supports.append({'foot':[x,y,h],'contact':'ray-cast against unchanged source stone'})
    annulus('Cooking Fire | trivet cradle',(0,0,.925),(0,0,1),.445,.031,collection,pivot,soot)
    # A low rear steam connection follows the existing 3x3 machine contract.
    # The world contact plane is at the north tile edge, separate from the pipe-cell center.
    tube('Cooking Fire | rear steam feed',[(0,.52,1.25),(0,.69,1.18),(0,.75,.67),(0,.91,.35),(0,1.40,.35)],.064,collection,pivot,soot)
    # Model an actual open socket instead of a capped cylinder.
    socket_profile=[(.064,0),(.085,0),(.085,.11),(.064,.11),(.052,.10),(.052,.01),(.064,0)]
    socket=lathe('Cooking Fire | open north steam socket',socket_profile,collection,pivot,iron,segments=64)
    socket.rotation_euler.x=-math.pi/2
    socket.location=(0,1.39,.35)
    annulus('Cooking Fire | steam collar',(0,.58,1.225),(0,1,0),.085,.015,collection,pivot,iron)
    marker=bpy.data.objects.new('SOCKET | steam input | north boundary',None)
    collection.objects.link(marker)
    marker.parent=pivot
    marker.location=(0,1.5,.35)
    marker.empty_display_type='ARROWS'
    marker.empty_display_size=.15
    marker['Factorio pipe cell']=[0,-1]
    marker['Factorio facing']='north'
    marker['Model axis mapping']='Blender +Y is Factorio north (-Y), provisional 1 unit per tile'
    marker['Status']='Model interface marker; native graphical placement not yet reviewed'
    # A visible liquid surface belongs to the open cauldron, not hidden internals.
    liquid=bpy.data.materials.new('Cooking Fire | dark cooking water')
    liquid.use_nodes=True
    shader=liquid.node_tree.nodes.get('Principled BSDF')
    shader.inputs['Base Color'].default_value=(.12,.083,.035,1)
    shader.inputs['Roughness'].default_value=.23
    shader.inputs['Metallic'].default_value=.10
    water=lathe('Cooking Fire | cooking surface',[(.001,1.43),(.496,1.43),(.496,1.435),(.001,1.435)],collection,pivot,liquid)
    # Camera angle/daylight are retained; fixed framing expands for the pot and socket.
    target=Vector((0,0,.70))
    scene.camera.location=target+Vector((0,-1,1)).normalized()*6
    scene.camera.rotation_euler=(target-scene.camera.location).to_track_quat('-Z','Y').to_euler()
    scene.camera.data.ortho_scale=3.35
    scene.render.resolution_x=scene.render.resolution_y=384
    scene.render.resolution_percentage=100
    scene.render.film_transparent=True
    scene.render.image_settings.file_format='PNG'
    scene.render.image_settings.color_mode='RGBA'
    scene.render.image_settings.color_depth='8'
    scene.render.fps=8
    scene.cycles.device='CPU'
    scene.cycles.samples=32
    scene.cycles.use_denoising=True
    scene.cycles.seed=5855
    scene.cycles.use_animated_seed=False
    scene.render.threads_mode='FIXED'
    scene.render.threads=4
    scene['Cooking Fire source SHA256']=SOURCE_SHA256
    scene['Cooking Fire status']='V1 model candidate derived from accepted Campfire V12; no game integration'
    scene['Frame states']='0 cold; 1-96 inherited fire animation'
    scene.frame_set(0)
    bpy.context.view_layer.update()
    assert source_meshes=={name:mesh_fingerprint(bpy.data.objects[name]) for name in source_meshes},'Source meshes were changed'
    assert source_actions==sorted(a.name for a in bpy.data.actions),'Source animation actions were changed'
    for image in bpy.data.images:
        if image.source=='FILE' and not image.packed_file:
            raise ValueError(f'Unpacked external texture: {image.name}')
    blend_path=out/'cooking-fire-v1.blend'
    bpy.ops.wm.save_as_mainfile(filepath=str(blend_path),check_existing=False,compress=True)
    bpy.ops.wm.open_mainfile(filepath=str(blend_path))
    scene=bpy.data.scenes['RENDER']
    bpy.context.window.scene=scene
    scene.frame_set(0)
    bpy.context.view_layer.update()
    assert source_meshes=={name:mesh_fingerprint(bpy.data.objects[name]) for name in source_meshes},'Reopened source geometry differs'
    pivot=bpy.data.objects['EXPORT | direction pivot']
    report={'asset':'Cooking Fire V1','status':'review candidate','source_commit':SOURCE_COMMIT,'source_path':SOURCE_PATH,'source_sha256':SOURCE_SHA256,'native_sha256':digest(blend_path),'blender':bpy.app.version_string,'source_mesh_count':len(source_meshes),'source_meshes_unchanged':True,'source_animation_actions_retained':source_actions,'source_mesh_fingerprints':source_meshes,'supports':supports,'camera':{'elevation_deg':45,'ortho_scale':3.35,'target':[0,0,.70]},'daylight':daylight,'native_reopen':'passed','game_integration':False,'captures':[]}
    report_path=out/'build-report.json'
    report_path.write_text(json.dumps(report,indent=2)+'\n')
    if args.render=='none':
        return
    tasks=[('working-north',37,0,False)]
    if args.render=='proof':
        tasks += [('idle-'+name,0,angle,False) for name,angle in [('north',0),('east',90),('south',180),('west',270)]]
        tasks += [('working-'+name,37,angle,False) for name,angle in [('east',90),('south',180),('west',270)]]
        tasks += [('source-campfire',37,0,True)]
        tasks += [(f'loop-{i:02d}',frame,0,False) for i,frame in enumerate(range(1,97,6))]
    for name,frame,angle,source_only in tasks:
        pivot.rotation_euler.z=math.radians(angle)
        scene.frame_set(frame)
        for obj in bpy.data.collections['05 | Cooking Fire additions'].objects:
            obj.hide_render=source_only
        bpy.context.view_layer.update()
        path=out/'renders'/(name+'.png')
        path.parent.mkdir(exist_ok=True)
        scene.render.filepath=str(path)
        print('COOKING_FIRE_CAPTURE',name,frame,angle,flush=True)
        bpy.ops.render.render(write_still=True)
        report['captures'].append({'name':name,'frame':frame,'angle':angle,'path':str(path.relative_to(out)),'sha256':digest(path)})
        report_path.write_text(json.dumps(report,indent=2)+'\n')


if __name__=='__main__':
    main()
