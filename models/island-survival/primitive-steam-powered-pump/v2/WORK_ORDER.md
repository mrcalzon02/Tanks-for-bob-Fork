# Primitive Steam-Powered Pump — active refinement work order

**Current focus confirmed after owner correction, 2026-11-15.** This is the
actual 1x2 pipe-to-pipe pump, distinct from Stone Water Wheel's shoreline intake.
Neither structure is unused: both have recipes, research and downstream consumers.
See `docs/art/STRUCTURE_FUNCTION_CONTRACTS.md`.

The successful V1 artifact was recovered from Dens-Mortis run `43183442468`,
artifact `13927757032`. Archive SHA256:
`169e42b5a833a85408b1fcc1a2c9c9bb4907b162812404b6c580319ed44a9ff0`.
The original editable master is retained in `../archive/v1-verified/pump-v1.blend`,
SHA256 `1c6e1b23d0ec1472d1c25303416b97b827735298f9a34724beecc7e085d9cd6c`.
The original 68 captures and six atlas candidates remain in the recovered artifact;
their success is not owner visual acceptance.

## Locked function

`pump/primitive-steam-powered-pump`, south fluid input `(0,+0.75)`, north output
`(0,-0.75)`, external visual joint planes Y -1/+1 at Z .36, one tile per unit.
Chemical burner, 20 kW, one fuel slot, pumping_speed 1, no fluid filter. Preserve
all gameplay fields, port vertices and native positions. No lifting buckets or
invented third external steam feed. Fixed geometry must survive all poses.

## V2 mechanism result

The V1 rod changed length to chase independently animated endpoints. V2 places
the crank and crosshead attachment in the same plane, reduces eccentricity to
match the original 0.206-tile stroke, solves a rigid 0.6-tile slider-crank and
adds physical pivot/rod eyes. The rod's mesh length is constant; no animated
scale simulates a connecting mechanism. Two original nonexported curve pipes
are replaced by actual hollow wall meshes with physical UVs for runtime export.

Source and actual reimported GLB checks passed across **97 poses**. Both have
31,420 triangles and zero detected degenerate triangles; source/export bounds
match exactly. Actual imported joint error is below 0.000001 tile, rigid-length
error below 0.000001 tile, and all four port meshes remain stationary. See
`../candidates/v2-mechanism01/mechanism-inspection.json` and
`../candidates/v2-mechanism01/runtime-inspection.json` for exact current hashes.
Four source facings and four actual-export facings were rendered and viewed.

These are scoped geometry/motion checks. **Visual finish, clearance, baked PBR,
production sprite capture, native game integration and owner approval remain open.**

## Next required repair: construction and surface quality

1. Redesign the tight hollow pipe elbows and internal reducers so walls do not
   intersect on small bend radii; retain the exact full-size external mouth meshes.
   Correct the near-end annulus winding before the next export.
2. Resolve the firebox/boiler load path and hot/cold material identities. The
   inherited wooden block and disconnected-looking pressure parts still read
   as a blockout. Build a plausible lined firebox, supported jacket, seams and
   mounted fittings; inspect all side/rear and moving poses.
3. Author per-part wood grain/end grain, aged copper, forged iron and their wear;
   unwrap and bake coherent albedo/roughness/normal maps. The inherited procedural
   bump is **not** an exported normal map. Current GLB embeds only the three
   existing FMPL structural-foot maps; this is an explicit unfinished gate.
4. Add neutral clay/close views and a real motion review; repair visually before
   propagating the full 68-frame production batch. Restore correct working/idle
   states and native fluid overlays, with no duplicate complete-object layer.
5. Complete 64/128/256 RGBA packing and a disposable Factorio 2.1 pump.animations
   adapter. Test fuel/working/stop/restart, real fluid transfer, all four pipe
   connections/rotations, save/reload and native pixel alignment. Present the
   concrete finished candidate for owner disposition before active replacement.

## Reproduce current mechanism study

Use Blender 5.x and the canonical FMPL camera tools at exact library commit
`939ff2d0fea5d236d7092b907c5f08961d5a7560`. `--fmpl-tools` points to the directory
containing its `capture_policy.py` and `blender_camera_guard.py`.
Verified Git blob identities are `107353f2e34ac301abec8cfcde1487d30129c5a6` and
`457b0a2517e70093658c8e5e1d561619858f59e0`, respectively. Current local cache:
`build/fmpl-pin/`. Do not silently substitute the different current-worktree policy.

```powershell
& 'C:\Program Files\Blender Foundation\Blender 5.0\blender.exe' --background --factory-startup --python-exit-code 1 --python models/island-survival/primitive-steam-powered-pump/v2/refine_pipe_pump.py -- --source models/island-survival/primitive-steam-powered-pump/archive/v1-verified/pump-v1.blend --out models/island-survival/primitive-steam-powered-pump/candidates/NEW-REVISION --fmpl-tools build/fmpl-pin
```

Run `v2/inspect_runtime_export.py` in a fresh Blender process against that output.
It sets the imported scene to the source 48 FPS before glTF import; using a
24-FPS fractional frame allowed the first rendered view to lose animated parts
despite valid geometry measurements. The current four export images were
rerendered and actually inspected after that correction. Never use the earlier
incomplete first-view proof as acceptance evidence.

## Gate state

P00/P01/P02 contract/provenance: source facts established; original sprite and
native engine review still need current evidence. P03 native reopen and scoped
mechanism checks passed. P05 canonical camera matrix passed; native calibration
pending. P06-P09 final layers/export/sprite QA pending. P10 engine and P11 visual
acceptance pending. P12 candidate checkpoint pending publication/readback.
No current asset is approved for replacement. No Mod Portal release is produced.
