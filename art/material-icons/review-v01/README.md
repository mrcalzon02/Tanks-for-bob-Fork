# Material and missing-icon pass — completed locally

The native audit covered Tech Priests and Tanks for Bob 1.8.103 with Factorio 2.1.24. All icon file references resolved; visual inspection found twenty different materials/documents using one crate image, ten related research icons using that crate, a literal water-wheel placeholder, an inconsistent calcifier icon, and unbound finished Tech Priests weapon/supply art.

The completed pass contains **111 new or newly rendered icons**: all **105 Tanks material/fluid/module icons**, water wheel and calcifier, Tech Priests field supply, and three existing authored faction-factory models rendered as inventory icons. **Twenty-five finished weapon/ammo icons** are also integrated into their actual canonical Tech Priests prototypes. The native graphical atlas loaded all **136** paths. No generic crate artwork remains bound in the Tanks runtime inventory.

Every modeled asset has selected editable Blender source, packed maps, an actual GLB export, independent source/capture reopen checks, source-to-export color/silhouette comparisons, and 64/128/256 transparent renders. The props use the established FMPL camera and selected C pose. Existing factory GLBs remain unchanged and upright under the same 45-degree optics. Assistant visual review and technical validity passed; owner visual acceptance is recorded separately as pending.

Native matched-source comparison shows **362 icon-record changes and zero non-icon prototype changes**. The shared checkout received unrelated actor, animation and furnace changes during production; those are preserved. A private baseline omitting only this task's art hooks isolates the icon delta. Logs and both snapshots remain in the build profiles. No normal game profile was installed or modified, and no public publication is claimed.

The full runtime inventory also covers legacy vehicle, gun, ammo and equipment icons. Intentional native/shared icon reuse is retained outside the material and explicit-placeholder pass. Existing Tech Priests salvage overlays and ability symbols remain identified in the audit rather than silently changing their meaning. Eleven finished hydrogen-chain icons still target review-only prototypes absent from this runtime profile; their existing sources are preserved without adding dummy production prototypes.

The actual-unit weapon/AAI work remains a separate pending task, recorded in `art/unit-arsenal/ACTUAL-UNIT-AAI-HANDOFF.md` in the hydrogen-production checkout. This icon pass does not claim combat integration completion.

## Review and rebuild

- `before-after-highlights.png`: representative original/replacement comparison.
- `modeled-materials-01.png` through `04.png`: every selected material/prop at 128 and 64 pixels.
- `native-icon-atlas.png`: actual Factorio sprite-path capture for all 136 integrated icons.
- `delivery-validation.json`: selected paths, model/icon/source hashes and technical/native evidence.
- `full-icon-only-native-validation.json`: exact native icon-only delta.
- `inventory.json` and `before/inventory.json`: engine-resolved after/before bindings and recipe icon inheritance.

The owning repositories keep sources under `art/source-to-3d/material-icons/<revision>/<asset>/`, with rebuild definitions and tools under `tools/art/material_icons/`. Earlier studies remain preserved. The review kit contains runtime PNGs, integration Lua, previews, manifests and build definitions; editable model and capture masters remain in those repository source folders.
