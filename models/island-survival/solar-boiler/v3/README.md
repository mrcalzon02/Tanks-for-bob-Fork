# Solar Boiler V3 — pressure, thermal accumulator and joint-steam animation

**Status: native Blender model/review candidate only.** No game sprite or gameplay
substitution and no release. V2's tested 3×2 footprint, three Factorio-aligned
physical ports, curved silver concentrators, real focal receiver pipes, four
stationary thermal lines, packed ferrocrete materials, and single calibrated
45° camera are preserved. The historical V1 and V2 `.blend` files are never
edited or overwritten.

This pass implements three tangible mechanisms:

1. **Gauge:** the previous pointer remains in the native file but is render-hidden;
   a new 3D pointer moves around the **true gauge-center pivot** and oscillates
   visibly through a closed 16-sample mechanical pressure cycle.
2. **Thermal accumulator:** a new 3D curved heating jacket fits directly over
   the center of the *existing* copper pressure drum. Its red-orange Cycles
   emission pulses from idle (off) through heated (on) states, supported by a
   localized red area of point-light illumination. Real retaining bands remain
   visible; there is no extra invented machine port or floating red plane.
3. **Pressure-joint steam:** 16 animated 3D vapor puffs, four staggered per joint,
   rise from the actual west/east **hot collector unions**, the steam extraction
   neck and the north steam-output flange. Water inlets do **not** emit steam.
   Earlier relief-valve vapor remains. The puffs drift and expand in four
   staggered cycles instead of all flashing together.

**Animation:** one idle frame at timeline 0; 16 sampled working frames at
`1, 7, ..., 91` and a matching closing key at frame `97`. Four orientations
rendered with the **same stationary** camera; 68 genuine 256×256 Cycles PNGs.
A 16-frame four-direction GIF, animated/idle atlas *previews* at 64, 128 and
256 pixels, 64px readability samples, and controlled isolated Cycles render
pairs for each effect are produced. The atlases are **not installed**.

## Reproduce on the existing Blender-capable runner

From the repo root (Blender 4.0+):

```sh
python3 models/island-survival/solar-boiler/v3/animate_solar_boiler_v3.py --self-check
blender -b -t 4 --factory-startup --python-exit-code 1 \
  --python models/island-survival/solar-boiler/v3/animate_solar_boiler_v3.py -- \
  --output models/island-survival/solar-boiler/generated-v3 --samples 24 --render all
blender -b -t 4 models/island-survival/solar-boiler/generated-v3/solar-boiler-v3.blend \
  --python-exit-code 1 --python models/island-survival/solar-boiler/v3/verify_solar_boiler_v3.py -- \
  --output models/island-survival/solar-boiler/generated-v3
/usr/bin/python3 models/island-survival/solar-boiler/v3/make_proof_sheet.py \
  --output models/island-survival/solar-boiler/generated-v3
```

Independent QA must prove the original V2 SHA-256 and all three 128-vertex
matching pipe planes survive, the canonical capture camera never rotates,
9 original FMPL PBR maps remain packed, loop frame 97 equals frame 1, all three
new effects actually change same-frame rendered pixels, and the output has
68 genuine Cycles frames without blank/overflowing alpha.

**Do not promote this candidate to Factorio until human visual review and
separate native game registration tests succeed.**

### Pilot-first rendering gate

The existing art workflow first runs a separate six-Cycles-image `--render pilot`
(needle extreme left/right, heat off/on, and joint vapor off/on at the **same**
frame). During each controlled comparison it temporarily mutes the corresponding
Blender animation channels, otherwise Blender's render dependency graph would
restore the same keyed value on both renders. A Pillow RGB pixel check requires
visible contributions for all three effects before the final 68-frame pass.
The pilot uses a scratch output and is never published as production art.

The hot jacket emission and local red-light output are restrained to preserve
pressure-gauge legibility and avoid washing the ferrocrete apron pink-white.
