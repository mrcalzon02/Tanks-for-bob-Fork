"""Extract the verified Cooking Fire V2 joint into a standalone Blender asset.

Run from the repository root:
  blender --background --python models/reference/factorio-fluid-interface/build_reference.py -- \
    --source models/island-survival/cooking-fire/v2/cooking-fire-v2.blend \
    --output models/reference/factorio-fluid-interface

This builder starts a new file. It never writes to the machine source.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import struct
import sys

import bpy
from mathutils import Matrix, Vector

STANDARD_ID = 'factorio-fluid-interface-v1'
ASSET_COLLECTION = 'FACTORIO_FLUID_INTERFACE_REFERENCE'
SOURCE_SHA256 = '6d95ba48a586956170dac4d9f37322068f66e25967f55eb54aed222933f2e675'
SOURCE_COMMIT = '807d024e74507d60fbdc04d17cd4738a02eaf225'
SOURCE_REPO_PATH = 'models/island-survival/cooking-fire/v2/cooking-fire-v2.blend'
DIMENSIONS = dict(units_per_tile=1.0, barrel_od=0.57, bore_id=0.49,
                  collar_od=0.68, collar_depth=0.075, centre_height=0.36,
                  adjacent_barrel_length=1.0)
SOURCES = {
    'reference_barrel': 'REFERENCE | one-tile pipe barrel',
    'reference_near_collar': 'REFERENCE | near pipe collar',
    'reference_far_collar': 'REFERENCE | far pipe collar',
    'machine_collar': 'Pump box | standard mounting collar',
    'machine_throat': 'Pump box | full-size throat',
}
NAMES = {
    'reference_barrel': 'IFACE | adjacent pipe barrel',
    'reference_near_collar': 'IFACE | adjacent near collar',
    'reference_far_collar': 'IFACE | adjacent far collar',
    'machine_collar': 'IFACE | machine collar template',
    'machine_throat': 'IFACE | machine throat template',
}


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def geometry_digest(obj):
    h = hashlib.sha256()
    for v in obj.data.vertices:
        h.update(struct.pack('<3f', *v.co))
    for face in obj.data.polygons:
        h.update(struct.pack('<I', len(face.vertices)))
        h.update(struct.pack('<' + 'I' * len(face.vertices), *face.vertices))
    return h.hexdigest()


def collection(name, parent):
    result = bpy.data.collections.new(name)
    parent.children.link(result)
    return result


def material(name, colour, metallic=0, roughness=.6, emission=0):
    result = bpy.data.materials.new(name)
    result.diffuse_color = (*colour, 1)
    result.use_nodes = True
    shader = result.node_tree.nodes.get('Principled BSDF')
    shader.inputs['Base Color'].default_value = (*colour, 1)
    shader.inputs['Metallic'].default_value = metallic
    shader.inputs['Roughness'].default_value = roughness
    if emission:
        shader.inputs['Emission Color'].default_value = (*colour, 1)
        shader.inputs['Emission Strength'].default_value = emission
    return result


def empty(name, role, parent, coll, location, display='PLAIN_AXES', size=.12):
    obj = bpy.data.objects.new(name, None)
    coll.objects.link(obj)
    obj.parent = parent
    obj.location = location
    obj.empty_display_type = display
    obj.empty_display_size = size
    obj.show_in_front = True
    obj['interface_role'] = role
    obj['standard_id'] = STANDARD_ID
    return obj


def line(name, points, coll, mat, radius=.006):
    data = bpy.data.curves.new(name, 'CURVE')
    data.dimensions = '3D'
    data.bevel_depth = radius
    data.bevel_resolution = 2
    spline = data.splines.new('POLY')
    spline.points.add(len(points)-1)
    for point, coordinate in zip(spline.points, points):
        point.co = (*coordinate, 1)
    obj = bpy.data.objects.new(name, data)
    coll.objects.link(obj)
    data.materials.append(mat)
    return obj


def plane(name, corners, coll, mat):
    data = bpy.data.meshes.new(name)
    data.from_pydata(corners, [], [(0, 1, 2, 3)])
    data.update()
    obj = bpy.data.objects.new(name, data)
    coll.objects.link(obj)
    data.materials.append(mat)
    return obj


def camera_setup(scene, coll, target=(0, .35, .12), scale=3.9,
                 resolution=(1500, 1050)):
    data = bpy.data.cameras.new('Reference | fixed 45 degree camera')
    camera = bpy.data.objects.new(data.name, data)
    coll.objects.link(camera)
    target = Vector(target)
    # Horizontal distance equals vertical distance: exactly 45 degrees.
    camera.location = target + Vector((4.8, 6.4, 8.0))
    camera.rotation_euler = (target-camera.location).to_track_quat('-Z', 'Y').to_euler()
    data.type = 'ORTHO'
    data.ortho_scale = scale
    scene.camera = camera
    scene.render.resolution_x, scene.render.resolution_y = resolution
    scene.render.resolution_percentage = 100
    return camera


def billboard(name, body, camera, coll, mat, xy, size=.09):
    data = bpy.data.curves.new(name, 'FONT')
    data.body = body
    data.size = size
    data.space_line = 1.2
    data.align_y = 'TOP_BASELINE'
    obj = bpy.data.objects.new(name, data)
    coll.objects.link(obj)
    obj.rotation_euler = camera.rotation_euler
    obj.location = camera.location + camera.rotation_euler.to_quaternion() @ Vector((xy[0], xy[1], -7))
    data.materials.append(mat)
    return obj


def setup_render(scene, coll):
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 64
    # Portable to Blender builds without OpenImageDenoise.
    scene.cycles.use_denoising = False
    scene.cycles.seed = 1109
    scene.render.threads_mode = 'FIXED'
    scene.render.threads = 4
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGBA'
    scene.render.film_transparent = False
    scene.view_settings.view_transform = 'AgX'
    world = bpy.data.worlds.new('Reference | studio world')
    world.use_nodes = True
    world.node_tree.nodes['Background'].inputs['Color'].default_value = (.065, .085, .11, 1)
    world.node_tree.nodes['Background'].inputs['Strength'].default_value = .25
    scene.world = world
    for name, position, power, size in (
        ('key', (0, 1, 5), 300, 5),
        ('fill', (-3, -2, 3), 180, 4),
        ('rim', (2, 3, 2), 150, 3),
    ):
        data = bpy.data.lights.new('Reference | ' + name, 'AREA')
        data.energy, data.shape, data.size = power, 'DISK', size
        obj = bpy.data.objects.new(data.name, data)
        coll.objects.link(obj)
        obj.location = position
        obj.rotation_euler = (Vector((0, .35, .3))-obj.location).to_track_quat('-Z', 'Y').to_euler()


def verify_native(scene, asset, source_records):
    roles = {obj['interface_role']: obj for obj in asset.all_objects}
    root = roles['placement_root']
    assert len(asset.all_objects) == 9
    assert len([o for o in asset.all_objects if o.type == 'MESH']) == 5
    assert all(o.type in {'MESH', 'EMPTY'} for o in asset.all_objects)
    assert root.parent is None and tuple(root.scale) == (1.0, 1.0, 1.0)
    assert (root.location-Vector((0, 0, 0))).length < 1e-7
    assert all(o.parent == root for o in asset.all_objects if o != root)
    assert all(tuple(o.scale) == (1.0, 1.0, 1.0) for o in asset.all_objects)
    assert not bpy.data.actions and not bpy.data.images and not bpy.data.libraries
    assert not any(o.animation_data for o in bpy.data.objects)
    for role, record in source_records.items():
        assert geometry_digest(roles[role]) == record['canonical_mesh_sha256']
    def mating_face(role):
        return [o.matrix_world @ v.co for o in [roles[role]]
                for v in o.data.vertices if abs(v.co.y) < 1e-6]
    machine, pipe = mating_face('machine_collar'), mating_face('reference_near_collar')
    assert len(machine) == len(pipe) == 128
    residual = max(min((a-b).length for b in pipe) for a in machine)
    assert residual < 1e-6
    bounds = {}
    for role in SOURCES:
        obj = roles[role]
        coords = [obj.matrix_world @ v.co for v in obj.data.vertices]
        bounds[role] = {'min': [min(v[i] for v in coords) for i in range(3)],
                        'max': [max(v[i] for v in coords) for i in range(3)]}
    for role, radius, span in (
        ('reference_barrel', .285, (0, 1)),
        ('reference_near_collar', .34, (0, .075)),
        ('reference_far_collar', .34, (.925, 1)),
        ('machine_collar', .34, (-.075, 0)),
        ('machine_throat', .285, (-.29, 0)),
    ):
        b = bounds[role]
        expected_min, expected_max = (-radius, span[0], .36-radius), (radius, span[1], .36+radius)
        assert max(abs(a-b) for a, b in zip(b['min'], expected_min)) < 1e-6
        assert max(abs(a-b) for a, b in zip(b['max'], expected_max)) < 1e-6
        radii = [math.hypot(v.co.x, v.co.z-.36) for v in roles[role].data.vertices]
        assert abs(min(radii)-.245) < 1e-6
        assert abs(max(radii)-radius) < 1e-6
    return {'saved_native_reopened': True, 'reference_meshes': 5,
            'fixture_objects': len(asset.all_objects), 'mating_vertices': 128,
            'max_mating_error_tiles': residual, 'tolerance_tiles': 1e-6,
            'unit_scales': True, 'no_animation_or_external_dependencies': True,
            'mesh_bounds': bounds}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--no-render', action='store_true')
    args = parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    source, out = args.source.resolve(), args.output.resolve()
    assert sha256(source) == SOURCE_SHA256, 'Expected exact committed Cooking Fire V2 source'
    out.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.name = 'FLUID INTERFACE | reusable modeling environment'
    scene.unit_settings.system = 'NONE'
    scene.unit_settings.scale_length = 1.0
    scene['standard_id'] = STANDARD_ID
    scene['units'] = 'One Blender unit equals one Factorio tile'
    scene['guide'] = 'docs/art/FLUID_CONNECTION_MODELING_GUIDE.md'
    asset = collection(ASSET_COLLECTION, scene.collection)
    asset['standard_id'] = STANDARD_ID
    asset['usage'] = 'Append this collection; move root to joint ground projection; do not scale.'
    asset.asset_mark()
    asset.asset_data.description = 'Standard pipe interface: 0.57 barrel / 0.49 bore / 0.68 collar, centre Z0.36; one tile per unit.'
    for tag in ('Factorio', 'pipe', 'modeling reference', 'fluid interface'):
        asset.asset_data.tags.new(tag)
    pipes = collection('IFACE | reference pipe only', asset)
    templates = collection('IFACE | machine mount templates', asset)
    markers = collection('IFACE | placement markers', asset)
    root = empty('IFACE | ground placement root', 'placement_root', None, asset, (0, 0, 0), 'ARROWS', .25)
    root.lock_scale = (True, True, True)
    root['joint_height'] = .36
    root['outward_local_axis'] = '+Y'
    root['direction_yaw_degrees'] = 'N0; E-90; S180; W90'
    for key, value in DIMENSIONS.items():
        root[key] = value
    with bpy.data.libraries.load(str(source), link=False) as (available, loaded):
        assert all(name in available.objects for name in SOURCES.values())
        loaded.objects = list(SOURCES.values())
    guide_mat = material('Reference | amber machine-side template', (.48, .23, .055), .45, .36)
    source_records = {}
    for role, obj in zip(SOURCES, loaded.objects):
        # The source uses vertices in machine coordinates and an identity export
        # pivot. Only the origin changes; topology and dimensions are preserved.
        assert max(abs(obj.matrix_world[i][j]-(1 if i == j else 0))
                   for i in range(4) for j in range(4)) < 1e-7
        source_mesh = geometry_digest(obj)
        before = [v.co.copy() for v in obj.data.vertices]
        obj.parent = None
        obj.matrix_world = Matrix.Identity(4)
        obj.data = obj.data.copy()
        obj.data.transform(Matrix.Translation((0, -1.5, 0)))
        obj.data.update()
        error = max((v.co-(old-Vector((0, 1.5, 0)))).length
                    for v, old in zip(obj.data.vertices, before))
        assert error < 1e-7
        obj.name = NAMES[role]
        obj.data.name = NAMES[role] + ' | mesh'
        obj.animation_data_clear()
        obj.parent = root
        obj.matrix_parent_inverse = Matrix.Identity(4)
        obj['interface_role'] = role
        obj['standard_id'] = STANDARD_ID
        obj['source_object'] = SOURCES[role]
        obj['usage'] = 'Reference only; duplicate machine template into authored machine collection before production.'
        obj.hide_render = False
        obj.hide_viewport = False
        (templates if role.startswith('machine_') else pipes).objects.link(obj)
        if role.startswith('machine_'):
            obj.data.materials.clear()
            obj.data.materials.append(guide_mat)
        source_records[role] = dict(source_object=SOURCES[role], source_mesh_sha256=source_mesh,
            canonical_mesh_sha256=geometry_digest(obj), vertices=len(obj.data.vertices),
            faces=len(obj.data.polygons), translation_only_error_tiles=error,
            modifiers=[{'type':m.type, 'width':m.width, 'segments':m.segments}
                       for m in obj.modifiers if m.type == 'BEVEL'])
    # Drop any source parent pulled in as a library dependency.
    for obj in list(bpy.data.objects):
        if obj.name not in asset.all_objects:
            bpy.data.objects.remove(obj, do_unlink=True)
    empty('IFACE | socket centre +Y outward', 'socket_marker', root, markers, (0, 0, .36), 'ARROWS', .24)
    empty('IFACE | machine pipe-cell centre', 'machine_cell_marker', root, markers, (0, -.5, 0), 'CUBE', .08)
    empty('IFACE | adjacent pipe-cell centre', 'adjacent_cell_marker', root, markers, (0, .5, 0), 'CUBE', .08)
    environment = collection('REVIEW ENVIRONMENT | do not append', scene.collection)
    floor = material('Reference | slate floor', (.012, .021, .032))
    grid = material('Reference | tile grid', (.045, .075, .10), emission=.1)
    white = material('Reference | labels', (.80, .89, .94), emission=1)
    amber = material('Reference | seam and dimensions', (.95, .42, .075), emission=.7)
    teal = material('Reference | pipe-side marker', (.09, .7, .67), emission=.5)
    plane('Reference | ground', [(-20, -20, -.016), (20, -20, -.016),
          (20, 20, -.016), (-20, 20, -.016)], environment, floor)
    for i in range(-2, 3):
        line('Reference | one-tile grid X ' + str(i), [(i, -2, -.008), (i, 3, -.008)], environment, grid, .003)
    for i in range(-2, 4):
        line('Reference | one-tile grid Y ' + str(i), [(-2, i, -.008), (2, i, -.008)], environment, grid, .003)
    line('Reference | joint ground line Y0', [(-.62, 0, .004), (.62, 0, .004)], environment, amber, .009)
    line('Reference | ground origin cross', [(0, -.15, .006), (0, .15, .006)], environment, amber, .009)
    # Renderable annular outline highlights the actual joint without changing it.
    circle = [(.353*math.cos(i*math.tau/96), 0, .36+.353*math.sin(i*math.tau/96)) for i in range(97)]
    line('Reference | mating plane outline Y0', circle, environment, amber, .005)
    line('Reference | one-tile dimension', [(.49, 0, .02), (.49, 1, .02)], environment, teal, .007)
    for y in (0, 1):
        line('Reference | pipe dimension tick', [(.43, y, .02), (.55, y, .02)], environment, teal, .007)
    line('Reference | centre height dimension', [(-.48, 0, .01), (-.48, 0, .36)], environment, amber, .006)
    for z in (0, .36):
        line('Reference | height dimension tick', [(-.54, 0, z+.01), (-.42, 0, z+.01)], environment, amber, .006)
    camera = camera_setup(scene, environment)
    setup_render(scene, environment)
    billboard('Reference | title', 'STANDARD FLUID INTERFACE', camera, environment, white, (-1.76, 1.13), .115)
    billboard('Reference | subtitle', 'Reusable pipe + machine mount  /  1 Blender unit = 1 tile', camera, environment, white, (-1.76, .95), .052)
    billboard('Reference | machine legend', 'AMBER\nMachine-side collar + throat template', camera, environment, amber, (-1.76, -.78), .061)
    billboard('Reference | pipe legend', 'IRON\nAdjacent pipe: 1.00 tile long', camera, environment, white, (.25, -.78), .061)
    billboard('Reference | dimensions', 'Barrel OD 0.57   |   Bore ID 0.49   |   Collar OD 0.68 x 0.075\nJoint: local Y0   |   Centre Z0.36   |   Ground root (0, 0, 0)', camera, environment, white, (-1.76, -1.03), .054)
    text = bpy.data.texts.new('START HERE | fluid interface reference')
    text.use_fake_user = True
    text.write('STANDARD: '+STANDARD_ID+'\n\nAppend collection '+ASSET_COLLECTION+
        '\nSelect IFACE | ground placement root. Put it on the ground at the machine/pipe boundary.'
        '\nLocal +Y faces out. Rotate N0 / E-90 / S180 / W90. Keep scale (1,1,1).'
        '\nSocket height .36; barrel OD .57; bore ID .49; collar OD .68; collar depth .075.'
        '\nAmber objects are machine-side templates. Copy needed parts into the machine collection.'
        '\nHide the reference fixture and environment for production sprite rendering.'
        '\nModel fit is separate from per-machine native sprite registration.'
        '\n\nFull guide: docs/art/FLUID_CONNECTION_MODELING_GUIDE.md'
        '\nHelper: models/reference/factorio-fluid-interface/append_reference.py\n')
    for action in list(bpy.data.actions):
        bpy.data.actions.remove(action)
    bpy.data.orphans_purge(do_recursive=True)
    for obj in scene.objects:
        obj.select_set(False)
    root.select_set(True)
    bpy.context.view_layer.objects.active = root
    bpy.context.view_layer.update()
    for screen in bpy.data.screens:
        for area in screen.areas:
            if area.type == 'VIEW_3D':
                area.spaces.active.region_3d.view_perspective = 'CAMERA'
                area.spaces.active.overlay.show_extras = True
                area.spaces.active.clip_end = 100
    native = out / 'factorio-fluid-interface-reference.blend'
    bpy.ops.wm.save_as_mainfile(filepath=str(native), check_existing=False, compress=True)
    bpy.ops.wm.open_mainfile(filepath=str(native))
    scene = bpy.context.scene
    verification = verify_native(scene, bpy.data.collections[ASSET_COLLECTION], source_records)
    manifest = dict(standard_id=STANDARD_ID, schema_version=1,
        asset_collection=ASSET_COLLECTION, root_name='IFACE | ground placement root',
        environment_collection='REVIEW ENVIRONMENT | do not append',
        native_file=native.name, native_sha256=sha256(native), blender=bpy.app.version_string,
        dimensions=DIMENSIONS,
        coordinate_contract=dict(root=[0,0,0], joint=[0,0,.36], joint_plane='Y0',
            outward_axis='+Y', blender_to_native_ground='(x,y) -> (x,-y)',
            native_facing_yaw_degrees=dict(N=0,E=-90,S=180,W=90)),
        source=dict(repository='mrcalzon02/Tanks-for-bob-Fork', commit=SOURCE_COMMIT,
            path=SOURCE_REPO_PATH, sha256=SOURCE_SHA256,
            original_dimensional_authority='mrcalzon02/Tech-Priests@0ea7ed22d508fb2f5c7d71102679b0be80a379ab:art/source-to-3d/boiler-v05/build_boiler_v05.py'),
        geometry=source_records, verification=verification,
        camera=dict(type='ORTHO',elevation_degrees=45),
        production_policy='Reference fixture/environment excluded; copy authored machine fitting into machine collection.',
        native_game_registration='Not performed by this reusable modeling-reference task.')
    if not args.no_render:
        scene.render.filepath = str(out/'reference-overview.png')
        bpy.ops.render.render(write_still=True)
        manifest['preview'] = dict(file='reference-overview.png', sha256=sha256(out/'reference-overview.png'))
    (out/'reference-manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    print('REFERENCE_BUILT', json.dumps(dict(native=str(native), sha256=manifest['native_sha256'], verification=verification)), flush=True)


if __name__ == '__main__':
    main()
