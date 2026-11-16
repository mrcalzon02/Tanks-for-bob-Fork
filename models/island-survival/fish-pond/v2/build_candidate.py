"""Refine the real V1 pond, bake portable surfaces, export and render a pilot."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import sys

import bpy
from mathutils import Vector

ROOT_NAME = 'EXPORT | rotate all clay and tools, never camera'
SOURCE_SHA = '0a7a738ddeba0f3675ce40724a20bf5acf1a0537e0bef085032cfc3d13100427'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')


def curves(owner):
    action = owner.animation_data.action if owner.animation_data else None
    if action is None:
        return []
    if hasattr(action, 'fcurves'):
        return list(action.fcurves)
    return [c for layer in action.layers for strip in layer.strips
            for bag in strip.channelbags for c in bag.fcurves]


def material(name, colour, rough=.8):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    shader = mat.node_tree.nodes.get('Principled BSDF')
    shader.inputs['Base Color'].default_value = (*colour, 1)
    shader.inputs['Roughness'].default_value = rough
    return mat


def ceramic_surface():
    mat = material('POND V2 | fired clay pipe walls', (.29, .135, .062), .83)
    nodes, links = mat.node_tree.nodes, mat.node_tree.links
    shader = nodes.get('Principled BSDF')
    noise = nodes.new('ShaderNodeTexNoise')
    noise.inputs['Scale'].default_value = 95
    bump = nodes.new('ShaderNodeBump')
    bump.inputs['Strength'].default_value = .18
    bump.inputs['Distance'].default_value = .008
    links.new(noise.outputs['Fac'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], shader.inputs['Normal'])
    return mat


def ports(root, reference, helpers):
    sys.path.insert(0, str(helpers))
    from mesh_util import mesh, box
    import bmesh
    if sha(reference) != 'af6d1d74f0439b327b0b4e496386aa35fdac0859c177b55707dbfb5243e691ca':
        raise ValueError('Fluid dimensional reference hash mismatch')
    ceramic = ceramic_surface()
    collection = bpy.data.collections.new('POND V2 | supported native fluid mouths')
    bpy.context.scene.collection.children.link(collection)
    for side, sign in [('north', 1), ('south', -1)]:
        # One connected wall avoids the coincident inner cylinders in the
        # separate reference collar/throat templates. Nominal dimensions and
        # the .003 arris come directly from that hash-pinned reference.
        outer = [(1.5,.36,.337), (1.497,.36,.34), (1.428,.36,.34),
                 (1.425,.36,.337), (1.425,.36,.288), (1.422,.36,.285),
                 (1.21,.36,.285), (1.13,.35,.274), (1.04,.30,.23),
                 (.96,.20,.18), (.90,.10,.145)]
        inner = [(1.5,.36,.248), (1.497,.36,.245), (1.21,.36,.245),
                 (1.13,.35,.234), (1.04,.30,.19), (.96,.20,.14), (.90,.10,.105)]
        vertices, faces, rings = [], [], []
        segments = 64
        for layer, profile in enumerate((outer, inner)):
            layer_rings = []
            for i, (y,z,radius) in enumerate(profile):
                tangent = Vector((0,-sign,0))
                if y < 1.21:
                    before, after = profile[i-1], profile[min(len(profile)-1,i+1)]
                    tangent = Vector((0,sign*(after[0]-before[0]),after[1]-before[1])).normalized()
                across = Vector((1,0,0))
                up = tangent.cross(across).normalized()
                center = Vector((0,sign*y,z))
                ring = []
                for k in range(segments):
                    ring.append(len(vertices))
                    vertices.append(tuple(center+radius*(math.cos(k*math.tau/segments)*across+math.sin(k*math.tau/segments)*up)))
                layer_rings.append(ring)
            rings.append(layer_rings)
            for a,b in zip(layer_rings,layer_rings[1:]):
                for k in range(segments):
                    j = (k+1)%segments
                    faces.append((a[k],a[j],b[j],b[k]))
        for end in (0,-1):
            a,b = rings[0][end],rings[1][end]
            for k in range(segments):
                j = (k+1)%segments
                faces.append((a[k],a[j],b[j],b[k]))
        obj = mesh('POND V2 | '+side+' continuous hollow ceramic mouth', vertices, faces,
                   ceramic, collection, root)
        bm = bmesh.new()
        bm.from_mesh(obj.data)
        bmesh.ops.recalc_face_normals(bm, faces=list(bm.faces))
        bm.to_mesh(obj.data)
        bm.free()
        for face in obj.data.polygons:
            face.use_smooth = True
        obj['full_hollow_wall'] = True
        obj['dimensional_reference_sha256'] = sha(reference)
        # Low fired-clay saddles meet the existing ground and support the mouth.
        for x in (-.27, .27):
            box('POND V2 | ' + side + ' mouth saddle', (x, sign*1.34, .10),
                (.18, .26, .20), ceramic, collection, root, bevel=.035)


def fish_refinement(scene):
    eye_mat = material('POND V2 | dark wet fish eyes', (.009, .012, .009), .3)
    fish = sorted((o for o in scene.objects if o.name.startswith('POND | fish') and o.name.endswith('body')), key=lambda o:o.name)
    for index, body in enumerate(fish):
        orbit = body.parent
        body['fmpl_visibility_group'] = 'working-fish'
        orbit.animation_data_clear()
        body.scale = (.85, .85, .85)
        # A separated school follows one ellipse. All headings use the actual
        # ellipse tangent; dense keys avoid corners and Euler seam reversal.
        previous = None
        for frame in range(1, 98):
            angle = index*math.pi/2 + (frame-1)*math.tau/96
            rx, ry = .46, .52
            heading = math.atan2(ry*math.cos(angle), -rx*math.sin(angle))
            if previous is not None:
                while heading-previous > math.pi:
                    heading -= math.tau
                while heading-previous < -math.pi:
                    heading += math.tau
            previous = heading
            orbit.location = (rx*math.cos(angle), ry*math.sin(angle), -.115-.006*index)
            orbit.rotation_euler.z = heading
            orbit.keyframe_insert(data_path='location', frame=frame)
            orbit.keyframe_insert(data_path='rotation_euler', frame=frame)
        for curve in curves(orbit):
            for key in curve.keyframe_points:
                key.interpolation = 'LINEAR'
        for curve in curves(body.data.shape_keys):
            for key in curve.keyframe_points:
                key.interpolation = 'LINEAR'
        for face in body.data.polygons:
            face.use_smooth = len(face.vertices) == 3 and face.index < 24
        # Source body and darker fin assignments are retained. The dorsal side
        # gets a species-specific gradient, so bake still explains anatomy.
        mat = body.data.materials[0]
        shader = mat.node_tree.nodes.get('Principled BSDF')
        base = tuple(shader.inputs['Base Color'].default_value[:3])
        nodes, links = mat.node_tree.nodes, mat.node_tree.links
        coord = nodes.new('ShaderNodeTexCoord')
        separate = nodes.new('ShaderNodeSeparateXYZ')
        ramp = nodes.new('ShaderNodeValToRGB')
        ramp.color_ramp.elements[0].color = (*[min(1, x*1.4+.05) for x in base], 1)
        ramp.color_ramp.elements[1].color = (*[x*.65 for x in base], 1)
        links.new(coord.outputs['Generated'], separate.inputs[0])
        links.new(separate.outputs['Z'], ramp.inputs[0])
        links.new(ramp.outputs['Color'], shader.inputs['Base Color'])
        for sign in (-1, 1):
            bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=8, radius=.012)
            eye = bpy.context.object
            eye.name = 'POND V2 | fish %02d eye' % (index+1)
            eye['fmpl_visibility_group'] = 'working-fish'
            eye.parent = body
            eye.location = (.115, sign*.025, .012)
            eye.data.materials.append(eye_mat)
            for frame, hidden in [(0, True), (1, False), (97, False)]:
                eye.hide_render = hidden
                eye.keyframe_insert(data_path='hide_render', frame=frame)


def portable_water():
    water = bpy.data.objects['POND | permanent filled water plane']
    mat = material('POND V2 | portable translucent water', (.045, .23, .27), .20)
    shader = mat.node_tree.nodes.get('Principled BSDF')
    shader.inputs['Alpha'].default_value = .53
    shader.inputs['IOR'].default_value = 1.33
    # Alpha alone closely reproduces the source's .47 Transparent mix without
    # introducing a nonportable arbitrary shader network or refraction shift.
    shader.inputs['Transmission Weight'].default_value = 0
    mat.surface_render_method = 'DITHERED'
    mat.use_transparency_overlap = False
    water.data.materials.clear()
    water.data.materials.append(mat)
    uv = water.data.uv_layers.new(name='Pond water planar coordinates')
    for loop in water.data.loops:
        co = water.data.vertices[loop.vertex_index].co
        uv.data[loop.index].uv = (co.x/2+.5, co.y/2+.5)
    return water


def bake(scene, objects, out, size):
    bpy.ops.object.select_all(action='DESELECT')
    for obj in objects:
        obj.select_set(True)
        if not obj.data.shape_keys:
            bpy.context.view_layer.objects.active = obj
            for modifier in list(obj.modifiers):
                bpy.ops.object.modifier_apply(modifier=modifier.name)
        while obj.data.uv_layers:
            obj.data.uv_layers.remove(obj.data.uv_layers[0])
        obj.data.uv_layers.new(name='Pond V2 padded authored atlas')
    bpy.context.view_layer.objects.active = objects[0]
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(angle_limit=math.radians(66), island_margin=.012,
                             area_weight=.8, correct_aspect=True, scale_to_bounds=False)
    bpy.ops.object.mode_set(mode='OBJECT')
    mats = list({mat for obj in objects for mat in obj.data.materials})
    for mat in mats:
        mat.use_nodes = True
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 8
    scene.render.bake.margin = 8
    scene.render.bake.use_selected_to_active = False
    scene.render.bake.use_clear = True
    scene.render.bake.use_pass_direct = False
    scene.render.bake.use_pass_indirect = False
    scene.render.bake.use_pass_color = True
    textures = {}
    for kind in ('albedo', 'roughness', 'normal'):
        im = bpy.data.images.new('fish-pond-v2-'+kind, width=size, height=size, alpha=False)
        if kind != 'albedo':
            im.colorspace_settings.name = 'Non-Color'
        targets = []
        swaps = []
        for mat in mats:
            nodes, links = mat.node_tree.nodes, mat.node_tree.links
            target = nodes.new('ShaderNodeTexImage')
            target.image = im
            nodes.active = target
            targets.append((mat, target))
            if kind == 'roughness':
                output = next(n for n in nodes if n.type == 'OUTPUT_MATERIAL' and n.is_active_output)
                surface_link = output.inputs['Surface'].links[0]
                shader = nodes.get('Principled BSDF')
                if shader is None:
                    raise ValueError('Expected portable opaque Principled surface: '+mat.name)
                emission = nodes.new('ShaderNodeEmission')
                rough = shader.inputs['Roughness']
                if rough.is_linked:
                    links.new(rough.links[0].from_socket, emission.inputs['Color'])
                else:
                    value = rough.default_value
                    emission.inputs['Color'].default_value = (value, value, value, 1)
                old_socket = surface_link.from_socket
                links.new(emission.outputs[0], output.inputs['Surface'])
                swaps.append((mat, output, old_socket, emission))
        bpy.ops.object.bake(type={'albedo':'DIFFUSE', 'roughness':'EMIT', 'normal':'NORMAL'}[kind])
        for mat, output, old, emission in swaps:
            mat.node_tree.links.new(old, output.inputs['Surface'])
            mat.node_tree.nodes.remove(emission)
        for mat, target in targets:
            mat.node_tree.nodes.remove(target)
        im.filepath_raw = str(out/(im.name+'.png'))
        im.file_format = 'PNG'
        im.save()
        im.pack()
        textures[kind] = im
    mat = material('POND V2 | baked basin fish and ceramic atlas', (.5, .3, .1))
    nodes, links = mat.node_tree.nodes, mat.node_tree.links
    shader = nodes.get('Principled BSDF')
    for kind, im in textures.items():
        node = nodes.new('ShaderNodeTexImage')
        node.image = im
        if kind == 'normal':
            normal = nodes.new('ShaderNodeNormalMap')
            links.new(node.outputs['Color'], normal.inputs['Color'])
            links.new(normal.outputs[0], shader.inputs['Normal'])
        else:
            links.new(node.outputs['Color'], shader.inputs['Base Color' if kind == 'albedo' else 'Roughness'])
    for obj in objects:
        obj.data.materials.clear()
        obj.data.materials.append(mat)
        for face in obj.data.polygons:
            face.material_index = 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--reference', type=Path, required=True)
    parser.add_argument('--helpers', type=Path, required=True)
    parser.add_argument('--fmpl-tools', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--texture-size', type=int, default=2048)
    parser.add_argument('--render', choices=('proof', 'all'), default='proof')
    args = parser.parse_args(sys.argv[sys.argv.index('--')+1:])
    source, out = args.source.resolve(), args.out.resolve()
    if sha(source) != SOURCE_SHA:
        raise ValueError('Fish V1 source hash mismatch')
    if out.exists():
        raise FileExistsError(out)
    out.mkdir(parents=True)
    bpy.ops.wm.open_mainfile(filepath=str(source))
    scene = bpy.context.scene
    scene.frame_set(1)
    scene.render.fps = 48
    scene.frame_start, scene.frame_end = 1, 97
    root = bpy.data.objects[ROOT_NAME]
    root.rotation_euler = (0, 0, 0)
    ports(root, args.reference.resolve(), args.helpers.resolve())
    fish_refinement(scene)
    water = portable_water()
    scene.frame_set(1)
    bpy.context.view_layer.update()
    objects = [o for o in root.children_recursive if o.type == 'MESH' and o != water]
    bake(scene, objects, out, args.texture_size)
    sys.path.insert(0, str(args.fmpl_tools.resolve()))
    from blender_camera_guard import install_canonical_camera, assert_clean, camera_record
    profile = {'camera_policy':'fmpl.factorio45.v1', 'capture_kind':'entity',
               'orientation_policy':'rotatable', 'directions':[0,90,180,270],
               'states':{'idle':[0], 'working':list(range(1,92,6))}, 'source_size':256,
               'camera_override':{'type':'ORTHO', 'elevation_deg':45, 'azimuth_deg':0,
                                  'distance':math.sqrt(72), 'ortho_scale':3.9, 'target':[0,0,.28]}}
    install_canonical_camera(scene, profile, bpy)
    scene.cycles.samples = 32
    scene.cycles.use_denoising = False
    scene.render.film_transparent = True
    scene.render.image_settings.color_mode = 'RGBA'
    assert_clean(scene, profile, bpy)
    native = out/'fish-pond-v2.blend'
    bpy.ops.wm.save_as_mainfile(filepath=str(native), compress=True)
    bpy.ops.wm.open_mainfile(filepath=str(native))
    scene = bpy.context.scene
    root = bpy.data.objects[ROOT_NAME]
    assert_clean(scene, profile, bpy)
    bpy.ops.object.select_all(action='DESELECT')
    for obj in [root, *list(root.children_recursive)]:
        obj.select_set(True)
    runtime = out/'fish-pond-v2.glb'
    bpy.ops.export_scene.gltf(filepath=str(runtime), export_format='GLB', use_selection=True,
        export_cameras=False, export_lights=False, export_animations=True,
        export_animation_mode='SCENE', export_frame_range=True, export_force_sampling=True,
        export_anim_scene_split_object=False,
        export_frame_step=1, export_apply=False, export_extras=True)
    projection = bpy.data.objects.new('SPRITE ONLY | square ground-grid projection', None)
    scene.collection.objects.link(projection)
    projection.scale.y = math.sqrt(2)
    root.parent = projection
    frames = []
    for facing, yaw in [('north',0), ('east',270), ('south',180), ('west',90)]:
        root.rotation_euler.z = math.radians(yaw)
        for state, indices in [('idle',[0]), ('working',list(range(16)) if args.render == 'all' else [4])]:
            for index in indices:
                frame = 0 if state == 'idle' else 1+6*index
                scene.frame_set(frame)
                assert_clean(scene, profile, bpy)
                path = out/(f'{facing}-{state}-{index:02d}.png')
                scene.render.filepath = str(path)
                bpy.ops.render.render(write_still=True)
                frames.append({'file':path.name, 'facing':facing, 'yaw':yaw, 'state':state,
                               'index':index, 'source_frame':frame, 'sha256':sha(path)})
    write(out/'capture-profile.json', profile)
    write(out/'build-report.json', {'schema':'tanks.fish-pond.v2.candidate', 'source_sha256':SOURCE_SHA,
        'native_sha256':sha(native), 'runtime_sha256':sha(runtime), 'blender':bpy.app.version_string,
        'fps':8, 'fish_count':4, 'unit_scale_runtime':True, 'visual_approved':False,
        'game_integrated':False, 'render_mode':args.render, 'camera':camera_record(scene),
        'sprite_global_y_projection':math.sqrt(2), 'images':frames})
    assert sha(source) == SOURCE_SHA
    print('FISH_POND_V2_CANDIDATE_COMPLETE', out, flush=True)


if __name__ == '__main__':
    main()
