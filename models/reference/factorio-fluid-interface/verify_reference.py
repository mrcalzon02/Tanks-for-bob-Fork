"""Verify real appending and mating geometry in fresh Blender machine scenes.

  blender --background --python-exit-code 1 --python verify_reference.py -- \
    --reference factorio-fluid-interface-reference.blend \
    --output append-verification.json

This focused check resets the current Blender file. Use it in a separate
background process, never in an unsaved modeling session.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import sys
import tempfile

import bpy
from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parent))
from append_reference import append_interface, EXPECTED_ROLES, STANDARD_ID

TOLERANCE = 1e-6
OUTWARD = {'N': Vector((0, 1, 0)), 'E': Vector((1, 0, 0)),
           'S': Vector((0, -1, 0)), 'W': Vector((-1, 0, 0))}


def close(actual, expected):
    error = (Vector(actual)-Vector(expected)).length
    assert error < TOLERANCE, (tuple(actual), tuple(expected), error)
    return error


def verify_case(collection, root, joint, facing):
    objects = list(collection.all_objects)
    roles = {obj.get('interface_role'): obj for obj in objects}
    assert len(objects) == 9 and set(roles) == EXPECTED_ROLES
    assert len([obj for obj in objects if obj.type == 'MESH']) == 5
    assert len([obj for obj in objects if obj.type == 'EMPTY']) == 4
    assert all(obj.library is None for obj in objects)
    assert all(obj == root or obj.parent == root for obj in objects)
    assert root.parent is None
    assert all(close(obj.scale, (1, 1, 1)) < TOLERANCE for obj in objects)
    assert all(obj.get('standard_id') == STANDARD_ID for obj in objects)
    close(root.matrix_world.translation, joint)
    outward = OUTWARD[facing]
    joint = Vector(joint)
    socket = joint + Vector((0, 0, .36))
    close(roles['socket_marker'].matrix_world.translation, socket)
    close(roles['machine_cell_marker'].matrix_world.translation, joint-outward*.5)
    close(roles['adjacent_cell_marker'].matrix_world.translation, joint+outward*.5)
    close(root.matrix_world.to_3x3() @ Vector((0, 1, 0)), outward)

    def mating_face(role):
        obj = roles[role]
        vertices = [obj.matrix_world @ v.co for v in obj.data.vertices if abs(v.co.y) < TOLERANCE]
        normals = [obj.matrix_world.to_3x3() @ poly.normal for poly in obj.data.polygons
                   if all(abs(obj.data.vertices[index].co.y) < TOLERANCE for index in poly.vertices)]
        return vertices, normals

    machine_face, machine_normals = mating_face('machine_collar')
    pipe_face, pipe_normals = mating_face('reference_near_collar')
    assert len(machine_face) == len(pipe_face) == 128
    assert len(machine_normals) == len(pipe_normals) == 64
    residual = max(min((a-b).length for b in pipe_face) for a in machine_face)
    assert residual < TOLERANCE
    assert all(normal.dot(outward) > 1-TOLERANCE for normal in machine_normals)
    assert all(normal.dot(outward) < -1+TOLERANCE for normal in pipe_normals)
    for vertex in machine_face+pipe_face:
        assert abs((vertex-socket).dot(outward)) < TOLERANCE

    # Verify diameters, bore and axial spans after actual world placement.
    for role, radius, span in (
        ('reference_barrel', .285, (0, 1)),
        ('reference_near_collar', .34, (0, .075)),
        ('reference_far_collar', .34, (.925, 1)),
        ('machine_collar', .34, (-.075, 0)),
        ('machine_throat', .285, (-.29, 0)),
    ):
        obj = roles[role]
        points = [obj.matrix_world @ vertex.co for vertex in obj.data.vertices]
        axial = [(p-socket).dot(outward) for p in points]
        radial = [(p-socket-outward*(p-socket).dot(outward)).length for p in points]
        assert abs(min(axial)-span[0]) < TOLERANCE
        assert abs(max(axial)-span[1]) < TOLERANCE
        assert abs(min(radial)-.245) < TOLERANCE
        assert abs(max(radial)-radius) < TOLERANCE
    return dict(facing=facing, joint_ground=list(joint), socket=list(socket),
                adjacent_pipe_cell=list(joint+outward*.5), object_count=len(objects),
                mesh_count=5, local_editable=True, unit_scales=True,
                opposed_face_normals=True, mating_face_vertices=128,
                max_mating_error_tiles=residual, dimensions_verified=True)


def sentinel(scene):
    data = bpy.data.meshes.new('Existing machine sentinel mesh')
    data.from_pydata([(0, 0, 0), (1, 0, 0), (0, 1, 0)], [], [(0, 1, 2)])
    obj = bpy.data.objects.new('Existing machine sentinel', data)
    scene.collection.objects.link(obj)
    obj.location = (9, 8, 7)
    obj['existing_machine_data'] = 'Must survive append unchanged'
    return obj


def assert_sentinel(scene):
    obj = scene.objects['Existing machine sentinel']
    close(obj.location, (9, 8, 7))
    assert obj['existing_machine_data'] == 'Must survive append unchanged'
    assert [list(v.co) for v in obj.data.vertices] == [[0, 0, 0], [1, 0, 0], [0, 1, 0]]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--reference', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    reference = args.reference.resolve()
    native_sha = hashlib.sha256(reference.read_bytes()).hexdigest()
    results = []
    cases = (
        ('3x3 cardinal boundaries', [('N', (0, 1.5, 0)), ('E', (1.5, 0, 0)),
                                    ('S', (0, -1.5, 0)), ('W', (-1.5, 0, 0))]),
        ('2x2 east rear-row boundary', [('E', (1, .5, 0))]),
    )
    with tempfile.TemporaryDirectory(prefix='fluid-reference-verify-') as temporary:
        for index, (label, placements) in enumerate(cases):
            bpy.ops.wm.read_factory_settings(use_empty=True)
            scene = bpy.context.scene
            existing = sentinel(scene)
            appended = []
            for case_index, (facing, joint) in enumerate(placements):
                before = set(bpy.data.objects)
                collection, root = append_interface(reference, joint_ground=joint,
                    facing=facing, name=f'Verification port {case_index}', scene=scene)
                bpy.context.view_layer.update()
                added = set(bpy.data.objects)-before
                assert added == set(collection.all_objects)
                assert len(added) == 9
                assert not any(obj.type in {'CAMERA', 'LIGHT', 'FONT'} for obj in added)
                assert not bpy.data.cameras and not bpy.data.lights
                # Blender can retain a Library bookkeeping entry after a local
                # append. Actual used IDs must all remain local and editable.
                assert not any(item.library is not None
                    for group in ('objects', 'collections', 'meshes', 'curves',
                                  'materials', 'node_groups', 'images')
                    for item in getattr(bpy.data, group))
                assert existing in scene.objects.values()
                assert_sentinel(scene)
                result = verify_case(collection, root, joint, facing)
                result['collection'] = collection.name
                result['root'] = root.name
                appended.append(result)
            assert len({r['root'] for r in appended}) == len(placements)
            assert len(scene.objects) == 1 + len(placements)*9
            # Reopening proves local ownership and saved parent transforms.
            native_test = str(Path(temporary)/f'append-test-{index}.blend')
            bpy.ops.wm.save_as_mainfile(filepath=native_test, check_existing=False, compress=True)
            bpy.ops.wm.open_mainfile(filepath=native_test)
            scene = bpy.context.scene
            bpy.context.view_layer.update()
            assert_sentinel(scene)
            for result in appended:
                collection = bpy.data.collections[result['collection']]
                root = bpy.data.objects[result['root']]
                reopened = verify_case(collection, root, result['joint_ground'], result['facing'])
                result['reopened_max_mating_error_tiles'] = reopened['max_mating_error_tiles']
            results.append(dict(scenario=label, fresh_scene=True, saved_reopened=True,
                original_machine_sentinel_preserved=True, unwanted_objects_imported=0,
                independent_appended_roots=True, placements=appended))
    assert hashlib.sha256(reference.read_bytes()).hexdigest() == native_sha
    receipt = dict(standard_id=STANDARD_ID, native_sha256=native_sha,
        blender=bpy.app.version_string, status='passed', tolerance_tiles=TOLERANCE,
        total_appended_assemblies=sum(len(s['placements']) for s in results),
        source_file_unchanged=True, scenarios=results)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(receipt, indent=2)+'\n')
    print('REFERENCE_APPEND_VERIFIED', json.dumps(receipt))


if __name__ == '__main__':
    main()
