-- Tanks compressor V2 barrel source; same recipes, footprint, burner and native fluidboxes.
local target=assert(data.raw['assembling-machine']['Steam-Compressor'])
local prefix='__tanks_for_bob_fork__/graphics/entity/steam-compressor-v2/'
local function facings(state)
  local result={}
  for i,name in ipairs({'north','east','south','west'}) do
    result[name]={filename=prefix..state..'-256.png',width=256,height=256,frame_count=16,line_length=8,y=(i-1)*512,animation_speed=4/60,scale=32*5.6/256,shift={0,-1.1/math.sqrt(2)}}
  end
  return result
end
target.graphics_set={animation=facings('working'),idle_animation=facings('idle'),always_draw_idle_animation=false}
target.match_animation_speed_to_activity=false
for _,box in ipairs(target.fluid_boxes) do box.pipe_picture=nil end

local icon="__tanks_for_bob_fork__/graphics/icons/steam-compressor-v2.png"
for _,kind in ipairs({"item","recipe","technology","assembling-machine"}) do
  local prototype=data.raw[kind] and data.raw[kind]["Steam-Compressor"]
  if prototype then prototype.icon=icon;prototype.icon_size=64;prototype.icons=nil end
end
