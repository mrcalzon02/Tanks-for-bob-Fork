-- Owner-accepted V3 two-port pipe pump, genuine four-way 16-frame Blender capture.
-- Preserve burner/rate/footprint; normalize legacy off-grid pipe cells below.
local pump = data.raw.pump["primitive-steam-powered-pump"]
assert(pump, "Primitive pipe-pump graphics require the original native pump")
-- A two-tile native pump uses half-tile internal connection cells. The legacy
-- +/- .75 positions target pipes at quarter-tile coordinates, which cannot be
-- reproduced by normal player placement. Keep the same faces and flows.
for _, port in ipairs(pump.fluid_box.pipe_connections) do
  assert(port.position[1] == 0 and (math.abs(port.position[2]) == .75 or math.abs(port.position[2]) == .5))
  port.position = {0, port.position[2] < 0 and -.5 or .5}
end
local root = "__tanks_for_bob_fork__/graphics/entity/primitive-pipe-pump-v3/"
local function facing(name, row, vertical)
  -- The derived capture unforeshortens the ground axis to Factorio's square
  -- tile grid. All four facings therefore use the same physical pixel scale.
  local scale = 32 * 3.85 / 256
  return {
    filename = root .. "working-256.png",
    priority = "high", width = 256, height = 256,
    x = 0, y = row * 512, line_length = 8, frame_count = 16,
    animation_speed = 8/60, scale = scale,
    shift = {0, -0.93/math.sqrt(2) + .25}
  }
end
pump.animations = {
  north = facing("north", 0, true),
  east = facing("east", 1, false),
  south = facing("south", 2, true),
  west = facing("west", 3, false)
}
-- The source captures the complete physical machine, glass and liquid sight.
-- Retaining vanilla overlays would draw a second unrelated pump over it.
pump.fluid_animation = nil
pump.glass_pictures = nil
