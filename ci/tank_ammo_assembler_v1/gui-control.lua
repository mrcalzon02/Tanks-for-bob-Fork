local layout=nil
local names={[0]='north',[4]='east',[8]='south',[12]='west'}
local function unit(state,recipe,dir) for _,u in ipairs(layout.units) do if u.state==state and (not recipe or u.recipe==recipe) and u.direction==(dir or 0) then return u end end;error('AMMO_GUI missing '..state..'/'..tostring(recipe)) end
local function shot(name,u,flow)
 local p={x=u.position.x,y=u.position.y}
 if flow then local d=u.direction;local x,y=0,-1;if d==4 then x,y=1,0 elseif d==8 then x,y=0,1 elseif d==12 then x,y=-1,0 end;if flow=='output' then x,y=-x,-y end;p.x=p.x+1.5*x;p.y=p.y+1.5*y end
 game.take_screenshot{surface=game.surfaces[1],position=p,resolution=flow and {768,640} or {640,640},zoom=flow and 6 or 3,path='ammo-assembler-v1/'..name..'.png',show_gui=false,show_entity_info=false,anti_alias=true,force_render=true,daytime=0,hide_clouds=true,hide_fog=true}
end
script.on_nth_tick(30,function(e)
 if not layout then layout=remote.call('ammo_assembler_proof','layout');assert(layout.machines==208);if remote.interfaces.freeplay and remote.interfaces.freeplay.set_skip_intro then remote.call('freeplay','set_skip_intro',true) end;game.speed=1 end
 if e.tick==300 then
  for _,d in ipairs({0,4,8,12}) do
   shot(names[d]..'-working',unit('recipe','tank-ammo-industrial-coke',d));shot(names[d]..'-input-pipe-close',unit('recipe','Rubberized-timber',d),'input');shot(names[d]..'-output-pipe-close',unit('recipe','tank-ammo-industrial-coke',d),'output')
  end
  shot('no-power',unit('no-power'));shot('no-fluid',unit('no-fluid'));shot('idle',unit('idle'))
 elseif e.tick==480 or e.tick==570 then
  local u=unit('blocked-item');shot(e.tick==480 and 'blocked-item-a' or 'blocked-item-b',u);local m=game.surfaces[1].find_entity('tank-ammo-assembling-machine',u.position);local name='unknown';for n,v in pairs(defines.entity_status) do if m.status==v then name=n end end;log('AMMO_GUI_BLOCKED_OBSERVATION '..helpers.table_to_json{tick=e.tick,status=name,is_crafting=m.is_crafting(),progress=m.crafting_progress,products_finished=m.products_finished})
 elseif e.tick==630 then shot('stopped-a',unit('stop-restart'))
 elseif e.tick==690 then shot('stopped-b',unit('stop-restart'))
 elseif e.tick==1020 then shot('restarted',unit('stop-restart'));game.speed=64
 elseif e.tick==9540 then game.speed=1;shot('blocked-fluid',unit('blocked-fluid'))
 elseif e.tick==9720 then game.speed=64
 elseif e.tick==10020 then shot('coke-output-complete',unit('recipe','tank-ammo-industrial-coke'))
 elseif e.tick==191940 then shot('long-wmd-complete',unit('recipe','tank-wmd-ammo'));shot('long-artillery-complete',unit('recipe','wmdartillery-ammo'))
 elseif e.tick==192000 then assert(remote.call('ammo_assembler_proof','snapshot')==208);game.auto_save('ammo-assembler-complete-client');log('AMMO_GUI_OPERATED_SAVE_REQUESTED machines=208');game.speed=1 end
end)
local times={};for i=0,31 do times[300+math.floor(i*7.5+.5)]=i end
script.on_event(defines.events.on_tick,function(e)
 if times[e.tick] then shot(string.format('north-motion-%02d',times[e.tick]),unit('recipe','tank-ammo-industrial-coke')) end
 if e.tick==9615 then shot('power-restored',unit('no-power'));shot('fluid-restored',unit('no-fluid'));shot('item-output-drained',unit('blocked-item'));shot('fluid-output-drained',unit('blocked-fluid')) end
end)
