"""Reopen source and actual GLB independently; compare all 97 working poses."""
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


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def geometry():
    graph = bpy.context.evaluated_depsgraph_get()
    result = {}
    for obj in bpy.context.scene.objects:
        if obj.type != 'MESH':
            continue
        evaluated = obj.evaluated_get(graph)
        mesh = evaluated.to_mesh()
        points = np.array([tuple(evaluated.matrix_world @ v.co) for v in mesh.vertices])
        mesh.calc_loop_triangles()
        result[obj.name] = {'points':points, 'triangles':len(mesh.loop_triangles),
            'degenerates':sum(t.area < 1e-12 for t in mesh.loop_triangles),
            'uv':len(mesh.uv_layers) > 0,
            'finite':bool(np.isfinite(points).all())}
        evaluated.to_mesh_clear()
    return result


def summary(data):
    points = np.concatenate([v['points'] for v in data.values()])
    return {'min':points.min(axis=0).tolist(), 'max':points.max(axis=0).tolist(),
        'triangles':sum(v['triangles'] for v in data.values()),
        'mesh_count':len(data), 'degenerate_objects':{k:v['degenerates'] for k,v in data.items() if v['degenerates']},
        'missing_uv':[k for k,v in data.items() if not v['uv']],
        'finite':all(v['finite'] for v in data.values())}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--candidate', type=Path, required=True)
    parser.add_argument('--fmpl-tools', type=Path, required=True)
    args = parser.parse_args(sys.argv[sys.argv.index('--')+1:])
    out = args.candidate.resolve()
    native, runtime = out/'fish-pond-v2.blend', out/'fish-pond-v2.glb'
    bpy.ops.wm.open_mainfile(filepath=str(native))
    scene = bpy.context.scene
    original = []
    for frame in range(1, 98):
        scene.frame_set(frame)
        original.append(geometry())
    source = summary(original[0])
    assert source['finite'] and not source['degenerate_objects'] and not source['missing_uv'], source
    bodies = sorted(k for k in original[0] if k.startswith('POND | fish') and k.endswith('body'))
    assert len(bodies) == 4
    source_seam = max(float(np.abs(original[0][name]['points']-original[-1][name]['points']).max()) for name in bodies)
    assert source_seam < 1e-6, source_seam
    packed = [{'name':im.name, 'packed':bool(im.packed_file), 'size':list(im.size)}
              for im in bpy.data.images if im.name.startswith('fish-pond-v2-')]
    assert len(packed) == 3 and all(im['packed'] for im in packed), packed
    blob = runtime.read_bytes()
    length, kind = struct.unpack_from('<II', blob, 12)
    assert kind == 0x4e4f534a
    gltf = json.loads(blob[20:20+length])
    assert len(gltf.get('animations', [])) == 1 and not gltf.get('cameras')
    assert all('uri' not in im for im in gltf.get('images', []))
    first = min(gltf['accessors'][sampler['input']]['min'][0]
                for anim in gltf['animations'] for sampler in anim['samplers'])
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.context.scene.render.fps = 48
    bpy.ops.import_scene.gltf(filepath=str(runtime))
    scene = bpy.context.scene

    def pose(frame):
        target = (first+(frame-1)/48)*scene.render.fps/scene.render.fps_base
        scene.frame_set(math.floor(target), subframe=target-math.floor(target))
        bpy.context.view_layer.update()

    pose(1)
    initial = geometry()
    imported = summary(initial)
    assert imported['finite'] and not imported['degenerate_objects'] and not imported['missing_uv'], imported
    assert set(initial) == set(original[0]), (set(initial)-set(original[0]), set(original[0])-set(initial))
    mouths = [obj for obj in scene.objects if obj.name.startswith('POND V2 | ') and 'continuous hollow ceramic mouth' in obj.name]
    assert len(mouths) == 2
    port_matrices = {obj.name:obj.matrix_world.copy() for obj in mouths}
    max_error = max_port = 0.0
    worst = None
    for frame in range(1, 98):
        pose(frame)
        data = geometry()
        for name, actual in data.items():
            expected = original[frame-1][name]['points']
            # Export can split vertices at UV/normal seams; every actual vertex
            # must still match an evaluated source vertex in world coordinates.
            points = actual['points']
            if name in bodies:
                error = np.sqrt(((points[:,None,:]-expected[None,:,:])**2).sum(axis=2)).min(axis=1).max()
            else:
                error = max(np.abs(points.min(axis=0)-expected.min(axis=0)).max(),
                            np.abs(points.max(axis=0)-expected.max(axis=0)).max())
            if error > max_error:
                max_error = float(error)
                worst = {'frame':frame, 'name':name, 'error':max_error,
                         'source_center':expected.mean(axis=0).tolist(),
                         'runtime_center':points.mean(axis=0).tolist(), 'first_time':first}
        for obj in mouths:
            max_port = max(max_port, max(abs(obj.matrix_world[i][j]-port_matrices[obj.name][i][j])
                                        for i in range(4) for j in range(4)))
    assert max_error < 1e-5 and max_port < 1e-7, (worst, max_port)
    pose(1)
    sockets = []
    for obj in mouths:
        points = initial[obj.name]['points']
        sign = 1 if 'north' in obj.name else -1
        joint = points[np.abs(points[:,1]-sign*1.5) < 1e-5]
        assert len(joint) >= 64, (obj.name, points.min(axis=0), points.max(axis=0))
        center = np.array([0, sign*1.5, .36])
        radii = np.sqrt((joint[:,0]-center[0])**2+(joint[:,2]-center[2])**2)
        straight = points[np.abs(points[:,1]-sign*1.497) < 1e-5]
        full_radii = np.sqrt(straight[:,0]**2+(straight[:,2]-.36)**2)
        # Canonical template has a .003 edge bevel. Its nominal barrel bore
        # and collar diameter occur behind the arris, not on the joint plane.
        assert abs(full_radii.max()-.34) < 1e-5 and abs(full_radii.min()-.245) < 1e-5
        assert abs(radii.max()-.337) < 1e-5 and abs(radii.min()-.248) < 1e-5
        # Rejoin only coincident export seam vertices for topology inspection.
        import bmesh
        bm = bmesh.new()
        bm.from_mesh(obj.data)
        bmesh.ops.remove_doubles(bm, verts=list(bm.verts), dist=1e-6)
        assert all(edge.is_manifold for edge in bm.edges), obj.name
        todo = set(bm.verts)
        components = 0
        while todo:
            components += 1
            pending = [todo.pop()]
            while pending:
                for edge in pending.pop().link_edges:
                    for vertex in edge.verts:
                        if vertex in todo:
                            todo.remove(vertex)
                            pending.append(vertex)
        assert components == 1, (obj.name, components)
        bm.free()
        sockets.append({'name':obj.name, 'joint_center':center.tolist(),
                        'outer_diameter':float(full_radii.max()*2), 'bore_diameter':float(full_radii.min()*2),
                        'joint_edge_bevel_tiles':.003, 'joint_edge_outer_diameter':float(radii.max()*2),
                        'joint_edge_inner_diameter':float(radii.min()*2),
                        'closed_manifold_wall':True, 'connected_components':components})
    textured = []
    water = []
    for mat in gltf['materials']:
        pbr = mat.get('pbrMetallicRoughness', {})
        if 'baseColorTexture' in pbr:
            assert 'normalTexture' in mat and 'metallicRoughnessTexture' in pbr
            textured.append(mat['name'])
        else:
            assert 'water' in mat['name'] and mat.get('alphaMode') == 'BLEND', mat
            water.append(mat['name'])
    assert textured and len(water) == 1
    sys.path.insert(0, str(args.fmpl_tools.resolve()))
    from blender_camera_guard import install_canonical_camera, temporary_inspection_camera, assert_clean
    profile = json.loads((out/'capture-profile.json').read_text())
    install_canonical_camera(scene, profile, bpy)
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 48
    scene.cycles.use_denoising = False
    scene.render.film_transparent = True
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGBA'
    scene.view_settings.view_transform = 'AgX'
    scene.world = bpy.data.worlds.new('Pond actual export | neutral inspection')
    scene.world.use_nodes = True
    scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value = .35
    for pos, power in [((-3,-4,6),450), ((3,2,4),180)]:
        light = bpy.data.lights.new('Pond inspection area', 'AREA')
        light.energy, light.size = power, 4
        obj = bpy.data.objects.new(light.name, light)
        scene.collection.objects.link(obj)
        obj.location = pos
        obj.rotation_euler = (Vector((0,0,0))-obj.location).to_track_quat('-Z','Y').to_euler()
    root = bpy.data.objects.new('INSPECT | imported pond rotation', None)
    scene.collection.objects.link(root)
    for obj in list(scene.objects):
        if obj is not root and obj.parent is None and obj.type not in {'CAMERA','LIGHT'}:
            world = obj.matrix_world.copy()
            obj.parent = root
            obj.matrix_world = world
    images = []
    for label, yaw in [('front',0), ('rear',180), ('close',0), ('clay',0)]:
        root.rotation_euler.z = math.radians(yaw)
        pose(25)
        if label == 'clay':
            clay = bpy.data.materials.new('Pond neutral clay inspection')
            clay.use_nodes = True
            clay.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = (.45,.45,.45,1)
            for obj in scene.objects:
                if obj.type == 'MESH':
                    obj.data.materials.clear()
                    obj.data.materials.append(clay)
        if label == 'close':
            with temporary_inspection_camera(scene, bpy, 'pond-close') as camera:
                camera.data.type = 'ORTHO'
                camera.data.ortho_scale = 2.4
                target = Vector((0, -.3, 0))
                camera.location = target+Vector((0,-6,6))
                camera.rotation_euler = (target-camera.location).to_track_quat('-Z','Y').to_euler()
                scene.camera = camera
                path = out/('actual-glb-'+label+'.png')
                scene.render.filepath = str(path)
                bpy.ops.render.render(write_still=True)
        else:
            assert_clean(scene, profile, bpy)
            path = out/('actual-glb-'+label+'.png')
            scene.render.filepath = str(path)
            bpy.ops.render.render(write_still=True)
        images.append({'file':path.name, 'sha256':sha(path)})
    result = {'schema':'tanks.fish-pond.v2.runtime-inspection', 'technical_checks_passed':True,
        'visual_approved':False, 'game_integrated':False, 'source_sha256':sha(native), 'glb_sha256':sha(runtime),
        'source_geometry':source, 'runtime_geometry':imported, 'sampled_working_poses':97,
        'max_export_error_tiles':max_error, 'max_socket_motion_tiles':max_port,
        'source_loop_seam_error_tiles':source_seam, 'sockets':sockets, 'packed_source_images':packed,
        'embedded_runtime_images':len(gltf.get('images',[])), 'textured_materials':textured,
        'water_uniform_alpha_material':water, 'runtime_renders':images,
        'idle_state_note':'Source/render visibility state; GLB exports the working loop. Consumers hide fish and eye nodes for idle.'}
    (out/'runtime-inspection.json').write_text(json.dumps(result, indent=2)+'\n')
    print('FISH_POND_ACTUAL_EXPORT_INSPECTED', json.dumps(result), flush=True)


if __name__ == '__main__':
    main()
