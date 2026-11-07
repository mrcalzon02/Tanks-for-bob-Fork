# Reusable Blender sprite export

Run from the repository root with Blender and Pillow installed:

```bash
python3 tools/art/export_sprites.py --config tools/art/profiles/campfire.json --out /tmp/campfire-export
python3 tools/art/export_sprites.py --config tools/art/profiles/campfire-static-four-view.json --out /tmp/campfire-static
python3 tools/art/export_sprites.py --pack-only --out /tmp/campfire-export
python3 -m unittest discover -s tools/art -p 'test_*.py' -v
```

The first command is the complete animated production test. The second tests static capture at four angles. Output directories must be new or empty; failed runs are retained for diagnosis. `--pack-only` rechecks existing captures without rendering. Tested locally in **Blender 4.3.2**, CPU Cycles, Pillow 13. The existing scoped Blender CI also exercises both commands and records its actual installed Blender version; a local pass does not imply a CI pass.

## Supply another model

Copy a profile. Set `source` relative to that profile, `adapter` to null (or omit it), `states` to a mapping of named states to explicit timeline frames, and `directions` to rotation angles in degrees. One timeline frame is a static capture; multiple frames form an animation. `pivot` is the model rotation center in world coordinates. Supply the required authored orthographic camera, Cycles materials, animation and lights in the source `.blend`; pack external textures first. List fixed ground objects in `exclude_rotation`, optional non-export objects in `hide_render`, and deliberately animated lights in `animated_lights`. The exporter fails if any other light or the camera moves during capture.

The exporter preserves the authored scene. It does **not** invent a camera, normalize object scale, fit each frame, trim sprites independently, or assert that every arbitrary model already matches Factorio lighting. Camera, origin and source geometry must be calibrated for each asset; clipping causes failure. Every direction rotates the model beneath an immutable camera/daylight rig. Armature/parent hierarchies rotate together.

`source_size` is the actual render canvas. Every size in `sizes` is downsampled from that same fixed canvas with premultiplied-alpha-aware Pillow RGBA resizing; no camera refit. The config pins samples and Cycles seed. The source SHA256, actual Blender version, camera matrix, ortho scale, color management, daylight values, frame numbers, material changes and output hashes live in `capture.json`. Procedural source shaders remain editable and maps stay packed.

## Output contract

- `master.blend`: editable MODEL and RENDER scenes with linked model objects, original materials/animation, fixed camera/light setup and export direction pivot. Both scene datablocks are explicitly retained in background saves.
- `frames/STATE/dNN/fNNN.png`: genuine transparent RGBA Blender captures in explicit timeline order.
- `STATE-SIZE.png`: full-object state atlases. Each direction occupies `ceil(frame_count / columns)` consecutive rows. `qa.json` records each cell rectangle; unused cells remain transparent.
- `capture.json`, `qa.json`, `reopen-qa.json`: capture provenance, atlas integrity results and independent native-master reopen checks.
- `contact-sheet.png`, `STATE-preview.gif`: review previews; their opaque preview background is never used in sprite atlases. GIF timing is rounded to GIF's 10ms resolution; use profile fps for playback in other consumers.
- `blender.log`, `reopen.log`, `export-config.json`: execution evidence.

The production campfire profile captures **four directions (0°, 90°, 180°, 270°)** with one idle frame and 16 burning frames per direction at timeline 1,7,…,91: **4 static frames + 64 actual animated Blender renders**. It produces 64/128/256px cells. Each burning atlas has eight columns by eight rows (two rows per direction), so sizes are respectively **512×512, 1024×1024 and 2048×2048**. Its idle atlas uses one column and four rows. A separate reduced-resolution four-view static regression profile remains available. Four direction-specific burning GIFs are emitted as `burning-d00-preview.gif` through `burning-d03-preview.gif` in addition to the original compatible `burning-preview.gif`. The passing CI job publishes the entire new result to `models/island-survival/blender/production-v11-four-view/` on main. Native-size alpha, frame count/order, unique animated cells, visible clipping and lossless cell extraction are checked. The actual saved `.blend` is reopened in a separate Blender process; campfire checks include 15 dry stone materials, 42 wood objects, six keyed flames and frame-dependent char/fire visibility.

These are **complete rendered state frames**, not working overlays to stack on top of an idle sprite. Game-layer extraction, Lua, engine deployment and in-game acceptance are separate work. This implements the user's corrected Blender-only scope. Visual approval remains pending: test success cannot approve the stone appearance, animation seam or Factorio lighting calibration.

## Campfire material adapter

`campfire-matte-stones` implements ART-CF-005 against the retained V9 source. Only stone Principled roughness/specular/coat/metallic inputs change: roughness .98, specular IOR level .08, metallic 0, coat 0. Original color graphs, tangent normals, geometry, bark, endgrain, wood-char state and animated flames remain editable. The material changes are recorded per material in the capture manifest. Disabling the adapter exports the unchanged source materials.

The profile excludes the development ground shadow catcher from beauty capture because its broad low-alpha shadow crossed the canvas boundary. Contact shading within the model remains. A separate ground-shadow atlas is **not** delivered by this profile; this is explicit output scope, not a claimed shadow-pass implementation. The original ground object remains in the saved editable scene, hidden from render.

## Recovery evidence

See [the dated recovery audit](../../docs/art/CAMPFIRE_5855_RECOVERY_AUDIT.md) and [the campfire ledger](../../models/island-survival/blender/CAMPFIRE_PRODUCTION_EXPORT_CHECKLIST.md). The original V9 and game graphics are preserved in their existing locations. The executable pipeline uses a local adapter around the authored scene; no Valerian preset, AshenHermit add-on or third-party HDRI was imported or claimed tested.
