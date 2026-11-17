-- Calcifier wet mineral bed: preserve actual recipes, burner, directions and both fixed socket positions.
local target=assert(data.raw['assembling-machine']['calcifier'])
local prefix='__tanks_for_bob_fork__/graphics/entity/calcifier-v2/'
local function facings(state)
  local result={}
  for i,name in ipairs({'north','east','south','west'}) do
    result[name]={filename=prefix..state..'-256.png',width=256,height=256,
      frame_count=16,line_length=8,y=(i-1)*512,animation_speed=4/60,
      scale=32*5.6/256,shift={0,-1.08/math.sqrt(2)+.2076834412}}
  end
  return result
end
target.graphics_set={animation=facings('working'),idle_animation=facings('idle'),always_draw_idle_animation=false}
target.match_animation_speed_to_activity=false
for _,box in ipairs(target.fluid_boxes) do box.pipe_picture=nil end
-- Each position is projected from the actual saved flue outlet for its facing.
for _,smoke in ipairs(target.energy_source.smoke or {}) do
  smoke.north_position={0.9899999619,-2.4845730726}
  smoke.east_position={1.0500000000,-0.4445729438}
  smoke.south_position={-0.9899999619,-0.3845729057}
  smoke.west_position={-1.0500000000,-2.4245730344}
  smoke.deviation={0.025,0.025}
end
local icon='__tanks_for_bob_fork__/graphics/icons/calcifier-v2.png'
for _,kind in ipairs({'item','recipe','technology','assembling-machine'}) do
  local prototype=data.raw[kind] and data.raw[kind]['calcifier']
  if prototype then prototype.icon=icon;prototype.icon_size=64;prototype.icons=nil end
end
