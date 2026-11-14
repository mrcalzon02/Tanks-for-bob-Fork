-- Beach Pump V12: approved native Blender art, fixed tile scale and split submerged tip.
local pump = assert(data.raw["offshore-pump"]["beachpump"], "Beach Pump not found")
assert(pump.pumping_speed == 0.01 and pump.fluid_source_offset[2] == -1, "Beach Pump gameplay contract changed")
-- Native runtime rejected legacy quarter-tile socket: adjacent pipe was at 1.25.
-- The model flange is at the half-tile edge; standard adjacent pipe is at 1.0.
local connection = assert(pump.fluid_box.pipe_connections[1])
assert(connection.direction == defines.direction.south and connection.position[1] == 0 and connection.position[2] == 0.25, "Unexpected inherited Beach Pump output")
connection.position = {0, 0}
-- Accepted V12 art. Full replacement excludes legacy underwater and reflection art.
pump.graphics_set = {
  underwater_layer_offset = 15,
  base_render_layer = "ground-patch",
  animation = {
    north = { filename = "__tanks_for_bob_fork__/graphics/entity/wooden-offshore-pump/v12/north-working-288.png", width = 288, height = 288, line_length = 8, frame_count = 32, animation_speed = 0.25, scale = 0.5, shift = {0.00000000, -0.65760939} },
    east = { filename = "__tanks_for_bob_fork__/graphics/entity/wooden-offshore-pump/v12/east-working-288.png", width = 288, height = 288, line_length = 8, frame_count = 32, animation_speed = 0.25, scale = 0.5, shift = {0.00000000, -0.65760939} },
    south = { filename = "__tanks_for_bob_fork__/graphics/entity/wooden-offshore-pump/v12/south-working-288.png", width = 288, height = 288, line_length = 8, frame_count = 32, animation_speed = 0.25, scale = 0.5, shift = {0.00000000, -0.65760939} },
    west = { filename = "__tanks_for_bob_fork__/graphics/entity/wooden-offshore-pump/v12/west-working-288.png", width = 288, height = 288, line_length = 8, frame_count = 32, animation_speed = 0.25, scale = 0.5, shift = {0.00000000, -0.65760939} },
  },
  underwater_pictures = {
    north = { filename = "__tanks_for_bob_fork__/graphics/entity/wooden-offshore-pump/v12/north-underwater-288.png", width = 288, height = 288, scale = 0.5, shift = {0.00000000, -0.65760939} },
    east = { filename = "__tanks_for_bob_fork__/graphics/entity/wooden-offshore-pump/v12/east-underwater-288.png", width = 288, height = 288, scale = 0.5, shift = {0.00000000, -0.65760939} },
    south = { filename = "__tanks_for_bob_fork__/graphics/entity/wooden-offshore-pump/v12/south-underwater-288.png", width = 288, height = 288, scale = 0.5, shift = {0.00000000, -0.65760939} },
    west = { filename = "__tanks_for_bob_fork__/graphics/entity/wooden-offshore-pump/v12/west-underwater-288.png", width = 288, height = 288, scale = 0.5, shift = {0.00000000, -0.65760939} },
  }
}

-- A legacy vanilla reflection must not depict a different pump underneath this model.
pump.water_reflection = nil
local icon = "__tanks_for_bob_fork__/graphics/icons/beachpump-v12.png"
pump.icon = icon
pump.icon_size = 64
pump.icon_mipmaps = nil
local item = data.raw.item["beachpump"]
if item then item.icon = icon; item.icon_size = 64; item.icon_mipmaps = nil end

-- Per-facing registration measured against the real Factorio adjacent pipe.
local registered_shift={north={0.00000000,-0.45625000},east={0.10000000,-0.48750000},south={0.00000000,-0.17500000},west={-0.11875000,-0.48750000}}
for facing,shift in pairs(registered_shift) do
  for _,set in ipairs({pump.graphics_set.animation,pump.graphics_set.underwater_pictures}) do
    set[facing].scale=0.6
    set[facing].shift=shift
  end
end
