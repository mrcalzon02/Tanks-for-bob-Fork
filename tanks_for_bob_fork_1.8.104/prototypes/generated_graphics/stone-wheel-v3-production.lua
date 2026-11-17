-- Native shoreline extraction unchanged: 0.5 water/tick, void energy, real socket.
local pump=assert(data.raw['offshore-pump']['stone-water-wheel'])
assert(pump.pumping_speed==.5 and pump.fluid_box.pipe_connections[1].position[2]==.25)
local prefix='__tanks_for_bob_fork__/graphics/entity/stone-water-wheel-v3/'
local shift={0,-.62/math.sqrt(2)+(.36/math.sqrt(2)-.046875)}
local function layer(facing,part,submerged)
 local s={filename=prefix..facing..'-working-'..part..'-256.png',width=256,height=256,
  frame_count=32,line_length=8,animation_speed=8/60,scale=32*3.3/256,shift=shift}
 if submerged then s.tint={r=.55,g=.74,b=.76,a=.62} end
 return s
end
local animation={}
for _,facing in ipairs({'north','east','south','west'}) do
 -- Both layers animate together. A frozen underwater Sprite4Way would detach
 -- moving buckets and paddles. The lower layer blends over native water.
 animation[facing]={layers={layer(facing,'underwater',true),layer(facing,'above-water',false)}}
end
pump.graphics_set={animation=animation,base_render_layer='ground-patch',underwater_layer_offset=15}
pump.water_reflection=nil
local icon='__tanks_for_bob_fork__/graphics/icons/stone-water-wheel-v3.png'
for _,kind in ipairs({'offshore-pump','item','recipe','technology'}) do
 local p=data.raw[kind] and data.raw[kind]['stone-water-wheel']
 if p then p.icon=icon;p.icon_size=64;p.icon_mipmaps=nil;p.icons=nil end
end
