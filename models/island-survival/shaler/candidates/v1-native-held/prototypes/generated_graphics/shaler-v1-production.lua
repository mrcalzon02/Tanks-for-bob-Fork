-- Authored Tanks Shaler: retain all current recipes, throughput, burner and fluidboxes.
local target=assert(data.raw['assembling-machine']['shaler'])
local prefix='__tanks_for_bob_fork__/graphics/entity/shaler-v1/'
local function facings(state)
  local result={}
  for i,name in ipairs({'north','east','south','west'}) do
    result[name]={filename=prefix..state..'-256.png',width=256,height=256,
      frame_count=16,line_length=8,y=(i-1)*512,animation_speed=4/60,
      scale=32*5.6/256,shift={0,-1/math.sqrt(2)}}
  end
  return result
end
target.graphics_set={animation=facings('working'),idle_animation=facings('idle'),always_draw_idle_animation=false}
target.match_animation_speed_to_activity=false
for _,box in ipairs(target.fluid_boxes) do box.pipe_picture=nil end
-- Each position is projected from the actual saved flue outlet for its facing.
for _,smoke in ipairs(target.energy_source.smoke or {}) do
  smoke.north_position={-1.0199999809,-2.2131052019}
  smoke.east_position={0.7600000381,-2.4731051447}
  smoke.south_position={1.0199999809,-0.6931051256}
  smoke.west_position={-0.7599998713,-0.4331050159}
  smoke.deviation={0.025,0.025}
end
local icon='__tanks_for_bob_fork__/graphics/icons/shaler-v1.png'
for _,kind in ipairs({'item','recipe','technology','assembling-machine'}) do
  local prototype=data.raw[kind] and data.raw[kind]['shaler']
  if prototype then prototype.icon=icon;prototype.icon_size=64;prototype.icons=nil end
end
