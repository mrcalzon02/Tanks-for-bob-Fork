# Fish Pond V1 — Clay Pit V4c derivative

**Stage:** Blender construction source, not yet rendered or approved. **No live game prototype, image, recipe, workflow, or release is changed by this source.**

The complete Clay Pit V4c native `.blend` is the authority. This builder opens that exact source, retains its one-piece excavated bowl, loose earth, original 45° orthographic camera, Cycles materials, and lighting, and removes only the clay-working props (bucket, hoist, shovel, lantern and their animation) *in the derivative*. The original source is never overwritten and is SHA-256 checked after the build.

The new pond has one elliptical water plane fitted inside the basin; four independent visible **3D fish** with closed tails and fins below the waterline; two render states: `idle` (water, no fish) and `working` (water and continuously swimming fish). Its 16-pose loop uses frames 1,7,...,91 with an exact frame-97 return, 8fps. The original source's **one fixed** orthographic camera stays at 45°; the model root rotates for four Factorio directions. No extra scene camera is created.

## Execution

From the repository root on a computer with Blender 4.3+ or 5.x installed:

```sh
python models/island-survival/fish-pond/v1/build_fish_pond_v1.py --self-check
blender -b --factory-startup --python models/island-survival/fish-pond/v1/build_fish_pond_v1.py -- \
  --out models/island-survival/fish-pond/generated-v1 --render all --samples 24
```

The builder fails if the target directory is not empty. `--render proof` saves the `.blend`, four idle PNGs and four working PNGs for a quick visual review. `--render all` saves the editable native scene and **68 true Blender renders** (4 idle + 4×16 working) with per-frame hashes in `build-report.json`. `--render none` saves the editable scene only.

Expected checks on the runner: Blender source reopening, four directions and the 16-frame cycle, fish visibility in idle/working, water coverage/shoreline, silhouettes at 64px, and a proper visual review before exporting Factorio atlases. The repository's old general exporter is *not automatically FMPL v0.4.0 compliant*; use the current pinned FMPL camera checks for final capture.

The `fish-pond` live prototype is still a 3×3 `assembling-machine` with north fluid input and south fluid output. That gameplay and native plumbing remain out of scope until graphics approval. Do not add decorative pipe mouths that have not been reconciled with native prototype positions.
