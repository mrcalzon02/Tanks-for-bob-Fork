# Clay Pit V2b — continuous wet-bank material correction

The first V2 physically modeled the user's confirmed wood/wax-paper lantern on the pole top, a rope, a water-filled wooden bucket, and the shovel over the lip. Its eight native Blender renders passed, but visual inspection revealed a **polygonal hard seam** where the dark wet region met the lighter clay slope. This is a material error, not part of the source sprite.

V2b preserves the entire previously committed V2 source and generated candidate under `models/island-survival/clay-pit/generated-v2/`; a new script and new output under `generated-v2b/` replace per-face angular wet/dry transitions with one continuous noisy Y-gradient based on the model's own generated texture coordinates. Subtle procedural grain is retained, specular remains matte. No new pits, poles or machinery. Lantern, rope, bucket, shovel and 45° four-way camera stay exactly as modeled in V2.

Reproduce with:

```bash
blender -b -t 4 --python-exit-code 1 --python models/island-survival/clay-pit/v2b/build_clay_pit_v2b.py -- --out /tmp/clay-pit-v2b --samples 28
/usr/bin/python3 models/island-survival/clay-pit/v2/make_v2_review.py --out /tmp/clay-pit-v2b --mod tanks_for_bob_fork_1.8.95 --v1 models/island-survival/clay-pit/generated-v1/working-d00.png
```

Workflow `.github/workflows/clay-pit-v2b.yml` builds eight real RGBA views and verifies alpha, unique directions, source sprite comparison, saved `.blend` independent reopen, and GitHub publication. V2b is **NOT production-approved or installed**. Render proof must be displayed inline before acceptance.
