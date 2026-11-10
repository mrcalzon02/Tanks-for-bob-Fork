# Solar Boiler V1 — 3×2 native Blender thermal collector

**State:** fresh editable 3D source with four cardinal idle/active proof views;
**not a replacement for the existing live sprite or any Factorio recipe**.

## Authoritative game geometry

The active `tanks_for_bob_fork_1.8.102` prototype is a real `boiler`, not an
assembling machine, occupying **3×2 tiles**. Its `fluid_box` water connections
are WEST `(-1,+0.5)` and EAST `(+1,+0.5)` (both `input-output`), and its
`output_fluid_box` steam output is NORTH `(0,-0.5)` (`output`). Local Blender
+Y is north, so the matching **machine boundary planes** are west
`(-1.5,-0.5,.36)`, east `(+1.5,-0.5,.36)` and north `(0,+1,.36)`.
These are visibly modeled full hollow hardware at the three separate ports;
actual native pipe-cell compatibility still needs a Factorio 2.1 in-game test.

`port-contract.json` retains the exact in-game cell and model-space mapping.
The connector hardware follows the measured Tech-Priests Boiler V05 / FMPL
`factorio-fluid-interface-v1`: barrel 0.57, bore 0.49, full collar 0.68,
thickness 0.075 Blender units. Each collar has eight actual fasteners, a hollow
reducer connected to the drum, and a separate render-hidden adjacent-pipe jig.

## What the source contains

An original three-tile ferrocrete equipment foundation with discrete paved
brick edging, true copper pressure drum and cast support saddles, two framed
solar-thermal reflective troughs with absorber pipes and actuating tilt,
physical hot collector conduits, west/east hollow water lines and north steam
output, a keyed pressure gauge and short relief vapor emitted from a real valve.
The boiler is thermal; it does **not** depict photovoltaic panels supplying
an imaginary electrical port.

**PBR authority:** the original ferrocrete, ferrocrete_light, ferrocrete_dark
albedo/ORM/normal map triplets from the *owner's* Tech-Priests industrial
library, imported using that library's own Blender importer at pinned FMPL
commit `939ff2d0fea5d236d7092b907c5f08961d5a7560`. The exact
source images are **packed into the native .blend**, not re-vendored or
regenerated in Tanks. All nine map blobs are verified against the FMPL catalog.
Other new copper, iron, brass, reflective and vapor finishes are explicitly
procedural candidate materials, **not** claimed to be inherited FMPL PBR.

The new scene uses one FMPL canonical 45-degree/zero-azimuth orthographic
camera and rotates only the machine root for four directional captures. No
additional picture cameras. A 16-key cycle records panel/relief motion but
only two poses per direction are rendered in this bounded **V1 proof**, with a
repeatable 64/128/256 pixel readability set. Full 16-frame atlas/export is a
separate acceptance step.

## Build / native reopen

Run from repository root on the existing Blender-capable CI runner:

```sh
python3 models/island-survival/solar-boiler/v1/stage_fmpl_source.py --output "$RUNNER_TEMP/solar-fmpl"
python3 models/island-survival/solar-boiler/v1/build_solar_boiler_v1.py --self-check
blender -b -t 4 --factory-startup --python-exit-code 1 \
  --python models/island-survival/solar-boiler/v1/build_solar_boiler_v1.py -- \
  --fmpl-root "$RUNNER_TEMP/solar-fmpl" \
  --output models/island-survival/solar-boiler/generated-v1 --render proof --samples 24
blender -b -t 4 models/island-survival/solar-boiler/generated-v1/solar-boiler-v1.blend \
  --python-exit-code 1 --python models/island-survival/solar-boiler/v1/verify_solar_boiler_v1.py -- \
  --fmpl-root "$RUNNER_TEMP/solar-fmpl" \
  --output models/island-survival/solar-boiler/generated-v1
python3 models/island-survival/solar-boiler/v1/make_proof_sheet.py \
  --output models/island-survival/solar-boiler/generated-v1
```

Do not replace an earlier output folder. Do not promote the original vanilla
boiler sprite or recipes, change gameplay, create a new workflow, or claim
Factorio runtime/visual acceptance from the Blender-only V1 receipts.
