# Campfire v2 — editable reconstruction

This folder contains the **actual** low-poly campfire reconstruction, not concept art or a sprite replacement.

Reference: `tanks_for_bob_fork_1.8.95/graphics/entity/campfire.png` and the separate working overlay `campfire-w.png`.

## Files

- `campfire-refined.obj`: Blender-importable physical stones, wood, ash and optional flame groups.
- `campfire-refined.mtl`: editable surface-material palette.
- `build_campfire.py`: deterministic geometry source, no third-party libraries needed.
- `render_campfire.py`: orthographic preview renderer (Python, NumPy, Pillow).
- `validate_campfire.py`: OBJ/material structural assertions.

## Build and inspect

From the repository root:

```sh
python models/island-survival/refined/build_campfire.py models/island-survival/refined
python models/island-survival/refined/validate_campfire.py
python models/island-survival/refined/render_campfire.py
```

Or import `campfire-refined.obj` in Blender using File > Import > Wavefront OBJ. Keep the matching MTL alongside it. Set camera to orthographic at approximately 47 degrees elevation; change the visibility of `flame_tongue_*` groups for the unlit/working states.

## Scope and next refinement

This is a **V2 geometry pass** that deliberately preserves the original `models/island-survival/obj/campfire.obj` blockout and the mod's original sprite assets. It uses distinct, irregular stones, 3 log pieces with caps/bark ridges, ash and charcoal, and detachable flame tongues. Nominal world units are tiles; X east, Y north, Z up. The original source sprite remains the visual authority. Further work should match the exact 64px silhouette, asymmetry, stone grading and bark texture at the game's camera and export resolution.

Important: no in-game graphic references were changed and no Blender-native .blend was produced. The OBJ+MTL can be imported and edited in Blender.
