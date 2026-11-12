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

**Source status:** Script and dimensional/functional contract authored;
genuine Blender render, independent source reopen, visual acceptance and
Factorio sprite integration require their own receipts. Do not replace
the real `OffshorePumpGraphicsSet` with assembler or ordinary pump graphics.
