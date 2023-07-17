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
  --newmachines

 {
    type = "lab",
    name = "pondering-hovel",
    icon = "__base__/graphics/icons/lab.png",
    icon_size = 64, icon_mipmaps = 4,
    flags = {"placeable-player", "player-creation"},
    minable = {mining_time = 0.2, result = "lab"},
    max_health = 50,
    corpse = "lab-remnants",
    dying_explosion = "lab-explosion",
    collision_box = {{-1.2, -1.2}, {1.2, 1.2}},
    selection_box = {{-1.5, -1.5}, {1.5, 1.5}},
    on_animation =
    {
      layers =
      {
        {
          filename = "__base__/graphics/entity/lab/lab.png",
          width = 98,
          height = 87,
          frame_count = 33,
          line_length = 11,
          animation_speed = 1 / 3,
          shift = util.by_pixel(0, 1.5),
          hr_version =
          {
            filename = "__base__/graphics/entity/lab/hr-lab.png",
            width = 194,
            height = 174,
            frame_count = 33,
            line_length = 11,
            animation_speed = 1 / 3,
            shift = util.by_pixel(0, 1.5),
            scale = 0.5
          }
        },
        {
          filename = "__base__/graphics/entity/lab/lab-integration.png",
          width = 122,
          height = 81,
          frame_count = 1,
          line_length = 1,
          repeat_count = 33,
          animation_speed = 1 / 3,
          shift = util.by_pixel(0, 15.5),
          hr_version =
          {
            filename = "__base__/graphics/entity/lab/hr-lab-integration.png",
            width = 242,
            height = 162,
            frame_count = 1,
            line_length = 1,
            repeat_count = 33,
            animation_speed = 1 / 3,
            shift = util.by_pixel(0, 15.5),
            scale = 0.5
          }
        },
        {
          filename = "__base__/graphics/entity/lab/lab-light.png",
          blend_mode = "additive",
          draw_as_light = true,
          width = 106,
          height = 100,
          frame_count = 33,
          line_length = 11,
          animation_speed = 1 / 3,
          shift = util.by_pixel(-1, 1),
          hr_version =
          {
            filename = "__base__/graphics/entity/lab/hr-lab-light.png",
            blend_mode = "additive",
            draw_as_light = true,
            width = 216,
            height = 194,
            frame_count = 33,
            line_length = 11,
            animation_speed = 1 / 3,
            shift = util.by_pixel(0, 0),
            scale = 0.5
          }
        },
        {
          filename = "__base__/graphics/entity/lab/lab-shadow.png",
          width = 122,
          height = 68,
          frame_count = 1,
          line_length = 1,
          repeat_count = 33,
          animation_speed = 1 / 3,
          shift = util.by_pixel(13, 11),
          draw_as_shadow = true,
          hr_version =
          {
            filename = "__base__/graphics/entity/lab/hr-lab-shadow.png",
            width = 242,
            height = 136,
            frame_count = 1,
            line_length = 1,
            repeat_count = 33,
            animation_speed = 1 / 3,
            shift = util.by_pixel(13, 11),
            scale = 0.5,
            draw_as_shadow = true
          }
        }
      }
    },
    off_animation =
    {
      layers =
      {
        {
          filename = "__base__/graphics/entity/lab/lab.png",
          width = 98,
          height = 87,
          frame_count = 1,
          shift = util.by_pixel(0, 1.5),
          hr_version =
          {
            filename = "__base__/graphics/entity/lab/hr-lab.png",
            width = 194,
            height = 174,
            frame_count = 1,
            shift = util.by_pixel(0, 1.5),
            scale = 0.5
          }
        },
        {
          filename = "__base__/graphics/entity/lab/lab-integration.png",
          width = 122,
          height = 81,
          frame_count = 1,
          shift = util.by_pixel(0, 15.5),
          hr_version =
          {
            filename = "__base__/graphics/entity/lab/hr-lab-integration.png",
            width = 242,
            height = 162,
            frame_count = 1,
            shift = util.by_pixel(0, 15.5),
            scale = 0.5
          }
        },
        {
          filename = "__base__/graphics/entity/lab/lab-shadow.png",
          width = 122,
          height = 68,
          frame_count = 1,
          shift = util.by_pixel(13, 11),
          draw_as_shadow = true,
          hr_version =
          {
            filename = "__base__/graphics/entity/lab/hr-lab-shadow.png",
            width = 242,
            height = 136,
            frame_count = 1,
            shift = util.by_pixel(13, 11),
            draw_as_shadow = true,
            scale = 0.5
          }
        }
      }
    },
    working_sound =
    {
      sound =
      {
        filename = "__base__/sound/lab.ogg",
        volume = 0.7
      },
      audible_distance_modifier = 0.7,
      fade_in_ticks = 4,
      fade_out_ticks = 20
    },
    energy_source =
    {
       type = "burner",
        fuel_category = "chemical",
        effectivity = 0.5,
        fuel_inventory_size = 1,
        emissions_per_minute = 2,
        light_flicker = {
            color = {0, 0, 0},
            minimum_intensity = 0.6,
            maximum_intensity = 0.95
        },
        smoke = {
            {
                name = "smoke",
                deviation = {0.1, 0.1},
                frequency = 5,
                position = {0.0, -0.8},
                starting_vertical_speed = 0.08,
                starting_frame_deviation = 60
            }
        }
    },
    energy_usage = "100kW",
    researching_speed = 0.8,
    inputs = {"cooked-fish","meal"},
    module_specification =
    {
      module_slots = 2,
    },
  },
--thinking hut
{
    type = "lab",
    name = "thinking hut",
    icon = "__base__/graphics/icons/lab.png",
    icon_size = 64, icon_mipmaps = 4,
    flags = {"placeable-player", "player-creation"},
    minable = {mining_time = 0.2, result = "lab"},
    max_health = 50,
    corpse = "lab-remnants",
    dying_explosion = "lab-explosion",
    collision_box = {{-1.2, -1.2}, {1.2, 1.2}},
    selection_box = {{-1.5, -1.5}, {1.5, 1.5}},
    on_animation =
    {
      layers =
      {
        {
          filename = "__base__/graphics/entity/lab/lab.png",
          width = 98,
          height = 87,
          frame_count = 33,
          line_length = 11,
          animation_speed = 1 / 3,
          shift = util.by_pixel(0, 1.5),
          hr_version =
          {
            filename = "__base__/graphics/entity/lab/hr-lab.png",
            width = 194,
            height = 174,
            frame_count = 33,
            line_length = 11,
            animation_speed = 1 / 3,
            shift = util.by_pixel(0, 1.5),
            scale = 0.5
          }
        },
        {
          filename = "__base__/graphics/entity/lab/lab-integration.png",
          width = 122,
          height = 81,
          frame_count = 1,
          line_length = 1,
          repeat_count = 33,
          animation_speed = 1 / 3,
          shift = util.by_pixel(0, 15.5),
          hr_version =
          {
            filename = "__base__/graphics/entity/lab/hr-lab-integration.png",
            width = 242,
            height = 162,
            frame_count = 1,
            line_length = 1,
            repeat_count = 33,
            animation_speed = 1 / 3,
            shift = util.by_pixel(0, 15.5),
            scale = 0.5
          }
        },
        {
          filename = "__base__/graphics/entity/lab/lab-light.png",
          blend_mode = "additive",
          draw_as_light = true,
          width = 106,
          height = 100,
          frame_count = 33,
          line_length = 11,
          animation_speed = 1 / 3,
          shift = util.by_pixel(-1, 1),
          hr_version =
          {
            filename = "__base__/graphics/entity/lab/hr-lab-light.png",
            blend_mode = "additive",
            draw_as_light = true,
            width = 216,
            height = 194,
            frame_count = 33,
            line_length = 11,
            animation_speed = 1 / 3,
            shift = util.by_pixel(0, 0),
            scale = 0.5
          }
        },
        {
          filename = "__base__/graphics/entity/lab/lab-shadow.png",
          width = 122,
          height = 68,
          frame_count = 1,
          line_length = 1,
          repeat_count = 33,
          animation_speed = 1 / 3,
          shift = util.by_pixel(13, 11),
          draw_as_shadow = true,
          hr_version =
          {
            filename = "__base__/graphics/entity/lab/hr-lab-shadow.png",
            width = 242,
            height = 136,
            frame_count = 1,
            line_length = 1,
            repeat_count = 33,
            animation_speed = 1 / 3,
            shift = util.by_pixel(13, 11),
            scale = 0.5,
            draw_as_shadow = true
          }
        }
      }
    },
    off_animation =
    {
      layers =
      {
        {
          filename = "__base__/graphics/entity/lab/lab.png",
          width = 98,
          height = 87,
          frame_count = 1,
          shift = util.by_pixel(0, 1.5),
          hr_version =
          {
            filename = "__base__/graphics/entity/lab/hr-lab.png",
            width = 194,
            height = 174,
            frame_count = 1,
            shift = util.by_pixel(0, 1.5),
            scale = 0.5
          }
        },
        {
          filename = "__base__/graphics/entity/lab/lab-integration.png",
          width = 122,
          height = 81,
          frame_count = 1,
          shift = util.by_pixel(0, 15.5),
          hr_version =
          {
            filename = "__base__/graphics/entity/lab/hr-lab-integration.png",
            width = 242,
            height = 162,
            frame_count = 1,
            shift = util.by_pixel(0, 15.5),
            scale = 0.5
          }
        },
        {
          filename = "__base__/graphics/entity/lab/lab-shadow.png",
          width = 122,
          height = 68,
          frame_count = 1,
          shift = util.by_pixel(13, 11),
          draw_as_shadow = true,
          hr_version =
          {
            filename = "__base__/graphics/entity/lab/hr-lab-shadow.png",
            width = 242,
            height = 136,
            frame_count = 1,
            shift = util.by_pixel(13, 11),
            draw_as_shadow = true,
            scale = 0.5
          }
        }
      }
    },
    working_sound =
    {
      sound =
      {
        filename = "__base__/sound/lab.ogg",
        volume = 0.7
      },
      audible_distance_modifier = 0.7,
      fade_in_ticks = 4,
      fade_out_ticks = 20
    },
    energy_source =
    {
       type = "burner",
        fuel_category = "chemical",
        effectivity = 1,
        fuel_inventory_size = 1,
        emissions_per_minute = 2,
        light_flicker = {
            color = {0, 0, 0},
            minimum_intensity = 0.6,
            maximum_intensity = 0.95
        },
        smoke = {
            {
                name = "smoke",
                deviation = {0.1, 0.1},
                frequency = 5,
                position = {0.0, -0.8},
                starting_vertical_speed = 0.08,
                starting_frame_deviation = 60
            }
        }
    },
    energy_usage = "20kW",
    researching_speed = 0.5,
    inputs = {"cooked-fish","meal"},
    module_specification =
    {
      module_slots = 1,
    },
  },

  --stone water wheel
    {
  type = "offshore-pump",
  name = "stone-water-wheel",
  icon = "__base__/graphics/icons/offshore-pump.png",
  icon_size = 64, icon_mipmaps = 4,
  flags = {"placeable-neutral", "player-creation", "filter-directions"},
  collision_mask = { "object-layer", "train-layer" },
  center_collision_mask = { "water-tile", "object-layer", "player-layer" },
  fluid_box_tile_collision_test = { "ground-tile" },
  adjacent_tile_collision_test = { "water-tile" },
  adjacent_tile_collision_mask = { "ground-tile" },
  adjacent_tile_collision_box = { { -1, -2 }, { 1, -1 } },
  minable = {mining_time = 0.1, result = "stone-water-wheel"},
  max_health = 150,
  corpse = "offshore-pump-remnants",
  dying_explosion = "offshore-pump-explosion",
  fluid = "water",
  resistances =
  {
    {
      type = "fire",
      percent = 70
    },
    {
      type = "impact",
      percent = 30
    }
  },
  collision_box = {{-0.6, -1.05}, {0.6, 0.3}},
  selection_box = {{-0.6, -1.49}, {0.6, 0.49}},
    fluid_box =
  {
    base_area = 1,
    height = 2,
    base_level = 1,
    pipe_covers = pipecoverspictures(),
    pipe_connections =
    {
      {
        position = {0, 1},
        type = "output"
      }
    },
    production_type = "output",
    filter = "water",
    minimum_temperature = 15,
    pipe_covers = pipecoverspictures(),
    pipe_connections =
    {
      {
        position = {0, 1},
        type = "output"
      }
    }
  },
  pumping_speed = 10,
  tile_width = 1,
  tile_height = 1,
    working_sound =
  {
    sound =
    {
      {
        filename = "__base__/sound/offshore-pump.ogg",
        volume = 0.5
      }
    },
    match_volume_to_activity = true,
    audible_distance_modifier = 0.7,
    max_sounds_per_type = 3,
    fade_in_ticks = 4,
    fade_out_ticks = 20
  },
  min_perceived_performance = 0.5,
  always_draw_fluid = true,
  graphics_set =
  {
    underwater_layer_offset = 30,
    base_render_layer = "ground-patch",
    animation =
    {
      north =
      {
        layers =
        {
          {
            filename = "__base__/graphics/entity/offshore-pump/offshore-pump_North.png",
            priority = "high",
            line_length = 8,
            frame_count = 32,
            animation_speed = 0.25,
            width = 48,
            height = 84,
            shift = util.by_pixel(-2, -16),
            hr_version =
            {
              filename = "__base__/graphics/entity/offshore-pump/hr-offshore-pump_North.png",
              priority = "high",
              line_length = 8,
              frame_count = 32,
              animation_speed = 0.25,
              width = 90,
              height = 162,
              shift = util.by_pixel(-1, -15),
              scale = 0.5
            }
          },
          {
            filename = "__base__/graphics/entity/offshore-pump/offshore-pump_North-shadow.png",
            priority = "high",
            line_length = 8,
            frame_count = 32,
            animation_speed = 0.25,
            width = 78,
            height = 70,
            shift = util.by_pixel(12, -8),
            draw_as_shadow = true,
            hr_version =
            {
              filename = "__base__/graphics/entity/offshore-pump/hr-offshore-pump_North-shadow.png",
              priority = "high",
              line_length = 8,
              frame_count = 32,
              animation_speed = 0.25,
              width = 150,
              height = 134,
              shift = util.by_pixel(13, -7),
              draw_as_shadow = true,
              scale = 0.5
            }
          }
        }
      },
      east =
      {
        layers =
        {
          {
            filename = "__base__/graphics/entity/offshore-pump/offshore-pump_East.png",
            priority = "high",
            line_length = 8,
            frame_count = 32,
            animation_speed = 0.25,
            width = 64,
            height = 52,
            shift = util.by_pixel(14, -2),
            hr_version =
            {
              filename = "__base__/graphics/entity/offshore-pump/hr-offshore-pump_East.png",
              priority = "high",
              line_length = 8,
              frame_count = 32,
              animation_speed = 0.25,
              width = 124,
              height = 102,
              shift = util.by_pixel(15, -2),
              scale = 0.5
            }
          },
          {
            filename = "__base__/graphics/entity/offshore-pump/offshore-pump_East-shadow.png",
            priority = "high",
            line_length = 8,
            frame_count = 32,
            animation_speed = 0.25,
            width = 88,
            height = 34,
            shift = util.by_pixel(28, 8),
            draw_as_shadow = true,
            hr_version =
            {
              filename = "__base__/graphics/entity/offshore-pump/hr-offshore-pump_East-shadow.png",
              priority = "high",
              line_length = 8,
              frame_count = 32,
              animation_speed = 0.25,
              width = 180,
              height = 66,
              shift = util.by_pixel(27, 8),
              draw_as_shadow = true,
              scale = 0.5
            }
          }
        }
      },
      south =
      {
        layers =
        {
          {
            filename = "__base__/graphics/entity/offshore-pump/offshore-pump_South.png",
            priority = "high",
            line_length = 8,
            frame_count = 32,
            animation_speed = 0.25,
            width = 48,
            height = 96,
            shift = util.by_pixel(-2, 0),
            hr_version =
            {
              filename = "__base__/graphics/entity/offshore-pump/hr-offshore-pump_South.png",
              priority = "high",
              line_length = 8,
              frame_count = 32,
              animation_speed = 0.25,
              width = 92,
              height = 192,
              shift = util.by_pixel(-1, 0),
              scale = 0.5
            }
          },
          {
            filename = "__base__/graphics/entity/offshore-pump/offshore-pump_South-shadow.png",
            priority = "high",
            line_length = 8,
            frame_count = 32,
            animation_speed = 0.25,
            width = 80,
            height = 66,
            shift = util.by_pixel(16, 22),
            draw_as_shadow = true,
            hr_version =
            {
              filename = "__base__/graphics/entity/offshore-pump/hr-offshore-pump_South-shadow.png",
              priority = "high",
              line_length = 8,
              frame_count = 32,
              animation_speed = 0.25,
              width = 164,
              height = 128,
              shift = util.by_pixel(15, 23),
              draw_as_shadow = true,
              scale = 0.5
            }
          }
        }
      },
      west =
      {
        layers =
        {
          {
            filename = "__base__/graphics/entity/offshore-pump/offshore-pump_West.png",
            priority = "high",
            line_length = 8,
            frame_count = 32,
            animation_speed = 0.25,
            width = 64,
            height = 52,
            shift = util.by_pixel(-16, -2),
            hr_version =
            {
              filename = "__base__/graphics/entity/offshore-pump/hr-offshore-pump_West.png",
              priority = "high",
              line_length = 8,
              frame_count = 32,
              animation_speed = 0.25,
              width = 124,
              height = 102,
              shift = util.by_pixel(-15, -2),
              scale = 0.5
            }
          },
          {
            filename = "__base__/graphics/entity/offshore-pump/offshore-pump_West-shadow.png",
            priority = "high",
            line_length = 8,
            frame_count = 32,
            animation_speed = 0.25,
            width = 88,
            height = 34,
            shift = util.by_pixel(-4, 8),
            draw_as_shadow = true,
            hr_version =
            {
              filename = "__base__/graphics/entity/offshore-pump/hr-offshore-pump_West-shadow.png",
              priority = "high",
              line_length = 8,
              frame_count = 32,
              animation_speed = 0.25,
              width = 172,
              height = 66,
              shift = util.by_pixel(-3, 8),
              draw_as_shadow = true,
              scale = 0.5
            }
          }
        }
      }
    },
    fluid_animation =
    {
      north =
      {
        filename = "__base__/graphics/entity/offshore-pump/offshore-pump_North-fluid.png",
        apply_runtime_tint = true,
        line_length = 8,
        frame_count = 32,
        animation_speed = 0.25,
        width = 22,
        height = 20,
        shift = util.by_pixel(-2, -22),
        hr_version = {
          filename = "__base__/graphics/entity/offshore-pump/hr-offshore-pump_North-fluid.png",
          apply_runtime_tint = true,
          line_length = 8,
          frame_count = 32,
          animation_speed = 0.25,
          width = 40,
          height = 40,
          shift = util.by_pixel(-1, -22),
          scale = 0.5
        }
      },
      east =
      {
        filename = "__base__/graphics/entity/offshore-pump/offshore-pump_East-fluid.png",
        apply_runtime_tint = true,
        line_length = 8,
        frame_count = 32,
        animation_speed = 0.25,
        width = 20,
        height = 24,
        shift = util.by_pixel(6, -10),
        hr_version = {
          filename = "__base__/graphics/entity/offshore-pump/hr-offshore-pump_East-fluid.png",
          apply_runtime_tint = true,
          line_length = 8,
          frame_count = 32,
          animation_speed = 0.25,
          width = 38,
          height = 50,
          shift = util.by_pixel(6, -11),
          scale = 0.5
        }
      },
      south =
      {
        filename = "__base__/graphics/entity/offshore-pump/offshore-pump_South-fluid.png",
        apply_runtime_tint = true,
        line_length = 8,
        frame_count = 32,
        animation_speed = 0.25,
        width = 20,
        height = 8,
        shift = util.by_pixel(-2, -4),
        hr_version = {
          filename = "__base__/graphics/entity/offshore-pump/hr-offshore-pump_South-fluid.png",
          apply_runtime_tint = true,
          line_length = 8,
          frame_count = 32,
          animation_speed = 0.25,
          width = 36,
          height = 14,
          shift = util.by_pixel(-1, -4),
          scale = 0.5
        }
      },
      west =
      {
        filename = "__base__/graphics/entity/offshore-pump/offshore-pump_West-fluid.png",
        apply_runtime_tint = true,
        line_length = 8,
        frame_count = 32,
        animation_speed = 0.25,
        width = 20,
        height = 24,
        shift = util.by_pixel(-8, -10),
        hr_version = {
          filename = "__base__/graphics/entity/offshore-pump/hr-offshore-pump_West-fluid.png",
          apply_runtime_tint = true,
          line_length = 8,
          frame_count = 32,
          animation_speed = 0.25,
          width = 36,
          height = 50,
          shift = util.by_pixel(-7, -11),
          scale = 0.5
        }
      }
    },
    glass_pictures =
    {
      north =
      {
        filename = "__base__/graphics/entity/offshore-pump/offshore-pump_North-glass.png",
        width = 18,
        height = 20,
        shift = util.by_pixel(-2, -22),
        hr_version =
        {
          filename = "__base__/graphics/entity/offshore-pump/hr-offshore-pump_North-glass.png",
          width = 36,
          height = 40,
          shift = util.by_pixel(-2, -22),
          scale = 0.5
        }
      },
      east =
      {
        filename = "__base__/graphics/entity/offshore-pump/offshore-pump_East-glass.png",
        width = 18,
        height = 18,
        shift = util.by_pixel(4, -14),
        hr_version =
        {
          filename = "__base__/graphics/entity/offshore-pump/hr-offshore-pump_East-glass.png",
          width = 30,
          height = 32,
          shift = util.by_pixel(5, -13),
          scale = 0.5
        }
      },
      south =
      {
        filename = "__base__/graphics/entity/offshore-pump/offshore-pump_South-glass.png",
        width = 22,
        height = 12,
        shift = util.by_pixel(-2, -6),
        hr_version =
        {
          filename = "__base__/graphics/entity/offshore-pump/hr-offshore-pump_South-glass.png",
          width = 40,
          height = 24,
          shift = util.by_pixel(-1, -6),
          scale = 0.5
        }
      },
      west =
      {
        filename = "__base__/graphics/entity/offshore-pump/offshore-pump_West-glass.png",
        width = 16,
        height = 16,
        shift = util.by_pixel(-6, -14),
        hr_version =
        {
          filename = "__base__/graphics/entity/offshore-pump/hr-offshore-pump_West-glass.png",
          width = 30,
          height = 32,
          shift = util.by_pixel(-6, -14),
          scale = 0.5
        }
      }
    },
    base_pictures =
    {
      north =
      {
        filename = "__base__/graphics/entity/offshore-pump/offshore-pump_North-legs.png",
        width = 60,
        height = 52,
        shift = util.by_pixel(-2, -4),
        hr_version =
        {
          filename = "__base__/graphics/entity/offshore-pump/hr-offshore-pump_North-legs.png",
          width = 114,
          height = 106,
          shift = util.by_pixel(-1, -5),
          scale = 0.5
        }
      },
      east =
      {
        filename = "__base__/graphics/entity/offshore-pump/offshore-pump_East-legs.png",
        width = 54,
        height = 32,
        shift = util.by_pixel(4, 12),
        hr_version =
        {
          filename = "__base__/graphics/entity/offshore-pump/hr-offshore-pump_East-legs.png",
          width = 106,
          height = 60,
          shift = util.by_pixel(4, 13),
          scale = 0.5
        }
      },
      south =
      {
        filename = "__base__/graphics/entity/offshore-pump/offshore-pump_South-legs.png",
        width = 56,
        height = 54,
        shift = util.by_pixel(-2, 6),
        hr_version =
        {
          filename = "__base__/graphics/entity/offshore-pump/hr-offshore-pump_South-legs.png",
          width = 110,
          height = 108,
          shift = util.by_pixel(-2, 6),
          scale = 0.5
        }
      },
      west =
      {
        filename = "__base__/graphics/entity/offshore-pump/offshore-pump_West-legs.png",
        width = 54,
        height = 32,
        shift = util.by_pixel(-6, 12),
        hr_version =
        {
          filename = "__base__/graphics/entity/offshore-pump/hr-offshore-pump_West-legs.png",
          width = 108,
          height = 64,
          shift = util.by_pixel(-6, 12),
          scale = 0.5
        }
      }
    },
    underwater_pictures =
    {
      north =
      {
        filename = "__base__/graphics/entity/offshore-pump/offshore-pump_North-underwater.png",
        width = 52,
        height = 16,
        shift = util.by_pixel(-2, -34),
        hr_version =
        {
          filename = "__base__/graphics/entity/offshore-pump/hr-offshore-pump_North-underwater.png",
          width = 98,
          height = 36,
          shift = util.by_pixel(-1, -32),
          scale = 0.5
        }
      },
      east =
      {
        filename = "__base__/graphics/entity/offshore-pump/offshore-pump_East-underwater.png",
        width = 18,
        height = 38,
        shift = util.by_pixel(40, 16),
        hr_version =
        {
          filename = "__base__/graphics/entity/offshore-pump/hr-offshore-pump_East-underwater.png",
          width = 40,
          height = 72,
          shift = util.by_pixel(39, 17),
          scale = 0.5
        }
      },
      south =
      {
        filename = "__base__/graphics/entity/offshore-pump/offshore-pump_South-underwater.png",
        width = 52,
        height = 26,
        shift = util.by_pixel(-2, 48),
        hr_version =
        {
          filename = "__base__/graphics/entity/offshore-pump/hr-offshore-pump_South-underwater.png",
          width = 98,
          height = 48,
          shift = util.by_pixel(-1, 49),
          scale = 0.5
        }
      },
      west =
      {
        filename = "__base__/graphics/entity/offshore-pump/offshore-pump_West-underwater.png",
        width = 20,
        height = 34,
        shift = util.by_pixel(-40, 18),
        hr_version =
        {
          filename = "__base__/graphics/entity/offshore-pump/hr-offshore-pump_West-underwater.png",
          width = 40,
          height = 72,
          shift = util.by_pixel(-40, 17),
          scale = 0.5
        }
      }
    }
  },
  placeable_position_visualization =
  {
    filename = "__core__/graphics/cursor-boxes-32x32.png",
    priority = "extra-high-no-scale",
    width = 64,
    height = 64,
    scale = 0.5,
    x = 3 * 64
  },
  circuit_wire_connection_points = circuit_connector_definitions["offshore-pump"].points,
  circuit_connector_sprites = circuit_connector_definitions["offshore-pump"].sprites,
  circuit_wire_max_distance = default_circuit_wire_max_distance,
  water_reflection =
  {
    pictures =
    {
      filename = "__base__/graphics/entity/offshore-pump/offshore-pump-reflection.png",
      priority = "extra-high",
      width = 132,
      height = 156,
      shift = util.by_pixel(0, 19),
      variation_count = 4,
      scale = 1
    },
    rotate = false,
    orientation_to_variation = true
  }
},
  --beach pump

  {
  type = "offshore-pump",
  name = "beachpump",
  icon = "__base__/graphics/icons/offshore-pump.png",
  icon_size = 64, icon_mipmaps = 4,
  flags = {"placeable-neutral", "player-creation", "filter-directions"},
  collision_mask = { "object-layer", "train-layer" },
  center_collision_mask = { "water-tile", "object-layer", "player-layer" },
  fluid_box_tile_collision_test = { "ground-tile" },
  adjacent_tile_collision_test = { "water-tile" },
  adjacent_tile_collision_mask = { "ground-tile" },
  adjacent_tile_collision_box = { { -1, -2 }, { 1, -1 } },
  minable = {mining_time = 0.1, result = "beachpump"},
  max_health = 50,
  corpse = "offshore-pump-remnants",
  dying_explosion = "offshore-pump-explosion",
  fluid = "water",
  resistances =
  {
    {
      type = "fire",
      percent = 70
    },
    {
      type = "impact",
      percent = 30
    }
  },
  collision_box = {{-0.6, -1.05}, {0.6, 0.3}},
  selection_box = {{-0.6, -1.49}, {0.6, 0.49}},
    fluid_box =
  {
    base_area = 1,
    height = 2,
    base_level = 1,
    pipe_covers = pipecoverspictures(),
    pipe_connections =
    {
      {
        position = {0, 1},
        type = "output"
      }
    },
    production_type = "output",
    filter = "water",
    minimum_temperature = 15,
    pipe_covers = pipecoverspictures(),
    pipe_connections =
    {
      {
        position = {0, 1},
        type = "output"
      }
    }
  },
  pumping_speed = 5,
  tile_width = 1,
  tile_height = 1,
    working_sound =
  {
    sound =
    {
      {
        filename = "__base__/sound/offshore-pump.ogg",
        volume = 0.5
      }
    },
    match_volume_to_activity = true,
    audible_distance_modifier = 0.7,
    max_sounds_per_type = 3,
    fade_in_ticks = 4,
    fade_out_ticks = 20
  },
  min_perceived_performance = 0.5,
  always_draw_fluid = true,
  graphics_set =
  {
    underwater_layer_offset = 30,
    base_render_layer = "ground-patch",
    animation =
    {
      north =
      {
        layers =
        {
          {
            filename = "__base__/graphics/entity/offshore-pump/offshore-pump_North.png",
            priority = "high",
            line_length = 8,
            frame_count = 32,
            animation_speed = 0.25,
            width = 48,
            height = 84,
            shift = util.by_pixel(-2, -16),
            hr_version =
            {
              filename = "__base__/graphics/entity/offshore-pump/hr-offshore-pump_North.png",
              priority = "high",
              line_length = 8,
              frame_count = 32,
              animation_speed = 0.25,
              width = 90,
              height = 162,
              shift = util.by_pixel(-1, -15),
              scale = 0.5
            }
          },
          {
            filename = "__base__/graphics/entity/offshore-pump/offshore-pump_North-shadow.png",
            priority = "high",
            line_length = 8,
            frame_count = 32,
            animation_speed = 0.25,
            width = 78,
            height = 70,
            shift = util.by_pixel(12, -8),
            draw_as_shadow = true,
            hr_version =
            {
              filename = "__base__/graphics/entity/offshore-pump/hr-offshore-pump_North-shadow.png",
              priority = "high",
              line_length = 8,
              frame_count = 32,
              animation_speed = 0.25,
              width = 150,
              height = 134,
              shift = util.by_pixel(13, -7),
              draw_as_shadow = true,
              scale = 0.5
            }
          }
        }
      },
      east =
      {
        layers =
        {
          {
            filename = "__base__/graphics/entity/offshore-pump/offshore-pump_East.png",
            priority = "high",
            line_length = 8,
            frame_count = 32,
            animation_speed = 0.25,
            width = 64,
            height = 52,
            shift = util.by_pixel(14, -2),
            hr_version =
            {
              filename = "__base__/graphics/entity/offshore-pump/hr-offshore-pump_East.png",
              priority = "high",
              line_length = 8,
              frame_count = 32,
              animation_speed = 0.25,
              width = 124,
              height = 102,
              shift = util.by_pixel(15, -2),
              scale = 0.5
            }
          },
          {
            filename = "__base__/graphics/entity/offshore-pump/offshore-pump_East-shadow.png",
            priority = "high",
            line_length = 8,
            frame_count = 32,
            animation_speed = 0.25,
            width = 88,
            height = 34,
            shift = util.by_pixel(28, 8),
            draw_as_shadow = true,
            hr_version =
            {
              filename = "__base__/graphics/entity/offshore-pump/hr-offshore-pump_East-shadow.png",
              priority = "high",
              line_length = 8,
              frame_count = 32,
              animation_speed = 0.25,
              width = 180,
              height = 66,
              shift = util.by_pixel(27, 8),
              draw_as_shadow = true,
              scale = 0.5
            }
          }
        }
      },
      south =
      {
        layers =
        {
          {
            filename = "__base__/graphics/entity/offshore-pump/offshore-pump_South.png",
            priority = "high",
            line_length = 8,
            frame_count = 32,
            animation_speed = 0.25,
            width = 48,
            height = 96,
            shift = util.by_pixel(-2, 0),
            hr_version =
            {
              filename = "__base__/graphics/entity/offshore-pump/hr-offshore-pump_South.png",
              priority = "high",
              line_length = 8,
              frame_count = 32,
              animation_speed = 0.25,
              width = 92,
              height = 192,
              shift = util.by_pixel(-1, 0),
              scale = 0.5
            }
          },
          {
            filename = "__base__/graphics/entity/offshore-pump/offshore-pump_South-shadow.png",
            priority = "high",
            line_length = 8,
            frame_count = 32,
            animation_speed = 0.25,
            width = 80,
            height = 66,
            shift = util.by_pixel(16, 22),
            draw_as_shadow = true,
            hr_version =
            {
              filename = "__base__/graphics/entity/offshore-pump/hr-offshore-pump_South-shadow.png",
              priority = "high",
              line_length = 8,
              frame_count = 32,
              animation_speed = 0.25,
              width = 164,
              height = 128,
              shift = util.by_pixel(15, 23),
              draw_as_shadow = true,
              scale = 0.5
            }
          }
        }
      },
      west =
      {
        layers =
        {
          {
            filename = "__base__/graphics/entity/offshore-pump/offshore-pump_West.png",
            priority = "high",
            line_length = 8,
            frame_count = 32,
            animation_speed = 0.25,
            width = 64,
            height = 52,
            shift = util.by_pixel(-16, -2),
            hr_version =
            {
              filename = "__base__/graphics/entity/offshore-pump/hr-offshore-pump_West.png",
              priority = "high",
              line_length = 8,
              frame_count = 32,
              animation_speed = 0.25,
              width = 124,
              height = 102,
              shift = util.by_pixel(-15, -2),
              scale = 0.5
            }
          },
          {
            filename = "__base__/graphics/entity/offshore-pump/offshore-pump_West-shadow.png",
            priority = "high",
            line_length = 8,
            frame_count = 32,
            animation_speed = 0.25,
            width = 88,
            height = 34,
            shift = util.by_pixel(-4, 8),
            draw_as_shadow = true,
            hr_version =
            {
              filename = "__base__/graphics/entity/offshore-pump/hr-offshore-pump_West-shadow.png",
              priority = "high",
              line_length = 8,
              frame_count = 32,
              animation_speed = 0.25,
              width = 172,
              height = 66,
              shift = util.by_pixel(-3, 8),
              draw_as_shadow = true,
              scale = 0.5
            }
          }
        }
      }
    },
    fluid_animation =
    {
      north =
      {
        filename = "__base__/graphics/entity/offshore-pump/offshore-pump_North-fluid.png",
        apply_runtime_tint = true,
        line_length = 8,
        frame_count = 32,
        animation_speed = 0.25,
        width = 22,
        height = 20,
        shift = util.by_pixel(-2, -22),
        hr_version = {
          filename = "__base__/graphics/entity/offshore-pump/hr-offshore-pump_North-fluid.png",
          apply_runtime_tint = true,
          line_length = 8,
          frame_count = 32,
          animation_speed = 0.25,
          width = 40,
          height = 40,
          shift = util.by_pixel(-1, -22),
          scale = 0.5
        }
      },
      east =
      {
        filename = "__base__/graphics/entity/offshore-pump/offshore-pump_East-fluid.png",
        apply_runtime_tint = true,
        line_length = 8,
        frame_count = 32,
        animation_speed = 0.25,
        width = 20,
        height = 24,
        shift = util.by_pixel(6, -10),
        hr_version = {
          filename = "__base__/graphics/entity/offshore-pump/hr-offshore-pump_East-fluid.png",
          apply_runtime_tint = true,
          line_length = 8,
          frame_count = 32,
          animation_speed = 0.25,
          width = 38,
          height = 50,
          shift = util.by_pixel(6, -11),
          scale = 0.5
        }
      },
      south =
      {
        filename = "__base__/graphics/entity/offshore-pump/offshore-pump_South-fluid.png",
        apply_runtime_tint = true,
        line_length = 8,
        frame_count = 32,
        animation_speed = 0.25,
        width = 20,
        height = 8,
        shift = util.by_pixel(-2, -4),
        hr_version = {
          filename = "__base__/graphics/entity/offshore-pump/hr-offshore-pump_South-fluid.png",
          apply_runtime_tint = true,
          line_length = 8,
          frame_count = 32,
          animation_speed = 0.25,
          width = 36,
          height = 14,
          shift = util.by_pixel(-1, -4),
          scale = 0.5
        }
      },
      west =
      {
        filename = "__base__/graphics/entity/offshore-pump/offshore-pump_West-fluid.png",
        apply_runtime_tint = true,
        line_length = 8,
        frame_count = 32,
        animation_speed = 0.25,
        width = 20,
        height = 24,
        shift = util.by_pixel(-8, -10),
        hr_version = {
          filename = "__base__/graphics/entity/offshore-pump/hr-offshore-pump_West-fluid.png",
          apply_runtime_tint = true,
          line_length = 8,
          frame_count = 32,
          animation_speed = 0.25,
          width = 36,
          height = 50,
          shift = util.by_pixel(-7, -11),
          scale = 0.5
        }
      }
    },
    glass_pictures =
    {
      north =
      {
        filename = "__base__/graphics/entity/offshore-pump/offshore-pump_North-glass.png",
        width = 18,
        height = 20,
        shift = util.by_pixel(-2, -22),
        hr_version =
        {
          filename = "__base__/graphics/entity/offshore-pump/hr-offshore-pump_North-glass.png",
          width = 36,
          height = 40,
          shift = util.by_pixel(-2, -22),
          scale = 0.5
        }
      },
      east =
      {
        filename = "__base__/graphics/entity/offshore-pump/offshore-pump_East-glass.png",
        width = 18,
        height = 18,
        shift = util.by_pixel(4, -14),
        hr_version =
        {
          filename = "__base__/graphics/entity/offshore-pump/hr-offshore-pump_East-glass.png",
          width = 30,
          height = 32,
          shift = util.by_pixel(5, -13),
          scale = 0.5
        }
      },
      south =
      {
        filename = "__base__/graphics/entity/offshore-pump/offshore-pump_South-glass.png",
        width = 22,
        height = 12,
        shift = util.by_pixel(-2, -6),
        hr_version =
        {
          filename = "__base__/graphics/entity/offshore-pump/hr-offshore-pump_South-glass.png",
          width = 40,
          height = 24,
          shift = util.by_pixel(-1, -6),
          scale = 0.5
        }
      },
      west =
      {
        filename = "__base__/graphics/entity/offshore-pump/offshore-pump_West-glass.png",
        width = 16,
        height = 16,
        shift = util.by_pixel(-6, -14),
        hr_version =
        {
          filename = "__base__/graphics/entity/offshore-pump/hr-offshore-pump_West-glass.png",
          width = 30,
          height = 32,
          shift = util.by_pixel(-6, -14),
          scale = 0.5
        }
      }
    },
    base_pictures =
    {
      north =
      {
        filename = "__base__/graphics/entity/offshore-pump/offshore-pump_North-legs.png",
        width = 60,
        height = 52,
        shift = util.by_pixel(-2, -4),
        hr_version =
        {
          filename = "__base__/graphics/entity/offshore-pump/hr-offshore-pump_North-legs.png",
          width = 114,
          height = 106,
          shift = util.by_pixel(-1, -5),
          scale = 0.5
        }
      },
      east =
      {
        filename = "__base__/graphics/entity/offshore-pump/offshore-pump_East-legs.png",
        width = 54,
        height = 32,
        shift = util.by_pixel(4, 12),
        hr_version =
        {
          filename = "__base__/graphics/entity/offshore-pump/hr-offshore-pump_East-legs.png",
          width = 106,
          height = 60,
          shift = util.by_pixel(4, 13),
          scale = 0.5
        }
      },
      south =
      {
        filename = "__base__/graphics/entity/offshore-pump/offshore-pump_South-legs.png",
        width = 56,
        height = 54,
        shift = util.by_pixel(-2, 6),
        hr_version =
        {
          filename = "__base__/graphics/entity/offshore-pump/hr-offshore-pump_South-legs.png",
          width = 110,
          height = 108,
          shift = util.by_pixel(-2, 6),
          scale = 0.5
        }
      },
      west =
      {
        filename = "__base__/graphics/entity/offshore-pump/offshore-pump_West-legs.png",
        width = 54,
        height = 32,
        shift = util.by_pixel(-6, 12),
        hr_version =
        {
          filename = "__base__/graphics/entity/offshore-pump/hr-offshore-pump_West-legs.png",
          width = 108,
          height = 64,
          shift = util.by_pixel(-6, 12),
          scale = 0.5
        }
      }
    },
    underwater_pictures =
    {
      north =
      {
        filename = "__base__/graphics/entity/offshore-pump/offshore-pump_North-underwater.png",
        width = 52,
        height = 16,
        shift = util.by_pixel(-2, -34),
        hr_version =
        {
          filename = "__base__/graphics/entity/offshore-pump/hr-offshore-pump_North-underwater.png",
          width = 98,
          height = 36,
          shift = util.by_pixel(-1, -32),
          scale = 0.5
        }
      },
      east =
      {
        filename = "__base__/graphics/entity/offshore-pump/offshore-pump_East-underwater.png",
        width = 18,
        height = 38,
        shift = util.by_pixel(40, 16),
        hr_version =
        {
          filename = "__base__/graphics/entity/offshore-pump/hr-offshore-pump_East-underwater.png",
          width = 40,
          height = 72,
          shift = util.by_pixel(39, 17),
          scale = 0.5
        }
      },
      south =
      {
        filename = "__base__/graphics/entity/offshore-pump/offshore-pump_South-underwater.png",
        width = 52,
        height = 26,
        shift = util.by_pixel(-2, 48),
        hr_version =
        {
          filename = "__base__/graphics/entity/offshore-pump/hr-offshore-pump_South-underwater.png",
          width = 98,
          height = 48,
          shift = util.by_pixel(-1, 49),
          scale = 0.5
        }
      },
      west =
      {
        filename = "__base__/graphics/entity/offshore-pump/offshore-pump_West-underwater.png",
        width = 20,
        height = 34,
        shift = util.by_pixel(-40, 18),
        hr_version =
        {
          filename = "__base__/graphics/entity/offshore-pump/hr-offshore-pump_West-underwater.png",
          width = 40,
          height = 72,
          shift = util.by_pixel(-40, 17),
          scale = 0.5
        }
      }
    }
  },
  placeable_position_visualization =
  {
    filename = "__core__/graphics/cursor-boxes-32x32.png",
    priority = "extra-high-no-scale",
    width = 64,
    height = 64,
    scale = 0.5,
    x = 3 * 64
  },
  circuit_wire_connection_points = circuit_connector_definitions["offshore-pump"].points,
  circuit_connector_sprites = circuit_connector_definitions["offshore-pump"].sprites,
  circuit_wire_max_distance = default_circuit_wire_max_distance,
  water_reflection =
  {
    pictures =
    {
      filename = "__base__/graphics/entity/offshore-pump/offshore-pump-reflection.png",
      priority = "extra-high",
      width = 132,
      height = 156,
      shift = util.by_pixel(0, 19),
      variation_count = 4,
      scale = 1
    },
    rotate = false,
    orientation_to_variation = true
  }
},
  --Growing plot
   {
    type = "assembling-machine",
    icon_size = 64,
    name = "growing-plot",
    icon = "__tanks_for_bob_fork__/graphics/icons/placeholder.png",
    flags = {"placeable-neutral", "placeable-player", "player-creation"},
    minable = {hardness = 0.2, mining_time = 0.5, result = "growing-plot"},
    max_health = 100,
    corpse = "big-remnants",
    dying_explosion = "medium-explosion",
    resistances = {
        {
            type = "fire",
            percent = 95
        }
    },
    open_sound = {filename = "__base__/sound/machine-open.ogg", volume = 0.85},
    close_sound = {filename = "__base__/sound/machine-close.ogg", volume = 0.75},
    working_sound = {
        sound = {
            {
                filename = "__base__/sound/furnace.ogg",
                volume = 0.8
            },
            {
                filename = "__base__/sound/furnace.ogg",
                volume = 0.8
            },
        },
        idle_sound = {filename = "__base__/sound/idle1.ogg", volume = 0.6},
        apparent_volume = 1.5,
    },
    collision_box = {{-1.2, -1.2}, {1.2, 1.2}},
    selection_box = {{-1.5, -1.5}, {1.5, 1.5}},
    animation = {
        filename = "__tanks_for_bob_fork__/graphics/entity/new/placeholder.png",
        priority = "high",
        width = 64,
        height = 64,
        frame_count = 1,
        line_length = 1,
        shift = {0.00, -0.00}
    },
    crafting_categories = {"Seablock"},
    crafting_speed = 0.30,
    energy_source = {
        type = "burner",
        fuel_category = "chemical",
        effectivity = 1,
        fuel_inventory_size = 1,
        emissions_per_minute = 2,
        light_flicker = {
            color = {0, 0, 0},
            minimum_intensity = 0.6,
            maximum_intensity = 0.95
        },
        smoke = {
            {
                name = "smoke",
                deviation = {0.1, 0.1},
                frequency = 5,
                position = {0.0, -0.8},
                starting_vertical_speed = 0.08,
                starting_frame_deviation = 60
            }
        }
    },
    working_visualisations = {
        {
            animation = {
                filename = "__tanks_for_bob_fork__/graphics/entity/new/placeholder.png",
                priority = "high",
                width = 64,
                height = 64,
                frame_count = 1,
                line_length = 1,
                shift = {0.00, -0.00}
            },
            light = {intensity = 0.4, size = 6}
        }
    },
    energy_usage = "20kW",
    ingredient_count = 6,
    module_specification = {module_slots = 0},
},
--woodbasin
{
    type = "storage-tank",
    name = "wood-basin",
    icon = "__base__/graphics/icons/storage-tank.png",
    icon_size = 64, icon_mipmaps = 4,
    flags = {"placeable-player", "player-creation"},
    minable = {mining_time = 0.5, result = "storage-tank"},
    max_health = 100,
    corpse = "storage-tank-remnants",
    dying_explosion = "storage-tank-explosion",
    collision_box = {{-1.3, -1.3}, {1.3, 1.3}},
    selection_box = {{-1.5, -1.5}, {1.5, 1.5}},
    fluid_box =
    {
      base_area = 250,
      pipe_covers = pipecoverspictures(),
      pipe_connections =
      {
        { position = {-1, -2} },
        { position = {2, 1} },
        { position = {1, 2} },
        { position = {-2, -1} }
      },
      hide_connection_info = true
    },
    two_direction_only = true,
    window_bounding_box = {{-0.125, 0.6875}, {0.1875, 1.1875}},
    pictures =
    {
      picture =
      {
        sheets =
        {
          {
            filename = "__base__/graphics/entity/storage-tank/storage-tank.png",
            priority = "extra-high",
            frames = 2,
            width = 110,
            height = 108,
            shift = util.by_pixel(0, 4),
            hr_version =
            {
              filename = "__base__/graphics/entity/storage-tank/hr-storage-tank.png",
              priority = "extra-high",
              frames = 2,
              width = 219,
              height = 215,
              shift = util.by_pixel(-0.25, 3.75),
              scale = 0.5
            }
          },
          {
            filename = "__base__/graphics/entity/storage-tank/storage-tank-shadow.png",
            priority = "extra-high",
            frames = 2,
            width = 146,
            height = 77,
            shift = util.by_pixel(30, 22.5),
            draw_as_shadow = true,
            hr_version =
            {
              filename = "__base__/graphics/entity/storage-tank/hr-storage-tank-shadow.png",
              priority = "extra-high",
              frames = 2,
              width = 291,
              height = 153,
              shift = util.by_pixel(29.75, 22.25),
              scale = 0.5,
              draw_as_shadow = true
            }
          }
        }
      },
      fluid_background =
      {
        filename = "__base__/graphics/entity/storage-tank/fluid-background.png",
        priority = "extra-high",
        width = 32,
        height = 15
      },
      window_background =
      {
        filename = "__base__/graphics/entity/storage-tank/window-background.png",
        priority = "extra-high",
        width = 17,
        height = 24,
        hr_version =
        {
          filename = "__base__/graphics/entity/storage-tank/hr-window-background.png",
          priority = "extra-high",
          width = 34,
          height = 48,
          scale = 0.5
        }
      },
      flow_sprite =
      {
        filename = "__base__/graphics/entity/pipe/fluid-flow-low-temperature.png",
        priority = "extra-high",
        width = 160,
        height = 20
      },
      gas_flow =
      {
        filename = "__base__/graphics/entity/pipe/steam.png",
        priority = "extra-high",
        line_length = 10,
        width = 24,
        height = 15,
        frame_count = 60,
        axially_symmetrical = false,
        direction_count = 1,
        animation_speed = 0.25,
        hr_version =
        {
          filename = "__base__/graphics/entity/pipe/hr-steam.png",
          priority = "extra-high",
          line_length = 10,
          width = 48,
          height = 30,
          frame_count = 60,
          axially_symmetrical = false,
          animation_speed = 0.25,
          direction_count = 1,
          scale = 0.5
        }
      }
    },
    flow_length_in_ticks = 360,
    working_sound =
    {
      sound =
      {
          filename = "__base__/sound/storage-tank.ogg",
          volume = 0.6
      },
      match_volume_to_activity = true,
      audible_distance_modifier = 0.5,
      max_sounds_per_type = 3
    },

    circuit_wire_connection_points = circuit_connector_definitions["storage-tank"].points,
    circuit_connector_sprites = circuit_connector_definitions["storage-tank"].sprites,
    circuit_wire_max_distance = default_circuit_wire_max_distance,
    water_reflection =
    {
      pictures =
      {
        filename = "__base__/graphics/entity/storage-tank/storage-tank-reflection.png",
        priority = "extra-high",
        width = 24,
        height = 24,
        shift = util.by_pixel(5, 35),
        variation_count = 1,
        scale = 5
      },
      rotate = false,
      orientation_to_variation = false
    }
  },
--quarry
 {
    type = "assembling-machine",
    icon_size = 64,
    name = "quarry",
    icon = "__tanks_for_bob_fork__/graphics/icons/placeholder.png",
    flags = {"placeable-neutral", "placeable-player", "player-creation"},
    minable = {hardness = 0.2, mining_time = 0.5, result = "quarry"},
    max_health = 100,
    corpse = "big-remnants",
    dying_explosion = "medium-explosion",
    resistances = {
        {
            type = "fire",
            percent = 95
        }
    },
    open_sound = {filename = "__base__/sound/machine-open.ogg", volume = 0.85},
    close_sound = {filename = "__base__/sound/machine-close.ogg", volume = 0.75},
    working_sound = {
        sound = {
            {
                filename = "__base__/sound/furnace.ogg",
                volume = 0.8
            },
            {
                filename = "__base__/sound/furnace.ogg",
                volume = 0.8
            },
        },
        idle_sound = {filename = "__base__/sound/idle1.ogg", volume = 0.6},
        apparent_volume = 1.5,
    },
    collision_box = {{-1.2, -1.2}, {1.2, 1.2}},
    selection_box = {{-1.5, -1.5}, {1.5, 1.5}},
    animation = {
        filename = "__tanks_for_bob_fork__/graphics/entity/new/placeholder.png",
        priority = "high",
        width = 64,
        height = 64,
        frame_count = 1,
        line_length = 1,
        shift = {0.00, -0.00}
    },
    crafting_categories = {"quarry"},
    crafting_speed = 0.30,
    energy_source = {
        type = "burner",
        fuel_category = "chemical",
        effectivity = 1,
        fuel_inventory_size = 1,
        emissions_per_minute = 2,
        light_flicker = {
            color = {0, 0, 0},
            minimum_intensity = 0.6,
            maximum_intensity = 0.95
        },
        smoke = {
            {
                name = "smoke",
                deviation = {0.1, 0.1},
                frequency = 5,
                position = {0.0, -0.8},
                starting_vertical_speed = 0.08,
                starting_frame_deviation = 60
            }
        }
    },
    working_visualisations = {
        {
            animation = {
                filename = "__tanks_for_bob_fork__/graphics/entity/new/placeholder.png",
                priority = "high",
                width = 64,
                height = 64,
                frame_count = 1,
                line_length = 1,
                shift = {0.00, -0.00}
            },
            light = {intensity = 0.4, size = 6}
        }
    },
    energy_usage = "5kW",
    ingredient_count = 3,
    module_specification = {module_slots = 0},
},
--woodbasin
{
    type = "storage-tank",
    name = "wood-basin",
    icon = "__base__/graphics/icons/storage-tank.png",
    icon_size = 64, icon_mipmaps = 4,
    flags = {"placeable-player", "player-creation"},
    minable = {mining_time = 0.5, result = "storage-tank"},
    max_health = 100,
    corpse = "storage-tank-remnants",
    dying_explosion = "storage-tank-explosion",
    collision_box = {{-1.3, -1.3}, {1.3, 1.3}},
    selection_box = {{-1.5, -1.5}, {1.5, 1.5}},
    fluid_box =
    {
      base_area = 250,
      pipe_covers = pipecoverspictures(),
      pipe_connections =
      {
        { position = {-1, -2} },
        { position = {2, 1} },
        { position = {1, 2} },
        { position = {-2, -1} }
      },
      hide_connection_info = true
    },
    two_direction_only = true,
    window_bounding_box = {{-0.125, 0.6875}, {0.1875, 1.1875}},
    pictures =
    {
      picture =
      {
        sheets =
        {
          {
            filename = "__base__/graphics/entity/storage-tank/storage-tank.png",
            priority = "extra-high",
            frames = 2,
            width = 110,
            height = 108,
            shift = util.by_pixel(0, 4),
            hr_version =
            {
              filename = "__base__/graphics/entity/storage-tank/hr-storage-tank.png",
              priority = "extra-high",
              frames = 2,
              width = 219,
              height = 215,
              shift = util.by_pixel(-0.25, 3.75),
              scale = 0.5
            }
          },
          {
            filename = "__base__/graphics/entity/storage-tank/storage-tank-shadow.png",
            priority = "extra-high",
            frames = 2,
            width = 146,
            height = 77,
            shift = util.by_pixel(30, 22.5),
            draw_as_shadow = true,
            hr_version =
            {
              filename = "__base__/graphics/entity/storage-tank/hr-storage-tank-shadow.png",
              priority = "extra-high",
              frames = 2,
              width = 291,
              height = 153,
              shift = util.by_pixel(29.75, 22.25),
              scale = 0.5,
              draw_as_shadow = true
            }
          }
        }
      },
      fluid_background =
      {
        filename = "__base__/graphics/entity/storage-tank/fluid-background.png",
        priority = "extra-high",
        width = 32,
        height = 15
      },
      window_background =
      {
        filename = "__base__/graphics/entity/storage-tank/window-background.png",
        priority = "extra-high",
        width = 17,
        height = 24,
        hr_version =
        {
          filename = "__base__/graphics/entity/storage-tank/hr-window-background.png",
          priority = "extra-high",
          width = 34,
          height = 48,
          scale = 0.5
        }
      },
      flow_sprite =
      {
        filename = "__base__/graphics/entity/pipe/fluid-flow-low-temperature.png",
        priority = "extra-high",
        width = 160,
        height = 20
      },
      gas_flow =
      {
        filename = "__base__/graphics/entity/pipe/steam.png",
        priority = "extra-high",
        line_length = 10,
        width = 24,
        height = 15,
        frame_count = 60,
        axially_symmetrical = false,
        direction_count = 1,
        animation_speed = 0.25,
        hr_version =
        {
          filename = "__base__/graphics/entity/pipe/hr-steam.png",
          priority = "extra-high",
          line_length = 10,
          width = 48,
          height = 30,
          frame_count = 60,
          axially_symmetrical = false,
          animation_speed = 0.25,
          direction_count = 1,
          scale = 0.5
        }
      }
    },
    flow_length_in_ticks = 360,
    working_sound =
    {
      sound =
      {
          filename = "__base__/sound/storage-tank.ogg",
          volume = 0.6
      },
      match_volume_to_activity = true,
      audible_distance_modifier = 0.5,
      max_sounds_per_type = 3
    },

    circuit_wire_connection_points = circuit_connector_definitions["storage-tank"].points,
    circuit_connector_sprites = circuit_connector_definitions["storage-tank"].sprites,
    circuit_wire_max_distance = default_circuit_wire_max_distance,
    water_reflection =
    {
      pictures =
      {
        filename = "__base__/graphics/entity/storage-tank/storage-tank-reflection.png",
        priority = "extra-high",
        width = 24,
        height = 24,
        shift = util.by_pixel(5, 35),
        variation_count = 1,
        scale = 5
      },
      rotate = false,
      orientation_to_variation = false
    }
  },

  --boiler
  {
    type = "boiler",
    name = "solar-boiler",
    icon = "__base__/graphics/icons/boiler.png",
    icon_size = 64, icon_mipmaps = 4,
    flags = {"placeable-neutral", "player-creation"},
    minable = {mining_time = 0.2, result = "solar-boiler"},
    max_health = 100,
    corpse = "boiler-remnants",
    dying_explosion = "boiler-explosion",
    mode = "output-to-separate-pipe",
    resistances =
    {
      {
        type = "fire",
        percent = 10
      },
      {
        type = "explosion",
        percent = 30
      },
      {
        type = "impact",
        percent = 30
      }
    },
    collision_box = {{-1.29, -0.79}, {1.29, 0.79}},
    selection_box = {{-1.5, -1}, {1.5, 1}},
    target_temperature = 105,
    fluid_box =
    {
      base_area = 1,
      height = 2,
      base_level = -1,
      pipe_covers = pipecoverspictures(),
      pipe_connections =
      {
        {type = "input-output", position = {-2, 0.5}},
        {type = "input-output", position = {2, 0.5}}
      },
      production_type = "input-output",
      filter = "water"
    },
    output_fluid_box =
    {
      base_area = 1,
      height = 2,
      base_level = 1,
      pipe_covers = pipecoverspictures(),
      pipe_connections =
      {
        {type = "output", position = {0, -1.5}}
      },
      production_type = "output",
      filter = "steam"
    },
    energy_consumption = "1MW",
    energy_source =
    {
      type = "burner",
      fuel_category = "chemical",
      effectivity = 5,
      fuel_inventory_size = 1,
      emissions_per_minute = 3,
      light_flicker =
      {
        color = {0,0,0},
        minimum_intensity = 0.6,
        maximum_intensity = 0.95
      },
      smoke =
      {
        {
          name = "smoke",
          north_position = util.by_pixel(-38, -47.5),
          south_position = util.by_pixel(38.5, -32),
          east_position = util.by_pixel(20, -70),
          west_position = util.by_pixel(-19, -8.5),
          frequency = 15,
          starting_vertical_speed = 0.0,
          starting_frame_deviation = 60
        }
      }
    },
    working_sound =
    {
      sound =
      {
        filename = "__base__/sound/boiler.ogg",
        volume = 0.7
      },
      --max_sounds_per_type = 3,
      audible_distance_modifier = 0.3,
      fade_in_ticks = 4,
      fade_out_ticks = 20
    },

    structure =
    {
      north =
      {
        layers =
        {
          {
            filename = "__base__/graphics/entity/boiler/boiler-N-idle.png",
            priority = "extra-high",
            width = 131,
            height = 108,
            shift = util.by_pixel(-0.5, 4),
            hr_version =
            {
              filename = "__base__/graphics/entity/boiler/hr-boiler-N-idle.png",
              priority = "extra-high",
              width = 269,
              height = 221,
              shift = util.by_pixel(-1.25, 5.25),
              scale = 0.5
            }
          },
          {
            filename = "__base__/graphics/entity/boiler/boiler-N-shadow.png",
            priority = "extra-high",
            width = 137,
            height = 82,
            shift = util.by_pixel(20.5, 9),
            draw_as_shadow = true,
            hr_version =
            {
              filename = "__base__/graphics/entity/boiler/hr-boiler-N-shadow.png",
              priority = "extra-high",
              width = 274,
              height = 164,
              scale = 0.5,
              shift = util.by_pixel(20.5, 9),
              draw_as_shadow = true
            }
          }
        }
      },
      east =
      {
        layers =
        {
          {
            filename = "__base__/graphics/entity/boiler/boiler-E-idle.png",
            priority = "extra-high",
            width = 105,
            height = 147,
            shift = util.by_pixel(-3.5, -0.5),
            hr_version =
            {
              filename = "__base__/graphics/entity/boiler/hr-boiler-E-idle.png",
              priority = "extra-high",
              width = 216,
              height = 301,
              shift = util.by_pixel(-3, 1.25),
              scale = 0.5
            }
          },
          {
            filename = "__base__/graphics/entity/boiler/boiler-E-shadow.png",
            priority = "extra-high",
            width = 92,
            height = 97,
            shift = util.by_pixel(30, 9.5),
            draw_as_shadow = true,
            hr_version =
            {
              filename = "__base__/graphics/entity/boiler/hr-boiler-E-shadow.png",
              priority = "extra-high",
              width = 184,
              height = 194,
              scale = 0.5,
              shift = util.by_pixel(30, 9.5),
              draw_as_shadow = true
            }
          }
        }
      },
      south =
      {
        layers =
        {
          {
            filename = "__base__/graphics/entity/boiler/boiler-S-idle.png",
            priority = "extra-high",
            width = 128,
            height = 95,
            shift = util.by_pixel(3, 12.5),
            hr_version =
            {
              filename = "__base__/graphics/entity/boiler/hr-boiler-S-idle.png",
              priority = "extra-high",
              width = 260,
              height = 192,
              shift = util.by_pixel(4, 13),
              scale = 0.5
            }
          },
          {
            filename = "__base__/graphics/entity/boiler/boiler-S-shadow.png",
            priority = "extra-high",
            width = 156,
            height = 66,
            shift = util.by_pixel(30, 16),
            draw_as_shadow = true,
            hr_version =
            {
              filename = "__base__/graphics/entity/boiler/hr-boiler-S-shadow.png",
              priority = "extra-high",
              width = 311,
              height = 131,
              scale = 0.5,
              shift = util.by_pixel(29.75, 15.75),
              draw_as_shadow = true
            }
          }
        }
      },
      west =
      {
        layers =
        {
          {
            filename = "__base__/graphics/entity/boiler/boiler-W-idle.png",
            priority = "extra-high",
            width = 96,
            height = 132,
            shift = util.by_pixel(1, 5),
            hr_version =
            {
              filename = "__base__/graphics/entity/boiler/hr-boiler-W-idle.png",
              priority = "extra-high",
              width = 196,
              height = 273,
              shift = util.by_pixel(1.5, 7.75),
              scale = 0.5
            }
          },
          {
            filename = "__base__/graphics/entity/boiler/boiler-W-shadow.png",
            priority = "extra-high",
            width = 103,
            height = 109,
            shift = util.by_pixel(19.5, 6.5),
            draw_as_shadow = true,
            hr_version =
            {
              filename = "__base__/graphics/entity/boiler/hr-boiler-W-shadow.png",
              priority = "extra-high",
              width = 206,
              height = 218,
              scale = 0.5,
              shift = util.by_pixel(19.5, 6.5),
              draw_as_shadow = true
            }
          }
        }
      }
    },

    patch =
    {
      east =
      {
        filename = "__base__/graphics/entity/boiler/boiler-E-patch.png",
        priority = "extra-high",
        width = 3,
        height = 17,
        shift = util.by_pixel(33.5, -13.5),
        hr_version =
        {
          filename = "__base__/graphics/entity/boiler/hr-boiler-E-patch.png",
          width = 6,
          height = 36,
          shift = util.by_pixel(33.5, -13.5),
          scale = 0.5
        }
      }
    },

    fire_flicker_enabled = true,
    fire =
    {
      north =
      {
        filename = "__base__/graphics/entity/boiler/boiler-N-fire.png",
        draw_as_glow = true,
        priority = "extra-high",
        frame_count = 64,
        line_length = 8,
        width = 12,
        height = 13,
        animation_speed = 0.5,
        shift = util.by_pixel(0, -8.5),
        hr_version =
        {
          filename = "__base__/graphics/entity/boiler/hr-boiler-N-fire.png",
          draw_as_glow = true,
          priority = "extra-high",
          frame_count = 64,
          line_length = 8,
          width = 26,
          height = 26,
          animation_speed = 0.5,
          shift = util.by_pixel(0, -8.5),
          scale = 0.5
        }
      },
      east =
      {
        filename = "__base__/graphics/entity/boiler/boiler-E-fire.png",
        draw_as_glow = true,
        priority = "extra-high",
        frame_count = 64,
        line_length = 8,
        width = 14,
        height = 14,
        animation_speed = 0.5,
        shift = util.by_pixel(-10, -22),
        hr_version =
        {
          filename = "__base__/graphics/entity/boiler/hr-boiler-E-fire.png",
          draw_as_glow = true,
          priority = "extra-high",
          frame_count = 64,
          line_length = 8,
          width = 28,
          height = 28,
          animation_speed = 0.5,
          shift = util.by_pixel(-9.5, -22),
          scale = 0.5
        }
      },
      south =
      {
        filename = "__base__/graphics/entity/boiler/boiler-S-fire.png",
        draw_as_glow = true,
        priority = "extra-high",
        frame_count = 64,
        line_length = 8,
        width = 12,
        height = 9,
        animation_speed = 0.5,
        shift = util.by_pixel(-1, -26.5),
        hr_version =
        {
          filename = "__base__/graphics/entity/boiler/hr-boiler-S-fire.png",
          draw_as_glow = true,
          priority = "extra-high",
          frame_count = 64,
          line_length = 8,
          width = 26,
          height = 16,
          animation_speed = 0.5,
          shift = util.by_pixel(-1, -26.5),
          scale = 0.5
        }
      },
      west =
      {
        filename = "__base__/graphics/entity/boiler/boiler-W-fire.png",
        draw_as_glow = true,
        priority = "extra-high",
        frame_count = 64,
        line_length = 8,
        width = 14,
        height = 14,
        animation_speed = 0.5,
        shift = util.by_pixel(13, -23),
        hr_version =
        {
          filename = "__base__/graphics/entity/boiler/hr-boiler-W-fire.png",
          draw_as_glow = true,
          priority = "extra-high",
          frame_count = 64,
          line_length = 8,
          width = 30,
          height = 29,
          animation_speed = 0.5,
          shift = util.by_pixel(13, -23.25),
          scale = 0.5
        }
      }
    },

    fire_glow_flicker_enabled = true,

    fire_glow =
    {
      north =
      {
        filename = "__base__/graphics/entity/boiler/boiler-N-light.png",
        draw_as_glow = true,
        priority = "extra-high",
        frame_count = 1,
        width = 100,
        height = 87,
        shift = util.by_pixel(-1, -6.5),
        blend_mode = "additive",
        hr_version =
        {
          filename = "__base__/graphics/entity/boiler/hr-boiler-N-light.png",
          draw_as_glow = true,
          priority = "extra-high",
          frame_count = 1,
          width = 200,
          height = 173,
          shift = util.by_pixel(-1, -6.75),
          blend_mode = "additive",
          scale = 0.5
        }
      },
      east =
      {
        filename = "__base__/graphics/entity/boiler/boiler-E-light.png",
        draw_as_glow = true,
        priority = "extra-high",
        frame_count = 1,
        width = 70,
        height = 122,
        shift = util.by_pixel(0, -13),
        blend_mode = "additive",
        hr_version =
        {
          filename = "__base__/graphics/entity/boiler/hr-boiler-E-light.png",
          draw_as_glow = true,
          priority = "extra-high",
          frame_count = 1,
          width = 139,
          height = 244,
          shift = util.by_pixel(0.25, -13),
          blend_mode = "additive",
          scale = 0.5
        }
      },
      south =
      {
        filename = "__base__/graphics/entity/boiler/boiler-S-light.png",
        draw_as_glow = true,
        priority = "extra-high",
        frame_count = 1,
        width = 100,
        height = 81,
        shift = util.by_pixel(1, 5.5),
        blend_mode = "additive",
        hr_version =
        {
          filename = "__base__/graphics/entity/boiler/hr-boiler-S-light.png",
          draw_as_glow = true,
          priority = "extra-high",
          frame_count = 1,
          width = 200,
          height = 162,
          shift = util.by_pixel(1, 5.5),
          blend_mode = "additive",
          scale = 0.5
        }
      },
      west =
      {
        filename = "__base__/graphics/entity/boiler/boiler-W-light.png",
        draw_as_glow = true,
        priority = "extra-high",
        frame_count = 1,
        width = 68,
        height = 109,
        shift = util.by_pixel(2, -6.5),
        blend_mode = "additive",
        hr_version =
        {
          filename = "__base__/graphics/entity/boiler/hr-boiler-W-light.png",
          draw_as_glow = true,
          priority = "extra-high",
          frame_count = 1,
          width = 136,
          height = 217,
          shift = util.by_pixel(2, -6.25),
          blend_mode = "additive",
          scale = 0.5
        }
      }
    },
    burning_cooldown = 20,
    water_reflection = boiler_reflection()
  },
--cooking-fire
 {
    type = "assembling-machine",
    icon_size = 64,
    name = "cooking-fire",
    icon = "__tanks_for_bob_fork__/graphics/icons/placeholder.png",
    flags = {"placeable-neutral", "placeable-player", "player-creation"},
    minable = {hardness = 0.2, mining_time = 0.5, result = "cooking-fire"},
    max_health = 100,
    corpse = "big-remnants",
    dying_explosion = "medium-explosion",
    resistances = {
        {
            type = "fire",
            percent = 95
        }
    },
    open_sound = {filename = "__base__/sound/machine-open.ogg", volume = 0.85},
    close_sound = {filename = "__base__/sound/machine-close.ogg", volume = 0.75},
    working_sound = {
        sound = {
            {
                filename = "__base__/sound/furnace.ogg",
                volume = 0.8
            },
            {
                filename = "__base__/sound/furnace.ogg",
                volume = 0.8
            },
        },
        idle_sound = {filename = "__base__/sound/idle1.ogg", volume = 0.6},
        apparent_volume = 1.5,
    },
    collision_box = {{-1.2, -1.2}, {1.2, 1.2}},
    selection_box = {{-1.5, -1.5}, {1.5, 1.5}},
    animation = {
        filename = "__tanks_for_bob_fork__/graphics/entity/new/placeholder.png",
        priority = "high",
        width = 64,
        height = 64,
        frame_count = 1,
        line_length = 1,
        shift = {0.00, -0.00}
    },
    crafting_categories = {"Seablock"},
    crafting_speed = 0.60,
    energy_source = {
        type = "burner",
        fuel_category = "chemical",
        effectivity = 1,
        fuel_inventory_size = 1,
        emissions_per_minute = 6,
        light_flicker = {
            color = {0, 0, 0},
            minimum_intensity = 0.6,
            maximum_intensity = 0.95
        },
        smoke = {
            {
                name = "smoke",
                deviation = {0.1, 0.1},
                frequency = 15,
                position = {0.0, -0.8},
                starting_vertical_speed = 0.08,
                starting_frame_deviation = 60
            }
        }
    },
    working_visualisations = {
        {
            animation = {
                filename = "__tanks_for_bob_fork__/graphics/entity/new/placeholder.png",
                priority = "high",
                width = 64,
                height = 64,
                frame_count = 1,
                line_length = 1,
                shift = {0.00, -0.00}
            },
            light = {intensity = 0.4, size = 6}
        }
    },
    energy_usage = "15kW",
    ingredient_count = 4,
    module_specification = {module_slots = 0},
},

--pump?

 {
    type = "pump",
    name = "primitive-steam-powered-pump",
    icon = "__base__/graphics/icons/pump.png",
    icon_size = 64, icon_mipmaps = 4,
    flags = {"placeable-neutral", "player-creation"},
    minable = {mining_time = 0.2, result = "primitive-steam-powered-pump"},
    max_health = 180,
    fast_replaceable_group = "pipe",
    corpse = "pump-remnants",
    dying_explosion = "pump-explosion",
    collision_box = {{-0.29, -0.9}, {0.29, 0.9}},
    selection_box = {{-0.5, -1}, {0.5, 1}},
    working_sound =
    {
      sound =
      {
          filename = "__base__/sound/pump.ogg",
          volume = 0.3
      },
      audible_distance_modifier = 0.5,
      max_sounds_per_type = 2
    },
       resistances =
    {
      {
        type = "fire",
        percent = 80
      },
      {
        type = "impact",
        percent = 30
      }
    },
    fluid_box =
    {
      base_area = 1,
      height = 4,
      pipe_covers = pipecoverspictures(),
      pipe_connections =
      {
        { position = {0, -1.5}, type="output" },
        { position = {0, 1.5}, type="input" }
      }
    },
    energy_source =
    {
        type = "burner",
        fuel_category = "chemical",
        effectivity = 1,
        fuel_inventory_size = 1,
        emissions_per_minute = 6,
        light_flicker = {
            color = {0, 0, 0},
            minimum_intensity = 0.6,
            maximum_intensity = 0.95
        },
        smoke = {
            {
                name = "smoke",
                deviation = {0.1, 0.1},
                frequency = 15,
                position = {0.0, -0.8},
                starting_vertical_speed = 0.08,
                starting_frame_deviation = 60
            }
        }
    },
    energy_usage = "25kW",
    pumping_speed = 100,

    animations =
    {
      north =
      {
        filename = "__base__/graphics/entity/pump/pump-north.png",
        width = 53,
        height = 79,
        line_length =8,
        frame_count =32,
        animation_speed = 0.5,
        shift = util.by_pixel(8.000, 7.500),
        hr_version =
        {
          filename = "__base__/graphics/entity/pump/hr-pump-north.png",
          width = 103,
          height = 164,
          scale = 0.5,
          line_length =8,
          frame_count =32,
          animation_speed = 0.5,
          shift = util.by_pixel(8, 3.5) -- {0.515625, 0.21875}
        }
      },
      east =
      {
        filename = "__base__/graphics/entity/pump/pump-east.png",
        width = 66,
        height = 60,
        line_length =8,
        frame_count =32,
        animation_speed = 0.5,
        shift = util.by_pixel(0, 4),
        hr_version =
        {
          filename = "__base__/graphics/entity/pump/hr-pump-east.png",
          width = 130,
          height = 109,
          scale = 0.5,
          line_length =8,
          frame_count =32,
          animation_speed = 0.5,
          shift = util.by_pixel(-0.5, 1.75) --{-0.03125, 0.109375}
        }
      },

      south =
      {
        filename = "__base__/graphics/entity/pump/pump-south.png",
        width = 62,
        height = 87,
        line_length =8,
        frame_count =32,
        animation_speed = 0.5,
        shift = util.by_pixel(13.5, 0.5),
        hr_version =
        {
          filename = "__base__/graphics/entity/pump/hr-pump-south.png",
          width = 114,
          height = 160,
          scale = 0.5,
          line_length =8,
          frame_count =32,
          animation_speed = 0.5,
          shift = util.by_pixel(12.5, -8) -- {0.75, -0.5}
        }
      },
      west =
      {
        filename = "__base__/graphics/entity/pump/pump-west.png",
        width = 69,
        height = 51,
        line_length =8,
        frame_count =32,
        animation_speed = 0.5,
        shift = util.by_pixel(0.5, -0.5),
        hr_version =
        {
          filename = "__base__/graphics/entity/pump/hr-pump-west.png",
          width = 131,
          height = 111,
          scale = 0.5,
          line_length =8,
          frame_count =32,
          animation_speed = 0.5,
          shift = util.by_pixel(-0.25, 1.25) -- {-0.015625, 0.078125}
        }
      }
    },

    fluid_wagon_connector_frame_count = 35,
    fluid_wagon_connector_alignment_tolerance = 2.0 / 32.0,



    fluid_animation =
    {
      north =
      {
        filename = "__base__/graphics/entity/pump/pump-north-liquid.png",
        apply_runtime_tint = true,
        width = 20,
        height = 13,
        line_length =8,
        frame_count =32,
        shift = util.by_pixel(-0.500, -14.500),
        hr_version =
        {
          filename = "__base__/graphics/entity/pump/hr-pump-north-liquid.png",
          apply_runtime_tint = true,
          width = 38,
          height = 22,
          scale = 0.5,
          line_length =8,
          frame_count =32,
          shift = util.by_pixel(-0.250, -16.750)
        }
      },

      east =
      {
        filename = "__base__/graphics/entity/pump/pump-east-liquid.png",
        width = 18,
        height = 24,
        line_length =8,
        frame_count =32,
        shift = util.by_pixel(6, -8),
        hr_version =
        {
          filename = "__base__/graphics/entity/pump/hr-pump-east-liquid.png",
          width = 35,
          height = 46,
          scale = 0.5,
          line_length =8,
          frame_count =32,
          shift = util.by_pixel(6.25, -8.5)
        }
      },

      south =
      {
        filename = "__base__/graphics/entity/pump/pump-south-liquid.png",
        width = 26,
        height = 55,
        line_length =8,
        frame_count =32,
        shift = util.by_pixel(3.5, 6.5),
        hr_version =
        {
          filename = "__base__/graphics/entity/pump/hr-pump-south-liquid.png",
          width = 38,
          height = 45,
          scale = 0.5,
          line_length =8,
          frame_count =32,
          shift = util.by_pixel(0.5, -9.25)
        }
      },
      west =
      {
        filename = "__base__/graphics/entity/pump/pump-west-liquid.png",
        width = 18,
        height = 24,
        line_length =8,
        frame_count =32,
        shift = util.by_pixel(-6, -9),
        hr_version =
        {
          filename = "__base__/graphics/entity/pump/hr-pump-west-liquid.png",
          width = 35,
          height = 47,
          scale = 0.5,
          line_length =8,
          frame_count =32,
          shift = util.by_pixel(-6.5, -9.5)
        }
      }
    },

    glass_pictures =
    {
      north =
      {
        filename = "__base__/graphics/entity/pump/pump-north-glass.png",
        width = 32,
        height = 64,
        hr_version =
        {
          filename = "__base__/graphics/entity/pump/hr-pump-north-glass.png",
          width = 64,
          height = 128,
          scale = 0.5
        }
      },
      east =
      {
        filename = "__base__/graphics/entity/pump/pump-east-glass.png",
        width = 32,
        height = 32,
        shift = util.by_pixel(0, -16),
        hr_version =
        {
          filename = "__base__/graphics/entity/pump/hr-pump-east-glass.png",
          width = 128,
          height = 192,
          scale = 0.5
        }
      },
      south =
      {
        filename = "__base__/graphics/entity/pump/pump-south-glass.png",
        width = 32,
        height = 64,
        hr_version =
        {
          filename = "__base__/graphics/entity/pump/hr-pump-south-glass.png",
          width = 64,
          height = 128,
          scale = 0.5
        }
      },
      west =
      {
        filename = "__base__/graphics/entity/pump/pump-west-glass.png",
        width = 32,
        height = 96,
        shift = util.by_pixel(0.000, 15.000),
        hr_version =
        {
          filename = "__base__/graphics/entity/pump/hr-pump-west-glass.png",
          width = 192,
          height = 192,
          scale = 0.5,
          shift = util.by_pixel(-16, 0)
        }
      }
    },

    circuit_wire_connection_points = circuit_connector_definitions["pump"].points,
    circuit_connector_sprites = circuit_connector_definitions["pump"].sprites,
    circuit_wire_max_distance = default_circuit_wire_max_distance
  },
--fishpond
{
    type = "assembling-machine",
    icon_size = 64,
    name = "fish-pond",
    icon = "__tanks_for_bob_fork__/graphics/icons/placeholder.png",
    flags = {"placeable-neutral", "placeable-player", "player-creation"},
    minable = {hardness = 0.2, mining_time = 0.5, result = "fish-pond"},
    max_health = 100,
    corpse = "big-remnants",
    dying_explosion = "medium-explosion",
    resistances = {
        {
            type = "fire",
            percent = 95
        }
    },
    open_sound = {filename = "__base__/sound/machine-open.ogg", volume = 0.85},
    close_sound = {filename = "__base__/sound/machine-close.ogg", volume = 0.75},
    working_sound = {
        sound = {
            {
                filename = "__base__/sound/furnace.ogg",
                volume = 0.8
            },
            {
                filename = "__base__/sound/furnace.ogg",
                volume = 0.8
            },
        },
        idle_sound = {filename = "__base__/sound/idle1.ogg", volume = 0.6},
        apparent_volume = 1.5,
    },
    collision_box = {{-1.2, -1.2}, {1.2, 1.2}},
    selection_box = {{-1.5, -1.5}, {1.5, 1.5}},
    animation = {
        filename = "__tanks_for_bob_fork__/graphics/entity/new/placeholder.png",
        priority = "high",
        width = 64,
        height = 64,
        frame_count = 1,
        line_length = 1,
        shift = {0.00, -0.00}
    },
    crafting_categories = {"fish"},
    crafting_speed = 0.60,
    energy_source = {
        type = "burner",
        fuel_category = "chemical",
        effectivity = 1,
        fuel_inventory_size = 1,
        emissions_per_minute = 6,
        light_flicker = {
            color = {0, 0, 0},
            minimum_intensity = 0.6,
            maximum_intensity = 0.95
        },
        smoke = {
            {
                name = "smoke",
                deviation = {0.1, 0.1},
                frequency = 15,
                position = {0.0, -0.8},
                starting_vertical_speed = 0.08,
                starting_frame_deviation = 60
            }
        }
    },
    working_visualisations = {
        {
            animation = {
                filename = "__tanks_for_bob_fork__/graphics/entity/new/placeholder.png",
                priority = "high",
                width = 64,
                height = 64,
                frame_count = 1,
                line_length = 1,
                shift = {0.00, -0.00}
            },
            light = {intensity = 0.4, size = 6}
        }
    },
    energy_usage = "15kW",
    ingredient_count = 4,
    module_specification = {module_slots = 0},
},
--calcifier
{
    type = "assembling-machine",
    icon_size = 64,
    name = "calcifier",
    icon = "__tanks_for_bob_fork__/graphics/icons/placeholder.png",
    flags = {"placeable-neutral", "placeable-player", "player-creation"},
    minable = {hardness = 0.2, mining_time = 0.5, result = "calcifier"},
    max_health = 100,
    corpse = "big-remnants",
    dying_explosion = "medium-explosion",
    resistances = {
        {
            type = "fire",
            percent = 95
        }
    },
    open_sound = {filename = "__base__/sound/machine-open.ogg", volume = 0.85},
    close_sound = {filename = "__base__/sound/machine-close.ogg", volume = 0.75},
    working_sound = {
        sound = {
            {
                filename = "__base__/sound/furnace.ogg",
                volume = 0.8
            },
            {
                filename = "__base__/sound/furnace.ogg",
                volume = 0.8
            },
        },
        idle_sound = {filename = "__base__/sound/idle1.ogg", volume = 0.6},
        apparent_volume = 1.5,
    },
    collision_box = {{-1.2, -1.2}, {1.2, 1.2}},
    selection_box = {{-1.5, -1.5}, {1.5, 1.5}},
    animation = {
        filename = "__tanks_for_bob_fork__/graphics/entity/new/placeholder.png",
        priority = "high",
        width = 64,
        height = 64,
        frame_count = 1,
        line_length = 1,
        shift = {0.00, -0.00}
    },
    crafting_categories = {"Calcifier"},
    crafting_speed = 0.60,
    energy_source = {
        type = "burner",
        fuel_category = "chemical",
        effectivity = 1,
        fuel_inventory_size = 1,
        emissions_per_minute = 6,
        light_flicker = {
            color = {0, 0, 0},
            minimum_intensity = 0.6,
            maximum_intensity = 0.95
        },
        smoke = {
            {
                name = "smoke",
                deviation = {0.1, 0.1},
                frequency = 15,
                position = {0.0, -0.8},
                starting_vertical_speed = 0.08,
                starting_frame_deviation = 60
            }
        }
    },
    working_visualisations = {
        {
            animation = {
                filename = "__tanks_for_bob_fork__/graphics/entity/new/placeholder.png",
                priority = "high",
                width = 64,
                height = 64,
                frame_count = 1,
                line_length = 1,
                shift = {0.00, -0.00}
            },
            light = {intensity = 0.4, size = 6}
        }
    },
    energy_usage = "1kW",
    ingredient_count = 4,
    module_specification = {module_slots = 0},
},
--steam condenser 
{
    type = "assembling-machine",
    icon_size = 64,
    name = "steam-condenser",
    icon = "__tanks_for_bob_fork__/graphics/icons/placeholder.png",
    flags = {"placeable-neutral", "placeable-player", "player-creation"},
    minable = {hardness = 0.2, mining_time = 0.5, result = "steam-condenser"},
    max_health = 100,
    corpse = "big-remnants",
    dying_explosion = "medium-explosion",
    resistances = {
        {
            type = "fire",
            percent = 95
        }
    },
    open_sound = {filename = "__base__/sound/machine-open.ogg", volume = 0.85},
    close_sound = {filename = "__base__/sound/machine-close.ogg", volume = 0.75},
    working_sound = {
        sound = {
            {
                filename = "__base__/sound/furnace.ogg",
                volume = 0.8
            },
            {
                filename = "__base__/sound/furnace.ogg",
                volume = 0.8
            },
        },
        idle_sound = {filename = "__base__/sound/idle1.ogg", volume = 0.6},
        apparent_volume = 1.5,
    },
    collision_box = {{-1.2, -1.2}, {1.2, 1.2}},
    selection_box = {{-1.5, -1.5}, {1.5, 1.5}},
    animation = {
        filename = "__tanks_for_bob_fork__/graphics/entity/new/placeholder.png",
        priority = "high",
        width = 64,
        height = 64,
        frame_count = 1,
        line_length = 1,
        shift = {0.00, -0.00}
    },
    crafting_categories = {"Steam"},
    crafting_speed = 0.60,
    energy_source = {
        type = "burner",
        fuel_category = "chemical",
        effectivity = 1,
        fuel_inventory_size = 1,
        emissions_per_minute = 6,
        light_flicker = {
            color = {0, 0, 0},
            minimum_intensity = 0.6,
            maximum_intensity = 0.95
        },
        smoke = {
            {
                name = "smoke",
                deviation = {0.1, 0.1},
                frequency = 15,
                position = {0.0, -0.8},
                starting_vertical_speed = 0.08,
                starting_frame_deviation = 60
            }
        }
    },
    working_visualisations = {
        {
            animation = {
                filename = "__tanks_for_bob_fork__/graphics/entity/new/placeholder.png",
                priority = "high",
                width = 64,
                height = 64,
                frame_count = 1,
                line_length = 1,
                shift = {0.00, -0.00}
            },
            light = {intensity = 0.4, size = 6}
        }
    },
    energy_usage = "1kW",
    ingredient_count = 4,
    module_specification = {module_slots = 0},
},

--shaler
 {
    type = "assembling-machine",
    icon_size = 64,
    name = "shaler",
    icon = "__tanks_for_bob_fork__/graphics/icons/placeholder.png",
    flags = {"placeable-neutral", "placeable-player", "player-creation"},
    minable = {hardness = 0.2, mining_time = 0.5, result = "shaler"},
    max_health = 100,
    corpse = "big-remnants",
    dying_explosion = "medium-explosion",
    resistances = {
        {
            type = "fire",
            percent = 95
        }
    },
    open_sound = {filename = "__base__/sound/machine-open.ogg", volume = 0.85},
    close_sound = {filename = "__base__/sound/machine-close.ogg", volume = 0.75},
    working_sound = {
        sound = {
            {
                filename = "__base__/sound/furnace.ogg",
                volume = 0.8
            },
            {
                filename = "__base__/sound/furnace.ogg",
                volume = 0.8
            },
        },
        idle_sound = {filename = "__base__/sound/idle1.ogg", volume = 0.6},
        apparent_volume = 1.5,
    },
    collision_box = {{-1.2, -1.2}, {1.2, 1.2}},
    selection_box = {{-1.5, -1.5}, {1.5, 1.5}},
    animation = {
        filename = "__tanks_for_bob_fork__/graphics/entity/new/placeholder.png",
        priority = "high",
        width = 64,
        height = 64,
        frame_count = 1,
        line_length = 1,
        shift = {0.00, -0.00}
    },
    crafting_categories = {"shaler"},
    crafting_speed = 0.90,
    energy_source = {
        type = "burner",
        fuel_category = "chemical",
        effectivity = .5,
        fuel_inventory_size = 1,
        emissions_per_minute = 6,
        light_flicker = {
            color = {0, 0, 0},
            minimum_intensity = 0.6,
            maximum_intensity = 0.95
        },
        smoke = {
            {
                name = "smoke",
                deviation = {0.1, 0.1},
                frequency = 15,
                position = {0.0, -0.8},
                starting_vertical_speed = 0.08,
                starting_frame_deviation = 60
            }
        }
    },
    working_visualisations = {
        {
            animation = {
                filename = "__tanks_for_bob_fork__/graphics/entity/new/placeholder.png",
                priority = "high",
                width = 64,
                height = 64,
                frame_count = 1,
                line_length = 1,
                shift = {0.00, -0.00}
            },
            light = {intensity = 0.4, size = 6}
        }
    },
    energy_usage = "10kW",
    ingredient_count = 2,
    module_specification = {module_slots = 0},
},

  --claypit
   {
    type = "assembling-machine",
    icon_size = 64,
    name = "clay-pit",
    icon = "__tanks_for_bob_fork__/graphics/icons/placeholder.png",
    flags = {"placeable-neutral", "placeable-player", "player-creation"},
    minable = {hardness = 0.2, mining_time = 0.5, result = "clay-pit"},
    max_health = 100,
    corpse = "big-remnants",
    dying_explosion = "medium-explosion",
    resistances = {
        {
            type = "fire",
            percent = 95
        }
    },
    open_sound = {filename = "__base__/sound/machine-open.ogg", volume = 0.85},
    close_sound = {filename = "__base__/sound/machine-close.ogg", volume = 0.75},
    working_sound = {
        sound = {
            {
                filename = "__base__/sound/furnace.ogg",
                volume = 0.8
            },
            {
                filename = "__base__/sound/furnace.ogg",
                volume = 0.8
            },
        },
        idle_sound = {filename = "__base__/sound/idle1.ogg", volume = 0.6},
        apparent_volume = 1.5,
    },
    collision_box = {{-1.2, -1.2}, {1.2, 1.2}},
    selection_box = {{-1.5, -1.5}, {1.5, 1.5}},
    animation = {
        filename = "__tanks_for_bob_fork__/graphics/entity/new/placeholder.png",
        priority = "high",
        width = 64,
        height = 64,
        frame_count = 1,
        line_length = 1,
        shift = {0.00, -0.00}
    },
    crafting_categories = {"clay"},
    crafting_speed = 0.30,
    energy_source = {
        type = "burner",
        fuel_category = "chemical",
        effectivity = .5,
        fuel_inventory_size = 1,
        emissions_per_minute = 6,
        light_flicker = {
            color = {0, 0, 0},
            minimum_intensity = 0.6,
            maximum_intensity = 0.95
        },
        smoke = {
            {
                name = "smoke",
                deviation = {0.1, 0.1},
                frequency = 15,
                position = {0.0, -0.8},
                starting_vertical_speed = 0.08,
                starting_frame_deviation = 60
            }
        }
    },
    working_visualisations = {
        {
            animation = {
                filename = "__tanks_for_bob_fork__/graphics/entity/new/placeholder.png",
                priority = "high",
                width = 64,
                height = 64,
                frame_count = 1,
                line_length = 1,
                shift = {0.00, -0.00}
            },
            light = {intensity = 0.4, size = 6}
        }
    },
    energy_usage = "20kW",
    ingredient_count = 2,
    module_specification = {module_slots = 0},
},

--pit-kiln

   {
    type = "assembling-machine",
    icon_size = 64,
    name = "pit-kiln",
    icon = "__tanks_for_bob_fork__/graphics/icons/placeholder.png",
    flags = {"placeable-neutral", "placeable-player", "player-creation"},
    minable = {hardness = 0.2, mining_time = 0.5, result = "pit-kiln"},
    max_health = 100,
    corpse = "big-remnants",
    dying_explosion = "medium-explosion",
    resistances = {
        {
            type = "fire",
            percent = 95
        }
    },
    open_sound = {filename = "__base__/sound/machine-open.ogg", volume = 0.85},
    close_sound = {filename = "__base__/sound/machine-close.ogg", volume = 0.75},
    working_sound = {
        sound = {
            {
                filename = "__base__/sound/furnace.ogg",
                volume = 0.8
            },
            {
                filename = "__base__/sound/furnace.ogg",
                volume = 0.8
            },
        },
        idle_sound = {filename = "__base__/sound/idle1.ogg", volume = 0.6},
        apparent_volume = 1.5,
    },
    collision_box = {{-1.2, -1.2}, {1.2, 1.2}},
    selection_box = {{-1.5, -1.5}, {1.5, 1.5}},
    animation = {
        filename = "__tanks_for_bob_fork__/graphics/entity/new/placeholder.png",
        priority = "high",
        width = 64,
        height = 64,
        frame_count = 1,
        line_length = 1,
        shift = {0.00, -0.00}
    },
    crafting_categories = {"pit-kiln"},
    crafting_speed = 0.30,
    energy_source = {
        type = "burner",
        fuel_category = "chemical",
        effectivity = .5,
        fuel_inventory_size = 1,
        emissions_per_minute = 6,
        light_flicker = {
            color = {0, 0, 0},
            minimum_intensity = 0.6,
            maximum_intensity = 0.95
        },
        smoke = {
            {
                name = "smoke",
                deviation = {0.1, 0.1},
                frequency = 15,
                position = {0.0, -0.8},
                starting_vertical_speed = 0.08,
                starting_frame_deviation = 60
            }
        }
    },
    working_visualisations = {
        {
            animation = {
                filename = "__tanks_for_bob_fork__/graphics/entity/new/placeholder.png",
                priority = "high",
                width = 64,
                height = 64,
                frame_count = 1,
                line_length = 1,
                shift = {0.00, -0.00}
            },
            light = {intensity = 0.4, size = 6}
        }
    },
    energy_usage = "20kW",
    ingredient_count = 2,
    module_specification = {module_slots = 0},
},

  --workbench
  {
    type = "assembling-machine",
    icon_size = 64,
    name = "workbench",
    icon = "__tanks_for_bob_fork__/graphics/icons/placeholder.png",
    flags = {"placeable-neutral", "placeable-player", "player-creation"},
    minable = {hardness = 0.2, mining_time = 0.5, result = "workbench"},
    max_health = 100,
    corpse = "big-remnants",
    dying_explosion = "medium-explosion",
    resistances = {
        {
            type = "fire",
            percent = 95
        }
    },
    open_sound = {filename = "__base__/sound/machine-open.ogg", volume = 0.85},
    close_sound = {filename = "__base__/sound/machine-close.ogg", volume = 0.75},
    working_sound = {
        sound = {
            {
                filename = "__base__/sound/furnace.ogg",
                volume = 0.8
            },
            {
                filename = "__base__/sound/furnace.ogg",
                volume = 0.8
            },
        },
        idle_sound = {filename = "__base__/sound/idle1.ogg", volume = 0.6},
        apparent_volume = 1.5,
    },
    collision_box = {{-1.2, -1.2}, {1.2, 1.2}},
    selection_box = {{-1.5, -1.5}, {1.5, 1.5}},
    animation = {
        filename = "__tanks_for_bob_fork__/graphics/entity/new/placeholder.png",
        priority = "high",
        width = 64,
        height = 64,
        frame_count = 1,
        line_length = 1,
        shift = {0.00, -0.00}
    },
    crafting_categories = {"Seablock"},
    crafting_speed = 0.30,
    energy_source = {
        type = "burner",
        fuel_category = "chemical",
        effectivity = .5,
        fuel_inventory_size = 1,
        emissions_per_minute = 6,
        light_flicker = {
            color = {0, 0, 0},
            minimum_intensity = 0.6,
            maximum_intensity = 0.95
        },
        smoke = {
            {
                name = "smoke",
                deviation = {0.1, 0.1},
                frequency = 15,
                position = {0.0, -0.8},
                starting_vertical_speed = 0.08,
                starting_frame_deviation = 60
            }
        }
    },
    working_visualisations = {
        {
            animation = {
                filename = "__tanks_for_bob_fork__/graphics/entity/new/placeholder.png",
                priority = "high",
                width = 64,
                height = 64,
                frame_count = 1,
                line_length = 1,
                shift = {0.00, -0.00}
            },
            light = {intensity = 0.4, size = 6}
        }
    },
    energy_usage = "20kW",
    ingredient_count = 2,
    module_specification = {module_slots = 0},
},
    --campfire
    {
    type = "assembling-machine",
    icon_size = 64,
    name = "campfire",
    icon = "__tanks_for_bob_fork__/graphics/icons/placeholder.png",
    flags = {"placeable-neutral", "placeable-player", "player-creation"},
    minable = {hardness = 0.2, mining_time = 0.5, result = "campfire"},
    max_health = 100,
    corpse = "big-remnants",
    dying_explosion = "medium-explosion",
    resistances = {
        {
            type = "fire",
            percent = 95
        }
    },
    open_sound = {filename = "__base__/sound/machine-open.ogg", volume = 0.85},
    close_sound = {filename = "__base__/sound/machine-close.ogg", volume = 0.75},
    working_sound = {
        sound = {
            {
                filename = "__base__/sound/furnace.ogg",
                volume = 0.8
            },
            {
                filename = "__base__/sound/furnace.ogg",
                volume = 0.8
            },
        },
        idle_sound = {filename = "__base__/sound/idle1.ogg", volume = 0.6},
        apparent_volume = 1.5,
    },
    collision_box = {{-1.2, -1.2}, {1.2, 1.2}},
    selection_box = {{-1.5, -1.5}, {1.5, 1.5}},
    animation = {
        filename = "__tanks_for_bob_fork__/graphics/entity/new/placeholder.png",
        priority = "high",
        width = 64,
        height = 64,
        frame_count = 1,
        line_length = 1,
        shift = {0.00, -0.00}
    },
    crafting_categories = {"cooking"},
    crafting_speed = 0.30,
    energy_source = {
        type = "burner",
        fuel_category = "chemical",
        effectivity = 1,
        fuel_inventory_size = 1,
        emissions_per_minute = 2,
        light_flicker = {
            color = {0, 0, 0},
            minimum_intensity = 0.6,
            maximum_intensity = 0.95
        },
        smoke = {
            {
                name = "smoke",
                deviation = {0.1, 0.1},
                frequency = 5,
                position = {0.0, -0.8},
                starting_vertical_speed = 0.08,
                starting_frame_deviation = 60
            }
        }
    },
    working_visualisations = {
        {
            animation = {
                filename = "__tanks_for_bob_fork__/graphics/entity/new/placeholder.png",
                priority = "high",
                width = 64,
                height = 64,
                frame_count = 1,
                line_length = 1,
                shift = {0.00, -0.00}
            },
            light = {intensity = 0.4, size = 6}
        }
    },
    energy_usage = "20kW",
    ingredient_count = 2,
    module_specification = {module_slots = 0},
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
