# Solar Boiler V2 — parabolic thermal reflector correction

**Status:** editable Blender source and real eight-view rendered proof; **not** yet approved or integrated as a Factorio sprite replacement.

## Why V1 needed rework

V1's alleged concentrating reflectors were **flat rectangular reflective strips**, with a large black tube passing over the center at an arbitrary elevation. They could read as blocked photovoltaic panels; neither interpretation represented a sound solar heat collector. V1's animated tilting troughs also conflicted with its rigid heat-transfer lines, which did not follow their movement.

## V2 construction contract

Each of the two collectors has a continuous closed steel-backed **parabolic mirrored trough**, polished silver/neutral rather than a rectangular grid of photovoltaic modules. Its cross section in local Blender units is **z = y² / (4f)** with focal height **f = 0.28** and aperture half width **0.34**. The thin, hollow black absorber tube runs longitudinally at **(y=0, z=f)**; end rings, curved structural ribs and physical tube standoffs support it. The actual mirror mesh is generated from this same equation—not inferred from a render. Ray-reflection checks establish that locally vertical incident rays meet the absorber line to numerical tolerance. The camera captures are for model proof, not photon simulation.

The troughs are fixed at a slight tilt and remain sky-facing. The previous unconnected rigid animation is removed. Each absorber has **two physical thermal fluid lines**: a hot outlet and a cool return, both modeled as hollow routed tube meshes. Their endpoints are verified against the absorber ends, seated into the pressure drum, and remain joined at idle/working frames. The prior `solar-boiler-v1.blend` stays immutable; derivative modeling replaces only V1's flat mirror/rod parts and the two wrong transfer lines. Source asset hashes and actual input/output coordinates are checked.

The existing **3×2** pad, PBR ferrocrete textures, boiler body, gauge, relief vapor and native-boundary water-west, water-east and steam-north collars remain unchanged. All three standard 0.57 OD / 0.49 bore / 0.68 flange interfaces and measured game-cell mapping survive. They are geometry assertions, **not** proof of native Factorio gameplay.

## Execute

From repo root, with Blender 4.0+ installed, using only the existing runner:

```bash
python3 models/island-survival/solar-boiler/v2/refine_solar_boiler_v2.py --self-check
blender -b -t 4 --factory-startup --python-exit-code 1 --python models/island-survival/solar-boiler/v2/refine_solar_boiler_v2.py -- --output models/island-survival/solar-boiler/generated-v2 --render proof --samples 24
blender -b -t 4 models/island-survival/solar-boiler/generated-v2/solar-boiler-v2.blend --python-exit-code 1 --python models/island-survival/solar-boiler/v2/verify_solar_boiler_v2.py -- --output models/island-survival/solar-boiler/generated-v2
python3 models/island-survival/solar-boiler/v2/make_proof_sheet.py --output models/island-survival/solar-boiler/generated-v2
```

An independent second Blender process reopens the derived file and checks the actual curved reflector vertices, optical focal line, physical thermal connections, unchanged native port mating surfaces, packed FMPL PBR images, and exactly one original 45° camera. The 4 idle + 4 working views and two real-size 64/128px samples are captured from this single fixed camera. **No new workflow or game graphics attachment.**
