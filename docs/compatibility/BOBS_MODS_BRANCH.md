# Bob's Mods compatibility branch — implementation plan

**Tracking issue:** [#1](https://github.com/mrcalzon02/Tanks-for-bob-Fork/issues/1)  
**Working branch:** [`compat/bobs-mods`](https://github.com/mrcalzon02/Tanks-for-bob-Fork/tree/compat/bobs-mods)  
**Base:** `main`; **active package under test:** `tanks_for_bob_fork_1.8.95`, Factorio 2.0.  
**Release status:** experimental only; no merge, tag, Mod Portal upload, or 2.1 retag until acceptance. Version must be incremented before eventual release.

## Goals and invariants

1. One fork distribution which works with **base-only**, official full-expansion, selected Bob modules, and the complete Bob suite. Bob's Mods remain optional; do not fork, embed or redistribute their code.
2. One **GitHub Actions job** and **one active combined integration environment**. Preserve the previously working official-mod headless check as the baseline within that same job; do not introduce a matrix/fanout of separate jobs.
3. Respect Bob's own configuration flags and prototype namespaces. Every modification must test both `mods["<id>"]` and prototype presence, avoid duplicate categories, and avoid altering Bob-owned definitions unless absolutely required.
4. Do not equate a successful data-stage launch with complete tech, resource, combat, performance, graphical, save or multiplayer compatibility. Keep observations and acceptance gates separate.
5. Do not change the published 1.8.95 release; branch development edits are unreleased until a new version is deliberately packaged and verified.

## Bob family discovery inventory

The Bob's (Updated) Modpack dependency list includes: `bobassembly`, `bobclasses`, `bobelectronics`, `bobenemies`, `bobequipment`, `bobgreenhouse`, `bobinserters`, `boblibrary`, `boblocale`, `boblogistics`, `bobmining`, `bobmodules`, `bobores`, `bobplates`, `bobpower`, `bobrevamp`, `bobtech`, `bobvehicleequipment`, `bobwarfare`. See https://mods.factorio.com/mod/Bobs-updated-modpack/dependencies and https://github.com/modded-factorio/bobsmods.

**Version discipline:** Factorio 2.0 must use Bob releases whose `info.json.factorio_version` is 2.0 (2.1.x module versions can still target engine 2.0); Bob's 3.0.x modules target the Factorio 2.1 family. Resolve each module to exact engine-compatible Portal release metadata, transitive dependencies, URL and SHA-256 before testing. Never download unverified `latest` (which may select a 2.1-only module) in the 2.0 environment.

## Configuration contract

| Setting / flag | Owner | Meaning | Default / rule |
| --- | --- | --- | --- |
| `tfbf-bobs-equipment-grids` | this fork | Assign Bob's vehicle equipment grids to fork-owned tank entities when `bobvehicleequipment` is present | true; does nothing without Bob module |
| `bobmods-vehicleequipment-enablevehiclegrids` | Bob | Enables equipment grids on base vehicles | Respect false; never override |
| `mods["bobvehicleequipment"]` | engine | Bob equipment integration detection | Require for grid mapping |
| `mods["bobassembly"]` | engine | Bob assembling integration detection | Validate *final* crafting categories first |
| `mods["bobplates"]` | engine | Bob metallurgy and intermediates | Design stage-specific recipes only after graph checks |
| `mods["bobwarfare"]` | engine | Bob tanks/ammunition/technologies | Check `bob-tanks-2/3`, no unconditional cross-caliber ammo |
| `mods["bobtech"]` | engine | Expanded labs/science | Validate research acceptance and prerequisite closure |

Additional toggles for metallurgy, tech conversion or ammunition are **not implemented** until their effects have been designed and runtime-tested; don't expose inert UI settings.

## Phased work (issue #1 is the single tracker)

- [x] **Phase 0:** branch created and linked to issue #1.
- [x] **Phase 1a:** source evaluation completed; identify Bob module IDs, assembler-copy behavior, equipment-grid omission and research/material dependencies.
- [x] **Phase 1b (source-level only):** add optional metadata for Bob family, a guarded equipment-grid adapter, a startup enable switch and static assertions; verify the edits on the branch.
- [x] **Phase 2:** produce one version-locked, licensed, reproducible Factorio 2.0 combined mod directory: `base`, `elevated-rails`, `quality`, `space-age`, `tanks_for_bob_fork`, and full Bob family. Keep mod credentials in Actions secrets; never log them or commit them.
- [ ] **Phase 3 (in progress; prototypes covered, progression incomplete):** complete the actual data-stage inventory: duplicate prototypes; every fork recipe's ingredient/result and recipe category; machines including Bob assembler 4/5/6; Bob equipment grids/categories; lab science acceptance; tech prerequisites/unlocks; resource reachability and pollution/waste/recycling outputs. Record exact failures, not guesses.
- [ ] **Phase 4:** add guarded, stage-appropriate Bob material, electronics, warfare, tank upgrade, ammo and research integrations, verifying progression after each small change. Do not replace a reachable vanilla branch with an unreachable Bob-only ingredient.
- [ ] **Phase 5:** execute headless create/benchmark/server, save/reload, ammunition inventory and firing/damage probes; record entity and recipe outcomes. Real multiplayer and graphical client checks remain distinct manual acceptance tasks.
- [ ] **Phase 6:** review result, add truthful support table and release notes, bump to a new version only when ready; merge only after all required game lifecycle/updater gates pass. Maintain one Actions job.

## First patch: equipment grids

From Bob's source `bobvehicleequipment/prototypes/equipment-grid.lua`: `bob-car` is 8x2, `bob-tank` 6x8, `bob-tank-2` 6x10, and `bob-tank-3` 6x12. Bob's own `data-updates.lua` assigns equipment grids to its tanks and vanilla tanks but not this fork's independently cloned tanks.

Initial intentional classification, subject to runtime balance review:
- `car-flamer`: `bob-car`
- `modular-tank`, `flame-tank`, `auto-tank`, `nade-tank`: `bob-tank`
- `flame-tank-wlsk`, `auto-tank-wlsk`, `nade-tank-wlsk`, `mine-tank`, `rocket-tank`: `bob-tank-2`
- `super-tank`, `super-tank-alternate`, `super-tank-wmd`: `bob-tank-3`

Apply in `data-final-fixes.lua`, after Bob's base assignments, only when both parties' startup switches allow it and the target equipment grid exists. Do not claim vehicle equipment works until the game loads and test equipment can be inserted.

## CI stage fidelity repair

`ci/stage_profile.py` selects the highest versioned source folder (currently 1.8.95). The old staging logic **overwrote** `data-final-fixes.lua` with the audit, which would silently bypass any compatibility adapter. Branch commit `d5612ac` stages `ci_data_audit.lua` and *appends* its require to the existing `data-final-fixes.lua` instead. This change passed a one-profile Factorio smoke and the full Bob suite; the original production data-final-fixes runs in the staged test. The current CI profile still enables **only official mods**, never Bob's mods; it cannot validate Bob integration until the version-locked combined mod directory is implemented.

## First verified full-family engine run

[GitHub Actions run #42153521791](https://github.com/mrcalzon02/Tanks-for-bob-Fork/actions/runs/42153521791) completed **success** on the 1.8.95 source under Factorio **2.0.77** with all 19 pinned Bob modules, plus Base, Elevated Rails, Quality and Space Age. The CI artifact `tanks-factorio-one-profile-audit` contains actual `mod-list.json`, Bob versions, Portal SHA-1s and downloaded SHA-256 hashes, `create.log`, `benchmark.log` and server logs.

Game evidence (from `create.log` and `suite-results.json`):
- `BOBS_AUDIT_CHECKED fork_vehicles=13 mapped_grids=13 expected_grids=true bob_assemblers=3 craft_category_matches=6/6 custom_labs=2 missing_fork_tech=0`.
- `DATA_AUDIT recipes=2610 technologies=769 ... tank_recipes=59 tank_without_unlock=0 no_machine=0 recycling_guards=3 warnings=0`.
- `SOURCE_REGISTRY_PASS declared_recipes=210 declared_technologies=88 recipes_missing_unlock=0`.
- `SUPPLY_GRAPH ... mod_recipes=210 optimistic_reachable=210 optimistic_blocked=0` (does **not** demonstrate practical science/technology/machinery reachability).
- `WEAPON_AUDIT ... vehicles=13 gun_slots=26 ... declared_ammo=13 declared_ammo_craftable=13 warnings=0`; no shots fired in this test.
- `RUNTIME_PASS tick=300 vehicles_spawned=8`, `DAMAGE_RESPONSE_PASS tick=600` and `AMMO_INVENTORY_CHECKED tick=900 attempted=7 accepted=7 skipped=1` (the missing flame-tank is a destroyed/absent diagnostic, not proven incompatibility).
- Map creation, 1,200-tick benchmark and private headless server startup **passed**. No new release was published.

**Subsequent live tests:**
- [Run #42153968206](https://github.com/mrcalzon02/Tanks-for-bob-Fork/actions/runs/42153968206) PASS. Actual `LuaEquipmentGrid.put` insertion at tick 1050: **7 surviving custom tanks**, **21 accepted Bob battery/motor/shield insertions**, **0 rejected**. Map/benchmark/server still passed.
- [Run #42154256045](https://github.com/mrcalzon02/Tanks-for-bob-Fork/actions/runs/42154256045) PASS. `BOBS_TECH_LAB_AUDIT technologies=90 lab_supported=90 no_lab=0 missing_science=0` for the fork science-requiring technologies plus Bob's `bob-tanks-2/3`; the 21/21 live equipment insertions still passed.
- **Remaining:** the optimistic recipe supply calculation is not a research-gated progression proof, and ammunition insertion does not prove actual firing/projectile hits. Client graphics, multiplayer and save migration still require appropriate evidence.

Exact pin amendment: Bob's Adjustable Inserters is **2.0.3** in the Factorio 2.0 Mod Portal; source repository `bobinserters/info.json` lists a 2.0.4 build that is not available as a matching Portal release. We pin the published 2.0.3 ZIP and verify it by Portal SHA-1.

## Verified Bob's Warfare versus fork tank progression

Source comparison: `bobwarfare/prototypes/technology/tank.lua`, `bobwarfare/prototypes/recipe/tank.lua`, and the fork's `prototypes/technology/technology.lua` and `prototypes/recipe/vehicles.lua`.

- Bob's **Tank Mk2** requires `tank`, `artillery`, `processing-unit`, and `production-science-pack` technology; its recipe consumes a vanilla tank, steel, gears and processing units.
- Bob's **Tank Mk3** requires `bob-tanks-2` and `military-4` technology and includes **utility science**; its recipe consumes a Bob Mk2 hull.
- The fork's `super-tank-research` currently requires `modular-tank-research2`, `military-3`, `encabulated-waste-recovery` and authorization; its `super-tank` and alternate recipes use vanilla tanks and fork-specific components.

**Compatibility decision:** **do not unconditionally replace a vanilla tank ingredient with `bob-tank-2` or `bob-tank-3`**; that would dramatically move a currently reachable fork tech into a later Bob science tier and undermine base-only support. Any Bob-hull metallurgy integration must instead be a *deliberately unlocked alternate advanced recipe*, with manufacturing and tech-gate closure tested before adoption. Likewise, do not automatically make unrelated Bob ammunition fit this fork's guns merely because both are tank weapons.

## Acceptance evidence required

A combined-mod CI artifact should contain engine version, exact Bob module IDs/versions/sha256, startup settings, mod-list, machine-category coverage, tank/equipment mapping, technology-graph discrepancies, recipe progression diagnostics, save-create log, 1200-tick simulation result, and dedicated-server-start result. Only game load/run failures and required multiplayer/updater failures block releases; balance/rendering/tech-audit observations remain separately identified unless they cause a required game failure or the user explicitly elevates one to a gate.

**Sources:** https://github.com/modded-factorio/bobsmods/tree/main/bobassembly ; https://github.com/modded-factorio/bobsmods/tree/main/bobvehicleequipment ; https://mods.factorio.com/mod/bobwarfare/changelog
