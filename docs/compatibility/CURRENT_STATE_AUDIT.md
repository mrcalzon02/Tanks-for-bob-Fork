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
- The 1.8.93 package has 545 files, including 484 PNGs, 33 Lua files,
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

### Recovered original high-resolution tank turret

`graphics/entity/tank/hr-tank-turreta.png` was absent from 1.8.93 and
referenced twice in `prototypes/entity/vehicles.lua`. The exact PNG
was recovered from the repo's 1.8.84/1.8.85 package tree.
Its paired XCF file has the **same Git blob SHA** in all three package
versions, so this is the matching original artwork, not a replacement.
The static missing-local-artwork gate should now pass.

### Factorio 2.1: engine-verified, separate package still required

All seven official-mod 2.1.23 CI profiles passed headless map creation,
data validation, simulated ticks, vehicle instantiation and private
dedicated-server startup in:
https://github.com/mrcalzon02/Tanks-for-bob-Fork/actions/runs/42133070510

The 2.1 jobs update `factorio_version` in a disposable test copy only.
The committed source 1.8.93 package still declares 2.0. A distinctly
versioned and verified 2.1 package is required before distribution on
Factorio 2.1; do not claim it is already published.

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

1. Re-run all 12 tests after restoring the original turret PNG and
   strengthening the runtime assertion to require tick 300 or later.
2. Test client-side sprites, turret masks and animations, and verify
   the matching original PNG renders as expected.
3. Build and validate a separately versioned Factorio 2.1 artifact;
   keep the Factorio 2.0 package installable.
4. Add deterministic firing, damage, ammo, placement, recall/GUI
   and progression scenarios, followed by real two-client multiplayer.
5. Consider earlier save migration tests and engine performance under
   several active tank fleets.

**Workflow:** https://github.com/mrcalzon02/Tanks-for-bob-Fork/actions/workflows/vanilla-factorio.yml

**12-profile engine baseline:** https://github.com/mrcalzon02/Tanks-for-bob-Fork/actions/runs/42133070510

## 6. Continued audit checks (2026-11-05)

A new CI-only engine audit tier is installed without changing published gameplay
definitions:

- **Optimistic recipe supply graph:** seeds world resources and conventional
  wood/fish/water sources, iterates all registered recipe ingredient/product
  relationships, and reports mod recipes with unresolved upstream inputs.
  This is diagnostic, **not** proof of real assembly-machine, technology,
  fuel, fluid-temperature, SeaBlock-map, or bootstrap accessibility.
- **Vehicle/weapon/ammo topology:** inspects 13 tank variants, installed
  gun prototypes, ammo-category matches, ammo recipes, item placement and
  mining results. Registrations do **not** prove that actual shots fire.
- **Live physical-damage response:** after the initial vehicle-instantiation
  smoke test (tick 300), uses Factorio's native entity.damage API at tick
  600 to confirm real hitpoint reduction/destruction. It does **not**
  simulate a fired projectile or prove self-damage mechanics.
- These audits run within the existing 12 official-mod matrix profiles and
  publish their observations in full headless creation/benchmark logs.
- Supply graph and weapon topology findings remain **diagnostic**;
  only genuinely failed engine lifecycle checks or explicitly verified
  runtime assertions cause a failing job.

**Test provenance:** these are CI-only harness files copied into an isolated
temporary mod install. They are not added to the distributable mod.

### Ammo audit correctness follow-up

The initial weapon pass reported 26 missing ammo links because the CI checker
incorrectly read `ammo_type.category` instead of Factorio's actual
`AmmoItemPrototype.ammo_category` property. This is a **checker bug**,
not evidence of missing ammunition. The checker was corrected before
drawing conclusions about ammo compatibility. See the next CI run for
the actual confirmed link count; firing and ammunition consumption remain
separate untested behaviors.

### Complete ammunition manifest and live inventory probe

The CI weapon audit now reads **all 13** ammo declarations from the source
manifest instead of nine guessed by filename; it validates those prototypes,
their top-level `ammo_category`, and an item-producing recipe. The existing
26 gun-slot-to-category checks remain.

The runtime harness also tries loading appropriate ammunition into eight
live tank variants at tick 900. Because one vehicle is deliberately destroyed
by the physical-damage probe at tick 600, the expected inventory count may
be seven. Insertion/rejection outcomes are logged as **diagnostics**, not
release blockers. This is not a live firing or ammo-consumption test.
