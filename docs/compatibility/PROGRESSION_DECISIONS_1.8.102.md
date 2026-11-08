# Applied progression decisions — 1.8.102

This implements the user's decisions following the
[classified 1.8.101 audit](PROGRESSION_ORDER_AUDIT_2026-11-08.md).
The starting commit is `cf4a7dbe6730e73e6dcc02f3ea5fe75c47149780`.
Factorio 2.1 remains the target and official expansion modules remain optional.

## Decision map

| Prior finding | User decision and resulting behavior |
| --- | --- |
| B1: poison mine magazines before their platform | Dedicated `poison-mine-ammunition` requires `new-munitions`, `modular-tank-research3` and native `land-mine`. It alone unlocks `minepack-poison`. Poison mortar keeps its old timing. |
| B3: WMD artillery ammunition before artillery | Dedicated `wmd-artillery-ammunition` requires WMD tank research (`super-tank-research2`) and native `artillery`. The WMD tank and tank ammunition remain on their original node. |
| B4: redundant stone-tools research | Removed the technology. Starter tool item and handcraft recipe remain. `pondering-hovel` now follows `meal` and `brick`, preserving the useful old ancestry. |
| B5: Cooking Fire loses ordinary cooking | Cooking Fire accepts both `cooking` and `advcooking`; its steam inlet is inactive for recipes that need no fluid. |
| B6: parallel vanilla manufacturing | Confirmed intentional. Existing vanilla science, plastics, circuits, engines and downstream chemistry requirements remain. |
| B7: coal/oil starvation | New `fish-resource-recovery` follows `fish-pond` and `meal`. It unlocks low-throughput fish carbonization and crude-oil extraction before the advanced material chain needs those resources. |
| B8: unused equipment and assets | Assessed in a [separate usability inventory](UNUSED_EQUIPMENT_AND_ASSETS_2026-11-08.md); no historical prototype or art is activated or deleted. |

B2, the alternative super-tank's independent mine-magazine availability, was
not resolved by these instructions. Its existing branch remains unchanged.

## Research and manufacturing

| Research | Prerequisites | Cost | Result |
| --- | --- | --- | --- |
| Fish Resource Recovery | Fish Pond + Meal | 10 cycles of 1 Seared Fish + 1 Meal, 10 s/cycle | Fish Carbonization + Fish Oil Extraction |
| Poison Mine Ammunition | Chemical munitions + specialist mine-vehicle branch + Land Mines | 40 cycles of 1 automation + 1 logistic + 1 military pack, 30 s/cycle | Poison mine magazines |
| WMD Artillery Ammunition | WMD tank development + Artillery | 100 cycles of the same three packs, 30 s/cycle | WMD artillery ammunition |

| Recipe | Inputs | Outputs | Station and duration at its current speed |
| --- | --- | --- | --- |
| Fish Carbonization | 8 raw fish | 1 vanilla coal + 1 fish ash | Campfire: 50 s; Cooking Fire: 25 s |
| Fish Oil Extraction | 10 raw fish | 10 vanilla crude oil | Workbench: about 66.7 s |
| Fish Ash Processing | 3 fish ash | 1 calcified bone dust | Cooking Fire: about 11.7 s |

The first two recipes have no starting coal, oil, steel-barrel or advanced
chemical input. Their burner machines can use wood. The low throughput keeps
normal resource extraction and later industrial processing valuable. Automatic
recycling, productivity and quality are disabled for these material-recovery
recipes, consistent with the existing primitive biological processing rules.

Ash processing is an alternative under the existing `bio-reactive-processing`
technology. The original raw-fish-to-bone-dust recipe remains unchanged. This
gives the requested ash byproduct a use without granting that later mineral
material at the new mid-tier recovery stage.

The Workbench retains its one-tile footprint, burner settings, crafting speed,
three-item capacity and existing graphics. A 100-unit fluid output connects
south in its default orientation. Select Fish Oil Extraction before rotating
the machine toward its adjacent pipe; ordinary solid recipes deactivate the
fluid box. Cooking Fire keeps its existing steam inlet and advanced recipes.

## Oil discovery compatibility

Factorio 2.1's original Oil Processing trigger requires mining a crude-oil
resource. Keeping only that trigger would leave a fish-only oil source unable
to introduce refining on an island without wells. The guarded compatibility
change replaces only that original trigger with native production of one unit
of crude oil. It retains Oil Gathering and every downstream vanilla prerequisite.
An independently replaced trigger from another mod is left alone.

Both a normal pumpjack and the Workbench must satisfy the production trigger;
oil made before Oil Gathering must not bypass its prerequisite. These are
explicit native integration checks. Reference:
[Wube's craft-fluid trigger](https://lua-api.factorio.com/latest/types/CraftFluidTechnologyTrigger.html).

## Existing saves

The native `migrations/1.8.102.lua` file transfers the old shared ammunition
unlock only if the old technology and every prerequisite of the new split
technology are already researched. Missing vehicle, Land Mines or Artillery
research leaves the corresponding magazine locked for its new research node.
Only those two research states and recipes are synchronized. Existing ammunition,
unrelated research and the wooden-material discovery handlers are untouched.

Removal of old stone-tools research is handled by normal prototype migration;
the useful starter recipe remains enabled. The native saved-game fixture also
checks that a pre-existing Workbench keeps its selected solid recipe and stored
ingredients, then accepts its new fluid recipe and output capacity.

## Validation and package

The source contains **213 declared custom recipes and 90 custom technologies**.
The final installable archive contains **573 files**. Package SHA-256:

`d21b17cfa1785cd586fc37afeae6d19f1097e87a81d3b43ed9823544d67b525c`

The final **single-profile suite passed under Factorio 2.1.24 build 87808**:
source/assets, data-stage checks, save creation, 1,200 simulation updates,
native progression, actual previous-package migration and private server
startup. All 14 ammunition declarations and 16 named machine cases passed.
The remote workflow was not dispatched; these are local engine results.

The native fixture passed **93 fresh checks, 11 historical-state setup checks
and 25 migration checks**. Relevant observations:

- Four real Thinking Huts completed Fish Resource Recovery using its actual
  Seared Fish and Meal inputs; research completed at simulation tick 3,120.
- Using wood fuel, Campfire made 2 coal + 2 ash and Cooking Fire made 5 coal +
  5 ash during the bounded run. No coal or oil was seeded into these machines.
- Each of four Workbench orientations completed two extraction cycles and
  delivered 20 crude oil to its correctly positioned adjacent pipe.
- Oil produced before Oil Gathering did not grant Oil Processing. After that
  prerequisite, Workbench production completed it. A separate ordinary
  pumpjack force also produced oil and completed the same technology.
- Cooking Fire cooked ordinary fish with no steam. Fish Resource Recovery
  did not unlock advanced ash processing; only the later biological technology
  did. Three actually manufactured ash were transferred and became one bone dust.
- A real save serialized with the exact prior 1.8.101 ZIP upgraded successfully.
  Eligible old poison/WMD artillery unlocks survived. Missing Land Mines,
  vehicle research or Artillery correctly left the corresponding upgrade locked.
- An old researched stone-tools node was removed while the starter recipe
  stayed available. The old Workbench kept its solid recipe and ingredients,
  then accepted the new fluid recipe and output capacity.

The live registry map has no missing custom recipes or technologies, no
disabled custom recipes without an unlock, no redundant starting unlocks,
no prerequisite cycles, no missing prerequisite references, and no custom
recipe without a compatible crafter. The research-material ancestry diagnostic
also reports no gaps; its scope still excludes proof of full logistics.

Every archive byte matches both the final source and the source snapshot used
by the passing native suite. All **516 prior graphics/sound files** are preserved
byte-for-byte. No previous package file was removed. The ash icon reuses existing
art through prototype layers; no image was generated or replaced.

Tests seed infrastructure, research supplies and machine inputs; they establish
the specified operations and migration, not a complete map playthrough or a
guarantee of every mod combination. The native saved-character join path is
tested; the older offline-player configuration-time wood discovery remains
covered by the focused unit test from the preceding audit.

### Evidence

- [Native production and saved-game assertions](evidence/1.8.102/native-progression.json)
- [Single-profile suite result](evidence/1.8.102/suite-results.json)
- [Package/source identity and artwork preservation](evidence/1.8.102/package-source-verification.json)
- [Current complete recipe/technology inventory](PROGRESSION_ORDER_INVENTORY_1.8.102.md)
- [Machine-readable live-registry map](PROGRESSION_ORDER_1.8.102.json)
