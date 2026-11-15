# Ongoing structure completion ledger

Updated 2026-11-15 against `7290824bf43711d0bb31bd8e2969c51459864f91`.

21 survival/manufacturing structures; excludes vehicles and Tech-Priests turrets.

Accepted historical art stays accepted. New/revised assets require independently reopened editable source, inspected exported artifact and true Blender renders, bounded repair, visual disposition and native runtime evidence. Missing receipts are pending, never automatic PASS.

**7 accepted/integrated; 4 advanced with open work; 10 requiring substantial production. Current focus: Primitive Steam-Powered Pump.**

| Structure | Latest known revision | Status | Remaining action |
| --- | --- | --- | --- |
| Campfire | V12 | accepted integrated | Preserve accepted source and installed animation. |
| Clay Pit | V4c | accepted integrated | Preserve readable swing and installed four-way animation. |
| Pit Kiln | V6 | accepted integrated | Preserve whole-tray motion and installed animation. |
| Lumberyard | V2b | accepted integrated | Preserve visible transmission and live growing-plot ID. |
| Timber Workbench | V8 one-tile | accepted integrated | Preserve accepted one-tile source and all eight sprite files; no duplicate rebuild. |
| Cooking Fire | V2 | accepted integrated | Preserve approved art and native steam-input integration. |
| Solar Boiler | V8 | accepted integrated | Optional graphical pipe-overlap diagnostic issue #4 remains separate; preserve accepted floorless source. |
| Beach Pump | V12 | repair required | Separate above-water and underwater geometry/passes, rerender all affected states/facings; verify shoreline, full output and landfill again. Accepted per-facing alignment must be preserved. |
| Steam Condenser | V24 local test / V1 repository master | advanced candidate | Recover exact V24 editable source, current atlases and receipts from origin; preserve accepted per-facing scale. Combined profile passed fuel-fed water/pipe tests, but active 1.8.103 entities.lua still binds the legacy 64px single-frame sprite. Complete source-backed promotion. |
| Primitive Steam-Powered Pump | V2 mechanism candidate; V1 full capture archived | advanced candidate | CURRENT FOCUS: V1 recovered and archived; rigid V2 linkage/actual GLB passed 97-pose checks. Construction and surface review requires rework: repair reducers/elbows, support and line firebox/boiler, bake model-specific maps, then full sprite/native integration and visual acceptance. |
| Fish Pond | V1 | advanced candidate | Reuse Clay Pit-derived basin and four animated fish. Inspect design and source, complete 16-pose four-way captures and atlases, test recipe/working states, then integrate reviewed candidate. |
| Stone Water Wheel | V2 failed study, held | rebuild required | Both recipe and technology are active, but this is a shoreline intake, not the pipe pump. Preserve rejected studies. If resuming lifting buckets, use independent upright pivots; repair outlet boolean degenerates and race joints before any production capture. |
| Wood Basin | OBJ blockout | rebuild required | Author timber-stave cistern, hoops, visible level/window; preserve 25000 volume and four declared corner connections/two-direction contract. |
| Tank Ammunition Assembler | OBJ blockout | rebuild required | Build distinct component/ammunition process, feed and discharge, moving tooling; verify native north/south fluids. |
| Tank Assembling Machine | OBJ blockout | rebuild required | Build heavy gantry and vehicle assembly bed with legible assembly motion; preserve prototype contract. |
| Steam Compressor | OBJ blockout | rebuild required | Build pressure barrel, reciprocating drive, valves and fixed native fittings; inspect mechanism clearance. |
| Quarry | OBJ blockout | rebuild required | Build supported excavation hoist, real cable path and lifted stone with readable working loop. |
| Shaler | OBJ blockout | rebuild required | Build crushing jaws, constrained transmission, material feed/discharge and cycle. |
| Calcifier | OBJ blockout | rebuild required | Build mineral furnace, charge/discharge, localized fuel/heat/exhaust and working states. |
| Thinking Hut | OBJ blockout | rebuild required | Build timber research shelter, tools and light with readable roof silhouette; appropriate subtle activity. |
| Pondering Hovel | OBJ blockout | rebuild required | Build evolved brick research shelter, supported chimney, lamp and restrained activity. |

## FMPL delivery and acceptance

For each unfinished structure: lock native dimensions and ports; author supported geometry and its surface plan; unwrap/bake model-specific materials; animate real mechanisms and prove loop/clearance; save and independently reopen the editable master; export and independently inspect the FMPL runtime artifact; render and actually view front/rear/close/clay and four production facings; pack true RGBA states/layers and atlases; validate native Factorio placement/working/stop/restart/save-reload; record visual disposition before replacement; publish and read back hashes.

FMPL uses the canonical pinned library in `fmpl-consumer.json`; validate the actual capture profile and matrix against its camera authority. Export/registry receipt audit is pending for historical accepted assets and does not authorize their rebuild. Candidate art may be saved and reviewed while approval remains pending.

## Continuation

Resume the existing Primitive Steam-Powered Pump artifact first: this is the pipe-to-pipe pump the owner identified. Keep the rejected wheel studies held; its separate shoreline intake remains in progression and any retained lifting buckets must stay upright. Recover exact Condenser V24 source/artifacts rather than duplicating them. Repair Beach Pump underwater occlusion while preserving owner-accepted placement. Finish Fish Pond export after reviewing its existing pilot, then continue through the remaining production targets. Reconcile the remote HEAD before publication and preserve concurrent work.

Owner review gates replacement of art; it does not block independent modeling, candidate capture or other structures. Never mark missing review or uninspected output PASS. Do not create a new CI workflow per structure, change progression/balance, duplicate the workbench, or add Tech-Priests turret/vehicle work.

## Evidence

- Campfire: [CAMPFIRE_ACCEPTED_21.md](../../docs/art/CAMPFIRE_ACCEPTED_21.md)
- Clay Pit: [CLAY_PIT_V4C_READABLE_SWING.md](../../docs/art/CLAY_PIT_V4C_READABLE_SWING.md)
- Pit Kiln: [PIT_KILN_V6_FINAL_MOTION.md](../../docs/art/PIT_KILN_V6_FINAL_MOTION.md)
- Lumberyard: [LUMBERYARD_V2B_VISIBLE_POWER_TRANSMISSION.md](../../docs/art/LUMBERYARD_V2B_VISIBLE_POWER_TRANSMISSION.md)
- Timber Workbench: [README.md](../../docs/art/workbench-v8-one-tile/README.md)
- Cooking Fire: [COOKING_FIRE_V2_ACTIVE_INTEGRATION.md](../../docs/art/COOKING_FIRE_V2_ACTIVE_INTEGRATION.md)
- Solar Boiler: [STRUCTURE_3D_PRODUCTION_ORDER.md](../../docs/art/STRUCTURE_3D_PRODUCTION_ORDER.md), [4](https://github.com/mrcalzon02/Tanks-for-bob-Fork/issues/4)
- Beach Pump: [2026-11-13.json](../../docs/art/local-machine-alignment/2026-11-13.json)
- Steam Condenser: [2026-11-13.json](../../docs/art/local-machine-alignment/2026-11-13.json), [contract.json](../../models/island-survival/steam-condenser/v1/contract.json), [entities.lua](../../tanks_for_bob_fork_1.8.103/prototypes/entity/entities.lua)
- Primitive Steam-Powered Pump: [STRUCTURE_3D_PRODUCTION_ORDER.md](../../docs/art/STRUCTURE_3D_PRODUCTION_ORDER.md), [43183442468](https://github.com/mrcalzon02/Dens-Mortis/actions/runs/43183442468), [WORK_ORDER.md](../../models/island-survival/primitive-steam-powered-pump/v2/WORK_ORDER.md), [runtime-inspection.json](../../models/island-survival/primitive-steam-powered-pump/candidates/v2-mechanism01/runtime-inspection.json), [visual-review.json](../../models/island-survival/primitive-steam-powered-pump/candidates/v2-mechanism01/visual-review.json)
- Fish Pond: [STRUCTURE_3D_PRODUCTION_ORDER.md](../../docs/art/STRUCTURE_3D_PRODUCTION_ORDER.md)
- Stone Water Wheel: [WORK_ORDER.md](../../models/island-survival/stone-water-wheel/v1/WORK_ORDER.md)
- Wood Basin: [designs.json](../../models/island-survival/designs.json)
- Tank Ammunition Assembler: [designs.json](../../models/island-survival/designs.json)
- Tank Assembling Machine: [designs.json](../../models/island-survival/designs.json)
- Steam Compressor: [designs.json](../../models/island-survival/designs.json)
- Quarry: [designs.json](../../models/island-survival/designs.json)
- Shaler: [designs.json](../../models/island-survival/designs.json)
- Calcifier: [designs.json](../../models/island-survival/designs.json)
- Thinking Hut: [designs.json](../../models/island-survival/designs.json)
- Pondering Hovel: [designs.json](../../models/island-survival/designs.json)
