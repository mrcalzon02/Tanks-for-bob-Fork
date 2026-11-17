-- Native visual fixtures seed levels; real pump fill/drain is separately tested headlessly.
local function units() return game.surfaces[1].find_entities_filtered{name='wood-basin'} end
local function level(ratio)
 for _,tank in pairs(units()) do
  local row=math.floor(tank.position.y/32);local name=row==1 and 'water' or row==2 and 'crude-oil' or 'steam'
  if ratio==0 then tank.clear_fluid_segment_fluid(1) else tank.set_fluid_segment_fluid(1,{name=name,amount=tank.get_fluid_segment_capacity(1)*ratio,temperature=name=='steam' and 165 or 25}) end
 end
end
local function capture(label,row)
 local s=game.surfaces[1]
 for d,name in ipairs({'north','east','south','west'}) do
  local p={x=d*32+.5,y=row*32+.5}
  game.take_screenshot{surface=s,position={x=p.x,y=p.y-.35},resolution={x=768,y=640},zoom=3,path='wood-basin-v1/'..name..'-'..label..'.png',show_gui=false,show_entity_info=false,anti_alias=true,force_render=true,daytime=0,hide_clouds=true,hide_fog=true}
 end
 game.set_wait_for_screenshots_to_finish();log('WOOD_BASIN_CAPTURE '..label..' tick='..game.tick)
end
script.on_nth_tick(1,function(event)
 if event.tick==1 then game.speed=1;for _,p in pairs(game.surfaces[1].find_entities_filtered{name='pump'}) do p.disabled_by_script=true end;level(0)
 elseif event.tick==30 then capture('empty',1)
 elseif event.tick==60 then level(.5)
 elseif event.tick==90 then capture('filling',1)
 elseif event.tick==120 then level(1)
 elseif event.tick==150 then capture('full',1)
 elseif event.tick==180 then capture('full-later',1)
 elseif event.tick==210 then capture('oil',2);capture('steam',3)
 elseif event.tick==240 then level(0)
 elseif event.tick==270 then capture('drained',1)
 elseif event.tick==300 then level(.75)
 elseif event.tick==330 then capture('refill',1)
 elseif event.tick==360 then
  local n=remote.call('wood_basin_proof','snapshot');if n~=12 then error('snapshot incomplete') end
  game.auto_save('wood-basin-complete-client')
 end
end)
