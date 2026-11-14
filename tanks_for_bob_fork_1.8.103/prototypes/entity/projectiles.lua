local WMDexorange = settings.startup["WMD1"].value
-- Balance pass: projectile damage/radius values trimmed toward roughly +10% over comparable vanilla roles.
-- WMDexorange is retained for startup-setting compatibility, but WMD blast radii below are capped to vanilla-like roles.
require("prototypes.entity.explosionsa")
data:extend(
{
 --50mm-Mortar
 {
    type = "projectile",
    name = "50mm-projectile",
    flags = {"not-on-map"},
    acceleration = 0.08,

    action =
    {
      {
        type = "direct",
        action_delivery =
        {
          type = "instant",
          target_effects =
          {
            {
              type = "create-entity",
              entity_name = "big-explosion",
              offset_deviation = { {-4,-4},{4,4}},
            },
            {
              type = "create-sticker",
              sticker = "slowdown-sticker"
            },
          }
        }
      },
      {
        type = "area",
--        perimeter = 6,
        radius = 6,
        action_delivery =
        {
          type = "instant",
          target_effects =
          {
            {
              type = "damage",
              damage = {amount = 110, type = "explosion"}
            },
          }
        }
      }
    },
    light = {intensity = 0.5, size = 8},
    animation =
    {
      filename = "__tanks_for_bob_fork__/graphics/entity/Cluster/Cluster.png",
      frame_count = 1,
      width = 6,
      height = 50,
      priority = "high"
    },
  },
 --50mm-Mortar-Poison
 {
    type = "projectile",
    name = "50mm-projectile-poison",
    flags = {"not-on-map"},
    acceleration = 0.015,
    action =
    {
      {
        type = "direct",
        action_delivery =
        {
          type = "instant",
          target_effects =
          {
            {
            type = "create-entity",
            entity_name = "explosion"
            },
            {
            type = "create-entity",
            entity_name = "small-scorchmark",
            check_buildability = true
            },
            {
               type = "create-entity",
               entity_name = "poison-cloud-2"
               --entity_name = "lazer-cloud"
            },
			{
        		type = "create-entity",
        		entity_name = "poison-cloud"
          },
          {
        		type = "damage",
        		damage = { amount = 30, type = "poison"}
          },
            {
                  type = "create-sticker",
            sticker = "slowdown-sticker"
            },
          }
        }
      },
      {
        type = "area",
        radius = 6,
        action_delivery =
        {
          type = "instant",
          target_effects =
          {
            {
            type = "damage",
            damage = {amount = 85, type = "explosion"}
            }
          }
        }
      }
    },
    light = {intensity = 0.5, size = 4},
    animation =
    {
      filename = "__tanks_for_bob_fork__/graphics/entity/Cluster/Cluster.png",
      frame_count = 1,
      width = 6,
      height = 50,
      priority = "high"
    },
  },
 --tank-mine-projectile
 {
    type = "projectile",
    name = "tank-mine-projectile",
    flags = {"not-on-map"},
    acceleration = 0.015,
    action =
    {
      {
    type = "direct",
        action_delivery =
      {
          type = "instant",
      target_effects =
          {
      {
            type = "create-entity",
            entity_name = "land-mine"
            },
          }
       }
    },
    },
    animation =
    {
      filename = "__base__/graphics/entity/land-mine/land-mine.png",
      frame_count = 1,
      width = 32,
      height = 32,
      priority = "high"
    },
  },
 --tank-mine-projectile-poison
 {
    type = "projectile",
    name = "tank-mine-projectile-poison",
    flags = {"not-on-map"},
    acceleration = 0.015,
    action =
    {
      {
        type = "direct",
        action_delivery =
        {
          type = "instant",
          target_effects =
          {
            {
              type = "create-entity",
              entity_name = "land-mine-poison"
            },
          }
       }
    },
    },
    animation =
    {
      filename = "__base__/graphics/entity/land-mine/land-mine.png",
      frame_count = 1,
      width = 32,
      height = 32,
      priority = "high"
    },
  },
--45mm-projectile
 {
    type = "projectile",
    name = "45mm-projectile",
    flags = {"not-on-map"},
    collision_box = {{-0.05, -1.1}, {0.05, 1.1}},
    acceleration = 0,
    direction_only = true,
    piercing_damage = 330,
    action =
    {
      {
        type = "direct",
        action_delivery =
        {
          type = "instant",
          target_effects =
          {
            {
              type = "create-entity",
              entity_name = "auto-cannon-hit",
            },
            {
              type = "damage",
              damage = { amount = 220 , type = "physical"}
            },
          }
        }
       }
    },
    animation =
    {
      filename = "__base__/graphics/entity/bullet/bullet.png",
      frame_count = 1,
      width = 3,
      height = 50,
      priority = "high"
    },
  },
--cannon-projectile-2 (cannon-shell-2
 {
    type = "projectile",
    name = "cannon-projectile-2",
    flags = {"not-on-map"},
    collision_box = {{-0.05, -1.1}, {0.05, 1.1}},
    acceleration = 0.1,
    direction_only = true,
    piercing_damage = 150,
    action =
    {
      {
        type = "direct",
        action_delivery =
        {
          type = "instant",
          target_effects =
          {
            {
              type = "create-entity",
              entity_name = "big-explosion"
            },
            {
              type = "create-entity",
              entity_name = "small-scorchmark",
              check_buildability = true
            },
            {
              type = "damage",
              damage = { amount = 300 , type = "physical"}
            }
          }
        }
      },
      {
        type = "area",
        radius = 4.5,
        action_delivery =
        {
          type = "instant",
          target_effects =
          {
            {
              type = "damage",
              damage = {amount = 275, type = "explosion"}
            }
          }
        }
      }
    },
    final_action =
    {
      type = "direct",
      action_delivery =
      {
        type = "instant",
        target_effects =
        {
          {
            type = "create-entity",
            entity_name = "small-scorchmark",
            check_buildability = true
          }
        }
      }
    },
    animation =
    {
      filename = "__base__/graphics/entity/bullet/bullet.png",
      frame_count = 1,
      width = 3,
      height = 50,
      priority = "high"
    },
  },
--tank-rockets
  {
    type = "projectile",
    name = "tank-rocket",
    flags = {"not-on-map"},
    acceleration = 0.007,
    action =
    {
      type = "direct",
      action_delivery =
      {
        type = "instant",
        target_effects =
        {
          {
            type = "create-entity",
            entity_name = "grenade-explosion"
          },
          {
            type = "nested-result",
            action =
            {
              type = "area",
              radius = 6,
              action_delivery =
              {
                type = "instant",
                target_effects =
                {
                  {
                    type = "damage",
                    damage = {amount = 110, type = "explosion"}
                  },
                  {
                    type = "create-entity",
                    entity_name = "explosion"
                  }
                }
              }
            },
          }
        }
      }
    },
    light = {intensity = 0.5, size = 15},
    animation =
    {
      filename = "__tanks_for_bob_fork__/graphics/entity/tank-rocket/tank-rocket.png",
      frame_count = 1,
      width = 10,
      height = 30,
      priority = "high"
    },
    shadow =
    {
      filename = "__tanks_for_bob_fork__/graphics/entity/tank-rocket/tank-rocket-shadow.png",
      frame_count = 1,
      width = 10,
      height = 30,
      priority = "high"
    },
    smoke =
    {
      {
        name = "smoke-fast",
        deviation = {0.15, 0.15},
        frequency = 1,
        position = {0, 0},
        slow_down_factor = 1,
        starting_frame = 3,
        starting_frame_deviation = 5,
        starting_frame_speed = 0,
        starting_frame_speed_deviation = 5
      }
    }
  },
  --WMD-Mortar
 {
    type = "projectile",
    name = "wmd-projectile",
    flags = {"not-on-map"},
    acceleration = 0.001,
	    picture =
		{
      filename = "__tanks_for_bob_fork__/graphics/entity/wmd-artillery-projectile/wmd-hr-shell.png",
      draw_as_glow = true,
      width = 64,
      height = 64,
      scale = 0.5
		},
    shadow =
		{
      filename = "__tanks_for_bob_fork__/graphics/entity/wmd-artillery-projectile/wmd-hr-shell-shadow.png",
      width = 64,
      height = 64,
      scale = 0.5
		},
    chart_picture =
		{
      filename = "__tanks_for_bob_fork__/graphics/entity/wmd-artillery-projectile/wmd-artillery-shoot-map-visualization.png",
      flags = { "icon" },
      frame_count = 1,
      width = 64,
      height = 64,
      priority = "high",
      scale = 0.25
		},
    action =
    {
      {
        type = "direct",
        action_delivery =
		
        {
          type = "instant",
          target_effects =
          {
            {
            type = "create-entity",
            entity_name = "nuke-explosion"
            },
			{
        		type = "create-entity",
        		entity_name = "poison-cloud"
          },
          {
          type = "nested-result",
          action =
          {
            type = "area",
            radius = 7,
            entity_flags = {"breaths-air"},
            action_delivery =
            {
              type = "instant",
              target_effects =
              {
                type = "damage",
                damage = { amount = 44, type = "poison"}
              },
            },
          },
        },
			{
            type = "nested-result",
            action =
            {
              type = "area",
              target_entities = false,
			  show_in_tooltip = false,
              trigger_from_target = true,
              repeat_count = 20,
              radius = 10,
              action_delivery =
              {
                type = "projectile",
                projectile = "atomic-bomb-wave-spawns-cluster-nuke-explosion",
                starting_speed = 0.1 * 0.7,
				deviation = {0.01, 0.05},
                starting_speed_deviation = nuke_shockwave_starting_speed_deviation
              },
			
            },
          },
		  {
            type = "set-tile",
            tile_name = "nuclear-ground",
            radius = 10,
            apply_projection = true,
           tile_collision_mask =
{
  layers =
  {
    water_tile = true
  }
}
          },
		  {
            type = "create-decorative",
            decorative = "nuclear-ground-patch",
            spawn_min_radius = 4.5,
            spawn_max_radius = 11.5,
            spawn_min = 5,
            spawn_max = 15,
            apply_projection = true,
            spread_evenly = true
          },
		  {
            type = "destroy-cliffs",
            radius = 6,
            explosion = "explosionnukea"
          },
		  {
            type = "camera-effect",
            effect = "screen-burn",
            duration = 60,
            ease_in_duration = 5,
            ease_out_duration = 60,
            delay = 0,
            strength = 6,
            full_strength_max_distance = 200,
            max_distance = 800
          },
		  {
            type = "nested-result",
            action =
            {
              type = "area",
              target_entities = false,
			  show_in_tooltip = false,
              trigger_from_target = true,
              repeat_count = 80,
              radius = 7,
              action_delivery =
              {
                type = "projectile",
                projectile = "atomic-bomb-wave-spawns-fire-smoke-explosion",
                starting_speed = 0.1 * 0.65,
				deviation = {0.01, 0.05},
                starting_speed_deviation = nuke_shockwave_starting_speed_deviation
              }
            }
          },
			{
            type = "nested-result",
            action =
            {
              type = "area",
              target_entities = false,
              trigger_from_target = true,
              repeat_count = 35,
              radius = 5,
              action_delivery =
              {
                type = "projectile",
                projectile = "atomic-bomb-ground-zero-projectile",
                starting_speed = 0.1 * 0.8,
				deviation = {0.01, 0.05},
                starting_speed_deviation = nuke_shockwave_starting_speed_deviation
              }
            }
          },
          {
            type = "nested-result",
            action =
            {
              type = "area",
              target_entities = false,
			  show_in_tooltip = false,
              trigger_from_target = true,
              repeat_count = 20,
              radius = 7,
              action_delivery =
              {
                type = "projectile",
                projectile = "atomic-bomb-wave",
                starting_speed = 0.5 * 0.7,
				deviation = {0.01, 0.05},
                starting_speed_deviation = nuke_shockwave_starting_speed_deviation
              },
            }
          },
            -- Do not create massive-scorchmark entities here.
            -- The permanent visual crater is already handled by nuclear-ground tiles
            -- and nuclear-ground-patch decoratives above. Extra corpse scorchmarks
            -- render as hard square blocks with some graphics/mod stacks.
          }
        }
      },
      {
        type = "area",
        radius = 35,
        action_delivery =
        {
          type = "instant",
          target_effects =
          {
            {
            type = "damage",
            damage = {amount = 440, type = "explosion"}
            },
            {
            type = "create-entity",
            entity_name = "explosion"
            }
			
          }
        }
      }
    },
    final_action =
    {
      type = "direct",
      action_delivery =
      {
        type = "instant",
        target_effects =
        {
          {
            type = "invoke-tile-trigger",
            repeat_count = 1
          },
          {
            type = "destroy-decoratives",
            from_render_layer = "decorative",
            to_render_layer = "object",
            include_soft_decoratives = true,
            include_decals = false,
            invoke_decorative_trigger = true,
            decoratives_with_trigger_only = false,
            radius = 12
          }
        }
      }
    },
    light = {intensity = 1.7, size = 22},
    animation =
    {
      filename = "__tanks_for_bob_fork__/graphics/icons/tank-ammo-wmd.png",
      frame_count = 1,
      width = 32,
      height = 32,
    scale = 1,
      priority = "high"
    },
  },
  --nuke artillery

 {
    type = "artillery-projectile",
    name = "wmdartillery-ammo",
    flags = {"not-on-map"},
    reveal_map = true,
    map_color = {r=1, g=1, b=0},
    picture =
		{
      filename = "__tanks_for_bob_fork__/graphics/entity/wmd-artillery-projectile/wmd-hr-shell.png",
      draw_as_glow = true,
      width = 64,
      height = 64,
      scale = 0.5
		},
    shadow =
		{
      filename = "__tanks_for_bob_fork__/graphics/entity/wmd-artillery-projectile/wmd-hr-shell-shadow.png",
      width = 64,
      height = 64,
      scale = 0.5
		},
    chart_picture =
		{
      filename = "__tanks_for_bob_fork__/graphics/entity/wmd-artillery-projectile/wmd-artillery-shoot-map-visualization.png",
      flags = { "icon" },
      frame_count = 1,
      width = 64,
      height = 64,
      priority = "high",
      scale = 0.25
		},
    action =
    {
      type = "direct",
      action_delivery =
      {
        type = "instant",
        target_effects =
        {
            {
            type = "create-entity",
            entity_name = "nuke-explosion"
            },
			{
        		type = "create-entity",
        		entity_name = "poison-cloud"
			},
          {
          type = "nested-result",
          action =
           {
            type = "area",
            radius = 8,
			pollute = 50,
            entity_flags = {"breaths-air"},
            action_delivery =
             {
              type = "instant",
              target_effects =
               {
                type = "damage",
                damage = { amount = 44, type = "poison"}
               },
             },
            },
           },
			{
            type = "nested-result",
            action =
            {
              type = "area",
              target_entities = false,
			  show_in_tooltip = false,
              trigger_from_target = true,
              repeat_count = 24,
              radius = 10,
              action_delivery =
              {
                type = "projectile",
                projectile = "atomic-bomb-wave-spawns-cluster-nuke-explosion",
                starting_speed = 0.1 * 0.7,
				deviation = {0.01, 0.05},
                starting_speed_deviation = nuke_shockwave_starting_speed_deviation
              },
			
            },
          },
		  {
            type = "set-tile",
            tile_name = "nuclear-ground",
            radius = 12,
            apply_projection = true,
            tile_collision_mask =
{
  layers =
  {
    water_tile = true
  }
}
          },
		  {
            type = "create-decorative",
            decorative = "nuclear-ground-patch",
            spawn_min_radius = 5.5,
            spawn_max_radius = 13.5,
            spawn_min = 11,
            spawn_max = 19,
            apply_projection = true,
            spread_evenly = true
          },
		  {
            type = "destroy-cliffs",
            radius = 8,
            explosion = "explosionnukea"
          },
		  {
            type = "camera-effect",
            effect = "screen-burn",
            duration = 60,
            ease_in_duration = 5,
            ease_out_duration = 60,
            delay = 0,
            strength = 6,
            full_strength_max_distance = 200,
            max_distance = 800
          },
		  {
            type = "nested-result",
            action =
            {
              type = "area",
              target_entities = false,
			  show_in_tooltip = false,
              trigger_from_target = true,
              repeat_count = 100,
              radius = 10,
              action_delivery =
              {
                type = "projectile",
                projectile = "atomic-bomb-wave-spawns-fire-smoke-explosion",
                starting_speed = 0.1 * 0.65,
				deviation = {0.01, 0.05},
                starting_speed_deviation = nuke_shockwave_starting_speed_deviation
              }
            }
          },
			{
            type = "nested-result",
            action =
            {
              type = "area",
              target_entities = false,
              trigger_from_target = true,
              repeat_count = 45,
              radius = 8,
              action_delivery =
              {
                type = "projectile",
                projectile = "atomic-bomb-ground-zero-projectile",
                starting_speed = 0.1 * 0.8,
				deviation = {0.01, 0.05},
                starting_speed_deviation = nuke_shockwave_starting_speed_deviation
              }
            }
          },
          {
            type = "nested-result",
            action =
            {
              type = "area",
              target_entities = false,
			  show_in_tooltip = false,
              trigger_from_target = true,
              repeat_count = 30,
              radius = 10,
              action_delivery =
              {
                type = "projectile",
                projectile = "atomic-bomb-wave",
                starting_speed = 0.5 * 0.7,
				deviation = {0.01, 0.05},
				reveal_map = true,
                starting_speed_deviation = nuke_shockwave_starting_speed_deviation
              },
            }
           },
          },
        
      
      {
        type = "area",
        radius = 4.4,
        action_delivery =
         {
          type = "instant",
          target_effects =
          {
             {
            type = "damage",
            damage = {amount = 1100, type = "explosion"}
             },
            {
            type = "create-entity",
            entity_name = "explosion"
            }
			
          }
         }
        
			--boom?
			
          },
          {
            type = "create-trivial-smoke",
            smoke_name = "artillery-smoke",
            initial_height = 0,
            speed_from_center = 0.05,
            speed_from_center_deviation = 0.005,
            offset_deviation = {{-4, -4}, {4, 4}},
            max_radius = 6.5,
            repeat_count = 4 * 4 * 15
          },
          {
            type = "create-entity",
            entity_name = "big-artillery-explosion"
          },
          {
            type = "show-explosion-on-chart",
            scale = 8
          }

      }
    },
    final_action =
    {
      type = "direct",
      action_delivery =
      {
        type = "instant",
        target_effects =
        {
          -- Do not create massive-scorchmark entities here.
          -- Nuclear scorch visuals are handled by set-tile nuclear-ground and
          -- create-decorative nuclear-ground-patch in the main impact action.
          {
            type = "invoke-tile-trigger",
            repeat_count = 1
          },
          {
          type = "destroy-decoratives",
          from_render_layer = "decorative",
          to_render_layer = "object",
          include_soft_decoratives = true, -- soft decoratives are decoratives with grows_through_rail_path = true
          include_decals = false,
          invoke_decorative_trigger = true,
          decoratives_with_trigger_only = false, -- if true, destroys only decoratives that have trigger_effect set
          radius = 12 -- expanded to match corrected nuke scorch footprint
          }
        }
      }
    },
    height_from_ground = 280 / 64
   },


  --piercing-shotgun-pellet-2
 {
    type = "projectile",
    name = "piercing-shotgun-pellet-2",
    flags = {"not-on-map"},
    collision_box = {{-0.05, -0.25}, {0.05, 0.25}},
    acceleration = 1,
    direction_only = true,
    action =
    {
      type = "direct",
      action_delivery =
      {
        type = "instant",
        target_effects =
        {
          type = "damage",
          damage = {amount = 9, type = "physical"}
        }
      }
    },
    animation =
    {
      filename = "__base__/graphics/entity/piercing-bullet/piercing-bullet.png",
      frame_count = 1,
      width = 3,
      height = 50,
      priority = "high",
    }
  }
 }
)