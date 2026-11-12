# Beach Pump V3 — genuine native Blender visual QA (candidate only)

**Technical render PASS. Human visual review FAIL / further refinement required.**
Real self-hosted Blender 5.2.3 run: https://github.com/mrcalzon02/Dens-Mortis/actions/runs/43302753995

- [Native four-direction contact sheet](review-four-directions.png): four idle + four working real Blender images.
- [8 FPS animated review](motion-review.gif): four concurrent cardinal views, 16 genuinely rendered Blender Cycles animation frames per view.
- [Build report](build-report.json), [native .blend independent reopen](native-reopen-qa.json), [render frame hashes](proof-qa.json), [six atlas receipts](candidate-atlas-qa.json).
- [V3 editable source](../v3/) regenerates genuine Blender model, frames, motion GIF and atlases.
- The actual native editable V3 master (.blend) is retained on the authorized Core30 runner and SHA256-confirmed in the original run logs, but is not yet Git-published as a whole file.

### Actual native 68-frame cycle
16 working steps x four directions plus four idle; frame 97 equals frame 1. V3 checks moving wheel/crank, keyed trough glints, real curved wheel meshes and stationary native fixture fitting.

Source .blend SHA256: `7ab069297904d21b23d9e84a1210130fe324d5b18d1cd4384ba436e68ea97928`
Contact sheet SHA256: `ae9a1ec44d36cb122bba1d13715af08cdd955fc6cad08d961f3de3ec46c7a44e`
Animated GIF SHA256: `674d8ab7d8f1f3751aea1f323ab0f1437bd7858fae1dd5b063a29273e52d7cc9`

### Visual audit status
V3 improves distinct mesh profiles, smaller metal housings and more exposed screw, but the raised rectangular deck and waterwheel readability at 64px remain visually unsatisfactory. This is *not* approved and must not replace original mod entity sprites. Native Factorio shoreline/pipe visual test remains outstanding. Original V1/V2 models and gameplay preserved.
