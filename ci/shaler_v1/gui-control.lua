local layout=nil
local facings={'north','east','south','west'}
local function row(name) for i,v in ipairs(layout.recipes) do if v==name then return i end end;error('SHALER_GUI: missing '..name) end
local function shot(name,r,d)
 game.take_screenshot{surface=game.surfaces[1],position={d*24+.5,r*24+.5},resolution={640,640},zoom=2.5,path='shaler-v1/'..name..'.png',show_gui=false,show_entity_info=false,anti_alias=true}
end
script.on_nth_tick(60,function(e)
 if not layout then layout=remote.call('shaler_proof','layout');assert(layout.machines==88);game.speed=1 end
 if e.tick==600 then
  for d,name in ipairs(facings) do shot(name..'-working-a',row('Steam-Charge'),d) end
  for _,pair in ipairs({{'water-washing','corporate-waste-reprocessing'},{'acid-working','radio-refine-2'},{'canister-packing','shalera'},{'canister-unpacking','shalerb'}}) do shot(pair[1],row(pair[2]),1) end
  for offset,name in ipairs({'no-fuel','blocked-item','blocked-fluid','idle','no-steam'}) do shot(name,#layout.recipes+offset,1) end
 elseif e.tick==660 then for d,name in ipairs(facings) do shot(name..'-working-b',row('Steam-Charge'),d) end
 elseif e.tick==900 then game.speed=64
 elseif e.tick==7200 then shot('blocked-item-full',#layout.recipes+2,1);shot('blocked-fluid-full',#layout.recipes+3,1)
 elseif e.tick==14400 then shot('restarted',row('Steam-Charge'),1)
 elseif e.tick==14460 then
  remote.call('shaler_proof','freeze');game.speed=64
 elseif e.tick>14460 and not storage.saved and remote.call('shaler_proof','settled') then
  assert(remote.call('shaler_proof','snapshot')==88);storage.saved=true;game.speed=1;game.auto_save('shaler-complete-client');log('SHALER_GUI_OPERATED_SAVE_REQUESTED machines=88 settled_tick='..e.tick)
 end
end)

-- Sixteen actual client frames across one four-second working loop.
script.on_event(defines.events.on_tick,function(e)
 if e.tick>=600 and e.tick<840 and (e.tick-600)%15==0 then
  game.take_screenshot{surface=game.surfaces[1],position={24.5,24.5},resolution={640,640},zoom=3,path=string.format('shaler-v1/north-motion-%02d.png',(e.tick-600)/15),show_gui=false,show_entity_info=false,anti_alias=true}
 end
end)
