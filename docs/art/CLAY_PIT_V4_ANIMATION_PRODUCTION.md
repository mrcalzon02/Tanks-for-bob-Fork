# Clay Pit V4 — approved implementation scope, pending visual signoff

Preserve the V3 geometry and existing animated-capable primitive kit. This V4
changes only the darker blended wet-clay basin, the tiny wax-paper lantern
emission and a real swinging wooden water bucket suspended on a taut rope.
The wooden support and shovel remain fixed.

## Exact Blender implementation

- Source: models/island-survival/clay-pit/generated-v3/clay-pit-v3.blend
- Builder: models/island-survival/clay-pit/v4/build_clay_pit_v4.py
- V4 revision: new directory generated-v4; all older V1/V2/V2b/V3 art retained.
- Geometry: original V3 basin and wooden rig are unchanged.
- Wet material: one continuous procedural shader with V3's soft transitions
  retained; darker saturation ramp and a wider, irregular moisture gradient.
- Rig: ANIMATION | bucket and rope pendulum pivot at (.04,-.17,.57), parented
  to the model rotation root. Rope, bucket, staves, wooden handle ties and
  water surface are children of this pivot.
- Swing: six degrees left and right, exact cosine path keyed at source timeline
  1,7,13,...,91, plus frame 97 matching frame 1; auto-clamped Bézier motion.
- Lantern: wax-paper brightness and the small POINT lamp energy are both keyed.
  It stays mounted on the wooden post. Flicker multipliers for the sixteen
  samples are [.94,1,.965,1.07,.955,.99,1.055,.985,.915,1.015,1.06,
  .97,.93,1.01,1.045,.975]. Key at frame 97 equals frame 1.
- Frame 0 idle: no props/lamp. Working: 16 keyed samples, 8 FPS => two-second loop.
- Camera: fixed orthographic Factorio 45° structure camera; rotate only the
  model root 0°,90°,180°,270°.
- Capture: 4 idle plus 64 working transparent 256px Blender PNGs, per-frame
  SHA256 hashes, saved editable .blend, four 16-frame preview GIFs, comparison
  with the original sprite and versioned QA.

## Run one authoring pass

blender -b -t 4 models/island-survival/clay-pit/generated-v3/clay-pit-v3.blend --python-exit-code 1 --python models/island-survival/clay-pit/v4/build_clay_pit_v4.py -- --out /tmp/clay-pit-v4 --samples 20

Then:

python3 models/island-survival/clay-pit/v4/make_v4_review.py --out /tmp/clay-pit-v4 --mod tanks_for_bob_fork_1.8.95 --previous models/island-survival/clay-pit/generated-v3/idle-d00.png

Or run the Clay Pit V4 workflow in GitHub Actions, which additionally
reopens the Blender master, validates keyframes and saves all proof.

## Acceptance boundary

V4 is not an in-game replacement until user visual acceptance. It does not
change the existing clay-pit prototypes, recipes, fluid connections or active
sprite files. After acceptance, create a new production profile pointing at
generated-v4/clay-pit-v4.blend with states idle:[0], working:[1,7,...,91],
directions [0,90,180,270], camera 45°, and the tiny lantern listed as an
intentionally animated light. Then use the reusable Factorio sprite production
command and explicit assembling-machine/clay-pit attachment.

## V4b tuned lighting publication

The first full V4 diagnostic render had an overbright lantern. V4b lowers the point-light energy to 2.4, wax-paper emission to 0.16× the flicker multiplier, and inner candle emission to 0.78×; native Blender Cycles sampling increases to 32. Publish final tuned files to `models/island-survival/clay-pit/generated-v4b/` to preserve the first V4 render as diagnostic history and avoid overwriting prior binary evidence. The actual bucket pivot and lighting keys remain unchanged.
