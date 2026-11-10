# Tanks-for-Bob Fork — 3D structure production order

This is the **survival / manufacturing structures** queue, separate from vehicle/tank art. Legacy first-pass OBJ geometry is not considered a production-ready `.blend`; state verification must inspect native source and actual sprite export evidence. Preserve every accepted source; never replace old assets in place. Use the canonical Tech-Priests FMPL asset library, actual Factorio tile/fluidbox dimensions, approved construction-pads/PBR, and one fixed calibrated 45° camera. User review precedes live graphics substitution.

## Current checkpoint (2026-11-10)

- **Cooking Fire V2: native Factorio 2.1.24 integration PASSED.** Byte-identical
  accepted four-view sprites and icon now reside in the actual active
  `tanks_for_bob_fork_1.8.102/` tree. Working and idle animation, the north
  steam input, native world creation, benchmark and server checks passed in
  [run 42893564032](https://github.com/mrcalzon02/Tanks-for-bob-Fork/actions/runs/42893564032).
  Source promotion commit: `5edcc5372e8758b142bfd32c6869db838f41a736`.
  A new Mod Portal release is a separate step.
- **Fish Pond V1: editable Blender candidate and cardinal review proof PASSED.**
  Actual Blender renders for 4 idle + 4 swimming directions, 64px checks,
  donor SHA, and saved native `.blend` reopen passed. See
  `models/island-survival/fish-pond/generated-v1/` in
  commit `fb3cb0da452a4bc7ac8295f24eb96f63583899d4`.
  Visual acceptance and full sixteen-frame four-direction production capture
  remain outstanding. **Do not replace live Fish Pond graphics yet.**
- **Solar Boiler V1: editable 3×2 Blender construction and cardinal proof PASSED.**
  Four idle and four working 256px Cycles renders, one calibrated FMPL 45°
  orthographic camera, 64/128px readability crops, true packed material maps,
  and native save/reopen checks are committed at
  `5ebc2d914ddde6ce941204b81f7a13d4b371b16e`.
  The owner-approved FMPL ferrocrete/ferrocrete_light/ferrocrete_dark
  PBR maps (9 total) were imported from the pinned Tech-Priests
  `939ff2d0fea5d236d7092b907c5f08961d5a7560` revision; custom
  copper/iron/reflective materials remain candidate finishes. Model-space
  west/east water and north steam mouth surfaces passed 128-vertex
  adjacent-pipe fit checks with error below 0.0000001 Blender unit.
  See [successful production run 42907291544](https://github.com/mrcalzon02/Tanks-for-bob-Fork/actions/runs/42907291544).
  Full sixteen-frame sprite atlas, native Factorio gameplay, and human visual
  acceptance remain pending; **do not replace live Solar Boiler graphics**.
- One-shot art/native push triggers were removed after their scoped jobs;
  the existing single-job manual workflows remain available.

## Production queue (next source: Steam Condenser)

1. **Fish Pond (V1 source/proof complete; awaiting visual approval)** — derived from Clay Pit V4c with one excavated basin, fitted water surface, four 3D swimming fish and editable tail strokes. Native source and eight cardinal proof renders are retained; proceed to complete animated atlases only after visual acceptance. Source: `models/island-survival/fish-pond/v1/build_fish_pond_v1.py`.
2. **Solar Boiler (V1 source and real Blender cardinal proof complete; awaiting visual review)** — new thermal collector/pressure-vessel model for the exact `type="boiler"` 3×2 footprint; three full-bore native-cell-mapped fittings: water west `(-1,+0.5)`, water east `(+1,+0.5)`, steam north `(0,-0.5)`. Source: `models/island-survival/solar-boiler/v1/`; native .blend, eight renders, test receipts: `models/island-survival/solar-boiler/generated-v1/`. No live sprite substitution until reviewed.
3. **Steam Condenser (next construction)** — rebuild for the active 3×3 Tanks `assembling-machine/steam-condenser` with north steam input at `(0,-1)` and south water output at `(0,+1)`. Start from reviewed condenser donor hardware and FMPL PBR/pipe fixtures, but do not paste the 2×2 Tech-Priests source wholesale. Create a visibly connected inlet → cooling body → condensate outlet, supported piping, and one 45° four-direction proof.
4. Primitive Steam-Powered Pump — real piston, rods and 1×2 model with measured north/south connections.
5. Beach Pump — unique shoreline lifting mechanism rather than inherited offshore pump graphics.
6. Stone Water Wheel — rotating stone-supported wheel and water outlet, rather than inherited offshore pump art.
7. Wood Basin — timber-stave cistern with fluid-level readout and accurate native ports.
8. Tank Ammunition Assembler — its own unique 3D machine, no longer duplicating Tank Assembler art; native north/south fluid links.
9. Tank Assembling Machine — dedicated heavy gantry, vehicle assembly bed and working motion.
10. Steam Compressor — pressure barrel, reciprocating drive, valves, and verified native fittings.
11. Quarry — stone excavation, hoist, and lifted material.
12. Shaler — moving crushing jaws and material feed/discharge.
13. Calcifier — mineral furnace, fuel/heat and exhaust.
14. Thinking Hut — timber, basic research tools, light and roof silhouette.
15. Pondering Hovel — evolved brick research shelter with lamp and chimney.

**Existing advanced model sources, not to rebuild from scratch:** Campfire V12, Clay Pit V4c, Pit Kiln V6, Lumberyard V2b (live ID `growing-plot`), Workbench V7/V8, Cooking Fire V2 (**native 2.1 integration passed**), Fish Pond V1 (**native Blender proof, awaiting visual acceptance**), and Solar Boiler V1 (**3×2 native Blender proof, awaiting visual acceptance**). The fish pond uses Clay Pit as a **donor**, not a second sculpt.

**Exclusions:** The Auto-Cannon Turret is a **Tech-Priests** asset, never a Tanks-for-Bob construction target. Tanks' dormant turret Lua is not a work authorization. Vehicle 3D art is tracked in a separate queue.

## Required asset evidence, per station

Source Blender `.blend` saved and independently reopened; source provenance and hashes; original base sprite comparison; genuine 64/128/256 RGBA preview with one 45° fixed camera, rotated model cardinal orientations; idle and working states where needed; verified seamless motion (no change in frame count unexpectedly); measured native tile footprint and fluid sockets when applicable; only then sprite/atlas export, Factorio client review, and optional integration. Do not create new GitHub Actions workflows for each machine.
