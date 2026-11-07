# Clay Pit V3 — feathered color and wet-clay edges
V3 retains the V2b excavated basin geometry, wood-and-wax-paper lantern on the support, rope, water-filled wooden bucket, shovel, and four 45° structure-camera views.
V2b used separate physical materials across some annular faces; these caused visible edge bands despite the per-material noise. **V3 assigns one continuous generated-coordinate material to every basin polygon** and blends an eased radial ochre-to-clay palette with a broad directional wetness field. Macro noise breaks the transition subtly and fine noise adds matte clay grain without glossy specular highlights. The large foreground dark wet area feathers naturally toward the back bank.
No existing V1, V2, V2b or Factorio in-game sprites are overwritten. V3 is not visually accepted until direct comparison.
Reproduction:
```bash
blender -b -t 4 --python-exit-code 1 --python models/island-survival/clay-pit/v3/build_clay_pit_v3.py -- --out /tmp/clay-pit-model-v3 --samples 28
/usr/bin/python3 models/island-survival/clay-pit/v2/make_v2_review.py --out /tmp/clay-pit-model-v3 --mod tanks_for_bob_fork_1.8.95 --v1 models/island-survival/clay-pit/generated-v2b/working-d00.png
```
Workflow `.github/workflows/clay-pit-v3.yml` captures and checks 8 genuine Blender source renders, the editable .blend, exact sprite comparison and one-material basin invariant, and commits the proof to `models/island-survival/clay-pit/generated-v3/` while preserving previous versions.