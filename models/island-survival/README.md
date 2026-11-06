# Island survival — low-poly geometry library (first pass)

**21 real, independent 3D meshes** committed as Wavefront `.obj` objects
with a shared `obj/survival-materials.mtl` palette. Geometry was built
from elementary boxes, cylinders, cones, beams, shallow rings and roofs to
establish separate editable primitive parts. There are no borrowed,
AI-rendered or flat image billboards masquerading as 3D.

**Status:** blockout / comparison models, **not** final screen-accurate meshes,
baked textures or replacements for Factorio's existing sprites. The
underlying sprite art remains authoritative. Do not merge these into
the mod package or replace existing in-game sprites without an explicit
visual comparison and approval.

## What's included

| Stage | Models |
| --- | --- |
| Water | `beachpump`, `wood-basin`, `stone-water-wheel`, `solar-boiler`, `primitive-steam-powered-pump`, `steam-condenser` |
| Wood and fire | `growing-plot`, `campfire`, `cooking-fire`, `workbench` |
| Clay and food | `clay-pit`, `fish-pond`, `pit-kiln` |
| Minerals | `quarry`, `calcifier`, `shaler` |
| Research | `thinking-hut`, `pondering-hovel` |
| Industry | `Steam-Compressor`, `tank-assembling-machine`, `tank-ammo-assembling-machine` |

Source sprites for **all 21 models** were checked against repository
filenames. See `designs.json`: each entry includes the specific sprite path,
approximate footprint, stage, object parts and modeling notes. The primitive
positions are an initial estimate of the game tile/selection footprint, **not
a measured pixel-to-vertex reconstruction**.

## View, rebuild, refine

1. In Blender, choose **File → Import → Wavefront (.obj)** and load any
   `obj/<entity-name>.obj`. Keep the MTL in the same directory.
2. Compare the 3D form with `tanks_for_bob_fork_1.8.95/<sprite>` listed
   under that name in `designs.json`. Begin with large silhouettes,
   height, roof angle, inlet/outlet orientation, and color blocking.
3. Refine the mesh in Blender or edit `designs.json` for deterministic
   primitive regeneration. The OBJ uses **X east, Y north, Z up**, with
   nominal scale 1 unit ≈ 1 Factorio tile.
4. With Node.js installed, regenerate with:

   `node tools/build_island_survival_models.mjs`

   Or check whether committed OBJ/MTL files match the JSON generator:

   `node tools/build_island_survival_models.mjs --check`

**Modeling next pass:** import original sprites as image planes; align a
consistent isometric camera, lights and render scale; compare shape contours
and proportions side by side; refine all 21 models as observations warrant.
Exporting refined Blender meshes and rendering new in-game sprites is
deliberately separate from these rough primitive assets.

## Recipe-chain relation

The first-pass meshes include the five repaired 3-ingredient Workbench
structures, the repaired Cooking Fire, and the dedicated fluid-capable Tank
Ammunition Assembler. Their geometry reflects the *intended* mechanical ports
and crafting role, not a claim that their existing 2D sprite art already
shows these fittings.

## Reference texturing and source credits

Follow the [Malcolm Riley / Unused Renders Blender reference workflow](../../docs/art/UNUSED_RENDERS_WORKFLOW_AND_CREDITS.md) when refining island-survival assets. His [tutorial wiki](https://github.com/malcolmriley/unused-renders/wiki) is part of our documented shader, lighting and sprite-rendering references, and he is credited for sharing it. Record file-level provenance and CC BY 4.0 attribution before importing any of his rendered images or Blender files. No third-party assets are added by this documentation change.
