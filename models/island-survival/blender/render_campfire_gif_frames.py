#!/usr/bin/env python3
"""Render actual keyed animation from the native Blender scene, one Cycles frame at a time."""
from __future__ import annotations
import argparse
from pathlib import Path
import sys

import bpy

args = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
parser = argparse.ArgumentParser()
parser.add_argument("--out", type=Path, required=True)
parser.add_argument("--samples", type=int, default=12)
parser.add_argument("--resolution", type=int, default=320)
opts = parser.parse_args(args)
opts.out.mkdir(parents=True, exist_ok=True)

scene = bpy.context.scene
assert scene.render.engine == "CYCLES", "Must use native Cycles renderer"
assert scene.camera is not None, "Missing native Blender camera"
assert scene.frame_start in (0,1) and scene.frame_end == 96, "Unexpected timeline"
flames = [ob for ob in scene.objects if ob.name.startswith("flame_tongue")]
fire_lights = [ob for ob in scene.objects if ob.name == "04 | animated fire light"]
assert len(flames) == 6, f"Expected six animated flame meshes; found {len(flames)}"
assert len(fire_lights) == 1 and fire_lights[0].data.animation_data, "Missing keyframed firelight"
assert all(ob.animation_data for ob in flames), "Flame geometry missing animation keyframes"
for ob in flames + fire_lights:
    ob.hide_render = False

scene.cycles.samples = opts.samples
scene.render.film_transparent = True
scene.render.resolution_x = opts.resolution
scene.render.resolution_y = opts.resolution
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"
scene.render.image_settings.color_mode = "RGBA"

# Sample the original keyed 96-frame cycle every 6 frames; frame 97 repeats frame 1.
frame_numbers = list(range(1, 97, 6))
assert len(frame_numbers) == 16
for index, frame in enumerate(frame_numbers):
    scene.frame_set(frame)
    scene.render.filepath = str(opts.out / f"frame_{index:03}.png")
    print(f"RENDER_ANIMATION_FRAME {index + 1}/{len(frame_numbers)} timeline={frame}", flush=True)
    bpy.ops.render.render(write_still=True)
    assert (opts.out / f"frame_{index:03}.png").stat().st_size > 1000
print(f"ANIMATION_FRAMES_OK count={len(frame_numbers)} source_blend={bpy.data.filepath}")
