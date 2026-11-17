local initialized=false
local names={'stone-working-a','tools-working','iron-brick-working','copper-brick-working','iron-stone-brick-working','copper-stone-brick-working','no-fuel','blocked','idle'}
local function shot(name,row)
 game.take_screenshot{surface=game.surfaces[1],position={24.5,row*24+.5},resolution={640,640},zoom=3,path='quarry-v1/'..name..'.png',show_gui=false,show_entity_info=false,anti_alias=true}
end
script.on_nth_tick(60,function(event)
 if not initialized then
  initialized=true
  local surface=game.surfaces[1];surface.always_day=true;surface.daytime=0
  for row=1,9 do for d=1,4 do
   local p={x=d*24+.5,y=row*24+.5};local tiles={}
   for x=-6,6 do for y=-6,6 do tiles[#tiles+1]={name='grass-1',position={p.x+x,p.y+y}} end end
   surface.set_tiles(tiles,true);surface.destroy_decoratives{area={{p.x-6,p.y-6},{p.x+6,p.y+6}}}
  end end
  game.speed=1
 end
 if event.tick%1200==0 then log('QUARRY_GUI_TICK '..event.tick) end
 if event.tick==600 then for row,name in ipairs(names) do shot(name,row) end
 elseif event.tick==660 then shot('stone-working-b',1)
 elseif event.tick==900 then game.speed=64
 elseif event.tick==11040 then shot('blocked-full',8)
 elseif event.tick==23040 then shot('restarted',1)
 elseif event.tick==23100 then
  local count=remote.call('quarry_proof','snapshot');assert(count==36)
  game.speed=1;game.auto_save('quarry-complete-client');log('QUARRY_GUI_OPERATED_SAVE_REQUESTED machines='..count)
 end
end)
