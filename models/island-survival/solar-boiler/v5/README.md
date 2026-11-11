# Solar Boiler V5 — glass accumulator, active boiling and wooden socket repair

Source-of-truth input: `../generated-v4/solar-boiler-v4.blend` (sha256 in its build receipt). Never overwrite the V4 source. The full machine remains constructed from approved V4/Campfire V8 wooden planking and polished timber parabolas, with the 3x2 native pipe mouths and 45° capture unchanged.

Changes in the new **editable Blender V5 derivative**:

- One irregular **hollow glass accumulator** with inner/outer walls and imperfect roughness; two vented glass end membranes and very small bronze edge hardware. It sits in physically supported notched wooden saddles above the main wooden barrel. No red-hot central copper shell or featureless orange tube.
- Visible 3D mineral-water liquid volume, keyed water meniscus with three independent 16-pose shape-key churning modes, a moving real foam crest, and at least 20 independent rising bubbles inside the glass. Idle has relatively still liquid; working shows roiling liquid.
- **Alternating, intermittent steam jets at the west and east glass end-cap vent holes**; a physically separate open jet on each end. Per-end gas lobes are 3D, volumetric and noise-feathered rather than hard spherical steam meshes. Previous roof-relief V4 gas wisps are render-hidden; no gas from native sealed pipe hookups.
- Two anatomically fitted **off-center wooden annular end-cap socket patches** with real 0.132-tile bores repair the missing wood above the two major side-pipe joins without plugging fluid passages. Preserve the original three metal pipe mouths and mating jig exact.

Current work order is pilot proof: four idle directions, four working directions, a 16-frame active north cycle, and four controlled Cycles effect-isolation renders to verify liquid and steam contributions at 256 and 64 pixels. Save the independent native `.blend`, genuine render contact sheet, and looping GIF. Full four-direction animated atlas and Factorio gameplay/sprite deployment remain gated by user visual acceptance. No additional workflows; reuse one existing bounded art workflow and retire its temporary trigger after completion.

Run on the existing Blender-capable runner from repository root:

```bash
python3 models/island-survival/solar-boiler/v5/build_solar_boiler_v5.py --self-check
blender -b -t 4 --factory-startup --python-exit-code 1 --python models/island-survival/solar-boiler/v5/build_solar_boiler_v5.py -- --output models/island-survival/solar-boiler/generated-v5 --render proof --samples 24
blender -b -t 4 models/island-survival/solar-boiler/generated-v5/solar-boiler-v5.blend --python-exit-code 1 --python models/island-survival/solar-boiler/v5/verify_solar_boiler_v5.py -- --output models/island-survival/solar-boiler/generated-v5
python3 models/island-survival/solar-boiler/v5/make_proof_sheet.py --output models/island-survival/solar-boiler/generated-v5
```

No live prototype/release modification is authorized by this work order. Preserve V4 original for independent restore/diff.
