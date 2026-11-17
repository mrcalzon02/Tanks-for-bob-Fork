-- Authored low-tech quarry: same fixed orientation, recipes, burner and footprint.
local target=assert(data.raw['assembling-machine']['quarry'])
local prefix='__tanks_for_bob_fork__/graphics/entity/quarry-v5/'
local function fixed(state)
  return {north={filename=prefix..state..'-256.png',width=256,height=256,
    frame_count=16,line_length=8,animation_speed=4/60,
    scale=32*5.6/256,shift={0,-0.63/math.sqrt(2)}}}
end
target.graphics_set={animation=fixed('working'),idle_animation=fixed('idle'),always_draw_idle_animation=false}
target.match_animation_speed_to_activity=false

-- Projected from the saved firebox flue outlet, including the sprite ground correction.
-- Native quarry orientation is fixed north; retain smoke rate and chemical emissions.
for _,smoke in ipairs(target.energy_source.smoke or {}) do
  smoke.position={1.2300001144,-0.6705888997}
  smoke.north_position=nil;smoke.east_position=nil
  smoke.south_position=nil;smoke.west_position=nil
  smoke.deviation={0.02,0.02}
end
