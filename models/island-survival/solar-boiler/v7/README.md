# Solar Boiler V7 — fixed ground, softer upper-body vibration

V7 is a **non-destructive derivative** of the already verified native
`../generated-v6/solar-boiler-v6.blend`. The immutable V6 scene, original
16×4 working frames, steam/glass animation, and previously committed evidence
remain untouched.

## What changes

- The concrete 3×2 pad, exterior pavers, seating plinths, saddle shoes,
  load-bearing collector supports and wooden seating cradles become genuinely
  grounded objects (no parent relationship to the shaking rig).
- The wooden pressure vessel, paired polished-wood concentrators, boiling
  glass focal tubes and boiling/steam effects remain animated.
- Upper-body rumble reduces to ~50% of V6 horizontal amplitude and <20% of
  its vertical amplitude. No rotating/moving camera.
- All 33 wood pipe sleeve flex channels are re-keyed with the same smaller
  motion. Their four-vertex root rings and all native 1×1 Factorio fluid
  connections remain fixed in world space.

## Actual native Blender capture

```bash
python3 models/island-survival/solar-boiler/v7/refine_solar_boiler_v7.py --self-check
blender -b -t 4 --factory-startup --python-exit-code 1 \
  --python models/island-survival/solar-boiler/v7/refine_solar_boiler_v7.py -- \
  --output models/island-survival/solar-boiler/generated-v7 --render all --samples 24
blender -b -t 4 models/island-survival/solar-boiler/generated-v7/solar-boiler-v7.blend \
  --python-exit-code 1 --python models/island-survival/solar-boiler/v7/verify_solar_boiler_v7.py -- \
  --output models/island-survival/solar-boiler/generated-v7
/usr/bin/python3 models/island-survival/solar-boiler/v7/make_proof_sheet.py \
  --output models/island-survival/solar-boiler/generated-v7
```

The native verifier checks actual evaluated world-space vertices at twenty
frames, including intermediate-frame interpolation, across **every anchored
mesh**, all three native pipe interfaces and 33 full timber socket ends. It
also checks the 97/1 closed loop, both live glass receivers, 24 boiling
bubbles, 12 steam lobes, 8 FPS, fixed Wube/FMLP camera and 68 Cycles PNG
hashes. Contact sheet, V6/V7 before–after render and 4-view GIF are generated
from the genuine Blender captures. 64, 128 and 256px atlases are review-only.

**Not authorized:** visual approval, replacing game sprites, changing
gameplay/footprint/pipe geometry, or publishing a Mod Portal release.
