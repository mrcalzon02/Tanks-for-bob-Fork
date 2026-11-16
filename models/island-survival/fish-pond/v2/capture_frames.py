"""Capture the inspected, unchanged pond source into a fresh production stage."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import shutil
import sys

import bpy


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--candidate', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--fmpl-tools', type=Path, required=True)
    args = parser.parse_args(sys.argv[sys.argv.index('--')+1:])
    source, out = args.candidate.resolve(), args.out.resolve()
    if out.exists():
        raise FileExistsError(out)
    inspect = json.loads((source/'runtime-inspection.json').read_text())
    assert inspect['technical_checks_passed']
    assert sha(source/'fish-pond-v2.blend') == inspect['source_sha256']
    assert sha(source/'fish-pond-v2.glb') == inspect['glb_sha256']
    out.mkdir(parents=True)
    for name in ('fish-pond-v2.blend', 'fish-pond-v2.glb', 'capture-profile.json',
                 'runtime-inspection.json', 'build-report.json'):
        shutil.copy2(source/name, out/name)
    for path in source.glob('fish-pond-v2-*.png'):
        shutil.copy2(path, out/path.name)
    for path in source.glob('actual-glb-*.png'):
        shutil.copy2(path, out/path.name)
    profile = json.loads((out/'capture-profile.json').read_text())
    sys.path.insert(0, str(args.fmpl_tools.resolve()))
    from blender_camera_guard import assert_clean
    bpy.ops.wm.open_mainfile(filepath=str(out/'fish-pond-v2.blend'))
    scene = bpy.context.scene
    root = bpy.data.objects['EXPORT | rotate all clay and tools, never camera']
    projection = bpy.data.objects.new('SPRITE ONLY | square ground-grid projection', None)
    scene.collection.objects.link(projection)
    projection.scale.y = math.sqrt(2)
    root.parent = projection
    images = []
    for facing, yaw in [('north',0), ('east',270), ('south',180), ('west',90)]:
        root.rotation_euler.z = math.radians(yaw)
        for state, frames in profile['states'].items():
            for index, frame in enumerate(frames):
                scene.frame_set(frame)
                assert_clean(scene, profile, bpy)
                path = out/(f'{facing}-{state}-{index:02d}.png')
                scene.render.filepath = str(path)
                bpy.ops.render.render(write_still=True)
                images.append({'file':path.name, 'facing':facing, 'yaw':yaw,
                               'state':state, 'index':index, 'source_frame':frame, 'sha256':sha(path)})
    receipt = {'schema':'tanks.fish-pond.v2.capture', 'source_sha256':inspect['source_sha256'],
        'runtime_sha256':inspect['glb_sha256'], 'genuine_blender_frames':len(images),
        'frame_size':[256,256], 'fps':8, 'images':images, 'owner_visual_approved':False,
        'native_game_verified':False, 'native_projection':{'global_ground_y_scale':math.sqrt(2),
            'runtime_geometry_changed':False}, 'idle_state':'filled water without fish',
        'working_state':'four swimming fish, editable tail strokes'}
    (out/'capture-manifest.json').write_text(json.dumps(receipt, indent=2)+'\n')
    print('FISH_POND_V2_FULL_CAPTURE', len(images), flush=True)


if __name__ == '__main__':
    main()
