#!/usr/bin/env python3
"""Build Fish Pond V1 by deriving the actual Clay Pit V4c native Blender scene.

Original Clay Pit meshes, material and camera are preserved. Only clay-working
implements are removed in the derivative; a filled water surface and four
actual low-poly fish are added. No game prototype or workflow is changed.

Pure animation math can be checked without Blender:
  python build_fish_pond_v1.py --self-check

Native Blender:
  blender -b --factory-startup --python build_fish_pond_v1.py -- \\
    --out models/island-survival/fish-pond/generated-v1 --render all
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import sys

FPS = 8
WORK_FRAMES = tuple(range(1, 92, 6))
LOOP_END = 97
CAMERA_SCALE = 3.30
FISH = (
    # name, x-radius, y-radius, start phase, direction, height, color
    ("copper", .28, .24, .0, 1, -.110, (.59, .31, .11, 1)),
    ("slate", .38, .31, 2.15, -1, -.108, (.20, .28, .30, 1)),
    ("gold", .43, .35, 4.0, 1, -.112, (.72, .53, .17, 1)),
    ("mottled", .20, .40, 1.4, -1, -.119, (.32, .47, .30, 1)),
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pose(spec, index: int):
    """Exact 16-step ellipse with an independently keyed, continuous heading."""
    _, rx, ry, start, direction, z, _ = spec
    angle = start + direction * 2 * math.pi * index / 16
    return ((rx * math.cos(angle), ry * math.sin(angle), z),
            angle + direction * math.pi / 2)


def self_check():
    assert len(WORK_FRAMES) == 16 and LOOP_END - WORK_FRAMES[-1] == 6
    assert len(FISH) == 4
    for spec in FISH:
        first, heading = pose(spec, 0)
        end, final_heading = pose(spec, 16)
        assert max(abs(a-b) for a, b in zip(first, end)) < 1e-12
        assert abs(abs(final_heading-heading)-2*math.pi) < 1e-12
        assert all(abs(v) <= .45 for v in first[:2])
        # Lowest fish geometry remains above the basin floor (-.21), below water (-.016).
        assert -.16 < first[2] < -.06
    print('FISH_POND_V1_ORBIT_SELF_CHECK_PASS')


def make_material(bpy, name, rgba, roughness=.42, metallic=0.0):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = rgba
    mat.use_nodes = True
    shader = mat.node_tree.nodes.get('Principled BSDF')
    shader.inputs['Base Color'].default_value = rgba
    shader.inputs['Roughness'].default_value = roughness
    shader.inputs['Metallic'].default_value = metallic
    return mat


def register_mesh(bpy, collection, name, vertices, faces, materials, root, material_ids=None):
    mesh = bpy.data.meshes.new(name + ' mesh')
    mesh.from_pydata(vertices, [], faces)
    mesh.update()
    ob = bpy.data.objects.new(name, mesh)
    collection.objects.link(ob)
    for mat in materials:
        mesh.materials.append(mat)
    if material_ids is not None:
        for poly, mat_index in zip(mesh.polygons, material_ids):
            poly.material_index = mat_index
    # Original V4c root is the only orientation pivot; camera never rotates.
    ob.parent = root
    return ob


def water_material(bpy):
    material = bpy.data.materials.new('POND | clear blue-green water - fish visible below')
    material.use_nodes = True
    nodes = material.node_tree.nodes
    nodes.clear()
    links = material.node_tree.links
    output = nodes.new('ShaderNodeOutputMaterial')
    surface = nodes.new('ShaderNodeBsdfPrincipled')
    surface.inputs['Base Color'].default_value = (.045, .23, .27, 1)
    surface.inputs['Roughness'].default_value = .20
    surface.inputs['IOR'].default_value = 1.33
    transmission = surface.inputs.get('Transmission Weight')
    if transmission is not None:
        transmission.default_value = .15
    transparent = nodes.new('ShaderNodeBsdfTransparent')
    mix = nodes.new('ShaderNodeMixShader')
    mix.inputs[0].default_value = .47
    links.new(surface.outputs['BSDF'], mix.inputs[1])
    links.new(transparent.outputs['BSDF'], mix.inputs[2])
    links.new(mix.outputs[0], output.inputs['Surface'])
    return material


def make_water(bpy, collection, root):
    # V3 bowl wall crosses z~-.016 at radial fraction .70 of its handmade rim.
    # This sits inside that wall: no extra pond, no free-standing cylinder.
    rings = ((.31, -.015), (.56, -.017), (.70, -.015))
    segments = 64
    vertices = [(0, 0, -.015)]
    for fraction, z in rings:
        for i in range(segments):
            a = 2*math.pi*i/segments
            uneven = 1 + .012*math.sin(5*a+.4) + .009*math.sin(8*a-.7)
            vertices.append((1.13*fraction*math.cos(a)*uneven,
                             1.29*fraction*math.sin(a)*uneven,
                             z + .002*math.sin(6*a+.3)))
    faces = []
    for i in range(segments):
        faces.append((0, 1+i, 1+(i+1)%segments))
    for ring in range(len(rings)-1):
        start = 1+ring*segments
        next_ring = start+segments
        for i in range(segments):
            j = (i+1)%segments
            faces.append((start+i, next_ring+i, next_ring+j, start+j))
    ob = register_mesh(bpy, collection, 'POND | permanent filled water plane',
                       vertices, faces, [water_material(bpy)], root)
    for poly in ob.data.polygons:
        poly.use_smooth = True
    return ob


def make_fish(bpy, collection, root, spec, index):
    name, _, _, _, _, _, rgba = spec
    orbit = bpy.data.objects.new(f'POND | fish {index+1:02d} {name} orbit', None)
    collection.objects.link(orbit)
    orbit.parent = root
    # Mesh is a closed, low-poly 3D body with an integral forked tail.
    outline = [(.170, 0), (.120, .038), (.024, .067), (-.080, .049),
               (-.136, .027), (-.220, .073), (-.200, 0), (-.220, -.073),
               (-.136, -.027), (-.080, -.049), (.024, -.067), (.120, -.038)]
    count = len(outline)
    vertices = [(x, y, 0) for x,y in outline]
    vertices += [(.005, 0, .039), (.005, 0, -.028)]
    faces = [(count, i, (i+1)%count) for i in range(count)]
    faces += [(count+1, (i+1)%count, i) for i in range(count)]
    # Raised dorsal fin reads in the fixed Factorio view.
    vertices += [(-.060, 0, .031), (-.105, 0, .072), (.012, 0, .033)]
    faces.append((count+2, count+3, count+4))
    body = make_material(bpy, f'POND | {name} scaled fish', rgba, .55)
    fin = make_material(bpy, f'POND | {name} fin and tail',
                        tuple(min(1, c*.75) for c in rgba[:3])+(1,), .62)
    indices = [1 if i in (4, 5, 6, 7) else 0 for i in range(count)]
    indices += [1 if i in (4, 5, 6, 7) else 0 for i in range(count)]
    indices.append(1)
    mesh = register_mesh(bpy, collection, f'POND | fish {index+1:02d} {name} body',
                         vertices, faces, [body,fin], orbit, indices)
    # Fish meshes, not orbit empties, disappear for the idle/empty-pond state.
    mesh.hide_render = True
    mesh.keyframe_insert(data_path='hide_render', frame=0)
    mesh.hide_render = False
    mesh.keyframe_insert(data_path='hide_render', frame=1)
    mesh.keyframe_insert(data_path='hide_render', frame=LOOP_END)
    # Blender 5.x layered Actions may not expose legacy action.fcurves.
    # Boolean hide_render channels hold exact states even without editing curves.
    if mesh.animation_data and mesh.animation_data.action:
        for curve in (getattr(mesh.animation_data.action, 'fcurves', None) or []):
            for key in curve.keyframe_points:
                key.interpolation = 'CONSTANT'
    for k,frame in enumerate((*WORK_FRAMES, LOOP_END)):
        position, heading = pose(spec, k)
        orbit.location = position
        orbit.rotation_euler.z = heading
        orbit.keyframe_insert(data_path='location', frame=frame)
        orbit.keyframe_insert(data_path='rotation_euler', frame=frame)
    # Linear interpolation avoids speed lurches; frame 97 matches frame 1.
    for curve in (getattr(orbit.animation_data.action, 'fcurves', None) or []):
        for key in curve.keyframe_points:
            key.interpolation = 'LINEAR'
    return orbit, mesh


def validate(bpy):
    scene = bpy.context.scene
    root = bpy.data.objects.get('EXPORT | rotate all clay and tools, never camera')
    if not root or not scene.camera or scene.camera.data.type != 'ORTHO':
        raise RuntimeError('Missing authentic Clay Pit 3D source/camera')
    if abs(scene.camera.data.ortho_scale-CAMERA_SCALE) > .01:
        raise RuntimeError('Clay Pit camera changed')
    if scene.camera.parent or scene.camera == root:
        raise RuntimeError('Camera accidentally joined rotating model')
    if not bpy.data.objects.get('EARTH | one broad excavated clay bowl'):
        raise RuntimeError('Original excavated clay basin missing')
    water = bpy.data.objects.get('POND | permanent filled water plane')
    bodies = [o for o in scene.objects if o.name.startswith('POND | fish') and o.name.endswith('body')]
    orbits = [o for o in scene.objects if o.name.startswith('POND | fish') and o.name.endswith('orbit')]
    if water is None or len(bodies) != 4 or len(orbits) != 4:
        raise RuntimeError('Expected one water plane and four 3D swimming fish')
    if any(o.name.startswith('WORK |') for o in scene.objects):
        raise RuntimeError('Clay Pit bucket/lantern/shovel accidentally retained')
    scene.frame_set(0)
    if any(not o.hide_render for o in bodies):
        raise RuntimeError('Idle pond has visible fish')
    scene.frame_set(1)
    if any(o.hide_render for o in bodies):
        raise RuntimeError('Working pond is missing fish')
    first = [(o.location.copy(),o.rotation_euler.z) for o in orbits]
    scene.frame_set(LOOP_END)
    for o,(loc,rot) in zip(orbits,first):
        if (o.location-loc).length > 1e-5 or abs(math.sin(o.rotation_euler.z-rot)) > 1e-5:
            raise RuntimeError('Fish orbit failed to close at loop seam')
    scene.frame_set(0)
    return len([o for o in scene.objects if o.name.startswith('EARTH |')])


def build(options):
    import bpy
    output = Path(options.out).resolve()
    if output.exists() and any(output.iterdir()):
        raise FileExistsError('Output must be empty: never overwrite earlier work')
    source = Path(options.source).resolve() if options.source else (
        Path(__file__).resolve().parents[2]/'clay-pit/generated-v4c/clay-pit-v4c.blend')
    if not source.is_file():
        raise FileNotFoundError(f'Clay Pit V4c source missing: {source}')
    source_hash = sha256(source)
    bpy.ops.wm.open_mainfile(filepath=str(source))
    scene = bpy.context.scene
    root = bpy.data.objects.get('EXPORT | rotate all clay and tools, never camera')
    if root is None or bpy.data.objects.get('EARTH | one broad excavated clay bowl') is None:
        raise RuntimeError('Expected original Clay Pit V4c scene')
    if scene.camera is None or abs(scene.camera.data.ortho_scale-CAMERA_SCALE) > .01:
        raise RuntimeError('Expected original Clay Pit 45-degree capture camera')
    scene.frame_set(0)
    root.rotation_euler.z = 0.0
    if root.location.length > 1e-6:
        raise RuntimeError('Clay Pit root origin has moved; refuse inaccurate pond')
    # Delete *only in this new scene* the Clay Pit-specific working props/animation.
    # The source on disk remains byte-for-byte intact.
    removed = []
    for obj in list(scene.objects):
        if obj.name.startswith('WORK |'):
            removed.append(obj.name)
            bpy.data.objects.remove(obj, do_unlink=True)
    rig = bpy.data.objects.get('ANIMATION | bucket and rope pendulum pivot')
    if rig:
        bpy.data.objects.remove(rig, do_unlink=True)
    pond = bpy.data.collections.new('FISH POND | water and animated fish')
    scene.collection.children.link(pond)
    make_water(bpy, pond, root)
    for index, spec in enumerate(FISH):
        make_fish(bpy, pond, root, spec, index)
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = options.samples
    scene.cycles.device = 'CPU'
    scene.render.resolution_x = scene.render.resolution_y = 256
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGBA'
    scene.render.film_transparent = True
    scene.render.fps = FPS
    scene.frame_end = 96
    scene['fish_pond_source_blend_sha256'] = source_hash
    scene['fish_pond_model_revision'] = 'v1-claypit-water-swimming-fish'
    ground_parts = validate(bpy)
    output.mkdir(parents=True,exist_ok=True)
    native = output/'fish-pond-v1.blend'
    bpy.ops.wm.save_as_mainfile(filepath=str(native), check_existing=False)
    frames = []
    if options.render != 'none':
        for state, indices in [('idle', [0]), ('working', list(range(16)) if options.render == 'all' else [4])]:
            for direction, degrees in enumerate((0,90,180,270)):
                root.rotation_euler.z = math.radians(degrees)
                for index in indices:
                    timeline = 0 if state == 'idle' else WORK_FRAMES[index]
                    scene.frame_set(timeline)
                    bpy.context.view_layer.update()
                    filename = (f'idle-d{direction:02d}.png' if state == 'idle' else
                                f'working-d{direction:02d}-f{index:03d}.png')
                    target = output/filename
                    scene.render.filepath = str(target)
                    bpy.ops.render.render(write_still=True)
                    frames.append({'state':state,'direction':direction,'index':index,
                                   'frame':timeline,'file':filename,'sha256':sha256(target)})
    report = {'schema':1,'asset':'fish-pond','revision':'v1','source':str(source),
              'source_sha256':source_hash,'master_sha256':sha256(native),
              'blender':bpy.app.version_string,'terrain_meshes_preserved':ground_parts,
              'clay_working_props_removed':len(removed),'water':True,'fish_count':4,
              'idle_has_fish':False,'working_animation_frames':16,'directions':[0,90,180,270],
              'camera_ortho_scale':CAMERA_SCALE,'render_mode':options.render,
              'renders':frames,'game_integration':False,'visual_approved':False}
    (output/'build-report.json').write_text(json.dumps(report,indent=2)+'\n')
    if sha256(source) != source_hash:
        raise RuntimeError('Original Clay Pit source unexpectedly changed')
    print('FISH_POND_V1_DERIVATIVE_COMPLETE',str(native),'frames',len(frames),flush=True)


def main():
    if '--self-check' in sys.argv:
        self_check()
        return
    ap = argparse.ArgumentParser()
    ap.add_argument('--source', default=None)
    ap.add_argument('--out', required=True)
    ap.add_argument('--samples', type=int, default=24)
    ap.add_argument('--render', choices=('none','proof','all'), default='all')
    args = ap.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else sys.argv[1:])
    if not 1 <= args.samples <= 4096:
        raise ValueError('Samples out of range')
    self_check()
    build(args)


if __name__ == '__main__':
    main()
