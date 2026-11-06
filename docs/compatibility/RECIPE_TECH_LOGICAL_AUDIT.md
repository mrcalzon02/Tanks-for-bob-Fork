# Tanks for Bob Fork — Recipe & technology logical audit

**Snapshot:** `main` commit `781c23483e3143b47a6a67f9d52f3287e8ead410`, released source folder `tanks_for_bob_fork_1.8.94`.
**Method:** read-only source/prototype-logic audit; **no gameplay modifications**. Scope is the **active** modules imported by `data.lua` (`prototypes/recipe/recipe.lua`, `prototypes/recipe/ammo.lua`, `prototypes/recipe/vehicles.lua`, `prototypes/technology/technology.lua`). The similarly named root-level `recipe.lua` is not an active import. Based on Factorio 2.0 prototype rules and the one-profile smoke-test evidence, not a manually played full progression campaign.

## Inventory and baseline checks

| Measure | Result |
| --- | ---: |
| Active source-declared recipes | **210** |
| Start-enabled / research-disabled recipes | **39 / 171** |
| Source-declared technologies | **88** |
| Disabled recipes without any declared technology unlock | **0** |
| Missing prerequisites in last successful Factorio engine audit / static tech cycles | **0 / 0** |
| Technology units mixing vanilla and custom science in one research cost | **0** |
| Empty-effect authorization gates | **12** |
| Start-enabled recipe also redundantly technology-unlocked | **1** |

The existing headless CI validates prototype registration, missing unlocks, technology prerequisite loops, synthetic supply reachability and 1,200 engine ticks. **Registration success does not prove a machine can select and craft its recipe.** The existing optimistic `ci/progression_audit.lua` ignores machine item-ingredient limits, custom machine fluid boxes, research state, factory placement and actual production.

## Critical defect A — workbench cannot craft five foundational structures

The only custom machine with `crafting_categories = {"Seablock"}` is the `workbench`, whose prototype sets **`ingredient_count = 2`** ([entity source L2564, L2590](../../tanks_for_bob_fork_1.8.94/prototypes/entity/entities.lua#L2564)). These research-unlocked **Seablock** recipes each require **3 different item ingredients**:

| Recipe | Required item types | Source |
| --- | ---: | --- |
| `clay-pit` | 3 | [L342](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L342) |
| `wood-basin` | 3 | [L403](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L403) |
| `fish-pond` | 3 | [L422](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L422) |
| `quarry` | 3 | [L441](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L441) |
| `primitive-steam-powered-pump` | 3 | [L460](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L460) |

Vanilla assembling machines gain `tank-crafting` and `tank-ammo-component` in [`data-updates.lua`](../../tanks_for_bob_fork_1.8.94/data-updates.lua#L22), **not `Seablock`**. There is no supported fallback machine for these five recipes. The workbench limit applies to distinct *item ingredient types*, not stack quantities or fluid ingredients.

**Consequence:** clay pits, wood basins, fish ponds, quarries and primitive steam-powered pumps can be unlocked in the research tree but not manufactured in the intended workbench. This strands fundamental clay/brick, water/steam, mineral and fish-production stages and invalidates the assumption that the early three-path bootstrap is functionally reachable. Factorio's `AssemblingMachinePrototype.ingredient_count` limits recipe selection, even if data-stage prototype validation succeeds.

**Recommended isolated repair:** raise Workbench `ingredient_count` from **2 to at least 3**, then prove each of the five recipes is selectable and actually crafts in the built machine. Do not change costs until this mechanical blocker is resolved.

## Critical defect B — advanced cooking has no steam input

The sole `advcooking` machine is `cooking-fire`, declared [here](../../tanks_for_bob_fork_1.8.94/prototypes/entity/entities.lua#L1237) with category assignment at [L1298](../../tanks_for_bob_fork_1.8.94/prototypes/entity/entities.lua#L1298) and **no `fluid_boxes` input**. But:

| Recipe | Fluid input | Source |
| --- | --- | --- |
| `rendered-organics` | 150 steam | [L1541](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L1541) |
| `steam-meal` | 500 steam | [L1596](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L1596) |

The other `meal` recipe is a solid-only alternative after `meal` technology, so the `steam-meal` route is not by itself a full science softlock. **`rendered-organics` has no alternate declared production recipe.**

**Consequence:** a source graph starting with `rendered-organics` unavailable and propagating only through unique declared production routes affects **54 recipe pathways**, **51 uniquely sourced product names**, and **39/88 technologies** whose required custom science or technology prerequisites ultimately rely on those products. Including the separate `steam-meal` recipe, the affected recipe set is **55/210**. This is a **conditional static dependency analysis**, not a live in-game reachability count; it assumes no untested alternative provider for the fork's custom intermediate items.

Representative broken chain:

`rendered-organics → enzyme-paste / denatured-organic-base → bio-synthetic-precursor → marseline-compound / other encabulation materials → Encabulator / SpervingArm → vehicle recipes`.

The corporate research chain also uses `stakeholder-review-summary`, `liability-contained-report`, `board-review-docket` and `board-advisory-risk-assessment`, all dependent on blocked intermediates; this makes the latter research authorizations unavailable in practical play even if their prerequisites contain no literal cycle.

**Recommended isolated repair:** add a correctly configured **steam input fluid box** to the `cooking-fire` entity or move the two steam recipes into a machine/category already possessing a valid steam input, preserving intended technology order. Test actual steam consumption and first `rendered-organics` output.

## Moderate issue C — dedicated tank-ammunition machine has no fluid ports

[`tank-ammo-assembling-machine`](../../tanks_for_bob_fork_1.8.94/prototypes/entity/entities.lua#L2749) supports `tank-ammo-component` with no fluid boxes, although `tank-ammo-industrial-coke` produces **100 crude oil** ([recipe L3790](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L3790)) and `Rubberized-timber` consumes **10 crude oil** ([recipe L3837](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L3837)). These cannot perform fluid handling on the dedicated machine.

**Qualification:** `data-updates.lua` also adds `tank-ammo-component` to vanilla assembling machines 1/2/3; **assembler 2/3 have fluid-handling capability**, providing an intended or accidental workaround after they become available. This is a **dedicated-machine restriction**, not a demonstrated global production softlock. Test category selection and byproduct extraction in assembler 2.

## Lower-priority staging issue D — redundant stone-tools unlock

[`stone-tools` recipe](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L135) is **enabled at startup**, but [technology `stone-tools`](../../tanks_for_bob_fork_1.8.94/prototypes/technology/technology.lua#L214) includes `unlock-recipe = "stone-tools"`. The technology may be intended as a prerequisite/education step; its unlock effect itself adds nothing. Consider whether the research is intentionally an authorization gate rather than restricting an already accessible tool.

## Deliberate gates and apparent non-defects

- The **12 empty-effect technologies are authorization gates**, not necessarily broken nodes; the technologies `organic-explosives2` and `organic-explosives3` actually grant combat `ammo-damage`/`gun-speed` effects and should **not** be counted as empty.
- The six zero-input recipes include intentionally slow manual desperation bootstrap paths and machine-powered gathering; do not remove or nerf these as a result of this audit.
- The 2.0 `clay`, `shaler`, `Calcifier` and `Steam-Compressor` fluid categories declare matching purpose-built machine fluid interfaces. The highest-confidence fluid omissions are the two `advcooking` recipes and the two dedicated tank-ammo fluid operations above.
- Two custom burner labs (`thinking-hut`, `pondering-hovel`) list the fork's custom research tools. The advanced military/vehicle technologies use ordinary science packs in separate technologies; no mixed-lab-research pack mismatch was found in declared technology units.
- Existing CI's optimistic **210/210 supply graph is not a manufacturing proof**. The root failures above are examples of why ingredient-only closure overstates progression.

## Acceptance criteria for a later repair iteration (not executed here)

1. **Machine capacity:** five three-item `Seablock` recipes selectable in a real powered Workbench, with required ingredients inserted and products emitted.
2. **Bio-chain:** `rendered-organics` actually consumes 150 steam; `enzyme-paste`, `denatured-organic-base` and `bio-synthetic-precursor` subsequently craft from normal player-produced inputs.
3. **Research:** player can produce and consume `stakeholder-review-summary`, `liability-contained-report` and `board-review-docket` in a configured lab, then unlock a representative tank.
4. **Vehicle:** a researched player-produced `SpervingArm` and `Encabulator` can be used to craft `auto-tank` or `flame-tank` in the intended factory.
5. **Regression:** the **existing one-job, one-Factorio-2.0-profile** CI continues to pass. Add diagnostic checks inside that same job if approved; do not reintroduce a matrix of jobs or profiles.

No gameplay changes were made by this audit. Findings and counts are source-logic analysis, to be confirmed with targeted in-game manufacturing tests.

## Complete declared recipe inventory (210 rows)

`Items / fluids` counts distinct ingredient entries, not total stack counts. `CAPACITY` means over the sole category machine's item ingredient limit; `FLUID` means category's sole dedicated machine lacks a fluid input; `TANK-FLUID` means the specialized tank-ammo machine lacks fluid handling but vanilla assembler 2/3 may provide a workaround; `DOWNSTREAM` means dependent on the missing rendered-organics route; `REDUNDANT-UNLOCK` means available before research.

| Recipe | Category | Availability | Items / fluids | Unlocked by | Static finding | Source |
| --- | --- | --- | ---: | --- | --- | --- |
| `stone` | `quarrying` | Start | 0 / 0 | — | — | [L8](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L8) |
| `Trees` | `growing` | Start | 0 / 0 | — | — | [L18](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L18) |
| `harvest-fish` | `fishery` | Start | 0 / 0 | — | — | [L28](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L28) |
| `desperation-gather-fish` | `crafting` | Start | 0 / 0 | — | — | [L45](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L45) |
| `desperation-scrape-driftwood` | `crafting` | Start | 0 / 0 | — | — | [L59](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L59) |
| `desperation-pick-stone` | `crafting` | Start | 0 / 0 | — | — | [L73](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L73) |
| `desperation-landfill` | `crafting` | Start | 1 / 0 | — | — | [L87](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L87) |
| `catch-fish` | `fishery` | Start | 1 / 0 | — | — | [L106](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L106) |
| `Sharp-stick` | `crafting` | Start | 1 / 0 | — | — | [L119](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L119) |
| `stone-tools` | `crafting` | Start | 2 / 0 | `stone-tools` | REDUNDANT-UNLOCK | [L135](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L135) |
| `Trees-with-tools` | `growing` | Start | 1 / 0 | — | — | [L145](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L145) |
| `stone-with-tools` | `quarrying` | Start | 1 / 0 | — | — | [L162](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L162) |
| `catch-fish-with-tools` | `fishery` | Start | 2 / 0 | — | — | [L179](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L179) |
| `Seared-fish` | `cooking` | Start | 1 / 0 | — | — | [L204](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L204) |
| `clay` | `clay` | Start | 1 / 1 | — | — | [L215](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L215) |
| `clay-with-tools` | `clay` | Start | 2 / 1 | — | — | [L225](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L225) |
| `fish-kit` | `tank-ammo-component` | Locked | 1 / 0 | `mechanized-infantry-research` | — | [L246](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L246) |
| `campfire` | `crafting` | Start | 1 / 0 | — | — | [L268](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L268) |
| `workbench` | `crafting` | Start | 1 / 0 | — | — | [L279](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L279) |
| `thinking-hut` | `crafting` | Start | 1 / 0 | — | — | [L290](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L290) |
| `beachpump` | `Seablock` | Locked | 2 / 0 | `beachpump` | — | [L301](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L301) |
| `growing-plot` | `Seablock` | Locked | 2 / 0 | `growing-plot` | — | [L314](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L314) |
| `wood-spear` | `Seablock` | Locked | 1 / 0 | `wood-spear` | — | [L327](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L327) |
| `clay-pit` | `Seablock` | Locked | 3 / 0 | `clay-pit` | CAPACITY | [L342](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L342) |
| `brick` | `pit-kiln` | Locked | 1 / 0 | `brick` | — | [L356](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L356) |
| `pit-kiln` | `Seablock` | Locked | 2 / 0 | `pit-kiln` | — | [L373](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L373) |
| `crude-glass` | `pit-kiln` | Locked | 1 / 0 | `crude-glass` | — | [L383](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L383) |
| `wood-basin` | `Seablock` | Locked | 3 / 0 | `wood-basin` | CAPACITY | [L403](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L403) |
| `fish-pond` | `Seablock` | Locked | 3 / 0 | `fish-pond` | CAPACITY | [L422](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L422) |
| `quarry` | `Seablock` | Locked | 3 / 0 | `quarry` | CAPACITY | [L441](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L441) |
| `primitive-steam-powered-pump` | `Seablock` | Locked | 3 / 0 | `primitive-steam-powered-pump` | CAPACITY | [L460](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L460) |
| `cooking-fire` | `Seablock` | Locked | 2 / 0 | `cooking-fire` | — | [L484](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L484) |
| `stone-water-wheel` | `Seablock` | Locked | 2 / 0 | `stone-water-wheel` | — | [L499](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L499) |
| `solar-boiler` | `Seablock` | Locked | 2 / 0 | `solar-boiler` | — | [L514](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L514) |
| `steam-condenser` | `Seablock` | Locked | 2 / 0 | `steam-condenser` | — | [L529](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L529) |
| `Steam-condenserA` | `Steam` | Start | 1 / 1 | — | — | [L544](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L544) |
| `pondering-hovel` | `Seablock` | Locked | 2 / 0 | `pondering-hovel` | — | [L566](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L566) |
| `hand-chip-iron-ore` | `crafting` | Start | 2 / 0 | — | — | [L583](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L583) |
| `hand-scrape-wood` | `crafting` | Start | 1 / 0 | — | — | [L605](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L605) |
| `hand-break-fish-for-stone` | `crafting` | Start | 2 / 0 | — | — | [L626](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L626) |
| `quarry-iron-ore` | `quarrying` | Start | 2 / 0 | — | — | [L647](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L647) |
| `quarry-copper-ore` | `quarrying` | Start | 2 / 0 | — | — | [L662](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L662) |
| `quarry-iron-orea` | `quarrying` | Start | 2 / 0 | — | — | [L677](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L677) |
| `quarry-copper-oreb` | `quarrying` | Start | 2 / 0 | — | — | [L692](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L692) |
| `workbenchA` | `crafting` | Start | 1 / 0 | — | — | [L707](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L707) |
| `stone-tools-iron` | `crafting` | Locked | 2 / 0 | `Steam-Compressor` | — | [L718](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L718) |
| `Canister` | `crafting` | Start | 2 / 0 | — | — | [L728](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L728) |
| `calcifier` | `Seablock` | Locked | 2 / 0 | `calcifier` | — | [L749](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L749) |
| `Calcifier-pro` | `Calcifier` | Start | 1 / 1 | — | — | [L764](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L764) |
| `shaler` | `Seablock` | Locked | 2 / 0 | `shaler` | — | [L781](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L781) |
| `Steam-Compressor` | `Seablock` | Locked | 2 / 0 | `Steam-Compressor` | — | [L796](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L796) |
| `Steam-Charge` | `shaler` | Start | 1 / 1 | — | — | [L811](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L811) |
| `Charged-Canister` | `Steam-Compressor` | Locked | 1 / 1 | `Steam-Compressor` | — | [L832](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L832) |
| `UnCharge-Canister` | `Steam-Compressor` | Locked | 1 / 0 | `Steam-Compressor` | — | [L848](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L848) |
| `Calcifier-pro-2` | `Calcifier` | Locked | 1 / 1 | `waste-processing-2` | — | [L872](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L872) |
| `Calcifier-pro-3` | `Calcifier` | Locked | 1 / 1 | `waste-processing-3` | — | [L893](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L893) |
| `Calcifier-pro-4` | `Calcifier` | Locked | 1 / 1 | `waste-processing-4` | — | [L914](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L914) |
| `Calcifier-pro-5` | `Calcifier` | Locked | 1 / 1 | `waste-processing-5` | — | [L935](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L935) |
| `shaler1` | `shaler` | Start | 1 / 1 | — | — | [L961](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L961) |
| `shalera` | `shaler` | Start | 2 / 0 | — | — | [L982](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L982) |
| `shalerb` | `shaler` | Start | 1 / 0 | — | — | [L1003](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L1003) |
| `shalerc` | `shaler` | Start | 2 / 0 | — | — | [L1024](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L1024) |
| `shaler3` | `shaler` | Start | 1 / 0 | — | — | [L1045](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L1045) |
| `shaler2` | `shaler` | Locked | 1 / 1 | `waste-processing-2` | — | [L1071](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L1071) |
| `shaler4` | `shaler` | Locked | 1 / 1 | `waste-processing-3` | — | [L1092](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L1092) |
| `shaler5` | `shaler` | Locked | 1 / 1 | `waste-processing-4` | — | [L1112](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L1112) |
| `shaler6` | `shaler` | Locked | 1 / 1 | `waste-processing-5` | — | [L1132](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L1132) |
| `radio-refine-2` | `shaler` | Locked | 1 / 1 | `waste-processing-2` | — | [L1157](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L1157) |
| `radio-refine-3` | `shaler` | Locked | 1 / 1 | `waste-processing-3` | — | [L1178](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L1178) |
| `radio-refine-4` | `shaler` | Locked | 1 / 1 | `waste-processing-4` | — | [L1199](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L1199) |
| `radio-refine-5` | `shaler` | Locked | 1 / 1 | `waste-processing-5` | — | [L1220](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L1220) |
| `ore-from-waste` | `tank-ammo-component` | Locked | 3 / 0 | `encabulated-waste-recovery` | DOWNSTREAM | [L1241](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L1241) |
| `ore-from-wasteb` | `tank-ammo-component` | Locked | 2 / 0 | `encabulated-waste-recovery` | — | [L1264](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L1264) |
| `ore-from-waster` | `tank-ammo-component` | Locked | 3 / 0 | `encabulated-waste-recovery` | DOWNSTREAM | [L1286](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L1286) |
| `tank-ammo-Reprocessing` | `tank-ammo-component` | Locked | 2 / 0 | `encabulated-waste-recovery` | — | [L1309](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L1309) |
| `tank-ammo-ecozone` | `tank-ammo-component` | Locked | 2 / 0 | `organic-explosives` | — | [L1333](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L1333) |
| `trace-mineral-slurry` | `clay` | Start | 1 / 1 | — | — | [L1361](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L1361) |
| `saline-particulate` | `smelting` | Locked | 1 / 0 | `mineral-fractionation` | — | [L1383](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L1383) |
| `ionic-scum` | `Calcifier` | Locked | 1 / 1 | `mineral-fractionation` | — | [L1404](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L1404) |
| `heavy-brine-fraction` | `shaler` | Locked | 1 / 1 | `mineral-fractionation` | — | [L1426](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L1426) |
| `microcrystal-sediment` | `Calcifier` | Locked | 2 / 1 | `mineral-fractionation` | — | [L1448](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L1448) |
| `fish-oil-residue` | `cooking` | Start | 1 / 0 | — | — | [L1477](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L1477) |
| `protein-slurry` | `advcooking` | Locked | 2 / 0 | `bio-reactive-processing` | — | [L1498](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L1498) |
| `calcified-bone-dust` | `advcooking` | Locked | 1 / 0 | `bio-reactive-processing` | — | [L1520](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L1520) |
| `rendered-organics` | `advcooking` | Locked | 1 / 1 | `bio-reactive-processing` | FLUID | [L1541](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L1541) |
| `enzyme-paste` | `advcooking` | Locked | 2 / 0 | `bio-reactive-processing` | DOWNSTREAM | [L1564](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L1564) |
| `meal` | `advcooking` | Locked | 1 / 0 | `meal` | — | [L1586](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L1586) |
| `steam-meal` | `advcooking` | Start | 1 / 1 | — | FLUID | [L1596](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L1596) |
| `charcoal` | `crafting` | Locked | 1 / 0 | `charcoal-processing` | — | [L1621](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L1621) |
| `wood-pulp` | `crafting` | Locked | 2 / 0 | `wood-pulp-processing` | — | [L1641](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L1641) |
| `crude-paper` | `crafting` | Locked | 2 / 0 | `crude-paperwork` | — | [L1662](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L1662) |
| `ink` | `crafting` | Locked | 2 / 0 | `crude-paperwork` | — | [L1683](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L1683) |
| `staples` | `crafting` | Locked | 2 / 0 | `basic-requisitioning` | — | [L1704](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L1704) |
| `stamps` | `crafting` | Locked | 3 / 0 | `basic-requisitioning` | — | [L1726](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L1726) |
| `folder` | `crafting` | Locked | 2 / 0 | `basic-requisitioning` | — | [L1748](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L1748) |
| `clipboard` | `crafting` | Locked | 3 / 0 | `basic-requisitioning` | — | [L1769](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L1769) |
| `requisition-slip` | `crafting` | Locked | 3 / 0 | `basic-requisitioning` | — | [L1791](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L1791) |
| `work-order-slip` | `crafting` | Locked | 4 / 0 | `work-order-generation` | — | [L1813](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L1813) |
| `certified-work-order` | `crafting` | Locked | 5 / 0 | `work-order-certification` | — | [L1836](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L1836) |
| `submitted-evaluation` | `crafting` | Locked | 5 / 0 | `evaluation-submission` | — | [L1860](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L1860) |
| `risk-assessment` | `crafting` | Locked | 5 / 0 | `preliminary-risk-assessment` | — | [L1884](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L1884) |
| `risk-assessed-work-order` | `crafting` | Locked | 5 / 0 | `risk-assessed-authorization` | — | [L1908](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L1908) |
| `corporate-waste-reprocessing` | `shaler` | Locked | 1 / 1 | `risk-assessed-authorization` | — | [L1932](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L1932) |
| `decompose-certified-work-order` | `crafting` | Locked | 1 / 0 | `evaluation-submission` | — | [L1955](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L1955) |
| `decompose-submitted-evaluation` | `crafting` | Locked | 1 / 0 | `preliminary-risk-assessment` | — | [L1975](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L1975) |
| `decompose-risk-assessed-work-order` | `crafting` | Locked | 1 / 0 | `risk-assessed-authorization` | — | [L1995](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L1995) |
| `decompose-audit-ready-deliverable` | `crafting` | Locked | 1 / 0 | `audit-ready-deliverables` | — | [L2015](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L2015) |
| `compliance-packet` | `crafting` | Locked | 4 / 0 | `compliance-packetization` | — | [L2036](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L2036) |
| `audit-ready-deliverable` | `crafting` | Locked | 4 / 0 | `audit-ready-deliverables` | — | [L2061](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L2061) |
| `stakeholder-review-summary` | `crafting` | Locked | 4 / 0 | `stakeholder-review-process` | DOWNSTREAM | [L2087](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L2087) |
| `liability-contained-report` | `crafting` | Locked | 4 / 0 | `liability-containment` | DOWNSTREAM | [L2113](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L2113) |
| `board-review-docket` | `crafting` | Locked | 4 / 0 | `board-review-procedure` | DOWNSTREAM | [L2138](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L2138) |
| `board-advisory-risk-assessment` | `crafting` | Locked | 5 / 0 | `board-advisory-risk-assessment` | DOWNSTREAM | [L2164](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L2164) |
| `hydrolyzed-suspension` | `crafting` | Locked | 4 / 0 | `brine-conditioning` | — | [L2195](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L2195) |
| `phase-diluted-brine` | `crafting` | Locked | 4 / 0 | `brine-conditioning` | — | [L2219](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L2219) |
| `osmotic-residue` | `crafting` | Locked | 4 / 0 | `brine-conditioning` | — | [L2243](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L2243) |
| `gradient-saline-matrix` | `crafting` | Locked | 4 / 0 | `brine-conditioning` | — | [L2267](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L2267) |
| `biphasic-brine-gel` | `crafting` | Locked | 4 / 0 | `brine-conditioning` | — | [L2291](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L2291) |
| `salinity-locked-emulsion` | `crafting` | Locked | 4 / 0 | `brine-conditioning` | — | [L2315](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L2315) |
| `hydrocoptic-precursor` | `crafting` | Locked | 4 / 0 | `brine-conditioning` | — | [L2339](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L2339) |
| `denatured-organic-base` | `crafting` | Locked | 4 / 0 | `organic-substrate-conditioning` | DOWNSTREAM | [L2364](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L2364) |
| `enzyme-saturated-mass` | `crafting` | Locked | 4 / 0 | `organic-substrate-conditioning` | DOWNSTREAM | [L2388](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L2388) |
| `lipid-carrier-gel` | `crafting` | Locked | 4 / 0 | `organic-substrate-conditioning` | DOWNSTREAM | [L2412](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L2412) |
| `bio-reactive-slurry` | `crafting` | Locked | 4 / 0 | `organic-substrate-conditioning` | DOWNSTREAM | [L2436](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L2436) |
| `catalytic-organic-medium` | `crafting` | Locked | 4 / 0 | `organic-substrate-conditioning` | DOWNSTREAM | [L2460](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L2460) |
| `reactive-enzyme-binder` | `crafting` | Locked | 4 / 0 | `organic-substrate-conditioning` | DOWNSTREAM | [L2485](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L2485) |
| `bio-synthetic-precursor` | `crafting` | Locked | 5 / 0 | `organic-substrate-conditioning` | DOWNSTREAM | [L2509](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L2509) |
| `crystalline-agglomerate` | `crafting` | Locked | 4 / 0 | `ceramic-lattice-conditioning` | — | [L2535](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L2535) |
| `fractured-lattice-mass` | `crafting` | Locked | 4 / 0 | `ceramic-lattice-conditioning` | — | [L2559](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L2559) |
| `ceramic-seed-grain` | `crafting` | Locked | 4 / 0 | `ceramic-lattice-conditioning` | — | [L2583](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L2583) |
| `mineral-phase-fragments` | `crafting` | Locked | 4 / 0 | `ceramic-lattice-conditioning` | — | [L2607](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L2607) |
| `ceramic-lattice-core` | `crafting` | Locked | 4 / 0 | `ceramic-lattice-conditioning` | — | [L2632](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L2632) |
| `compressed-crystal-bed` | `crafting` | Locked | 4 / 0 | `ceramic-lattice-conditioning` | — | [L2656](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L2656) |
| `bioceramic-preform` | `crafting` | Locked | 5 / 0 | `ceramic-lattice-conditioning` | — | [L2681](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L2681) |
| `charged-ionic-matrix` | `crafting` | Locked | 4 / 0 | `ionic-phase-conditioning` | — | [L2706](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L2706) |
| `dielectric-suspension` | `crafting` | Locked | 4 / 0 | `ionic-phase-conditioning` | — | [L2731](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L2731) |
| `conductive-residue` | `crafting` | Locked | 4 / 0 | `ionic-phase-conditioning` | — | [L2755](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L2755) |
| `phase-unstable-granulate` | `crafting` | Locked | 4 / 0 | `ionic-phase-conditioning` | — | [L2780](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L2780) |
| `balanced-reactive-medium` | `crafting` | Locked | 4 / 0 | `ionic-phase-conditioning` | — | [L2805](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L2805) |
| `phase-primed-carrier` | `crafting` | Locked | 4 / 0 | `ionic-phase-conditioning` | — | [L2830](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L2830) |
| `electro-phase-precursor` | `crafting` | Locked | 5 / 0 | `ionic-phase-conditioning` | — | [L2855](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L2855) |
| `marseline-compound` | `crafting` | Locked | 3 / 0 | `biomineral-synthesis` | DOWNSTREAM | [L2885](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L2885) |
| `bioceramic-grit` | `smelting` | Locked | 2 / 0 | `biomineral-synthesis` | — | [L2908](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L2908) |
| `hydrocoptic-crystal` | `Calcifier` | Locked | 2 / 1 | `biomineral-synthesis` | — | [L2930](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L2930) |
| `amulite-flakes` | `shaler` | Locked | 2 / 1 | `biomineral-synthesis` | DOWNSTREAM | [L2954](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L2954) |
| `phase-reactive-granules` | `crafting` | Locked | 3 / 0 | `biomineral-synthesis` | — | [L2977](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L2977) |
| `oscillated-lubricant` | `crafting` | Locked | 3 / 0 | `stabilized-emulsion-systems` | DOWNSTREAM | [L3006](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L3006) |
| `stabilized-brine-gel` | `crafting` | Locked | 2 / 0 | `stabilized-emulsion-systems` | DOWNSTREAM | [L3029](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L3029) |
| `dielectric-chowder` | `crafting` | Locked | 3 / 0 | `stabilized-emulsion-systems` | DOWNSTREAM | [L3051](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L3051) |
| `pre-turbulated-emulsion` | `crafting` | Locked | 3 / 0 | `stabilized-emulsion-systems` | DOWNSTREAM | [L3075](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L3075) |
| `viscoelastic-froth` | `crafting` | Locked | 3 / 0 | `stabilized-emulsion-systems` | DOWNSTREAM | [L3099](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L3099) |
| `compress-toxic-sludge` | `crafting-with-fluid` | Locked | 1 / 1 | `toxic-sludge-condensation` | — | [L3125](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L3125) |
| `industrial-waste-to-toxic-sludge` | `crafting-with-fluid` | Locked | 1 / 1 | `toxic-sludge-condensation` | — | [L3146](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L3146) |
| `radioactive-waste-to-toxic-sludge` | `crafting-with-fluid` | Locked | 1 / 1 | `toxic-sludge-condensation` | — | [L3168](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L3168) |
| `corporate-waste-to-toxic-sludge` | `crafting-with-fluid` | Locked | 1 / 1 | `toxic-sludge-condensation` | — | [L3190](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L3190) |
| `executive-marseline-resin` | `tank-ammo-component` | Locked | 3 / 0 | `pre-encabulation-materials` | DOWNSTREAM | [L3215](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L3215) |
| `encabuloy-alloy` | `crafting` | Locked | 4 / 0 | `pre-encabulation-materials` | — | [L3239](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L3239) |
| `hyperphase-matrix` | `tank-ammo-component` | Locked | 3 / 0 | `advanced-encabulation-substrates` | DOWNSTREAM | [L3264](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L3264) |
| `retrograde-polymer-sheet` | `crafting` | Locked | 3 / 0 | `advanced-encabulation-substrates` | DOWNSTREAM | [L3288](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L3288) |
| `duplexed-substrate` | `tank-ammo-component` | Locked | 3 / 0 | `advanced-encabulation-substrates` | DOWNSTREAM | [L3311](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L3311) |
| `Hydrocoptic-marselvanes` | `tank-ammo-component` | Locked | 3 / 0 | `encabulator-support-componentry` | DOWNSTREAM | [L3343](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L3343) |
| `PhaseDetractor` | `tank-ammo-component` | Locked | 3 / 0 | `encabulator-support-componentry` | DOWNSTREAM | [L3367](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L3367) |
| `Cradinal-grametter` | `tank-ammo-component` | Locked | 4 / 0 | `encabulator-support-componentry` | DOWNSTREAM | [L3391](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L3391) |
| `Alumatedplate` | `tank-ammo-component` | Locked | 3 / 0 | `alumated-plate-research` | DOWNSTREAM | [L3416](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L3416) |
| `Retro-Encabulator` | `tank-ammo-component` | Locked | 4 / 0 | `retro-encabulator-research` | DOWNSTREAM | [L3446](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L3446) |
| `Encabulator` | `tank-ammo-component` | Locked | 4 / 0 | `Encabulation-research` | DOWNSTREAM | [L3471](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L3471) |
| `SpervingArm` | `tank-ammo-component` | Locked | 4 / 0 | `sperving-arm-research` | DOWNSTREAM | [L3496](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L3496) |
| `DuctedSpervingArm` | `tank-ammo-component` | Locked | 4 / 0 | `ducted-sperving-arm-research` | DOWNSTREAM | [L3521](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L3521) |
| `TurboEncabulator` | `tank-ammo-component` | Locked | 4 / 0 | `Turbo-Encabulation-research` | DOWNSTREAM | [L3546](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L3546) |
| `HyperEncabulator` | `tank-ammo-component` | Locked | 4 / 0 | `Hyper-Encabulation-research` | DOWNSTREAM | [L3571](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L3571) |
| `DuplexedSpervingArm` | `tank-ammo-component` | Locked | 4 / 0 | `duplexed-sperving-arm-research` | DOWNSTREAM | [L3596](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L3596) |
| `FramulatedEncabulator` | `tank-ammo-component` | Locked | 4 / 0 | `framulated-encabulator-research` | DOWNSTREAM | [L3621](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L3621) |
| `tank-ammo-assembling-machine` | `tank-ammo-component` | Locked | 4 / 0 | `encabulated-device-integration` | DOWNSTREAM | [L3651](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L3651) |
| `tank-assembling-machine` | `tank-ammo-component` | Locked | 4 / 0 | `encabulated-device-integration` | DOWNSTREAM | [L3672](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L3672) |
| `tank-light-chasis-wlsk` | `tank-crafting` | Locked | 4 / 0 | `modular-tank-research2` | DOWNSTREAM | [L3693](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L3693) |
| `tank-ammo-universal-explosive` | `tank-ammo-component` | Locked | 2 / 0 | `explosive-encabulation-engineering` | DOWNSTREAM | [L3719](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L3719) |
| `tank-ammo-universal-explosive-synthetic` | `tank-ammo-component` | Locked | 2 / 0 | `organic-explosives` | — | [L3742](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L3742) |
| `tank-ammo-explosive-synthetic` | `tank-ammo-component` | Locked | 2 / 0 | `organic-explosives` | — | [L3766](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L3766) |
| `tank-ammo-industrial-coke` | `tank-ammo-component` | Locked | 2 / 0 | `industrial-coke-processing` | TANK-FLUID | [L3790](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L3790) |
| `tank-ammo-Explosive-Engineering` | `tank-ammo-component` | Locked | 2 / 0 | `explosive-encabulation-engineering` | — | [L3814](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L3814) |
| `Rubberized-timber` | `tank-ammo-component` | Locked | 2 / 1 | `industrial-coke-processing` | TANK-FLUID | [L3837](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L3837) |
| `tank-ammo-casing` | `tank-ammo-component` | Locked | 1 / 0 | `tank-casing-research` | — | [L3860](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L3860) |
| `tank-ammo-reinforced-casing` | `tank-ammo-component` | Locked | 1 / 0 | `tank-casing-research` | — | [L3878](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L3878) |
| `land-mine-poison` | `tank-ammo-component` | Locked | 3 / 0 | `new-munitions` | — | [L3897](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/recipe.lua#L3897) |
| `flame-thrower-ammo-tanker` | `tank-ammo-component` | Locked | 2 / 0 | `modular-tank-research` | — | [L4](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/ammo.lua#L4) |
| `flame-thrower-ammo-tanker-2` | `tank-ammo-component` | Locked | 1 / 0 | `modular-tank-research` | — | [L22](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/ammo.lua#L22) |
| `ap-bullet-brick` | `tank-ammo-component` | Locked | 2 / 0 | `mechanized-infantry-research` | — | [L39](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/ammo.lua#L39) |
| `piercing-shotgun-shell-brick` | `tank-ammo-component` | Locked | 2 / 0 | `mechanized-infantry-research` | — | [L54](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/ammo.lua#L54) |
| `45mm-auto` | `tank-ammo-component` | Locked | 2 / 0 | `modular-tank-research` | — | [L69](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/ammo.lua#L69) |
| `50mm-mortar` | `tank-ammo-component` | Locked | 2 / 0 | `modular-tank-research` | — | [L84](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/ammo.lua#L84) |
| `50mm-mortar-poison` | `tank-ammo-component` | Locked | 3 / 0 | `new-munitions` | — | [L99](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/ammo.lua#L99) |
| `minepack` | `tank-ammo-component` | Locked | 2 / 0 | `modular-tank-research3` | — | [L115](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/ammo.lua#L115) |
| `minepack-poison` | `tank-ammo-component` | Locked | 2 / 0 | `new-munitions` | — | [L130](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/ammo.lua#L130) |
| `rocketpack` | `tank-ammo-component` | Locked | 3 / 0 | `modular-tank-research3` | — | [L145](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/ammo.lua#L145) |
| `cannon-shell-2` | `tank-ammo-component` | Locked | 2 / 0 | `modular-tank-research` | — | [L161](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/ammo.lua#L161) |
| `wmdartillery-ammo` | `tank-ammo-component` | Locked | 4 / 0 | `super-tank-research2` | — | [L176](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/ammo.lua#L176) |
| `tank-wmd-ammo` | `tank-ammo-component` | Locked | 5 / 0 | `super-tank-research2` | — | [L199](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/ammo.lua#L199) |
| `cannon-shell-convert` | `tank-ammo-component` | Locked | 1 / 0 | `modular-tank-research` | — | [L225](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/ammo.lua#L225) |
| `flame-tank` | `tank-crafting` | Locked | 4 / 0 | `modular-tank-research` | DOWNSTREAM | [L4](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/vehicles.lua#L4) |
| `auto-tank` | `tank-crafting` | Locked | 4 / 0 | `modular-tank-research` | DOWNSTREAM | [L21](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/vehicles.lua#L21) |
| `nade-tank` | `tank-crafting` | Locked | 4 / 0 | `modular-tank-research` | DOWNSTREAM | [L38](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/vehicles.lua#L38) |
| `flame-tank-wlsk` | `tank-crafting` | Locked | 2 / 0 | `modular-tank-research2` | DOWNSTREAM | [L55](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/vehicles.lua#L55) |
| `auto-tank-wlsk` | `tank-crafting` | Locked | 2 / 0 | `modular-tank-research2` | DOWNSTREAM | [L70](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/vehicles.lua#L70) |
| `nade-tank-wlsk` | `tank-crafting` | Locked | 2 / 0 | `modular-tank-research2` | DOWNSTREAM | [L85](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/vehicles.lua#L85) |
| `mine-tank` | `tank-crafting` | Locked | 4 / 0 | `modular-tank-research3` | DOWNSTREAM | [L100](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/vehicles.lua#L100) |
| `rocket-tank` | `tank-crafting` | Locked | 4 / 0 | `modular-tank-research3` | DOWNSTREAM | [L117](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/vehicles.lua#L117) |
| `super-tank` | `tank-crafting` | Locked | 4 / 0 | `super-tank-research` | DOWNSTREAM | [L134](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/vehicles.lua#L134) |
| `super-tank-alternate` | `tank-crafting` | Locked | 4 / 0 | `super-tank-research` | DOWNSTREAM | [L151](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/vehicles.lua#L151) |
| `super-tank-wmd` | `tank-crafting` | Locked | 4 / 0 | `super-tank-research2` | DOWNSTREAM | [L168](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/vehicles.lua#L168) |
| `car-flamer` | `tank-crafting` | Locked | 3 / 0 | `modular-tank-research` | DOWNSTREAM | [L185](../../tanks_for_bob_fork_1.8.94/prototypes/recipe/vehicles.lua#L185) |

## Complete technology inventory (88 rows)

`RESEARCH-AT-RISK` is a *conditional* transitive flag under the missing rendered-organics input. All remaining nodes may still have other gameplay or economic requirements not modeled by the graph.

| Technology | Prerequisites (count) | Research ingredient types | Recipe unlocks | Finding | Source |
| --- | ---: | --- | ---: | --- | --- |
| `beachpump` | 0 | `Seared-fish` | 1 | — | [L12](../../tanks_for_bob_fork_1.8.94/prototypes/technology/technology.lua#L12) |
| `wood-basin` | 1 | `Seared-fish` | 1 | — | [L32](../../tanks_for_bob_fork_1.8.94/prototypes/technology/technology.lua#L32) |
| `stone-water-wheel` | 2 | `Seared-fish` | 1 | — | [L48](../../tanks_for_bob_fork_1.8.94/prototypes/technology/technology.lua#L48) |
| `solar-boiler` | 1 | `Seared-fish` | 1 | — | [L64](../../tanks_for_bob_fork_1.8.94/prototypes/technology/technology.lua#L64) |
| `primitive-steam-powered-pump` | 1 | `Seared-fish` | 1 | — | [L80](../../tanks_for_bob_fork_1.8.94/prototypes/technology/technology.lua#L80) |
| `steam-condenser` | 2 | `Seared-fish` | 1 | — | [L96](../../tanks_for_bob_fork_1.8.94/prototypes/technology/technology.lua#L96) |
| `calcifier` | 1 | `Seared-fish` | 1 | — | [L112](../../tanks_for_bob_fork_1.8.94/prototypes/technology/technology.lua#L112) |
| `shaler` | 1 | `Seared-fish` | 1 | — | [L128](../../tanks_for_bob_fork_1.8.94/prototypes/technology/technology.lua#L128) |
| `growing-plot` | 1 | `Seared-fish` | 1 | — | [L148](../../tanks_for_bob_fork_1.8.94/prototypes/technology/technology.lua#L148) |
| `wood-spear` | 1 | `Seared-fish` | 1 | — | [L164](../../tanks_for_bob_fork_1.8.94/prototypes/technology/technology.lua#L164) |
| `cooking-fire` | 2 | `Seared-fish` | 1 | — | [L180](../../tanks_for_bob_fork_1.8.94/prototypes/technology/technology.lua#L180) |
| `meal` | 1 | `Seared-fish` | 1 | — | [L196](../../tanks_for_bob_fork_1.8.94/prototypes/technology/technology.lua#L196) |
| `stone-tools` | 1 | `Seared-fish`, `meal` | 1 | — | [L212](../../tanks_for_bob_fork_1.8.94/prototypes/technology/technology.lua#L212) |
| `pondering-hovel` | 2 | `Seared-fish`, `meal` | 1 | — | [L228](../../tanks_for_bob_fork_1.8.94/prototypes/technology/technology.lua#L228) |
| `quarry` | 1 | `Seared-fish`, `meal` | 1 | — | [L244](../../tanks_for_bob_fork_1.8.94/prototypes/technology/technology.lua#L244) |
| `clay-pit` | 1 | `Seared-fish` | 1 | — | [L264](../../tanks_for_bob_fork_1.8.94/prototypes/technology/technology.lua#L264) |
| `fish-pond` | 3 | `Seared-fish` | 1 | — | [L280](../../tanks_for_bob_fork_1.8.94/prototypes/technology/technology.lua#L280) |
| `pit-kiln` | 1 | `Seared-fish` | 1 | — | [L296](../../tanks_for_bob_fork_1.8.94/prototypes/technology/technology.lua#L296) |
| `brick` | 1 | `Seared-fish` | 1 | — | [L312](../../tanks_for_bob_fork_1.8.94/prototypes/technology/technology.lua#L312) |
| `crude-glass` | 1 | `Seared-fish` | 1 | — | [L328](../../tanks_for_bob_fork_1.8.94/prototypes/technology/technology.lua#L328) |
| `Steam-Compressor` | 4 | `Seared-fish`, `meal` | 4 | — | [L348](../../tanks_for_bob_fork_1.8.94/prototypes/technology/technology.lua#L348) |
| `charcoal-processing` | 1 | `Seared-fish` | 1 | — | [L371](../../tanks_for_bob_fork_1.8.94/prototypes/technology/technology.lua#L371) |
| `wood-pulp-processing` | 2 | `Seared-fish` | 1 | — | [L387](../../tanks_for_bob_fork_1.8.94/prototypes/technology/technology.lua#L387) |
| `crude-paperwork` | 1 | `Seared-fish` | 2 | — | [L403](../../tanks_for_bob_fork_1.8.94/prototypes/technology/technology.lua#L403) |
| `basic-requisitioning` | 3 | `Seared-fish`, `meal` | 5 | — | [L420](../../tanks_for_bob_fork_1.8.94/prototypes/technology/technology.lua#L420) |
| `work-order-generation` | 1 | `Seared-fish`, `meal`, `requisition-slip` | 1 | — | [L440](../../tanks_for_bob_fork_1.8.94/prototypes/technology/technology.lua#L440) |
| `work-order-certification` | 1 | `Seared-fish`, `meal`, `work-order-slip` | 1 | — | [L456](../../tanks_for_bob_fork_1.8.94/prototypes/technology/technology.lua#L456) |
| `evaluation-submission` | 2 | `Seared-fish`, `meal`, `certified-work-order` | 2 | — | [L472](../../tanks_for_bob_fork_1.8.94/prototypes/technology/technology.lua#L472) |
| `preliminary-risk-assessment` | 3 | `Seared-fish`, `meal`, `submitted-evaluation` | 2 | — | [L489](../../tanks_for_bob_fork_1.8.94/prototypes/technology/technology.lua#L489) |
| `toxic-sludge-condensation` | 1 | `Seared-fish`, `meal`, `risk-assessed-work-order` | 4 | — | [L506](../../tanks_for_bob_fork_1.8.94/prototypes/technology/technology.lua#L506) |
| `risk-assessed-authorization` | 1 | `Seared-fish`, `meal`, `risk-assessment` | 3 | — | [L532](../../tanks_for_bob_fork_1.8.94/prototypes/technology/technology.lua#L532) |
| `compliance-packetization` | 2 | `Seared-fish`, `meal`, `risk-assessed-work-order` | 1 | — | [L550](../../tanks_for_bob_fork_1.8.94/prototypes/technology/technology.lua#L550) |
| `audit-ready-deliverables` | 1 | `Seared-fish`, `meal`, `compliance-packet` | 2 | — | [L566](../../tanks_for_bob_fork_1.8.94/prototypes/technology/technology.lua#L566) |
| `stakeholder-review-process` | 2 | `Seared-fish`, `meal`, `audit-ready-deliverable` | 1 | — | [L583](../../tanks_for_bob_fork_1.8.94/prototypes/technology/technology.lua#L583) |
| `liability-containment` | 1 | `Seared-fish`, `meal`, `stakeholder-review-summary` | 1 | RESEARCH-AT-RISK | [L599](../../tanks_for_bob_fork_1.8.94/prototypes/technology/technology.lua#L599) |
| `board-review-procedure` | 2 | `Seared-fish`, `meal`, `liability-contained-report` | 1 | RESEARCH-AT-RISK | [L615](../../tanks_for_bob_fork_1.8.94/prototypes/technology/technology.lua#L615) |
| `board-advisory-risk-assessment` | 3 | `Seared-fish`, `meal`, `board-review-docket`, `liability-contained-report` | 1 | RESEARCH-AT-RISK | [L631](../../tanks_for_bob_fork_1.8.94/prototypes/technology/technology.lua#L631) |
| `waste-processing-2` | 2 | `Seared-fish`, `meal`, `work-order-slip` | 3 | — | [L651](../../tanks_for_bob_fork_1.8.94/prototypes/technology/technology.lua#L651) |
| `waste-processing-3` | 3 | `Seared-fish`, `meal`, `certified-work-order` | 3 | — | [L669](../../tanks_for_bob_fork_1.8.94/prototypes/technology/technology.lua#L669) |
| `mineral-fractionation` | 4 | `Seared-fish`, `meal`, `work-order-slip` | 4 | — | [L693](../../tanks_for_bob_fork_1.8.94/prototypes/technology/technology.lua#L693) |
| `ceramic-lattice-conditioning` | 4 | `Seared-fish`, `meal`, `submitted-evaluation` | 7 | — | [L712](../../tanks_for_bob_fork_1.8.94/prototypes/technology/technology.lua#L712) |
| `bio-reactive-processing` | 3 | `Seared-fish`, `meal`, `certified-work-order` | 4 | — | [L736](../../tanks_for_bob_fork_1.8.94/prototypes/technology/technology.lua#L736) |
| `organic-substrate-conditioning` | 2 | `Seared-fish`, `meal`, `submitted-evaluation` | 7 | — | [L755](../../tanks_for_bob_fork_1.8.94/prototypes/technology/technology.lua#L755) |
| `brine-conditioning` | 3 | `Seared-fish`, `meal`, `risk-assessment` | 7 | — | [L779](../../tanks_for_bob_fork_1.8.94/prototypes/technology/technology.lua#L779) |
| `stabilized-emulsion-systems` | 4 | `Seared-fish`, `meal`, `audit-ready-deliverable` | 5 | — | [L801](../../tanks_for_bob_fork_1.8.94/prototypes/technology/technology.lua#L801) |
| `ionic-phase-conditioning` | 3 | `Seared-fish`, `meal`, `risk-assessed-work-order` | 7 | — | [L823](../../tanks_for_bob_fork_1.8.94/prototypes/technology/technology.lua#L823) |
| `biomineral-synthesis` | 4 | `Seared-fish`, `meal`, `compliance-packet` | 5 | — | [L845](../../tanks_for_bob_fork_1.8.94/prototypes/technology/technology.lua#L845) |
| `pre-encabulation-materials` | 3 | `Seared-fish`, `meal`, `audit-ready-deliverable` | 2 | — | [L869](../../tanks_for_bob_fork_1.8.94/prototypes/technology/technology.lua#L869) |
| `advanced-encabulation-substrates` | 3 | `Seared-fish`, `meal`, `stakeholder-review-summary` | 3 | RESEARCH-AT-RISK | [L886](../../tanks_for_bob_fork_1.8.94/prototypes/technology/technology.lua#L886) |
| `alumated-plate-research` | 2 | `Seared-fish`, `meal`, `compliance-packet` | 1 | — | [L904](../../tanks_for_bob_fork_1.8.94/prototypes/technology/technology.lua#L904) |
| `tank-casing-research` | 2 | `Seared-fish`, `meal`, `risk-assessed-work-order` | 2 | — | [L920](../../tanks_for_bob_fork_1.8.94/prototypes/technology/technology.lua#L920) |
| `encabulator-support-componentry` | 3 | `Seared-fish`, `meal`, `compliance-packet` | 3 | — | [L939](../../tanks_for_bob_fork_1.8.94/prototypes/technology/technology.lua#L939) |
| `retro-encabulator-research` | 3 | `Seared-fish`, `meal`, `compliance-packet` | 1 | RESEARCH-AT-RISK | [L962](../../tanks_for_bob_fork_1.8.94/prototypes/technology/technology.lua#L962) |
| `Encabulation-research` | 3 | `Seared-fish`, `meal`, `audit-ready-deliverable` | 1 | RESEARCH-AT-RISK | [L978](../../tanks_for_bob_fork_1.8.94/prototypes/technology/technology.lua#L978) |
| `Turbo-Encabulation-research` | 3 | `Seared-fish`, `meal`, `stakeholder-review-summary` | 1 | RESEARCH-AT-RISK | [L995](../../tanks_for_bob_fork_1.8.94/prototypes/technology/technology.lua#L995) |
| `Hyper-Encabulation-research` | 3 | `Seared-fish`, `meal`, `liability-contained-report` | 1 | RESEARCH-AT-RISK | [L1011](../../tanks_for_bob_fork_1.8.94/prototypes/technology/technology.lua#L1011) |
| `framulated-encabulator-research` | 3 | `Seared-fish`, `meal`, `board-review-docket` | 1 | RESEARCH-AT-RISK | [L1028](../../tanks_for_bob_fork_1.8.94/prototypes/technology/technology.lua#L1028) |
| `sperving-arm-research` | 3 | `Seared-fish`, `meal`, `audit-ready-deliverable` | 1 | RESEARCH-AT-RISK | [L1051](../../tanks_for_bob_fork_1.8.94/prototypes/technology/technology.lua#L1051) |
| `ducted-sperving-arm-research` | 4 | `Seared-fish`, `meal`, `stakeholder-review-summary` | 1 | RESEARCH-AT-RISK | [L1067](../../tanks_for_bob_fork_1.8.94/prototypes/technology/technology.lua#L1067) |
| `duplexed-sperving-arm-research` | 3 | `Seared-fish`, `meal`, `liability-contained-report` | 1 | RESEARCH-AT-RISK | [L1084](../../tanks_for_bob_fork_1.8.94/prototypes/technology/technology.lua#L1084) |
| `organic-explosives` | 3 | `Seared-fish`, `meal`, `submitted-evaluation` | 3 | — | [L1104](../../tanks_for_bob_fork_1.8.94/prototypes/technology/technology.lua#L1104) |
| `explosive-encabulation-engineering` | 3 | `Seared-fish`, `meal`, `stakeholder-review-summary` | 2 | RESEARCH-AT-RISK | [L1122](../../tanks_for_bob_fork_1.8.94/prototypes/technology/technology.lua#L1122) |
| `industrial-coke-processing` | 3 | `Seared-fish`, `meal`, `liability-contained-report` | 2 | RESEARCH-AT-RISK | [L1139](../../tanks_for_bob_fork_1.8.94/prototypes/technology/technology.lua#L1139) |
| `encabulated-waste-recovery` | 4 | `Seared-fish`, `meal`, `liability-contained-report` | 4 | RESEARCH-AT-RISK | [L1156](../../tanks_for_bob_fork_1.8.94/prototypes/technology/technology.lua#L1156) |
| `waste-processing-4-authorization` | 3 | `meal`, `stakeholder-review-summary` | 0 | RESEARCH-AT-RISK | [L1175](../../tanks_for_bob_fork_1.8.94/prototypes/technology/technology.lua#L1175) |
| `waste-processing-4` | 3 | `automation-science-pack`, `logistic-science-pack` | 3 | RESEARCH-AT-RISK | [L1190](../../tanks_for_bob_fork_1.8.94/prototypes/technology/technology.lua#L1190) |
| `waste-processing-5-authorization` | 4 | `meal`, `board-advisory-risk-assessment` | 0 | RESEARCH-AT-RISK | [L1208](../../tanks_for_bob_fork_1.8.94/prototypes/technology/technology.lua#L1208) |
| `waste-processing-5` | 4 | `automation-science-pack`, `logistic-science-pack`, `military-science-pack` | 3 | RESEARCH-AT-RISK | [L1223](../../tanks_for_bob_fork_1.8.94/prototypes/technology/technology.lua#L1223) |
| `encabulated-device-integration-authorization` | 4 | `meal`, `board-review-docket` | 0 | RESEARCH-AT-RISK | [L1246](../../tanks_for_bob_fork_1.8.94/prototypes/technology/technology.lua#L1246) |
| `encabulated-device-integration` | 1 | `automation-science-pack`, `logistic-science-pack` | 2 | RESEARCH-AT-RISK | [L1261](../../tanks_for_bob_fork_1.8.94/prototypes/technology/technology.lua#L1261) |
| `modular-tank-research-authorization` | 2 | `meal`, `board-review-docket` | 0 | RESEARCH-AT-RISK | [L1279](../../tanks_for_bob_fork_1.8.94/prototypes/technology/technology.lua#L1279) |
| `modular-tank-research` | 2 | `automation-science-pack`, `logistic-science-pack`, `military-science-pack` | 10 | RESEARCH-AT-RISK | [L1294](../../tanks_for_bob_fork_1.8.94/prototypes/technology/technology.lua#L1294) |
| `modular-tank-research2-authorization` | 2 | `meal`, `liability-contained-report` | 0 | RESEARCH-AT-RISK | [L1320](../../tanks_for_bob_fork_1.8.94/prototypes/technology/technology.lua#L1320) |
| `modular-tank-research2` | 2 | `automation-science-pack`, `logistic-science-pack`, `military-science-pack` | 4 | RESEARCH-AT-RISK | [L1335](../../tanks_for_bob_fork_1.8.94/prototypes/technology/technology.lua#L1335) |
| `modular-tank-research3-authorization` | 2 | `meal`, `liability-contained-report` | 0 | RESEARCH-AT-RISK | [L1355](../../tanks_for_bob_fork_1.8.94/prototypes/technology/technology.lua#L1355) |
| `modular-tank-research3` | 3 | `automation-science-pack`, `logistic-science-pack`, `military-science-pack` | 4 | RESEARCH-AT-RISK | [L1370](../../tanks_for_bob_fork_1.8.94/prototypes/technology/technology.lua#L1370) |
| `mechanized-infantry-authorization` | 2 | `meal`, `risk-assessed-work-order` | 0 | RESEARCH-AT-RISK | [L1390](../../tanks_for_bob_fork_1.8.94/prototypes/technology/technology.lua#L1390) |
| `mechanized-infantry-research` | 1 | `automation-science-pack`, `logistic-science-pack`, `military-science-pack` | 3 | RESEARCH-AT-RISK | [L1405](../../tanks_for_bob_fork_1.8.94/prototypes/technology/technology.lua#L1405) |
| `new-munitions-authorization` | 2 | `meal`, `board-review-docket` | 0 | RESEARCH-AT-RISK | [L1424](../../tanks_for_bob_fork_1.8.94/prototypes/technology/technology.lua#L1424) |
| `new-munitions` | 3 | `automation-science-pack`, `logistic-science-pack`, `military-science-pack` | 3 | RESEARCH-AT-RISK | [L1439](../../tanks_for_bob_fork_1.8.94/prototypes/technology/technology.lua#L1439) |
| `organic-explosives2-authorization` | 3 | `meal`, `stakeholder-review-summary` | 0 | RESEARCH-AT-RISK | [L1458](../../tanks_for_bob_fork_1.8.94/prototypes/technology/technology.lua#L1458) |
| `organic-explosives2` | 3 | `automation-science-pack`, `logistic-science-pack`, `military-science-pack` | 0 | RESEARCH-AT-RISK | [L1473](../../tanks_for_bob_fork_1.8.94/prototypes/technology/technology.lua#L1473) |
| `organic-explosives3-authorization` | 3 | `meal`, `board-review-docket` | 0 | RESEARCH-AT-RISK | [L1493](../../tanks_for_bob_fork_1.8.94/prototypes/technology/technology.lua#L1493) |
| `organic-explosives3` | 3 | `automation-science-pack`, `logistic-science-pack`, `military-science-pack` | 0 | RESEARCH-AT-RISK | [L1508](../../tanks_for_bob_fork_1.8.94/prototypes/technology/technology.lua#L1508) |
| `super-tank-authorization` | 3 | `meal`, `board-advisory-risk-assessment` | 0 | RESEARCH-AT-RISK | [L1527](../../tanks_for_bob_fork_1.8.94/prototypes/technology/technology.lua#L1527) |
| `super-tank-research` | 4 | `automation-science-pack`, `logistic-science-pack`, `military-science-pack` | 2 | RESEARCH-AT-RISK | [L1542](../../tanks_for_bob_fork_1.8.94/prototypes/technology/technology.lua#L1542) |
| `super-tank-wmd-authorization` | 3 | `meal`, `board-advisory-risk-assessment` | 0 | RESEARCH-AT-RISK | [L1559](../../tanks_for_bob_fork_1.8.94/prototypes/technology/technology.lua#L1559) |
| `super-tank-research2` | 3 | `automation-science-pack`, `logistic-science-pack`, `military-science-pack` | 3 | RESEARCH-AT-RISK | [L1574](../../tanks_for_bob_fork_1.8.94/prototypes/technology/technology.lua#L1574) |

## Follow-up implementation in v1.8.95

The original inventory above is a **snapshot of the 1.8.94 problem state**;
its line references continue to point at the audited version. The next
version addresses the confirmed mechanical category/port defects:

- `workbench.ingredient_count`: **2 → 3**, allowing all five distinct
  three-ingredient `Seablock` structure recipes.
- `cooking-fire`: **north fluid input** for `rendered-organics` and
  `steam-meal` using its existing `advcooking` category.
- `tank-ammo-assembling-machine`: **north input / south output** fluid
  boxes for `Rubberized-timber` and `tank-ammo-industrial-coke`.
- `ci/recipe_machine_audit.lua`: nine specific regression checks inside
  the existing single-profile Factorio engine CI job.

The apparent **55-recipe / 39-technology impact** is a conditional
transitive dependency estimate for the original broken `rendered-organics`
production path, **not** 55 independent source defects. Repair of the root
steam-input mismatch removes that modeled blocker, but manual full-graph
research and factory operation still must be demonstrated.
