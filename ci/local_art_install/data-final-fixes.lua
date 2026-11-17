-- Last-loaded proof addon: assert the completed sprites survive the full pack.
local function check(v,m) if not v then error('LOCAL_ART_INSTALL: '..m) end end
local function frame(node,needle)
  if type(node)~='table' then return nil end
  if node.filename and node.filename:find(needle,1,true) then return node end
  for _,child in pairs(node) do local found=frame(child,needle);if found then return found end end
end
local fire=assert(data.raw['assembling-machine']['cooking-fire'])
local pond=assert(data.raw['assembling-machine']['fish-pond'])
local solar=assert(data.raw.boiler['solar-boiler'])
local pump=assert(data.raw.pump['primitive-steam-powered-pump'])
for _,d in ipairs({'north','east','south','west'}) do
  local tests={
    {fire.graphics_set.animation[d],'cooking-fire-v2-production-working.png'},
    {fire.graphics_set.idle_animation[d],'cooking-fire-v2-production-idle.png'},
    {solar.pictures[d],'solar-boiler-v8-aligned/working-256.png'},
    {pond.graphics_set.animation[d],'fish-pond-v2/working-256.png'},
    {pond.graphics_set.idle_animation[d],'fish-pond-v2/idle-256.png'},
    {pump.animations[d],'primitive-pipe-pump-v3/working-256.png'}}
  for _,test in ipairs(tests) do
    local image=frame(test[1],test[2])
    check(image and image.frame_count==16 and image.width==256,'missing active sprite '..test[2]..'/'..d)
  end
end
for _,name in ipairs({'cooking-fire','solar-boiler','fish-pond','primitive-steam-powered-pump'}) do
  check(data.raw.item[name] and data.raw.item[name].place_result==name,'missing placeable item '..name)
end
for _,port in ipairs(pump.fluid_box.pipe_connections) do
  check(port.position[1]==0 and math.abs(port.position[2])==.5,'pump port is off the normal player grid')
end
log('LOCAL_ART_INSTALL_BINDINGS_PASS four_assets=4 facings=4 working_frames=16 native_version='..mods.tanks_for_bob_fork)
