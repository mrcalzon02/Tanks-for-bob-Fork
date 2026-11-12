# Tanks-for-Bob Fork — 3D structure production order

This is the **survival / manufacturing structures** queue, separate from vehicle/tank art. Legacy first-pass OBJ geometry is not considered a production-ready `.blend`; state verification must inspect native source and actual sprite export evidence. Preserve every accepted source; never replace old assets in place. Use the canonical Tech-Priests FMPL asset library, actual Factorio tile/fluidbox dimensions, approved construction-pads/PBR, and one fixed calibrated 45° camera. User review precedes live graphics substitution.

## Current checkpoint (2026-11-11)

- **Solar Boiler V8: production integrated; graphical-client diagnostics remain open.**
  The user-approved floorless editable native V8, 4 idle + 64 genuine working
  Blender frames, 16-pose 8 FPS loops and full 64/128/256 preview atlases are
  published in `models/island-survival/solar-boiler/generated-v8/`. The
  3×2 production `BoilerPictureSet` directional graphics are installed in
  `tanks_for_bob_fork_1.8.102/graphics/entity/solar-boiler-v8/` and registered
  by `prototypes/generated_graphics/solar-boiler-v8-production.lua`. The
  native Factorio **2.1.24** engine load and 12/12 physical water/steam pipe
  connections across all four facings passed [run 43120594298](https://github.com/mrcalzon02/Tanks-for-bob-Fork/actions/runs/43120594298).
  V8 integration: [commit d60230f](https://github.com/mrcalzon02/Tanks-for-bob-Fork/commit/d60230ff8c5a3331de5a15e9da6b74b885595f1e).
  The true 1.0× and 2.9× in-client screenshot capture fixture and 16-image
  comparison matrix were refined in [commit e4c201c](https://github.com/mrcalzon02/Tanks-for-bob-Fork/commit/e4c201c1964e65a6baa4f886a66a9b19bdc0bbc6).
  **Unresolved visual diagnostic:** no genuine interactive client screenshots
  have been reviewed; Core30 service Session 0 is barred from rendering and
  a one-shot cross-session Task Scheduler registration failed with Windows
  `0x80070005` permissions. Preserve [issue #4](https://github.com/mrcalzon02/Tanks-for-bob-Fork/issues/4)
  for optional final pipe-overlap inspection. Do not claim that diagnostic passed;
  it does **not** block releases under the user's build/runtime-only gates.
- **Steam Condenser V1: new Tanks-native 3×3 Blender construction staged.**
  New original modeling script, pinned canonical north/south full-bore sockets,
  approved packed FMPL ferrocrete PBR donor, keyframed fan, gauge and mist are
  at `models/island-survival/steam-condenser/v1/`. First true Blender render and
  independent saved `.blend` reopen are the current construction gates;
  prototype installation is deferred until actual proof is inspected.

## Historical checkpoint (2026-11-10)

- **Solar Boiler V6: paired glass focal receivers and anchored timber rumble — full native 4-way Blender proof PASSED.**
  The misplaced V5 above-barrel glass is render-hidden but preserved in the source.
  Two **actual focal-line glass tubes** now hold boiling water, four keyed water
  surfaces and 24 rising bubbles; four exposed end-relief sites vent
  intermittent procedural, noise-feathered steam. The wooden barrel and both
  polished-wood concentrators shake subtly on a shared 16-pose cycle while the
  original 3x2 three-port Factorio fixture remains rigid. Thirty-three bentwood
  stave skins have shape keys with their **entire external socket ring locked**,
  a 12.5% rigid lead-in and smooth flex toward the boiler. Independent native
  reopening checked world-space socket motion at frames 0/1/25/49/73/91/97
  (under 0.000001 tile), unchanged metal port mouths and adjacent 128-vertex
  fitting geometry, one fixed 45-degree camera, approved packed wood/concrete
  textures, two repaired wooden pipe-junction holes, and frame-97 loop closure.
  The six-image Cycles pilot passed, followed by **68 real production frames**
  (4 idle, 4 x 16 working) and six independent same-frame effect images.
  Measured 64px pixel differences were **23 boiling, 7 steam, 441 rumble**.
  Native source and proof commit:
  `847514c7e0091543bfd23dfae895c39986837bf1`.
  [Successful production run 42988367558](https://github.com/mrcalzon02/Tanks-for-bob-Fork/actions/runs/42988367558).
  Source: `models/island-survival/solar-boiler/v6/`;
  review: `models/island-survival/solar-boiler/generated-v6/`.
  **Owner visual acceptance and Factorio native sprite attachment are pending.**
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
  The owner-authored FMPL ferrocrete/ferrocrete_light/ferrocrete_dark
  PBR maps (9 total) were imported from the pinned Tech-Priests
  `939ff2d0fea5d236d7092b907c5f08961d5a7560` revision; custom
  copper/iron/reflective materials remain candidate finishes. Model-space
  west/east water and north steam mouth surfaces passed 128-vertex
  adjacent-pipe fit checks with error below 0.0000001 Blender unit.
  See [successful production run 42907291544](https://github.com/mrcalzon02/Tanks-for-bob-Fork/actions/runs/42907291544).
  Full sixteen-frame sprite atlas, native Factorio gameplay, and human visual
  acceptance remain pending; **do not replace live Solar Boiler graphics**.
- **Solar Boiler V2: corrected parabolic collector native Blender proof PASSED.**
  V1's flat reflector strips and arbitrary center bar were replaced by two
  actual concave parabolic mirror surfaces with black absorber tubes at the
  verified focal height (0.28 Blender unit). This is a real geometry/optics
  correction, not a label change; six traced rays per reflector intersect the
  focal receiver axis and the reopened mesh equation agrees within 1e-8 units.
  Four hollow thermal circulation lines join the collectors to the original
  pressure drum with stationary supported mounting. All three original
  native-aligned Factorio fluid fittings, the 3x2 footprint, FMPL packed
  ferrocrete PBR and one 45-degree camera passed independent reopen tests.
  The original V1 model remains untouched. Native .blend and eight true Cycles
  views are in `models/island-survival/solar-boiler/generated-v2/`, commit
  `fcd3c75fd1753626a71cb6519cf1c1616677a724`,
  [successful run 42913231902](https://github.com/mrcalzon02/Tanks-for-bob-Fork/actions/runs/42913231902).
  **Awaiting owner visual acceptance; not yet integrated into the live mod.**
- **Solar Boiler V3: complete gauge/heat/steam working animation technically PASSED.**
  The model derives from the preserved V2 parabolic concentrators and contains a
  true gauge-center oscillating pointer, 3D red-emissive thermal jacket over the
  existing copper pressure accumulator, a restrained localized red light, and
  four sets of staggered steam puffs attached only to two hot collector unions
  and the steam neck/output flange (never the water intakes).
  One native Blender `.blend`, 4 idle renders, 64 working Cycles frames
  (16 × 4 orientations), 6 controlled effect-isolation renders, 64/128/256
  preview-only atlases, and a genuine four-direction 16-frame GIF are committed
  in `d3a5148ab4b249740cb9550bc43c92143576ef19`.
  The reproducible pilot gate passed before the main capture; identical-frame
  image isolation measured 46 changed gauge pixels, 3053 thermal pixels and
  136 joint-steam pixels. Independent Blender reopening verified matching loop
  frame 1/97, three original full-bore ports and their 128-vertex flange faces,
  unchanged V2 source hash, all 9 packed FMPL PBR maps, 1 camera and
  3×2 footprint. The successful
  [Actions run 42922593398](https://github.com/mrcalzon02/Tanks-for-bob-Fork/actions/runs/42922593398)
  is **art/export proof, not gameplay integration, human visual acceptance,
  or a Mod Portal release**.
- **Solar Boiler V4: predominantly wooden construction approved as technical source, not visually accepted.**
  Eighteen bowed wooden barrel staves, 65 bent-plank conduit meshes, two polished
  parabolic wooden reflectors, small retained metal fittings and the approved
  Campfire wood source shader are committed at
  `0b91477dd60db8a3ae96aa4c0ef9e68797f92bf0`.
  This replaced V3's visually rejected glowing copper main vessel, but the old
  roof gap above the two large pipe-to-barrel junctions remained for V5 repair.
- **Solar Boiler V5: native glass accumulator/boiling-fluid/wood-joint proof PASSED.**
  Source commit `bbddbdbd940bef49ad82a2b4c299b20f3745aca3`; actual
  [Blender proof run 42943111518](https://github.com/mrcalzon02/Tanks-for-bob-Fork/actions/runs/42943111518).
  The editable V5 derivative retains V4's eighteen barrel staves, 65 bentwood
  conduit planks and two polished-wood parabolas. It adds an uneven hollow
  handblown-style glass vessel with true liquid volume, 3 animated meniscus
  shape keys, moving foam crest and 22 rising bubbles, two individually
  intermittent end-glass steam jets (7 of 16 frames per side), and two fitted
  wooden roof patches around the side-barrel pipe bores (radius 0.132 Blender
  tile unit). The original **three** native metal fluid fittings were
  independently checked with matching adjacent-pipe face geometry.
  **Native Blender reopen passed.** Four idle and four working cardinal Cycles
  views, 16 working north frames at 8 FPS, and four real effect-isolation
  renders passed; changed RGB pixels at 64px were **28 fluid** and
  **13 steam**. The V5 proof contact sheet, looping GIF, editable native .blend,
  and receipts reside under `models/island-survival/solar-boiler/generated-v5/`.
  Candidate only: user visual review, complete animated cardinal sprite
  export and Factorio 2.1 game integration are still pending.
- One-shot art/native push triggers were removed after their scoped jobs;
  the existing single-job manual workflows remain available.

## Production queue (Solar Boiler V8 installed; Steam Condenser V1 proof passed; Primitive Steam Pump V1 full art candidate passed)

1. **Fish Pond (V1 source/proof complete; awaiting visual approval)** — derived from Clay Pit V4c with one excavated basin, fitted water surface, four 3D swimming fish and editable tail strokes. Native source and eight cardinal proof renders are retained; proceed to complete animated atlases only after visual acceptance. Source: `models/island-survival/fish-pond/v1/build_fish_pond_v1.py`.
2. **Solar Boiler (V8 live production integration complete)** — approved floorless wooden-barrel parabolic concentrator source, 68 genuine Cycles frames, glass focal water/steam effects, fixed 3×2 interfaces and four facings. Actual graphics and Factorio 2.1.24 engine fluid behavior passed; see the checkpoint above. **Visual in-client pipe-mouth screenshot acceptance remains separately tracked under issue #4; not a release blocker.**
3. **Steam Condenser (V1 genuine Blender proof + independent reopen PASS; game candidate only)** — exact 3×3 Tanks original with north steam and south water, reusable full-bore fitting geometry and approved FMPL PBR. [Core30 native proof run 43176065275](https://github.com/mrcalzon02/Dens-Mortis/actions/runs/43176065275) completed successfully and retained the editable Blender model, four idle/four working Cycles frames and genuine four-direction contact sheet. Full 68-frame atlas export, owner visual approval and Factorio prototype substitution remain outstanding; **do not replace live sprites yet**.
4. **Primitive Steam-Powered Pump V1 (actual full Blender production/atlas candidate PASSED; game acceptance pending)** — an original 1×2 editable Blender source with true reciprocating piston, keyed connecting rod, six-spoke 3D flywheel, timber/forged-metal construction, and two stationary canonical FMPL full-bore collars. Native north OUTPUT `(0,-0.75)` and south INPUT `(0,+0.75)` remain unchanged for the **actual `pump` prototype**. [Core30 four-view native proof](https://github.com/mrcalzon02/Dens-Mortis/actions/runs/43181815716) independently reopened the true Blender model, checked rigid ports and loop seam. [Full 68-frame artifact](https://github.com/mrcalzon02/Dens-Mortis/actions/runs/43182697995/artifacts/13926299660) contains SHA-verified native source and all 68 Cycles frames, six validated candidate atlases at 64/128/256, and the four-direction review. The earlier full-render PowerShell count false-negative was repaired and the independently verified run [43183442468](https://github.com/mrcalzon02/Dens-Mortis/actions/runs/43183442468) **succeeded**, including explicit per-atlas SHA256 checks. User visual design approval and the official Factorio `PumpPrototype.animations` client test are still separate gates; **no live game graphics or gameplay altered**.
5. **Beach Pump V1 (68 real Cycles frames + 6 verified atlases, original editable model committed; game-client approval pending)** — a distinct shoreline wave-powered paddle, carved timber rocker, physically linked lifting diaphragm, saltwood dock and suction grille, four separate FMPL footings and one static canonical south fluid outlet. The live `offshore-pump/beachpump` selection bounds are `{{-0.6,-1.49},{0.6,0.49}}`, single native water output `(0,+0.25)` south and source offset `(0,-1)`; **no gameplay change**. [Core30 native 68-frame render #43262584206](https://github.com/mrcalzon02/Dens-Mortis/actions/runs/43262584206) **passed** the separate Blender 5.2.3 reopen, 16-pose/97 seam and 256-vertex stationary collar checks, four idle + 64 working PNG hashes, and six actual 64/128/256 atlases. [Inline four-way render proof](../../models/island-survival/beach-pump/generated-v1-full/review-four-directions.png), [all six atlases](../../models/island-survival/beach-pump/generated-v1-full/) and byte-identical [editable native Blender master reassembly](../../models/island-survival/beach-pump/generated-v1-full/NATIVE-SOURCE.md) are GitHub-visible despite exhausted Actions artifact quota. **Do not replace the existing vanilla fallback graphics until a real Factorio 2.1 client validates offshore-pump animation/shoreline fit.**
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

**Existing advanced model sources, not to rebuild from scratch:** Campfire V12, Clay Pit V4c, Pit Kiln V6, Lumberyard V2b (live ID `growing-plot`), Workbench V7/V8, Cooking Fire V2 (**native 2.1 integration passed**), Fish Pond V1 (**native Blender proof, awaiting visual acceptance**), and Solar Boiler V8 (**full 68-frame four-way production sprite integrated; native Factorio pipe connection pass, GUI screenshot diagnostic open**). The fish pond uses Clay Pit as a **donor**, not a second sculpt.

**Exclusions:** The Auto-Cannon Turret is a **Tech-Priests** asset, never a Tanks-for-Bob construction target. Tanks' dormant turret Lua is not a work authorization. Vehicle 3D art is tracked in a separate queue.

## Required asset evidence, per station

Source Blender `.blend` saved and independently reopened; source provenance and hashes; original base sprite comparison; genuine 64/128/256 RGBA preview with one 45° fixed camera, rotated model cardinal orientations; idle and working states where needed; verified seamless motion (no change in frame count unexpectedly); measured native tile footprint and fluid sockets when applicable; only then sprite/atlas export, Factorio client review, and optional integration. Do not create new GitHub Actions workflows for each machine.
