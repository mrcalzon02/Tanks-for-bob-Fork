# Campfire — FACTORIO-SPRITE-PRODUCTION-v1 work order

**Invocation:** “Execute FACTORIO-SPRITE-PRODUCTION-v1 for the Tanks for Bob campfire.”
**Master:** [production sprite runbook](../../../docs/art/FACTORIO_PRODUCTION_SPRITE_WORKFLOW.md).
**Status:** Blender-only executable export implemented and locally verified. **V10 remains an unapproved art candidate.** See [recovery audit](../../../docs/art/CAMPFIRE_5855_RECOVERY_AUDIT.md).
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

## Current Blender-only execution gates

The user corrected scope to Blender capture/packing without game integration. Historical broader requirements and proposed in-game values below are retained for future integration, not prerequisites for this candidate export. Actual output is full-object states, not working overlays. Local runtime is Blender 4.3.2, not a claimed Blender 4.5 preset test.

| ID | Status | Known evidence / outstanding requirement |
| --- | --- | --- |
| P00 | PASS | Remote baseline 2310ddda97b469015f6ee9c42fc10e775ea6649a; recovery audit records actual prior commits and missing process |
| P01 | NOT_APPLICABLE | User corrected task to Blender-only export; engine/schema validation remains a later game-integration task |
| P02 | PASS | Existing tracked procedural source and packed maps retained; no new third-party HDRI/preset/image imports; source hashes in production-v10/capture.json |
| P03 | PASS | production-v10/reopen-qa.json and reopen.log: actual saved editable master independently reopened in Blender 4.3.2; 15 stones, 42 wood objects, six flames, cold/burning char toggles |
| P04 | PASS | Documented local adapter tools/art/SPRITE_EXPORT.md executed on actual model; no untested external exporter claimed |
| P05 | IN_PROGRESS | Camera/daylight fixed and recorded in production-v10/capture.json; repeated frame test recorded in integration-checks.json. Final art/Factorio lighting calibration remains unaccepted |
| P06 | NOT_APPLICABLE | Blender-only full-object state atlases avoid base-plus-overlay duplication by using complete states. Separate game overlays/shadows are outside this execution scope |
| P07 | PASS | production-v10/frames and capture.json: idle + 16 burning transparent captures, 256px source canvas, fixed camera and no independent cropping |
| P08 | PASS | production-v10/qa.json: six atlases, 64/128/256px cells, 16 burning frames at 8×2; static-four-view separately tested. Lua remains outside Blender-only scope |
| P09 | PASS | production-v10/qa.json, reopen-qa.json, process-tests.txt: dimensions, alpha, clipping, frame hashes/order, unique cells, atlas extraction and 14 regression tests; visual review is P11 |
| P10 | NOT_APPLICABLE | User's Blender-only scope excludes Factorio deployment/load/state tests; none claimed |
| P11 | PENDING | Stone reflectivity change implemented as V10 review candidate; explicit user art acceptance, final lighting/native readability and animation seam review still pending |
| P12 | IN_PROGRESS | Source/candidate publication to main and remote readback are the remaining step of this recovery; game sprite replacement is not authorized by this export |

### Next command when asked to execute (current scope)

Read `tools/art/SPRITE_EXPORT.md` and run its `export_sprites.py` entrypoint into a new directory. Reopen/packing verification is automatic. Review actual stone appearance and motion; do not stop Blender export for an absent game binary. Do not mark P05/P11 accepted from test success.

### Historical integration sequence (only for a future integration request)

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
| ART-CF-005 | 2026-11-06 Alaska | P05/P11 | Stones looked sparkling/wet; correction was never logged or committed | V10 adapter, per-material before/after capture.json, stone-material-comparison.png | Material/reopen tests pass; visual acceptance pending |
| ART-CF-006 | 2026-11-06 Alaska | P07/P09 | Development shadow catcher crossed alpha canvas bounds | Profile hides ground from beauty export; original object retained editable | Final frames pass clipping; separate shadow atlas not delivered |
| ART-CF-007 | 2026-11-06 Alaska | P03/P09 | Background save discarded RENDER scene despite successful renders | Retain MODEL/RENDER with fake users; independent reopen verifier | Both scenes and state/material/camera checks pass |

### Recovery execution record

See `docs/art/CAMPFIRE_5855_RECOVERY_AUDIT.md` for the repository-based verdict and original commit receipts. Final V10 capture and static four-view outputs live in `production-v10/`. This is a locally verified executable Blender process with unapproved candidate art, not a game integration result.

**Important:** Art diagnostics do not retroactively block unrelated gameplay releases. However **the new campfire sprite itself must not replace the approved sprite** until its own engine/load tests and visual signoff succeed.

## Command-line audit (structure and gate status only)

~~~bash
python3 tools/art/validate_export_checklist.py models/island-survival/blender/CAMPFIRE_PRODUCTION_EXPORT_CHECKLIST.md
python3 tools/art/validate_export_checklist.py models/island-survival/blender/CAMPFIRE_PRODUCTION_EXPORT_CHECKLIST.md --require export
python3 tools/art/validate_export_checklist.py models/island-survival/blender/CAMPFIRE_PRODUCTION_EXPORT_CHECKLIST.md --require publish
python3 -m unittest discover -s tools/art -p 'test_*.py' -v
~~~

The first audit should **pass structural validation** while naming P01 as the next unresolved gate. Both stricter modes must fail closed until the corresponding steps have independent evidence. This validator does not simulate Factorio or approve art.
