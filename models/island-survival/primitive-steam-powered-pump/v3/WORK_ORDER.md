# Primitive Steam-Powered Pump V3 — accepted and integrated

The owner accepted the displayed V3 on 2026-11-15 and directed a small amount of
movement followed by integration and moving on. That supersedes the earlier
open cosmetic-rework plan. The final source retains that design and adds subtle
relief-lever/stem movement alongside the existing piston, flywheel and gauge.

The final editable master and actual inspected GLB are in
`../candidates/v3-production02/`. They retain all four immutable port meshes,
the 1x2 native pump, 0.206-tile stroke and rigid 0.6-tile rod. The single collinear
floor vertex was dissolved without changing the visible shape. Actual reimport
checks cover 97 poses, 21 embedded PBR images, explicit albedo/normal/metallic-
roughness channels, fixed ports, finite geometry and no degenerate triangles.

All **68** production PNGs are genuine Blender captures: four idle plus sixteen
working poses for each of four facings. `../candidates/v3-atlases02/` contains
six verified 64/128/256 atlases. The derived sprite capture unforeshortens the
stationary camera's ground-depth axis to match Factorio's square ground grid;
the editable master and GLB remain at exact unit scale. This fixes north/south
mouth diameter and placement without changing the approved source geometry.

The active 1.8.103 source loads
`prototypes/generated_graphics/primitive-pipe-pump-v3-production.lua` from
`data-final-fixes.lua`. It changes only pump animation and removes the unrelated
vanilla glass/fluid overlays. Fuel, pumping speed, health, recipes, research,
native connections and placement stay intact. No per-tick gameplay controller.

## Verified delivery

- `v3/FMPL_MODEL.json`: model/export/atlas hashes and delivery contract.
- `docs/art/primitive-pipe-pump-v3/engine-receipt.json`: Factorio **2.1.24** load,
  twelve placed pumps, 24 actual pipe connections, water and oil transfer, no-fuel,
  stop/restart, fully blocked output including internal storage, and save/reload.
- `docs/art/primitive-pipe-pump-v3/capture-receipt.json`: eight genuine graphical
  client screenshots, all four close views inspected against adjacent vanilla
  pipes. Temporary clients closed after capture.
- `build/pipe-pump-v3-package/tanks_for_bob_fork_1.8.103.zip`: installable package,
  source-byte verified. No Mod Portal upload and no user gameplay save modified.

## Test-fixture corrections retained in history

Factorio 2.1 makes `active` read-only; the fixture now uses
`disabled_by_script`. Stop tests allow existing output-buffer fluid to settle
before measuring continued transfer. A full-output test must fill the pump's
own 200-unit internal buffer as well as the output segment. The graphical
fixture now finds the engine's snapped pump positions by a small-radius query;
the initial exact-position east lookup caused the temporary capture popup the
owner reported. These are fixture corrections, not gameplay changes.

**Disposition: preserve this accepted pump and move to Fish Pond.**
