data:extend (
{
-- Special  
--teleport-effect
 {
    type = "explosion",
    name = "pre-teleport-effect",
    flags = {"not-on-map"},
    animations =
    {
      {
        filename = "__tanks_for_bob_fork__/graphics/entity/teleport/teleport-effect.png",
        priority = "extra-high",
        width = 48,
        height = 64,
        frame_count = 1,
        line_length = 10,
        --shift = {-0.56, -0.96},
        animation_speed = 0.5
      }
    },
  },
--teleport-effect
 {
    type = "explosion",
    name = "teleport-effect",
    flags = {"not-on-map"},
    animations =
    {
      {
        filename = "__tanks_for_bob_fork__/graphics/entity/teleport/teleport-effect.png",
        priority = "extra-high",
        width = 48,
        height = 64,
        frame_count = 100,
        line_length = 10,
        --shift = {-0.56, -0.96},
        animation_speed = 0.5
      }
    },
    light = {intensity = 1, size = 50},
    sound =
    {
      aggregation =
      {
        max_count = 1,
        remove = true
      },
      variations =
      {
        {
          filename = "__base__/sound/fight/old/laser.ogg",
          volume = 0.8
        },
      }
    },
  },
-- tank-assembly
	{
    type = "assembling-machine",
    icon_size = 64,
    name = "tank-assembling-machine",
    icon = "__tanks_for_bob_fork__/graphics/icons/tank-assembling-machine.png",
    flags = {"placeable-neutral","placeable-player", "player-creation"},
    minable = {hardness = 0.2, mining_time = 0.5, result = "tank-assembling-machine"},
    max_health = 300,
    corpse = "big-remnants",
    dying_explosion = "medium-explosion",
    resistances = 
    {
      {
        type = "fire",
        percent = 95
      }
    },
    open_sound = { filename = "__base__/sound/machine-open.ogg", volume = 0.85 },
    close_sound = { filename = "__base__/sound/machine-close.ogg", volume = 0.75 },
    working_sound =
    {
      sound = {
        {
          filename = "__base__/sound/assembling-machine-t3-1.ogg",
          volume = 0.8
        },
        {
          filename = "__base__/sound/assembling-machine-t3-2.ogg",
          volume = 0.8
        },
      },
      idle_sound = { filename = "__base__/sound/idle1.ogg", volume = 0.6 },
      apparent_volume = 1.5,
    },
    collision_box = {{-1.2, -1.2}, {1.2, 1.2}},
    selection_box = {{-1.5, -1.5}, {1.5, 1.5}},
    animation =
    {
      filename = "__tanks_for_bob_fork__/graphics/entity/tank-assembling-machine/tank-assembling-machine.png",
      priority = "high",
      width = 142,
      height = 113,
      frame_count = 32,
      line_length = 8,
      shift = {0.84, -0.09}
    },
    crafting_categories = {"tank-crafting"},
    crafting_speed = 1.00,
    energy_source =
    {
      type = "electric",
      usage_priority = "secondary-input",
      emissions = 0.05 / 3.5
    },
    energy_usage = "250kW",
    ingredient_count = 6,
    module_slots = 4,
    allowed_effects = {"consumption", "speed", "productivity", "pollution"}
  },
-- munition maker
	{
    type = "assembling-machine",
    name = "tank-ammo-assembling-machine",
    icon = "__tanks_for_bob_fork__/graphics/icons/tank-ammo-assembling-machine.png",
    icon_size = 64,
    flags = {"placeable-neutral","placeable-player", "player-creation"},
    minable = {hardness = 0.2, mining_time = 0.5, result = "tank-ammo-assembling-machine"},
    max_health = 450,
    corpse = "big-remnants",
    dying_explosion = "medium-explosion",
    resistances = 
    {
      {
        type = "fire",
        percent = 95
      }
    },
    open_sound = { filename = "__base__/sound/machine-open.ogg", volume = 0.85 },
    close_sound = { filename = "__base__/sound/machine-close.ogg", volume = 0.75 },
    working_sound =
    {
      sound = {
        {
          filename = "__base__/sound/assembling-machine-t3-1.ogg",
          volume = 0.8
        },
        {
          filename = "__base__/sound/assembling-machine-t3-2.ogg",
          volume = 0.8
        },
      },
      idle_sound = { filename = "__base__/sound/idle1.ogg", volume = 0.6 },
      apparent_volume = 1.5,
    },
    collision_box = {{-1.2, -1.2}, {1.2, 1.2}},
    selection_box = {{-1.5, -1.5}, {1.5, 1.5}},
    --fast_replaceable_group = "assembling-machine",
    animation =
    {
      filename = "__tanks_for_bob_fork__/graphics/entity/tank-assembling-machine/tank-assembling-machine.png",
      priority = "high",
      width = 142,
      height = 113,
      frame_count = 32,
      line_length = 8,
      shift = {0.84, -0.09}
    },
    crafting_categories = {"tank-ammo-component"},
    crafting_speed = 1.00,
    energy_source =
    {
      type = "electric",
      usage_priority = "secondary-input",
      emissions = 0.05 / 3.5
    },
    energy_usage = "175kW",
    ingredient_count = 6,
    module_slots = 1,
    allowed_effects = {"consumption", "speed", "productivity", "pollution"}
  },
-- tank-flame-thrower-explosion
	{
	    type = "flame-thrower-explosion",
	    name = "tank-flame-thrower-explosion",
	    flags = {"not-on-map"},
	    animation_speed = 1,
	    animations =
	    {
	      {
	        filename = "__base__/graphics/entity/flamethrower-fire-stream/flamethrower-explosion.png",
	        priority = "extra-high",
	        width = 64,
	        height = 64,
	        frame_count = 64,
		      scale = 1.5,
	        line_length = 8
	      }
	    },
	    light = {intensity = 0.4, size = 16},
	    slow_down_factor = 0.98,
	    smoke = "smoke-fast",
	    smoke_count = 1,
	    smoke_slow_down_factor = 0.95,
	    damage = 
	    {	
	    	amount = 1.50, 
	    	type = "fire"
	    }
  },
-- massive-scorchmark
	{
    type = "corpse",
    name = "massive-scorchmark",
    icon = "__base__/graphics/icons/small-scorchmark.png",
    icon_size = 64,
    flags = {"placeable-neutral", "not-on-map", "placeable-off-grid"},
    collision_box = {{-1.5, -1.5}, {1.5, 1.5}},
    collision_mask = {"doodad-layer", "not-colliding-with-itself"},
    selection_box = {{-1, -1}, {1, 1}},
    selectable_in_game = false,
    time_before_removed = 60 * 60 * 10, -- 10 minutes
    final_render_layer = "ground-patch-higher2",
    subgroup = "remnants",
    order="d[remnants]-b[scorchmark]-a[small]",
    animation =
    {
--      sheet=
--      {
        width = 128,
        height = 92,
		    scale = 5,
        frame_count = 1,
        direction_count = 1,
        filename = "__base__/graphics/entity/scorchmark/small-scorchmark.png",
        variation_count = 3
--      }
    },
    ground_patch =
    {
      sheet =
      {
        filename = "__base__/graphics/entity/scorchmark/small-scorchmark.png",
        width = 128,
        height = 92,
        line_length = 4,
        shift = util.by_pixel(0, 2),
        variation_count = 4,
        hr_version =
        {
          filename = "__base__/graphics/entity/scorchmark/hr-small-scorchmark.png",
          width = 256,
          height = 182,
          line_length = 4,
          shift = util.by_pixel(0, 2),
          variation_count = 4,
          scale = 5.0
        }
      }
    },
    ground_patch_higher =
    {
      sheet =
      {
        filename = "__base__/graphics/entity/scorchmark/small-scorchmark-top.png",
        width = 34,
        height = 28,
        line_length = 4,
        variation_count = 4,
        shift = util.by_pixel(0, -2),
        hr_version =
        {
          filename = "__base__/graphics/entity/scorchmark/hr-small-scorchmark-top.png",
          width = 68,
          height = 54,
          line_length = 4,
          shift = util.by_pixel(0, -2),
          variation_count = 4,
          scale = 5.0
        }
      }
    }
  },
-- land-mine-poison
  {
    type = "land-mine",
    icon_size = 64,
    name = "land-mine-poison",
    icon = "__base__/graphics/icons/land-mine.png",
    flags =
    {
      "placeable-player",
      "placeable-enemy",
      "player-creation",
      "placeable-off-grid"
    },
    minable = {mining_time = 1, result = "land-mine"},
    max_health = 15,
    corpse = "small-remnants",
    collision_box = {{-0.4,-0.4}, {0.4, 0.4}},
    selection_box = {{-0.5, -0.5}, {0.5, 0.5}},
    dying_explosion = "explosion-hit",
    picture_safe =
    {
      filename = "__base__/graphics/entity/land-mine/land-mine.png",
      priority = "medium",
      width = 32,
      height = 32
    },
    picture_set =
    {
      filename = "__base__/graphics/entity/land-mine/land-mine-set.png",
      priority = "medium",
      width = 32,
      height = 32
    },
    trigger_radius = 3.5,
    action =
    {
      type = "direct",
      action_delivery =
      {
        type = "instant",
        source_effects =
        {
          {
            type = "nested-result",
            affects_target = true,
            action =
            {
              type = "area",
              radius = 6,
              collision_mask = { "player-layer" },
              action_delivery =
              {
                type = "instant",
                target_effects = 
				        {
                  type = "damage",
                  damage = { amount = 300, type = "explosion"}
                },
              }
            },
          },
          {
        		type = "create-entity",
        		entity_name = "poison-cloud"
          },
          {
        		type = "damage",
        		damage = { amount = 10, type = "poison"}
          }
        }
      }
    },
  },
-- lazer-cloud
  {
    type = "trivial-smoke",
    name = "lazer-cloud",
    flags = {"not-on-map"},
    show_when_smoke_off = true,
    animation =
    {
      filename = "__base__/graphics/entity/cloud/cloud-45-frames.png",
      priority = "low",
      width = 256,
      height = 256,
      frame_count = 45,
      animation_speed = 3,
      line_length = 7,
      scale = 3,
    },
    slow_down_factor = 0,
    wind_speed_factor = 0,
    cyclic = true,
    duration = 60 * 9,
    fade_away_duration = 60 * 9,
    spread_duration = 40,
    color = { r = 0.2, g = 0.2, b = 0.9 },
    action =
    {
      type = "direct",
      action_delivery =
      {
        type = "instant",
        target_effects =
        {
          type = "nested-result",
          action =
          {
            type = "area",
            radius = 11,
            entity_flags = {"breaths-air"},
            action_delivery =
            {
              type = "instant",
              target_effects =
              {
                type = "damage",
                damage = { amount = 15, type = "laser"}
              }
            }
          }
        }
      }
    },
    action_frequency = 30
  },
-- poison-cloud-2
  {
    type = "smoke-with-trigger",
    name = "poison-cloud-2",
    flags = {"not-on-map"},
    show_when_smoke_off = true,
    animation =
    {
      filename = "__base__/graphics/entity/cloud/cloud-45-frames.png",
      priority = "low",
      width = 256,
      height = 256,
      frame_count = 45,
      animation_speed = 0.5,
      line_length = 7,
      scale = 3,
    },
    slow_down_factor = 0,
    affected_by_wind = false,
    cyclic = true,
    duration = 60 * 20,
    fade_away_duration = 2 * 60,
    spread_duration = 10,
    color = { r = 0.2, g = 0.9, b = 0.2 },
    action =
    {
      type = "direct",
      action_delivery =
      {
        type = "instant",
        target_effects =
        {
          type = "nested-result",
          action =
          {
            type = "area",
            radius = 11,
            entity_flags = {"breaths-air"},
            action_delivery =
            {
              type = "instant",
              target_effects =
              {
                type = "damage",
                damage = { amount = 65, type = "poison"}
              }
            }
          }
        }
      }
    },
    action_frequency = 30
  },
-- Bullet hit sound
  {
    type = "explosion",
    name = "auto-cannon-hit",
    flags = {"not-on-map"},
    animations =
    {
      {
        filename = "__base__/graphics/entity/explosion-gunshot/explosion-gunshot.png",
        priority = "extra-high",
        width = 34,
        height = 38,
        frame_count = 13,
        animation_speed = 1.5,
        shift = {0, 0}
      }
    },
    rotate = true,
    light = {intensity = 1, size = 10},
    smoke = "smoke-fast",
    smoke_count = 1,
    smoke_slow_down_factor = 1,
    sound =
    {
      filename = "__tanks_for_bob_fork__/sound/fight/auto-cannon-hit.ogg",
      volume = 1.0
      
    }
  },
}
)
