# Stone Water Wheel — ongoing authored production

Target: `offshore-pump/stone-water-wheel` in active source 1.8.103 at
`7290824bf43711d0bb31bd8e2969c51459864f91`. This is the first of ten substantial
structure production targets. Preserve accepted machines and the existing game art.

Native contract: collision `{-0.6,-1.05}..{0.6,0.3}`, selection
`{-0.6,-1.49}..{0.6,0.49}`, tile width/height 1/1, source offset `(0,-1)`,
water output `(0,+0.25)` facing south, pumping speed **0.5 per tick**, void
energy source. Do not accidentally copy Beach Pump's 0.01 pumping speed.
The source-derived visual mouth `(0,-0.49,0.36)` is nominal modeling placement;
it requires independent native offshore-pump registration and is not a proven
fluidbox-to-render conversion.

Canonical connector: `factorio-fluid-interface-v1`, exact native SHA256
`af6d1d74f0439b327b0b4e496386aa35fdac0859c177b55707dbfb5243e691ca`.
Preserve full bore 0.49, collar OD 0.68, barrel OD 0.57, centre height 0.36.
FMPL camera authority is consumed from the pinned
`939ff2d0fea5d236d7092b907c5f08961d5a7560` library. The two actual policy files
are verified separately from the current local Tech-Priests worktree, whose
capture_policy.py has changed. No claim that the entire consumer checkout passed.
Original FMPL ferrocrete image bytes were read back against the catalog's
`b16f98c6e62d0a82697fd01eaa3fc6953c35ccde` source and checked before use.

## Current state

**Owner steering, 2026-11-15:** lifting buckets must stay upright. This study
modeled the separate shoreline intake; current production focus moves to the
existing Primitive Steam-Powered Pump, the actual pipe-to-pipe pump. Both have
real recipes/research. Preserve the wheel studies as rejected/held, not production.
V2 pilot02 also has 16 degenerate triangles on bored receiver planks and visible
race-joint defects; its overall technical inspection failed. Do not promote it.

**V1 rejected by owner as rough on 2026-11-15. V2 refinement is in progress.**
The first candidate is retained as a failed study, not an approval reference.
It cannot be installed or marked complete. Genuine V1 editable source, animated
GLB and four-direction pilot renders exist in `../candidates/v1-pilot05/`.
The V2 builder is `../v2/refine_stone_water_wheel.py`; it replaces block geometry
with fitted curved timber, tenoned spokes, shaped scoops, hollow bearings,
carved bearing seats, an open receiver with a real outlet bore and a continuous
supported discharge race. Unique timber/stone albedo, normal and roughness maps
are packed; FMPL ferrocrete remains restricted to structural feet.

## Gates

| Gate | Status | Evidence / limitation |
| --- | --- | --- |
| P00 baseline | IN_PROGRESS | Current prototype inspected; exact original inherited base-game sprite comparison still needed |
| P01 engine prototype/version | PENDING | Existing source targets 2.1; no new native test yet |
| P02 art source/license | IN_PROGRESS | Original geometry/maps, verified owner-authored FMPL maps and canonical fixture; final manifest pending |
| P03 Blender MODEL reopened | IN_PROGRESS | V1 reopened; V2 independent reopen and construction review pending |
| P04 community export preset tested | PENDING | Existing local FMPL camera/Blender adapter used; no external add-on pass claimed |
| P05 RENDER camera/lighting calibrated | IN_PROGRESS | Canonical fixed 45-degree matrix validated; native sprite calibration pending |
| P06 idle/working layers verified | IN_PROGRESS | Above/underwater passes use world-height holdouts; validate current outputs |
| P07 Blender output frames exported | IN_PROGRESS | Four-way pilot only; no accepted full production batch |
| P08 sheet and Lua export verified | PENDING | No production atlas or prototype substitution |
| P09 automated sprite QA | IN_PROGRESS | Independent native/export checks under repair; no overall PASS |
| P10 exact Factorio client tested | PENDING | Shoreline, output/full/landfill, pipe registration, stop/restart and reload remain |
| P11 human visual art approval | PENDING | V1 explicitly rejected; V2 has no owner approval |
| P12 committed/published/read back | PENDING | Local artifacts; source checkpoint/publication pending |

## Append-only defects and review

- 2026-11-15 / V1: owner rejected rough construction. Reopen source, surface,
  render, export and visual gates; do not propagate a full batch. V2 is a real
  construction revision, not extra subdivisions or a renamed atlas.
- V1 pilot01: Blender image load used unresolved relative paths; repaired to
  absolute paths. Failed study preserved.
- V1 pilot02/04: sandbox temporary image export failed; source retained; exact
  Blender operation rerun with approved runtime access. Never label failed exports PASS.
- V1 pilot03: collector intersected the spinning wheel. The receiver was moved
  clear, then rebuilt as an open plank vessel in V2.
- V1 independent GLB inspection: a 0.00114578-tile bounds discrepancy came from
  comparing source frame 1 with an interpolated imported pose at Blender's 24 FPS.
  Inspect the export's declared first timestamp, converted to the imported scene
  frame/subframe. Exact-pose geometry checks then proceeded without loosening tolerance.
- V1 layer check exposed hidden surfaces through complementary transparent
  geometry. Replace transparent masking with holdouts so the first visible surface
  occludes the other pass. Current split must still be independently checked.
- V2 pilot01: periodic stone texture read as woven, supports hid too much wheel,
  race segments missed the receiver and the outlet lacked a true bored wall.
  V2 pilot02 replaces the stone field with nonperiodic multiscale mineral detail,
  narrows the piers, joins the race into the vessel and bores its front wall.

## Resume

Inspect the latest V2 source and actual GLB; view front, rear, close and clay
proofs and a real motion comparison. Repair construction, water pickup/discharge,
texture density and moving clearance before full 16-pose cardinal capture.
Keep native socket placement fixed during those repairs. Package 64/128/256
states with correct separate shoreline layers, then test a disposable Factorio
copy. Present concrete revised art for visual disposition before active replacement.
Register the accepted source/export with canonical FMPL only after its receipts pass.
