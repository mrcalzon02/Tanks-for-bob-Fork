# Progression order audit — 8 November 2026

**Follow-up:** The user's subsequent decisions are implemented in
[1.8.102](PROGRESSION_DECISIONS_1.8.102.md). This document preserves the original
classification checkpoint and 1.8.101 evidence. The separate
[unused-equipment and asset inventory](UNUSED_EQUIPMENT_AND_ASSETS_2026-11-08.md)
records usability findings without activating or deleting historical content.

## Baseline and decision checkpoint

This classification was written **before gameplay reorganization**. The audited
commit is `6edc2dd7a04e632fb198f0a2f8aafa70644ef315` on `main`. The actual
published package is **1.8.100 for Factorio 2.1**, not the 1.8.95 / 2.0 package
still advertised by the old README and generic test runner.

The published ZIP was matched to the Mod Portal SHA-1
`f408c2ab1a4e7f17c62674b64a4f652a5f65ae0a`; its SHA-256 is
`c70c4ea68328032d8c72b926735b71d58ab49222bf0ed28fb74850169cfb6a39`.
Its progression source matches `tanks_for_bob_fork_1.8.95/`; the subsequent
release scripts add accepted structure artwork and Lumberyard display text.
The exact 1.8.100 package loaded, created a save, and simulated 300 updates
under **Factorio 2.1.23, build 87750** with all official modules enabled.
That proves startup, not playable progression.

Scope: **210 custom recipes, 88 custom technologies, 14 ammunition prototypes,
11 gun prototypes, 14 specialized crafting machines, and 2 custom labs**.
There are 39 initially enabled recipes and 12 explicit authorization nodes
without effects. The live full-expansion registry contains 1,040 recipes and
365 technologies, including official and generated recycling content.

The inventory appendix records every custom recipe and technology. Dormant
legacy recipe/turret files are excluded because `data.lua` does not load them.
The separate Bob compatibility branch is not merged or changed by this audit.

[Complete 210-recipe / 88-technology inventory](PROGRESSION_ORDER_INVENTORY_2026-11-08.md)
· [Machine-readable baseline](PROGRESSION_ORDER_BASELINE_2026-11-08.json)
· [Corrected live-registry map](PROGRESSION_ORDER_AFTER_2026-11-08.json)

## Intended progression

1. Gather wood, stone and fish by hand, including the deliberately slow
   zero-input SeaBlock fallback recipes. Make basic tools and a wooden weapon.
2. Build a campfire, workbench and Thinking Hut. Cook fish to support early
   research. Wood acquisition provides the foundational wooden-ammunition
   discovery requested by the user.
3. Develop the water, timber and clay/kiln branches. Brick enables the
   water-wheel/solar-boiler path and the Cooking Fire. Tools and meals lead to
   the hovel/quarry branch. These branches join at the Steam Compressor.
4. Produce paper, ink, requisitions, work orders and progressively more
   demanding paperwork. Develop mineral, biological and brine processing.
5. Combine these materials into encabulation components and authorizations.
   Ordinary Factorio metallurgy, electronics and chemical production run
   alongside the custom chain.
6. Introduce military platforms with usable standard ammunition, then specialist
   vehicles, upgraded munitions and WMD systems. Industrial ingredients can
   legitimately precede the weapons that eventually consume them.

## A. Immediate obvious fixes

| ID | Confirmed problem | Selected remedy | Preserved behavior |
| --- | --- | --- | --- |
| A1 | `Sharp-stick` ammunition starts enabled; `wood-spear` is disabled, requires the workbench category, and needs `growing-plot` plus fish research. | Start with the wooden weapon handcraft recipe. Move the existing `wood-spear` technology to the root, give it a wood-acquisition trigger, and use it to unlock wooden ammunition. Both tree harvesting and crafted driftwood must count. | Stable prototype IDs, wood costs, damage and ammunition consumption. No general conversion of technologies to harvesting tasks. |
| A2 | `bioceramic-grit` has two different item ingredients and two possible item products but uses ordinary `smelting`. Vanilla furnaces have one input and one output slot. | Use the existing two-ingredient `pit-kiln` category. The kiln is already available before this research. | Research cost/prerequisites, heat processing, ingredients, yields and waste. |
| A3 | `saline-particulate` also uses `smelting` while producing saline plus possible industrial waste into a one-slot furnace output. | Use `pit-kiln`, which can hold the separate products. Record the observed baseline engine symptom before reporting the repair as verified. | All materials, probabilities and research staging. |
| A4 | The ammunition manifest scans only `prototypes/item/ammo.lua`; wooden ammunition is declared in `prototypes/item/item.lua`. The vehicle-only audit therefore misses the user's example. | Include both active ammunition declaration files and test the wooden weapon's actual starting/material-unlock behavior. Add actual production checks for the two kiln recipes. | One manually dispatched CI job; no new workflow fan-out or release gate based on aesthetics. |
| A5 | The generic source selector, README and test runner point at 1.8.95 / Factorio 2.0, while distribution is a composed 1.8.100 / 2.1 ZIP. | Promote the verified package, including its accepted artwork, to the next directly versioned 2.1 source; test and package that same source. | Old releases and historical source remain intact. No retagging or implicit portal publication. |

Source evidence: `prototypes/recipe/recipe.lua` (`Sharp-stick`, `wood-spear`,
`saline-particulate`, `bioceramic-grit`),
`prototypes/technology/technology.lua` (`wood-spear`),
`prototypes/item/item.lua` (wood ammunition/gun),
`prototypes/entity/entities.lua` (`pit-kiln`), and `ci/stage_profile.py`.

## B. Human judgment required — preserve pending decisions

These findings are mapped before changes. A confirmed mismatch does not always
have one harmless remedy: adding a prerequisite can also delay unrelated
recipes sharing the technology. Those design choices are not silently applied.

| ID | Finding | Consequence and decision |
| --- | --- | --- |
| B1 | `new-munitions` can unlock `minepack-poison` before a mine-launching platform. | Adding `modular-tank-research3` as a prerequisite fixes the ordering but also delays poison mortar, which already has a working platform. Alternative: separate the poison-mine upgrade into its own research. Choose the intended branch structure. |
| B2 | `super-tank-alternate` can be researched before either mine magazine recipe. | Its flamethrower works, but its mine gun may not. Require specialist vehicle research, or unlock standard mine magazines alongside this tank; the latter preserves independent vehicle branches. |
| B3 | WMD artillery ammunition is unlocked by WMD tank research without requiring artillery. | Prefer separate WMD artillery conversion research requiring both WMD development and artillery. Requiring artillery for the entire WMD tank node would also delay the tank and couple it to Space Age's artillery progression. |
| B4 | `stone-tools` research unlocks the already available basic stone-tools recipe. | Keep starting tools: early infrastructure needs them. Decide whether this later node should be a demonstration milestone, grant improved tooling, or be removed with downstream prerequisites rewired. Disabling the starter recipe is not a repair. |
| B5 | Cooking Fire consumes a campfire but supports only `advcooking`, losing `cooking`. | A player must retain or rebuild a campfire for Seared Fish and fish-oil residue. Decide whether the upgraded fire should inherit both categories or remain specialized. This is not a hard lock. |
| B6 | Several custom unlocks rely on parallel vanilla manufacturing not guaranteed by their explicit custom prerequisites. | Examples include blue circuits/electric engines for the WLSK chassis, plastic and blue circuits for advanced substrates, and electric engines for later tanks. Decide whether research may preview these recipes or whether named vanilla manufacturing technologies should become explicit prerequisites. Do not collapse the survival tree into vanilla science without that decision. |
| B7 | A literal resource-free island has a conditional oil/coal bootstrap loop. | The fork's `tank-ammo-industrial-coke` can create coal/oil, but its Hyper-Encabulation gate already requires advanced substrates, which require plastic and blue circuits. With no natural oil/coal or another mod's supply, this cannot bootstrap the same ingredients. Choose a primitive oil/coal route, earlier low-yield processing, or a stated map-resource requirement. This differs from an ordinary Nauvis start. |
| B8 | The generic `modular-tank` item/entity has no active manufacturing recipe; `tank-artillery` is an unused gun. | Determine whether they are retained compatibility/development prototypes or intended player equipment. Do not invent recipes or activate dormant assets as an ordering fix. |

`steam-meal` is initially enabled but requires Cooking Fire and steam. It is an
industrial alternative to conventional meal production, not automatically an
error. If exclusive meal research gating is intended, that is a separate
design decision rather than justification for removing the alternative now.

## C. No ordering error found in the inspected relationships

| Relationship | Assessment |
| --- | --- |
| Hand gathering → basic tools/campfire/workbench/Thinking Hut → cooked-fish research | Starter inputs and machines are available. Keep zero-input fallback recipes. |
| Research references and custom prerequisite graph | All custom recipes/technologies are registered, all disabled custom recipes have unlocks, and no custom prerequisite cycle was found. |
| Custom research-material ancestry | No research input requires a custom recipe exclusively outside that technology's ancestor set. This item-ancestry result does not excuse machine failures or prove a full playthrough. |
| Lab support | Both custom burner labs accept all 14 custom research materials. Ordinary science research uses ordinary labs. |
| Specialized machine capacities and fluids | Prior workbench three-item capacity, Cooking Fire steam input and ammunition-assembler fluid input/output repairs are present. The two furnace recipes are the identified category/capacity exceptions. |
| Enabled machine operations | Clay, quarry, fishery, timber, condenser and waste recipes remain gated by constructing their machines. A recipe being enabled does not mean its products are available at the start. |
| Dedicated tank/ammunition assembler construction | General assembler 1/2/3 receive the custom categories in `data-updates.lua`; assembler 2 provides fluid handling. Their specialized replacements do not require themselves to bootstrap. |
| First modular tanks and normal ammunition | Platforms and their standard flame/autocannon/mortar/cannon ammunition unlock together. |
| Specialist mine/rocket tanks | Basic mine/rocket magazines and their respective platforms unlock together. |
| Bullet and shotgun ammunition bricks | Existing native weapons accept their native ammunition categories. No additional custom gun is needed. |
| WLSK upgrades | Their recipes consume earlier vehicles and retain the established ammunition families. |
| WMD tank ammunition | The WMD tank and its own ammunition unlock together. WMD artillery ammunition is the separate B3 decision. |
| Casings, explosives, authorizations and damage upgrades | Components can serve industrial uses before weapons; authorization-only nodes and useful damage upgrades are not missing-recipe defects. |

## Complete ammunition map

| Ammunition | Category | First usable consumer | Classification |
| --- | --- | --- | --- |
| `Sharp-stick` | `wood` | `wood-spear` | A1 |
| `flame-thrower-ammo-tanker` | `tank-spray-ammo` | Flame tank / flame car | No error |
| `flame-thrower-ammo-tanker-2` | `tank-spray-ammo-2` | Flame tank | No error |
| `45mm-auto` | `auto-cannon-ammo` | Autocannon tank | No error |
| `50mm-mortar` | `tank-nade-ammo` | Grenade/mortar tank | No error |
| `cannon-shell-2` | `cannon-shell` | Native/custom cannon tank | No error |
| `minepack` | `tank-mine-ammo` | Mine tank | No error |
| `rocketpack` | `tank-rocket-ammo` | Rocket tank | No error |
| `50mm-mortar-poison` | `tank-nade-ammo` | Earlier grenade/mortar tank | No error |
| `minepack-poison` | `tank-mine-ammo` | Mine tank / alternative super-tank | B1 |
| `piercing-shotgun-shell-brick` | `shotgun-shell` | Native handheld/mounted shotgun | No error |
| `ap-bullet-brick` | `bullet` | Native handheld/mounted bullet gun | No error |
| `tank-wmd-ammo` | `tank-wmd-ammo` | WMD super-tank | No error |
| `wmdartillery-ammo` | `artillery-shell` | Native artillery platform | B3 |

## Verification limits

Prototype loading, a 300-tick benchmark, and the older optimistic 210/210
ingredient closure do not establish a full factory/research playthrough.
The repair must be checked with fresh unresearched force state, tree and
driftwood wood-acquisition paths, upgrade/reload behavior, and powered kiln
production. Seeded ingredient fixtures prove those operations, not the time,
terrain, balance or logistics of reaching every endgame recipe.

Official references: [technology triggers](https://lua-api.factorio.com/latest/types/TechnologyTrigger.html),
[scripted material triggers](https://lua-api.factorio.com/latest/types/ScriptedTechnologyTrigger.html),
[furnace recipe selection](https://lua-api.factorio.com/latest/auxiliary/furnace-recipe-selection.html),
[furnace input/output capacity](https://lua-api.factorio.com/latest/prototypes/FurnacePrototype.html).
Baseline distribution evidence: [1.8.100 build](https://github.com/mrcalzon02/Tanks-for-bob-Fork/actions/runs/42430309774),
[Mod Portal metadata](https://mods.factorio.com/api/mods/tanks_for_bob_fork/full).

## Repair and verification results

The A-class repairs are implemented in **`tanks_for_bob_fork_1.8.101`**, a
directly buildable Factorio 2.1 source promoted from the verified 1.8.100 ZIP.
All **516 existing artwork/sound files** remain byte-identical; no prior file
was removed. All B-class design decisions remain unchanged. The two kiln
recipes retain their ingredient amounts, yields, waste probabilities and
technology unlocks. The wooden weapon and ammunition retain their costs and
combat properties. The wooden technology's changed semantics are reflected in
all 14 existing base locales and the English Mechanicus overlay.

### Observed before/after production

The controlled base-only test used Factorio 2.1.23 and 12,000 simulation ticks.
It seeded target materials, fuel, electricity and recipe enablement. It proves
machine feasibility, not acquisition of those prerequisites.

| Operation | Published 1.8.100 | Category-only corrected candidate |
| --- | --- | --- |
| Each ordinary furnace: saline particulate | Inputs rejected; no selected recipe; zero output | Recipe assigned to kiln instead |
| Each ordinary furnace: bioceramic grit | Inputs rejected; no selected recipe; zero output | Recipe assigned to kiln instead |
| Pit Kiln: saline particulate | No selectable recipe; zero output | 27 saline particulate |
| Pit Kiln: bioceramic grit | No selectable recipe; zero output | 7 grit + 1 industrial waste |
| Stone / steel / electric furnace iron controls | 62 / 124 / 124 plates | 62 / 124 / 124 plates |
| Pit Kiln brick control | 2 bricks | 2 bricks |

Saline's waste output is probabilistic and did not appear in this short
fixture; bioceramic waste production was directly observed. The final,
unmodified **1.8.101 ZIP** separately passed native kiln production checks.
[Baseline comparison evidence](evidence/2026-11-08/machine-baseline-comparison.json).

### Exact-package native tests

The installable package SHA-256 is
`3ef42495a542b7a3f925aa640484d88d7e206ea0d5763061cd3bed48e7ebb3d8`.
The package was tested under **Factorio 2.1.24, build 87808**, with all official
modules enabled and a separate diagnostic addon. All **33 fresh-player and
machine checks passed**:

- A fresh force starts with the spear recipe enabled and ammunition locked.
- A real player mines a real tree, receives wood and discovers ammunition.
- The player actually handcrafts the starting wooden weapon.
- A separate unresearched force handcrafts the original 90-second driftwood
  recipe. The resulting native crafted-item event completes discovery before
  the wood reaches the player's inventory.
- Rare-quality wood in the real player inventory also completes discovery.
- Both corrected recipes are selected and manufacture products in real kilns.

The **single-profile integrated suite also passed**: actual 2.1 source staging
with unchanged metadata, source/assets, data-stage checks, map creation,
1,200-tick smoke simulation, native progression and private server startup.
It registered all 14 ammunition types, passed 11 machine regressions, spawned
8 vehicles, observed physical damage, and inserted ammunition in 7 surviving
test vehicles. These are not claims of firing every weapon or of two-client
multiplayer. The suite was executed locally; no remote workflow was dispatched.

The actual final data dump contains 210 declared custom recipes and 88 custom
technologies, with zero missing recipe/technology references, zero disabled
custom recipes without unlocks, zero prerequisite cycles, and zero custom
recipes without a compatible crafter. `stone-tools` remains the explicitly
deferred redundant unlock B4. Fourteen focused mocked Lua tests separately
cover event payloads, force isolation, migration logic and unrelated state
preservation; those mocks are not substituted for the native checks above.

[Native exact-package evidence](evidence/2026-11-08/native-progression-fresh.json)
· [Integrated suite evidence](evidence/2026-11-08/suite-results.json)
· [Source/artwork preservation](evidence/2026-11-08/source-preservation.json).

### Historical-save migration

The optional historical-save fixture also passed against that exact final ZIP:
**7 legacy-state setup checks and 15 migration checks**, in addition to a new
passing run of all 33 fresh checks. It used the verified published 1.8.100
package to serialize a normal scenario save, then loaded that save with
1.8.101 under Factorio 2.1.24. The engine reported the real version change.

- Every tested old force receives the default wooden weapon recipe.
- Completed wooden research keeps its ammunition unlock. Unrelated completed
  Automation research survives the upgrade.
- Empty, unresearched forces keep ammunition locked.
- A force with the old fish-funded research 40% complete changes to the new
  material discovery without falsely completing it; the obsolete lab research
  leaves its queue. Wood acquisition now completes that discovery.
- Three wood were serialized in a real character inventory, survived loading,
  and completed discovery when the native test player joined that character.

This normal headless converter creates no offline player. The saved-character
join path is therefore demonstrated natively; discovery for an already
existing offline player during `on_configuration_changed` is covered by the
focused Lua unit tests, not claimed as native saved-player evidence. The
engine reapplies recipe effects before configuration handlers, so arbitrary
unrelated recipe-enabled overrides are not promised to survive prototype
migration. The production handler itself only synchronizes the two wooden
recipes and does not reset unrelated research or recipes.

The final run also observed both kiln byproducts: 27 saline particulate and
2 industrial waste, and 7 bioceramic grit and 2 industrial waste. These seeded
machine results remain separate from the unresolved resource-free island
bootstrap decision B7.

[Native historical-save evidence](evidence/2026-11-08/native-progression-migration.json).
