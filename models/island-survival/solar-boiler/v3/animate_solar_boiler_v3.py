#!/usr/bin/env python3
"""Solar Boiler V3 -- physically located cyclic pressure, red heat and joint steam.

Derive the HASH-VERIFIED Solar Boiler V2 Blender source. Preserve the calibrated
3x2 footprint, three native Factorio fluid mouths, optical concentrators, four
permanently coupled thermal lines, packed FMPL PBR maps and single 45-degree
camera. Add keyed, editable geometry/materials; never change live sprites.

One 16-pose working loop sampled frames 1,7,...91 with frame 97 == frame 1,
plus frame 0 idle. Genuine Blender/Cycles views for all four model rotations.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
from pathlib import Path
import struct
import sys

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / 'generated-v2' / 'solar-boiler-v2.blend'
REPORT = HERE.parent / 'generated-v2' / 'build-report.json'
FRAMES = tuple(range(1, 92, 6))
LOOP_END = 97
DIRECTIONS = (0, 90, 180, 270)
ENDPOINTS = ('west-hot-union', 'east-hot-union', 'steam-extraction-neck', 'steam-output-flange')


def digest(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def gauge_degrees(index):
    """Cyclic mechanical gauge needle twitch; index 0 and 16 are identical."""
    angle = 25 * math.sin(math.tau * 2 * index / 16)
    angle += 6 * math.sin(math.tau * 5 * index / 16)
    return angle


def heat_strength(index):
    """Heat reservoir varies from a visible ember to the full operational red."""
    return 0.12 + 1.50 * (0.5 + 0.5 * math.sin(math.tau * index / 16))


def puff_state(index, phase, emitter):
    age = ((index - phase) % 16) / 16.0
    drift = (0.026 * math.sin(math.tau * age + emitter * 1.3),
             0.024 * math.cos(math.tau * age + emitter * 0.8),
             0.13 * age)
    radius = 0.026 + 0.067 * age
    return drift, radius, age


def self_check():
    assert len(FRAMES) == 16 and FRAMES == tuple(range(1, 92, 6))
    assert abs(gauge_degrees(0) - gauge_degrees(16)) < 1e-10
    assert abs(heat_strength(0) - heat_strength(16)) < 1e-10
    assert max(gauge_degrees(i) for i in range(16)) - min(gauge_degrees(i) for i in range(16)) > 45
    assert min(heat_strength(i) for i in range(16)) >= 0.11999
    assert max(heat_strength(i) for i in range(16)) > 1.61999
    for emitter in range(4):
        for phase in (0, 4, 8, 12):
            assert puff_state(0, phase, emitter) == puff_state(16, phase, emitter)
    source = json.loads(REPORT.read_text())
    assert source['native_footprint_tiles'] == [3, 2]
    assert source['parabolic_concentrators'] == 2
    assert source['stationary_collector_and_continuous_thermal_lines'] is True
    print('SOLAR_V3_WORKING_CYCLE_MATH_PASS', flush=True)


def mesh_fingerprint(ob):
    h = hashlib.sha256()
    for v in ob.data.vertices:
        h.update(struct.pack('<3f', *v.co))
    for poly in ob.data.polygons:
        h.update(struct.pack('<I', len(poly.vertices)))
        for index in poly.vertices:
            h.update(struct.pack('<I', index))
    return h.hexdigest()


def emissive_copper(bpy):
    mat = bpy.data.materials.new('Solar Boiler V3 | thermal accumulator variable red emission')
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    shader = nodes.get('Principled BSDF')
    shader.inputs['Base Color'].default_value = (0.11, 0.025, 0.011, 1)
    shader.inputs['Metallic'].default_value = .48
    shader.inputs['Roughness'].default_value = .38
    shader.inputs['Emission Color'].default_value = (1, .035, .012, 1)
    socket = shader.inputs['Emission Strength']
    for f, val in [(0, 0)] + [(frame, heat_strength(i)) for i, frame in enumerate(FRAMES)] + [(97, heat_strength(0))]:
        socket.default_value = float(val)
        socket.keyframe_insert(data_path='default_value', frame=f)
    socket.default_value = 0.0
    mat['role'] = 'Central pressure-drum thermal accumulator; red emissive Cycles surface'
    return mat, socket


def vapor_material(bpy):
    mat = bpy.data.materials.new('Solar Boiler V3 | translucent joint-pressure vapor')
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    links = mat.node_tree.links
    output = nodes.new('ShaderNodeOutputMaterial')
    transparent = nodes.new('ShaderNodeBsdfTransparent')
    tinted = nodes.new('ShaderNodeBsdfPrincipled')
    tinted.inputs['Base Color'].default_value = (.81, .87, .89, 1)
    tinted.inputs['Roughness'].default_value = .95
    mix = nodes.new('ShaderNodeMixShader')
    mix.inputs[0].default_value = .33
    links.new(transparent.outputs[0], mix.inputs[1])
    links.new(tinted.outputs['BSDF'], mix.inputs[2])
    links.new(mix.outputs[0], output.inputs['Surface'])
    mat['role'] = 'True visible but partially transparent steam at specific high-pressure joints'
    return mat


def keyframe_linear(item, frame, path):
    item.keyframe_insert(data_path=path, frame=int(frame))
    action = getattr(getattr(item, 'animation_data', None), 'action', None)
    curves = getattr(action, 'fcurves', None) or []
    for curve in curves:
        for key in curve.keyframe_points:
            key.interpolation = 'LINEAR'


def add_needle(bpy, base, root, collection, mats):
    # Keep the historical needle untouched as source, but render-hide it to
    # avoid drawing two pointers. New pivot is exactly at the original dial.
    original = bpy.data.objects['GAUGE | live pressure needle']
    original.hide_render = True
    original['solar_v3_superseded_render_only'] = 'Pivoted pressure indicator'
    pivot = bpy.data.objects.new('GAUGE V3 | real face-center needle pivot', None)
    collection.objects.link(pivot)
    pivot.parent = root
    pivot.location = (0, -.563, .94)
    pivot['role'] = 'mechanical face-normal pivot, not off-axis rod rotation'
    base.rod(bpy, 'GAUGE V3 | crimson actual oscillating needle',
             (0, 0, 0), (.122, 0, .033), .018,
             mats['aged_iron'], collection, pivot)
    base.sphere(bpy, 'GAUGE V3 | readable crimson needle tip',
             (.119, 0, .033), (.017, .018, .017),
             mats['needle'], collection, pivot)
    base.cyl(bpy, 'GAUGE V3 | bronze pointer arbor', (0, 0, 0), .025, .028,
             mats['bronze'], collection, pivot, rotation=(math.pi / 2, 0, 0), segments=24)
    for frame, degrees in [(0, 0.0)] + [(fr, gauge_degrees(i)) for i, fr in enumerate(FRAMES)] + [(LOOP_END, gauge_degrees(0))]:
        pivot.rotation_euler.y = math.radians(degrees)
        keyframe_linear(pivot, frame, 'rotation_euler')
    return pivot


def add_accumulator(bpy, base, root, collection, mats):
    material, socket = emissive_copper(bpy)
    # A 0.48-tile axial jacket on the real central copper accumulator drum:
    # visible curved *shell* plus non-glowing retaining bands, not a floating
    # red sprite or an additional imaginary pressure chamber.
    shell = base.annulus(bpy,
        'ACCUMULATOR V3 | red-hot cylindrical pressure drum jacket',
        (0, -.10, .77), (1, 0, 0), .378, .369, .49,
        material, collection, root, segments=72)
    shell['pressure_source'] = 'PROCESS | horizontal copper steam drum'
    shell['mean_radius_bu'] = .3735
    shell['render_isolation_group'] = 'accumulator_heat'
    for x in (-.26, .26):
        base.annulus(bpy, 'ACCUMULATOR V3 | real retaining band',
                     (x, -.10, .77), (1, 0, 0), .397, .366, .040,
                     mats['aged_iron'], collection, root, segments=72)
    # A low-area real Cycles heat source conveys nearby red flicker at 64px.
    lamp_data = bpy.data.lights.new('ACCUMULATOR V3 | localized hot red glow', 'POINT')
    lamp_data.color = (1.0, .045, .016)
    lamp_data.shadow_soft_size = .22
    lamp = bpy.data.objects.new('ACCUMULATOR V3 | localized thermal radiation', lamp_data)
    collection.objects.link(lamp)
    lamp.parent = root
    lamp.location = (0, -.30, .75)
    for frame, val in [(0, 0.0)] + [(f, heat_strength(i)*1.8) for i, f in enumerate(FRAMES)] + [(LOOP_END, heat_strength(0)*1.8)]:
        lamp_data.energy = float(val)
        keyframe_linear(lamp_data, frame, 'energy')
    return shell, material, socket, lamp


def joint_positions(bpy, source_report):
    positions = {}
    for label in ('west', 'east'):
        endpoint = source_report['solar_thermal_endpoints'][label]['hot_drum']
        # The hot union is the actual collector-to-drum pressurized junction.
        prefix = f'CONCENTRATOR | {label} | hot collector outlet to drum |'
        matches = [o for o in bpy.data.objects if o.type == 'MESH' and o.name.startswith(prefix)]
        assert len(matches) == 1, (label, [o.name for o in matches])
        collar = matches[0]
        positions[label + '-hot-union'] = (endpoint, collar.name)
    outlet = bpy.data.objects['PORT | steam-north | full machine collar']
    positions['steam-output-flange'] = (list(outlet['port_center']), outlet.name)
    neck = bpy.data.objects['PROCESS | steam drum steam extraction neck']
    positions['steam-extraction-neck'] = ([0, .22, 1.05], neck.name)
    assert set(positions) == set(ENDPOINTS)
    return positions


def add_steam(bpy, base, root, collection, mats, joints):
    material = vapor_material(bpy)
    wisps = []
    for e, (name, (anchor, socket_name)) in enumerate(sorted(joints.items())):
        for phase in (0, 4, 8, 12):
            vapor = base.sphere(bpy,
                f'STEAM JOINT V3 | {name} | phase {phase:02d}',
                tuple(anchor), (.035, .04, .048), material, collection, root)
            vapor['joint_id'] = name
            vapor['physical_anchor'] = socket_name
            vapor['joint_xyz'] = list(anchor)
            vapor['phase'] = phase
            vapor['render_isolation_group'] = 'joint_steam'
            vapor.hide_render = True
            keyframe_linear(vapor, 0, 'hide_render')
            for i, frame in enumerate((*FRAMES, LOOP_END)):
                drift, radius, age = puff_state(i, phase, e)
                vapor.location = tuple(anchor[j] + drift[j] for j in range(3))
                vapor.scale = (radius, radius*.90, radius*1.55)
                vapor.rotation_euler.z = math.radians(30 * math.sin(math.tau * age + e))
                vapor.hide_render = False
                for prop in ('location', 'scale', 'rotation_euler', 'hide_render'):
                    keyframe_linear(vapor, frame, prop)
            wisps.append(vapor)
    return wisps


def camera_record(scene):
    cam = scene.camera
    return {'name': cam.name, 'matrix_world': [list(row) for row in cam.matrix_world],
            'type': cam.data.type, 'ortho_scale': cam.data.ortho_scale,
            'shift_x': cam.data.shift_x, 'shift_y': cam.data.shift_y,
            'resolution': [scene.render.resolution_x, scene.render.resolution_y]}


def render(bpy, scene, filename):
    scene.render.filepath = str(filename)
    print('SOLAR_V3_CYCLES_RENDER', filename.name, 'frame', scene.frame_current, flush=True)
    bpy.ops.render.render(write_still=True)
    return {'file': filename.name, 'sha256': digest(filename), 'frame': scene.frame_current}


def build(opts):
    import bpy
    from mathutils import Vector
    sys.path.insert(0, str(HERE.parent/'v1'))
    import build_solar_boiler_v1 as base
    self_check()
    source = (opts.source or SOURCE).resolve()
    if source != SOURCE.resolve():
        raise ValueError('V3 must derive the exact committed V2 model')
    if opts.output.exists() and any(opts.output.iterdir()):
        raise FileExistsError('Refusing to overwrite prior Solar Boiler production evidence')
    source_report = json.loads(REPORT.read_text())
    original_hash = digest(source)
    assert original_hash == source_report['native_sha256'], 'V2 model SHA has changed'
    bpy.ops.wm.open_mainfile(filepath=str(source))
    scene = bpy.context.scene
    root = bpy.data.objects['EXPORT | rotate Solar Boiler model, never camera']
    assert list(root['footprint_tiles']) == [3, 2]
    scene.frame_set(0); root.rotation_euler.z = 0
    bpy.context.view_layer.update()
    fixed_camera = camera_record(scene)
    assert fixed_camera == source_report['camera']
    assert len([o for o in bpy.data.objects if o.type == 'CAMERA']) == 1
    protected = {o.name: mesh_fingerprint(o) for o in scene.objects if o.type == 'MESH'}
    mats = {k:bpy.data.materials['Solar Boiler | '+k] for k in ('needle', 'bronze', 'aged_iron')}
    mats['steam'] = bpy.data.materials['Solar Boiler | steam']
    collection = bpy.data.collections.new('07 | V3 red heat, pressure gauge and joint vapor')
    scene.collection.children.link(collection)
    pivot = add_needle(bpy, base, root, collection, mats)
    jacket, emission, heat_socket, lamp = add_accumulator(bpy, base, root, collection, mats)
    joints = joint_positions(bpy, source_report)
    wisps = add_steam(bpy, base, root, collection, mats, joints)
    for name, fingerprint in protected.items():
        ob = bpy.data.objects.get(name)
        assert ob and mesh_fingerprint(ob) == fingerprint, ('V2 original changed', name)
    for id in ('water-west', 'water-east', 'steam-north'):
        assert bpy.data.objects.get(f'PORT | {id} | full machine collar')
    for key in ('ferrocrete', 'ferrocrete_light', 'ferrocrete_dark'):
        mat = bpy.data.materials['TP Library | '+key]
        assert len([n for n in mat.node_tree.nodes if n.type=='TEX_IMAGE' and n.image and n.image.packed_file]) == 3
    scene['solar_boiler_revision'] = 'V3 full 16-frame mechanical, thermal and vapor effects candidate'
    scene['solar_boiler_v2_sha256'] = original_hash
    scene['game_integration'] = False
    scene.frame_start = 0; scene.frame_end = 97
    scene.render.engine = 'CYCLES'
    scene.cycles.device = 'CPU'; scene.cycles.samples = opts.samples
    scene.cycles.seed = 5855; scene.cycles.use_animated_seed = False
    if hasattr(scene.cycles, 'use_denoising'): scene.cycles.use_denoising = False
    for view_layer in scene.view_layers:
        if hasattr(view_layer.cycles, 'use_denoising'): view_layer.cycles.use_denoising = False
    scene.render.film_transparent = True
    scene.render.resolution_x = scene.render.resolution_y = 256
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGBA'
    scene.render.image_settings.color_depth = '8'
    scene.render.threads_mode = 'FIXED'; scene.render.threads = 4
    scene.render.fps = 8
    root.rotation_euler.z = 0; scene.frame_set(0); bpy.context.view_layer.update()
    assert camera_record(scene) == fixed_camera
    opts.output.mkdir(parents=True, exist_ok=True)
    native = opts.output/'solar-boiler-v3.blend'
    bpy.ops.file.pack_all()
    bpy.ops.wm.save_as_mainfile(filepath=str(native), compress=True, check_existing=False)
    report = {'schema':'tanks.solar-boiler.v3.animated','status':'editable 3D animation candidate',
              'source_v2':'models/island-survival/solar-boiler/generated-v2/solar-boiler-v2.blend',
              'source_v2_sha256':original_hash, 'native_sha256':digest(native),
              'footprint':[3,2], 'ports_unchanged':True, 'reflections_unchanged':True,
              'packed_fmpl_pbr':True, 'camera': fixed_camera,
              'frames':list(FRAMES), 'loop_seam_frame':97, 'working_fps':8,
              'gauge_pivot':pivot.name, 'accumulator_jacket':jacket.name,
              'accumulator_material':emission.name,'accumulator_light':lamp.name,
              'joint_vapor_count':len(wisps),'joint_vapor_anchor_names':{name:meta[1] for name,meta in joints.items()},
              'materials':{'steam': 'Solar Boiler V3 | translucent joint-pressure vapor', 'red':'Solar Boiler V3 | thermal accumulator variable red emission'},
              'original_meshes_preserved':len(protected),
              'render_count':0,'renders':[], 'visual_approved':False, 'game_integrated':False}
    manifest = opts.output/'build-report.json'
    manifest.write_text(json.dumps(report, indent=2)+'\n')
    if opts.render == 'none':
        assert digest(source)==original_hash
        return
    # Render controlled images FIRST, and only then pay for the full 68-frame
    # atlas. Blender re-evaluates animated properties when rendering: mute the
    # particular animation channels temporarily so the controlled switches
    # actually affect photons instead of being overwritten by their fcurves.
    root.rotation_euler.z = 0
    scene.frame_set(25); bpy.context.view_layer.update()
    isolation = {}

    def curves(datablock, path=None):
        action = getattr(getattr(datablock, 'animation_data', None), 'action', None)
        all_curves = getattr(action, 'fcurves', None) or []
        return [fc for fc in all_curves if path is None or fc.data_path == path]

    def capture_pair(group, tracks, choices):
        if not tracks:
            raise RuntimeError('Missing isolation animation channel for '+group)
        previous = [(fc, fc.mute) for fc in tracks]
        for fc in tracks: fc.mute = True
        bpy.context.view_layer.update()
        outputs = []
        try:
            for label, adjust in choices:
                adjust()
                bpy.context.view_layer.update()
                image = opts.output/f'effects-{group}-{label}.png'
                rec = render(bpy, scene, image)
                rec['effect'] = group; rec['setting'] = label
                outputs.append(rec)
        finally:
            for fc, old_mute in previous: fc.mute = old_mute
            scene.frame_set(24); scene.frame_set(25)
            bpy.context.view_layer.update()
        isolation[group] = outputs

    capture_pair('gauge', curves(pivot), [
        ('left', lambda: setattr(pivot.rotation_euler, 'y', math.radians(-37))),
        ('right', lambda: setattr(pivot.rotation_euler, 'y', math.radians(37)))])
    capture_pair('heat', curves(emission.node_tree) + curves(lamp.data), [
        ('off', lambda: (setattr(heat_socket, 'default_value', 0.), setattr(lamp.data, 'energy', 0.))),
        ('on', lambda: (setattr(heat_socket, 'default_value', heat_strength(4)), setattr(lamp.data, 'energy', heat_strength(4)*1.8)))])
    capture_pair('joint-steam', [fc for ob in wisps for fc in curves(ob, 'hide_render')], [
        ('off', lambda: [setattr(o, 'hide_render', True) for o in wisps]),
        ('on', lambda: [setattr(o, 'hide_render', False) for o in wisps])])
    report['isolation'] = isolation
    manifest.write_text(json.dumps(report,indent=2)+'\n')
    if opts.render == 'pilot':
        assert digest(source)==original_hash
        print('SOLAR_V3_SIX_EFFECT_ISOLATION_IMAGES_READY',flush=True)
        return
    for i, yaw in enumerate(DIRECTIONS):
        root.rotation_euler.z = math.radians(yaw)
        scene.frame_set(0)
        bpy.context.view_layer.update()
        assert camera_record(scene) == fixed_camera
        rec = render(bpy, scene, opts.output/f'idle-d{i:02d}.png')
        rec.update({'direction':i,'state':'idle','yaw':yaw})
        report['renders'].append(rec)
        manifest.write_text(json.dumps(report,indent=2)+'\n')
        for j, frame in enumerate(FRAMES):
            scene.frame_set(frame); bpy.context.view_layer.update()
            rec=render(bpy, scene, opts.output/f'working-d{i:02d}-f{j:03d}.png')
            rec.update({'direction':i,'state':'working','yaw':yaw,'index':j})
            report['renders'].append(rec)
            manifest.write_text(json.dumps(report,indent=2)+'\n')
    report['render_count'] = len(report['renders'])
    manifest.write_text(json.dumps(report,indent=2)+'\n')
    root.rotation_euler.z = 0; scene.frame_set(0); bpy.context.view_layer.update()
    assert camera_record(scene) == fixed_camera
    assert digest(source) == original_hash
    print('SOLAR_V3_ANIMATED_68_FRAMES_COMPLETE', len(report['renders']), flush=True)


def main():
    if '--self-check' in sys.argv:
        self_check(); return
    parser=argparse.ArgumentParser()
    parser.add_argument('--source',type=Path)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--samples',type=int,default=24)
    parser.add_argument('--render',choices=('all','pilot','none'),default='all')
    args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else sys.argv[1:])
    if not 4 <= args.samples <= 48: raise ValueError('Render samples must be 4..48')
    build(args)

if __name__=='__main__': main()
