# Solar Boiler V8 — Floorless machine (Option A)

Source of truth is the real, independently verified editable V7 scene:
`../generated-v7/solar-boiler-v7.blend`.

**User-approved scope:** remove the 3×2 concrete base pad and its **ten**
perimeter concrete pavers. That is an actual deletion of **11 Blender mesh
objects**, not a visibility switch or a replacement material. **Retain** all
20 ground-locked functional supports: original cast boiler seating plinths,
steel saddle shoes, collector braces/stands, glass receivers, wooden cradles,
three Factorio grid-aligned fluid connections and original wood barrel.

This matches vanilla Factorio practice: underlying terrain/concrete/brick
floors remain supplied by player choice. Prototype footprint remains **3×2**
because the removed slab was only reference geometry, not game collision.

Keep the verified V7 gentle upper-body rumble, pipe shape-key flex, steam
venting, glass bubbles, all four directional views, one Wube 45° orthographic
camera, all source materials, no new embellishments.

## Existing reusable single-job production pipeline

```bash
python3 models/island-survival/solar-boiler/v8/remove_solar_boiler_floor_v8.py --self-check
blender -b -t 4 --factory-startup --python-exit-code 1 \
  --python models/island-survival/solar-boiler/v8/remove_solar_boiler_floor_v8.py -- \
  --output models/island-survival/solar-boiler/generated-v8 --render all --samples 24
blender -b -t 4 models/island-survival/solar-boiler/generated-v8/solar-boiler-v8.blend \
  --python-exit-code 1 --python models/island-survival/solar-boiler/v8/verify_solar_boiler_v8.py -- \
  --output models/island-survival/solar-boiler/generated-v8
/usr/bin/python3 models/island-survival/solar-boiler/v8/make_proof_sheet.py \
  --output models/island-survival/solar-boiler/generated-v8
```

QA reopens the .blend and checks all 11 removed objects are absent from
Blender datablocks; 20 structural supports have no evaluated-world vertex
drift at 20 frames; three Factorio pipe mouths and 33 wooden pipe mouth
cross-sections remain static; both glass tubes, 24 bubbles, 12 steam lobes,
16-frame loop, camera and real render PNG hashes are preserved. A real V7
vs V8 Blender comparison plus 4-direction contact and animated GIF are
produced from Cycles rendered frames. The transparent silhouette is measured
on every direction; 64/128/256px atlases are preview-only.

No game sprite substitution, tile occupancy changes or Mod Portal release
until owner visual approval.
