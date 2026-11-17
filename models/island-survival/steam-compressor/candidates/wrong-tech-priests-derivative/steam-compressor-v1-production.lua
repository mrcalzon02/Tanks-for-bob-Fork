-- Tanks compressor V1; same recipes, footprint, burner and native fluidboxes.
local target=assert(data.raw['assembling-machine']['Steam-Compressor'])
local prefix='__tanks_for_bob_fork__/graphics/entity/steam-compressor-v1/'
local function facings(state)
  local result={}
  for i,name in ipairs({'north','east','south','west'}) do
    result[name]={filename=prefix..state..'-256.png',width=256,height=256,frame_count=16,line_length=8,y=(i-1)*512,animation_speed=2/60,scale=32*4.8/256,shift={0,-.6/math.sqrt(2)}}
  end
  return result
end
target.graphics_set={animation=facings('working'),idle_animation=facings('idle'),always_draw_idle_animation=false}
target.match_animation_speed_to_activity=false
for _,box in ipairs(target.fluid_boxes) do box.pipe_picture=nil end
