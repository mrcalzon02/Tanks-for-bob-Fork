# Pump identity and actual progression use

Checked against source 1.8.103 at `7290824bf43711d0bb31bd8e2969c51459864f91`
on 2026-11-15, after the owner questioned the bucket-wheel direction.

| Structure | Actual prototype/function | Use in progression | Art consequence |
| --- | --- | --- | --- |
| Beach Pump (`beachpump`) | `offshore-pump`; shoreline water source, 0.01 pumping_speed, void energy; one south outlet | Root Beach Pump research unlocks its recipe; Wood Basin follows | Shoreline intake/outlet and correct native underwater layers |
| Stone Water Wheel (`stone-water-wheel`) | `offshore-pump`; shoreline water source, 0.5 pumping_speed, void energy; one south outlet | Wood Basin + Brick unlock its technology/recipe; Solar Boiler requires it | Separate intake asset. Any retained lifting buckets must remain upright; V1/V2 studies are unaccepted |
| Primitive Steam-Powered Pump (`primitive-steam-powered-pump`) | `pump`; transfers existing fluid from south input `(0,+0.75)` to north output `(0,-0.75)`; pumping_speed 1, chemical burner, 20 kW, one fuel slot, no fluid filter | Solar Boiler unlocks its technology/recipe; Steam Condenser requires it plus Crude Glass | Actual enclosed pipe pump with piston, rod, flywheel and fixed 1x2 ports. No lifting buckets and no invented third external steam port |

These are three distinct entity IDs, recipes and research steps. The current
pipe-pump art still uses vanilla pump animation in active `entities.lua`.
Its original dedicated 3D candidate already has a verified 68-frame artifact:
[run 43183442468](https://github.com/mrcalzon02/Dens-Mortis/actions/runs/43183442468),
artifact `13927757032`, archive SHA256
`169e42b5a833a85408b1fcc1a2c9c9bb4907b162812404b6c580319ed44a9ff0`.
Expected saved master SHA256:
`1c6e1b23d0ec1472d1c25303416b97b827735298f9a34724beecc7e085d9cd6c`.
Recover and inspect it before rebuilding; artifact success does not grant visual
approval or prove active integration.

Sources: active `prototypes/entity/entities.lua`, `prototypes/recipe/recipe.lua`,
`prototypes/technology/technology.lua`, and the existing pump V1 README/contract.
No recipe, research, energy or fluid behavior is changed by this audit.
