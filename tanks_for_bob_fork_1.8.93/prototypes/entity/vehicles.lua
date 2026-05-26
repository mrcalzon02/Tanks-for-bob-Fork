--Battle Tanks
-- Vehicle scale helpers
-- Keeps body sprites, turret sprites, selection boxes, and collision boxes in the same visual family.
-- Normal-resolution sprite scale and hr_version scale are intentionally different: Factorio HR sprites are normally half-scale.
-- Standardized vehicle sizing.
-- 1.08 keeps each vehicle slightly larger visually; 2.16 doubles the collision/selection footprint from the prior pass.
-- Turret/mask offsets are centralized so every tank uses the same hull-relative anchor.
local STANDARD_VEHICLE_BODY_SCALE = 1.08
-- The vanilla tank body sprite and the runtime-tint body mask do not stay visually aligned
-- after this mod's enlarged vehicle pass if they are forced to the exact same scale.
-- Keep the actual hull at 1.08, but slightly over-scale only the body tint mask so
-- the team-color layer reaches the same apparent hull coverage as the base-game tank.
local STANDARD_VEHICLE_BODY_TINT_SCALE = 1.15
-- Raise only the hull/body runtime-tint layer after scaling; negative Y is upward in util.by_pixel-style pixel space.
local STANDARD_VEHICLE_BODY_TINT_Y_OFFSET_PIXELS = -15.0
local STANDARD_VEHICLE_TURRET_SCALE = 2.28
local STANDARD_VEHICLE_FOOTPRINT_SCALE = 2.16
local STANDARD_TURRET_X_OFFSET_PIXELS = -13.0
local STANDARD_TURRET_Y_OFFSET_PIXELS = -69.5
local STANDARD_TURRET_MASK_X_OFFSET_PIXELS = -13.0
local STANDARD_TURRET_MASK_Y_OFFSET_PIXELS = -54.0

local function set_layered_animation_scale(animation, scale)
  if not animation or not animation.layers then return end
  for _, layer in pairs(animation.layers) do
    if layer then
      layer.scale = scale
      if layer.hr_version then
        layer.hr_version.scale = scale / 2
      end
    end
  end
end

local function set_tank_body_animation_scale(animation, body_scale, body_tint_scale)
  if not animation or not animation.layers then return end
  body_tint_scale = body_tint_scale or body_scale

  for _, layer in pairs(animation.layers) do
    if layer then
      local layer_scale = layer.apply_runtime_tint and body_tint_scale or body_scale
      layer.scale = layer_scale
      if layer.hr_version then
        layer.hr_version.scale = layer_scale / 2
      end
    end
  end
end

local function shift_body_tint_y(animation, y_pixels)
  if not animation or not animation.layers then return end
  for _, layer in pairs(animation.layers) do
    if layer and layer.apply_runtime_tint then
      local shift = layer.shift or {0, 0}
      layer.shift = {shift[1] or 0, (shift[2] or 0) + y_pixels / 32}

      if layer.hr_version then
        local hr_shift = layer.hr_version.shift or shift
        layer.hr_version.shift = {hr_shift[1] or 0, (hr_shift[2] or 0) + y_pixels / 32}
      end
    end
  end
end

local function set_vehicle_footprint(vehicle, width_scale, length_scale)
  length_scale = length_scale or width_scale
  vehicle.collision_box = {{-0.9 * width_scale, -1.3 * length_scale}, {0.9 * width_scale, 1.3 * length_scale}}
  vehicle.selection_box = {{-0.9 * width_scale, -1.3 * length_scale}, {0.9 * width_scale, 1.3 * length_scale}}
end

local function use_turreta_turret_sprite(vehicle)
  if not vehicle or not vehicle.turret_animation or not vehicle.turret_animation.layers then return end

  -- All tank turret sprites are forced to the same anchor point so they sit
  -- consistently relative to the hull instead of inheriting per-variant offsets.
  -- Raised 7 pixels from v4 and kept shifted left about 13 pixels to center the turret on the hull.
  local turret_shift = util.by_pixel(STANDARD_TURRET_X_OFFSET_PIXELS, STANDARD_TURRET_Y_OFFSET_PIXELS)
  local tint_shift = util.by_pixel(STANDARD_TURRET_MASK_X_OFFSET_PIXELS, STANDARD_TURRET_MASK_Y_OFFSET_PIXELS)

  for _, layer in pairs(vehicle.turret_animation.layers) do
    if layer then
      if layer.apply_runtime_tint then
        layer.filename = "__tanks_for_bob_fork__/graphics/entity/tank/tank-turret-maske.png"
        layer.width = 36
        layer.height = 33
        layer.shift = tint_shift
        -- Keep the team-color mask matched to the turret scale; the prior 1.25 multiplier over-expanded it onto the hull.
        layer.scale = STANDARD_VEHICLE_TURRET_SCALE
        if layer.hr_version then
          layer.hr_version.filename = "__tanks_for_bob_fork__/graphics/entity/tank/hr-tank-turret-maske.png"
          layer.hr_version.width = 72
          layer.hr_version.height = 66
          layer.hr_version.shift = tint_shift
          layer.hr_version.scale = STANDARD_VEHICLE_TURRET_SCALE / 2
        end
      else
        layer.filename = "__tanks_for_bob_fork__/graphics/entity/tank/tank-turreta.png"
        layer.width = 90
        layer.height = 67
        layer.shift = turret_shift
        layer.scale = STANDARD_VEHICLE_TURRET_SCALE
        if layer.hr_version then
          layer.hr_version.filename = "__tanks_for_bob_fork__/graphics/entity/tank/hr-tank-turreta.png"
          layer.hr_version.width = 179
          layer.hr_version.height = 132
          layer.hr_version.shift = turret_shift
          layer.hr_version.scale = STANDARD_VEHICLE_TURRET_SCALE / 2
        end
      end
    end
  end
end

local function scale_tank_vehicle(vehicle, body_scale, turret_scale, width_scale, length_scale, body_tint_scale)
  set_tank_body_animation_scale(vehicle.animation, body_scale, body_tint_scale or STANDARD_VEHICLE_BODY_TINT_SCALE)
  shift_body_tint_y(vehicle.animation, STANDARD_VEHICLE_BODY_TINT_Y_OFFSET_PIXELS)
  set_layered_animation_scale(vehicle.turret_animation, turret_scale or body_scale)
  use_turreta_turret_sprite(vehicle)
  set_vehicle_footprint(vehicle, width_scale or body_scale, length_scale or body_scale)
end

local function shift_animation_y(animation, y_pixels)
  if not animation or not animation.layers then return end
  for _, layer in pairs(animation.layers) do
    if layer then
      local shift = layer.shift or {0, 0}
      layer.shift = {shift[1] or 0, (shift[2] or 0) + y_pixels / 32}
      if layer.hr_version then
        local hr_shift = layer.hr_version.shift or shift
        layer.hr_version.shift = {hr_shift[1] or 0, (hr_shift[2] or 0) + y_pixels / 32}
      end
    end
  end
end

local function shift_vehicle_turret_y(vehicle, y_pixels)
  shift_animation_y(vehicle.turret_animation, y_pixels)
end

-- Modular tank T1
local modularTank = table.deepcopy(data.raw.car["tank"])
modularTank.name = "modular-tank"
modularTank.icon = "__tanks_for_bob_fork__/graphics/icons/auto-tank.png"
modularTank.max_health = 1200
modularTank.minable = {mining_time = 1, result = "modular-tank"}
modularTank.resistances = {
      {
        type = "fire",
        decrease = 15,
        percent = 60
      },
      {
        type = "physical",
        decrease = 15,
        percent = 60
      },
      {
        type = "impact",
        decrease = 50,
        percent = 60
      },
      {
        type = "explosion",
        decrease = 15,
        percent = 50
      },
      {
        type = "acid",
        decrease = 15,
        percent = 35
      }
    }
modularTank.turret_rotation_speed = 0.10 /60
modularTank.weight = 10000
modularTank.inventory_size = 4
modularTank.guns = { "tank-auto-cannon", "tank-cannon-2" }

scale_tank_vehicle(modularTank, STANDARD_VEHICLE_BODY_SCALE, STANDARD_VEHICLE_TURRET_SCALE, STANDARD_VEHICLE_FOOTPRINT_SCALE, STANDARD_VEHICLE_FOOTPRINT_SCALE)

data:extend{modularTank}

--Battle Tanks
-- flame-tank
local flameTank = table.deepcopy(data.raw.car["tank"])
flameTank.name = "flame-tank"
flameTank.icon = "__tanks_for_bob_fork__/graphics/icons/flame-tank.png"
flameTank.max_health = 1250
flameTank.minable = {mining_time = 1, result = "flame-tank"}
flameTank.resistances = {
      {
        type = "fire",
        decrease = 95,
        percent = 95
      },
      {
        type = "physical",
        decrease = 25,
        percent = 45
      },
      {
        type = "impact",
        decrease = 50,
        percent = 60
      },
      {
        type = "explosion",
        decrease = 30,
        percent = 45
      },
      {
        type = "acid",
        decrease = 20,
        percent = 40
      }
    }
flameTank.turret_rotation_speed = 0.10 /60
flameTank.braking_power = "300kW"
flameTank.weight = 10000
flameTank.inventory_size = 10
flameTank.rotation_speed = 0.0055
flameTank.guns = { "tank-flamer", "tank-flamer-2" }

scale_tank_vehicle(flameTank, STANDARD_VEHICLE_BODY_SCALE, STANDARD_VEHICLE_TURRET_SCALE, STANDARD_VEHICLE_FOOTPRINT_SCALE, STANDARD_VEHICLE_FOOTPRINT_SCALE)

data:extend{flameTank}

--flame-tank lvl2

--Battle Tanks
-- flame-tank
local flameTankWLSK = table.deepcopy(data.raw.car["tank"])
flameTankWLSK.name = "flame-tank-wlsk"
flameTankWLSK.icon = "__tanks_for_bob_fork__/graphics/icons/flame-tank-wlsk.png"
flameTankWLSK.max_health = 2000
flameTankWLSK.minable = {mining_time = 1, result = "flame-tank-wlsk"}
flameTankWLSK.resistances = {
      {
        type = "fire",
        decrease = 95,
        percent = 95
      },
      {
        type = "physical",
        decrease = 35,
        percent = 55
      },
      {
        type = "impact",
        decrease = 50,
        percent = 60
      },
      {
        type = "explosion",
        decrease = 30,
        percent = 45
      },
      {
        type = "acid",
        decrease = 25,
        percent = 45
      }
    }
flameTankWLSK.turret_rotation_speed = 0.10 /60
flameTankWLSK.braking_power = "300kW"
flameTankWLSK.weight = 20000
flameTankWLSK.inventory_size = 10
flameTankWLSK.rotation_speed = 0.0055
flameTankWLSK.guns = { "tank-flamer", "tank-flamer-2" }

scale_tank_vehicle(flameTankWLSK, STANDARD_VEHICLE_BODY_SCALE, STANDARD_VEHICLE_TURRET_SCALE, STANDARD_VEHICLE_FOOTPRINT_SCALE, STANDARD_VEHICLE_FOOTPRINT_SCALE)

data:extend{flameTankWLSK}

--auto-tank
local autoTank = table.deepcopy(data.raw.car["tank"])
autoTank.name = "auto-tank"
autoTank.icon = "__tanks_for_bob_fork__/graphics/icons/auto-tank.png"
autoTank.max_health = 3000
autoTank.minable = {mining_time = 1, result = "auto-tank"}
autoTank.resistances = {
      {
        type = "fire",
        decrease = 15,
        percent = 50
      },
      {
        type = "physical",
        decrease = 15,
        percent = 30
      },
      {
        type = "impact",
        decrease = 50,
        percent = 60
      },
      {
        type = "explosion",
        decrease = 15,
        percent = 30
      },
      {
        type = "acid",
        decrease = 15,
        percent = 25
      }
    }
autoTank.turret_rotation_speed = 0.10 /60
autoTank.braking_power = "500kW"    
autoTank.weight = 10000
autoTank.inventory_size = 9
autoTank.guns = { "tank-auto-cannon", "tank-cannon-2" }
autoTank.rotation_speed = 0.0035

scale_tank_vehicle(autoTank, STANDARD_VEHICLE_BODY_SCALE, STANDARD_VEHICLE_TURRET_SCALE, STANDARD_VEHICLE_FOOTPRINT_SCALE, STANDARD_VEHICLE_FOOTPRINT_SCALE)

data:extend{autoTank}

--auto-tank-lvl2
local autoTankWLSK = table.deepcopy(data.raw.car["tank"])
autoTankWLSK.name = "auto-tank-wlsk"
autoTankWLSK.icon = "__tanks_for_bob_fork__/graphics/icons/auto-tank-lvl2.png"
autoTankWLSK.max_health = 3750
autoTankWLSK.minable = {mining_time = 1, result = "auto-tank-wlsk"}
autoTankWLSK.resistances = {
      {
        type = "fire",
        decrease = 15,
        percent = 50
      },
      {
        type = "physical",
        decrease = 15,
        percent = 35
      },
      {
        type = "impact",
        decrease = 50,
        percent = 60
      },
      {
        type = "explosion",
        decrease = 20,
        percent = 35
      },
      {
        type = "acid",
        decrease = 15,
        percent = 35
      }
    }
autoTankWLSK.turret_rotation_speed = 0.10 /60
autoTankWLSK.braking_power = "500kW"
autoTankWLSK.weight = 10000
autoTankWLSK.inventory_size = 9
autoTankWLSK.guns = { "tank-auto-cannon", "tank-cannon-2" }
autoTankWLSK.rotation_speed = 0.0035

scale_tank_vehicle(autoTankWLSK, STANDARD_VEHICLE_BODY_SCALE, STANDARD_VEHICLE_TURRET_SCALE, STANDARD_VEHICLE_FOOTPRINT_SCALE, STANDARD_VEHICLE_FOOTPRINT_SCALE)

data:extend{autoTankWLSK}


--auto-tank-lvl2
local nadeTank = table.deepcopy(data.raw.car["tank"])
nadeTank.name = "nade-tank"
nadeTank.icon = "__tanks_for_bob_fork__/graphics/icons/nade-tank.png"
nadeTank.max_health = 1000
nadeTank.minable = {mining_time = 1, result = "nade-tank"}
nadeTank.resistances = {
      {
        type = "fire",
        decrease = 15,
        percent = 50
      },
      {
        type = "physical",
        decrease = 15,
        percent = 30
      },
      {
        type = "impact",
        decrease = 50,
        percent = 60
      },
      {
        type = "explosion",
        decrease = 15,
        percent = 30
      },
      {
        type = "acid",
        decrease = 10,
        percent = 20
      }
    }
nadeTank.turret_rotation_speed = 0.10 /60
nadeTank.braking_power = "500kW"
nadeTank.weight = 10000
nadeTank.inventory_size = 13
nadeTank.guns = { "tank-machinegun-turret", "tank-nade-cannon" }
nadeTank.rotation_speed = 0.0035

scale_tank_vehicle(nadeTank, STANDARD_VEHICLE_BODY_SCALE, STANDARD_VEHICLE_TURRET_SCALE, STANDARD_VEHICLE_FOOTPRINT_SCALE, STANDARD_VEHICLE_FOOTPRINT_SCALE)

data:extend{nadeTank}

--nade-tank-wlsk
local nadeTankWLSK = table.deepcopy(data.raw.car["tank"])
nadeTankWLSK.name = "nade-tank-wlsk"
nadeTankWLSK.icon = "__tanks_for_bob_fork__/graphics/icons/nade-tank-wlsk.png"
nadeTankWLSK.max_health = 1750
nadeTankWLSK.minable = {mining_time = 1, result = "nade-tank-wlsk"}
nadeTankWLSK.resistances = {
      {
        type = "fire",
        decrease = 15,
        percent = 50
      },
      {
        type = "physical",
        decrease = 15,
        percent = 35
      },
      {
        type = "impact",
        decrease = 50,
        percent = 60
      },
      {
        type = "explosion",
        decrease = 20,
        percent = 35
      },
      {
        type = "acid",
        decrease = 15,
        percent = 30
      }
    }
nadeTankWLSK.turret_rotation_speed = 0.10 /60
nadeTankWLSK.braking_power = "500kW"
nadeTankWLSK.weight = 10000
nadeTankWLSK.inventory_size = 14
nadeTankWLSK.guns = { "tank-machinegun-turret", "tank-nade-cannon" }
nadeTankWLSK.rotation_speed = 0.0035

scale_tank_vehicle(nadeTankWLSK, STANDARD_VEHICLE_BODY_SCALE, STANDARD_VEHICLE_TURRET_SCALE, STANDARD_VEHICLE_FOOTPRINT_SCALE, STANDARD_VEHICLE_FOOTPRINT_SCALE)

data:extend{nadeTankWLSK}

--mine-tank
local mineTank = table.deepcopy(data.raw.car["tank"])
mineTank.name = "mine-tank"
mineTank.icon = "__tanks_for_bob_fork__/graphics/icons/mine-tank.png"
mineTank.max_health = 1000
mineTank.minable = {mining_time = 1, result = "mine-tank"}
mineTank.resistances = {
      {
        type = "fire",
        decrease = 15,
        percent = 50
      },
      {
        type = "physical",
        decrease = 15,
        percent = 30
      },
      {
        type = "impact",
        decrease = 50,
        percent = 60
      },
      {
        type = "explosion",
        decrease = 15,
        percent = 30
      },
      {
        type = "acid",
        decrease = 10,
        percent = 20
      }
    }
mineTank.turret_rotation_speed = 0.10 /60
mineTank.braking_power = "500kW"
mineTank.weight = 10000
mineTank.inventory_size = 15
mineTank.guns = { "tank-mine-cannon", "combat-shotgun" }
mineTank.rotation_speed = 0.0035

scale_tank_vehicle(mineTank, STANDARD_VEHICLE_BODY_SCALE, STANDARD_VEHICLE_TURRET_SCALE, STANDARD_VEHICLE_FOOTPRINT_SCALE, STANDARD_VEHICLE_FOOTPRINT_SCALE)

data:extend{mineTank}

--rocket-tank
local rocketTank = table.deepcopy(data.raw.car["tank"])
rocketTank.name = "rocket-tank"
rocketTank.icon = "__tanks_for_bob_fork__/graphics/icons/rocket-tank.png"
rocketTank.max_health = 1000
rocketTank.minable = {mining_time = 1, result = "rocket-tank"}
rocketTank.resistances = {
    {
      type = "fire",
      decrease = 15,
      percent = 50
    },
    {
      type = "physical",
      decrease = 15,
      percent = 30
    },
    {
      type = "impact",
      decrease = 50,
        percent = 60
    },
    {
      type = "explosion",
      decrease = 15,
      percent = 30
    },
    {
      type = "acid",
      decrease = 10,
      percent = 20
    }
  }
rocketTank.turret_rotation_speed = 0.10 /60
rocketTank.braking_power = "500kW"
rocketTank.weight = 10000
rocketTank.inventory_size = 10
rocketTank.guns = { "tank-machinegun-turret", "tank-rocket-cannon"}
rocketTank.rotation_speed = 0.0035

scale_tank_vehicle(rocketTank, STANDARD_VEHICLE_BODY_SCALE, STANDARD_VEHICLE_TURRET_SCALE, STANDARD_VEHICLE_FOOTPRINT_SCALE, STANDARD_VEHICLE_FOOTPRINT_SCALE)

data:extend{rocketTank}

--SuperTank shared
local superTank_shared_resistances = {
      {
        type = "fire",
        decrease = 15,
        percent = 65
      },
      {
        type = "physical",
        decrease = 35,
        percent = 65
      },
      {
        type = "impact",
        decrease = 15,
        percent = 65
      },
      {
        type = "explosion",
        decrease = 15,
        percent = 65
      },
      {
        type = "acid",
        decrease = 10,
        percent = 50
      }
    }
local superTank_shared_collision_box = {{-0.9 * STANDARD_VEHICLE_FOOTPRINT_SCALE, -1.3 * STANDARD_VEHICLE_FOOTPRINT_SCALE}, {0.9 * STANDARD_VEHICLE_FOOTPRINT_SCALE, 1.3 * STANDARD_VEHICLE_FOOTPRINT_SCALE}}
local superTank_shared_selection_box =  {{-0.9 * STANDARD_VEHICLE_FOOTPRINT_SCALE, -1.3 * STANDARD_VEHICLE_FOOTPRINT_SCALE}, {0.9 * STANDARD_VEHICLE_FOOTPRINT_SCALE, 1.3 * STANDARD_VEHICLE_FOOTPRINT_SCALE}}
local superTank_shared_burner =     {
      effectivity = 0.5,
      fuel_inventory_size = 4,
      smoke =
      {
        {
          name = "smoke",
          deviation = {0.25, 0.25},
          frequency = 50,
          position = {-0.75, 2.50},
          slow_down_factor = 0.9,
          starting_frame = 3,
          starting_frame_deviation = 5,
          starting_frame_speed = 0,
          starting_frame_speed_deviation = 5
        },
        {
          name = "smoke",
          deviation = {0.25, 0.25},
          frequency = 75,
          position = {0.0, 2.50},
          slow_down_factor = 0.9,
          starting_frame = 3,
          starting_frame_deviation = 5,
          starting_frame_speed = 0,
          starting_frame_speed_deviation = 5
        },
        {
          name = "smoke",
          deviation = {0.25, 0.25},
          frequency = 50,
          position = {0.75, 2.50},
          slow_down_factor = 0.9,
          starting_frame = 3,
          starting_frame_deviation = 5,
          starting_frame_speed = 0,
          starting_frame_speed_deviation = 5
        }
      }
    }

--Super Heavy
local superTank = table.deepcopy(data.raw.car["tank"])

superTank.name = "super-tank"
superTank.icon = "__tanks_for_bob_fork__/graphics/icons/super-tank.png"
superTank.max_health = 4500
superTank.minable = {mining_time = 1, result = "super-tank"}
superTank.corpse = "big-remnants"
superTank.dying_explosion = "medium-explosion"

superTank.resistances = superTank_shared_resistances
superTank.collision_box = superTank_shared_collision_box
superTank.selection_box = superTank_shared_selection_box
superTank.burner = superTank_shared_burner

local tank_shift_y2 = -10
superTank.turret_animation =
    {
      layers =
      {
        {
          filename = "__tanks_for_bob_fork__/graphics/entity/tank/tank-turreta.png",
          priority = "low",
          line_length = 8,
          width = 90,
          height = 67,
          frame_count = 1,
          direction_count = 64,
		  shift = util.by_pixel(1.25-2, -40.5 + tank_shift_y2),
          animation_speed = 8,
		  scale = 1.05,
          hr_version =
          {
            filename = "__tanks_for_bob_fork__/graphics/entity/tank/hr-tank-turreta.png",
            priority = "low",
            line_length = 8,
            width = 179,
            height = 132,
            frame_count = 1,
            direction_count = 64,
			shift = util.by_pixel(1.25-2, -40.5 + tank_shift_y2),
            animation_speed = 8,
			scale = 0.525,
          }
        },
        {
          filename = "__tanks_for_bob_fork__/graphics/entity/tank/tank-turret-maske.png",
          priority = "low",
          line_length = 8,
          width = 36,
          height = 33,
          frame_count = 1,
          apply_runtime_tint = true,
          direction_count = 64,
		  shift = util.by_pixel(0, -25. + tank_shift_y2),
		  scale = 1.05,
          hr_version =
          {
            filename = "__tanks_for_bob_fork__/graphics/entity/tank/hr-tank-turret-maske.png",
            priority = "low",
            line_length = 8,
            width = 72,
            height = 66,
            frame_count = 1,
            apply_runtime_tint = true,
            direction_count = 64,
            shift = util.by_pixel(0, -25. + tank_shift_y2),
            scale = 0.525,
          }
        },
      }
    }
superTank.turret_rotation_speed = 0.50 /60
superTank.braking_power = "250kW"
superTank.weight = 50000
superTank.inventory_size = 32
superTank.guns = { "tank-machinegun-turret", "tank-cannon-2" }
superTank.rotation_speed = 0.0035
superTank.consumption = "1250kW"
set_tank_body_animation_scale(superTank.animation, STANDARD_VEHICLE_BODY_SCALE, STANDARD_VEHICLE_BODY_TINT_SCALE)
shift_body_tint_y(superTank.animation, STANDARD_VEHICLE_BODY_TINT_Y_OFFSET_PIXELS)
set_layered_animation_scale(superTank.turret_animation, STANDARD_VEHICLE_TURRET_SCALE)
use_turreta_turret_sprite(superTank)
set_vehicle_footprint(superTank, STANDARD_VEHICLE_FOOTPRINT_SCALE, STANDARD_VEHICLE_FOOTPRINT_SCALE)

data:extend{superTank}

-- Super tank alternative

local superTankAlternative = table.deepcopy(data.raw.car["tank"])
superTankAlternative.name = "super-tank-alternate"
superTankAlternative.icon = "__tanks_for_bob_fork__/graphics/icons/super-tank-alternate.png"
superTankAlternative.max_health = 4500
superTankAlternative.minable = {mining_time = 1, result = "super-tank-alternate"}
superTankAlternative.corpse = "big-remnants"
superTankAlternative.dying_explosion = "medium-explosion"

superTankAlternative.resistances = superTank_shared_resistances
superTankAlternative.collision_box = superTank_shared_collision_box
superTankAlternative.selection_box = superTank_shared_selection_box
superTankAlternative.burner = superTank_shared_burner

scale_tank_vehicle(superTankAlternative, STANDARD_VEHICLE_BODY_SCALE, STANDARD_VEHICLE_TURRET_SCALE, STANDARD_VEHICLE_FOOTPRINT_SCALE, STANDARD_VEHICLE_FOOTPRINT_SCALE)

superTankAlternative.turret_rotation_speed = 0.50 /60
superTankAlternative.braking_power = "250kW"
superTankAlternative.weight = 50000
superTankAlternative.inventory_size = 64
superTankAlternative.guns = { "tank-flamer-2", "tank-mine-cannon" }
superTankAlternative.rotation_speed = 0.0035
superTankAlternative.consumption = "1250kW"

data:extend{superTankAlternative}


-- Super tank alternative

local superTankWMD = table.deepcopy(data.raw.car["tank"])
superTankWMD.name = "super-tank-wmd"
superTankWMD.icon = "__tanks_for_bob_fork__/graphics/icons/super-tank-alternate.png"
superTankWMD.max_health = 4500
superTankWMD.minable = {mining_time = 1, result = "super-tank-wmd"}
superTankWMD.corpse = "big-remnants"
superTankWMD.dying_explosion = "medium-explosion"

superTankWMD.resistances = superTank_shared_resistances
superTankWMD.collision_box = superTank_shared_collision_box
superTankWMD.selection_box = superTank_shared_selection_box
superTankWMD.burner = superTank_shared_burner

scale_tank_vehicle(superTankWMD, STANDARD_VEHICLE_BODY_SCALE, STANDARD_VEHICLE_TURRET_SCALE, STANDARD_VEHICLE_FOOTPRINT_SCALE, STANDARD_VEHICLE_FOOTPRINT_SCALE)

superTankWMD.turret_rotation_speed = 0.50 /60
superTankWMD.braking_power = "250kW"
superTankWMD.weight = 50000
superTankWMD.inventory_size = 32
superTankWMD.guns = { "tank-wmd-cannon", "tank-machinegun-turret" }
superTankWMD.rotation_speed = 0.0035
superTankWMD.consumption = "1250kW"

data:extend{superTankWMD}

--car-flamer

local carFlamer = table.deepcopy(data.raw.car["car"])
carFlamer.name = "car-flamer"
carFlamer.icon = "__tanks_for_bob_fork__/graphics/icons/car-flamer.png"
carFlamer.max_health = 450
carFlamer.minable = {mining_time = 1, result = "car-flamer"}
carFlamer.resistances =     {
      {
        type = "fire",
        percent = 95
      },
      {
        type = "impact",
        percent = 50,
        decrease = 55
      }
    }
carFlamer.turret_rotation_speed = 0.50 /60
carFlamer.braking_power = "500kW"
carFlamer.weight = 750
carFlamer.inventory_size = 25
carFlamer.guns = { "tank-flamer", "tank-machinegun-turret" }
carFlamer.rotation_speed = 0.015
set_layered_animation_scale(carFlamer.animation, STANDARD_VEHICLE_BODY_SCALE)
set_layered_animation_scale(carFlamer.turret_animation, STANDARD_VEHICLE_TURRET_SCALE)
carFlamer.collision_box = {{-0.7 * STANDARD_VEHICLE_FOOTPRINT_SCALE, -1.0 * STANDARD_VEHICLE_FOOTPRINT_SCALE}, {0.7 * STANDARD_VEHICLE_FOOTPRINT_SCALE, 1.0 * STANDARD_VEHICLE_FOOTPRINT_SCALE}}
carFlamer.selection_box = {{-0.8 * STANDARD_VEHICLE_FOOTPRINT_SCALE, -1.1 * STANDARD_VEHICLE_FOOTPRINT_SCALE}, {0.8 * STANDARD_VEHICLE_FOOTPRINT_SCALE, 1.1 * STANDARD_VEHICLE_FOOTPRINT_SCALE}}

data:extend{carFlamer}