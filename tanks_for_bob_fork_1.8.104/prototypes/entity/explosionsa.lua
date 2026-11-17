data:extend({
  {
    type = "explosion",
    name = "explosionnukea",
    localised_name = {"entity-name.explosionnukea"},
    icon = "__base__/graphics/item-group/effects.png",
    icon_size = 64,
    flags = {"not-on-map"},
    hidden = true,
    subgroup = "explosions",

    -- Sound-only helper explosion.
    -- The actual nuclear visuals/scorchmarks are handled in projectile target_effects.
    animations = util.empty_sprite(),

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
  }
})