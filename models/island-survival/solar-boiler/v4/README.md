# Solar Boiler V4 — survival timber construction & steam correction

**State:** new editable V4 Blender derivative, owner visual review pending. The V3 historical `.blend` and live Factorio 2.1.102 sprite are not overwritten or retargeted.

## Corrections from owner review

- **Majority wood:** main large horizontal barrel becomes **18 separately warped stave planks** with wooden hoops and end planks; shaped wooden cradles support it. The original copper shell and V3 red glowing jacket are preserved in the `.blend` as **render-hidden historical geometry**, not the visible machine.
- **Side fluid conduits:** three main intake/output routes are now visibly made of **curving, loosely fitted timber staves**, with overlapping wood cinches. Four smaller collector-to-barrel sheath routes likewise use bentwood planks. Preserve the actual metal cavity/liner behind the wood, and the three original exposed **metal** native pipe flanges and their 128-vertex mating geometry. The pipe mouths remain open at exactly the Factorio grid edges.
- **Parabolic wood mirrors:** duplicate the exact verified V2 continuous paraboloid mesh as a **polished wood** reflector surface with UV-mapped inherited end-grain image maps, including brown rough timber backing and curved ribs. No blanket recoloring of metal into brown plastic. The focal metal absorber tubes are the only hot parts, with restrained bronze-warm emission.
- **Steam:** remove visible V3 spherical steam from sealed joints, water pipes and the steam pipeline flange. Keep a **real open relief nozzle on top of the barrel**, generating 4 primary plus 8 feathered steam wisps from physically bounded animated volume geometry. A procedural 3D noise mask attenuates volume density radially and vertically *before* the mesh edge; no white balls, particle-sheet overlays, opaque cones or hard plume silhouettes. Animate a loop across 16 poses / 97 closure, 8 fps, no simulation cache.
- **Approved textures:** wood material **maps are copied from the accepted Campfire V8 native `.blend`** (source materials are selected from the real `02 | Firewood` mesh slots; their names are not guessed) using the accepted V8 nonrepeating procedural grain/color and roughness system plus its packed original tangent-space normal maps. Local per-machine copies only alter roughness/clearcoat for sun-polished wood; original library shaders and maps remain unchanged. Preserve all nine packed source FMPL ferrocrete PBR images on the foundation.

## Source and artifact contract

- V3 source `models/island-survival/solar-boiler/generated-v3/solar-boiler-v3.blend`, SHA-256 verified against its own build receipt before opening. The source on disk is never written.
- Camera remains a **single fixed orthographic 45-degree, zero-azimuth FMPL camera**, with machine root rotations 0,90,180,270. No additional inspection or icon camera.
- Exact `solar-boiler` **3×2** Factorio `boiler` port contract: west/east bidirectional water and north steam; original metal machine/adjacent pipe mating annuli and native coordinates unmodified.
- Native output: `models/island-survival/solar-boiler/generated-v4/solar-boiler-v4.blend`, independently reopened and checked for wood source map provenance, open-mouthed pipe fit, no red jacket, genuine 3D steam and keyed gauge/receiver cycles.
- Pilot output: 4 cardinal idle + 4 cardinal working + 16 north-working real 256px Cycles PNGs; same pixel data yields a North GIF and 64px game-size diagnostics. This is **not yet a 64-frame four-direction production animated atlas** and cannot be deployed without the owner's visual review.

## Reproduce on the existing Blender runner

```bash
python3 models/island-survival/solar-boiler/v4/build_solar_boiler_v4.py --self-check
blender -b -t 4 --factory-startup --python-exit-code 1 \
  --python models/island-survival/solar-boiler/v4/build_solar_boiler_v4.py -- \
  --output models/island-survival/solar-boiler/generated-v4 --render pilot --samples 24
blender -b -t 4 models/island-survival/solar-boiler/generated-v4/solar-boiler-v4.blend \
  --python-exit-code 1 --python models/island-survival/solar-boiler/v4/verify_solar_boiler_v4.py -- \
  --output models/island-survival/solar-boiler/generated-v4
python3 models/island-survival/solar-boiler/v4/make_proof_sheet.py \
  --output models/island-survival/solar-boiler/generated-v4
```

Visual approval and live Factorio 2.1 integration are **separate gates**. No unrelated Tech-Priests assets, game prototypes, crafting recipes, technologies or releases may be edited by this modeling run. Reuse the existing one-job art workflow; do not add workflows or schedules.
