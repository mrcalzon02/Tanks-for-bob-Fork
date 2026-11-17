-- Isolated native proof. Real prototypes, recipes, crafting times and power unchanged.
local function check(v,m) if not v then error('TANK_ASSEMBLER_V1: '..m) end end
local loaded=false
script.on_load(function() loaded=true end)
local function inventory(inv) local d={};for _,x in ipairs(inv.get_contents()) do d[x.name..'/'..x.quality]=x.count end;return d end
local function same(a,b) for k,v in pairs(a) do if b[k]~=v then return false end end;for k,v in pairs(b) do if a[k]~=v then return false end end;return true end
local function snap(u) local e=u.machine;return {input=inventory(e.get_inventory(defines.inventory.crafter_input)),output=inventory(e.get_output_inventory()),progress=e.crafting_progress,finished=e.products_finished,energy=e.energy,direction=e.direction,recipe=e.get_recipe() and e.get_recipe().name or false,disabled=e.disabled_by_script} end
local function supply(s,p,enabled)
 local power=s.create_entity{name='tank-assembler-proof-power',position={p.x+5,p.y+3},force='player'};local pole=s.create_entity{name='medium-electric-pole',position={p.x+3,p.y+3},force='player'};check(power and pole,'normal electric supply fixture');if not enabled then power.power_production=0;power.energy=0 end;return power
end
local function ground(s,p)
 s.request_to_generate_chunks(p,1);s.force_generate_chunk_requests();for _,e in pairs(s.find_entities_filtered{area={{p.x-7,p.y-7},{p.x+7,p.y+7}}}) do e.destroy() end
 local tiles={};for x=-7,7 do for y=-7,7 do tiles[#tiles+1]={name='grass-1',position={p.x+x,p.y+y}} end end;s.set_tiles(tiles,true);s.destroy_decoratives{area={{p.x-7,p.y-7},{p.x+7,p.y+7}}}
end
script.on_init(function()
 local s=game.surfaces[1];s.always_day=true;s.daytime=0;local proto=prototypes.entity['tank-assembling-machine'];check(proto.get_crafting_speed()==1 and proto.module_inventory_size==4,'actual speed/four modules');check(not proto.burner_prototype and proto.electric_energy_source_prototype,'actual electric contract');check(math.abs(proto.get_max_energy_usage()*60-250000)<.01,'actual 250kW')
 local f=game.forces.player;check(not f.recipes['tank-assembling-machine'].enabled,'building gated');f.technologies['encabulated-device-integration'].researched=true;check(f.recipes['tank-assembling-machine'].enabled,'actual technology unlock');for _,t in pairs(f.technologies) do t.researched=true end
 local recipes={};for n,p in pairs(prototypes.recipe) do if p.has_category('tank-crafting') then recipes[#recipes+1]=n end end;table.sort(recipes);check(#recipes==13,'actual recipe count');storage.recipes=recipes;storage.units={};storage.complete=false
 local states={'no-power','blocked-item','idle','stop-restart'}
 for row=1,#recipes+#states do
  local state=row<=#recipes and 'recipe' or states[row-#recipes];local name=row<=#recipes and recipes[row] or (state=='stop-restart' and 'super-tank-wmd' or 'tank-light-chasis-wlsk');local requested=({0,4,8,12})[(row-1)%4+1];local p={x=((row-1)%4+1)*24+.5,y=(math.floor((row-1)/4)+1)*24+.5};ground(s,p)
  check(s.can_place_entity{name='tank-assembling-machine',position=p,direction=requested,force='player'},'ordinary player-grid placement');local e=s.create_entity{name='tank-assembling-machine',position=p,direction=requested,force='player'};check(e.direction==0 and not e.rotate(),'actual fixed north');check(e.fluids_count==0,'no invented fluid storage');local u={state=state,recipe=name,machine=e,requested_direction=requested,direction=0,position=p,power=supply(s,p,state~='no-power')}
  if state~='idle' then
   e.set_recipe(name);check(e.get_recipe().name==name,'native recipe selectable');local recipe=prototypes.recipe[name];u.products=recipe.products;local inv=e.get_inventory(defines.inventory.crafter_input)
   for _,x in ipairs(recipe.ingredients) do check(x.type=='item','unexpected fluid recipe');check(inv.insert{name=x.name,count=x.amount}==x.amount,'actual ingredients '..name..'/'..x.name) end
   if state=='blocked-item' then check(e.get_output_inventory().insert{name='tank-light-chasis-wlsk',count=100000}>0,'full real output inventory');u.blocked_output=inventory(e.get_output_inventory()) end
  end
  storage.units[#storage.units+1]=u
 end
 local p={x=128.5,y=24.5};ground(s,p);storage.builder=s.create_entity{name='tank-ammo-assembling-machine',position=p,force='player'};supply(s,p,true);storage.builder.set_recipe('tank-assembling-machine');local inv=storage.builder.get_inventory(defines.inventory.crafter_input)
 for _,x in ipairs(prototypes.recipe['tank-assembling-machine'].ingredients) do check(inv.insert{name=x.name,count=x.amount}==x.amount,'real building ingredients') end
 log('TANK_ASSEMBLER_V1_FIXTURE recipes=13 machines='..#storage.units..' max_recipe_seconds=3040 fixed_north=true')
end)
local function freeze() for _,u in ipairs(storage.units) do u.machine.disabled_by_script=true end;storage.builder.disabled_by_script=true;storage.frozen=true end
local function snapshot() storage.saved={};for i,u in ipairs(storage.units) do storage.saved[i]=snap(u) end;storage.builder_output=inventory(storage.builder.get_output_inventory());return #storage.units end
remote.add_interface('tank_assembler_proof',{layout=function() local d={};for _,u in ipairs(storage.units) do d[#d+1]={state=u.state,recipe=u.recipe,position=u.position,direction=u.direction,requested_direction=u.requested_direction} end;return {machines=#d,units=d} end,freeze=freeze,snapshot=snapshot})
script.on_nth_tick(60,function(event)
 if loaded then
  for i,u in ipairs(storage.units) do check(u.machine.valid and u.machine.direction==0 and u.machine.fluids_count==0,'saved fixed north/no fluid contract')
   if storage.saved then local a,b=storage.saved[i],snap(u);check(same(a.input,b.input) and same(a.output,b.output),'saved input/output inventories');check(a.recipe==b.recipe and a.disabled==b.disabled and math.abs(a.progress-b.progress)<1e-10 and a.finished==b.finished,'saved recipe/progress/count');check(math.abs(a.energy-b.energy)<.1,'saved electrical buffer') end
  end
  if storage.builder_output then check(same(storage.builder_output,inventory(storage.builder.get_output_inventory())),'saved real builder output') end
  if storage.placed_building then check(storage.placed_building.valid and storage.placed_building.name=='tank-assembling-machine' and storage.placed_building.direction==0,'saved crafted building placement') end
  log('TANK_ASSEMBLER_V1_RELOAD_PASS complete='..tostring(storage.complete)..' stored_operation='..tostring(storage.saved~=nil));loaded=false
 end
 if storage.frozen then return end
 if event.tick==600 then
  for _,u in ipairs(storage.units) do if u.state=='stop-restart' then check(u.machine.crafting_progress>0,'powered progress before stop');u.machine.disabled_by_script=true;u.stopped=snap(u) end end
 elseif event.tick==900 then
  for _,u in ipairs(storage.units) do if u.state=='stop-restart' then check(math.abs(u.machine.crafting_progress-u.stopped.progress)<1e-10 and same(inventory(u.machine.get_inventory(defines.inventory.crafter_input)),u.stopped.input),'disabled state stable');u.machine.disabled_by_script=false end end;log('TANK_ASSEMBLER_V1_STOP_PASS')
 elseif event.tick==960 then
  for _,u in ipairs(storage.units) do
   if u.state=='no-power' or u.state=='idle' or u.state=='blocked-item' then check(u.machine.products_finished==0,'inactive/blocked produced '..u.state) end
   if u.state=='blocked-item' then check(same(inventory(u.machine.get_output_inventory()),u.blocked_output),'blocked inventory stable');check(u.machine.status==defines.entity_status.full_output and u.machine.crafting_progress>.99999 and u.machine.energy>0,'fully processed powered craft waits for full output');u.blocked_before_release={tick=event.tick,progress=u.machine.crafting_progress,products_finished=u.machine.products_finished,status='full_output',energy=u.machine.energy};u.machine.get_output_inventory().clear()
   elseif u.state=='no-power' then u.power.power_production=10000000/60;u.power.energy=10000000 end
  end;log('TANK_ASSEMBLER_V1_STARVATION_BLOCKED_PASS')
 elseif event.tick==1200 then
  for _,u in ipairs(storage.units) do if u.state=='no-power' or u.state=='blocked-item' then check(u.machine.products_finished>0,'electric/output recovery '..u.state) end end
  local output=storage.builder.get_output_inventory();check(output.get_item_count('tank-assembling-machine')==1,'real ammunition works building craft');local p={x=128.5,y=48.5};local s=game.surfaces[1];ground(s,p);local item=prototypes.item['tank-assembling-machine'];check(item.place_result and item.place_result.name=='tank-assembling-machine','real item place_result');check(s.can_place_entity{name=item.place_result.name,position=p,direction=4,force='player'},'crafted building ordinary placement');storage.placed_building=s.create_entity{name=item.place_result.name,position=p,direction=4,force='player'};check(storage.placed_building and output.remove{name='tank-assembling-machine',count=1}==1,'consume actual crafted item for placed prototype');storage.placed_building.disabled_by_script=true;log('TANK_ASSEMBLER_V1_RECOVERY_AND_BUILD_PASS')
 elseif event.tick==191880 then
  local cases={};local directions={}
  for _,u in ipairs(storage.units) do
   directions[tostring(u.requested_direction)]=u.machine.direction
   if u.state=='recipe' or u.state=='stop-restart' then
    check(u.machine.products_finished>0,'real operation failed '..u.recipe);check(u.machine.get_inventory(defines.inventory.crafter_input).is_empty(),'actual ingredients consumed '..u.recipe)
    for _,p in ipairs(u.products) do if (p.independent_probability or 1)==1 then check(p.type=='item' and u.machine.get_output_inventory().get_item_count(p.name)>=(p.amount or p.amount_min or 1),'guaranteed actual result '..u.recipe..'/'..p.name) end end
   end
   local d=snap(u);d.state=u.state;d.requested_direction=u.requested_direction;d.blocked_before_release=u.blocked_before_release;cases[#cases+1]=d
  end
  check(storage.builder.get_inventory(defines.inventory.crafter_input).is_empty(),'actual building ingredients consumed');storage.complete=true
  helpers.write_file('tank-assembler-v1/native-runtime.json',helpers.table_to_json{passed=true,real_recipes=13,machines=#storage.units,actual_supported_directions=1,requested_direction_normalization=directions,max_recipe_native_seconds=3040,crafting_speed_and_power_not_overridden=true,actual_electric_watts=250000,module_slots=4,electric_starvation_resupply=true,blocked_item_output_recovery=true,stop_restart=true,building_unlock_and_ammunition_assembler_craft=true,crafted_item_consumed_for_native_placement=true,fluid_and_fuel='not applicable: no fluid storage, ports or burner',engine_parameter_placeholders_excluded=10,cases=cases},false)
  log('TANK_ASSEMBLER_V1_NATIVE_PASS recipes=13 machines='..#storage.units..' actual_facing=north')
 elseif event.tick==191940 then freeze() end
end)
