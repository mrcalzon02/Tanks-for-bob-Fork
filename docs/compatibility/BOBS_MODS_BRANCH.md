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
- [ ] **Phase 2:** produce one version-locked, licensed, reproducible Factorio 2.0 combined mod directory: `base`, `elevated-rails`, `quality`, `space-age`, `tanks_for_bob_fork`, and full Bob family. Keep mod credentials in Actions secrets; never log them or commit them.
- [ ] **Phase 3:** complete the actual data-stage inventory: duplicate prototypes; every fork recipe's ingredient/result and recipe category; machines including Bob assembler 4/5/6; Bob equipment grids/categories; lab science acceptance; tech prerequisites/unlocks; resource reachability and pollution/waste/recycling outputs. Record exact failures, not guesses.
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

`ci/stage_profile.py` selects the highest versioned source folder (currently 1.8.95). The old staging logic **overwrote** `data-final-fixes.lua` with the audit, which would silently bypass any compatibility adapter. Branch commit `d5612ac` stages `ci_data_audit.lua` and *appends* its require to the existing `data-final-fixes.lua` instead. This change must pass the regular one-profile Factorio smoke before treating the baseline as preserved. The current CI profile still enables **only official mods**, never Bob's mods; it cannot validate Bob integration until the version-locked combined mod directory is implemented.

## Acceptance evidence required

A combined-mod CI artifact should contain engine version, exact Bob module IDs/versions/sha256, startup settings, mod-list, machine-category coverage, tank/equipment mapping, technology-graph discrepancies, recipe progression diagnostics, save-create log, 1200-tick simulation result, and dedicated-server-start result. Only game load/run failures and required multiplayer/updater failures block releases; balance/rendering/tech-audit observations remain separately identified unless they cause a required game failure or the user explicitly elevates one to a gate.

**Sources:** https://github.com/modded-factorio/bobsmods/tree/main/bobassembly ; https://github.com/modded-factorio/bobsmods/tree/main/bobvehicleequipment ; https://mods.factorio.com/mod/bobwarfare/changelog
