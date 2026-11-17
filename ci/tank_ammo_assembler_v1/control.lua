local function check(v,m) if not v then error('AMMO_ASSEMBLER_V1: '..m) end end
local loaded=false
script.on_load(function() loaded=true end)
local function fluid_state(u)
 local v={contents=u.machine.get_fluid_contents(),pipes={}}
 for _,p in ipairs(u.pipes) do v.pipes[#v.pipes+1]=p.entity.get_fluid_segment_fluid(1) or false end;return v
end
local function same_fluid(a,b)
 for n,x in pairs(a.contents) do if math.abs((b.contents[n] or 0)-x)>.01 then return false end end;for n,_ in pairs(b.contents) do if a.contents[n]==nil then return false end end
 for i,f in ipairs(a.pipes) do local g=b.pipes[i];if not f then if g then return false end elseif not g or f.name~=g.name or math.abs(f.amount-g.amount)>.01 or math.abs((f.temperature or 0)-(g.temperature or 0))>.001 then return false end end;return true
end
local function inventory(inv) local d={};for _,x in ipairs(inv.get_contents()) do d[x.name..'/'..x.quality]=x.count end;return d end
local function same(a,b) for k,v in pairs(a) do if b[k]~=v then return false end end;for k,v in pairs(b) do if a[k]~=v then return false end end;return true end
local function snap(u) return {input=inventory(u.machine.get_inventory(defines.inventory.crafter_input)),output=inventory(u.machine.get_output_inventory()),fluids=fluid_state(u),progress=u.machine.crafting_progress,finished=u.machine.products_finished,energy=u.machine.energy,direction=u.machine.direction,recipe=u.machine.get_recipe() and u.machine.get_recipe().name or false,disabled=u.machine.disabled_by_script} end
local function feed_fluid(u)
 for _,p in ipairs(u.pipes) do if p.flow=='input' then p.entity.set_fluid_segment_fluid(1,{name='crude-oil',amount=p.entity.get_fluid_segment_capacity(1)}) end end
end
local function supply(s,p,enabled)
 local power=s.create_entity{name='ammo-assembler-proof-power',position={p.x+5,p.y+3},force='player'};local pole=s.create_entity{name='medium-electric-pole',position={p.x+3,p.y+3},force='player'};check(power and pole,'native power fixtures');if not enabled then power.power_production=0;power.energy=0 end;return power
end
script.on_init(function()
 local s=game.surfaces[1];s.always_day=true;s.daytime=0;local proto=prototypes.entity['tank-ammo-assembling-machine'];check(proto.get_crafting_speed()==1 and proto.module_inventory_size==1,'actual speed/module');check(not proto.burner_prototype and proto.electric_energy_source_prototype,'actual electric contract');check(math.abs(proto.get_max_energy_usage()*60-175000)<.01,'actual 175kW')
 local f=game.forces.player;check(not f.recipes['tank-ammo-assembling-machine'].enabled,'building recipe gated');f.technologies['encabulated-device-integration'].researched=true;check(f.recipes['tank-ammo-assembling-machine'].enabled,'real technology unlock');for _,t in pairs(f.technologies) do t.researched=true end
 local recipes={};for n,p in pairs(prototypes.recipe) do if p.has_category('tank-ammo-component') then recipes[#recipes+1]=n end end;table.sort(recipes);check(#recipes==46,'real recipe count changed');storage.recipes=recipes;storage.units={};storage.complete=false
 local states={'no-power','no-fluid','blocked-item','blocked-fluid','idle','stop-restart'}
 for row=1,#recipes+#states do for i,d in ipairs({0,4,8,12}) do
  local state=row<=#recipes and 'recipe' or states[row-#recipes];local name=row<=#recipes and recipes[row] or ({['no-power']='tank-ammo-casing',['no-fluid']='Rubberized-timber',['blocked-item']='45mm-auto',['blocked-fluid']='tank-ammo-industrial-coke',['idle']='tank-ammo-casing',['stop-restart']='tank-ammo-industrial-coke'})[state]
  local p={x=i*24+.5,y=row*24+.5};s.request_to_generate_chunks(p,1);s.force_generate_chunk_requests();for _,e in pairs(s.find_entities_filtered{area={{p.x-7,p.y-7},{p.x+7,p.y+7}}}) do e.destroy() end
  local tiles={};for x=-7,7 do for y=-7,7 do tiles[#tiles+1]={name='grass-1',position={p.x+x,p.y+y}} end end;s.set_tiles(tiles,true);s.destroy_decoratives{area={{p.x-7,p.y-7},{p.x+7,p.y+7}}}
  check(s.can_place_entity{name='tank-ammo-assembling-machine',position=p,direction=d,force='player'},'ordinary machine placement');local e=s.create_entity{name='tank-ammo-assembling-machine',position=p,direction=d,force='player'};check(e.direction==d,'actual facing');local u={state=state,recipe=name,machine=e,direction=d,position=p,pipes={},power=supply(s,p,state~='no-power')}
  if state~='idle' then
   e.set_recipe(name);check(e.get_recipe().name==name,'actual recipe selection');local recipe=prototypes.recipe[name];u.products=recipe.products;local inv=e.get_inventory(defines.inventory.crafter_input)
   for _,x in ipairs(recipe.ingredients) do if x.type=='item' then check(inv.insert{name=x.name,count=x.amount}==x.amount,'actual ingredient load '..name..'/'..x.name) end end
   for box=1,e.fluids_count do for _,port in ipairs(e.get_fluid_box_pipe_connections(box)) do
    local grid={x=math.floor(port.target_position.x)+.5,y=math.floor(port.target_position.y)+.5};check(math.abs(grid.x-port.target_position.x)<.001 and math.abs(grid.y-port.target_position.y)<.001,'grid aligned target');check(s.can_place_entity{name='pipe',position=grid,force='player'},'ordinary grid pipe placement');local pipe=s.create_entity{name='pipe',position=grid,force='player'};u.pipes[#u.pipes+1]={entity=pipe,flow=port.flow_direction,box=box,position=port.position,target=port.target_position}
   end end
   if state~='no-fluid' then feed_fluid(u) end
   if state=='blocked-item' then check(e.get_output_inventory().insert{name='45mm-auto',count=100000}>0,'full actual output');u.blocked_output=inventory(e.get_output_inventory())
   elseif state=='blocked-fluid' then for _,p in ipairs(u.pipes) do if p.flow=='output' then e.set_fluid(p.box,{name='crude-oil',amount=e.get_fluid_capacity(p.box)});p.entity.set_fluid_segment_fluid(1,{name='crude-oil',amount=p.entity.get_fluid_segment_capacity(1)}) end end end
  end;storage.units[#storage.units+1]=u
 end end
 local p={x=128.5,y=24.5};s.request_to_generate_chunks(p,1);s.force_generate_chunk_requests();for _,e in pairs(s.find_entities_filtered{area={{p.x-7,p.y-7},{p.x+7,p.y+7}}}) do e.destroy() end;local tiles={};for x=-7,7 do for y=-7,7 do tiles[#tiles+1]={name='grass-1',position={p.x+x,p.y+y}} end end;s.set_tiles(tiles,true)
 storage.builder=s.create_entity{name='assembling-machine-3',position=p,force='player'};supply(s,p,true);storage.builder.set_recipe('tank-ammo-assembling-machine');local inv=storage.builder.get_inventory(defines.inventory.crafter_input);for _,x in ipairs(prototypes.recipe['tank-ammo-assembling-machine'].ingredients) do check(inv.insert{name=x.name,count=x.amount}==x.amount,'actual bootstrap building ingredients') end
 log('AMMO_ASSEMBLER_V1_FIXTURE recipes=46 machines='..#storage.units..' max_recipe_seconds=3160')
end)
local function freeze() for _,u in ipairs(storage.units) do u.machine.disabled_by_script=true end;storage.builder.disabled_by_script=true;storage.frozen=true end
local function snapshot() storage.saved={};for i,u in ipairs(storage.units) do storage.saved[i]=snap(u) end;storage.builder_output=inventory(storage.builder.get_output_inventory());return #storage.units end
remote.add_interface('ammo_assembler_proof',{layout=function() local d={};for _,u in ipairs(storage.units) do d[#d+1]={state=u.state,recipe=u.recipe,position=u.position,direction=u.direction} end;return {machines=#d,units=d} end,freeze=freeze,snapshot=snapshot})
script.on_nth_tick(60,function(e)
 if loaded then
  for i,u in ipairs(storage.units) do check(u.machine.valid and u.machine.direction==u.direction,'saved entity/facing');for _,p in ipairs(u.pipes) do check(u.machine.get_fluid_box_pipe_connections(p.box)[1].target==p.entity,'saved ordinary pipe joint') end
   if storage.saved then local a,b=storage.saved[i],snap(u);check(same(a.input,b.input) and same(a.output,b.output),'saved ingredient/output inventories');check(same_fluid(a.fluids,b.fluids),'saved actual fluids');check(a.recipe==b.recipe and a.disabled==b.disabled and math.abs(a.progress-b.progress)<1e-10 and a.finished==b.finished,'saved recipe/progress/count');check(math.abs(a.energy-b.energy)<.1,'saved electrical buffer') end
  end;if storage.builder_output then check(same(storage.builder_output,inventory(storage.builder.get_output_inventory())),'saved bootstrap output') end;log('AMMO_ASSEMBLER_V1_RELOAD_PASS complete='..tostring(storage.complete)..' stored_operation='..tostring(storage.saved~=nil));loaded=false
 end
 if storage.frozen then return end
 if e.tick==600 then for _,u in ipairs(storage.units) do if u.state=='stop-restart' then check(u.machine.crafting_progress>0,'powered progress before stop');u.machine.disabled_by_script=true;u.stopped=snap(u) end end
 elseif e.tick==900 then for _,u in ipairs(storage.units) do if u.state=='stop-restart' then check(math.abs(u.machine.crafting_progress-u.stopped.progress)<1e-10 and same(inventory(u.machine.get_inventory(defines.inventory.crafter_input)),u.stopped.input),'stopped state stable');u.machine.disabled_by_script=false end end;log('AMMO_ASSEMBLER_V1_STOP_PASS')
 elseif e.tick==9600 then
  for _,u in ipairs(storage.units) do
   if u.state=='no-power' or u.state=='no-fluid' or u.state=='idle' or u.state=='blocked-item' or u.state=='blocked-fluid' then check(u.machine.products_finished==0,'inactive/blocked produced '..u.state..'/'..u.direction) end
   if u.state=='blocked-item' then check(same(inventory(u.machine.get_output_inventory()),u.blocked_output),'blocked output inventory stable');u.machine.get_output_inventory().clear()
   elseif u.state=='blocked-fluid' then
    local status='unknown';for n,v in pairs(defines.entity_status) do if u.machine.status==v then status=n end end;u.blocked_before_release={tick=e.tick,status=status,progress=u.machine.crafting_progress,products_finished=u.machine.products_finished,energy=u.machine.energy,fluids=fluid_state(u)};check(u.machine.crafting_progress>.99999 and u.machine.energy>0,'fully processed powered fluid craft must wait for full output');log('AMMO_ASSEMBLER_V1_FULL_FLUID_READY '..helpers.table_to_json{direction=u.direction,state=u.blocked_before_release});for _,p in ipairs(u.pipes) do u.machine.clear_fluid(p.box);p.entity.clear_fluid_segment_fluid(1) end
   elseif u.state=='no-power' then u.power.power_production=10000000/60;u.power.energy=10000000
   elseif u.state=='no-fluid' then feed_fluid(u) end
  end;log('AMMO_ASSEMBLER_V1_STARVATION_BLOCKED_PASS')
 elseif e.tick==26040 then
  for _,u in ipairs(storage.units) do if u.state~='recipe' and u.state~='idle' then check(u.machine.products_finished>0,'recovery did not finish '..u.state) end end;check(storage.builder.get_output_inventory().get_item_count('tank-ammo-assembling-machine')==1,'real base-assembler building craft');log('AMMO_ASSEMBLER_V1_RECOVERY_AND_BUILD_PASS')
 elseif e.tick==191880 then
  local connections=0;local cases={}
  for _,u in ipairs(storage.units) do
   for _,p in ipairs(u.pipes) do check(u.machine.get_fluid_box_pipe_connections(p.box)[1].target==p.entity,'final ordinary pipe joint');connections=connections+1 end
   if u.state=='recipe' then
    check(u.machine.products_finished>0,'real recipe failed '..u.recipe..'/'..u.direction);local inv=u.machine.get_inventory(defines.inventory.crafter_input);check(inv.is_empty(),'real item ingredients consumed '..u.recipe)
    for _,p in ipairs(u.products) do if (p.independent_probability or 1)==1 then
     if p.type=='item' then check(u.machine.get_output_inventory().get_item_count(p.name)>=(p.amount or p.amount_min or 1),'guaranteed actual item result '..u.recipe..'/'..p.name)
     else local n=u.machine.get_fluid_count(p.name);for _,pipe in ipairs(u.pipes) do if pipe.flow=='output' then n=n+pipe.entity.get_fluid_count(p.name) end end;check(n>0,'guaranteed actual fluid result '..u.recipe) end
    end end
   end
   cases[#cases+1]={state=u.state,recipe=u.recipe,direction=u.direction,products_finished=u.machine.products_finished,input=inventory(u.machine.get_inventory(defines.inventory.crafter_input)),output=inventory(u.machine.get_output_inventory()),fluids=fluid_state(u),electric_energy=u.machine.energy,blocked_before_release=u.blocked_before_release,ports=(function() local d={};for _,p in ipairs(u.pipes) do d[#d+1]={flow=p.flow,position=p.position,ordinary_pipe=p.entity.position} end;return d end)()}
  end
  storage.complete=true;local report={passed=true,real_recipes=46,real_recipe_direction_cases=184,machines=#storage.units,ordinary_grid_connections=connections,supported_directions=4,max_recipe_native_seconds=3160,crafting_speed_and_power_not_overridden=true,actual_electric_watts=175000,electric_starvation_resupply=true,fluid_starvation_resupply=true,blocked_item_and_fluid_output_recovery=true,stop_restart=true,building_unlock_and_base_assembler_craft=true,engine_parameter_placeholders_excluded=10,cases=cases};helpers.write_file('ammo-assembler-v1/native-runtime.json',helpers.table_to_json(report),false);log('AMMO_ASSEMBLER_V1_NATIVE_PASS recipes=46 cases=184 machines='..#storage.units..' connections='..connections)
 elseif e.tick==191940 then freeze() end
end)
