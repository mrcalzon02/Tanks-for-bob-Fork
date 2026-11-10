# Tanks-for-Bob Fork — 3D structure production order

This is the **survival / manufacturing structures** queue, separate from vehicle/tank art. Legacy first-pass OBJ geometry is not considered a production-ready `.blend`; state verification must inspect native source and actual sprite export evidence. Preserve every accepted source; never replace old assets in place. Use the canonical Tech-Priests FMPL asset library, actual Factorio tile/fluidbox dimensions, approved construction-pads/PBR, and one fixed calibrated 45° camera. User review precedes live graphics substitution.

## First target: Fish Pond

1. **Fish Pond (V1 underway)** — derive Clay Pit V4c, fill the single existing excavation with water, idle=water only, working=four true 3D swimming fish on looping tracks. Source: `models/island-survival/fish-pond/v1/build_fish_pond_v1.py`.
2. Solar Boiler — adapt proven Boiler donors to this exact prototype's 3×2 footprint and 3 fluid ports, physical solar collector rather than old inherited vanilla sprites.
3. Steam Condenser — rebuild around the 3×3 Tanks prototype using actual condenser donor components; do not paste in the 2×2 Tech-Priests machine wholesale.
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

**Existing advanced model sources, not to rebuild from scratch:** Campfire V12, Clay Pit V4c, Pit Kiln V6, Lumberyard V2b (live ID `growing-plot`), Workbench V7/V8, and Cooking Fire V2 (the last requires a separate game-integration check). The fish pond uses Clay Pit as a **donor**, not a second sculpt.

**Exclusions:** The Auto-Cannon Turret is a **Tech-Priests** asset, never a Tanks-for-Bob construction target. Tanks' dormant turret Lua is not a work authorization. Vehicle 3D art is tracked in a separate queue.

## Required asset evidence, per station

Source Blender `.blend` saved and independently reopened; source provenance and hashes; original base sprite comparison; genuine 64/128/256 RGBA preview with one 45° fixed camera, rotated model cardinal orientations; idle and working states where needed; verified seamless motion (no change in frame count unexpectedly); measured native tile footprint and fluid sockets when applicable; only then sprite/atlas export, Factorio client review, and optional integration. Do not create new GitHub Actions workflows for each machine.
