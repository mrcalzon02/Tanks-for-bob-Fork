# Tanks! for Bob Fork 1.8.95

**Factorio 2.0**, original official modules optional. This version repairs
the early island/SeaBlock survival recipe bottlenecks discovered in the
[logical audit](https://github.com/mrcalzon02/Tanks-for-bob-Fork/blob/main/docs/compatibility/RECIPE_TECH_LOGICAL_AUDIT.md).

## Recipe chain and machinery repairs

- The primitive **workbench** can now accept **3 different item ingredients**
  (previously 2). This enables the three-ingredient recipes for
  `clay-pit`, `wood-basin`, `fish-pond`, `quarry`, and
  `primitive-steam-powered-pump`.
- **Cooking Fire** has a north-side steam input. The `rendered-organics`
  and `steam-meal` recipes can now use the actual steam they require,
  restoring the source of the organic branch of encabulation ingredients.
- The dedicated **Tank Ammunition Assembler** has north fluid input and south
  fluid output ports for `Rubberized-timber` and
  `tank-ammo-industrial-coke` instead of relying on a different assembler.
- A nine-recipe machine/category/fluids feasibility check is included
  inside the existing single Factorio CI profile.

The changes do **not** bypass existing technology locks, alter recipe
ingredients/amounts, or change the expensive progression design.

## Testing and limits

Current automated verification remains **one GitHub Actions job, one Factorio
2.0.77 full-official-expansion profile** (Base + Elevated Rails + Quality +
Space Age). The engine is used to verify loading, save creation, prototype
registration, 1,200 ticks, dedicated server startup, and recipe/machine
configuration checks.

A passing engine smoke test is **not** proof of full manual survival
playthrough, fluid transport, research progression or GUI appearance.
The previous 2.1 probes were temporary metadata tests; this release
is Factorio **2.0** only.

## Initial 3D model library

21 editable, low-poly reference meshes in Wavefront OBJ format are in the
[repository's island-survival model library](https://github.com/mrcalzon02/Tanks-for-bob-Fork/tree/main/models/island-survival).
They are separate developmental geometry and **are not bundled into the game
ZIP or used to replace game sprites**.
