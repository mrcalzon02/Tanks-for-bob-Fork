# Solar Boiler V3 — animation and visual proof checkpoint

**Repository:** `mrcalzon02/Tanks-for-bob-Fork`

**Source commit:** `d3a5148ab4b249740cb9550bc43c92143576ef19`

**Proof workflow:** https://github.com/mrcalzon02/Tanks-for-bob-Fork/actions/runs/42922593398

## Construction

- The original 3×2 V2 curved-parabolic solar thermal collectors, two actual focal
  receiver tubes and four continuous thermal lines are preserved in full, as
  are the copper steam drum, original FMPL ferrocrete PBR maps and boiler ports.
- The historical gauge pointer is retained as source but render-hidden. The
  new bronze-arbor pointer pivots at the real ivory gauge dial center.
- The existing copper pressure drum receives an actual emissive cylindrical
  heat jacket and restrained red light. The light was reduced after a real
  Cycles review revealed that its initial power washed out the dial.
- Four steam vent groups are attached to genuine source objects at the east/west
  hot thermal-line drum unions, steam extraction neck and steam-output flange.
  The west/east water inlets remain unvented. Each group has four phase-staggered
  animated vapor meshes with individually keyed 3D scale and position.

## Proof

The file `models/island-survival/solar-boiler/generated-v3/proof-qa.json`
contains independent real RGBA image checks for 68 native Cycles render views
(4 idle + 4×16 working), 8 fps, with 16 sample positions in the closed loop.
The `native-reopen-qa.json` record checks all source-preserving 3D geometry,
one 45-degree orthographic camera, packed FMPL maps, three exact standard
port fittings (face error under 1e-5 Blender unit), actual Blender animation
on frame 1 and matching frame 97, and four distinct physical steam joint IDs.

A six-image pilot renders three **same-frame controlled comparisons** before
full capture. Material, light, gauge and hide-render fcurves are temporarily
muted only for those comparisons, so Blender does not silently restore both
images to identical animation values. It records changed pixels as follows:

| Effect | Changed RGB pixels (12/255 threshold) |
| --- | ---: |
| Gauge left vs right | 46 |
| Thermal accumulator off vs on | 3053 |
| Four joint-vent groups off vs on | 136 |

Native visual evidence is at:
- `models/island-survival/solar-boiler/generated-v3/review-four-directions.png`
- `models/island-survival/solar-boiler/generated-v3/working-four-directions.gif`
- `models/island-survival/solar-boiler/generated-v3/solar-boiler-v3.blend`
- `models/island-survival/solar-boiler/generated-v3/preview-only-solar-boiler-v3-{idle,working}-{64,128,256}.png`

**Owner visual approval: pending. Game sprite attachment: not performed.
Native Factorio 2.1 smoke with these V3 sprites: not performed. Mod Portal
publication: not performed.**

No new workflow was created; the bounded one-shot trigger was retired after
verified publication. Rebuild from the checked-in V3 Python source and the
immutable V2 native Blender source using the commands in
`models/island-survival/solar-boiler/v3/README.md`.
