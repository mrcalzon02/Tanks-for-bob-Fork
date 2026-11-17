local layout=nil
local names={[0]='north',[4]='east',[8]='south',[12]='west'}
local delta=.36/math.sqrt(2)-.046875
local smoke={[0]={.98,-.50-2.685/math.sqrt(2)+delta},[4]={.50,.98-2.685/math.sqrt(2)+delta},[8]={-.98,.50-2.685/math.sqrt(2)+delta},[12]={-.50,-.98-2.685/math.sqrt(2)+delta}}
local function unit(state,dir) for _,u in ipairs(layout.units) do if u.state==state and u.direction==(dir or 0) then return u end end;error('CONDENSER_GUI missing '..state) end
local function shot(name,u,close)
 local p={x=u.position.x,y=u.position.y-.4};local zoom=3
 if close=='pipe' then local d=u.direction;local x,y=0,-1;if d==4 then x,y=1,0 elseif d==8 then x,y=0,1 elseif d==12 then x,y=-1,0 end;p.x=u.position.x+1.5*x;p.y=u.position.y+1.5*y;zoom=6
 elseif close=='smoke' then local offset=smoke[u.direction];p.x=u.position.x+offset[1];p.y=u.position.y+offset[2];zoom=5 end
 game.take_screenshot{surface=game.surfaces[1],position=p,resolution=close and {768,640} or {640,640},zoom=zoom,path='steam-condenser-v2/'..name..'.png',show_gui=false,show_entity_info=false,anti_alias=true,force_render=true,daytime=0,hide_clouds=true,hide_fog=true}
end
script.on_nth_tick(30,function(e)
 if not layout then layout=remote.call('steam_condenser_proof','layout');assert(layout.machines==24);if remote.interfaces.freeplay and remote.interfaces.freeplay.set_skip_intro then remote.call('freeplay','set_skip_intro',true) end;game.speed=1 end
 if e.tick==300 then
  for _,dir in ipairs({0,4,8,12}) do local u=unit('recipe',dir);shot(names[dir]..'-working',u);shot(names[dir]..'-steam-pipe-close',u,'pipe');shot(names[dir]..'-smoke-close',u,'smoke') end
  shot('no-fuel',unit('no-fuel'));shot('no-steam',unit('no-steam'));shot('idle',unit('idle'))
 elseif e.tick==630 then shot('stopped-a',unit('stop-restart'))
 elseif e.tick==690 then shot('stopped-b',unit('stop-restart'))
 elseif e.tick==1020 then shot('restarted',unit('stop-restart'));game.speed=64
 elseif e.tick==3600 then game.speed=1
 elseif e.tick==3660 or e.tick==3720 then
  local u=unit('blocked-item');shot(e.tick==3660 and 'blocked-item-a' or 'blocked-item-b',u);local m=game.surfaces[1].find_entity('steam-condenser',u.position);log('CONDENSER_GUI_BLOCKED_OBSERVATION '..helpers.table_to_json{tick=e.tick,full_output=m.status==defines.entity_status.full_output,progress=m.crafting_progress,products_finished=m.products_finished,remaining_fuel=m.burner.remaining_burning_fuel})
 elseif e.tick==4020 then shot('fuel-restored',unit('no-fuel'));shot('steam-restored',unit('no-steam'));shot('item-output-drained',unit('blocked-item'));game.speed=64
 elseif e.tick==8310 then for _,dir in ipairs({0,4,8,12}) do shot(names[dir]..'-completed',unit('recipe',dir)) end;shot('crafted-building-placed',{position={x=96.5,y=36.5}})
 elseif e.tick==8400 then assert(remote.call('steam_condenser_proof','snapshot')==24);game.auto_save('steam-condenser-complete-client');log('CONDENSER_GUI_OPERATED_SAVE_REQUESTED machines=24');game.speed=1 end
end)
local times={};for i=0,31 do times[300+math.floor(i*7.5+.5)]=i end
script.on_event(defines.events.on_tick,function(e) if times[e.tick] then shot(string.format('north-motion-%02d',times[e.tick]),unit('recipe')) end end)
