local requested=false
script.on_nth_tick(30,function()
  if game.tick<30 then return end
  if requested then return end
  requested=true
  local surface=game.surfaces[1]
  surface.always_day=true
  surface.daytime=0
  local names={"north","east","south","west"}
  for d,name in ipairs(names) do
    local center={x=d*24+.5,y=24}
    local nearby=surface.find_entities_filtered{name="primitive-steam-powered-pump",position=center,radius=2}
    local pump=nearby[1]
    if not pump then error("PIPE_PUMP_V3_GUI: missing native pump "..name) end
    for _,zoom in ipairs({{label="normal",value=1},{label="close",value=2.5}}) do
      game.take_screenshot{surface=surface,position={x=pump.position.x,y=pump.position.y-.5},
        resolution={x=768,y=512},zoom=zoom.value,path="pipe-pump-v3/"..name.."-"..zoom.label..".png",
        show_gui=false,show_entity_info=false,anti_alias=true,force_render=true,daytime=0,hide_clouds=true,hide_fog=true}
    end
  end
  game.set_wait_for_screenshots_to_finish()
  log("PIPE_PUMP_V3_GUI_QUEUE_COMPLETE count=8")
end)
