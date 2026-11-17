local layout=nil
local names={[0]='north',[4]='east',[8]='south',[12]='west'}
local function unit(state,dir) for _,u in ipairs(layout.units) do if u.state==state and u.direction==(dir or 0) then return u end end;error('WHEEL_GUI missing '..state) end
local function shot(name,u,close)
 local p={x=u.position.x,y=u.position.y};if close then local d=u.direction;if d==0 then p.y=p.y+.5 elseif d==4 then p.x=p.x-.5 elseif d==8 then p.y=p.y-.5 else p.x=p.x+.5 end end
 game.take_screenshot{surface=game.surfaces[1],position=p,resolution=close and {768,640} or {640,640},zoom=close and 6 or 3,path='stone-wheel-v3/'..name..'.png',show_gui=false,show_entity_info=false,anti_alias=true}
end
script.on_nth_tick(30,function(e)
 if not layout then layout=remote.call('stone_wheel_proof','layout');assert(layout.machines==16);if remote.interfaces.freeplay and remote.interfaces.freeplay.set_skip_intro then remote.call('freeplay','set_skip_intro',true) end;game.speed=1 end
 if e.tick==300 then
  for _,d in ipairs({0,4,8,12}) do local u=unit('working',d);shot(names[d]..'-working',u);shot(names[d]..'-pipe-close',u,true) end
  shot('full-output-a',unit('full-output'))
 elseif e.tick==390 then shot('full-output-b',unit('full-output'))
 elseif e.tick==630 then shot('stopped-a',unit('stop-restart'))
 elseif e.tick==660 then shot('landfill',unit('landfill'))
 elseif e.tick==690 then shot('stopped-b',unit('stop-restart'))
 elseif e.tick==900 then shot('restarted',unit('stop-restart'));shot('source-restored',unit('landfill'))
 elseif e.tick==960 then shot('full-output-drained',unit('full-output'))
 elseif e.tick==1020 then game.speed=64
 elseif e.tick==10920 then assert(remote.call('stone_wheel_proof','snapshot')==16);game.auto_save('stone-wheel-complete-client');log('WHEEL_GUI_OPERATED_SAVE_REQUESTED machines=16');game.speed=1 end
end)
local times={};for i=0,31 do times[300+math.floor(i*7.5+.5)]=i end
script.on_event(defines.events.on_tick,function(e) if times[e.tick] then shot(string.format('north-motion-%02d',times[e.tick]),unit('working')) end end)
