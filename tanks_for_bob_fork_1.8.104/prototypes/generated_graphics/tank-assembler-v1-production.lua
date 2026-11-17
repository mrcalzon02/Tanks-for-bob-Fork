-- Art only. Actual 3x3 fixed-north, 250kW vehicle upgrade assembler unchanged.
local machine=assert(data.raw['assembling-machine']['tank-assembling-machine'])
local prefix='__tanks_for_bob_fork__/graphics/entity/tank-assembler-v1/'
local function sprite(state)
  return {filename=prefix..state..'-256.png',width=256,height=256,
    frame_count=32,line_length=8,animation_speed=8/60,
    scale=32*6.4/256,shift={0,-1.25/math.sqrt(2)}}
end
machine.graphics_set={animation=sprite('working'),idle_animation=sprite('idle'),
  always_draw_idle_animation=false,animation_progress=1}
machine.match_animation_speed_to_activity=false
local icon='__tanks_for_bob_fork__/graphics/icons/tank-assembler-v1.png'
for _,kind in ipairs({'assembling-machine','item','recipe'}) do
  local p=data.raw[kind] and data.raw[kind]['tank-assembling-machine']
  if p then p.icon=icon;p.icon_size=64;p.icons=nil end
end
