#!/usr/bin/env python3
"""Assemble transparently rendered Blender timeline samples into a real looping GIF."""
import argparse
from pathlib import Path
from PIL import Image

p = argparse.ArgumentParser()
p.add_argument("--frames", required=True, type=Path)
p.add_argument("--out", required=True, type=Path)
opts = p.parse_args()
paths = sorted(opts.frames.glob("frame_*.png"))
assert len(paths) == 16, f"Expected 16 real rendered frames, found {len(paths)}"
images = []
for src in paths:
    with Image.open(src) as inp:
        assert inp.size == (320, 320), f"Unexpected render size {inp.size} in {src}"
        # Stable neutral backdrop for correct transparent-frame display in GIF viewers.
        rgba = inp.convert("RGBA")
        bg = Image.new("RGBA", rgba.size, (28, 30, 34, 255))
        bg.alpha_composite(rgba)
        images.append(bg.convert("RGB").quantize(colors=255, method=Image.Quantize.MEDIANCUT))
opts.out.parent.mkdir(parents=True, exist_ok=True)
images[0].save(opts.out, format="GIF", save_all=True, append_images=images[1:],
               duration=125, loop=0, disposal=2, optimize=False)
with Image.open(opts.out) as gif:
    assert gif.n_frames == len(paths), f"GIF contains {gif.n_frames} not {len(paths)}"
    assert gif.info.get("loop") == 0, "GIF does not loop"
print(f"ANIMATED_GIF_OK {opts.out} frames={len(paths)} duration_ms=2000 bytes={opts.out.stat().st_size}")
