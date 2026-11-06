# Campfire V4 — timber/stone geometry refinement

Status: **comparison model / further art review required**. Do not replace original game sprites yet.

This is a second refinement cycle after the V2 campfire blockout.
It deliberately retains the V2 files for side-by-side comparison.

## Included
- `build_campfire_v4.py`: deterministic procedural, editable geometry generator.
- `campfire-refined-v4.obj` and `.mtl`: actual model and material palette; import into Blender together.
- `render_campfire_v4.py`: standalone software preview of the OBJ triangles using Pillow and NumPy; no conceptual art.
- `validate_campfire_v4.py`: checks topology, group and material references, finite coordinates, and bit-for-bit regeneration.

Geometry: **2,933 vertices, 4,995 triangles, 71 named groups**.
Includes individually irregular stones, six crooked and tapered wood/twig pieces,
exposed log endgrain, bark furrows, kindling, charcoal/embers and separate optional flames.
Built for the existing 64px sprite camera, not hidden internal detail.

## Local reproduction
```sh
python3 build_campfire_v4.py .
python3 validate_campfire_v4.py
python3 render_campfire_v4.py
```

Import `campfire-refined-v4.obj` with `campfire-refined-v4.mtl` next to it in Blender.
X east, Y north, Z up; nominal units. Renderer is a software OBJ preview, **not a Blender Cycles render**.

## Further required
- Refine irregular timber cracks and split end faces. Current bark is intentionally simplified compared with real bark.
- Shrink and differentiate several overly large stone chunks.
- Match pixel-for-pixel silhouette from `tanks_for_bob_fork_1.8.95/graphics/entity/campfire.png` at 64px.
- Tune emissive flames and work-state light separately from the physical geometry.
- Keep `tanks_for_bob_fork_1.8.95/graphics/entity/campfire*.png` unchanged pending approval.
