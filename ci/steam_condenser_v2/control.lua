-- Actual Tanks recipe, ordinary grid pipes and chemical burner. No target overrides.
local function check(v,m) if not v then error('STEAM_CONDENSER_V2: '..m) end end
local loaded=false
script.on_load(function() loaded=true end)
local function inv(v) local d={};for _,x in ipairs(v.get_contents()) do d[x.name..'/'..x.quality]=x.count end;return d end
local function same(a,b) for k,v in pairs(a) do if b[k]~=v then return false end end;for k,v in pairs(b) do if a[k]~=v then return false end end;return true end
local function fluid(e) local f=e.get_fluid(1);return f and {name=f.name,amount=f.amount,temperature=f.temperature} or false end
local function fsame(a,b) if not a then return not b end;return b and a.name==b.name and math.abs(a.amount-b.amount)<.01 and math.abs(a.temperature-b.temperature)<.001 end
local function snap(u)
 local e=u.machine;return {input=inv(e.get_inventory(defines.inventory.crafter_input)),output=inv(e.get_output_inventory()),fuel=inv(e.get_fuel_inventory()),remaining_fuel=e.burner.remaining_burning_fuel,burning=e.burner.currently_burning and e.burner.currently_burning.name or false,energy=e.energy,progress=e.crafting_progress,finished=e.products_finished,direction=e.direction,disabled=e.disabled_by_script,recipe=e.get_recipe() and e.get_recipe().name or false,fluid=e.fluids_count>0 and fluid(e) or false,pipe=u.pipe and fluid(u.pipe) or false,extension=u.extension and fluid(u.extension) or false}
end
local function ground(s,p)
 s.request_to_generate_chunks(p,1);s.force_generate_chunk_requests();for _,e in pairs(s.find_entities_filtered{area={{p.x-5,p.y-5},{p.x+5,p.y+5}}}) do e.destroy() end;local tiles={};for x=-5,5 do for y=-5,5 do tiles[#tiles+1]={name='grass-1',position={p.x+x,p.y+y}} end end;s.set_tiles(tiles,true);s.destroy_decoratives{area={{p.x-5,p.y-5},{p.x+5,p.y+5}}}
end
local function steam(u)
 local capacity=u.pipe.get_fluid_segment_capacity(1);check(math.abs(capacity-200)<.001,'two ordinary pipes have native200 capacity');u.pipe.set_fluid_segment_fluid(1,{name='steam',amount=200,temperature=165})
end
script.on_init(function()
 local p=prototypes.entity['steam-condenser'];check(p.get_crafting_speed()==.6 and p.module_inventory_size==0,'actual speed/modules');check(p.burner_prototype and not p.electric_energy_source_prototype and p.burner_prototype.effectivity==1,'actual chemical burner');check(math.abs(p.get_max_energy_usage()*60-1000)<.01,'actual1kW')
 local f=game.forces.player;check(not f.recipes['steam-condenser'].enabled,'building recipe gated');f.technologies['steam-condenser'].researched=true;check(f.recipes['steam-condenser'].enabled,'real technology unlock');local n=0;for _,q in pairs(prototypes.recipe) do if q.has_category('Steam') then n=n+1;check(q.name=='Steam-condenserA','actual sole recipe') end end;check(n==1,'sole real recipe')
 storage.units={};storage.complete=false;local s=game.surfaces[1];s.always_day=true;s.daytime=0
 for row,state in ipairs({'recipe','no-fuel','no-steam','blocked-item','idle','stop-restart'}) do for i,dir in ipairs({0,4,8,12}) do
  local p={x=i*18+.5,y=row*18+.5};ground(s,p);check(s.can_place_entity{name='steam-condenser',position=p,direction=dir,force='player'},'ordinary player-grid machine placement');local e=s.create_entity{name='steam-condenser',position=p,direction=dir,force='player'};check(e.direction==dir,'supported facing');local u={state=state,direction=dir,position=p,machine=e}
  if state~='idle' then
   e.set_recipe('Steam-condenserA');check(e.fluids_count==1,'running recipe exposes inlet only');local ports=e.get_fluid_box_pipe_connections(1);check(#ports==1 and ports[1].flow_direction=='input','actual steam-only inlet');local pos=ports[1].target_position;check(math.abs(pos.x-(math.floor(pos.x)+.5))<.001 and math.abs(pos.y-(math.floor(pos.y)+.5))<.001,'normal player-grid pipe')
   check(s.can_place_entity{name='pipe',position=pos,force='player'},'legal ordinary inlet pipe');u.pipe=s.create_entity{name='pipe',position=pos,force='player'};check(e.get_fluid_box_pipe_connections(1)[1].target==u.pipe,'native input pipe joint');local dx,dy=(pos.x-p.x)/2,(pos.y-p.y)/2;local extension={x=pos.x+dx,y=pos.y+dy};check(s.can_place_entity{name='pipe',position=extension,force='player'},'legal second ordinary pipe');u.extension=s.create_entity{name='pipe',position=extension,force='player'}
   check(e.get_inventory(defines.inventory.crafter_input).insert{name='wood',count=5}==5,'actual wood5 charge');if state~='no-fuel' then check(e.get_fuel_inventory().insert{name='coal',count=1}==1,'ordinary chemical fuel') end;if state~='no-steam' then steam(u) end
   if state=='blocked-item' then check(e.get_output_inventory().insert{name='stone',count=100000}>0,'full native item output');u.blocked=inv(e.get_output_inventory()) end
  end
  storage.units[#storage.units+1]=u
 end end
 local p={x=96.5,y=18.5};ground(s,p);storage.builder=s.create_entity{name='workbench',position=p,force='player'};storage.builder.set_recipe('steam-condenser');local input=storage.builder.get_inventory(defines.inventory.crafter_input);check(input.insert{name='crude-glass',count=10}==10 and input.insert{name='brick',count=5}==5,'actual building ingredients');storage.builder.get_fuel_inventory().insert{name='coal',count=20}
 log('STEAM_CONDENSER_V2_FIXTURE machines=24 real_recipes=1 directions=4 normal_craft_seconds=58.33333333')
end)
local function freeze() for _,u in ipairs(storage.units) do u.machine.disabled_by_script=true end;storage.builder.disabled_by_script=true;storage.frozen=true end
local function snapshot() storage.saved={};for i,u in ipairs(storage.units) do storage.saved[i]=snap(u) end;storage.builder_saved=snap{machine=storage.builder};return #storage.units end
remote.add_interface('steam_condenser_proof',{layout=function() local d={};for _,u in ipairs(storage.units) do d[#d+1]={state=u.state,direction=u.direction,position=u.position,pipe=u.pipe and u.pipe.position or false} end;return {machines=#d,units=d} end,freeze=freeze,snapshot=snapshot})
script.on_nth_tick(60,function(event)
 if loaded then
  for i,u in ipairs(storage.units) do check(u.machine.valid and u.machine.direction==u.direction,'saved actual entity/facing');if u.pipe then check(u.machine.get_fluid_box_pipe_connections(1)[1].target==u.pipe,'saved ordinary pipe joint') end
   if storage.saved then local a,b=storage.saved[i],snap(u);check(same(a.input,b.input) and same(a.output,b.output) and same(a.fuel,b.fuel),'saved inventories');check(a.burning==b.burning and math.abs(a.remaining_fuel-b.remaining_fuel)<.1 and math.abs(a.energy-b.energy)<.1,'saved actual chemical fuel/buffer');check(a.recipe==b.recipe and a.disabled==b.disabled and a.finished==b.finished and math.abs(a.progress-b.progress)<1e-10,'saved recipe/progress/count');check(fsame(a.fluid,b.fluid) and fsame(a.pipe,b.pipe) and fsame(a.extension,b.extension),'saved actual steam/type/temp') end
  end
  if storage.builder_saved then local a,b=storage.builder_saved,snap{machine=storage.builder};check(same(a.input,b.input) and same(a.output,b.output) and same(a.fuel,b.fuel) and math.abs(a.remaining_fuel-b.remaining_fuel)<.1 and math.abs(a.progress-b.progress)<1e-10 and a.finished==b.finished,'saved actual builder') end
  if storage.placed then check(storage.placed.valid and storage.placed.name=='steam-condenser','saved real crafted building placement') end;log('STEAM_CONDENSER_V2_RELOAD_PASS complete='..tostring(storage.complete)..' stored_operation='..tostring(storage.saved~=nil));loaded=false
 end
 if storage.frozen then return end
 if event.tick==600 then for _,u in ipairs(storage.units) do if u.state=='stop-restart' then check(u.machine.crafting_progress>0,'normal progress before stop');u.machine.disabled_by_script=true;u.stopped=snap(u) end end
 elseif event.tick==900 then for _,u in ipairs(storage.units) do if u.state=='stop-restart' then check(math.abs(u.machine.crafting_progress-u.stopped.progress)<1e-10,'disabled progress holds');u.machine.disabled_by_script=false end end;log('STEAM_CONDENSER_V2_STOP_PASS')
 elseif event.tick==3900 then
  for _,u in ipairs(storage.units) do
   if u.state=='no-fuel' or u.state=='no-steam' or u.state=='blocked-item' or u.state=='idle' then check(u.machine.products_finished==0,'inactive/blocked produced '..u.state) end
   if u.state=='blocked-item' then check(same(inv(u.machine.get_output_inventory()),u.blocked),'full output remains');check(u.machine.status==defines.entity_status.full_output and u.machine.crafting_progress>.99999,'powered complete craft waits for item output');u.blocked_before_release={status='full_output',tick=event.tick,progress=u.machine.crafting_progress,products_finished=u.machine.products_finished,remaining_fuel=u.machine.burner.remaining_burning_fuel};u.machine.get_output_inventory().clear()
   elseif u.state=='no-fuel' then u.machine.get_fuel_inventory().insert{name='coal',count=1}
   elseif u.state=='no-steam' then steam(u) end
  end;log('STEAM_CONDENSER_V2_STARVATION_BLOCKED_PASS')
 elseif event.tick==8100 then
  local cases={};local joints=0
  for _,u in ipairs(storage.units) do
   if u.state~='idle' then check(u.machine.products_finished==1,'actual craft count '..u.state);check(u.machine.get_inventory(defines.inventory.crafter_input).is_empty(),'actual wood consumed');check(u.machine.get_output_inventory().get_item_count('stone')==10 and u.machine.get_output_inventory().get_item_count('tank-ammo-Industrialwaste')==1,'actual stone10/waste1');check(u.machine.get_fluid_count('steam')+u.pipe.get_fluid_count('steam')+u.extension.get_fluid_count('steam')<.01,'actual200 steam consumed');check(u.machine.get_fluid_box_pipe_connections(1)[1].target==u.pipe,'retained ordinary joint');check(u.machine.burner.remaining_burning_fuel>0 and u.machine.burner.remaining_burning_fuel<prototypes.item.coal.fuel_value,'real fuel consumed');joints=joints+1 end
   local d=snap(u);d.state=u.state;d.blocked_before_release=u.blocked_before_release;cases[#cases+1]=d
  end
  local output=storage.builder.get_output_inventory();check(output.get_item_count('steam-condenser')==1 and storage.builder.get_inventory(defines.inventory.crafter_input).is_empty(),'real Workbench building craft');local s=game.surfaces[1];local p={x=96.5,y=36.5};ground(s,p);check(prototypes.item['steam-condenser'].place_result.name=='steam-condenser','actual item binding');check(s.can_place_entity{name='steam-condenser',position=p,direction=4,force='player'},'actual crafted item ordinary placement');storage.placed=s.create_entity{name='steam-condenser',position=p,direction=4,force='player'};check(storage.placed and output.remove{name='steam-condenser',count=1}==1,'consume actual crafted building item');storage.placed.disabled_by_script=true
  storage.complete=true;helpers.write_file('steam-condenser-v2/native-runtime.json',helpers.table_to_json{passed=true,machines=24,real_recipes=1,actual_directions=4,recipe_direction_cases=4,ordinary_machine_pipe_joints=joints,ordinary_pipe_entities=40,steam_amount_per_craft=200,steam_temperature=165,wood_per_craft=5,stone_per_craft=10,waste_per_craft=1,actual_crafting_speed=.6,actual_burner_watts=1000,module_slots=0,gameplay_and_crafting_speed_not_overridden=true,fuel_and_steam_starvation_resupply=true,item_full_output_recovery=true,stop_restart=true,real_workbench_build_unlock_and_scripted_item_placement=true,fluid_output='none in actual recipe',cases=cases},false);log('STEAM_CONDENSER_V2_NATIVE_PASS machines=24 recipes=1 actual_directions=4 pipe_joints='..joints)
 elseif event.tick==8340 then freeze() end
end)
