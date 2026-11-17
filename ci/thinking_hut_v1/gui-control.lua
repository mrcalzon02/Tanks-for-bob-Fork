local layout=nil
local function find(state,technology)
 for _,u in ipairs(layout.units) do if u.state==state and (not technology or u.technology==technology) then return u end end
 error('HUT_GUI missing '..state..' '..tostring(technology))
end
local function shot(name,u,close)
 local p=u.position
 game.take_screenshot{surface=game.surfaces[1],position=close and {p.x-.98,p.y+1.32-1.4/math.sqrt(2)} or p,resolution=close and {512,512} or {640,640},zoom=close and 8 or 2.5,path='thinking-hut-v1/'..name..'.png',show_gui=false,show_entity_info=false,anti_alias=true}
end
script.on_nth_tick(60,function(e)
 if not layout then
  layout=remote.call('thinking_hut_proof','layout');assert(layout.machines==24)
  if remote.interfaces.freeplay and remote.interfaces.freeplay.set_skip_intro then remote.call('freeplay','set_skip_intro',true) end
  game.speed=1
 end
 local working=find('real-research','beachpump')
 if e.tick==120 then shot('smoke-origin',working)
 elseif e.tick==600 then
  shot('working-a',working);shot('lantern-working-close',working,true)
  for _,state in ipairs({'no-fuel','missing-meal','idle'}) do shot(state,find(state)) end
  shot('document-research',find('real-research','work-order-generation'))
  shot('risk-assessment-research',find('real-research','brine-conditioning'))
  shot('board-docket-research',find('real-research','board-advisory-risk-assessment'))
 elseif e.tick==660 then shot('working-b',working)
 elseif e.tick==900 then local s=game.surfaces[1];s.always_day=false;s.freeze_daytime=true;s.daytime=.45
 elseif e.tick==960 then shot('night-working',working);shot('night-idle',find('idle'));shot('night-lantern-close',working,true)
 elseif e.tick==1020 then local s=game.surfaces[1];s.daytime=0;s.always_day=true;game.speed=64
 elseif e.tick==9000 then shot('completed-research-idle',find('completed-idle'))
 elseif e.tick==10800 then shot('restarted',find('stop-restart'));shot('refuelled',find('no-fuel'));shot('resupplied',find('missing-meal'))
 elseif e.tick==10860 then remote.call('thinking_hut_proof','freeze')
 elseif e.tick==10920 then assert(remote.call('thinking_hut_proof','snapshot')==24);game.auto_save('thinking-hut-complete-client');log('HUT_GUI_OPERATED_SAVE_REQUESTED labs=24');game.speed=1
 end
end)
script.on_event(defines.events.on_tick,function(e)
 if e.tick>=600 and e.tick<840 and (e.tick-600)%15==0 then
  shot(string.format('north-motion-%02d',(e.tick-600)/15),find('real-research','beachpump'))
 end
end)
