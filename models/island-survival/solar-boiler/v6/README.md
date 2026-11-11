# Solar Boiler V6 â Optical focal glass receivers and anchored rumble

**Source of truth:** `../generated-v5/solar-boiler-v5.blend`, validated by
SHA-256 against the committed V5 `build-report.json`. New work is a separate
editable Blender derivative; do not overwrite V5, V4, or the live Factorio
prototype.

## Corrections

- Hide the mistaken V5 above-barrel glass accumulator, its liquid, saddles,
  and end steam, but preserve the two V5 **wooden side-pipe roof repairs**.
- Convert the **two actual optical focal absorber lines** into hollow,
  imperfect glass thermal receivers: one inside each polished-wood parabolic
  concentrator. Endpoints are read from V2's saved physical hot/cold collector
  coordinates, so they are not new arbitrary glass cylinders.
- Each glass receiver contains a 3D colored water body, two distinct moving
  meniscus/foam surfaces with three animated shape keys, and twelve rising
  bubbles. The steam comes from small open relief holes on the ends of the
  glass receivers, **never** from sealed Factorio pipe connections.
- The entire wooden machine, including both parabolic concentrator roots,
  receives a tiny closed-loop shaking transform. The three world-aligned
  native Factorio collars, studs, and adjacent-pipe fixtures stay rigid.
  The 33 large bentwood inlet/outlet planks carry localized shape-key flex:
  zero displacement at the native pipe mouth, increasing toward the wooden
  machine. Small non-external pipes and barrel move with the machine.
- Retain 18 barrel staves, 65 existing bentwood planks, both corrected wooden
  side-pipe joins, both polished-wood reflectors, all packed Campfire V8 wood
  source materials, ferrocrete maps, original gauge and 3Ã2 occupancy.

## Capture and QA

16 working poses at 8 fps, frame 97 matching frame 1. The existing one-camera
45Â° FMPL capture rotates the model 0Â°, 90Â°, 180Â°, 270Â°; **never** four picture
cameras. Pilot output includes 4 idle images, **64 actual working Cycles
renders**, 6 real isolation renders (boiling bubbles, glass-end steam, wooden
rumble), true 64/128/256 preview-only atlases, a 4-view 16-frame GIF, and an
editable `.blend`. The exact saved Blender model is reopened independently.

QA measures frame-by-frame that the three unchanged native socket collar rings
still coincide with their original fixed reference pipe flanges while both
optical concentrators move. The wood large-pipe skin flex must be zero at the
connection plane. Other gates check two true focal glass tubes, 24 boiling
bubbles, four independently timed relief sites, glass and foam keyframes, the
absence of V5's misplaced above-barrel glass, packed materials, all 68
non-isolation frames and real effects at native 64px size.

### Existing runner commands (from repo root)

```bash
python3 models/island-survival/solar-boiler/v6/build_solar_boiler_v6.py --self-check
blender -b -t 4 --factory-startup --python-exit-code 1 \
  --python models/island-survival/solar-boiler/v6/build_solar_boiler_v6.py -- \
  --output models/island-survival/solar-boiler/generated-v6 --render all --samples 24
blender -b -t 4 models/island-survival/solar-boiler/generated-v6/solar-boiler-v6.blend \
  --python-exit-code 1 --python models/island-survival/solar-boiler/v6/verify_solar_boiler_v6.py -- \
  --output models/island-survival/solar-boiler/generated-v6
python3 models/island-survival/solar-boiler/v6/make_proof_sheet.py \
  --output models/island-survival/solar-boiler/generated-v6
```

**Not automatically authorized:** live Factorio sprite substitution, prototype
attachment, changing gameplay, Factorio Mod Portal publication or owner visual
approval. The 64/128/256 atlases are preview-only until reviewed.
