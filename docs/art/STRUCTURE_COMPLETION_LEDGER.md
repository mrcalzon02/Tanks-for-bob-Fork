# Ongoing structure completion ledger

Updated 2026-11-17; original baseline `7290824bf43711d0bb31bd8e2969c51459864f91`.

21 survival/manufacturing structures; excludes vehicles and Tech-Priests turrets.

Owner priority 2026-11-15: finish working, animated, operational and close enough; defer cosmetic polish. Preserve accepted art and verify actual prototype behavior. Track source/export/FMPL receipts honestly; missing receipts are pending, never automatic PASS. See docs/art/OPERATIONAL_FINISH_POLICY.md.

**21 accepted/integrated. All original eleven remaining machines delivered; audit receipts before continuing authorized Tech-Priests scope. The historical condenser V1 candidate remains held.**

| Structure | Latest known revision | Status | Remaining action |
| --- | --- | --- | --- |
| Campfire | V12 | accepted integrated | Preserve accepted source and installed animation. |
| Clay Pit | V4c | accepted integrated | Preserve readable swing and installed four-way animation. |
| Pit Kiln | V6 | accepted integrated | Preserve whole-tray motion and installed animation. |
| Lumberyard | V2b | accepted integrated | Preserve visible transmission and live growing-plot ID. |
| Timber Workbench | V8 one-tile | accepted integrated | Preserve accepted one-tile source and all eight sprite files; no duplicate rebuild. |
| Cooking Fire | V2 | accepted integrated | Preserve approved art and native steam-input integration. |
| Solar Boiler | V8 | accepted integrated | Optional graphical pipe-overlap diagnostic issue #4 remains separate; preserve accepted floorless source. |
| Beach Pump | V12 | accepted integrated | Owner accepted installed V12 as operational and close enough on 2026-11-15. Preserve animation, native flow/full-output/landfill and alignment. Underwater occlusion is deferred visual review; archive/FMPL receipt recovery remains separate. |
| Steam Condenser | V2 actual wood-steam-to-stone treatment chamber | accepted integrated | Retained ten-group starter, supported brick/clay chamber and offset piston/belt drive, 385-pose source/GLB sweep, 132 genuine frames, four native recipe cases, 20 machine pipe joints, exact inputs/results/fuel and power/blocked/stop/reload proof. Sixty client PNGs; source/canonical FMPL pushed and read back. Historical V1 water-output candidate stays held. |
| Primitive Steam-Powered Pump | V3 owner-approved, animated and integrated | accepted integrated | Complete: 68 native Blender frames, six atlases, saved editable source, inspected GLB, actual four-facing water/oil transfer, no-fuel, stop/restart, full-output and save/reload tests, plus eight genuine client screenshots. Preserve this accepted design and move on. |
| Fish Pond | V2 | accepted integrated | Preserve the accepted clay basin, four swimmers, baked portable source and tested native idle/working integration. |
| Stone Water Wheel | V3 upright cam-drained buckets | accepted integrated | Saved source/actual GLB 385-pose sweeps and upright pivots, 32 working frames per facing, sixteen native grid joints, 30/s extraction, full/drain/stop/landfill and operated reload; remote source and canonical FMPL verified. Preserve. |
| Wood Basin | V1 native contents-driven cistern | accepted integrated | Preserve passive 25000-unit cistern, four fixed corner fittings, two art orientations and native fluid window. |
| Tank Ammunition Assembler | V1 primitive electric press/packing and wood-oil works | accepted integrated | All eight starter groups, 33 source/export PBR images, 385-pose source/GLB fit/clearance, 32 working frames/facing, all 46 recipes/four directions, 20 grid joints, late full-output/power/fluid recovery and operated reload; pushed and canonical FMPL read back. Preserve. |
| Tank Assembling Machine | V1 primitive electric vehicle conversion gantry | accepted integrated | All nine starter groups; upright engine lift and attached joining tool; source/GLB 385-pose clearance, 33 genuine source captures, all 13 actual recipes, fixed north, power/full-output/stop/restart and actual operated reload. Forty-six native screenshots and 32 distinct eight-fps phases; source pushed and canonical FMPL read back. Preserve. |
| Steam Compressor | V2 owner-identified barrel source | accepted integrated | Preserve operational barrel compressor and delivery receipts; no cosmetic rework. |
| Quarry | V5 detailed rooted excavation hoist | accepted integrated | Complete: packed editable source, inspected GLB, 17 true frames, six real recipes, fuel/blocked/stop/restart, actual operated-save reload and 12 client screenshots; aligned flue smoke. Canonical FMPL registered and remote delivery verified. Preserve this operational asset. |
| Shaler | V2 geared thermal waste processor | accepted integrated | Complete: supported brick chimney, keyed gear train and two linked piston mechanisms, process hoses, packed/reopened source, inspected GLB, 68 true frames, all 17 native recipes/four facings, 88 pipe joints, blocked/fuel/stop/restart and settled operated-save reload. Thirty-six client captures and genuine working video; canonical FMPL/remote delivery verified. |
| Calcifier | V2 offset drive and full-size registered sockets | accepted integrated | Eight real recipes/four facings, 44 grid pipe joints, 385-pose source/GLB clearance review, placed-pipe closeups, native stop/restart and operated reload; source pushed and canonical FMPL read back. Preserve. |
| Thinking Hut | V1 supported shelter and refined working lantern | accepted integrated | Fixed native north; all 19 research input combinations and 14 accepted items exercised; 385-pose source/GLB clearance, upright pans, native day/night/idle, fuel/input recovery and operated reload; source/checkpoint pushed and canonical FMPL verified. Preserve. |
| Pondering Hovel | V1 masonry research upgrade | accepted integrated | Real Workbench construction/unlock, all 19 research input combinations and 14 inputs, source/GLB 385-pose clearance, day/night working lantern, fuel/input recovery and actual operated reload; pushed and canonical FMPL verified. Preserve. |

## FMPL delivery and acceptance

For each unfinished structure: lock native dimensions and ports; author supported geometry and its surface plan; unwrap/bake model-specific materials; animate real mechanisms and prove loop/clearance; save and independently reopen the editable master; export and independently inspect the FMPL runtime artifact; render and actually view front/rear/close/clay and four production facings; pack true RGBA states/layers and atlases; validate native Factorio placement/working/stop/restart/save-reload; record visual disposition before replacement; publish and read back hashes.

FMPL uses the canonical pinned library in `fmpl-consumer.json`; validate the actual capture profile and matrix against its camera authority. Export/registry receipt audit is pending for historical accepted assets and does not authorize their rebuild. Candidate art may be saved and reviewed while approval remains pending.

## Continuation

The enduring goal is active. Resume from docs/art/REMAINING_STRUCTURES_HANDOFF.md and the current active_structure in the JSON ledger. Preserve all accepted assets; Beach Pump V12 underwater polish is deferred. Keep the unfamiliar Tanks condenser candidate held and uninstalled; actual recipes, not names, define function. Tech-Priests atmospheric condenser V24 is a separate machine. Keep rejected wheel studies held and lifting buckets upright. Reconcile remote HEAD and preserve concurrent work.

Follow docs/art/OPERATIONAL_FINISH_POLICY.md: prioritize working animated integration and necessary operational checks, using judgment for close-enough visuals. Do not request routine promotion permission again or add cosmetic production cycles. Never fabricate specific owner visual approval or missing source/export receipts. Do not create extra CI workflows, change progression/balance, duplicate the workbench, or add Tech-Priests work before Tanks is complete. After Tanks, the owner has authorized unfinished Tech-Priests buildings, engines and dropped turrets.

## Evidence

- Campfire: [CAMPFIRE_ACCEPTED_21.md](../../docs/art/CAMPFIRE_ACCEPTED_21.md)
- Clay Pit: [CLAY_PIT_V4C_READABLE_SWING.md](../../docs/art/CLAY_PIT_V4C_READABLE_SWING.md)
- Pit Kiln: [PIT_KILN_V6_FINAL_MOTION.md](../../docs/art/PIT_KILN_V6_FINAL_MOTION.md)
- Lumberyard: [LUMBERYARD_V2B_VISIBLE_POWER_TRANSMISSION.md](../../docs/art/LUMBERYARD_V2B_VISIBLE_POWER_TRANSMISSION.md)
- Timber Workbench: [README.md](../../docs/art/workbench-v8-one-tile/README.md)
- Cooking Fire: [COOKING_FIRE_V2_ACTIVE_INTEGRATION.md](../../docs/art/COOKING_FIRE_V2_ACTIVE_INTEGRATION.md)
- Solar Boiler: [STRUCTURE_3D_PRODUCTION_ORDER.md](../../docs/art/STRUCTURE_3D_PRODUCTION_ORDER.md), [4](https://github.com/mrcalzon02/Tanks-for-bob-Fork/issues/4), [verification.json](../../docs/art/checkpoint-2026-11-16/verification.json)
- Beach Pump: [2026-11-13.json](../../docs/art/local-machine-alignment/2026-11-13.json), [OPERATIONAL_FINISH_POLICY.md](../../docs/art/OPERATIONAL_FINISH_POLICY.md)
- Steam Condenser: [2026-11-13.json](../../docs/art/local-machine-alignment/2026-11-13.json), [contract.json](../../models/island-survival/steam-condenser/v1/contract.json), [entities.lua](../../tanks_for_bob_fork_1.8.103/prototypes/entity/entities.lua)
- Primitive Steam-Powered Pump: [FMPL_MODEL.json](../../models/island-survival/primitive-steam-powered-pump/v3/FMPL_MODEL.json), [engine-receipt.json](../../docs/art/primitive-pipe-pump-v3/engine-receipt.json), [capture-receipt.json](../../docs/art/primitive-pipe-pump-v3/capture-receipt.json), [verification.json](../../docs/art/checkpoint-2026-11-16/verification.json)
- Fish Pond: [README.md](../../docs/art/fish-pond-v2/README.md), [FMPL_MODEL.json](../../models/island-survival/fish-pond/v2/FMPL_MODEL.json), [verification.json](../../docs/art/checkpoint-2026-11-16/verification.json)
- Stone Water Wheel: [FMPL_MODEL.json](../../models/island-survival/stone-water-wheel/v3/FMPL_MODEL.json), [native delivery](../../docs/art/stone-water-wheel-v3/README.md)
- Wood Basin: [FMPL_MODEL.json](../../models/island-survival/wood-basin/v1/FMPL_MODEL.json), [engine-receipt.json](../../docs/art/wood-basin-v1/engine-receipt.json), [capture-verification.json](../../docs/art/wood-basin-v1/capture-verification.json)
- Tank Ammunition Assembler: [FMPL_MODEL.json](../../models/island-survival/tank-ammo-assembling-machine/v1/FMPL_MODEL.json), [native delivery](../../docs/art/tank-ammo-assembler-v1/README.md)
- Tank Assembling Machine: [designs.json](../../models/island-survival/designs.json)
- Steam Compressor: [FMPL_MODEL.json](../../models/island-survival/steam-compressor/v2/FMPL_MODEL.json), [engine-receipt.json](../../docs/art/steam-compressor-v2/engine-receipt.json), [capture-receipt.json](../../docs/art/steam-compressor-v2/capture-receipt.json)
- Quarry: [designs.json](../../models/island-survival/designs.json)
- Shaler: [designs.json](../../models/island-survival/designs.json)
- Calcifier: [designs.json](../../models/island-survival/designs.json)
- Thinking Hut: [designs.json](../../models/island-survival/designs.json)
- Pondering Hovel: [FMPL_MODEL.json](../../models/island-survival/pondering-hovel/v1/FMPL_MODEL.json), [native delivery](../../docs/art/pondering-hovel-v1/README.md)
