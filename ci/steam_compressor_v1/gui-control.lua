-- Capture actual production art at differing working poses and idle.
local function capture(label,row)
  local surface=game.surfaces[1]
  for d,name in ipairs({'north','east','south','west'}) do
    local p={x=d*24+.5,y=row*24+.5}
    game.take_screenshot{surface=surface,position={x=p.x,y=p.y-.35},resolution={x=640,y=480},zoom=3,path='steam-compressor-v1/'..name..'-'..label..'.png',show_gui=false,show_entity_info=false,anti_alias=true,force_render=true,daytime=0,hide_clouds=true,hide_fog=true}
  end
  game.set_wait_for_screenshots_to_finish()
end
script.on_nth_tick(30,function(event)
  if event.tick==30 then game.speed=8 end
  if event.tick==600 then capture('working',1);capture('idle',6) end
  if event.tick==720 then capture('later',1) end
  if event.tick==3630 then game.auto_save('steam-compressor-complete-client') end
end)
