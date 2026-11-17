local done=false
script.on_nth_tick(30,function(ev)
  if done or ev.tick<30 then return end;done=true
  local sf=game.surfaces[1];sf.always_day=true;sf.daytime=0
  for d,name in ipairs({'north','east','south','west'}) do
    local m=sf.find_entities_filtered{name='steam-condenser',position={d*24+.5,24.5},radius=2}[1]
    if not m then error('TANKS_CONDENSER_V1_GUI missing '..name) end
    game.take_screenshot{surface=sf,position={m.position.x,m.position.y-.6},resolution={768,512},zoom=2,
      path='steam-condenser-v1/'..name..'-close.png',show_gui=false,show_entity_info=false,
      anti_alias=true,force_render=true,daytime=0,hide_clouds=true,hide_fog=true}
  end
  game.set_wait_for_screenshots_to_finish();log('TANKS_CONDENSER_V1_GUI_COMPLETE count=4')
end)
