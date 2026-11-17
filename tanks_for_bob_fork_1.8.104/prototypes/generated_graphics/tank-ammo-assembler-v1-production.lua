-- Art only: retain all 46 component recipes, electric 175kW, one module and ports.
local target=assert(data.raw['assembling-machine']['tank-ammo-assembling-machine'])
local prefix='__tanks_for_bob_fork__/graphics/entity/tank-ammo-assembler-v1/'
local function facing(state)
 local d={};local working=state=='working'
 for i,name in ipairs({'north','east','south','west'}) do
  d[name]={filename=prefix..state..'-256.png',width=256,height=256,
   frame_count=32,line_length=8,
   y=(i-1)*1024,animation_speed=8/60,
   scale=32*5.8/256,shift={0,-1/math.sqrt(2)+.36/math.sqrt(2)-.046875}}
 end;return d
end
target.graphics_set={animation=facing('working'),idle_animation=facing('idle'),always_draw_idle_animation=false}
target.match_animation_speed_to_activity=false
for _,box in ipairs(target.fluid_boxes) do box.pipe_picture=nil end
local icon='__tanks_for_bob_fork__/graphics/icons/tank-ammo-assembler-v1.png'
for _,kind in ipairs({'assembling-machine','item','recipe'}) do
 local p=data.raw[kind] and data.raw[kind]['tank-ammo-assembling-machine']
 if p then p.icon=icon;p.icon_size=64;p.icons=nil end
end
