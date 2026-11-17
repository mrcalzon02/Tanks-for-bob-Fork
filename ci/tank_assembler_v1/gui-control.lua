local layout=nil
local function unit(state,recipe)
 for _,u in ipairs(layout.units) do if u.state==state and (not recipe or u.recipe==recipe) then return u end end
 error('TANK_GUI missing '..state..'/'..tostring(recipe))
end
local function shot(name,u)
 game.take_screenshot{surface=game.surfaces[1],position={x=u.position.x,y=u.position.y-.6},resolution={640,640},zoom=3,path='tank-assembler-v1/'..name..'.png',show_gui=false,show_entity_info=false,anti_alias=true,force_render=true,daytime=0,hide_clouds=true,hide_fog=true}
end
script.on_nth_tick(30,function(e)
 if not layout then layout=remote.call('tank_assembler_proof','layout');assert(layout.machines==17);if remote.interfaces.freeplay and remote.interfaces.freeplay.set_skip_intro then remote.call('freeplay','set_skip_intro',true) end;game.speed=1 end
 if e.tick==300 then
  shot('working',unit('recipe','super-tank-wmd'));shot('no-power',unit('no-power'));shot('idle',unit('idle'))
 elseif e.tick==480 or e.tick==570 then
  local u=unit('blocked-item');shot(e.tick==480 and 'blocked-item-a' or 'blocked-item-b',u);local m=game.surfaces[1].find_entity('tank-assembling-machine',u.position);log('TANK_GUI_BLOCKED_OBSERVATION '..helpers.table_to_json{tick=e.tick,full_output=m.status==defines.entity_status.full_output,is_crafting=m.is_crafting(),progress=m.crafting_progress,products_finished=m.products_finished})
 elseif e.tick==630 then shot('stopped-a',unit('stop-restart'))
 elseif e.tick==690 then shot('stopped-b',unit('stop-restart'))
 elseif e.tick==1020 then shot('restarted',unit('stop-restart'));shot('power-restored',unit('no-power'));shot('item-output-drained',unit('blocked-item'));game.speed=64
 elseif e.tick==1230 then shot('crafted-building-placed',{position={x=128.5,y=48.5}})
 elseif e.tick==191940 then shot('long-wmd-complete',unit('recipe','super-tank-wmd'));shot('super-tank-complete',unit('recipe','super-tank'));shot('car-upgrade-complete',unit('recipe','car-flamer'))
 elseif e.tick==192000 then assert(remote.call('tank_assembler_proof','snapshot')==17);game.auto_save('tank-assembler-complete-client');log('TANK_GUI_OPERATED_SAVE_REQUESTED machines=17');game.speed=1 end
end)
local times={};for i=0,31 do times[300+math.floor(i*7.5+.5)]=i end
script.on_event(defines.events.on_tick,function(e)
 if times[e.tick] then shot(string.format('north-motion-%02d',times[e.tick]),unit('recipe','super-tank-wmd')) end
end)
