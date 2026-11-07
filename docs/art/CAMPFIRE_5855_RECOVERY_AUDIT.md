# 5855 campfire process recovery audit — 2026-11-06 (Alaska)

## Verdict before this recovery

**The requested executable export process was not finished in GitHub.** The repository did contain native V9 art and the process paperwork. This is verified from the actual remote `main` at `2310ddda97b469015f6ee9c42fc10e775ea6649a`, rather than assuming that an earlier assistant's completion claim was sufficient.

| Recovered item | Actual repository evidence | Status before recovery |
| --- | --- | --- |
| Editable V9, renders and animated preview | `models/island-survival/blender/generated-v9/`; source publication `fd83c3c6b959448d3471520fe17d35ad606c9be8`, later generated publication `2310ddd` | Committed |
| Runbook and work order | `e281550` | Committed |
| Checklist validator and issue reference | `5bddfec` | Committed |
| Existing CI checklist invocation | `483a7e5` | Committed |
| Reusable production frame/atlas exporter | No implementation in audited tree; runbook explicitly says it must still be introduced | Unfinished |
| Production atlas/capture QA evidence | No production atlas or capture/packing manifest in audited tree | Unfinished |
| Stone reflectivity correction requested in 5855 | No correction or defect entry in audited tree | Unfinished |

Conversation retrieval recovered the earlier corrected scope: **Blender-only**, including static/animated captures, packed sheets, editable `.blend` and previews. It did not return a complete transcript of the named audit or recover a later local exporter. Filename searches also found V9 deliverables, not a later production package. Therefore this is a verified repository audit plus recovery implementation; it is not a claim to have recovered every message or inaccessible scratch file from the prior conversation.

## Work completed by this recovery

- Added the single entrypoint `tools/art/export_sprites.py`, Blender capture worker, independent saved-master verifier and documented profile format. No game runtime is required for Blender capture.
- Executed the full campfire test: one idle + 16 burning source frames, six full-object state atlases, paired 64/128/256px cells, contact sheet and 16-frame preview GIF.
- Added and executed a four-direction static test at 0/90/180/270 degrees. The same exporter handles static and animated assets with explicit timeline sampling.
- Added the V10 dry-stone material adapter and logged all prior/current material values. The art remains a review candidate, **not accepted**.
- Preserved source V9, retained all original game sprites, and kept the existing scoped CI job. Extended that job to execute and upload both export tests; CI result is independent of the local verification recorded here.

## Defects found during actual execution

| ID | Finding | Correction and evidence |
| --- | --- | --- |
| ART-CF-005 | User rejected sparkling/wet-looking stone response; no existing logged correction | Principled roughness .98, specular IOR level .08, metallic/coat zero, 15 stone materials; all before/after inputs recorded in `production-v10/capture.json`. Visual acceptance pending. |
| ART-CF-006 | First capture's development shadow catcher crossed the canvas: idle alpha bounds `(0,78,256,247)` on a 256px canvas | Integrity check rejected capture; profile excludes ground from beauty export. All final state frames pass clipping checks. Separate ground-shadow output remains outside this profile. |
| ART-CF-007 | Separate reopen exposed Blender discarding the copied RENDER scene during background save | Explicit fake users retain MODEL and RENDER; final independent reopen confirms both scenes, camera, daylight and source state. |

Failed runs were retained outside the deliverable tree while fixes were made; only passing final captures are published. Tests intentionally inject missing/reordered/corrupt frames, duplicate animation cells, opaque images and clipping; they must reject each case.

## Evidence

Primary evidence directory: `models/island-survival/blender/production-v10/`.

| Check | Evidence |
| --- | --- |
| Actual source revision and frozen rig | `capture.json` (source SHA256, tool version, camera, daylight, color management, per-frame hashes) |
| Atlas count, dimensions, alpha and exact packed cell content | `qa.json`; six atlases, 17 real captures |
| Independent editable master reopen | `reopen-qa.json`, `reopen.log`, `master.blend` |
| Four-direction static capture | `static-four-view/capture.json`, `static-four-view/qa.json`, its reopened `master.blend` |
| Repeat-capture determinism and before/after materials | `integration-checks.json`, `stone-material-comparison.png` |
| Regression tests | `process-tests.txt`; 14 tests |
| Script usage and output semantics | `tools/art/SPRITE_EXPORT.md` |

## Remaining acceptance boundaries

The Blender executable capture/pack process and candidate outputs are implemented and locally verified. **Campfire visual acceptance is still pending**, including the stone correction, lighting calibration, native readability and animation loop seam. No third-party HDRI/preset/add-on has been imported or falsely marked tested. Ground-shadow atlas, working overlays, Lua and game integration are not part of this Blender-only completion. No Factorio load or gameplay result is claimed.

## GitHub publication receipt

Pending publication and remote readback of this implementation. This section will be updated only after the remote tree is verified.
