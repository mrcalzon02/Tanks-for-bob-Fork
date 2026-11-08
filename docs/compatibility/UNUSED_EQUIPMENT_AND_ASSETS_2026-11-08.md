# Unused equipment and asset reuse inventory — 2026-11-08

## Result and scope

**There are useful spare assets, but none of the three genuinely orphaned player-equipment definitions is a complete new feature ready to enable.** The generic `modular-tank` needs a recipe and a distinct role; `tank-artillery` duplicates an existing mounted gun; and `tank-recall-token` belongs to a disabled runtime feature. A dormant turret is a separate incomplete implementation. The strongest low-scope reuse candidates are alternative resolutions of accepted artwork, staged charcoal/casing/ash icons, and two alternative sound files.

This is a separate inventory from the progression repair audit. It changes no production prototype, recipe, technology, image, sound, or event handler. Nothing was activated or deleted, and no new engine test, render, or audio audition was performed for this inventory.

The committed baseline is `cf4a7dbe6730e73e6dcc02f3ea5fe75c47149780`, containing source **1.8.101**. Registered-prototype evidence comes from the existing **Factorio 2.1.24** dump with the official expansion mods enabled. The concurrent **1.8.102** source was also inspected for reachable references. All **514** PNG/OGG media files in that source match the 1.8.101 media bytes; its new fish recipes add no local artwork references. Engine observations in this document therefore remain explicitly attributed to 1.8.101 rather than being presented as a new 1.8.102 execution.

The complete machine-readable companion is [UNUSED_EQUIPMENT_AND_ASSETS_2026-11-08.json](UNUSED_EQUIPMENT_AND_ASSETS_2026-11-08.json). It includes **every one of the 295 unreferenced media filenames**, dimensions, byte size, SHA-256, classification, reuse assessment, and exact duplicate relationships. It also lists the 219 protected media files, five orphan prototype records, dormant Lua paths, 51 model/source files, and four staged third-party images.

| Classification | Meaning in this inventory |
| --- | --- |
| **Ready candidate** | An identifiable, technically available candidate exists. Visual/audio suitability and its eventual integration still need review; this is not approval to ship. |
| **Needs integration** | Useful pieces exist, but gameplay, prototype, recipe, consumer, animation, or layer wiring is missing. |
| **Historical or superseded** | Duplicate, replaced, deliberately disconnected, older iteration, authoring source, or backup. Preserve until a separate decision. |
| **Uncertain** | The intended target or suitability is not sufficiently established for a stronger recommendation. |

## 1. Loaded equipment that is not normally obtainable

“No producer” below excludes Quality's generated recycling-only recipes. A recycling recipe that requires an existing copy does not establish an acquisition path. The family technologies named `modular-tank-research*` do not themselves prove that the generic `modular-tank` item is unlocked. The active vehicle, weapon, capsule, recipe and technology definitions were checked separately. [Sources: loaded definitions and entry point](#sources-and-evidence).

| Candidate | What is already present | Missing connection or conflict | Classification and reuse decision |
| --- | --- | --- | --- |
| **`modular-tank`** | Registered item and placeable car; 1,200 health; 4 inventory slots; `tank-auto-cannon` and `tank-cannon-2`; existing ammunition; inherited vanilla `medium-equipment-grid`, 6×8 with the `armor` equipment category. | No non-recycling producer, recipe unlock, or component consumer. It shares its icon and gun pair with the obtainable `auto-tank`, which has 3,000 health and 9 inventory slots. | **Needs integration.** Plausible base for an earlier dual-gun platform, if that role is wanted. Decide purpose, costs and research position before adding a recipe. A distinct icon is optional design work. Preserve the existing prototype ID for compatibility. |
| **`tank-artillery`** | Registered gun with `tank-nade-ammo`, range 45 and cooldown 50; existing `50mm-mortar` and `50mm-mortar-poison` ammunition. | No item recipe and no vehicle mount. In the actual loaded dump, **every field except `name` equals `tank-nade-cannon`**. It is a projectile gun, not an artillery turret/wagon or an artillery targeting system. | **Historical or superseded.** Treat as a duplicate/possible legacy alias. Reuse the already-mounted mortar gun unless a distinct weapon is intentionally designed. Giving this duplicate a recipe would not create a new artillery capability. |
| **`tank-recall-token`** | Registered capsule and `pre-teleport-effect`/`teleport-effect` definitions; the shared teleport sheet is still referenced. | No recipe; no `tank-recall` technology; driving, GUI and trigger-created-entity hooks are commented out. Dormant functions reference the absent technology, old `global` state and passenger handling; the actual `player.teleport(...)` call is commented out. | **Historical or superseded.** Restoration would require a modern runtime feature, state/save/player handling, acquisition and gameplay decisions. Keep it dormant. The capsule and image existing does not establish working recall. |

The two required equipment files, `prototypes/item/equipment.lua` and `prototypes/equipment/equipment.lua`, are **empty**. They contain no spare shield, reactor, battery, or vehicle equipment definitions. This does not mean the vehicles lack equipment support: their cloned vanilla tank provides the grid described above.

### Loaded auxiliary definitions without an active consumer

| Definition | Evidence | Classification and recommendation |
| --- | --- | --- |
| **`massive-scorchmark`** (`corpse`) | No active incoming use was found. Both relevant nuclear projectile blocks explicitly avoid creating it: their comments explain that extra corpse scorchmarks caused hard square visual blocks, while nuclear tiles/decoratives already handle the crater. | **Historical or superseded.** Preserve the ID; reconnecting it would risk restoring a known visual defect. It uses base-game sprites, so it is not a missing local graphic. |
| **`lazer-cloud`** (`trivial-smoke`) | No active incoming use was found. The projectile file contains it as a commented alternative beside the active poison-cloud effect. Its definition includes old laser-damage data. | **Historical or superseded.** This is an old effect sketch, not a proven spare cloud weapon. Review the current prototype's behavior and choose a consumer before considering reuse. |

`teleport-effect` is also unconsumed by an active handler, but is grouped with the recall feature rather than counted as another player-equipment candidate.

## 2. Dormant code and implementation fragments

The reachability check starts at the package's `data.lua`, `data-updates.lua`, `settings.lua` and `control.lua` and follows local literal `require` calls. Optional official compatibility branches are included conservatively. Migration files are excluded from this dormant-code classification because Factorio loads them by convention.

| Files or feature | Assessment | Classification and decision |
| --- | --- | --- |
| `prototypes/item/turret.lua`; `prototypes/entity/turrets.lua`; `prototypes/recipe/turret.lua` | None is loaded. Their `auto-cannon-turret` item, recipe and entity are absent from the actual dump. The sketch has 400 health, range 45, cooldown 6 and a 40-second recipe using 20 steel plates and 20 electronic circuits. It has no technology unlock. | **Needs integration.** Keep these files dormant until a dedicated turret design and port are undertaken. |
| Root **`recipe.lua`** | A 4,013-line duplicate, not the active `prototypes/recipe/recipe.lua`. Its 184 recipe IDs overlap existing recipes; it is not 184 unused recipes. It retains the old weapon/ammunition ordering and old smelting assignment for the two kiln recipes. | **Historical or superseded.** Do not require it: it would redefine existing IDs and could undo repairs. |
| Empty equipment files noted above | Loaded stubs, zero definitions. | **Historical or superseded** scaffolding. There is no hidden equipment system to switch on. |

The dormant turret has several concrete porting problems:

- Its attack type is `projectile`, but `tank-spray-ammo` is the existing **flamethrower stream** ammunition family. The current `tank-flamer` and tanker ammunition use stream delivery. Decide whether this is intended to be a ballistic turret or a flame turret before choosing ammunition.
- `projectile_creation_distance = 3,5` assigns `3` and adds a stray positional `5` to the Lua table. It does not express decimal `3.5`.
- `make_heavy_gunshot_sounds()` is not defined in the current mod or the inspected 2.1.24 base/core sources. Some turret animation helpers do exist in base, so the whole helper set should not be described as missing.
- Its recipe uses older untyped ingredient tuples and a singular `result`; sprite dimensions and legacy base paths also need a current schema review.
- Its code references **base-game turret graphics**, not the 39 local turret sheets listed below. Those spare sheets are a separate integration choice.

These are source-level findings. The dormant files were not enabled to manufacture a failure or represented as having passed engine execution.

## 3. Packaged media with no active reference

| Media status | Files | Meaning |
| --- | ---: | --- |
| Referenced by registered prototypes | **218** | Protected, including dynamically assembled paths, shared sheets and references from dormant gameplay features such as the recall capsule. |
| Referenced only by newly reachable source literals | **0** | The current-source pass added no further media to the protected set. |
| Package metadata | **1** | `thumbnail.png`; not an unused gameplay sprite. |
| No active reference found | **295** | **261 entity PNGs, 32 icon PNGs and 2 OGGs**, totaling **23,390,884 bytes** before archive compression. |

The 295 candidates divide into **14 ready candidates, 254 needing integration, 19 historical/superseded files and 8 uncertain files**. These are individual file counts, not counts of new weapons or machines. The three packaged `.xcf` authoring files are counted separately below.

### Reuse groups covering all 295 files

The companion JSON expands every group into exact filenames and records the more specific classification of duplicate or backup members.

| Group | Files | Reuse assessment |
| --- | ---: | --- |
| Accepted machine art at alternate resolutions | **12** | **Ready candidate.** Campfire V12 and clay-pit V4c each have unused 64-pixel-frame idle/working atlases; pit-kiln V6 has unused 64/256 variants; lumberyard V2b has unused 64/128 variants. They are alternatives for the same accepted machines. Match frame sizes, direction offsets and scale before any reference change. |
| Superseded original machine sheets and icons | **12** | **Historical or superseded.** Original campfire, clay-pit, pit-kiln and growing-plot art. The lumberyard appearance is already installed on the existing `growing-plot` prototype. Original rollback art was intentionally retained by the production builders. |
| Local tank sheets | **32** | **Needs integration** for 30 alternative layers; one named backup and one exact duplicate are **historical**. Current vehicles inherit vanilla hull/shadow layers and use four selected custom turret/mask sheets. No tank is missing its body merely because local alternatives are unused. |
| Local `gun-turret` sheets | **39** | **Needs integration.** Animation, mask, shadow and remnant pieces have no active local consumer. The dormant turret's base-game graphics are separate. |
| Wooden offshore-pump sheets | **53** | **Needs integration.** Directional body, fluid/glass, legs, underwater, shadow, reflection and remnant assets are available. The current beachpump uses cloned base offshore-pump art. A wooden-pump visual replacement needs current layer mapping and visual review. |
| Local pipes/covers and wood-pipe icons | **67** | **Needs integration.** 49 pipe sheets, 16 cover sheets and 2 icons. Current machines use base pipe-cover helpers; no loaded wood-pipe/wood-pipe-to-ground item and entity chain was found. |
| Iron-wall sheets and companion icons | **30** | **Needs integration.** 28 entity sheets and 2 icons. No loaded iron-wall item/entity/recipe/technology exists. A full wall feature would need mechanics and progression, not just a sprite path. |
| Optional machine layers/remnants | **14** | **Needs integration** for 12 files; 2 duplicate thinking-hut remnants under pondering-hovel are **historical**. Includes workbench shadows/remnants, hovel integration/remnants, hut remnants and basin remnants. The machines themselves are already active and currently use existing/base corpse definitions. |
| Alternative projectile/explosion effects | **8** | **Needs integration.** Six explosion sheets, one bullet-artillery sheet and one toxic-thrower sheet. A filename alone does not provide a complete new ammunition type or a correctly timed effect. |
| Unassigned assembler sheet | **1** | **Uncertain.** `graphics/entity/assembling-machine/assembling-machine.png` has no identified current destination. Establish intended appearance and provenance before choosing a machine. |
| Duplicate placeholder aliases | **3** | **Historical or superseded.** `graphics/entity/new/placeholder.png`, `graphics/icons/aqueduct1.png` and `graphics/icons/stone-basin.png` are byte-identical to the active stone-water-wheel icon. They are not three distinct completed structure designs. |
| Unimplemented vehicle-component icons | **13** | **Needs integration.** Turret, chassis and super-tank subsystem pictures do not establish corresponding active standalone components. Any component system needs item IDs, recipes, consumers and progression. |
| Alternative vehicle icons | **2** | **Needs integration.** `auto-tank-lvl3.png` and `auto-tank-wlsk.png`; the latter is 65×64 pixels and requires explicit sizing review. |
| Unassigned concept icons | **5** | **Uncertain.** Industrial waste, rubberized timber, industrial coke, corporate compliance and shell-conversion filenames suggest uses, but exact targets and visual fit need selection. `corporate-compliance` currently names a subgroup, not an icon-bearing equipment item. |
| Spare placeholder icons | **2** | **Uncertain.** `Placeholder128.png` and `Placeholder32.png`; preserve as generic source material rather than counting them as finished content. |
| Alternative artillery audio | **2** | **Ready candidate.** `heavy-artillery.ogg` and `heavy-artillery-2.ogg`; the active shared gun sound is `heavy-artillery-3.ogg`. Listening, volume and mixing review remain necessary. |

### Exact icon appendix

All paths below are relative to `tanks_for_bob_fork_1.8.102/graphics/icons/`. These are the **32** icon PNGs with no active reference; the JSON supplies dimensions and hashes.

| Purpose group | Exact filenames |
| --- | --- |
| Superseded machine icons | `campfire.png`, `clay-pit.png`, `growing-plot.png`, `pit-kiln.png` |
| Duplicate aliases | `aqueduct1.png`, `stone-basin.png` |
| Wall and pipe proposals | `iron-wall.png`, `iron-wall-research.png`, `wood-pipes.png`, `wood-pipe-to-ground.png` |
| Alternative vehicles | `auto-tank-lvl3.png`, `auto-tank-wlsk.png` |
| Vehicle turret/chassis components | `tank-auto-turret.png`, `tank-flame-turret.png`, `tank-light-chasis.png`, `tank-mine-turret.png`, `tank-nade-turret.png`, `tank-poison-turret.png`, `tank-rocket-turret.png` |
| Super-tank components | `tank-super-armour-system.png`, `tank-super-chasis.png`, `tank-super-drive-system.png`, `tank-super-loading-system.png`, `tank-super-turret.png`, `tank-super-ventilation-system.png` |
| Unassigned concepts | `Industrialwaste2.png`, `Rubberized timber.png`, `corporate-compliance.png`, `industrial-coke.png`, `tank-ammo-shellconvert.png` |
| Placeholders | `Placeholder128.png`, `Placeholder32.png` |

### Exact duplicate evidence

SHA-256 equality confirms these relationships; similarity was not inferred from names or thumbnails:

- Unused `graphics/entity/tank/hr-tank-turretb.png` equals **referenced** `graphics/entity/tank/hr-tank-turreta.png`.
- The three placeholder aliases listed above equal **referenced** `graphics/icons/stone-water-wheel.png`.
- The two `thinking-hut-remnants.png`/`hr-thinking-hut-remnants.png` sheets under `pondering-hovel/remnants/` equal the corresponding sheets under `thinking-hut/remnants/`. All four are presently unreferenced.

## 4. Source artwork and staged candidates outside the live media set

### Active production sources — protected

The Git tree contains **1,490 entries under `models/` and `art/`**, including 1,227 PNGs, 25 `.blend` files, 3 `.blend1` backups, 66 GIFs and 23 OBJ files. Many PNGs are individual animation frames, contact sheets or iteration exports. They are not 1,227 independent spare in-game assets. These directories are outside the installable source package and were catalogued through Git metadata and the existing production documents; sparse-excluded binaries were not opened or rendered.

The following four Blender masters are part of the current production history, not unused feature candidates:

| Live appearance | Current documented master |
| --- | --- |
| Campfire V12 | `models/island-survival/blender/production-v12-structure-45/master.blend` |
| Clay pit V4c | `models/island-survival/clay-pit/generated-v4c/clay-pit-v4c.blend` |
| Pit kiln V6 | `models/island-survival/pit-kiln/generated-v6/pit-kiln-v6-inward-pitch.blend`; production atlases in `production-v6/` |
| Lumberyard V2b, installed on `growing-plot` | `models/island-survival/lumberyard/generated-v2b/steam-lumberyard-v2b.blend` |

The campfire, clay-pit, kiln and lumberyard release builders and accepted-art documents establish this provenance. Older generated versions, camera experiments, `.blend1` backups and previous production atlases are **historical or superseded**. They can supply geometry or materials for deliberate future work, but they should not replace the accepted live art merely because they exist. [Production evidence](#sources-and-evidence).

### Blockout geometry library

The documented `models/island-survival/obj/` library contains **21 blockout/comparison meshes**, with a shared material file and generator. Its own README explicitly distinguishes these from final screen-accurate models and sprite replacements.

| Existing machine family | Blockout names |
| --- | --- |
| Water | `beachpump`, `wood-basin`, `stone-water-wheel`, `solar-boiler`, `primitive-steam-powered-pump`, `steam-condenser` |
| Wood/fire | `growing-plot`, `campfire`, `cooking-fire`, `workbench` |
| Clay/food | `clay-pit`, `fish-pond`, `pit-kiln` |
| Minerals | `quarry`, `calcifier`, `shaler` |
| Research | `thinking-hut`, `pondering-hovel` |
| Industry | `Steam-Compressor`, `tank-assembling-machine`, `tank-ammo-assembling-machine` |

Campfire, clay-pit, pit-kiln and growing-plot now have accepted detailed replacements. Those four old blockouts are **historical**; the remaining **17 need integration/modeling** before they can become replacement sprites. They are useful starting geometry for existing machines, not 17 additional gameplay machines. The two other OBJ files in the larger tree belong to older refined-campfire work.

### Four staged third-party images

The repository's [per-file provenance ledger](../../art/third-party/unused-renders/README.md) records these as unmodified Malcolm Riley / **Unused Renders** images under CC BY 4.0. They are outside the mod package, are not active replacements, and have not been visually approved in this audit. This records the repository's existing provenance; it is not a new upstream license investigation.

| Exact path under `art/third-party/unused-renders/item-mipped/` | Existing or possible destination | Assessment |
| --- | --- | --- |
| `pile-charcoal-2.png` | `charcoal`, which currently uses `Placeholder.png` | **Ready candidate** for a later native-resolution comparison; clearest existing placeholder replacement opportunity. |
| `part-bullet-casings-1.png` | `tank-ammo-casing` | **Ready candidate** for comparison with the current casing icon; the current item is already functional. |
| `pile-ashes-1.png` | Possible `fish-ash` icon in the concurrent 1.8.102 work | **Ready candidate** for visual review. A general ash render may be suitable, but the filename does not itself establish fish-ash identity or approval. |
| `pile-chunk-wood-chips-1.png` | Wood-processing reference | **Uncertain.** No exact standalone wood-chip item was identified for it in this audit. |

These are completed 2D item-render sheets, not seamless material textures or 3D source meshes. Any later use should retain the ledger's exact source credit, record the destination and modifications, and undergo the normal visual integration review.

### Editable source files currently inside the package

| Exact path | Bytes | Assessment |
| --- | ---: | --- |
| `graphics/entity/tank/hr-tank-turreta.xcf` | 1,004,853 | Editable GIMP source for tank art. |
| `graphics/entity/tank/tank-turretHR-1xcf.xcf` | 1,500,169 | Editable GIMP source/iteration. |
| `graphics/icons/tank-group.xcf` | 32,281 | Editable GIMP icon source. |

These total **2,537,303 bytes** and are **source/history**, not runtime sprites. A later packaging decision could separate authoring sources from an installable archive while preserving them in Git. This inventory makes no such change.

## 5. Deliberately protected: false positives to avoid

Nine guns have no standalone manufacturing recipe because vehicles mount them. They are used components, not abandoned equipment:

| Gun | Registered vehicle consumers |
| --- | --- |
| `tank-auto-cannon` | `modular-tank`, `auto-tank`, `auto-tank-wlsk` |
| `tank-cannon-2` | `modular-tank`, `auto-tank`, `auto-tank-wlsk`, `super-tank` |
| `tank-flamer` | `flame-tank`, `flame-tank-wlsk`, `car-flamer` |
| `tank-flamer-2` | `flame-tank`, `flame-tank-wlsk`, `super-tank-alternate` |
| `tank-machinegun-turret` | `nade-tank`, `nade-tank-wlsk`, `rocket-tank`, `super-tank`, `super-tank-wmd`, `car-flamer` |
| `tank-mine-cannon` | `mine-tank`, `super-tank-alternate` |
| `tank-nade-cannon` | `nade-tank`, `nade-tank-wlsk` |
| `tank-rocket-cannon` | `rocket-tank` |
| `tank-wmd-cannon` | `super-tank-wmd` |

The audit also protects:

- **Shared and generated sprite references.** The recursive final-dump scan sees references that a simple filename grep would miss. Active custom tank sheets include `tank-turreta.png`, `hr-tank-turreta.png`, `tank-turret-maske.png` and `hr-tank-turret-maske.png`.
- **Current machine art and its sources.** Workbench, research hut/hovel and basin body art is active even where optional shadows/remnants are spare. Accepted campfire/clay/kiln/lumberyard exports and production masters are retained.
- **Active projectile/effect chains.** Current custom projectiles have ammunition consumers. `explosionnukea` and `nuclearexplosiona.ogg` are deliberately consumed by WMD projectile effects. `poison-cloud-2` and the flame stream also have active consumers.
- **Registered recall art.** `graphics/entity/teleport/teleport-effect.png` is still prototype-referenced even though recall is not normally available. This is a gameplay-wiring issue, not an unreferenced-file finding.
- **Metadata and migrations.** The mod thumbnail is used by package presentation, and migration scripts are loaded without a Lua `require` edge.

## 6. Practical reuse order

1. **Review small, existing-purpose candidates first:** the staged charcoal icon, alternative casing/ash icons if wanted, accepted atlas resolution variants where there is a concrete size/performance need, and alternative artillery audio where there is a sound-design goal.
2. **Make a gameplay decision for `modular-tank` before implementation.** It has the strongest complete equipment foundation, but it currently overlaps an obtainable platform and has no progression role.
3. **Treat the turret, wooden pipes, iron wall and component-icon set as separate features.** Each needs a consumer/recipe/research design as well as technical integration. A collection of artwork is not evidence that these features were intended to be enabled in this release.
4. **Keep duplicate and deliberately disabled content in history.** The artillery alias, recall feature, scorchmark, stale root recipe file and superseded art are poor candidates for automatic activation. Preserve IDs and sources until compatibility and design decisions are made.

There is **no deletion list** in this report. “No active reference found” is bounded to the audited source and prototype evidence; it does not prove that old saves, external mods, scenarios, or future art work have no use for a path or prototype ID.

## Sources and evidence

| Evidence | What it supports |
| --- | --- |
| [1.8.102 entry point](../../tanks_for_bob_fork_1.8.102/data.lua), [runtime entry point](../../tanks_for_bob_fork_1.8.102/control.lua) | Loaded versus dormant files; disabled recall handlers; current literal references. |
| [Vehicle entities](../../tanks_for_bob_fork_1.8.102/prototypes/entity/vehicles.lua), [vehicle items](../../tanks_for_bob_fork_1.8.102/prototypes/item/vehicles.lua), [guns](../../tanks_for_bob_fork_1.8.102/prototypes/item/gun.lua), [capsules](../../tanks_for_bob_fork_1.8.102/prototypes/item/capsule.lua) | Registered equipment, mounted consumers and recall capsule. |
| [Vehicle recipes](../../tanks_for_bob_fork_1.8.102/prototypes/recipe/vehicles.lua), [main recipes](../../tanks_for_bob_fork_1.8.102/prototypes/recipe/recipe.lua), [technologies](../../tanks_for_bob_fork_1.8.102/prototypes/technology/technology.lua) | Acquisition/consumer gaps, family unlocks, current fish-ash context. |
| [Entity definitions](../../tanks_for_bob_fork_1.8.102/prototypes/entity/entities.lua), [projectiles](../../tanks_for_bob_fork_1.8.102/prototypes/entity/projectiles.lua), [dormant turret](../../tanks_for_bob_fork_1.8.102/prototypes/entity/turrets.lua) | Optional sprite layers, unused helpers, explicit scorchmark disconnection, turret porting issues. |
| [Campfire acceptance](../art/CAMPFIRE_ACCEPTED_21.md), [clay V4c](../art/CLAY_PIT_V4C_READABLE_SWING.md), [kiln V6](../art/PIT_KILN_V6_FINAL_MOTION.md), [lumberyard V2b](../art/LUMBERYARD_V2B_VISIBLE_POWER_TRANSMISSION.md) | Accepted current appearances, source iterations and live growing-plot/lumberyard identity. |
| [Campfire builder](../../tools/art/build_accepted_campfire_21.py), [clay builder](../../tools/art/build_clay_pit_21_release.py), [kiln builder](../../tools/art/build_pit_kiln_21_release.py), [lumberyard builder](../../tools/art/build_lumberyard_21_release.py) | Selected production exports, scale variants and intentional original-art preservation. |
| [Blockout library README](../../models/island-survival/README.md), [third-party ledger](../../art/third-party/unused-renders/README.md), [reuse and credit workflow](../art/UNUSED_RENDERS_WORKFLOW_AND_CREDITS.md) | Source-model limitations; four staged images and their recorded provenance. |
| [Companion inventory](UNUSED_EQUIPMENT_AND_ASSETS_2026-11-08.json) | Exact 295-file candidate list; protected media; dimensions; SHA-256 identities; individual decisions; model blob IDs. |

The reused engine dump is `/workspace/scratch/bcbf5d5b43f0/verification/runtime/script-output/data-raw-dump.json`, SHA-256 `71eea4a62e00f36f9c6e9d049629235a9abb74fa139b5d0d25c204af2095329b`. It is external verification evidence, not a new test result generated by this inventory. Sparse source-art classification relies on the committed Git tree and the cited documentation, not on opening every binary. Visual quality, animation alignment, audio mixing and compatibility with arbitrary third-party mod packs remain outside this read-only assessment.
