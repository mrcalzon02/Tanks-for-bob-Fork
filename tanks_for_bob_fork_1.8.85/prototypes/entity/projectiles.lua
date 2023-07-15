local WMDexorange = settings.startup["WMD1"].value
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
              damage = {amount = 150, type = "explosion"}
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
        		damage = { amount = 150, type = "poison"}
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
        radius = 15,
        action_delivery =
        {
          type = "instant",
          target_effects =
          {
            {
            type = "damage",
            damage = {amount = 190, type = "explosion"}
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
    piercing_damage = 200,
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
              damage = { amount = 190 , type = "physical"}
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
    piercing_damage = 20,
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
              damage = { amount = 225 , type = "physical"}
            }
          }
        }
      },
      {
        type = "area",
        radius = 2.5,
        action_delivery =
        {
          type = "instant",
          target_effects =
          {
            {
              type = "damage",
              damage = {amount = 220, type = "explosion"}
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
              radius = 7,
              action_delivery =
              {
                type = "instant",
                target_effects =
                {
                  {
                    type = "damage",
                    damage = {amount = 190, type = "explosion"}
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
            radius = 11,
            entity_flags = {"breaths-air"},
            action_delivery =
            {
              type = "instant",
              target_effects =
              {
                type = "damage",
                damage = { amount = 148, type = "poison"}
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
              repeat_count = 70,
              radius = 14,
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
            radius = 8,
            apply_projection = true,
            tile_collision_mask = { "water-tile",}
          },
		  {
            type = "create-decorative",
            decorative = "nuclear-ground-patch",
            spawn_min_radius = 4.5,
            spawn_max_radius = 8.5,
            spawn_min = 5,
            spawn_max = 15,
            apply_projection = true,
            spread_evenly = true
          },
		  {
            type = "destroy-cliffs",
            radius = 9,
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
              repeat_count = 250,
              radius = 9,
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
              repeat_count = 90,
              radius = 6,
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
              repeat_count = 50,
              radius = 8,
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
            {
            type = "create-entity",
            entity_name = "massive-scorchmark",
            check_buildability = true
            }
          }
        }
      },
      {
        type = "area",
        radius = WMDexorange,
        action_delivery =
        {
          type = "instant",
          target_effects =
          {
            {
            type = "damage",
            damage = {amount = 850, type = "explosion"}
            },
            {
            type = "create-entity",
            entity_name = "explosion"
            }
			
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
            radius = 32,
			pollute = 200,
            entity_flags = {"breaths-air"},
            action_delivery =
             {
              type = "instant",
              target_effects =
               {
                type = "damage",
                damage = { amount = 148, type = "poison"}
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
              repeat_count = 70,
              radius = 24,
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
            radius = 14,
            apply_projection = true,
            tile_collision_mask = { "water-tile",}
          },
		  {
            type = "create-decorative",
            decorative = "nuclear-ground-patch",
            spawn_min_radius = 8.5,
            spawn_max_radius = 18.5,
            spawn_min = 11,
            spawn_max = 19,
            apply_projection = true,
            spread_evenly = true
          },
		  {
            type = "destroy-cliffs",
            radius = 29,
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
              repeat_count = 350,
              radius = 25,
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
              repeat_count = 120,
              radius = 23,
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
              repeat_count = 80,
              radius = 25,
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
        radius = WMDexorange,
        action_delivery =
         {
          type = "instant",
          target_effects =
          {
             {
            type = "damage",
            damage = {amount = 450, type = "explosion"}
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
            scale = 8/32
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
            entity_name = "massive-scorchmark",
            check_buildability = true
          },
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
          radius = 13.5 -- large radius for demostrative purposes
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
          damage = {amount = 230, type = "physical"}
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