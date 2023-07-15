
data:extend (

{
  {
    type = "explosion",
    name = "explosionnukea",
    localised_name = {"entity-name.explosionnukea"},
    icon = "__base__/graphics/item-group/effects.png",
    icon_size = 64,
    flags = {"not-on-map", "hidden"},
    subgroup = "explosions",
	animations = util.empty_sprite(),
    --light = {intensity = 1, size = 20, color = {r=1.0, g=1.0, b=1.0}},
    smoke = "smoke-fast",
    smoke_count = 1,
    smoke_slow_down_factor = 1,
    
	sound =
	{
        {
          filename = "__tanks_for_bob_fork__/sound/fight/nuclearexplosiona.ogg",
          volume = 1
        }
      }
  },
 }
)