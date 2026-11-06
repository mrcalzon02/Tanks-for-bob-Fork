# Factorio art pipeline — Malcolm Riley / Unused Renders

## Credit and authoritative upstream resources

**Credit: Malcolm Riley**, creator of [Unused Renders](https://github.com/malcolmriley/unused-renders) and the [Unused Renders Factorio/Blender tutorial wiki](https://github.com/malcolmriley/unused-renders/wiki). Thank you for publicly sharing these tutorials and render resources.

- Upstream source: https://github.com/malcolmriley/unused-renders
- Tutorial reference: https://github.com/malcolmriley/unused-renders/wiki
- Upstream asset license: https://github.com/malcolmriley/unused-renders/blob/main/LICENSE
- License deed: https://creativecommons.org/licenses/by/4.0/

The author states on the wiki that **tutorial text is CC0**, whereas **tutorial images and Blender files are CC BY 4.0**. The upstream render repository is also licensed **CC BY 4.0**. Attribution is appropriate regardless of whether required for a technique-only workflow. These terms do **not** mean Wube's base Factorio art is CC BY 4.0; base-game art follows its own rights and must not be copied into this repo merely because it is used as a visual target.

## Approved pipeline: reference, model, texture, render, compare

1. **Identify the actual source sprite and entity footprint.** Record the original mod path, idle and active visuals and selection/collision bounds. It is the visual target, not a texture to blindly paste onto 3D.
2. **Model only camera-visible geometry.** Begin with silhouette and major material boundaries. Favor separately editable parts (stone, bark, exposed wood, ash, glow); do not add unseen interior mechanisms.
3. **Generate appropriate procedural materials and textures.** Follow Malcolm Riley's wiki for Blender shaders/geometry nodes where applicable (e.g. surface break-up and detailed material response). For the campfire: varied stone tone and roughness, bark grain, exposed wood rings, ash/char and emissive embers. Avoid uniform noise and details invisible in the final camera.
4. **Match the Factorio render language.** Test a Nauvis-like HDRI or suitably recreated environment, controlled edge highlights, and ambient occlusion in recesses. These are specific rendering principles highlighted in the Unused Renders wiki, not a claim that every render must literally reuse an upstream HDRI.
5. **Keep static geometry and animated/emissive layers separate.** Render idle and working states at the same camera position, with proper alpha/background and original pixel scale.
6. **Compare to the mod's source sprites.** Inspect side by side both at working resolution and native 64px (or the actual assigned sprite dimensions), adjust silhouette, proportion, value, hue and level of detail until recognizable.
7. **Verify license/provenance before shipping third-party resources.** Store upstream URL, filename or commit, author, license link, modifications and destination path in the per-asset log below. Do not describe reference-only study as asset incorporation.

### Application to the campfire

The V4 rough model and V5 texture experimentation precede this new reference integration. **No specific Unused Renders texture or Blender file has yet been copied into the campfire or this repository by this documentation change.** Its tutorial methods will inform subsequent refinement: natural bark and cut ends, less uniformly faceted stones, physically coherent material roughness, and matching the original sprite's directional highlights.

## Provenance and attribution ledger

Create one entry for **each** upstream image/mesh/material actually incorporated or adapted, and update it whenever the asset changes. Example fields (do not treat this template as an existing import):

| Our asset/path | Source author | Original source URL + exact file/revision | License URL | Transformations | Credit status |
| --- | --- | --- | --- | --- | --- |
| _(no imported Unused Renders assets recorded yet)_ | — | — | — | Reference methodology only | General credit here and in root README |

**Required credit text for asset reuse (adapt specifics):**

> Artwork based on "[original file name]" from **Unused Renders** by **Malcolm Riley** ([source](https://github.com/malcolmriley/unused-renders)), licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Adapted for Tanks for Bob Fork: [specific changes].

Credit must remain with distributed work (README, credits/NOTICE file, or linked in-mod credits as appropriate), identify modifications, link the material and the license, and not imply endorsement. Do not silently convert licensed images into "original" textures. The project repository's existing license is unchanged by this reference-credit addition.

## Existing-asset-first reuse (asset library)

Before making any replacement item icon from scratch, search the [Unused Renders catalog](https://github.com/malcolmriley/unused-renders/tree/main/item) and compare the exact candidate at native game resolution. The available catalog contains finished PNG renders and mipmapped item sprite sheets. Copy only art with appropriate semantic and visual fit, preserve the exact CC BY 4.0 source credit, and test in Factorio before switching a live reference.

Four unmodified CC BY 4.0 assets are staged at [`art/third-party/unused-renders/item-mipped/`](../../art/third-party/unused-renders/item-mipped) for charcoal, casing, ash and wood-chip studies. See [their provenance ledger](../../art/third-party/unused-renders/README.md). These are **not** live sprite replacements or 3D mesh source assets.
