# FACTORIO-SPRITE-PRODUCTION-v1 — asset execution template

Copy to the asset's source directory as ASSET_PRODUCTION_EXPORT_CHECKLIST.md. Do not change gate IDs. See [canonical runbook](FACTORIO_PRODUCTION_SPRITE_WORKFLOW.md) (relative link must be adjusted after copying).

## Identity / baseline (fill only from checked sources)

- Asset and prototype type/name:
- Target repository / branch / starting SHA:
- Original sprite path, hash, source frame geometry:
- Exact prototype path and line range; collision/selection/shift/scale:
- Target installed Factorio version + official API page:
- Blender binary/version; actual editable .blend path and SHA:
- Reference model/camera and preset commit/version:
- Lighting/HDRI source, author, license, calibration values:
- Active development branch, production output directory and rollback assets:
- Tentative number of orientations, states, frames, atlas shape / speed (mark **PROPOSED** if not tested):
- Assumptions/unknowns; GitHub tracking issue:

## Gates: fill PASS only after adding evidence

| Gate | Status | Evidence link/path + tested revision | Reviewer/date |
| --- | --- | --- | --- |
| P00 baseline | PENDING | — | — |
| P01 engine prototype/version | PENDING | — | — |
| P02 art source/license | PENDING | — | — |
| P03 Blender MODEL reopened | PENDING | — | — |
| P04 community export preset tested | PENDING | — | — |
| P05 RENDER camera/lighting calibrated | PENDING | — | — |
| P06 idle/working layers verified | PENDING | — | — |
| P07 Blender output frames exported | PENDING | — | — |
| P08 sheet and Lua export verified | PENDING | — | — |
| P09 automated sprite QA | PENDING | — | — |
| P10 exact Factorio client tested | PENDING | — | — |
| P11 human visual art approval | PENDING | — | — |
| P12 committed/published/read back | PENDING | — | — |

## Layer specification (complete before P06)

| Layer/state | From Blender collection/pass | Output path | Frames, frame size, atlas shape | Engine use/registration | Verified? |
| --- | --- | --- | --- | --- | --- |
| Idle physical structure | — | — | — | — | PENDING |
| Burning-only modifications | — | — | — | — | PENDING |
| Fire and embers | — | — | — | — | PENDING |
| Shadow | — | — | — | — | PENDING |
| Additional effects (only if needed) | — | — | — | — | PENDING |

## Execution log (append entries; never delete failures)

| UTC timestamp | Stage | Git SHA / Blender version | Action / evidence | Result / next blocker |
| --- | --- | --- | --- | --- |

## Defect / process audit trail (append)

| ID | Date | Gate(s) reopened | Symptom & root cause | Fix commit/evidence | Retest & approval |
| --- | --- | --- | --- | --- | --- |

## Release decision

- Source asset approved? **NO** until P11.
- Replacement integrated in active mod? **NO** until P12 and verified engine load.
- Other-gameplay releases are not blocked solely by art diagnostics; art replacement is not approved without its own visual acceptance.
