# FACTORIO-FOUR-WAY-SPRITE-PRODUCTION-v1

**Single-command entry point:** `tools/art/produce_factorio_asset.py`  
**Reference asset:** the approved four-direction **Campfire V12** (`production-v12-structure-45/`).  
**Scope:** author/animate the mesh in Blender first, then run one command to render, validate, atlas-pack, prepare prototype references, and optionally publish. No unknown prototype is silently modified.

## One command

Run from the root of `mrcalzon02/Tanks-for-bob-Fork`, with Blender and Python Pillow installed:

```bash
python3 tools/art/produce_factorio_asset.py --job tools/art/jobs/campfire-next.json
```

This produces an immutable, versioned output under `models/sprite-production/campfire/v13-repro/`. It **does not** replace or alter the approved V12 sprite. To create a local mod installation (without committing) append `--install`. To install and commit/push to GitHub `main` in one authenticated command append `--publish`. No force push, no retag, no overwriting existing named files; remote commit SHA readback is mandatory. If a push fails the tool reports failure, retaining the generated data and logs.

To repackage a verified earlier render without rerendering (useful for fast regression tests):

```bash
python3 tools/art/produce_factorio_asset.py \
  --job tools/art/jobs/campfire-next.json \
  --from-capture models/island-survival/blender/production-v12-structure-45
```

**GitHub Actions:** `.github/workflows/factorio-art-production.yml` has a manual Run workflow entry for the same command. Its default push-triggered check uses the verified V12 capture for a fast packaging smoke test, while a manual Run workflow performs a fresh Blender render. The optional manual `publish` input installs/commits the versioned graphics. The job uploads QA and review files to Actions artifacts in all cases.

## New-model setup, once per asset

1. Make the model in Blender and save an editable `.blend` with **real keyframed animation** for each desired moving state. An arbitrary static model cannot have missing animation magically invented by a frame sampler; design/author the action first. Pack textures, retain a Cycles orthographic scene and a stable lighting rig.
2. Copy `tools/art/profiles/campfire-structure-replacement.json` to a new asset profile. Point `source` to the **actual `.blend`** (relative to that profile); set `adapter` to `null` unless you have a specific authored material adapter. Set `states` to `idle` (one timeline frame), plus an optional active state with the **exact keyframed frames** to capture. Set FPS, source resolution, sizes, samples and seed. Retain `directions: [0,90,180,270]`; specify `exclude_rotation`, `hide_render`, and `animated_lights` correctly.
3. Retain `camera_override.elevation_deg=45`, `azimuth_deg=0`; adjust camera `target`/`ortho_scale` and profile pivot for the asset's placement footprint. The camera and daylight stay fixed. **Rotate the model**, not the 2D finished PNG. Measure native-size readability and avoid per-frame recentering or crop.
4. Copy `tools/art/jobs/campfire-next.json` to a new job and update `asset`, **unique revision**, profile path, mod directory/name, active-state name (or `null` for static), primary cell size, graphics scale and shift. For hi-res graphics use 128px cells with `scale=0.5` only when a 64px effective footprint is appropriate; larger entities require their own calibrated scale. The mod name must match its `info.json`.
5. Execute the single command. Inspect `four-way-review.png` directly in the chat, check the individual GIF loops/rotations, and inspect `production-receipt.json` for hashes and QA. When satisfactory, use `--install` and then/or `--publish` with a new revision. Attach the generated `prototype-ready.lua` fields to the correct entity prototype **only after checking its API type**. Load and rotate the entity in Factorio before marking engine integration complete.

## Output contract

```text
models/sprite-production/ASSET/REVISION/
  capture/                    master.blend, all 4-direction RGBA source frames,
                              atlases, qa.json, reopen-qa.json, hashes,
                              directional GIF previews, logs
  prototype_ready/graphics/entity/
                              ASSET-REVISION-idle.png,
                              ASSET-REVISION-ACTIVE.png,
                              plus requested -64 and -256 sizes
  prototype_ready/graphics/icons/ASSET-REVISION.png
  prototype-ready.lua         four cardinal entries with correct y offsets
  four-way-review.png         directly inspectable sprite proof
  production-receipt.json     reproducibility and integration status
```

The source exporter (`tools/art/export_sprites.py`) captures all four rotations beneath a fixed camera/daylight, keeps full-object RGBA frames in one fixed canvas, generates native masters, and fails closed on clipping, alpha errors, missing/duplicate frames or mismatched hashes. The wrapper verifies the saved Blender master, full capture manifest and atlas hashes; repacks into Factorio directional groups with matching idle/active frame counts (repeating a static idle frame), checks saved output roundtrips, emits correct 8-column **Animation4Way** Lua, creates an icon candidate, and records hashes. It rejects atlases exceeding 8192px in either dimension.

### Explicit limitations

- **Art preparation is not animation authoring.** Keyframe animation or an asset-specific authoring script must exist before capture.
- **The Lua file is prototype-ready, not magically installed into every kind of entity.** The crafting-machine snippet is meant for `graphics_set` and replaces neither unrelated fields nor gameplay logic. Full-object idle/working sprites are *alternatives*, never overlaid twice.
- **Sprites are only prepared until connected to the intended prototype.** The producer does not claim an actual Factorio client-load test; runtime suitability and visual acceptance are separate.
- **No hidden rendering work:** after every model/art export, display the real `four-way-review.png` or actual frames in the chat, not just a GitHub link.

## Validation and sources

```bash
python3 -m unittest discover -s tools/art -p 'test_*.py' -v
```

Always retain a passing CI run/remote commit readback and the capture SHA256 evidence. Original art stays available for rollback. Primary source: the already validated Campfire V12 asset and `tools/art/SPRITE_EXPORT.md`.

Factorio prototype references: [Animation4Way](https://lua-api.factorio.com/latest/types/Animation4Way.html), [WorkingVisualisations](https://lua-api.factorio.com/latest/types/WorkingVisualisations.html) (idle and active animations must have matching frame counts), and [AnimationParameters](https://lua-api.factorio.com/latest/types/AnimationParameters.html) (`fps / 60` animation speed).
