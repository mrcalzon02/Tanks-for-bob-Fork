# Beach Pump V2 — Archimedes screw / waterwheel / large crank

New real editable Blender mesh and keyed working rig, replacing the previous
V1 wave paddle and diaphragm **inside the new Blender source only**. V1 donor
source, model and game are unchanged. Native primitive offshore-pump behavior
is unchanged: pulls water directly from the shoreline, produces 0.01/tick,
feeds the one south native pipe output at (0,+0.25), and needs no fuel/power.

## What is modeled (not a picture)

- Exposed 3-turn swept bronze Archimedes helix around a keyed inclined axis.
- Open timber cradle, braces, lower strainer and six actual blue-green water pockets.
- Timber water-trough with continuous colored water, ending in falling droplets.
- Vertical eight-paddle wooden wheel, real 3D spokes and hubs, rotating in phase.
- Large external eccentric crank arm and projecting wooden hand grip.
- Gearbox/input shaft visually couples the wheel to the screw.
- Catch sump plumbed into the unaltered FMPL single south full-bore fitting.
- The unchanged four separate FMPL stone footings, wood skids, one fixed 45°
  camera, packed V1 materials and stationary exact native pipe mouth.

The waterwheel-driving-its-own-screw loop is an intentionally **stylized**
mechanism: the visual motion is synchronized; this is not an assertion that
the model is a physically self-powered perpetual-motion device.

## Reproducible native Blender

```sh
python models/island-survival/beach-pump/v2/build_beach_pump_v2.py --self-check
blender -b --factory-startup --python-exit-code 1 \
  --python models/island-survival/beach-pump/v2/build_beach_pump_v2.py -- \
  --out models/island-survival/beach-pump/generated-v2 --render proof --samples 16
```

Production is 4 idle and 64 true Blender Cycles working frames (16 poses at
8 FPS, loop frame 97 identical to frame 1), rotated 0/90/180/270 beneath the
same fixed camera. A new verified output directory is required, no overwrite.

**Native Blender 5.2.3 status: PASS.** The new editable V2 machine was built and
independently reopened in [Core30 run 43287477872](https://github.com/mrcalzon02/Dens-Mortis/actions/runs/43287477872).
The [genuine four-direction Cycles render](../generated-v2/review-four-directions.png)
and actual Blender model-source QA receipts are committed alongside the source.

The original source is 3,399,311 bytes; SHA256
`ee9c9ba560f8b28a580c7307e642f1f6c420627a3165131a0c4f6b53987d0646`.
Its 12 Git source parts are **byte-identical** to the independently reopened
Blender master, verified by post-commit readback. Reassemble the actual
editable file from a Git checkout:

```sh
python3 models/island-survival/beach-pump/generated-v2/assemble_native.py
```

Native QA proved the 580-vertex helical flight, eight-paddle wheel, large
external rotating crank, visible water pockets and trough-to-wheel drops,
exact loop seam and both stationary full-bore pipe-fitting meshes.

**Still pending:** full 68-frame production atlas export, owner visual
acceptance and in-client Factorio 2.1 offshore-pump graphics check. Do not
replace live graphics or alter the shoreline-to-pipe water mechanics.
