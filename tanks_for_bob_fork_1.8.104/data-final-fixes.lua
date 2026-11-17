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

-- Accepted primitive pipe pump: restrained native mechanism animation, same gameplay.
require("prototypes.generated_graphics.primitive-pipe-pump-v3-production")

-- Accepted Fish Pond: preserved clay basin and restrained swimming animation.
require("prototypes.generated_graphics.fish-pond-v2-production")

-- Reviewed modeled material and missing-item inventory artwork.
require("prototypes.generated_graphics.material-icons-v01")

-- Tanks compressor: owner-identified barrel/frame source, same gameplay.
require("prototypes.generated_graphics.steam-compressor-v2-production")

-- Native passive storage with actual fluid-level and flow visualization.
require("prototypes.generated_graphics.wood-basin-v1-production")

-- Detailed excavation hoist with terrain rooted into the native ground plane.
require("prototypes.generated_graphics.quarry-v5-production")

-- Low-tech steam/water waste processing and guided canister packing.
require("prototypes.generated_graphics.shaler-v2-production")

-- Heated mineral growth bed with constrained geared paddle drive.
require("prototypes.generated_graphics.calcifier-v2-production")

-- Timber/thatch burner research shelter and its supported study lantern.
require("prototypes.generated_graphics.thinking-hut-v1-production")

-- Masonry research upgrade with fitted folio, balance and working lantern.
require("prototypes.generated_graphics.pondering-hovel-v1-production")

-- Upright bucket shoreline intake with animated upper and submerged layers.
require("prototypes.generated_graphics.stone-wheel-v3-production")

-- Primitive electric press, packing and closed wood/oil component works.
require("prototypes.generated_graphics.tank-ammo-assembler-v1-production")
require("prototypes.generated_graphics.tank-assembler-v1-production")
require("prototypes.generated_graphics.steam-condenser-v2-production")
