# Unused Renders — candidate asset imports

**Author and artwork credit:** Malcolm Riley, [Unused Renders](https://github.com/malcolmriley/unused-renders), licensed [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Source: https://github.com/malcolmriley/unused-renders.

The following **original rendered PNG assets** were copied unmodified from Malcolm Riley's repository, using the provided **Factorio-ready mipmapped variants**. They are staged as *candidates and references*, **not incorporated into the active mod**, and not approved as replacement icons. No runtime prototype paths were changed.

| Staged file | Exact upstream asset | Intended evaluation | Modifications and use status |
| --- | --- | --- | --- |
| [`pile-charcoal-2.png`](item-mipped/pile-charcoal-2.png) | [Upstream `item/mipped/pile-charcoal-2.png`](https://github.com/malcolmriley/unused-renders/blob/main/item/mipped/pile-charcoal-2.png) | charcoal (item icon candidate) | Unmodified upstream file; staged, not referenced by Factorio |
| [`part-bullet-casings-1.png`](item-mipped/part-bullet-casings-1.png) | [Upstream `item/mipped/part-bullet-casings-1.png`](https://github.com/malcolmriley/unused-renders/blob/main/item/mipped/part-bullet-casings-1.png) | casing (item icon candidate) | Unmodified upstream file; staged, not referenced by Factorio |
| [`pile-ashes-1.png`](item-mipped/pile-ashes-1.png) | [Upstream `item/mipped/pile-ashes-1.png`](https://github.com/malcolmriley/unused-renders/blob/main/item/mipped/pile-ashes-1.png) | campfire ash / future ash item (visual reference) | Unmodified upstream file; staged, not referenced by Factorio |
| [`pile-chunk-wood-chips-1.png`](item-mipped/pile-chunk-wood-chips-1.png) | [Upstream `item/mipped/pile-chunk-wood-chips-1.png`](https://github.com/malcolmriley/unused-renders/blob/main/item/mipped/pile-chunk-wood-chips-1.png) | wood-processing intermediates (visual reference) | Unmodified upstream file; staged, not referenced by Factorio |

## What has and has not been obtained

- The upstream repository contains 431 `item/original` sprites and their 431 `item/mipped` copies, plus fluid and technology graphics; it has no top-level or tracked .blend file in its current repository tree.
- Mipmapped item sprites are complete item render sheets, **not seamless material textures** and **not 3D source meshes**. Do not apply them indiscriminately to mesh UVs.
- Candidate charcoal and casing graphics can be assessed against current item icons before deciding on a replacement. Wood chips and ashes serve as direct visual references unless a matching game item is identified.
- Higher-resolution `item/original` variants are available upstream for more detailed study without redrawing. Fetch exact original source paths as needed, retaining original credit.
- Each reuse or adaptation must record the exact upstream file and link, author, license, what was changed, and the new game path, then confirm rendering and load tests before release.

## Reproduction / verification

Original upstream source: `https://github.com/malcolmriley/unused-renders/tree/main/item/mipped`.

For any of the four paths above, compare byte-for-byte to the same `item/mipped/<filename>` in the upstream repository. These imported assets were created directly from GitHub's base64 file API. The root project credit and extended process documentation are at [`docs/art/UNUSED_RENDERS_WORKFLOW_AND_CREDITS.md`](../../../docs/art/UNUSED_RENDERS_WORKFLOW_AND_CREDITS.md).

This import does **not** grant any rights to Wube's vanilla graphics, and it does not imply that Malcolm Riley endorses this fork.
