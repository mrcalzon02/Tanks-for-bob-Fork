-- Staged Fish Pond V2 adapter. Promotion must replace only the asset prefix.
local target = assert(data.raw["assembling-machine"]["fish-pond"])
local prefix = "__fish-pond-v2-proof__/graphics/"
local function facings(state)
  local result = {}
  for i, name in ipairs({"north", "east", "south", "west"}) do
    result[name] = {
      filename = prefix .. state .. "-256.png", width = 256, height = 256,
      frame_count = 16, line_length = 8, y = (i-1)*512,
      animation_speed = 8/60, scale = 32*3.9/256,
      shift = {0, -.28/math.sqrt(2) + .25}
    }
  end
  return result
end
local graphics = {
  animation = facings("working"), idle_animation = facings("idle"),
  always_draw_idle_animation = false
}
-- Keep the existing native light, while removing the duplicated legacy body.
local previous = target.graphics_set
if previous and previous.working_visualisations then
  graphics.working_visualisations = {}
  for _, visual in ipairs(previous.working_visualisations) do
    local clean = table.deepcopy(visual)
    for _, key in ipairs({"animation", "north_animation", "east_animation", "south_animation", "west_animation"}) do
      clean[key] = nil
    end
    if next(clean) then table.insert(graphics.working_visualisations, clean) end
  end
end
target.graphics_set = graphics
target.match_animation_speed_to_activity = false
-- Authored mouths replace only the assembler connector pictures. Keep native
-- covers, volumes, connection positions, flows, recipes, burner and collision.
for _, box in ipairs(target.fluid_boxes) do box.pipe_picture = nil end
