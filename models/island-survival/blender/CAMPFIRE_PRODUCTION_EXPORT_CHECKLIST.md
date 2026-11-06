# Campfire — FACTORIO-SPRITE-PRODUCTION-v1 work order

**Invocation:** “Execute FACTORIO-SPRITE-PRODUCTION-v1 for the Tanks for Bob campfire.”  
**Master:** [production sprite runbook](../../../docs/art/FACTORIO_PRODUCTION_SPRITE_WORKFLOW.md).  
**Status:** Planning and native Blender asset completed. **Not production export-ready; game sprites unchanged.**  
**GitHub tracking issue:** [#3 — Campfire production export](https://github.com/mrcalzon02/Tanks-for-bob-Fork/issues/3).  
**Baseline audited:** 2026-11-06, main at fd83c3c6b959448d3471520fe17d35ad606c9be8.

## Verified current sources (baseline, not target assumptions)

- Entity source: tanks_for_bob_fork_1.8.95/prototypes/entity/entities.lua, around lines 2609–2699.
- Prototype: assembling-machine named campfire, chemical burner, cooking category.
- Collision: [-1.2,-1.2] to [1.2,1.2]; selection: [-1.5,-1.5] to [1.5,1.5].
- Idle: graphics/entity/campfire.png, 64×64, frame_count 1, line_length 1, shift {0,0}.
- Working: graphics/entity/campfire-w.png, 64×64 cells, frame_count 2, line_length 2, shift {0,0}; working light intensity .4 size 6.
- Blender: models/island-survival/blender/generated-v9/campfire-v9-animated.blend; development preview and GIF available, 15 stones, 42 wood component objects, 6 animated flame meshes; V9 uses frame 0 idle/normal wood and frames 1–96 burning with localized char.
- Existing ONE scoped development build: .github/workflows/campfire-blender.yml; **does not produce Factorio production spritesheets**.
- **Version discrepancy to resolve P01:** repository's documented headless smoke target includes Factorio 2.0.77; recent requirements mention 2.1. Confirm actual install/runtime + current official prototype schema before any production integration. Do not claim load compatibility in either version from a preview.
- Community setup: Valerian Factorio forum .blend (not yet downloaded/tested); AshenHermit Blender Factorio Utils v0.8 (not yet tested in Blender 4.5). HDRI/edge/AO setup per Malcolm Riley tutorial (not yet calibrated in V9).

## Proposed export (NOT approved or committed)

| Parameter | Existing in game | Candidate | Approval dependency |
| --- | --- | --- | --- |
| Camera / directions | 1 entity view | 1 fixed orthographic view | P05 registration against real source |
| Idle | 64×64 × 1 | Same with normal uncharred wood | P03/P05/P06 |
| Working | 64×64 × 2 | 64×64 × 16 at 8 columns × 2 rows (512×128) | P06/P08 timing and actual engine |
| Hi-res working | none evidenced | 128×128 frames, 8×2 (1024×256), proposed scale 0.5 | P05/P08; confirm API syntax |
| Fire timing | not pinned | 8fps (~.133333 animation_speed at 60 UPS) | P01/P10; working constant_speed |
| Body/working layers | base + working overlay | base natural wood; aligned char mask + flames; distinct shadow as needed | P06 ensure no duplicate stones or wood |
| Fire lighting | engine light 0.4 / size 6 | preserve while comparing, adjust only if needed | P10 gameplay view |
| Blender sampling | full V9 frame range 1–96 | 16 evenly sampled frames | P07/P09 continuity and loop |
| Origin / scale / shift | current 64px shift {0,0} | unknown, to calibrate; no per-frame crop | P05 |
| Distribution | original sprites | no switch yet | P11 user approval, P12 |

## Execution gates

| ID | Status | Known evidence / outstanding requirement |
| --- | --- | --- |
| P00 | PASS | Existing prototype & native V9 source located above; baseline commit fd83c3c (revalidate on later HEAD) |
| P01 | BLOCKED | Factorio 2.0.77 vs 2.1 and relevant working_visualisation API not yet locked to tested binary |
| P02 | PENDING | Actual V9 maps procedural; verify source/license provenance on any future HDRI/preset/image imports; reference-only credits already documented |
| P03 | IN_PROGRESS | V9 saved .blend reopened in GitHub CI run 42308478856; objects/animation/char tests passed; production Blender 4.5 LTS reopen and source comparison still pending |
| P04 | PENDING | Pin and test Valerian .blend and AshenHermit exporter in Blender 4.5 LTS |
| P05 | PENDING | Create HDRI + AO/edge camera calibration; source sprite side-by-side and frozen settings |
| P06 | PENDING | Extract base vs burning-only char/flame overlays; prove registration and absence of double-drawn stones/logs |
| P07 | PENDING | Render genuine transparent production frames from Blender, fixed camera and canvas |
| P08 | PENDING | Verify packer, 1 direction, 16 candidate frames, 8×2 layout, Lua and hi-res syntax |
| P09 | PENDING | Verify alpha, sheet dimensions, transitions, masks, hashes and actual fidelity |
| P10 | PENDING | Exact client load + idle/fuel/work/stop/restart in disposable mod |
| P11 | PENDING | Original-vs-new side-by-side & explicit art approval |
| P12 | PENDING | Merge only approved replacement, remote readback and rollback preservation |

### Next command when asked to execute

Open this file and runbook. Start with **P01**, not an arbitrary re-model or new GIF. Resolve installed engine target and exact 2.1-vs-2.0 API; then source/compatibility checks P02-P04; then camera and lighting P05; then passes, exporter and tests. Never infer that a preview job completed P05–P12.

### Pre-existing process defects / resolved errors

| ID | Gate(s) implicated | Recorded defect and correction |
| --- | --- | --- |
| ART-CF-001 | P03/P06 | Previous GIF existed but was incorrectly treated as proof of all render objects. New native .blend reopen/mesh manifest required. |
| ART-CF-002 | P06/P09 | V9 early idle/burning stills were identical despite saved shader drivers; replaced with timeline-keyed frame 0 cold and frames 1–96 burning, and added image-difference check. |
| ART-CF-003 | P06/P09 | First char-only diagnostic had flames obscuring the result; later scene renders flames-hidden char study and validates content difference. |
| ART-CF-004 | P04/P05 | Earlier 4.0.2 preview was treated as if a 4.5 production-camera/HDRI preset had been calibrated. This remains open pending actual preset tests. |

### Evidence / follow-up records

- Blender code and output: [source directory](https://github.com/mrcalzon02/Tanks-for-bob-Fork/tree/main/models/island-survival/blender).
- Latest V9 production-candidate build: [GitHub run 42308478856](https://github.com/mrcalzon02/Tanks-for-bob-Fork/actions/runs/42308478856).
- Unchanged original sprites: tanks_for_bob_fork_1.8.95/graphics/entity/campfire.png and campfire-w.png.
- New dated findings, source commit, failures, fixes, render hashes and game acceptance must be **appended below**, rather than replacing this history.

## Execution log

| UTC date | Stage | Evidence | Result |
| --- | --- | --- | --- |
| 2026-11-06 | P00/P03 baseline | V9 GitHub build run 42308478856; main fd83c3c | Native source exists, development rendering passed; not Factorio export approval |
| 2026-11-06 | Process v1 established | FACTORIO_PRODUCTION_SPRITE_WORKFLOW.md | P01 and remaining production gates to execute |

## Future defect register

| Defect ID | Date | Gate reopened | Failure and cause | Fix SHA / evidence | Re-test status |
| --- | --- | --- | --- | --- | --- |

**Important:** Art diagnostics do not retroactively block unrelated gameplay releases. However **the new campfire sprite itself must not replace the approved sprite** until its own engine/load tests and visual signoff succeed.

## Command-line audit (structure and gate status only)

~~~bash
python3 tools/art/validate_export_checklist.py models/island-survival/blender/CAMPFIRE_PRODUCTION_EXPORT_CHECKLIST.md
python3 tools/art/validate_export_checklist.py models/island-survival/blender/CAMPFIRE_PRODUCTION_EXPORT_CHECKLIST.md --require export
python3 tools/art/validate_export_checklist.py models/island-survival/blender/CAMPFIRE_PRODUCTION_EXPORT_CHECKLIST.md --require publish
python3 -m unittest discover -s tools/art -p 'test_*.py' -v
~~~

The first audit should **pass structural validation** while naming P01 as the next unresolved gate. Both stricter modes must fail closed until the corresponding steps have independent evidence. This validator does not simulate Factorio or approve art.
