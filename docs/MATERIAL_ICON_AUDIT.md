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

## Selected Tanks-for-bob-Fork assets

| Prototype | Source | State |
|---|---|---|
| clay | `art/source-to-3d/material-icons/v01/clay` | Native and assistant review passed |
| brick | `art/source-to-3d/material-icons/v01/brick` | Native and assistant review passed |
| charcoal | `art/source-to-3d/material-icons/v02/charcoal` | Native and assistant review passed |
| crude-paper | `art/source-to-3d/material-icons/v02/crude-paper` | Native and assistant review passed |
| ink | `art/source-to-3d/material-icons/v01/ink` | Native and assistant review passed |
| calcifier | `art/source-to-3d/material-icons/v01/calcifier` | Native and assistant review passed |
| crude-glass | `art/source-to-3d/material-icons/v02/crude-glass` | Native and assistant review passed |
| toxic-sludge | `art/source-to-3d/material-icons/v01/toxic-sludge` | Native and assistant review passed |
| stone-tools | `art/source-to-3d/material-icons/v01/stone-tools` | Native and assistant review passed |
| wood-pulp | `art/source-to-3d/material-icons/v02/wood-pulp` | Native and assistant review passed |
| staples | `art/source-to-3d/material-icons/v01/staples` | Native and assistant review passed |
| stamps | `art/source-to-3d/material-icons/v01/stamps` | Native and assistant review passed |
| folder | `art/source-to-3d/material-icons/v01/folder` | Native and assistant review passed |
| clipboard | `art/source-to-3d/material-icons/v01/clipboard` | Native and assistant review passed |
| corporate-waste | `art/source-to-3d/material-icons/v01/corporate-waste` | Native and assistant review passed |
| PhaseDetractor | `art/source-to-3d/material-icons/v01/phasedetractor` | Native and assistant review passed |
| Canister | `art/source-to-3d/material-icons/v02/canister` | Native and assistant review passed |
| Charged-Canister | `art/source-to-3d/material-icons/v02/charged-canister` | Native and assistant review passed |
| Canister-waste | `art/source-to-3d/material-icons/v02/canister-waste` | Native and assistant review passed |
| Canister-Radioactivewaste | `art/source-to-3d/material-icons/v02/canister-radioactivewaste` | Native and assistant review passed |
| Alumatedplate | `art/source-to-3d/material-icons/v01/alumatedplate` | Native and assistant review passed |
| trace-mineral-slurry | `art/source-to-3d/material-icons/v01/trace-mineral-slurry` | Native and assistant review passed |
| saline-particulate | `art/source-to-3d/material-icons/v01/saline-particulate` | Native and assistant review passed |
| ionic-scum | `art/source-to-3d/material-icons/v02/ionic-scum` | Native and assistant review passed |
| heavy-brine-fraction | `art/source-to-3d/material-icons/v02/heavy-brine-fraction` | Native and assistant review passed |
| microcrystal-sediment | `art/source-to-3d/material-icons/v02/microcrystal-sediment` | Native and assistant review passed |
| fish-oil-residue | `art/source-to-3d/material-icons/v02/fish-oil-residue` | Native and assistant review passed |
| fish-ash | `art/source-to-3d/material-icons/v01/fish-ash` | Native and assistant review passed |
| protein-slurry | `art/source-to-3d/material-icons/v01/protein-slurry` | Native and assistant review passed |
| calcified-bone-dust | `art/source-to-3d/material-icons/v01/calcified-bone-dust` | Native and assistant review passed |
| enzyme-paste | `art/source-to-3d/material-icons/v01/enzyme-paste` | Native and assistant review passed |
| rendered-organics | `art/source-to-3d/material-icons/v01/rendered-organics` | Native and assistant review passed |
| hydrolyzed-suspension | `art/source-to-3d/material-icons/v02/hydrolyzed-suspension` | Native and assistant review passed |
| phase-diluted-brine | `art/source-to-3d/material-icons/v02/phase-diluted-brine` | Native and assistant review passed |
| osmotic-residue | `art/source-to-3d/material-icons/v01/osmotic-residue` | Native and assistant review passed |
| gradient-saline-matrix | `art/source-to-3d/material-icons/v01/gradient-saline-matrix` | Native and assistant review passed |
| biphasic-brine-gel | `art/source-to-3d/material-icons/v02/biphasic-brine-gel` | Native and assistant review passed |
| salinity-locked-emulsion | `art/source-to-3d/material-icons/v02/salinity-locked-emulsion` | Native and assistant review passed |
| hydrocoptic-precursor | `art/source-to-3d/material-icons/v01/hydrocoptic-precursor` | Native and assistant review passed |
| denatured-organic-base | `art/source-to-3d/material-icons/v01/denatured-organic-base` | Native and assistant review passed |
| enzyme-saturated-mass | `art/source-to-3d/material-icons/v02/enzyme-saturated-mass` | Native and assistant review passed |
| lipid-carrier-gel | `art/source-to-3d/material-icons/v01/lipid-carrier-gel` | Native and assistant review passed |
| bio-reactive-slurry | `art/source-to-3d/material-icons/v02/bio-reactive-slurry` | Native and assistant review passed |
| catalytic-organic-medium | `art/source-to-3d/material-icons/v01/catalytic-organic-medium` | Native and assistant review passed |
| reactive-enzyme-binder | `art/source-to-3d/material-icons/v01/reactive-enzyme-binder` | Native and assistant review passed |
| bio-synthetic-precursor | `art/source-to-3d/material-icons/v01/bio-synthetic-precursor` | Native and assistant review passed |
| crystalline-agglomerate | `art/source-to-3d/material-icons/v02/crystalline-agglomerate` | Native and assistant review passed |
| fractured-lattice-mass | `art/source-to-3d/material-icons/v01/fractured-lattice-mass` | Native and assistant review passed |
| ceramic-seed-grain | `art/source-to-3d/material-icons/v01/ceramic-seed-grain` | Native and assistant review passed |
| mineral-phase-fragments | `art/source-to-3d/material-icons/v01/mineral-phase-fragments` | Native and assistant review passed |
| ceramic-lattice-core | `art/source-to-3d/material-icons/v01/ceramic-lattice-core` | Native and assistant review passed |
| compressed-crystal-bed | `art/source-to-3d/material-icons/v01/compressed-crystal-bed` | Native and assistant review passed |
| bioceramic-preform | `art/source-to-3d/material-icons/v01/bioceramic-preform` | Native and assistant review passed |
| charged-ionic-matrix | `art/source-to-3d/material-icons/v01/charged-ionic-matrix` | Native and assistant review passed |
| dielectric-suspension | `art/source-to-3d/material-icons/v02/dielectric-suspension` | Native and assistant review passed |
| conductive-residue | `art/source-to-3d/material-icons/v01/conductive-residue` | Native and assistant review passed |
| phase-unstable-granulate | `art/source-to-3d/material-icons/v01/phase-unstable-granulate` | Native and assistant review passed |
| balanced-reactive-medium | `art/source-to-3d/material-icons/v01/balanced-reactive-medium` | Native and assistant review passed |
| phase-primed-carrier | `art/source-to-3d/material-icons/v01/phase-primed-carrier` | Native and assistant review passed |
| electro-phase-precursor | `art/source-to-3d/material-icons/v01/electro-phase-precursor` | Native and assistant review passed |
| marseline-compound | `art/source-to-3d/material-icons/v02/marseline-compound` | Native and assistant review passed |
| bioceramic-grit | `art/source-to-3d/material-icons/v01/bioceramic-grit` | Native and assistant review passed |
| hydrocoptic-crystal | `art/source-to-3d/material-icons/v02/hydrocoptic-crystal` | Native and assistant review passed |
| amulite-flakes | `art/source-to-3d/material-icons/v01/amulite-flakes` | Native and assistant review passed |
| phase-reactive-granules | `art/source-to-3d/material-icons/v01/phase-reactive-granules` | Native and assistant review passed |
| oscillated-lubricant | `art/source-to-3d/material-icons/v02/oscillated-lubricant` | Native and assistant review passed |
| stabilized-brine-gel | `art/source-to-3d/material-icons/v01/stabilized-brine-gel` | Native and assistant review passed |
| dielectric-chowder | `art/source-to-3d/material-icons/v01/dielectric-chowder` | Native and assistant review passed |
| pre-turbulated-emulsion | `art/source-to-3d/material-icons/v01/pre-turbulated-emulsion` | Native and assistant review passed |
| viscoelastic-froth | `art/source-to-3d/material-icons/v01/viscoelastic-froth` | Native and assistant review passed |
| executive-marseline-resin | `art/source-to-3d/material-icons/v01/executive-marseline-resin` | Native and assistant review passed |
| encabuloy-alloy | `art/source-to-3d/material-icons/v01/encabuloy-alloy` | Native and assistant review passed |
| hyperphase-matrix | `art/source-to-3d/material-icons/v01/hyperphase-matrix` | Native and assistant review passed |
| retrograde-polymer-sheet | `art/source-to-3d/material-icons/v01/retrograde-polymer-sheet` | Native and assistant review passed |
| duplexed-substrate | `art/source-to-3d/material-icons/v01/duplexed-substrate` | Native and assistant review passed |
| tank-light-chasis-wlsk | `art/source-to-3d/material-icons/v01/tank-light-chasis-wlsk` | Native and assistant review passed |
| tank-ammo-casing | `art/source-to-3d/material-icons/v01/tank-ammo-casing` | Native and assistant review passed |
| tank-ammo-reinforced-casing | `art/source-to-3d/material-icons/v01/tank-ammo-reinforced-casing` | Native and assistant review passed |
| tank-ammo-Industrialwaste | `art/source-to-3d/material-icons/v02/tank-ammo-industrialwaste` | Native and assistant review passed |
| tank-ammo-Radioactivewaste | `art/source-to-3d/material-icons/v02/tank-ammo-radioactivewaste` | Native and assistant review passed |
| tank-ammo-universal-explosive | `art/source-to-3d/material-icons/v01/tank-ammo-universal-explosive` | Native and assistant review passed |
| compressed-biohazard-waste | `art/source-to-3d/material-icons/v02/compressed-biohazard-waste` | Native and assistant review passed |
| Seared-fish | `art/source-to-3d/material-icons/v01/seared-fish` | Native and assistant review passed |
| meal | `art/source-to-3d/material-icons/v01/meal` | Native and assistant review passed |
| requisition-slip | `art/source-to-3d/material-icons/v02/requisition-slip` | Native and assistant review passed |
| work-order-slip | `art/source-to-3d/material-icons/v01/work-order-slip` | Native and assistant review passed |
| certified-work-order | `art/source-to-3d/material-icons/v01/certified-work-order` | Native and assistant review passed |
| submitted-evaluation | `art/source-to-3d/material-icons/v01/submitted-evaluation` | Native and assistant review passed |
| risk-assessment | `art/source-to-3d/material-icons/v01/risk-assessment` | Native and assistant review passed |
| risk-assessed-work-order | `art/source-to-3d/material-icons/v01/risk-assessed-work-order` | Native and assistant review passed |
| compliance-packet | `art/source-to-3d/material-icons/v01/compliance-packet` | Native and assistant review passed |
| audit-ready-deliverable | `art/source-to-3d/material-icons/v02/audit-ready-deliverable` | Native and assistant review passed |
| stakeholder-review-summary | `art/source-to-3d/material-icons/v01/stakeholder-review-summary` | Native and assistant review passed |
| liability-contained-report | `art/source-to-3d/material-icons/v02/liability-contained-report` | Native and assistant review passed |
| board-review-docket | `art/source-to-3d/material-icons/v01/board-review-docket` | Native and assistant review passed |
| board-advisory-risk-assessment | `art/source-to-3d/material-icons/v02/board-advisory-risk-assessment` | Native and assistant review passed |
| Cradinal-grametter | `art/source-to-3d/material-icons/v01/cradinal-grametter` | Native and assistant review passed |
| Hydrocoptic-marselvanes | `art/source-to-3d/material-icons/v01/hydrocoptic-marselvanes` | Native and assistant review passed |
| Retro-Encabulator | `art/source-to-3d/material-icons/v01/retro-encabulator` | Native and assistant review passed |
| SpervingArm | `art/source-to-3d/material-icons/v02/spervingarm` | Native and assistant review passed |
| DuctedSpervingArm | `art/source-to-3d/material-icons/v02/ductedspervingarm` | Native and assistant review passed |
| DuplexedSpervingArm | `art/source-to-3d/material-icons/v02/duplexedspervingarm` | Native and assistant review passed |
| Encabulator | `art/source-to-3d/material-icons/v01/encabulator` | Native and assistant review passed |
| TurboEncabulator | `art/source-to-3d/material-icons/v01/turboencabulator` | Native and assistant review passed |
| HyperEncabulator | `art/source-to-3d/material-icons/v01/hyperencabulator` | Native and assistant review passed |
| FramulatedEncabulator | `art/source-to-3d/material-icons/v01/framulatedencabulator` | Native and assistant review passed |
| stone-water-wheel | `art/source-to-3d/material-icons/v01/stone-water-wheel` | Native and assistant review passed |
