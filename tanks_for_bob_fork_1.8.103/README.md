# Tanks! for Bob Fork 1.8.102

For **Factorio 2.1**. Only the base game is required; official expansion modules
remain optional. This package retains the accepted artwork from 1.8.100.

## Progression corrections

- Make the wooden spear by hand from the start.
- Acquire wood by harvesting, crafting driftwood or receiving it to complete
  the root Wooden Ammunition technology and unlock sharp-stick ammunition.
  No laboratory research or Lumberyard is required for this first weapon.
- Make saline particulate and bioceramic grit in the existing **Pit Kiln**.
  Ordinary furnaces cannot accommodate these recipes' ingredients/products.
- Existing saves retain a previously researched wooden-ammunition unlock; the
  weapon's starting recipe is made available on configuration change.

## Applied progression decisions

- Poison mine magazines require chemical munitions, the specialist mine-vehicle
  branch and vanilla Land Mines through their own upgrade technology.
- WMD artillery ammunition has its own technology requiring WMD development
  and vanilla Artillery. The WMD tank retains its original research stage.
- Stone tools remain available from the start. Their redundant technology is
  removed; the hovel follows Meal and Brick directly.
- Cooking Fire keeps ordinary cooking as well as advanced cooking.
- Fish Resource Recovery follows Fish Pond and Meal, costing 10 Seared Fish
  and 10 Meals across 10 research cycles of 10 seconds.

| Recipe | Inputs | Outputs | Machine |
| --- | --- | --- | --- |
| Fish Carbonization | 8 raw fish | 1 coal + 1 fish ash | Campfire or Cooking Fire |
| Fish Oil Extraction | 10 raw fish | 10 crude oil | Workbench, with output pipe |
| Fish Ash Processing | 3 fish ash | 1 calcified bone dust | Cooking Fire; later Bio-reactive Processing research |

Carbonization takes 50 seconds in Campfire or 25 seconds in Cooking Fire.
Oil extraction takes about 66.7 seconds in Workbench. These machines still
need burner fuel; wood is sufficient, so the recovery routes need no starting
coal or oil. The Workbench's outlet faces south in its default orientation and
rotates with the machine. Solid recipes remain available.

Vanilla manufacturing prerequisites remain. Oil Processing accepts crude oil
production from either a pumpjack or Workbench after Oil Gathering. Plastics,
circuits and later refining still require their normal vanilla research.

Existing saves keep a previously unlocked poison-mine or WMD-artillery recipe
only when its newly explicit prerequisites are already researched. Otherwise
the corresponding new upgrade remains available for research. Existing items
and unrelated research are preserved.

## Audit and source

[Complete classified audit](https://github.com/mrcalzon02/Tanks-for-bob-Fork/blob/main/docs/compatibility/PROGRESSION_ORDER_AUDIT_2026-11-08.md)

[Applied decisions and test evidence](https://github.com/mrcalzon02/Tanks-for-bob-Fork/blob/main/docs/compatibility/PROGRESSION_DECISIONS_1.8.102.md)

[Unused equipment and assets](https://github.com/mrcalzon02/Tanks-for-bob-Fork/blob/main/docs/compatibility/UNUSED_EQUIPMENT_AND_ASSETS_2026-11-08.md)

[Current source and build instructions](https://github.com/mrcalzon02/Tanks-for-bob-Fork)

Place the versioned ZIP in Factorio's mods directory without unpacking it.
