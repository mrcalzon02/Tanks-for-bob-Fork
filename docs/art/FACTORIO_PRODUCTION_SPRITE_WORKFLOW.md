# FACTORIO-SPRITE-PRODUCTION-v1 — Blender-to-Factorio export runbook

**Machines with pipe fittings:** use the [fluid connection modeling guide](FLUID_CONNECTION_MODELING_GUIDE.md) and its [standalone Blender reference](../../models/reference/factorio-fluid-interface/factorio-fluid-interface-reference.blend) before modeling the receiving box, manifold or neck. The reference establishes joint size, height, direction and ground origin; keep its helpers out of production captures and verify native sprite placement for each machine.

**Stable invocation:** “Execute FACTORIO-SPRITE-PRODUCTION-v1 for <entity> in <repo>.”
**Authority:** This version-controlled document, plus the filled asset-specific work order. No remembered guess or previous assistant response overrides the checked-in procedure.
**State:** Executable Blender capture/packing is now implemented and verified with the campfire; art approval and game integration remain separate.
**Scope:** Factorio 2D entity/icon production from editable Blender masters; no recipe, balance, tech, or unrelated mod changes.

Start by reading this document, the work-order template, the specific asset work order, the current prototype, and the exact source sprite. Record the source commit before editing. Do not declare a gate passed without linked evidence.

## Effective Blender-only execution scope (v1.1, 2026-11-06)

The user corrected the active campfire task to **Blender-only capture and atlas output**, without game integration/testing. Engine API/binary discovery must not block that task. For this scope, use the [working executable process](../../tools/art/SPRITE_EXPORT.md) and [recovery audit](CAMPFIRE_5855_RECOVERY_AUDIT.md). The original broader gates below remain applicable when a later task explicitly requests game integration. They do not prevent committing scripts or unapproved candidate art.

```bash
python3 tools/art/export_sprites.py --config tools/art/profiles/campfire.json --out /tmp/campfire-export
```

This creates complete RGBA state frames, not base/working overlays. P01 and P10 engine requirements are not applicable to Blender-only execution; P06 game-layer separation and P08 Lua are deferred to integration. P11 remains pending until actual user visual acceptance. P12 distinguishes source/candidate publication from replacing accepted game art. The implementation uses the existing authored camera/light rig and a tested local adapter, rather than claiming external community presets have been installed. It preserves their source references for future calibration.

## Sources and precedence

1. **Hard truth:** currently checked-out Lua entity definition, exact original mod sprite and its actual frame layout, installed target Factorio version, current official prototype API. Never infer footprint from rough model JSON.
2. **Native editable master:** actual saved Blender geometry, animation, shaders, packed maps, cameras and lights; save, reopen and inspect it. Flat renders/GIFs are previews, not the master.
3. **Engine art workflow:** [Wube FFF-146](https://factorio.com/blog/post/fff-146) and [FFF-194](https://factorio.com/blog/post/fff-194): separate MODEL and RENDER scenes, render/view layers, composite outputs, sheet packing and Lua generation.
4. **Lighting technique:** [Malcolm Riley Unused Renders wiki](https://github.com/malcolmriley/unused-renders/wiki): Nauvis-like HDRI, edge highlights, ambient occlusion in concavities. Tutorial text CC0; imported images/.blend CC BY 4.0.
5. **Community starting calibration:** [Valerian Blender setup](https://forums.factorio.com/viewtopic.php?p=627369), not absolute truth: ortho camera Euler (45,0,180); sun (0,39.3,5); Standard/Medium High Contrast; exposure -0.150; world strength 0.055; ground bounce and shadow pass. Confirm actual settings against source sprite before approval.
6. **Exporter candidate:** [AshenHermit Blender Factorio Utils](https://github.com/AshenHermit/blender-factorio-utils): single/multiple directions, NLA actions, shadow catcher, tiles and Lua/sheet export. Check the version, license and Blender compatibility; do not claim it runs in 4.5 without a test.
7. **Existing Foundry tools:** [HB-TTRPG-tools Factorio Render Pipeline](https://github.com/mrcalzon02/HB-TTRPG-tools/tree/main/tools/factorio-render-pipeline), its setup/strict manifest preflight and source-first contract. Its thruster-specific scripts are not generic campfire exporters.
8. **Artwork sourcing:** [Snouz index and license policy](FACTORIO_GRAPHICS_SOURCE_REFERENCES.md) and [Unused Renders credits](UNUSED_RENDERS_WORKFLOW_AND_CREDITS.md). Search only for a current need, verify per-file rights, retain attribution. No unauthorized base-game texture redistribution, uncredited asset copying, bulk gallery, or image-generated substitutes for 3D.

## State model and failure behavior

- Gate state: **PENDING / IN_PROGRESS / PASS / BLOCKED / NOT_APPLICABLE**. PASS requires a dated evidence path/link, tested source revision and tool version. NOT_APPLICABLE requires documented reason and a reviewer; never quietly delete a gate.
- **Candidate ≠ approved.** The original game graphics remain active until a separately approved integration commit. A GIF does not prove a correct atlas, live-game alignment or valid Lua.
- If inputs, references, licenses, compatibility, calibration or output layers are unknown: set BLOCKED and report the exact missing condition. No placeholders disguised as proof.
- When a mistake is found: create a dated deviation entry with gate ID, symptom, root cause, fix commit and rechecks. Invalidate affected gate and all dependent later gates. Never overwrite the prior accepted blend or graphics. No destructive push.
- Do not create new CI jobs per texture, resolution, frame count or test profile. Reuse the existing scoped art workflow or one local entrypoint. An automation can run static checks and render, but manual art approval and game visual review must remain distinct.

## Required execution gates

| ID | Gate / mandatory action | Required acceptance evidence | Stop condition |
| --- | --- | --- | --- |
| P00 | **Establish baseline.** Fetch repo, branch, SHA, asset work order, authoritative sprite paths and Lua definition; locate approved master and prior comparison. | SHA, paths, source images and inspected Lua excerpt | Missing source/reference |
| P01 | **Lock engine contract.** Read actual mod/Factorio version and [official prototype API](https://lua-api.factorio.com/latest/), including animation state/working_visualisation semantics, dimensions, scale/shift, directions, speed and lights. Explicitly resolve 2.0-vs-2.1 differences. | Versioned API URL, engine/test binary, captured fields; uncertainties identified | Version/schema mismatch |
| P02 | **Source and rights audit.** Exact files/revisions, author, license, adaptations and destination; distinguish visual-reference-only from actual import. | Asset provenance ledger updated | Unlicensed or untraceable imported artwork |
| P03 | **Validate editable MODEL.** Reopen .blend in the chosen Blender (4.5 LTS preferred), inspect real mesh objects, material nodes, UV/normal maps, timeline and state toggles. Model only visible geometry, compare source silhouette. | Reopen log/manifest, idle + working test renders, original side-by-side | Missing, floating, hidden or noneditable objects |
| P04 | **Validate community preset.** Pin version/commit of Valerian .blend and candidate AshenHermit add-on; test installation and export in target Blender; record results. If incompatible, implement a documented local adapter with equivalent outputs, not a pretend pass. | Test log, preset hash/version, valid scene/export sample | Add-on not verified |
| P05 | **Calibrate RENDER scene and lighting.** Create linked MODEL/RENDER scenes and compositor passes. Fix orthographic camera, tile jig, origin, canvas, sun and licensed HDRI, edge highlight, AO, shadow catcher and color management. Use Valerian values only as starting candidates. Keep daylight immutable while firelight flickers. | Frozen camera/lighting parameter file, comparison with true source at native size, repeat render test | Camera/scale/lighting unverified |
| P06 | **Plan exact state/layers.** Confirm idle vs working model, frame ranges/directions, overlay registration and anchor. Only animated combustion darkens the wood. Avoid drawing the full burning object twice over the idle base. Identify color, char overlay, fire, shadow and optional emissive images separately. | Layer graph, alpha/visibility proof for idle and working | Incorrect overlay/occlusion or absent masks |
| P07 | **Export repeatable frames.** Render transparent PNG RGBA frames from real Blender using one fixed camera/pivot/lighting rig; no independent per-frame trimming, camera adjustment or frame renumbering. Keep source high-res and deliverable sizes paired. | Ordered frames and per-frame hash manifest; Blender log and .blend SHA | Missing frames, wrong state, jitters or clipping |
| P08 | **Pack atlas + Lua.** Use community exporter if verified; else equivalent pinned script. Derive frame_count, line_length, directions, frame dimensions, shifts/scales, speed and optional shadows from measured outputs. No guessed cells/engine fields. | Spritesheets, generated Lua excerpt, layout manifest/contact sheet, atlas tests | Sheet/frame count does not match Lua |
| P09 | **Automated output QA.** Verify exact dimensions, alpha and padding, no opaque full-frame rectangles, alpha fringe, sheet bounds, sequential frame ordering, same center/shift/camera, shading/char mask and shadow alignment, no dead/duplicate frames, source hashes. | Machine-readable report with explicit failure counts | Any integrity check fails |
| P10 | **Engine load and state test.** Deploy on disposable mod copy, never overwrite release art first. Test target Factorio startup/load and actual gameplay placement, fuel/working/stop/restart, original bounding boxes, layers/light, shadow, zoom, animation loop and logs. | Exact engine version, test command, unedited log, in-game screenshots/clip | Load/run/placement/overlay failure |
| P11 | **Visual acceptance.** Compare original source sprite and new art at identical native zoom/position and in context. Confirm readable materials, motion, consistent Factorio lighting; preserve diagnostics. Visual approval gates art replacement, not unrelated game releases. | Side-by-side / animation + explicit reviewer disposition | Unreviewed or rejected replacement |
| P12 | **Publish and read back.** Commit native source, scripts, licensed assets, atlases, Lua, reports and credit to proper branch; remote SHA/readback; rollback images preserved. Re-run necessary load check. | GitHub commit SHA, read-back checksums, release notes if actually released | Push/readback or regression failure |

**Dependencies:** P00-P02 precede any imported art; P03-P05 precede P06-P08; P08-P09 precede P10; P10-P11 precede P12. A failed prerequisite blocks later PASS. Advanced techniques, additional directions and hi-res layers are chosen from the entity contract, not generated gratuitously.

## Numerical and rendering rules

- Record actual camera XYZ/rotation, orthographic scale, projection target, output pixels and pixels-per-tile. Keep them immutable across every pass and frame. The Factorio prototype's frame dimensions and shift are authoritative; rough mesh dimensions are not.
- The default existing Factorio engine rate is 60 ticks/sec. Proposed animation_speed for an 8-frames/sec animation is 8/60, **subject to engine validation** and working-visualisation constant_speed semantics. Check runtime; do not assume sprite speed equals Blender render FPS.
- Frame layout proposed for campfire, **not accepted yet**: idle 1×64×64; working 16 frames of 64×64 in an 8×2 atlas (512×128), direction_count 1; candidate high resolution 128×128 frames/0.5 scale. Preserve original 2-frame working setup until approved.
- Transparent scene and material effects must be composited to avoid duplicate body geometry. Separate firelight in engine may be needed; don't bake a broad game-incorrect orange rectangle. Distinguish Blender input normal maps from Factorio render-output sprites.
- Do not self-approve a release by validating file presence: an earlier campfire run passed with identical idle/burning previews; current process must actually compare output content and state isolation. Reopen and inspect the saved .blend.
- Evidence location for each execution: asset-specific work order links to immutable commit(s), CI run(s), manifests, original sprite paths and game screenshots. File names alone aren't proof.

## Invocation and repeatable commands

For any asset:

1. Create an instance from [the asset checklist template](FACTORIO_PRODUCTION_ASSET_CHECKLIST_TEMPLATE.md) in its own Blender/source directory. Fill measured prototype properties and mark every gate PENDING before execution.
2. Say **“Execute FACTORIO-SPRITE-PRODUCTION-v1 for <asset>”**. The executor reads this SOP and the instance, checks the current branch/head, starts at the first unpassed gate, performs the actual work, attaches evidence and advances only when allowed.
3. For the campfire specifically use [the active campfire work order](../../models/island-survival/blender/CAMPFIRE_PRODUCTION_EXPORT_CHECKLIST.md).
4. Audit the checklist with the standard-library CLI: python3 tools/art/validate_export_checklist.py <work-order.md>. Use --require export or --require publish for fail-closed production readiness checks; execute python3 -m unittest discover -s tools/art -p 'test_*.py' -v for regression verification. This checks statuses, not actual Blender/game output.
5. For environment setup use the existing shared [bootstrap](https://github.com/mrcalzon02/HB-TTRPG-tools/blob/main/tools/factorio-render-pipeline/bootstrap.py) install/verify commands and record output. For existing V9 source use the [scoped Blender workflow](../../.github/workflows/campfire-blender.yml); it is a *development preview and animation workflow*, NOT a finished Factorio sprite packer.
6. The documented local fallback is now `tools/art/export_sprites.py`; its implementation and final campfire outputs are recorded in the recovery audit. Use a new profile for another authored model and revalidate its framing, required directions and timeline. External add-on compatibility is not claimed by this fallback.
7. After any change rerun affected checks and update deviations. Check remote SHA and output artifacts after push.

### Compact audit entry format

Use an append-only entry in the asset work order:

- **ID/date/revision/gate**; **what was wrong or missing**; **source that exposed it**; **effect on existing art**.
- **Root cause**; **correction files and commit**; **before/after render or raw logs**; **dependent gates invalidated**; **re-test result**; **reviewer decision**.
- A closed deviation must cite actual evidence. When the same failure recurs, reopen it; never silently erase failed history.

## Changes to this standard

Treat missing steps as process defects. Add a new Pxx gate or amend a gate via reviewed Git commit; record revision, rationale, test and all affected asset checklists. Existing completed assets must explicitly decide whether a process change triggers revalidation. Do not modify this runbook from memory alone.

**v1 (2026-11-06):** First standardized, auditable production-sprite procedure. It documents previously missing release gates; does not claim any campfire production atlas or Factorio graphical-client acceptance.

**v1.1 (2026-11-06, Alaska):** Implement and execute Blender-only capture/packing, independent master reopen and four-direction static test; honor corrected scope, log stone-reflectivity correction and retain pending art approval. No game integration is claimed.

