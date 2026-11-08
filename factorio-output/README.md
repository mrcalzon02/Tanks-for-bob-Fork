# Factorio Output — a copyable Blender → Factorio sprite module

**The reusable 'do the thing' engine:** supply an authored `.blend` and a small JSON job, and it runs calibrated 45° orthographic capture at 0°, 90°, 180° and 270°, exports actual idle and animated RGBA frames, packs 64/128/256px Factorio atlases, creates a 64px item icon, prepares four-direction Lua, independently reopens the Blender master, verifies hashes and can commit/push the result to GitHub.

This is the reusable process behind our campfire, clay pit, pit kiln and lumberyard work. It is deliberately isolated under `factorio-output/`; no Tanks for Bob-specific gameplay code is necessary to copy the engine. A source `.blend` still needs to be modeled and animated by the artist—this module automates *output*, not 3D modeling.

## Copy into another GitHub repository

1. Copy the complete `factorio-output/` folder to the other repository root.
2. Copy `factorio-output/workflow.template.yml` to `.github/workflows/factorio-output.yml`. It is byte-for-byte the same runnable workflow used here.
3. Supply a real, editable Cycles `.blend` with an orthographic camera, packed external textures, stationary daylight, and authored keyframes.
4. Copy and edit `factorio-output/examples/demo-profile.json` (points to the `.blend`, states/timeline frames, the fixed camera and resolutions) and `demo-job.json` (names the mod, asset, revision, icon/scale and optional prototype).
5. Use GitHub **Actions → Factorio Output → Run workflow**, mode `review`. Inspect the generated review and GIFs before running `publish` or `deploy`.

## One command

```bash
python3 factorio-output/run.py --job factorio-output/examples/demo-job.json
python3 factorio-output/run.py --job jobs/my-machine.json --blender blender
python3 factorio-output/run.py --job jobs/my-machine.json --from-capture models/previous-verified-capture
```

To generate the editable demonstration `.blend` before running the sample locally:

```bash
blender -b -t 2 --python factorio-output/examples/make_demo_scene.py
python3 factorio-output/run.py --job factorio-output/examples/demo-job.json
```

The example is a genuine Blender test scene, not a gameplay-ready mod. Replace its `demo-mod` and `demo.blend` with your own actual project before publishing. Dependencies: Python 3, Pillow, Blender with Cycles. Prototype deployment additionally requires Lua 5.4 and luac; the CI installs these with `apt-get install blender python3-pil lua5.4`.

## Review, publish and deploy

| Mode | Result | Mod/GitHub mutation |
| --- | --- | --- |
| `review` | Render genuine Blender frames and four orientations; generate atlases, preview GIFs, item icon, Lua and QA | None |
| `publish` (`--publish`) | Install versioned sprite/icon files, commit/push to `main`, read back GitHub remote SHA | Assets only; **no prototype attachment** |
| `deploy` (`--deploy`) | As publish, plus guarded `data-final-fixes.lua` override of the **exact named** assembling-machine/furnace prototype with Lua syntax/runtime probes | Explicit prototype and icons |
| `--from-capture` | Reuse a verified capture made by **this same module**; no Blender rerender | Depends on mode |

The `prototype` field in the job must name the exact `type`, `name`, source `.lua` path, and optional `item_icon`. The target must have exactly one declaration. Existing managed attachments require `--replace-attachment` with `deploy`. No forced push, destructive overwrite or silent mutation. Releases require a fresh revision directory.

**Deploy does not publish to the Factorio Mod Portal.** A separate official game-load/benchmark/publishing workflow is required for external distribution. Passing hashes, Lua checks and visual capture tests is not proof of the in-game appearance.

## Call it from a second workflow

```yaml
jobs:
  factorio_art:
    uses: ./.github/workflows/factorio-output.yml
    with:
      job: jobs/my-machine.json
      mode: review
```

After art acceptance, change mode to `publish` for versioned assets, or explicitly `deploy` to attach the targeted prototype. The module refuses to overwrite a previous output directory and verifies the GitHub push by remote SHA readback.

## Deliverables and audit

`models/sprite-production/ASSET/REVISION/` contains `capture/master.blend`, `capture/frames`, verified directional sheets, a contact sheet and GIFs, `prototype_ready/graphics/entity` sprites, an item icon, `prototype-ready.lua`, `four-way-review.png`, and `production-receipt.json` (SHA256 provenance and attachment status).

The runtime consists of vendored `scripts/produce_factorio_asset.py`, `export_sprites.py`, `render_sprite_frames.py`, `verify_sprite_master.py`, and `attach_factorio_prototype.py`. `tests/` runs the original fail-closed exporter/attachment tests plus portability checks. `.github/workflows/factorio-output-tests.yml` executes a real end-to-end smoke test with a generated Blender demo model.

All original source tools under `tools/art/` are retained; this independent copy makes the GitHub output recipe discoverable, teachable and reusable in other Factorio mods.
