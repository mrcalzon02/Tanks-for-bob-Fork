local layout=nil
local facings={'north','east','south','west'}
local function row(name) for i,v in ipairs(layout.recipes) do if v==name then return i end end;error('CALCIFIER_GUI: missing '..name) end
local function shot(name,r,d)
 game.take_screenshot{surface=game.surfaces[1],position={d*24+.5,r*24+.5},resolution={640,640},zoom=2.5,path='calcifier-v2/'..name..'.png',show_gui=false,show_entity_info=false,anti_alias=true}
end
script.on_nth_tick(60,function(e)
 if not layout then
  layout=remote.call('calcifier_proof','layout');assert(layout.machines==48)
  if remote.interfaces.freeplay and remote.interfaces.freeplay.set_skip_intro then remote.call('freeplay','set_skip_intro',true);log('CALCIFIER_GUI_SKIP_INTRO '..tostring(remote.call('freeplay','get_skip_intro'))) end
  game.speed=1
 end
 if e.tick==600 then
  for d,name in ipairs(facings) do shot(name..'-working-a',row('Calcifier-pro'),d) end
  for d,name in ipairs(facings) do local delta=({{0,-1},{1,0},{0,1},{-1,0}})[d];game.take_screenshot{surface=game.surfaces[1],position={d*24+.5+delta[1]*1.5,row('Calcifier-pro')*24+.5+delta[2]*1.5},resolution={640,640},zoom=8,path='calcifier-v2/'..name..'-inlet-joint.png',show_gui=false,show_entity_info=false,anti_alias=true} end
  for _,pair in ipairs({{'steam-scaling','Calcifier-pro-5'},{'crystal-growth','hydrocoptic-crystal'},{'ionic-treatment','ionic-scum'},{'sediment-growth','microcrystal-sediment'}}) do shot(pair[1],row(pair[2]),1) end
  for offset,name in ipairs({'no-fuel','blocked-item','idle','no-fluid'}) do shot(name,#layout.recipes+offset,1) end
 elseif e.tick==660 then for d,name in ipairs(facings) do shot(name..'-working-b',row('Calcifier-pro'),d) end
 elseif e.tick==900 then game.speed=64
 elseif e.tick==7200 then shot('blocked-item-full',#layout.recipes+2,1)
 elseif e.tick==14400 then shot('restarted',row('Calcifier-pro'),1)
 elseif e.tick==14460 then
  remote.call('calcifier_proof','freeze');game.speed=64
 elseif e.tick>14460 and not storage.saved and remote.call('calcifier_proof','settled') then
  assert(remote.call('calcifier_proof','snapshot')==48);storage.saved=true;game.speed=1;game.auto_save('calcifier-complete-client');log('CALCIFIER_GUI_OPERATED_SAVE_REQUESTED machines=48 settled_tick='..e.tick)
 end
end)

-- Sixteen actual client frames across one four-second working loop.
script.on_event(defines.events.on_tick,function(e)
 if e.tick>=600 and e.tick<840 and (e.tick-600)%15==0 then
  game.take_screenshot{surface=game.surfaces[1],position={24.5,24.5},resolution={640,640},zoom=3,path=string.format('calcifier-v2/north-motion-%02d.png',(e.tick-600)/15),show_gui=false,show_entity_info=false,anti_alias=true}
 end
end)
