local function check(v,m) if not v then error('CALCIFIER_V2: '..m) end end
local dirs={defines.direction.north,defines.direction.east,defines.direction.south,defines.direction.west}
local loaded=false
script.on_load(function() loaded=true end)
local function products(u)
 local n=0;for _,p in ipairs(u.products) do if p.type=='item' then n=n+u.machine.get_output_inventory().get_item_count(p.name) end end;return n
end
local function feed(u)
 for _,p in ipairs(u.pipes) do if p.flow=='input' then p.entity.set_fluid_segment_fluid(1,{name=u.fluid,amount=p.entity.get_fluid_segment_capacity(1),temperature=u.fluid=='steam' and 165 or 15}) end end
end
local function fluid_state(u)
 local v={contents=u.machine.get_fluid_contents(),pipes={}}
 for _,p in ipairs(u.pipes) do v.pipes[#v.pipes+1]=p.entity.get_fluid_segment_fluid(1) or false end
 return v
end
local function fluid_equal(a,b)
 for name,amount in pairs(a.contents) do if math.abs((b.contents[name] or 0)-amount)>.01 then return false end end
 for name,_ in pairs(b.contents) do if a.contents[name]==nil then return false end end
 for i,f in ipairs(a.pipes) do
  local g=b.pipes[i]
  if not f then if g then return false end
  elseif not g or f.name~=g.name or math.abs(f.amount-g.amount)>.01 or math.abs((f.temperature or 0)-(g.temperature or 0))>.001 then return false end
 end
 return true
end
script.on_init(function()
 if remote.interfaces.freeplay and remote.interfaces.freeplay.set_skip_intro then remote.call("freeplay","set_skip_intro",true) end
 local s=game.surfaces[1];s.always_day=true;s.daytime=0;storage.units={};storage.complete=false
 check(prototypes.item.calcifier.place_result.name=='calcifier','item binding')
 game.forces.player.technologies.calcifier.researched=true;check(game.forces.player.recipes.calcifier.enabled,'technology unlock')
 for _,t in pairs(game.forces.player.technologies) do t.researched=true end
 local recipes={};for name,p in pairs(prototypes.recipe) do if p.has_category('Calcifier') then recipes[#recipes+1]=name end end;table.sort(recipes)
 storage.recipes=recipes;local contracts={}
 for _,name in ipairs(recipes) do local p=prototypes.recipe[name];contracts[#contracts+1]={name=name,energy=p.energy,ingredients=p.ingredients,products=p.products} end
 helpers.write_file('calcifier-v2/runtime-contract.json',helpers.table_to_json{recipes=contracts},false)
 for row=1,#recipes+4 do for d=1,4 do s.request_to_generate_chunks({d*24+.5,row*24+.5},1) end end;s.force_generate_chunk_requests()
 for row=1,#recipes+4 do for d,dir in ipairs(dirs) do
  local state=row<=#recipes and 'recipe' or ({'unfuelled','blocked-item','idle','no-fluid'})[row-#recipes]
  local name=row<=#recipes and recipes[row] or 'Calcifier-pro';local recipe=prototypes.recipe[name]
  for _,product in ipairs(recipe.products) do check(product.type=='item','Calcifier contract changed: fluid result requires output testing') end
  local p={x=d*24+.5,y=row*24+.5};local area={{p.x-6,p.y-6},{p.x+6,p.y+6}}
  for _,e in pairs(s.find_entities_filtered{area=area}) do e.destroy() end
  local tiles={};for x=-6,6 do for y=-6,6 do tiles[#tiles+1]={name='grass-1',position={p.x+x,p.y+y}} end end;s.set_tiles(tiles,true);s.destroy_decoratives{area=area}
  check(s.can_place_entity{name='calcifier',position=p,direction=dir,force='player'},'placement')
  local m=s.create_entity{name='calcifier',position=p,direction=dir,force='player'}
  if row==1 and d==1 then local before=m.direction;local result=m.rotate{reverse=false};storage.rotation={before=before,after=m.direction,result=result};m.direction=dir end
  local u={machine=m,state=state,recipe=name,products=recipe.products,pipes={},actual_direction=m.direction}
  if state~='idle' then
   check(m.set_recipe(name)~=nil,'select recipe '..name)
   for _,i in ipairs(recipe.ingredients) do
    if i.type=='item' then check(m.get_inventory(defines.inventory.crafter_input).insert{name=i.name,count=i.amount*(name=='Calcifier-pro' and 20 or 3)}>0,'insert '..i.name) else u.fluid=i.name end
   end
   local expected=0;for _,i in ipairs(recipe.ingredients) do if i.type=='fluid' then expected=expected+1 end end;for _,i in ipairs(recipe.products) do if i.type=='fluid' then expected=expected+1 end end
   for box=1,expected do for _,port in ipairs(m.get_fluid_box_pipe_connections(box)) do
    local grid={x=math.floor(port.target_position.x)+.5,y=math.floor(port.target_position.y)+.5}
    check(math.abs(grid.x-port.target_position.x)<.001 and math.abs(grid.y-port.target_position.y)<.001,'off-grid socket')
    check(s.can_place_entity{name='pipe',position=grid,force='player'},'pipe collision')
    local pipe=s.create_entity{name='pipe',position=grid,force='player'};u.pipes[#u.pipes+1]={entity=pipe,flow=port.flow_direction,box=box,target=grid}
   end end
   check(#u.pipes==expected,'fluid connection count '..name)
  end
  if state~='unfuelled' then m.get_fuel_inventory().insert{name='coal',count=20} end
  if state~='no-fluid' then feed(u) end
  if state=='blocked-item' then m.get_output_inventory().insert{name='stone',count=100000};u.blocked=products(u) end
  storage.units[#storage.units+1]=u
 end end
 log('CALCIFIER_CONTRACT '..helpers.table_to_json{recipes=recipes,machines=#storage.units,rotation=storage.rotation})
end)
script.on_nth_tick(60,function(e)
 if loaded then
  for i,u in ipairs(storage.units) do check(u.machine.valid,'saved machine');for _,p in ipairs(u.pipes) do local ports=u.machine.get_fluid_box_pipe_connections(p.box);check(#ports==1 and ports[1].target,'saved pipe lost') end;if storage.saved_products then check(products(u)==storage.saved_products[i],'saved products changed') end end
  if storage.saved_fluids then for i,u in ipairs(storage.units) do check(fluid_equal(storage.saved_fluids[i],fluid_state(u)),'saved machine/pipe fluid amount, type or temperature changed unit='..i) end end
  log('CALCIFIER_V2_RELOAD_PASS complete='..tostring(storage.complete)..' stored_products='..tostring(storage.saved_products~=nil));loaded=false
 end
 if not storage.frozen then for _,u in ipairs(storage.units) do if u.state~='no-fluid' then feed(u) end end end
 if e.tick==7200 then
  local connections=0
  for _,u in ipairs(storage.units) do
   for _,p in ipairs(u.pipes) do local ports=u.machine.get_fluid_box_pipe_connections(p.box);check(#ports==1 and ports[1].target,'pipe detached');connections=connections+1 end
   if u.state=='recipe' then
    log('CALCIFIER_RECIPE_DIAG '..helpers.table_to_json{recipe=u.recipe,direction=u.actual_direction,output=u.machine.get_output_inventory().get_contents(),fluids=u.machine.get_fluid_contents(),status=u.machine.status,progress=u.machine.crafting_progress})
    for _,p in ipairs(u.products) do if (p.independent_probability or 1)==1 then
     if p.type=='item' then check(u.machine.get_output_inventory().get_item_count(p.name)>=(p.amount or p.amount_min or 1),'missing real result '..u.recipe..'/'..p.name)
     else local amount=u.machine.get_fluid_contents()[p.name] or 0;for _,pipe in ipairs(u.pipes) do if pipe.flow=='output' then local f=pipe.entity.get_fluid_segment_fluid(1);amount=amount+(f and f.name==p.name and f.amount or 0) end end;check(amount>0,'fluid output missing '..u.recipe) end
    end end
    if u.recipe=='Calcifier-pro' then u.machine.disabled_by_script=true;u.stopped=products(u);u.progress=u.machine.crafting_progress end
   elseif u.state=='unfuelled' or u.state=='idle' or u.state=='no-fluid' then check(products(u)==0 and u.machine.crafting_progress==0,'inactive worked '..u.state)
   elseif u.state=='blocked-item' then check(products(u)==u.blocked,'full item output produced');u.progress=u.machine.crafting_progress
   end
  end
  storage.connections=connections;log('CALCIFIER_V2_ALL_RECIPES_FUEL_IDLE_BLOCKED_PASS')
 elseif e.tick==7320 then
  for _,u in ipairs(storage.units) do
   if u.stopped then check(products(u)==u.stopped and math.abs(u.machine.crafting_progress-u.progress)<.0001,'disabled advanced');u.machine.disabled_by_script=false end
   if u.state=='blocked-item' then check(products(u)==u.blocked and math.abs(u.machine.crafting_progress-u.progress)<.0001,'blocked advanced');u.machine.get_output_inventory().clear() end
  end;log('CALCIFIER_V2_STOP_PASS')
 elseif e.tick==14400 then
  for _,u in ipairs(storage.units) do if u.stopped then check(products(u)>u.stopped,'restart failed') end;if u.state=='blocked-item' then check(products(u)>0,'unblocking failed '..u.state) end end
  storage.complete=true;local receipt={passed=true,machines=#storage.units,real_recipes=storage.recipes,player_grid_connections=storage.connections,rotation=storage.rotation,fuel=true,no_fuel=true,no_fluid=true,idle=true,blocked_item=true,fluid_output_blocking='not applicable: all actual products are items',stop_restart=true,prototype_overrides=false}
  helpers.write_file('calcifier-v2/native-runtime.json',helpers.table_to_json(receipt),false);log('CALCIFIER_V2_NATIVE_PASS '..helpers.table_to_json(receipt));game.auto_save('calcifier-operational')
 end
end)
remote.add_interface('calcifier_proof',{
 layout=function() return {recipes=storage.recipes,machines=#storage.units} end,
 freeze=function() check(storage.complete,'freeze before operations');storage.frozen=true;for _,u in ipairs(storage.units) do u.machine.disabled_by_script=true end end,
 settled=function()
  check(storage.frozen,'settle before freeze');local now={};local stable=storage.previous_fluids~=nil
  for i,u in ipairs(storage.units) do now[i]=fluid_state(u);if stable and not fluid_equal(storage.previous_fluids[i],now[i]) then stable=false end end
  storage.previous_fluids=now;storage.stable_checks=stable and (storage.stable_checks or 0)+1 or 0
  return storage.stable_checks>=2
 end,
 snapshot=function()
  check(storage.frozen and storage.stable_checks>=2,'snapshot before fluid settling');storage.saved_products={};storage.saved_fluids={}
  for _,u in ipairs(storage.units) do storage.saved_products[#storage.saved_products+1]=products(u);storage.saved_fluids[#storage.saved_fluids+1]=fluid_state(u) end
  return #storage.saved_products
 end
})
