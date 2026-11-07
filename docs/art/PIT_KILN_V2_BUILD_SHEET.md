# Pit Kiln V2 — hand-molded wet-brick staging and interior firing ring

The user clarified that the primitive kiln is a *clay pit with a campfire heating core*, where wet unfired bricks are placed along the inner slope so the pit reflects heat into them, without exposing bricks directly to flames. A small rough wooden slab supports a separate pile of wet hand-formed bricks before placement.

## Source truth and component reuse
- Source model: `models/island-survival/pit-kiln/generated-v1/pit-kiln-v1.blend`.
- Reuses the single continuous clay excavation inherited from Clay Pit V3, central crossed-wood fire, pale kiln stones and 16-frame fire light/animation.
- Adds **one actual rough wooden staging slab** resting against the outer upper/right pit lip, with **four wet hand-shaped bricks** on it (three bottom, one top).
- Places **ten separate crude unfired bricks** along the inner clay bank in a spaced, incomplete arc; no bricks inside the fuel/flame core, no engineered kiln wall.
- Clay brick materials are matte damp russet/umber/clay slip with noise and imperfect beveled edges. Wood is a hand-split crude board, not an industrial pallet.
- Idle: staged wet bricks and firewood, no flames and no firing-bank brick layout. Active: same staging pile plus ten green bricks along inner slope and central fire. This is a whole-state render, not overlay-compositing twice.
- Static brick placement during active animation; only the fire moves. No invented hands or automated placement mechanism.
- Four genuine model rotations 0, 90, 180, 270 degrees under the fixed 45 degree orthographic structure camera.
- 4 idle + 64 working 256px transparent Cycles PNGs, four looping GIFs, actual editable `.blend` and source/proof comparison. Original in-game pit-kiln sprites/prototype remain unmodified until art approval.

## One-run V2 production test
```bash
blender -b -t 4 models/island-survival/pit-kiln/generated-v1/pit-kiln-v1.blend \
  --python-exit-code 1 --python models/island-survival/pit-kiln/v2/build_pit_kiln_v2.py \
  -- --out /tmp/pit-kiln-v2 --samples 24
/usr/bin/python3 models/island-survival/pit-kiln/v2/make_pit_kiln_v2_review.py \
  --out /tmp/pit-kiln-v2 --mod tanks_for_bob_fork_1.8.95
```
GitHub Actions workflow: `.github/workflows/pit-kiln-v2.yml`, versioned published output: `models/island-survival/pit-kiln/generated-v2/`. Material/geometry visual acceptance remains separate from software and capture QA.
