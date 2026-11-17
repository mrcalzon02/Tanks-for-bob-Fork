local function check(v,m) if not v then error('STONE_WHEEL_V3: '..m) end end
local function turn(x,y,d) if d==0 then return x,y elseif d==4 then return -y,x elseif d==8 then return -x,-y else return y,-x end end
local function total(u) return (u.pump.get_fluid_contents().water or 0)+(u.pipe.get_fluid_contents().water or 0) end
local function clear(u) u.pump.clear_fluid(1);u.pipe.clear_fluid_segment_fluid(1) end
local function snap(u) return {amount=total(u),direction=u.pump.direction,position=u.pump.position,source_tile=u.pump.surface.get_tile(u.source).name,source_fluid=u.pump.get_fluid_source_fluid(),disabled=u.pump.disabled_by_script} end
local loaded=false
script.on_load(function() loaded=true end)
script.on_init(function()
 local s=game.surfaces[1];s.always_day=true;s.daytime=0
 local proto=prototypes.entity['stone-water-wheel'];check(proto.get_pumping_speed()==.5,'actual pumping speed');check(not proto.burner_prototype and not proto.electric_energy_source_prototype,'no player fuel or power')
 local f=game.forces.player;check(not f.recipes['stone-water-wheel'].enabled,'building initially gated');f.technologies['wood-basin'].researched=true;f.technologies.brick.researched=true;f.technologies['stone-water-wheel'].researched=true;check(f.recipes['stone-water-wheel'].enabled,'real unlock')
 storage.units={};storage.complete=false
 for j,state in ipairs({'working','full-output','stop-restart','landfill'}) do for i,d in ipairs({0,4,8,12}) do
  local p={x=8.5+(i-1)*20,y=8.5+(j-1)*20};s.request_to_generate_chunks(p,1);s.force_generate_chunk_requests()
  for _,e in pairs(s.find_entities_filtered{area={{p.x-6,p.y-6},{p.x+6,p.y+6}}}) do e.destroy() end
  local tiles={};for x=-5,5 do for y=-5,5 do local a,b=turn(x,y,d);tiles[#tiles+1]={name=y<0 and 'water' or 'grass-1',position={p.x+a,p.y+b}} end end;s.set_tiles(tiles,true);s.destroy_decoratives{area={{p.x-6,p.y-6},{p.x+6,p.y+6}}}
  check(s.can_place_entity{name='stone-water-wheel',position=p,direction=d,force='player'},'legal shore placement')
  local e=s.create_entity{name='stone-water-wheel',position=p,direction=d,force='player'};check(e.direction==d,'actual facing')
  local ports=e.get_fluid_box_pipe_connections(1);check(#ports==1 and ports[1].flow_direction=='output','one real output')
  local q=ports[1];local grid={x=math.floor(q.target_position.x)+.5,y=math.floor(q.target_position.y)+.5};check(s.can_place_entity{name='pipe',position=grid,force='player'},'ordinary grid pipe placement');local pipe=s.create_entity{name='pipe',position=grid,force='player'}
  local sx,sy=turn(0,-1,d);local u={state=state,pump=e,pipe=pipe,source={x=p.x+sx,y=p.y+sy},position=p,direction=d,removed=0};storage.units[#storage.units+1]=u
  if state=='full-output' then e.set_fluid(1,{name='water',amount=e.get_fluid_capacity(1)});pipe.set_fluid_segment_fluid(1,{name='water',amount=pipe.get_fluid_segment_capacity(1)});u.full=total(u) end
 end end
 local p={88.5,8.5};s.request_to_generate_chunks(p,1);s.force_generate_chunk_requests();for _,e in pairs(s.find_entities_filtered{area={{85,5},{92,12}}}) do e.destroy() end;local tiles={};for x=85,92 do for y=5,12 do tiles[#tiles+1]={name='grass-1',position={x,y}} end end;s.set_tiles(tiles,true)
 storage.builder=s.create_entity{name='workbench',position=p,force='player'};check(storage.builder.set_recipe('stone-water-wheel')~=nil,'real building category');local inv=storage.builder.get_inventory(defines.inventory.crafter_input);inv.insert{name='wood',count=5};inv.insert{name='brick',count=10};storage.builder.get_fuel_inventory().insert{name='coal',count=20}
 log('STONE_WHEEL_V3_FIXTURE machines=16 connections=16')
end)
local function freeze() for _,u in ipairs(storage.units) do u.pump.disabled_by_script=true end;storage.builder.disabled_by_script=true;storage.frozen=true end
local function snapshot() storage.saved={};for i,u in ipairs(storage.units) do storage.saved[i]=snap(u) end;storage.builder_output=storage.builder.get_output_inventory().get_item_count('stone-water-wheel');return #storage.units end
remote.add_interface('stone_wheel_proof',{layout=function() local units={};for _,u in ipairs(storage.units) do units[#units+1]={state=u.state,position=u.position,direction=u.direction} end;return {machines=#units,units=units} end,freeze=freeze,snapshot=snapshot})
script.on_nth_tick(60,function(e)
 if loaded then
  for i,u in ipairs(storage.units) do check(u.pump.valid and u.pipe.valid,'saved entities');check(u.pump.get_fluid_box_pipe_connections(1)[1].target==u.pipe,'saved actual connection');if storage.saved then local x,y=snap(u),storage.saved[i];check(math.abs(x.amount-y.amount)<.01 and x.direction==y.direction and x.disabled==y.disabled and x.source_tile==y.source_tile,'saved network/state/facing/source') end end
  if storage.builder_output then check(storage.builder.get_output_inventory().get_item_count('stone-water-wheel')==storage.builder_output,'saved construction output') end
  log('STONE_WHEEL_V3_RELOAD_PASS complete='..tostring(storage.complete)..' stored_networks='..tostring(storage.saved~=nil));loaded=false
 end
 if storage.frozen then return end
 for _,u in ipairs(storage.units) do
  check(u.pump.valid and u.pipe.valid,'valid native structures');check(u.pump.get_fluid_box_pipe_connections(1)[1].target==u.pipe,'native ordinary grid connection')
  if e.tick==120 and u.state~='full-output' then check(math.abs(total(u)-60)<.01,'actual 30/s source rate') end
  if e.tick==600 then
   if u.state=='full-output' then check(math.abs(total(u)-u.full)<.01,'full output stable');u.blocked_status=u.pump.status
   elseif u.state=='stop-restart' then check(total(u)>10,'working before stop');u.pump.disabled_by_script=true;clear(u)
   elseif u.state=='landfill' then clear(u);u.pump.surface.set_tiles({{name='landfill',position=u.source}},true,false,false);u.landfill_before=total(u)
   end
  elseif e.tick==720 then
   if u.state=='stop-restart' then check(total(u)<.001,'stopped output');u.pump.disabled_by_script=false
   elseif u.state=='landfill' then u.landfill_amount=total(u);u.landfill_status=u.pump.status;u.landfill_source_fluid=u.pump.get_fluid_source_fluid();u.landfill_visible_tile=u.pump.surface.get_tile(u.source).name;u.landfill_hidden_tile=u.pump.surface.get_hidden_tile(u.source);u.pump.surface.set_tiles({{name='water',position=u.source}},true,false,false);clear(u)
   end
  elseif e.tick==840 then
   if u.state=='stop-restart' or u.state=='landfill' then check(total(u)>10,'restart/source restoration') end
   if u.state=='full-output' then clear(u) end
  elseif e.tick==960 and u.state=='full-output' then check(total(u)>10,'drained full output recovers') end
  if u.state=='working' and e.tick>120 then u.removed=u.removed+u.pipe.extract_fluid{name='water',amount=60} end
 end
 if e.tick==10800 then
  check(storage.builder.get_output_inventory().get_item_count('stone-water-wheel')==1,'actual workbench craft');local inv=storage.builder.get_inventory(defines.inventory.crafter_input);check(inv.get_item_count('wood')==0 and inv.get_item_count('brick')==0,'real ingredients consumed')
  local units={};for _,u in ipairs(storage.units) do local q=u.pump.get_fluid_box_pipe_connections(1)[1];units[#units+1]={state=u.state,direction=u.direction,position=u.position,port_position=q.position,reported_target=q.target_position,ordinary_pipe=u.pipe.position,network_amount=total(u),water_consumed_by_test_demand=u.removed,blocked_status=u.blocked_status,landfill_amount_after_120_ticks=u.landfill_amount,landfill_status=u.landfill_status,landfill_visible_tile=u.landfill_visible_tile,landfill_hidden_tile=u.landfill_hidden_tile,landfill_source_fluid=u.landfill_source_fluid} end
  storage.complete=true;local report={passed=true,machines=16,ordinary_grid_connections=16,supported_directions=4,extraction_rate_water_per_second=30,void_energy_no_player_fuel_or_electricity=true,normal_shore_placement=true,full_output_and_drain_recovery=true,stop_restart=true,source_landfill_and_restoration_observed=true,construction_unlock_and_actual_workbench_craft=true,processing_recipes='none: native shoreline intake',units=units};helpers.write_file('stone-wheel-v3/native-runtime.json',helpers.table_to_json(report),false);log('STONE_WHEEL_V3_NATIVE_PASS '..helpers.table_to_json(report))
 elseif e.tick==10860 then freeze();snapshot() end
end)
