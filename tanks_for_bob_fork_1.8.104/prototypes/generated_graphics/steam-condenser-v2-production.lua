-- Art only. Actual wood+steam -> stone+waste, chemical1kW and ports unchanged.
local target=assert(data.raw['assembling-machine']['steam-condenser'])
local prefix='__tanks_for_bob_fork__/graphics/entity/steam-condenser-v2/'
local registration=.36/math.sqrt(2)-.046875
local function facings(state)
  local result={}
  for i,name in ipairs({'north','east','south','west'}) do
    result[name]={filename=prefix..state..'-256.png',width=256,height=256,
      frame_count=32,line_length=8,y=(i-1)*1024,animation_speed=8/60,
      scale=32*6.2/256,shift={0,-1.1/math.sqrt(2)+registration}}
  end
  return result
end
target.graphics_set={animation=facings('working'),idle_animation=facings('idle'),
  always_draw_idle_animation=false,animation_progress=1}
target.match_animation_speed_to_activity=false
for _,box in ipairs(target.fluid_boxes) do
  box.pipe_picture=nil
  -- The actual recipe exposes no output fluidbox. Suppress its legacy cap art.
  if box.production_type=='output' then box.pipe_covers=nil end
end
-- Projected from the actual founded hollow brick stack mouth in the source.
local elevation=2.685/math.sqrt(2)
for _,smoke in ipairs(target.energy_source.smoke or {}) do
  smoke.north_position={.98,-.50-elevation+registration}
  smoke.east_position={.50,.98-elevation+registration}
  smoke.south_position={-.98,.50-elevation+registration}
  smoke.west_position={-.50,-.98-elevation+registration}
  smoke.deviation={.025,.025}
end
local icon='__tanks_for_bob_fork__/graphics/icons/steam-condenser-v2.png'
for _,kind in ipairs({'assembling-machine','item','recipe','technology'}) do
  local p=data.raw[kind] and data.raw[kind]['steam-condenser']
  if p then p.icon=icon;p.icon_size=64;p.icons=nil end
end
