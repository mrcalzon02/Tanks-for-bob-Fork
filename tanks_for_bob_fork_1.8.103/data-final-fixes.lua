-- Visual-only one-tile registration of the approved V7 corrected hammer workbench.
-- Keep 1x1 collision, recipes, production, fuel and south-facing fluid outlet unchanged.
-- Render source: verified OLD-CORE30 V7 Blender 5.2 animation (four directions, 96 frames).
local bench = data.raw["assembling-machine"] and data.raw["assembling-machine"]["workbench"]
if bench then
  local root = "__tanks_for_bob_fork__/graphics/entity/workbench-v8-one-tile/"
  local function one_way(name, idle)
    return {
      filename = root .. (idle and "idle-" or "working-") .. name .. ".png",
      priority = "high", width = 128, height = 128,
      frame_count = idle and 1 or 96,
      repeat_count = idle and 96 or 1,
      line_length = idle and 1 or 12,
      animation_speed = 0.2,
      scale = 0.33,
      shift = {0, -0.07}
    }
  end
  local function four_way(idle)
    return {
      north = one_way("north", idle),
      east = one_way("east", idle),
      south = one_way("south", idle),
      west = one_way("west", idle)
    }
  end
  bench.graphics_set = {
    animation = four_way(false),
    idle_animation = four_way(true),
    always_draw_idle_animation = false
  }
  bench.selection_box = {{-0.5, -0.5}, {0.5, 0.5}}
  bench.match_animation_speed_to_activity = false
  -- No other prototype parameters are changed; existing fluid box remains south.
end

-- Accepted Cooking Fire V2: four-direction idle/working art, no gameplay changes.
require("prototypes.generated_graphics.cooking-fire-v2-production")

-- Approved V8 Solar Boiler; BoilerPictureSet adapter, 3x2 original connections.
require("prototypes.generated_graphics.solar-boiler-v8-production")

-- Accepted Beach Pump V12 and native tile-aligned output socket.
require("prototypes.generated_graphics.beach-pump-v12-production")
