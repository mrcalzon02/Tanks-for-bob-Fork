-- Six actual quarry recipes, placement, fuel, blocked output and stop/restart.
local function check(v,m) if not v then error('QUARRY_V1: '..m) end end
local names={'north','east','south','west'}
local dirs={defines.direction.north,defines.direction.east,defines.direction.south,defines.direction.west}
local recipes={
 {'stone','stone',8},
 {'stone-with-tools','stone',20,{{'stone-tools',20}}},
 {'quarry-iron-ore','iron-ore',10,{{'stone-tools',20},{'brick',100}}},
 {'quarry-copper-ore','copper-ore',10,{{'stone-tools',20},{'brick',100}}},
 {'quarry-iron-orea','iron-ore',20,{{'stone-tools',20},{'stone-brick',100}}},
 {'quarry-copper-oreb','copper-ore',20,{{'stone-tools',20},{'stone-brick',100}}}
}
local loaded=false
script.on_load(function() loaded=true end)
local function count(u) return u.machine.get_output_inventory().get_item_count(u.product) end
script.on_init(function()
 storage.units={};storage.complete=false
 local s=game.surfaces[1];s.always_day=true;s.daytime=0
 game.forces.player.technologies['quarry'].researched=true
 check(game.forces.player.recipes['quarry'].enabled,'building technology did not unlock recipe')
 check(prototypes.item['quarry'].place_result.name=='quarry','placeable item mismatch')
 for row=1,9 do for d=1,4 do s.request_to_generate_chunks({d*24+.5,row*24+.5},1) end end;s.force_generate_chunk_requests()
 for row=1,9 do for d,dir in ipairs(dirs) do
  local spec=recipes[row] or (row==8 and recipes[3] or recipes[1])
  local state=row<=6 and 'recipe' or row==7 and 'unfuelled' or row==8 and 'blocked' or 'idle'
  local p={x=d*24+.5,y=row*24+.5};local area={{p.x-6,p.y-6},{p.x+6,p.y+6}}
  for _,e in pairs(s.find_entities_filtered{area=area}) do e.destroy() end
  local tiles={};for x=-6,6 do for y=-6,6 do tiles[#tiles+1]={name='refined-concrete',position={p.x+x,p.y+y}} end end
  s.set_tiles(tiles,true);s.destroy_decoratives{area=area}
  check(s.can_place_entity{name='quarry',position=p,direction=dir,force='player'},'normal player placement failed')
  local m=s.create_entity{name='quarry',position=p,direction=dir,force='player'}
  local u={machine=m,state=state,recipe=spec[1],product=spec[2],minimum=spec[3],facing=names[d],actual_direction=m.direction}
  if row==1 and d==1 then
   local ok,result=pcall(function() return m.rotate{reverse=false} end)
   storage.rotation_probe={call_supported=ok,result=ok and result or tostring(result),direction_before=dir,direction_after=m.direction}
   m.direction=dir
  end
  if state~='idle' then check(m.set_recipe(spec[1])~=nil,'real recipe selection failed') end
  if state~='unfuelled' then check(m.get_fuel_inventory().insert{name='coal',count=10}>0,'chemical fuel rejected') end
  for _,ing in ipairs(spec[4] or {}) do check(m.get_inventory(defines.inventory.crafter_input).insert{name=ing[1],count=ing[2]}>0,'input rejected '..ing[1]) end
  if state=='blocked' then
   m.get_output_inventory().insert{name='iron-ore',count=100000}
   u.blocked=count(u);check(u.blocked>0,'failed to fill output')
  end
  check(next(m.get_fluid_contents())==nil,'unexpected quarry fluid')
  storage.units[#storage.units+1]=u
 end end
 log('QUARRY_V1_CONTRACT '..helpers.table_to_json{machines=36,recipes=6,rotation_probe=storage.rotation_probe,fluids=0})
end)
script.on_nth_tick(60,function(event)
 if loaded then
  check(#storage.units==36,'saved quarry count changed')
  for i,u in ipairs(storage.units) do
   check(u.machine.valid,'saved quarry invalid')
   if storage.saved_products then check(count(u)==storage.saved_products[i],'saved output inventory changed') end
  end
  log('QUARRY_V1_RELOAD_PASS complete='..tostring(storage.complete)..' stored_products='..tostring(storage.saved_products~=nil));loaded=false
 end
 if event.tick==11040 then
  for _,u in ipairs(storage.units) do
   if u.state=='recipe' then
    check(count(u)>=u.minimum,'real recipe failed '..u.recipe..'/'..u.facing)
    if u.recipe=='stone-with-tools' then check(u.machine.get_output_inventory().get_item_count('stone-tools')>=1,'tool return missing') end
    if u.recipe=='stone' then u.machine.disabled_by_script=true;u.stopped_count=count(u);u.stopped_progress=u.machine.crafting_progress end
   elseif u.state=='unfuelled' then check(count(u)==0 and u.machine.crafting_progress==0,'unfuelled machine worked')
   elseif u.state=='blocked' then
    log('QUARRY_BLOCKED_DIAG '..helpers.table_to_json{count=count(u),before=u.blocked,progress=u.machine.crafting_progress,crafting=u.machine.is_crafting(),status=u.machine.status})
    check(count(u)==u.blocked,'full output produced extra items');u.blocked_progress=u.machine.crafting_progress
   elseif u.state=='idle' then check(count(u)==0 and not u.machine.is_crafting(),'idle machine worked') end
  end
  log('QUARRY_V1_SIX_RECIPES_FUEL_IDLE_BLOCKED_PASS')
 elseif event.tick==11160 then
  for _,u in ipairs(storage.units) do
   if u.state=='recipe' and u.recipe=='stone' then
    check(count(u)==u.stopped_count and math.abs(u.machine.crafting_progress-u.stopped_progress)<.0001,'disabled quarry advanced')
    u.machine.disabled_by_script=false
   elseif u.state=='blocked' then check(count(u)==u.blocked and math.abs(u.machine.crafting_progress-u.blocked_progress)<.0001,'blocked quarry continued processing');u.machine.get_output_inventory().clear() end
  end
  log('QUARRY_V1_STOP_PASS')
 elseif event.tick==23040 then
  for _,u in ipairs(storage.units) do
   if u.state=='recipe' and u.recipe=='stone' then check(count(u)>u.stopped_count,'restart failed') end
   if u.state=='blocked' then check(count(u)>0,'unblocking failed') end
  end
  storage.complete=true
  local receipt={passed=true,machines=36,real_recipes=6,requested_cardinal_tests=4,native_player_orientations=1,placement=true,no_fluid_connections=true,chemical_fuel=true,no_fuel_stopped=true,idle=true,blocked_output=true,stop_restart=true,unblocking=true,rotation_probe=storage.rotation_probe,prototype_overrides=false}
  helpers.write_file('quarry-v1/native-runtime.json',helpers.table_to_json(receipt),false);log('QUARRY_V1_NATIVE_PASS '..helpers.table_to_json(receipt));game.auto_save('quarry-operational')
 end
end)
remote.add_interface('quarry_proof',{snapshot=function()
 storage.saved_products={};for _,u in ipairs(storage.units) do u.machine.disabled_by_script=true;storage.saved_products[#storage.saved_products+1]=count(u) end
 return #storage.saved_products
end})
