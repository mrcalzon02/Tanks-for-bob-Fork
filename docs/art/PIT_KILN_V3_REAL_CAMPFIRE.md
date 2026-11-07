# Pit Kiln V3 — reuse the actual existing animated campfire, not invented flames

The user correctly called out that Pit Kiln V1/V2 created eight *new generic flame tongues* instead of using our already-built, tested and approved animated campfire source.

**This is corrected in V3:** load the six original keyed `flame_tongue*` Blender mesh objects and the original keyed `04 | animated fire light` object **directly** from the archived `models/island-survival/blender/generated-v9/campfire-v9-animated.blend`. Their actual authored Blender animation actions, meshes, textures/materials, and light curves are retained. Remove ALL eight synthetic kiln V1/V2 flame objects and its substitute light; never stack duplicate fires. Scale and offset the imported assembly to fit the V2 kiln hearth; preserve the exact frame sampling at 1,7,13,...91, 16 frames at 8 fps.

The imported Blender source is named and SHA256-recorded in `build-report.json` alongside the actual action names. The model continues to reuse the native clay-pit earthwork basin plus V2's wooden staging slab, four unfired bricks on the board, and ten bricks around the inner wall outside the flame core.

Four actual 45-degree orthographic orientations, four idle renders, 64 active renders, the saved native `.blend` and animated GIF previews are required. GitHub CI independently reopens the Blender master and verifies source objects/animation actions, actual source frame hashes, distinct animated frames and presence of original V2 bricks.

**Do not install or promote until visual review.** V1 and V2 stay preserved, as do live Factorio prototypes. This is a correction to animation source authenticity, not permission to alter gameplay.
