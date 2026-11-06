-- Reuse Factorio's official assembler pipe sprites across 2.0 and 2.1.
-- The global assembler2pipepictures helper was removed in Factorio 2.1.
local function tanks_assembler_pipe_pictures()
  if type(assembler2pipepictures) == "function" then
    return assembler2pipepictures()
  end
  local standard = (data.raw["assembling-machine"] or {})["assembling-machine-2"]
  for _, box in pairs(standard and standard.fluid_boxes or {}) do
    if type(box) == "table" and box.pipe_picture then
      return table.deepcopy(box.pipe_picture)
    end
  end
  return nil
end

-- Solar boiler: deep-copy the base boiler first so all vanilla graphics/sprite layers remain valid.
local solar_boiler = table.deepcopy(data.raw["boiler"]["boiler"])

solar_boiler.name = "solar-boiler"
solar_boiler.icon = "__base__/graphics/icons/boiler.png"
solar_boiler.icon_size = 64
solar_boiler.icon_mipmaps = 4
solar_boiler.flags = {"placeable-neutral", "player-creation"}
solar_boiler.minable = {mining_time = 0.2, result = "solar-boiler"}
solar_boiler.max_health = 100
solar_boiler.corpse = "boiler-remnants"
solar_boiler.dying_explosion = "boiler-explosion"
solar_boiler.mode = "output-to-separate-pipe"

solar_boiler.resistances =
{
  {type = "fire", percent = 10},
  {type = "explosion", percent = 30},
  {type = "impact", percent = 30}
}

solar_boiler.collision_box = {{-1.29, -0.79}, {1.29, 0.79}}
solar_boiler.selection_box = {{-1.5, -1}, {1.5, 1}}
solar_boiler.target_temperature = 101

solar_boiler.fluid_box =
{
  volume = 200,
  pipe_covers = pipecoverspictures(),
  pipe_connections =
  {
    {flow_direction = "input-output", position = {-1, 0.5}, direction = defines.direction.west},
    {flow_direction = "input-output", position = {1, 0.5}, direction = defines.direction.east}
  },
  production_flow_direction = "input-output",
  filter = "water"
}

solar_boiler.output_fluid_box =
{
  volume = 200,
  pipe_covers = pipecoverspictures(),
  pipe_connections =
  {
    {flow_direction = "output", position = {0, -0.5}, direction = defines.direction.north}
  },
  production_flow_direction = "output",
  filter = "steam"
}

solar_boiler.energy_consumption = "1MW"
solar_boiler.energy_source = { type = "void" }

solar_boiler.working_sound =
{
  sound =
  {
    filename = "__base__/sound/boiler.ogg",
    volume = 0.7
  },
  audible_distance_modifier = 0.3,
  fade_in_ticks = 4,
  fade_out_ticks = 20
}

-- Keep these explicit so later edits cannot accidentally strip the copied boiler graphics.
solar_boiler.structure = table.deepcopy(data.raw["boiler"]["boiler"].structure)
solar_boiler.patch = table.deepcopy(data.raw["boiler"]["boiler"].patch)
solar_boiler.fire = table.deepcopy(data.raw["boiler"]["boiler"].fire)
solar_boiler.fire_glow = table.deepcopy(data.raw["boiler"]["boiler"].fire_glow)
solar_boiler.water_reflection = table.deepcopy(data.raw["boiler"]["boiler"].water_reflection)
solar_boiler.fire_flicker_enabled = false
solar_boiler.fire_glow_flicker_enabled = false
solar_boiler.burning_cooldown = 20

data:extend(
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
      size = {48, 64},
      frame_count = 1,
      line_length = 10,
      animation_speed = 0.5
    }
  }
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
      size = {48, 64},
      frame_count = 100,
      line_length = 10,
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
      }
    }
  }
},
  --newmachines

 {
  type = "lab",
  name = "pondering-hovel",
  icon = "__tanks_for_bob_fork__/graphics/icons/pondering-hovel.png",
  icon_size = 64,
  icon_mipmaps = 4,
  flags = {"placeable-player", "player-creation"},
  minable = {mining_time = 0.2, result = "pondering-hovel"},
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
        filename = "__tanks_for_bob_fork__/graphics/entity/pondering-hovel/pondering-hovel.png",
        width = 32,
        height = 36,
        frame_count = 1,
        line_length = 1,
        animation_speed = 1 / 3,
        shift = util.by_pixel(0, 0),
        scale = 2,
        hr_version =
        {
          filename = "__tanks_for_bob_fork__/graphics/entity/pondering-hovel/hr-pondering-hovel.png",
          width = 62,
          height = 72,
          frame_count = 1,
          line_length = 1,
          animation_speed = 1 / 3,
          shift = util.by_pixel(0, 0),
          scale = 1
        }
      },
      {
        filename = "__tanks_for_bob_fork__/graphics/entity/pondering-hovel/pondering-hovel.png",
        width = 32,
        height = 36,
        frame_count = 1,
        line_length = 1,
        repeat_count = 1,
        animation_speed = 1 / 3,
        shift = util.by_pixel(0, 0),
        scale = 2,
        hr_version =
        {
          filename = "__tanks_for_bob_fork__/graphics/entity/pondering-hovel/hr-pondering-hovel.png",
          width = 62,
          height = 72,
          frame_count = 1,
          line_length = 1,
          repeat_count = 1,
          animation_speed = 1 / 3,
          shift = util.by_pixel(0,0),
          scale = 1
        }
      },
      {
        filename = "__tanks_for_bob_fork__/graphics/entity/pondering-hovel/pondering-hovel-light.png",
        blend_mode = "additive",
        draw_as_light = true,
        width = 32,
        height = 36,
        frame_count = 1,
        line_length = 1,
        animation_speed = 1 / 3,
        shift = util.by_pixel(0,0),
        scale = 2,
        hr_version =
        {
          filename = "__tanks_for_bob_fork__/graphics/entity/pondering-hovel/hr-pondering-hovel-light.png",
          blend_mode = "additive",
          draw_as_light = true,
          width = 32,
          height = 36,
          frame_count = 1,
          line_length = 1,
          animation_speed = 1 / 3,
          shift = util.by_pixel(0, 0),
          scale = 1
        }
      },
      {
        filename = "__tanks_for_bob_fork__/graphics/entity/pondering-hovel/pondering-hovel-shadow.png",
        width = 52,
        height = 20,
        frame_count = 1,
        line_length = 1,
        repeat_count = 1,
        animation_speed = 1 / 3,
        shift = util.by_pixel(0, 0),
        draw_as_shadow = true,
        scale = 2,
        hr_version =
        {
          filename = "__tanks_for_bob_fork__/graphics/entity/pondering-hovel/hr-pondering-hovel-shadow.png",
          width = 104,
          height = 40,
          frame_count = 1,
          line_length = 1,
          repeat_count = 1,
          animation_speed = 1 / 3,
          shift = util.by_pixel(0, 0),
          scale = 1,
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
        filename = "__tanks_for_bob_fork__/graphics/entity/pondering-hovel/pondering-hovel.png",
        width = 32,
        height = 36,
        frame_count = 1,
        shift = util.by_pixel(0, 0),
        scale = 2,
        hr_version =
        {
          filename = "__tanks_for_bob_fork__/graphics/entity/pondering-hovel/hr-pondering-hovel.png",
          width = 62,
          height = 72,
          frame_count = 1,
          shift = util.by_pixel(0, 0),
          scale = 1
        }
      },
      {
        filename = "__tanks_for_bob_fork__/graphics/entity/pondering-hovel/pondering-hovel.png",
        width = 32,
        height = 36,
        frame_count = 1,
        shift = util.by_pixel(0, 0),
        scale = 2,
        hr_version =
        {
          filename = "__tanks_for_bob_fork__/graphics/entity/pondering-hovel/hr-pondering-hovel.png",
          width = 62,
          height = 72,
          frame_count = 1,
          shift = util.by_pixel(0, 0),
          scale = 1
        }
      },
      {
        filename = "__tanks_for_bob_fork__/graphics/entity/pondering-hovel/pondering-hovel-shadow.png",
        width = 52,
        height = 20,
        frame_count = 1,
        shift = util.by_pixel(10, 20),
        draw_as_shadow = true,
        scale = 2,
        hr_version =
        {
          filename = "__tanks_for_bob_fork__/graphics/entity/pondering-hovel/hr-pondering-hovel-shadow.png",
          width = 104,
          height = 40,
          frame_count = 1,
          shift = util.by_pixel(20, 40),
          scale = 1,
          draw_as_shadow = true
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
    fuel_categories = {"chemical"},
    effectivity = 0.5,
    fuel_inventory_size = 1,
    emissions_per_minute = {pollution = 2},
    light_flicker =
    {
      color = {0, 0, 0},
      minimum_intensity = 0.6,
      maximum_intensity = 0.95
    },
    smoke =
    {
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
  inputs = {
    "Seared-fish",
    "meal",
    "requisition-slip",
    "work-order-slip",
    "certified-work-order",
    "submitted-evaluation",
    "risk-assessment",
    "risk-assessed-work-order",
    "compliance-packet",
    "audit-ready-deliverable",
    "stakeholder-review-summary",
    "liability-contained-report",
    "board-review-docket",
    "board-advisory-risk-assessment"
  },
  module_specification =
  {
    module_slots = 0,
  }
},

--thinking-hut
{
  type = "lab",
  name = "thinking-hut",
  icon = "__tanks_for_bob_fork__/graphics/icons/thinking-hut.png",
  icon_size = 64,
  icon_mipmaps = 4,
  flags = {"placeable-player", "player-creation"},
  minable = {mining_time = 0.2, result = "thinking-hut"},
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
        filename = "__tanks_for_bob_fork__/graphics/entity/thinking-hut/thinking-hut.png",
        width = 32,
        height = 36,
        frame_count = 1,
        line_length = 1,
        animation_speed = 1 / 3,
        shift = util.by_pixel(0, 0),
		scale = 2,
        hr_version =
        {
          filename = "__tanks_for_bob_fork__/graphics/entity/thinking-hut/hr-thinking-hut.png",
          width = 62,
          height = 72,
          frame_count = 1,
          line_length = 1,
          animation_speed = 1 / 3,
          shift = util.by_pixel(0, 0),
          scale = 1.5
        }
      },
      {
        filename = "__tanks_for_bob_fork__/graphics/entity/thinking-hut/thinking-hut-integration.png",
        width = 52,
        height = 20,
        frame_count = 1,
        line_length = 1,
        repeat_count = 1,
        animation_speed = 1 / 3,
        shift = util.by_pixel(0, 20),
        scale = 2,
        hr_version =
        {
          filename = "__tanks_for_bob_fork__/graphics/entity/thinking-hut/hr-thinking-hut-integration.png",
          width = 104,
          height = 40,
          frame_count = 1,
          line_length = 1,
          repeat_count = 1,
          animation_speed = 1 / 3,
          shift = util.by_pixel(0, 40),
          scale = 2
        }
      },
      {
        filename = "__tanks_for_bob_fork__/graphics/entity/thinking-hut/thinking-hut-light.png",
        width = 32,
        height = 36,
        frame_count = 1,
        line_length = 1,
        animation_speed = 1 / 3,
        shift = util.by_pixel(0, 0),
        scale = 2,
        hr_version =
        {
          filename = "__tanks_for_bob_fork__/graphics/entity/thinking-hut/hr-thinking-hut-light.png",
          width = 62,
          height = 72,
          frame_count = 1,
          line_length = 1,
          animation_speed = 1 / 3,
          shift = util.by_pixel(0, 0),
          scale = 1.5
        }
      },
      {
        filename = "__tanks_for_bob_fork__/graphics/entity/thinking-hut/thinking-hut-shadow.png",
        width = 52,
        height = 20,
        frame_count = 1,
        line_length = 1,
        repeat_count = 1,
        animation_speed = 1 / 3,
        shift = util.by_pixel(15, 20),
        draw_as_shadow = true,
        scale = 2,
        hr_version =
        {
          filename = "__tanks_for_bob_fork__/graphics/entity/thinking-hut/hr-thinking-hut-shadow.png",
          width = 104,
          height = 40,
          frame_count = 1,
          line_length = 1,
          repeat_count = 1,
          animation_speed = 1 / 3,
          shift = util.by_pixel(15, 20),
          scale = 2,
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
        filename = "__tanks_for_bob_fork__/graphics/entity/thinking-hut/thinking-hut.png",
        width = 32,
        height = 36,
        frame_count = 1,
        shift = util.by_pixel(0, 0),
		scale = 2,
        hr_version =
        {
          filename = "__tanks_for_bob_fork__/graphics/entity/thinking-hut/hr-thinking-hut.png",
          width = 62,
          height = 72,
          frame_count = 1,
          shift = util.by_pixel(0, 0),
          scale = 1.5
        }
      },
      {
        filename = "__tanks_for_bob_fork__/graphics/entity/thinking-hut/thinking-hut-integration.png",
        width = 52,
        height = 20,
        frame_count = 1,
        shift = util.by_pixel(0, 24.1),
		scale = 2,
        hr_version =
        {
          filename = "__tanks_for_bob_fork__/graphics/entity/thinking-hut/hr-thinking-hut-integration.png",
          width = 104,
          height = 40,
          frame_count = 1,
          shift = util.by_pixel(0, 24.1),
          scale = 2
        }
      },
      {
        filename = "__tanks_for_bob_fork__/graphics/entity/thinking-hut/thinking-hut-shadow.png",
        width = 52,
        height = 20,
        frame_count = 1,
        shift = util.by_pixel(15, 22),
        draw_as_shadow = true,
		scale = 2,
        hr_version =
        {
          filename = "__tanks_for_bob_fork__/graphics/entity/thinking-hut/hr-thinking-hut-shadow.png",
          width = 104,
          height = 40,
          frame_count = 1,
          shift = util.by_pixel(15, 22),
          draw_as_shadow = true,
          scale = 2
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
    fuel_categories = {"chemical"},
    effectivity = 1,
    fuel_inventory_size = 1,
    emissions_per_minute = {pollution = 2},
    light_flicker =
    {
      color = {0, 0, 0},
      minimum_intensity = 0.6,
      maximum_intensity = 0.95
    },
    smoke =
    {
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
  inputs = {
    "Seared-fish",
    "meal",
    "requisition-slip",
    "work-order-slip",
    "certified-work-order",
    "submitted-evaluation",
    "risk-assessment",
    "risk-assessed-work-order",
    "compliance-packet",
    "audit-ready-deliverable",
    "stakeholder-review-summary",
    "liability-contained-report",
    "board-review-docket",
    "board-advisory-risk-assessment"
  },
  module_specification =
  {
    module_slots = 0
  }
}
}
)

-- =========================================================
-- Stone Water Wheel
-- Deep-copy offshore pump with void energy and extremely slow pumping
-- =========================================================

local stone_water_wheel = table.deepcopy(data.raw["offshore-pump"]["offshore-pump"])

stone_water_wheel.name = "stone-water-wheel"
stone_water_wheel.icon = "__tanks_for_bob_fork__/graphics/icons/stone-water-wheel.png"
stone_water_wheel.icon_size = 64
stone_water_wheel.icon_mipmaps = 4

stone_water_wheel.flags = {"placeable-neutral", "player-creation", "filter-directions"}
stone_water_wheel.minable = {mining_time = 0.2, result = "stone-water-wheel"}
stone_water_wheel.max_health = 150
stone_water_wheel.corpse = "offshore-pump-remnants"
stone_water_wheel.dying_explosion = "offshore-pump-explosion"

stone_water_wheel.fluid = "water"

stone_water_wheel.resistances =
{
  {type = "fire", percent = 70},
  {type = "impact", percent = 30}
}

stone_water_wheel.collision_box = {{-0.6, -1.05}, {0.6, 0.3}}
stone_water_wheel.selection_box = {{-0.6, -1.49}, {0.6, 0.49}}

stone_water_wheel.energy_usage = "1W"
stone_water_wheel.energy_source =
{
  type = "void"
}

-- Extremely slow output. Base offshore pump is usually 20.
-- This is intentionally miserable.
stone_water_wheel.pumping_speed = 0.5

stone_water_wheel.fluid_box =
{
  volume = 200,
  pipe_covers = pipecoverspictures(),
  pipe_connections =
  {
    {
      flow_direction = "output",
      position = {0, 0.25},
      direction = defines.direction.south
    }
  },
  production_flow_direction = "output",
  filter = "water",
  minimum_temperature = 15
}

-- Factorio 2.1 removed FluidBox minimum/maximum temperature constraints.
if (mods["base"] or ""):match("^2%.1%.") then
  stone_water_wheel.fluid_box.minimum_temperature = nil
  stone_water_wheel.fluid_box.maximum_temperature = nil
end

stone_water_wheel.fluid_source_offset = {0, -1}
stone_water_wheel.tile_width = 1
stone_water_wheel.tile_height = 1

stone_water_wheel.working_sound =
{
  sound =
  {
    {
      filename = "__base__/sound/offshore-pump.ogg",
      volume = 0.35
    }
  },
  match_volume_to_activity = true,
  audible_distance_modifier = 0.6,
  max_sounds_per_type = 3,
  fade_in_ticks = 4,
  fade_out_ticks = 20
}

stone_water_wheel.min_perceived_performance = 0.3
stone_water_wheel.always_draw_fluid = true

data:extend({
  stone_water_wheel
})

-- =========================================================
-- BeachPump
-- Deep-copy offshore pump with wooden-offshore-pump graphics,
-- void energy, and very slow pumping
-- =========================================================

local BeachPump = table.deepcopy(data.raw["offshore-pump"]["offshore-pump"])

BeachPump.name = "beachpump"
BeachPump.icon = "__tanks_for_bob_fork__/graphics/icons/beachpump.png"
BeachPump.icon_size = 64
BeachPump.icon_mipmaps = 4

BeachPump.flags = {"placeable-neutral", "player-creation", "filter-directions"}
BeachPump.minable = {mining_time = 0.1, result = "beachpump"}
BeachPump.max_health = 50
BeachPump.corpse = "offshore-pump-remnants"
BeachPump.dying_explosion = "offshore-pump-explosion"

BeachPump.fluid = "water"

BeachPump.resistances =
{
  {type = "fire", percent = 70},
  {type = "impact", percent = 30}
}

BeachPump.collision_box = {{-0.6, -1.05}, {0.6, 0.3}}
BeachPump.selection_box = {{-0.6, -1.49}, {0.6, 0.49}}

BeachPump.energy_usage = "1W"
BeachPump.energy_source =
{
  type = "void"
}

-- Very slow starter water source.
BeachPump.pumping_speed = 0.01

BeachPump.fluid_box =
{
  volume = 200,
  pipe_covers = pipecoverspictures(),
  pipe_connections =
  {
    {
      flow_direction = "output",
      position = {0, 0.25},
      direction = defines.direction.south
    }
  },
  production_flow_direction = "output",
  filter = "water",
  minimum_temperature = 15
}

if (mods["base"] or ""):match("^2%.1%.") then
  BeachPump.fluid_box.minimum_temperature = nil
  BeachPump.fluid_box.maximum_temperature = nil
end

BeachPump.fluid_source_offset = {0, -1}
BeachPump.tile_width = 1
BeachPump.tile_height = 1

BeachPump.working_sound =
{
  sound =
  {
    {
      filename = "__base__/sound/offshore-pump.ogg",
      volume = 0.3
    }
  },
  match_volume_to_activity = true,
  audible_distance_modifier = 0.5,
  max_sounds_per_type = 3,
  fade_in_ticks = 4,
  fade_out_ticks = 20
}

BeachPump.min_perceived_performance = 0.3
BeachPump.always_draw_fluid = true

-- Preserve custom wooden-offshore-pump graphics while inheriting the
-- base offshore pump structure.
local wooden_path = "__tanks_for_bob_fork__/graphics/entity/wooden-offshore-pump/"

-- Factorio 2.x/base-prototype compatibility guard:
-- some copied offshore-pump sprite layers no longer expose hr_version.
-- Do not index missing sprite tables; update only what exists.
local function set_sprite_filename(sprite, filename)
  if sprite then
    sprite.filename = filename
  end
end

local function set_hr_sprite_filename(sprite, filename)
  if sprite and sprite.hr_version then
    sprite.hr_version.filename = filename
  end
end

local function set_sprite_pair(sprite, normal_filename, hr_filename)
  set_sprite_filename(sprite, wooden_path .. normal_filename)
  set_hr_sprite_filename(sprite, wooden_path .. hr_filename)
end

local gs = BeachPump.graphics_set or {}
local animation = gs.animation or {}

if animation.north and animation.north.layers then
  set_sprite_pair(animation.north.layers[1], "offshore-pump_North.png", "hr-offshore-pump_North.png")
  set_sprite_pair(animation.north.layers[2], "offshore-pump_North-shadow.png", "hr-offshore-pump_North-shadow.png")
end

if animation.east and animation.east.layers then
  set_sprite_pair(animation.east.layers[1], "offshore-pump_East.png", "hr-offshore-pump_East.png")
  set_sprite_pair(animation.east.layers[2], "offshore-pump_East-shadow.png", "hr-offshore-pump_East-shadow.png")
end

if animation.south and animation.south.layers then
  set_sprite_pair(animation.south.layers[1], "offshore-pump_South.png", "hr-offshore-pump_South.png")
  set_sprite_pair(animation.south.layers[2], "offshore-pump_South-shadow.png", "hr-offshore-pump_South-shadow.png")
end

if animation.west and animation.west.layers then
  set_sprite_pair(animation.west.layers[1], "offshore-pump_West.png", "hr-offshore-pump_West.png")
  set_sprite_pair(animation.west.layers[2], "offshore-pump_West-shadow.png", "hr-offshore-pump_West-shadow.png")
end

local fluid_animation = gs.fluid_animation or {}
set_sprite_pair(fluid_animation.north, "offshore-pump_North-fluid.png", "hr-offshore-pump_North-fluid.png")
set_sprite_pair(fluid_animation.east, "offshore-pump_East-fluid.png", "hr-offshore-pump_East-fluid.png")
set_sprite_pair(fluid_animation.south, "offshore-pump_South-fluid.png", "hr-offshore-pump_South-fluid.png")
set_sprite_pair(fluid_animation.west, "offshore-pump_West-fluid.png", "hr-offshore-pump_West-fluid.png")

local glass_pictures = gs.glass_pictures or {}
set_sprite_pair(glass_pictures.north, "offshore-pump_North-glass.png", "hr-offshore-pump_North-glass.png")
set_sprite_pair(glass_pictures.east, "offshore-pump_East-glass.png", "hr-offshore-pump_East-glass.png")
set_sprite_pair(glass_pictures.south, "offshore-pump_South-glass.png", "hr-offshore-pump_South-glass.png")
set_sprite_pair(glass_pictures.west, "offshore-pump_West-glass.png", "hr-offshore-pump_West-glass.png")

local base_pictures = gs.base_pictures or {}
set_sprite_pair(base_pictures.north, "offshore-pump_North-legs.png", "hr-offshore-pump_North-legs.png")
set_sprite_pair(base_pictures.east, "offshore-pump_East-legs.png", "hr-offshore-pump_East-legs.png")
set_sprite_pair(base_pictures.south, "offshore-pump_South-legs.png", "hr-offshore-pump_South-legs.png")
-- The custom wooden south legs sprite is 56x54, while the copied base prototype
-- expects a 56x56 rectangle. Without this override Factorio reads below the PNG.
if base_pictures.south then
  base_pictures.south.width = 56
  base_pictures.south.height = 54
  if base_pictures.south.hr_version then
    base_pictures.south.hr_version.width = 112
    base_pictures.south.hr_version.height = 108
  end
end
set_sprite_pair(base_pictures.west, "offshore-pump_West-legs.png", "hr-offshore-pump_West-legs.png")

local underwater_pictures = gs.underwater_pictures or {}
set_sprite_pair(underwater_pictures.north, "offshore-pump_North-underwater.png", "hr-offshore-pump_North-underwater.png")
set_sprite_pair(underwater_pictures.east, "offshore-pump_East-underwater.png", "hr-offshore-pump_East-underwater.png")
set_sprite_pair(underwater_pictures.south, "offshore-pump_South-underwater.png", "hr-offshore-pump_South-underwater.png")
set_sprite_pair(underwater_pictures.west, "offshore-pump_West-underwater.png", "hr-offshore-pump_West-underwater.png")

BeachPump.water_reflection =
{
  pictures =
  {
    filename = wooden_path .. "offshore-pump-reflection.png",
    priority = "extra-high",
    width = 132,
    height = 156,
    shift = util.by_pixel(0, 19),
    variation_count = 1,
    scale = 1
  },
  rotate = false,
  orientation_to_variation = false
}

-- Emergency load-safety fallback: the custom wooden-offshore-pump sprite sheets
-- do not match the inherited vanilla offshore-pump frame geometry. Reset BeachPump
-- to the vanilla copied graphics so Factorio does not attempt to read outside
-- the actual PNG bounds during prototype validation. This preserves the entity,
-- recipe/item placement, fluid behavior, and balance while avoiding startup crashes.
if data.raw["offshore-pump"] and data.raw["offshore-pump"]["offshore-pump"] then
  BeachPump.graphics_set = table.deepcopy(data.raw["offshore-pump"]["offshore-pump"].graphics_set)
  BeachPump.water_reflection = table.deepcopy(data.raw["offshore-pump"]["offshore-pump"].water_reflection)
end

data:extend({
  BeachPump
})

data:extend(
{
  --Growing plot
   {
    type = "assembling-machine",
    icon_size = 64,
    name = "growing-plot",
    icon = "__tanks_for_bob_fork__/graphics/icons/growing-plot.png",
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
                filename = "__base__/sound/particles/tree-leaves-4.ogg",
                volume = 0.6
            },
            {
                filename = "__base__/sound/particles/tree-leaves-1.ogg",
                volume = 0.6
            },
        },
        idle_sound = {filename = "__base__/sound/idle1.ogg", volume = 0.6},
        apparent_volume = 1.5,
    },
    collision_box = {{-2, -2}, {2, 2}},
    selection_box = {{-2, -2}, {2, 2}},
    graphics_set =
    {
      animation = {
          filename = "__tanks_for_bob_fork__/graphics/entity/growing-plot/growing-plot.png",
          priority = "high",
          width = 187,
          height = 310,
          frame_count = 1,
          line_length = 1,
          shift = {0.00, -2.50}
      },
      working_visualisations = {
          {
              animation = {
                  filename = "__tanks_for_bob_fork__/graphics/entity/growing-plot/growing-plot-w.png",
                  priority = "high",
                  width = 187,
                  height = 310,
                  frame_count = 4,
                  line_length = 4,
                  shift = {0.00, -2.50}
              },
              light = {intensity = 0.4, size = 6}
          }
      }
    },

    crafting_categories = {"growing"},
    crafting_speed = 0.30,
    energy_source = {
        type = "burner",
        fuel_categories = {"chemical"},
        effectivity = 1,
        fuel_inventory_size = 1,
        emissions_per_minute = {pollution = 2},
        light_flicker = {
            color = {0, 0, 0},
            minimum_intensity = 0.6,
            maximum_intensity = 0.95
        },
            },

    energy_usage = "20kW",
    ingredient_count = 1,
    module_specification = {module_slots = 0},
},

--quarry
 {
    type = "assembling-machine",
    icon_size = 64,
    name = "quarry",
    icon = "__tanks_for_bob_fork__/graphics/icons/quarry.png",
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
    graphics_set =
    {
      animation = {
          filename = "__tanks_for_bob_fork__/graphics/entity/quarry/quarry.png",
          priority = "high",
          width = 84,
          height = 80,
          frame_count = 30,
          line_length = 6,
          shift = {0.0, -0.00}
  		--
			
  		--
      },
      working_visualisations = {
          {
              animation = {
                  filename = "__tanks_for_bob_fork__/graphics/entity/quarry/quarry.png",
                  priority = "high",
                  width = 84,
                  height = 80,
                  frame_count = 30,
                  line_length = 6,
                  shift = {0.0, -0.00}
              },
              light = {intensity = 0.4, size = 6}
          }
      }
    },

    crafting_categories = {"quarrying"},
    crafting_speed = 0.35,
    energy_source = {
        type = "burner",
        fuel_categories = {"chemical"},
        effectivity = 1,
        fuel_inventory_size = 1,
        emissions_per_minute = {pollution = 2},
        light_flicker = {
            color = {0, 0, 0},
            minimum_intensity = 0.6,
            maximum_intensity = 0.95
        },
        smoke = {
            {
                name = "smoke",
                deviation = {0.1, 0.1},
                frequency = 1,
                position = {0.0, -0.8},
                starting_vertical_speed = 0.08,
                starting_frame_deviation = 60
            }
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
    icon = "__tanks_for_bob_fork__/graphics/icons/wood-basin.png",
    icon_size = 64, icon_mipmaps = 4,
    flags = {"placeable-player", "player-creation"},
    minable = {mining_time = 0.5, result = "wood-basin"},
    max_health = 100,
    corpse = "storage-tank-remnants",
    dying_explosion = "storage-tank-explosion",
    collision_box = {{-1.3, -1.3}, {1.3, 1.3}},
    selection_box = {{-1.5, -1.5}, {1.5, 1.5}},
    fluid_box =
    {
      volume = 25000,
      pipe_covers = pipecoverspictures(),
      pipe_connections =
      {
        {flow_direction = "input-output", position = {-1, -1}, direction = defines.direction.north},
        {flow_direction = "input-output", position = {1, 1}, direction = defines.direction.east},
        {flow_direction = "input-output", position = {1, 1}, direction = defines.direction.south},
        {flow_direction = "input-output", position = {-1, -1}, direction = defines.direction.west}
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
            filename = "__tanks_for_bob_fork__/graphics/entity/wood-basin/storage-tank.png",
            priority = "extra-high",
            frames = 2,
            width = 110,
            height = 108,
            shift = util.by_pixel(0, 4),
            hr_version =
            {
              filename = "__tanks_for_bob_fork__/graphics/entity/wood-basin/hr-storage-tank.png",
              priority = "extra-high",
              frames = 2,
              width = 219,
              height = 215,
              shift = util.by_pixel(-0.25, 3.75),
              scale = 0.5
            }
          },
          {
            filename = "__tanks_for_bob_fork__/graphics/entity/wood-basin/storage-tank-shadow.png",
            priority = "extra-high",
            frames = 2,
            width = 146,
            height = 77,
            shift = util.by_pixel(30, 22.5),
            draw_as_shadow = true,
            hr_version =
            {
              filename = "__tanks_for_bob_fork__/graphics/entity/wood-basin/hr-storage-tank-shadow.png",
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
        filename = "__tanks_for_bob_fork__/graphics/entity/wood-basin/fluid-background.png",
        priority = "extra-high",
        width = 32,
        height = 15
      },
      window_background =
      {
        filename = "__tanks_for_bob_fork__/graphics/entity/wood-basin/window-background.png",
        priority = "extra-high",
        width = 17,
        height = 24,
        hr_version =
        {
          filename = "__tanks_for_bob_fork__/graphics/entity/wood-basin/hr-window-background.png",
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
        filename = "__tanks_for_bob_fork__/graphics/entity/wood-basin/storage-tank-reflection.png",
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
  solar_boiler,
--cooking-fire
 {
    type = "assembling-machine",
    icon_size = 64,
    name = "cooking-fire",
    icon = "__tanks_for_bob_fork__/graphics/icons/cooking-fire.png",
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
    graphics_set =
    {
      animation = {
          filename = "__tanks_for_bob_fork__/graphics/entity/cooking-fire.png",
          priority = "high",
          width = 64,
          height = 64,
          frame_count = 1,
          line_length = 1,
          shift = {0.00, -0.00}
      },
          working_visualisations = {
          {
              animation = {
                  filename = "__tanks_for_bob_fork__/graphics/entity/cooking-fire.png",
                  priority = "high",
                  width = 64,
                  height = 64,
                  frame_count = 1,
                  line_length = 1,
                  shift = {0.00, -0.00}
              },
              light = {intensity = 0.4, size = 6}
          }
      }
    },

    crafting_categories = {"advcooking"},
    crafting_speed = 0.60,
    -- Steam rendering and steam-meal require an actual fluid connection.
    -- This port retains the existing 3x3 footprint and north-facing supply.
    fluid_boxes = {
      {
        production_type = "input",
        pipe_picture = tanks_assembler_pipe_pictures(),
        pipe_covers = pipecoverspictures(),
        volume = 1000,
        pipe_connections = {
          {flow_direction = "input", position = {0, -1}, direction = defines.direction.north}
        },
        secondary_draw_orders = {north = -1}
      }
    },
    off_when_no_fluid_recipe = true,
    energy_source = {
        type = "burner",
        fuel_categories = {"chemical"},
        effectivity = 1.5,
        fuel_inventory_size = 1,
        emissions_per_minute = {pollution = 6},
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

    energy_usage = "15kW",
    ingredient_count = 6,
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
      volume = 200,
      pipe_covers = pipecoverspictures(),
      pipe_connections =
      {
        {flow_direction = "output", position = {0, -0.75}, direction = defines.direction.north},
        {flow_direction = "input", position = {0, 0.75}, direction = defines.direction.south}
      }
    },
    energy_source =
    {
        type = "burner",
        fuel_categories = {"chemical"},
        effectivity = 1,
        fuel_inventory_size = 1,
        emissions_per_minute = {pollution = 6},
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
    energy_usage = "20kW",
    pumping_speed = 1,

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
        frame_count =8,
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
        height = 45,
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
    icon = "__tanks_for_bob_fork__/graphics/icons/fish-pond.png",
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
    graphics_set =
    {
      animation = {
          filename = "__tanks_for_bob_fork__/graphics/entity/fish-pond.png",
          priority = "high",
          width = 64,
          height = 64,
          frame_count = 1,
          line_length = 1,
          shift = {0.00, -0.00}
      },
      working_visualisations = {
          {
              animation = {
                  filename = "__tanks_for_bob_fork__/graphics/entity/fish-pond.png",
                  priority = "high",
                  width = 64,
                  height = 64,
                  frame_count = 1,
                  line_length = 1,
                  shift = {0.00, -0.00}
              },
              light = {intensity = 0.4, size = 6}
          }
      }
    },

  fluid_boxes =
{
  {
    production_type = "input",
    pipe_picture = tanks_assembler_pipe_pictures(),
    pipe_covers = pipecoverspictures(),
    volume = 1000,
    pipe_connections =
    {
      {
        flow_direction = "input",
        position = {0, -1},
        direction = defines.direction.north
      }
    },
    secondary_draw_orders = { north = -1 }
  },
  {
    production_type = "output",
    pipe_picture = tanks_assembler_pipe_pictures(),
    pipe_covers = pipecoverspictures(),
    volume = 1000,
    pipe_connections =
    {
      {
        flow_direction = "output",
        position = {0, 1},
        direction = defines.direction.south
      }
    },
    secondary_draw_orders = { north = -1 }
  }
},
	off_when_no_fluid_recipe = true,
    crafting_categories = {"fishery"},
    crafting_speed = 0.60,
    energy_source = {
        type = "burner",
        fuel_categories = {"chemical"},
        effectivity = 1,
        fuel_inventory_size = 1,
        emissions_per_minute = {pollution = 6},
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

    energy_usage = "15kW",
    ingredient_count = 4,
    module_specification = {module_slots = 0},
},
--calcifier
{
    type = "assembling-machine",
    icon_size = 64,
    name = "calcifier",
    icon = "__tanks_for_bob_fork__/graphics/icons/Placeholder.png",
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
    graphics_set =
    {
      animation = {
          filename = "__tanks_for_bob_fork__/graphics/entity/calcifier.png",
          priority = "high",
          width = 64,
          height = 64,
          frame_count = 1,
          line_length = 1,
          shift = {0.00, -0.00}
      },
      working_visualisations = {
          {
              animation = {
                  filename = "__tanks_for_bob_fork__/graphics/entity/calcifier-w.png",
                  priority = "high",
                  width = 64,
                  height = 64,
                  frame_count = 4,
                  line_length = 4,
                  shift = {0.00, -0.00}
              },
              light = {intensity = 0.4, size = 6}
          }
      }
    },

    crafting_categories = {"Calcifier"},
    crafting_speed = 0.60,
    energy_source = {
        type = "burner",
        fuel_categories = {"chemical"},
        effectivity = 1,
        fuel_inventory_size = 1,
        emissions_per_minute = {pollution = 6},
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
    fluid_boxes =
{
  {
    production_type = "input",
    pipe_picture = tanks_assembler_pipe_pictures(),
    pipe_covers = pipecoverspictures(),
    volume = 1000,
    pipe_connections =
    {
      {
        flow_direction = "input",
        position = {0, -1},
        direction = defines.direction.north
      }
    },
    secondary_draw_orders = { north = -1 }
  },
  {
    production_type = "output",
    pipe_picture = tanks_assembler_pipe_pictures(),
    pipe_covers = pipecoverspictures(),
    volume = 1000,
    pipe_connections =
    {
      {
        flow_direction = "output",
        position = {0, 1},
        direction = defines.direction.south
      }
    },
    secondary_draw_orders = { north = -1 }
  }
},

	  off_when_no_fluid_recipe = true,

    energy_usage = "1kW",
    ingredient_count = 4,
    module_specification = {module_slots = 0},
},
--steam condenser 
{
    type = "assembling-machine",
    icon_size = 64,
    name = "steam-condenser",
    icon = "__tanks_for_bob_fork__/graphics/icons/steam-condenser.png",
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
    graphics_set =
    {
      animation = {
          filename = "__tanks_for_bob_fork__/graphics/entity/steam-condenser.png",
          priority = "high",
          width = 64,
          height = 64,
          frame_count = 1,
          line_length = 1,
          shift = {0.00, -0.00}
      },
      working_visualisations = {
          {
              animation = {
                  filename = "__tanks_for_bob_fork__/graphics/entity/steam-condenser.png",
                  priority = "high",
                  width = 64,
                  height = 64,
                  frame_count = 1,
                  line_length = 1,
                  shift = {0.00, -0.00}
              },
              light = {intensity = 0.4, size = 6}
          }
      }
    },

    crafting_categories = {"Steam"},
    crafting_speed = 0.60,
    energy_source = {
        type = "burner",
        fuel_categories = {"chemical"},
        effectivity = 1,
        fuel_inventory_size = 1,
        emissions_per_minute = {pollution = 6},
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
   fluid_boxes =
{
  {
    production_type = "input",
    pipe_picture = tanks_assembler_pipe_pictures(),
    pipe_covers = pipecoverspictures(),
    volume = 1000,
    pipe_connections =
    {
      {
        flow_direction = "input",
        position = {0, -1},
        direction = defines.direction.north
      }
    },
    secondary_draw_orders = { north = -1 }
  },
  {
    production_type = "output",
    pipe_picture = tanks_assembler_pipe_pictures(),
    pipe_covers = pipecoverspictures(),
    volume = 1000,
    pipe_connections =
    {
      {
        flow_direction = "output",
        position = {0, 1},
        direction = defines.direction.south
      }
    },
    secondary_draw_orders = { north = -1 }
  }
},
	      off_when_no_fluid_recipe = true,

    energy_usage = "1kW",
    ingredient_count = 4,
    module_specification = {module_slots = 0},
},

--shaler
 {
    type = "assembling-machine",
    icon_size = 64,
    name = "shaler",
    icon = "__tanks_for_bob_fork__/graphics/icons/shaler.png",
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
    graphics_set =
    {
      animation = {
          filename = "__tanks_for_bob_fork__/graphics/entity/shaler.png",
          priority = "high",
          width = 64,
          height = 64,
          frame_count = 1,
          line_length = 1,
          shift = {0.00, -0.00}
      },
      working_visualisations = {
          {
              animation = {
                  filename = "__tanks_for_bob_fork__/graphics/entity/shaler.png",
                  priority = "high",
                  width = 64,
                  height = 64,
                  frame_count = 1,
                  line_length = 1,
                  shift = {0.00, -0.00}
              },
              light = {intensity = 0.4, size = 6}
          }
      }
    },

    crafting_categories = {"shaler"},
    crafting_speed = 0.90,
    energy_source = {
        type = "burner",
        fuel_categories = {"chemical"},
        effectivity = .5,
        fuel_inventory_size = 1,
        emissions_per_minute = {pollution = 6},
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
    fluid_boxes =
{
  {
    production_type = "input",
    pipe_picture = tanks_assembler_pipe_pictures(),
    pipe_covers = pipecoverspictures(),
    volume = 1000,
    pipe_connections =
    {
      {
        flow_direction = "input",
        position = {0, -1},
        direction = defines.direction.north
      }
    },
    secondary_draw_orders = { north = -1 }
  },
  {
    production_type = "output",
    pipe_picture = tanks_assembler_pipe_pictures(),
    pipe_covers = pipecoverspictures(),
    volume = 1000,
    pipe_connections =
    {
      {
        flow_direction = "output",
        position = {0, 1},
        direction = defines.direction.south
      }
    },
    secondary_draw_orders = { north = -1 }
  }
},

	   off_when_no_fluid_recipe = true,

    energy_usage = "10kW",
    ingredient_count = 2,
    module_specification = {module_slots = 0},
},
--Steam-Compressor
{
    type = "assembling-machine",
    icon_size = 64,
    name = "Steam-Compressor",
    icon = "__tanks_for_bob_fork__/graphics/icons/Steam-Compressor.png",
    flags = {"placeable-neutral", "placeable-player", "player-creation"},
    minable = {hardness = 0.2, mining_time = 0.5, result = "Steam-Compressor"},
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
    graphics_set =
    {
      animation = {
          filename = "__tanks_for_bob_fork__/graphics/entity/Steam-Compressor.png",
          priority = "high",
          width = 64,
          height = 64,
          frame_count = 1,
          line_length = 1,
          shift = {0.00, -0.00}
      },
      working_visualisations = {
          {
              animation = {
                  filename = "__tanks_for_bob_fork__/graphics/entity/Steam-Compressor.png",
                  priority = "high",
                  width = 64,
                  height = 64,
                  frame_count = 1,
                  line_length = 1,
                  shift = {0.00, -0.00}
              },
              light = {intensity = 0.4, size = 6}
          }
      }
    },

    crafting_categories = {"Steam-Compressor"},
    crafting_speed = 1.0,
    energy_source = {
        type = "burner",
        fuel_categories = {"chemical"},
        effectivity = .7,
        fuel_inventory_size = 1,
        emissions_per_minute = {pollution = 1},
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
   fluid_boxes =
{
  {
    production_type = "input",
    pipe_picture = tanks_assembler_pipe_pictures(),
    pipe_covers = pipecoverspictures(),
    volume = 1000,
    pipe_connections =
    {
      {
        flow_direction = "input",
        position = {0, -1},
        direction = defines.direction.north
      }
    },
    secondary_draw_orders = { north = -1 }
  },
  {
    production_type = "output",
    pipe_picture = tanks_assembler_pipe_pictures(),
    pipe_covers = pipecoverspictures(),
    volume = 1000,
    pipe_connections =
    {
      {
        flow_direction = "output",
        position = {0, 1},
        direction = defines.direction.south
      }
    },
    secondary_draw_orders = { north = -1 }
  }
},
	      off_when_no_fluid_recipe = true,

    energy_usage = "10kW",
    ingredient_count = 2,
    module_specification = {module_slots = 0},
},

  --claypit
   {
    type = "assembling-machine",
    icon_size = 64,
    name = "clay-pit",
    icon = "__tanks_for_bob_fork__/graphics/icons/clay-pit.png",
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
   fluid_boxes =
{
  {
    production_type = "input",
    pipe_picture = tanks_assembler_pipe_pictures(),
    pipe_covers = pipecoverspictures(),
    volume = 1000,
    pipe_connections =
    {
      {
        flow_direction = "input",
        position = {0, -1},
        direction = defines.direction.north
      }
    },
    secondary_draw_orders = { north = -1 }
  },
  {
    production_type = "output",
    pipe_picture = tanks_assembler_pipe_pictures(),
    pipe_covers = pipecoverspictures(),
    volume = 1000,
    pipe_connections =
    {
      {
        flow_direction = "output",
        position = {0, 1},
        direction = defines.direction.south
      }
    },
    secondary_draw_orders = { north = -1 }
  }
},

	      off_when_no_fluid_recipe = true,
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
    graphics_set =
    {
      animation = {
          filename = "__tanks_for_bob_fork__/graphics/entity/clay-pit.png",
          priority = "high",
          width = 64,
          height = 64,
          frame_count = 1,
          line_length = 1,
          shift = {0.00, -0.00}
      },
      working_visualisations = {
          {
              animation = {
                  filename = "__tanks_for_bob_fork__/graphics/entity/clay-pit-w.png",
                  priority = "high",
                  width = 64,
                  height = 64,
                  frame_count = 1,
                  line_length = 1,
                  shift = {0.00, -0.00}
              },
              light = {intensity = 0.3, size = 3}
          }
      }
    },

    crafting_categories = {"clay"},
    crafting_speed = 0.30,
    energy_source = {
        type = "burner",
        fuel_categories = {"chemical"},
        effectivity = .5,
        fuel_inventory_size = 1,
        emissions_per_minute = {pollution = 1},
        light_flicker = {
            color = {0, 0, 0},
            minimum_intensity = 0.6,
            maximum_intensity = 0.95
        },
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
    icon = "__tanks_for_bob_fork__/graphics/icons/pit-kiln.png",
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
    graphics_set =
    {
      animation = {
          filename = "__tanks_for_bob_fork__/graphics/entity/pit-kiln.png",
          priority = "high",
          width = 64,
          height = 64,
          frame_count = 1,
          line_length = 1,
          shift = {0.00, -0.00}
      },
      working_visualisations = {
          {
              animation = {
                  filename = "__tanks_for_bob_fork__/graphics/entity/pit-kiln-w.png",
                  priority = "high",
                  width = 64,
                  height = 64,
                  frame_count = 2,
                  line_length = 2,
                  shift = {0.00, -0.00}
              },
              light = {intensity = 0.4, size = 6}
          }
      }
    },

    crafting_categories = {"pit-kiln"},
    crafting_speed = 0.30,
    energy_source = {
        type = "burner",
        fuel_categories = {"chemical"},
        effectivity = .5,
        fuel_inventory_size = 1,
        emissions_per_minute = {pollution = 6},
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

    energy_usage = "20kW",
    ingredient_count = 2,
    module_specification = {module_slots = 0},
},

  --workbench
{
        type = "assembling-machine",
        icon_size = 64,
        name = "workbench",
        icon = "__tanks_for_bob_fork__/graphics/icons/workbench.png",
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
                }
            },
            idle_sound = {filename = "__base__/sound/idle1.ogg", volume = 0.6},
            apparent_volume = 1.5,
        },
        collision_box = {{-0.5, -0.5}, {0.5, 0.5}},
        selection_box = {{-0.9, -0.9}, {0.9, 0.9}},
    graphics_set =
    {
          animation = {
              filename = "__tanks_for_bob_fork__/graphics/entity/workbench/workbench.png",
              priority = "high",
              width = 64,
              height = 64,
              frame_count = 1,
              line_length = 1,
              shift = {0.00, -0.00},
              variation_count = 1,
              hr_version = {
                  filename = "__tanks_for_bob_fork__/graphics/entity/workbench/hr-workbench.png",
                  width = 139,
                  height = 124,
                  frame_count = 1,
                  line_length = 1,
                  shift = util.by_pixel(0, 0),
                  variation_count = 1,
                  scale = 0.5,
              }
          },
          working_visualisations = {
              {
                  animation = {
                      filename = "__tanks_for_bob_fork__/graphics/entity/workbench/workbench-w.png",
                      priority = "high",
                      width = 64,
                      height = 64,
                      frame_count = 4,
                      line_length = 4,
                      shift = {0.00, -0.00},
                          variation_count = 2,
                      hr_version = {
                          filename = "__tanks_for_bob_fork__/graphics/entity/workbench/hr-workbench-w.png",
                          width = 139,
                          height = 124,
                          frame_count = 4,
                          line_length = 4,
                          shift = util.by_pixel(0, 0),
                          variation_count = 2,
                          scale = 0.5,
                      },
                  },
                  light = {intensity = 0.5, size = 5}
              }
          }
    },

        crafting_categories = {"Seablock"},
        crafting_speed = 0.30,
        energy_source = {
            type = "burner",
            fuel_categories = {"chemical"},
            effectivity = 0.5, -- Corrected from .5 to 0.5
            fuel_inventory_size = 1,
            emissions_per_minute = {pollution = .5},
            light_flicker = {
                color = {0, 0, 0},
                minimum_intensity = 0.6,
                maximum_intensity = 1.95
            },
            smoke = {
                {
                    name = "smoke",
                    deviation = {0.1, 0.1},
                    frequency = .5,
                    position = {0.0, -0.8},
                    starting_vertical_speed = 0.08,
                    starting_frame_deviation = 60
                }
            }
        },

        energy_usage = "20kW",
        -- Five early Seablock structures require three distinct ingredients.
        ingredient_count = 3,
        module_specification = {module_slots = 0},
    },
    --campfire
    {
    type = "assembling-machine",
    icon_size = 64,
    name = "campfire",
    icon = "__tanks_for_bob_fork__/graphics/icons/campfire.png",
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
    graphics_set =
    {
      animation = {
          filename = "__tanks_for_bob_fork__/graphics/entity/campfire.png",
          priority = "high",
          width = 64,
          height = 64,
          frame_count = 1,
          line_length = 1,
          shift = {0.00, -0.00}
      },
      working_visualisations = {
          {
              animation = {
                  filename = "__tanks_for_bob_fork__/graphics/entity/campfire-w.png",
                  priority = "high",
                  width = 64,
                  height = 64,
                  frame_count = 2,
                  line_length = 2,
                  shift = {0.00, -0.00}
              },
              light = {intensity = 0.4, size = 6}
          }
      }
    },

    crafting_categories = {"cooking"},
    crafting_speed = 0.30,
    energy_source = {
        type = "burner",
        fuel_categories = {"chemical"},
        effectivity = 1,
        fuel_inventory_size = 1,
        emissions_per_minute = {pollution = 2},
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
    graphics_set =
    {
      animation =
      {
        filename = "__tanks_for_bob_fork__/graphics/entity/tank-assembling-machine/tank-assembling-machine.png",
        priority = "high",
        width = 142,
        height = 113,
        frame_count = 32,
        line_length = 8,
        shift = {0.84, -0.09}
      }
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
    graphics_set =
    {
      animation =
      {
        filename = "__tanks_for_bob_fork__/graphics/entity/tank-assembling-machine/tank-assembling-machine.png",
        priority = "high",
        width = 142,
        height = 113,
        frame_count = 32,
        line_length = 8,
        shift = {0.84, -0.09}
      }
    },

    crafting_categories = {"tank-ammo-component"},
    crafting_speed = 1.00,
    -- Industrial coke produces crude oil; rubberized timber consumes it.
    -- The dedicated ammunition assembler must support BOTH directions.
    fluid_boxes = {
      {
        production_type = "input",
        pipe_picture = tanks_assembler_pipe_pictures(),
        pipe_covers = pipecoverspictures(),
        volume = 1000,
        pipe_connections = {
          {flow_direction = "input", position = {0, -1}, direction = defines.direction.north}
        },
        secondary_draw_orders = {north = -1}
      },
      {
        production_type = "output",
        pipe_picture = tanks_assembler_pipe_pictures(),
        pipe_covers = pipecoverspictures(),
        volume = 1000,
        pipe_connections = {
          {flow_direction = "output", position = {0, 1}, direction = defines.direction.south}
        },
        secondary_draw_orders = {north = -1}
      }
    },
    off_when_no_fluid_recipe = true,
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
	    type = "stream",
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
particle_spawn_interval = 1,
particle_spawn_timeout = 6,
particle_horizontal_speed = 0.2,
particle_horizontal_speed_deviation = 0.05,
particle_vertical_acceleration = 0.005,
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
    collision_mask =
{
  layers =
  {
    doodad = true
  },
  not_colliding_with_itself = true
},
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
        height = 64,
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
  minable = {mining_time = 1, result = "land-mine-poison"},
  max_health = 15,
  corpse = "small-remnants",
  collision_box = {{-0.4, -0.4}, {0.4, 0.4}},
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
            collision_mask =
            {
              layers =
              {
                player = true
              }
            },
            action_delivery =
            {
              type = "instant",
              target_effects =
              {
                {
                  type = "damage",
                  damage = {amount = 300, type = "explosion"}
                }
              }
            }
          }
        },
        {
          type = "create-entity",
          entity_name = "poison-cloud"
        },
        {
          type = "damage",
          damage = {amount = 10, type = "poison"}
        }
      }
    }
  }
},
-- lazer-cloud
  {
    type = "trivial-smoke",
    name = "lazer-cloud",
    flags = {"not-on-map"},
    show_when_smoke_off = true,
    animation =
{
  filename = "__base__/graphics/entity/smoke/smoke.png",
  priority = "low",
  width = 152,
  height = 120,
  frame_count = 60,
  line_length = 5,
  animation_speed = 0.25,
  scale = 3
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
  filename = "__base__/graphics/entity/smoke/smoke.png",
  priority = "low",
  width = 152,
  height = 120,
  frame_count = 60,
  line_length = 5,
  animation_speed = 0.25,
  scale = 3
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
