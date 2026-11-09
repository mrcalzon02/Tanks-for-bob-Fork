# Timber workbench V8 — one-tile sprite registration

**Scope:** graphical correction for the existing Tanks-for-Bob `workbench` entity, **Factorio 2.1**. Retains the V7 face-first hammer impacts, sparks, heating and cooling; only the graphical registration and overlarge selection outline change. No recipe, item, fuel, fluid, production speed or collision changes. The existing south-facing crude-oil output is preserved.

## Source provenance

Uses the actual V7 edited Blender source and 384 rendered RGBA frames captured on OLD-CORE30 in successful GitHub run [42574735569](https://github.com/mrcalzon02/HB-TTRPG-tools/actions/runs/42574735569), artifact `old-core30-repair-42574735569-1` (ID 13654023883). Source generator is `models/island-survival/blender/workbench-v7/workbench_v7.py`. The verified animation remains intact; this is **not** an image-generation replacement or a change to the 3D model. Existing source V7 scripts and ZIP are retained.

## Measurements and fit decision

Each source frame is 128×128. Idle alpha bounds across the four directions are 82–84 px wide by 89–91 px high, measured at alpha>20/255. At previous drawing `scale=0.5`, that spans **1.28–1.31 tiles wide and 1.39–1.42 tiles high**. The new `scale=0.33` spans **0.85–0.87 tile wide and 0.92–0.94 tile high**, with shift `(0,-0.07)` placing the resting legs within a single 32×32 px cell. The hammer may rise above the tile while moving; that is animation, not the 1×1 ground footprint. Former selection box `±0.9` was 1.8×1.8; now `±0.5` exactly matches the existing 1×1 collision/placement box.

The eight PNGs in `tanks_for_bob_fork_1.8.102/graphics/entity/workbench-v8-one-tile` are exact source-frame images or exact repacks; **pixel data was never altered or blurred**. They contain four 1536×1024 working sheets (12×8 each, 96 poses) and four 128×128 static idle images. Every one of the 384 unpacked cells was independently compared against the original rendered PNG pixels. `manifest.json` records source/archive hashes, offsets and all output hashes.

The visual-only integration uses `data-final-fixes.lua` so the original legacy graphics definition and all gameplay fields remain intact. Actual Factorio GUI visual acceptance, connected crude-oil pipe positioning and independent 2.1 graphical-client test remain **open**; passing image checks or a headless game launch is not equivalent to a zoomed-out in-game visual inspection.

## Reproduce from preserved artifact

```bash
python tools/art/workbench/pack_v7_one_tile.py \
 --input-zip /path/to/old-core30-workbench-v7-proof.zip \
 --out tanks_for_bob_fork_1.8.102/graphics/entity/workbench-v8-one-tile
```

Compare actual source frames at their two sizes in `docs/art/workbench-v8-one-tile/workbench_v7_one_tile_rest_proof.png` and `workbench_v7_one_tile_impact_proof.png`. A green outline corresponds to one 32×32 tile, magnified 5× for review.
