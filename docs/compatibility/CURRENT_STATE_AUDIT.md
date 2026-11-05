# Tanks for Bob Fork — current-state development audit

**Audit date:** 2026-11-05
**Test target:** latest checked-in package `tanks_for_bob_fork_1.8.93`
**Repositories involved:** only `mrcalzon02/Tanks-for-bob-Fork`
**Engine baseline:** Factorio 2.0.77 plus official-mod 2.1.23 compatibility probes

This report distinguishes verified engine outcomes, static inspection findings,
and test coverage still missing. It does **not** imply that every gameplay
system has passed just because the engine can launch.

## 1. Repository and source inventory

- Three versioned source folders are present: 1.8.84, 1.8.85, 1.8.93.
- The 1.8.93 package has 544 files, including 483 PNGs, 33 Lua files,
  three XCF source images, six OGG files, 15 locale CFGs and metadata.
- The literal-require dependency scan finds 25 active/reachable Lua files
  out of 33; the remaining files include migrations and legacy source.
- The active Lua code contains 210 distinct literal recipe declarations and
  88 distinct technology declarations, according to the source scanner.
- An unreferenced root-level `recipe.lua` (about 121 KB) is present.
  It is not imported by `data.lua`; it should not be counted as a live
  second recipe registry or removed without a separate review.
- The fork is more than tank combat content: it includes SeaBlock-like
  bootstrap, industrial waste, science/meal, corporate paperwork,
  intermediary and custom manufacturing chains.

All counts are source-audit observations, not a promise that every declared
recipe is craftable or every technology economically reachable.

## 2. Actual engine evidence

**Verified green baseline:** the five Factorio 2.0.77 jobs in
https://github.com/mrcalzon02/Tanks-for-bob-Fork/actions/runs/42132183969

These five combinations individually passed: base; base + Elevated Rails;
base + Quality; base + Elevated Rails + Quality; and base + Space Age
(with its official components). The workflow checked real data initialization,
a deterministic save, 1,200 ticks with vehicle instantiation, and a real
private dedicated-server startup.

Data-stage snapshot for the vanilla-only profile in that run:
- `429` total registered recipes including official base.
- `284` total registered technologies including official base.
- `59` recipes categorized as `tank-crafting` or `tank-ammo-component`.
- `0` disabled tank-category recipes without a technology unlock
  according to the initial data-stage scan.
- `4` globally disabled recipes without unlocks are present; this
  includes vanilla/official prototypes and requires provenance review.
- Category-to-machine support for the two tank-specific categories passed.

Space Age/Quality runs also reached the data audit; protected waste
recipes had `auto_recycle=false` as expected for the three sampled probes.

## 3. Confirmed defects and remediations

### Repaired on main during this audit

- Repaired case-sensitive `prototypes/Compatibility` Lua import paths.
- Installed a real loadable `space-age.lua` from existing compatibility
  patch text; it now activates for Quality/Recycler where relevant.
- Removed duplicate `growing` recipe-category declaration.
- Declared official modules as optional dependencies with no mandatory DLC.
- Corrected 80+ case-sensitive graphics references to *existing* repository
  assets rather than inventing replacement graphics.
- Added primary-output icon inheritance for original multi-output recipes
  missing a recipe icon, including item and science-tool outputs.
- Added Factorio 2.1 conditional adaptations for assembler pipe images,
  item fuel categories, offshore-pump fluid-box temperatures,
  recipe category arrays, and renamed product probability property.
- Added a 12-profile CI matrix and audit artifacts independent of Tech Priests.

### Still open: missing rendered high-resolution tank turret

`graphics/entity/tank/hr-tank-turreta.png` is referenced twice in
`prototypes/entity/vehicles.lua` (near lines 103 and 643), but it is
absent from the 1.8.93 package. An XCF source with the corresponding
base name exists; it is **not** a PNG image usable by Factorio at runtime.
Do not silently substitute another turret image. Export the correct sprite
and inspect alignment, expected dimensions, masks and animation frames.

This single unique path is why the comprehensive static graphics gate
remains red after the capitalization repairs. Headless launch success
does not demonstrate that all sprites render correctly.

### Factorio 2.1: not yet certified

Factorio 2.1 has breaking prototype schema changes. The compatibility
matrix tests it using temporary metadata; the checked-in package still
reports 2.0. Success requires all seven 2.1 profiles to pass before a
separately tagged 2.1 package is considered ready. Follow the most recent
CI run rather than assuming the source adaptations above are sufficient.

## 4. Functional areas not yet proven

- Full ingredient/technology acquisition chain, dead-end-free survival and
  SeaBlock progression, full production of every intermediate and waste
  reprocessing recipe in a simulated factory.
- Tank driving, weapon and ammo category assignments, actual hits,
  self-damage, flamer/rocket/mine and super-tank weapon behaviors.
- Sprite loading, turret facing, layers, graphics alignment, shadow/mask
  correctness and icon visibility in the **client** (headless-only CI).
- Tank recall GUI and teleporter function: `control.lua` contains
  function definitions but its example event-handler registrations are
  commented out. Treat recall as **not proven operational**.
- Dedicated-server two-client synchronization, save migrations through
  old mod versions, genuine persistence after restart and rejoin.
- Economy balance, damage balance and performance under massed tank combat.

None of the above untested features is implicitly counted as passed.

## 5. Next acceptance work

1. Finish Factorio 2.1 schema migration and obtain seven green 2.1 runtime
   jobs. Retain the passing 2.0 matrix unchanged.
2. Export the missing turret image from source and validate actual sprite
   sheets, including rendering in a client.
3. Finish source-manifest-to-runtime checks of all recipe and technology
   declarations, then identify disabled-but-unlocked or dead-end recipes.
4. Add deterministic combat, ammo, placement, controls and research
   progression scenarios, then real multiplayer join/save/rejoin testing.
5. Only then prepare a separately versioned 2.1 release artifact if desired.

**Workflow:** https://github.com/mrcalzon02/Tanks-for-bob-Fork/actions/workflows/vanilla-factorio.yml
**Current test evidence:** https://github.com/mrcalzon02/Tanks-for-bob-Fork/actions/runs/42132183969
