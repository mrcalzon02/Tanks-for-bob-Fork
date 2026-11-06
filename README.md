# Tanks! for Bob Fork — Factorio 2.0

A Factorio tank and vehicle expansion originally created to provide stronger firepower against large biter hordes. The fork includes specialized tanks, guns, ammunition, and substantial intermediate-product and technology chains.

**Current version:** `tanks_for_bob_fork_1.8.95.zip` — Factorio **2.0** target, with base game required and official expansion modules optional. [GitHub release](https://github.com/mrcalzon02/Tanks-for-bob-Fork/releases/tag/v1.8.95).

## 1.8.95 recipe-chain repairs and model development

The island-survival production chain now has mechanical fixes for **five
early three-ingredient Workbench recipes** and **two steam-based Cooking Fire
recipes**. The specialized ammunition assembler also has **input and output
fluid connections**. These repairs preserve the existing research
prerequisites and recipe costs.

A new [21-structure primitive 3D model library](models/island-survival/README.md)
includes editable **Wavefront OBJ geometry, materials, and sprite links**.
These are source-controlled visual-comparison models, **not in-game sprite
replacements**. Their primitive proportions must be checked against the
existing art before visual approval.

[See the logical audit and follow-up](docs/compatibility/RECIPE_TECH_LOGICAL_AUDIT.md)
for what was fixed and what still requires manual playtesting.

## Official Factorio compatibility — verified November 5, 2026

**Current automated CI:** exactly **one job and one Factorio 2.0.77 profile**, with Base, Elevated Rails, Quality and Space Age enabled together. This includes static source, recipe, ammunition, vehicle, damage, save creation, benchmark and server-startup checks. [View current checks](https://github.com/mrcalzon02/Tanks-for-bob-Fork/actions/workflows/vanilla-factorio.yml).

Previously, [12 Factorio 2.0/2.1 profiles passed](https://github.com/mrcalzon02/Tanks-for-bob-Fork/actions/runs/42136857118). Those results are retained **for historical reference only**; current CI does not retest all twelve or Factorio 2.1.

| Official module | Factorio 2.0.77 | Factorio 2.1.23 | Notes |
| --- | --- | --- | --- |
| `core` | Built-in | Built-in | Required by Factorio |
| `base` | **Pass** | **Pass*** | The fork requires base |
| `elevated-rails` | **Pass** | **Pass*** | Optional, individually tested |
| `quality` | **Pass** | **Pass*** | Optional, individually tested |
| `recycler` | Part of Quality | **Pass*** | Standalone official module in 2.1 |
| `space-age` | **Pass** | **Pass*** | Full expansion profile tested |
| Space Age **without Quality** | Not separately tested | **Pass*** | Explicit 2.1 test profile |

\* **Factorio 2.1 test-only probe:** CI updates the `factorio_version` metadata **only in a disposable copy** to exercise the 2.1 engine. This release's actual `info.json` specifies **Factorio 2.0**, and the downloadable package is **not** a published 2.1 build. All these checks run with **only this fork and official mods**; they do not certify Bob's Enemies, AAI, Mechanicus, or other third-party mods.

### Historical 12-profile results (not run by current CI)

| Engine | Official mods enabled besides `core` |
| --- | --- |
| 2.0.77 | `base` |
| 2.0.77 | `base` + `elevated-rails` |
| 2.0.77 | `base` + `quality` |
| 2.0.77 | `base` + `elevated-rails` + `quality` |
| 2.0.77 | `base` + `elevated-rails` + `quality` + `space-age` |
| 2.1.23 | `base` |
| 2.1.23 | `base` + `elevated-rails` |
| 2.1.23 | `base` + `recycler` |
| 2.1.23 | `base` + `quality` + `recycler` |
| 2.1.23 | `base` + `elevated-rails` + `quality` + `recycler` |
| 2.1.23 | `base` + `elevated-rails` + `recycler` + `space-age` |
| 2.1.23 | `base` + `elevated-rails` + `quality` + `recycler` + `space-age` |

### What is actually tested

| Audit | Observed result | Scope |
| --- | --- | --- |
| Active source registry | **210 recipes / 88 technologies** present | Factorio data stage + source declaration manifest |
| Disabled mod recipes lacking technology unlock | **0** in the source-declared manifest | Does not prove end-to-end research feasibility |
| Recipe supply closure | **210/210** optimistically reachable | Diagnostic only; ignores research, machines, power, terrain and logistics |
| Vehicle prototypes | **13** variants inspected | Prototype registry and item-placement relationships |
| Mounted gun slots | **26/26** link to ammunition categories | Registry match; not real firing |
| Declared ammunition | **13/13** prototype and crafting output checks | Includes custom and vanilla-category ammunition |
| Spawning/simulation | **8** vehicles spawned after tick **300** | Real headless simulation, 1,200 ticks |
| Physical damage | **Passed** at tick **600** | Actual engine hitpoint response: **1,250 → 0** |
| Tank ammunition inventory | **7/7** surviving tested vehicles accepted assigned ammo at tick **900** | The eighth vehicle was intentionally destroyed in the damage check |
| Dedicated server | **Pass** for the current full-expansion profile; earlier 12-profile baseline | Private headless server startup, not two connected clients |
| Source/asset audit | **Pass** | Active Lua module paths, case-sensitive image references, duplicates |

**Not yet established:** a player driving each tank; firing projectiles and consuming ammo; explosions, stream rendering and turret sprite alignment in the graphical client; a complete technology-gated production path; recall/teleport GUI behavior; two-client multiplayer; migration of older saves; and large-fleet balance. In `control.lua`, the recall event registrations are currently commented out, so the existence of recall functions is **not** proof that recall works.

### Compatibility repairs already merged

- Repaired case-sensitive Lua imports and artwork references, and restored the original matching high-resolution turret asset.
- Corrected missing recipe icon references and duplicate recipe-category definitions.
- Adjusted affected Factorio 2.1 prototype helpers/properties for engine probe compatibility.
- Added conditional Quality / Recycler / Space Age waste-loop protections.
- Added independent, repeatable official-mod Factorio CI suites; no Tech Priests dependency.

### Reports, logs, and source

- [Current one-job compatibility results](https://github.com/mrcalzon02/Tanks-for-bob-Fork/actions/workflows/vanilla-factorio.yml)
- [Official modules: full matrix, test method, version caveats](docs/compatibility/OFFICIAL_MOD_SUPPORT.md)
- [Current-state source and functionality audit](docs/compatibility/CURRENT_STATE_AUDIT.md)
- [Reusable CI workflow](.github/workflows/vanilla-factorio.yml)
- [Release notes](docs/releases/v1.8.95.md)

## Factorio Mod Portal distribution

Version **1.8.95** is built and uploaded to the [Factorio Mod Portal](https://mods.factorio.com/mod/tanks_for_bob_fork) by the same **single** CI job after the full official-expansion Factorio 2.0.77 smoke test passes. Uploads require the private GitHub Actions secret `FACTORIO_MOD_UPLOAD_KEY`. Existing published versions are never overwritten.

## Installing

Download **`tanks_for_bob_fork_1.8.95.zip`** from the GitHub release and place it in Factorio's `mods` directory without unpacking it. For this package use Factorio 2.0 and enable the fork alongside `base`; Elevated Rails, Quality, and Space Age remain optional. A corresponding SHA-256 checksum is published with the ZIP.

## Background

The original motivation was stronger tank firepower for difficult biter scenarios. This fork expands the vehicle family with autocannon, flame, mortar/grenade, rocket, mine and super-tank options, plus added ammunition, intermediates, research, and manufacturing paths. Gameplay features and historical descriptions in the mod folder's README do not supersede the verified test limitations above.

## Blender texturing and rendering references

**Acknowledgment — Malcolm Riley:** [Unused Renders](https://github.com/malcolmriley/unused-renders) and its [Factorio Blender tutorial wiki](https://github.com/malcolmriley/unused-renders/wiki) are adopted as references for the island-survival 3D asset texturing/rendering workflow. Special thanks to Malcolm Riley for sharing his Blender methods and art resources.

The wiki's **tutorial text is CC0**, while **images and Blender files are CC BY 4.0**, with credit and license link required for reused/adapted artwork. Referencing the methods alone does not mean assets from that repository have been imported. See [texturing workflow and provenance requirements](docs/art/UNUSED_RENDERS_WORKFLOW_AND_CREDITS.md) for techniques, licensing boundaries, and per-asset attribution.
