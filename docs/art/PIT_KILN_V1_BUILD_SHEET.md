# Pit kiln — source-guided first reconstruction (V1)

The next C-block worksite after the clay pit is **pit-kiln**. The active mod prototype is assembling-machine/pit-kiln and refers to a 64x64 idle base sprite `graphics/entity/pit-kiln.png` plus a two-frame 128x64 flame overlay `graphics/entity/pit-kiln-w.png`. The item icon file is a 120x64 source sheet; only the in-game base 64x64 is the literal visual reference. The kiln's production recipe consumes a clay pit and a campfire; gameplay remains untouched.

## Visible source object list
- One ochre raised excavation lip and soft damp inner bank, inherited as real editable geometry from Clay Pit V3.
- Five to nine rough pale heat stones and dark ash/charcoal pieces clustered near the excavation center.
- Three crossed hand-laid fuel logs. These are small uneven sticks, not a brick structure or chimney.
- A few short additional fuel billets at the rim when active (existing source overlay).
- A small flame, yellow central tongues and orange outskirts; working animation is a full-object alternative state in this Blender prototype (not yet wired into the live mod).
- Source image is deliberately **not** being used as a billboard plane. No hidden mechanics, underside, kiln lining or industrial walls are invented.

## First-pass geometry and look
Re-use `models/island-survival/clay-pit/generated-v3/clay-pit-v3.blend` as the shared primitive earthwork kit. Remove clay pit's lantern, rope, bucket, shovel and support props. Preserve the V3 basin and feathered clay materials; add separate editable stone, coal, timber and flame objects with descriptive names. The stones are matte rough grey/ash-white with darker charcoal beneath. Retain the fixed orthographic 45-degree Factorio camera and a calibrated 3.55 Blender-unit framing.

## Native test
Run the dedicated `.github/workflows/pit-kiln-v1.yml`. It renders four idle directions and 16 animated burning frames at each cardinal angle, 68 true Blender PNG captures, four GIFs, a directly inspectable comparison sheet and a saved editable `.blend`. The original sprite paths and gameplay prototype remain unchanged.

Current status: greybox/first shader and animation pass. The kiln is **not** yet artist-approved, installed, or Mod Portal-published. Judge its material detail, stone placement and flame motion against the actual sprites before running the previously accepted Factorio production packager.

## V1 camera proof correction
The first CI pass rendered all 68 frames but the visible 90°/270° basin touched the transparent canvas. The independent alpha clipping check rejected it. Enlarging the orthographic scale from 3.15 to 3.55 preserves the calibrated 45° elevation and consistent four-view centering while leaving safe transparent margins. Never relax the clipping gate to hide real cut-off geometry.
