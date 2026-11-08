# Tanks! for Bob Fork — Factorio 2.1

**Current source: 1.8.102.** The current source is directly buildable from
[`tanks_for_bob_fork_1.8.102`](tanks_for_bob_fork_1.8.102), including the accepted
Campfire, Clay Pit, Pit Kiln and Lumberyard artwork carried forward from the
verified **1.8.100** Mod Portal package. Base Factorio 2.1 is required; Elevated
Rails, Quality, Recycler and Space Age remain optional.

## Progression audit and repairs — 8 November 2026

The [classified audit](docs/compatibility/PROGRESSION_ORDER_AUDIT_2026-11-08.md)
was mapped before gameplay changes. It covers **210 recipes, 88 technologies,
14 ammunition prototypes and 11 guns**, including practical machine capacity
and research/material ancestry. The [complete inventory](docs/compatibility/PROGRESSION_ORDER_INVENTORY_2026-11-08.md)
and [machine-readable baseline](docs/compatibility/PROGRESSION_ORDER_BASELINE_2026-11-08.json)
record the inspected package.

The clear corrections are:

- The **wooden spear starts handcraftable**. Acquiring wood completes its root
  material technology and unlocks sharp-stick ammunition, including both tree
  harvesting and SeaBlock driftwood crafting. No lab or Lumberyard is needed.
- **Saline particulate and bioceramic grit use the Pit Kiln**. Ordinary
  furnaces reject their ingredients because the recipes need separate products
  or multiple item inputs. Existing ingredients, outputs and research stay intact.
- The ammunition audit includes the wooden ammunition it previously missed.
- The source selector, package builder and existing single-job test workflow
  now operate on the actual **2.1 source**, rather than an old 2.0 probe.

### Applied design decisions in 1.8.102

The [follow-up decision record](docs/compatibility/PROGRESSION_DECISIONS_1.8.102.md)
implements the user's choices after that audit. Current source contains
**213 recipes and 90 custom technologies**.

- Poison mine magazines now have a separate upgrade after their specialist
  vehicle branch, chemical munitions and vanilla Land Mines.
- WMD artillery ammunition requires both WMD development and vanilla Artillery;
  the WMD tank keeps its original research timing.
- Removed the redundant stone-tools technology. Starting tools remain available;
  the hovel now follows Meal and Brick directly.
- Cooking Fire retains ordinary cooking as well as advanced cooking.
- Fish Resource Recovery follows Fish Pond and Meal. Campfire/Cooking Fire
  carbonizes fish into coal and ash; Workbench extracts usable crude oil through
  its new pipe outlet. Ash can later become calcified bone dust at its existing
  biological-processing tier.
- Vanilla manufacturing dependencies remain. Oil Processing recognizes crude
  oil production so the fish route can satisfy its discovery while retaining
  Oil Gathering and all downstream chemistry prerequisites.

[Unused equipment and asset usability inventory](docs/compatibility/UNUSED_EQUIPMENT_AND_ASSETS_2026-11-08.md)
is maintained separately. Historical prototypes are assessed rather than
activated or deleted. The alternative super-tank's independent mine-ammunition
branch remains the one unresolved decision from the original audit.

## Build the installable package

```bash
python3 ci/package_mod.py --output dist
```

The command selects the highest versioned source and creates
`tanks_for_bob_fork_1.8.102.zip` plus its SHA-256 file. It checks that every
archived file matches the source and refuses to overwrite an existing package.
Place the ZIP in Factorio's `mods` directory without unpacking it.

This source change does not publish a Mod Portal release. Previously published
versions and tags are retained. The [Mod Portal](https://mods.factorio.com/mod/tanks_for_bob_fork)
last published baseline for this audit is **1.8.100**; the older 1.8.95 GitHub
release targets Factorio 2.0 and is historical.

## Verification

The [single manually dispatched compatibility job](.github/workflows/vanilla-factorio.yml)
uses **Factorio 2.1.24** with Base, Elevated Rails, Recycler, Quality and Space
Age enabled together. Ordinary commits do not dispatch it. No release upload
is performed by this audit workflow.

The checks cover actual source loading, save creation/reload, simulation,
vehicle/ammunition registry checks, server startup, and targeted progression
fixtures. The earlier 1.8.100 baseline was also inspected in **2.1.23** with
explicit base-only and full official-module configurations. See the audit's
verification section for observed results and fixture limits.

A successful load or an ingredient-only graph does not prove a full survival
playthrough, driving/firing every vehicle, two-client multiplayer, or endgame
balance. Seeded machine tests prove their production operations; the actual
wood-acquisition fixtures separately exercise the starting unlock.

[CI instructions](ci/README.md) ·
[Original 1.8.95 logical audit](docs/compatibility/RECIPE_TECH_LOGICAL_AUDIT.md) ·
[Historical official-module checks](docs/compatibility/OFFICIAL_MOD_SUPPORT.md)

## Background

This fork expands the vehicle family with autocannon, flame, mortar/grenade,
rocket, mine and super-tank options, alongside the island-survival, paperwork,
advanced-material and ammunition manufacturing chains. Existing equipment IDs
are preserved for saves; the obsolete stone-tools technology is deliberately
removed. Bob compatibility development remains on its
separate branch.

## Blender texturing and rendering references

**Acknowledgment — Malcolm Riley:** [Unused Renders](https://github.com/malcolmriley/unused-renders) and its [Factorio Blender tutorial wiki](https://github.com/malcolmriley/unused-renders/wiki) are adopted as references for the island-survival 3D asset texturing/rendering workflow. Special thanks to Malcolm Riley for sharing his Blender methods and art resources.

The wiki's **tutorial text is CC0**, while **images and Blender files are CC BY 4.0**, with credit and license link required for reused/adapted artwork. Referencing the methods alone does not mean assets from that repository have been imported. See [texturing workflow and provenance requirements](docs/art/UNUSED_RENDERS_WORKFLOW_AND_CREDITS.md) for techniques, licensing boundaries, and per-asset attribution.

**Existing-art reuse:** We also stage selected CC BY 4.0 [Unused Renders candidate item sprites](art/third-party/unused-renders/README.md) for comparison before redrawing icons. These credited candidates are not yet wired into game prototypes; original art remains active until visually reviewed and tested.

### Additional Factorio art sources

For individual licensed graphics and Blender-reference research, see [snouz's curated catalog](https://github.com/snouz/factorio_free_graphics_for_modders) and our [mixed-license provenance policy](docs/art/FACTORIO_GRAPHICS_SOURCE_REFERENCES.md). The collection is credited to snouz as curator and the respective original artists. [Campfire V6 geometry notes](models/island-survival/refined/README-v6.md) track the ongoing smoothed model work; active sprites are unchanged.

### Repeatable Factorio production-sprite export procedure

Use the [versioned Blender-to-Factorio production export runbook](docs/art/FACTORIO_PRODUCTION_SPRITE_WORKFLOW.md) for every new 3D-derived structure or animation. The [per-asset checklist template](docs/art/FACTORIO_PRODUCTION_ASSET_CHECKLIST_TEMPLATE.md) records mandatory evidence, failures, correction history and approval. The first active instance is the [campfire work order](models/island-survival/blender/CAMPFIRE_PRODUCTION_EXPORT_CHECKLIST.md). **This documents the steps; it does not mark an uncalibrated asset export-ready or replace current sprites.**
