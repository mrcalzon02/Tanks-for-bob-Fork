# Primitive Steam-Powered Pump V1 — original 1x2 Blender machine

This is the next Tanks for Bob island-survival machine after the Steam Condenser.
The live prototype is an actual **pump**, not an assembling-machine. Its live
native ports are **north output at (0,-0.75)** and **south input at
(0,+0.75)**. These are not the integer coordinates of the other water machines.

The true external full-bore flange planes sit at Blender Y +1 / -1 on the
1x2 tile border, Z .36. Ports, elbows, pipe casing, and foundations are static.
The exposed copper drive piston, wooden crosshead, hand-made flywheel, connecting
rod, gauge needle, steam pressure relief and water-level sight have independent
real geometry; the drive is a seamless 16-pose loop at eight FPS.

The parts are original and restricted to the 1x2 machine. Original wood/aged
metal procedural surfaces are supplemented by a verified packed FMPL ferrocrete
material from the accepted Solar Boiler V8, used only on small ground footings.
No full raised square concrete floor is attached; the game terrain remains visible.

## Genuine Blender execution

Run from repository root with Blender 5.2 on a **trusted** worker:

```sh
python models/island-survival/primitive-steam-powered-pump/v1/build_pump_v1.py --self-check
blender -b --factory-startup --python-exit-code 1 \
  --python models/island-survival/primitive-steam-powered-pump/v1/build_pump_v1.py -- \
  --out models/island-survival/primitive-steam-powered-pump/generated-v1 --render proof --samples 16
blender -b models/island-survival/primitive-steam-powered-pump/generated-v1/pump-v1.blend \
  --python-exit-code 1 --python models/island-survival/primitive-steam-powered-pump/v1/verify_pump_v1.py -- \
  models/island-survival/primitive-steam-powered-pump/generated-v1
```

The builder refuses to overwrite output, checks SHA256 of both immutable
references, appends only measured template collars/throats, creates the model
and a fixed 45-degree orthographic camera, and saves a native editable .blend.
`--render proof` creates eight genuine PNGs (idle/working x four rotations);
`--render all` makes 68 genuine frames. Actual native Blender reopen and image
checks are required before marking rendering complete.

**Status:** authored source, not yet independently rendered or approved.
The current vanilla pump graphic remains live. Do not set new `pump.animations`
until 2.1 pump schema, native pipe overlay, four game rotations, production
atlas and actual client visual review are validated. No workflow duplication,
gameplay edits or release in this stage.
