# Cooking Fire V2 — active Factorio 2.1 package promotion

**Mod package:** `tanks_for_bob_fork_1.8.102/` (actual active 2.1 tree).
**Prototype:** `assembling-machine/cooking-fire`, preserving the 3×3 tile footprint,
burner, cooking/advcooking categories, recipes and original north steam input.
**Artwork:** byte-identical 256px idle and working four-way atlases (16 frames,
8 FPS, 45° model capture), plus 64/128 source atlases and 64px icon.
No Blender rerender or model rework is performed during this promotion.

The earlier standalone deployment to `tanks_for_bob_fork_1.8.95/`
was *not* a current 2.1 release because that folder declares Factorio 2.0.
The one-profile 2.1.24 engine audit exposed the issue by checking the actual
selected 1.8.102 source, rather than the historical art folder.

The active `data-final-fixes.lua` retains the existing workbench V8 one-tile
replacement and requires `prototypes.generated_graphics.cooking-fire-v2-production`.
The V2 attachment strips only the obsolete overlaid single-frame animation from
the prior working visualisation; lighting is retained. It also promotes the
accepted item/entity icon. Production game logic is not modified.

**Verification:** `ci/data_audit.lua` asserts all four directional active/idle
frames, file targets, animation speed, icon, burner and north steam input.
Actual Factorio 2.1 native-engine results must be checked before claiming
runtime acceptance. Do not infer them from Lua-only probes.

## Factorio 2.1 native verification — complete

The corrected active 1.8.102 package passed official **Factorio 2.1.24**
`space-age-full` suite in [Actions run 42893564032](https://github.com/mrcalzon02/Tanks-for-bob-Fork/actions/runs/42893564032):
static audit PASS, data-stage Cooking Fire sprite and 3x3 north fluid-port
assertions PASS, map creation PASS, 1200-tick benchmark PASS, progression
runtime PASS, dedicated-server smoke PASS, 1/1 profile passed.
This is source/native runtime integration acceptance, **not** proof of
Mod Portal publication or human visual approval of Fish Pond V1.
