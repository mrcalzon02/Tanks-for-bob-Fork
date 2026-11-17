-- Actual Tanks recipes and player-grid connections; no prototype overrides.
local function check(v,m) if not v then error('TANKS_COMPRESSOR: '..m) end end
local names={'north','east','south','west'}
local dirs={defines.direction.north,defines.direction.east,defines.direction.south,defines.direction.west}
local loaded=false
script.on_load(function() loaded=true end)
local function count(u) return u.machine.get_output_inventory().get_item_count(u.recipe=='Charged-Canister' and 'Charged-Canister' or 'Canister') end
local function fuel(u) u.machine.get_fuel_inventory().insert{name='coal',count=10} end
local function fill(u)
  for _,p in ipairs(u.pipes) do
    if p.flow=='input' then p.entity.set_fluid_segment_fluid(1,{name='steam',amount=p.entity.get_fluid_segment_capacity(1),temperature=165}) end
  end
end
script.on_init(function()
  local s=game.surfaces[1];s.always_day=true;s.daytime=0
  storage.units={};storage.complete=false
  for row=1,7 do for d=1,4 do s.request_to_generate_chunks({d*24+.5,row*24+.5},1) end end
  s.force_generate_chunk_requests()
  check(prototypes.item['Steam-Compressor'].place_result.name=='Steam-Compressor','placeable item binding')
  check(game.forces.player.technologies['Steam-Compressor']~=nil,'unlock technology missing')
  game.forces.player.technologies['Steam-Compressor'].researched=true
  check(game.forces.player.recipes['Charged-Canister'].enabled and game.forces.player.recipes['UnCharge-Canister'].enabled,'real technology did not unlock operations')
  for row,state in ipairs({'charge','release','unfuelled','blocked-item','blocked-fluid','idle'}) do
    for d,direction in ipairs(dirs) do
      local pos={x=d*24+.5,y=row*24+.5}
      for _,e in pairs(s.find_entities_filtered{area={{pos.x-5,pos.y-5},{pos.x+5,pos.y+5}}}) do e.destroy() end
      local tiles={};for x=-5,5 do for y=-5,5 do tiles[#tiles+1]={name='refined-concrete',position={pos.x+x,pos.y+y}} end end
      s.set_tiles(tiles,true);s.destroy_decoratives{area={{pos.x-5,pos.y-5},{pos.x+5,pos.y+5}}}
      check(s.can_place_entity{name='Steam-Compressor',position=pos,direction=direction,force='player'},'player machine placement '..state..names[d])
      local m=s.create_entity{name='Steam-Compressor',position=pos,direction=direction,force='player'}
      local recipe=(state=='release' or state=='blocked-fluid') and 'UnCharge-Canister' or 'Charged-Canister'
      local u={machine=m,state=state,facing=names[d],pipes={},recipe=recipe}
      if state~='idle' then m.set_recipe(recipe) end
      if state~='unfuelled' then fuel(u) end
      if state~='idle' then
        m.get_inventory(defines.inventory.crafter_input).insert{name=recipe=='Charged-Canister' and 'Canister' or 'Charged-Canister',count=20}
        -- Both real recipes enable exactly one fluidbox (input or output).
        for box=1,1 do
          for _,port in ipairs(m.get_fluid_box_pipe_connections(box)) do
            local grid={x=math.floor(port.target_position.x)+.5,y=math.floor(port.target_position.y)+.5}
            check(math.abs(grid.x-port.target_position.x)<.001 and math.abs(grid.y-port.target_position.y)<.001,'off-grid pipe')
            check(s.can_place_entity{name='pipe',position=grid,force='player'},'pipe collision')
            local pipe=s.create_entity{name='pipe',position=grid,force='player'}
            u.pipes[#u.pipes+1]={entity=pipe,flow=port.flow_direction,box=box,target=grid}
          end
        end
        check(#u.pipes>=1,'no usable fluid joint')
        fill(u)
      end
      if state=='blocked-item' then m.get_output_inventory().insert{name='Charged-Canister',count=100000};u.blocked_count=count(u) end
      if state=='blocked-fluid' then
        for _,p in ipairs(u.pipes) do if p.flow=='output' then p.entity.set_fluid_segment_fluid(1,{name='steam',amount=p.entity.get_fluid_segment_capacity(1),temperature=165}) end end
        m.insert_fluid{name='steam',amount=100000,temperature=165}
      end
      storage.units[#storage.units+1]=u
    end
  end
end)
script.on_nth_tick(60,function(event)
  if loaded then
    check(#storage.units==24,'saved units missing')
    for _,u in ipairs(storage.units) do
      check(u.machine.valid,'saved machine invalid')
      for _,p in ipairs(u.pipes) do check(p.entity.valid,'saved pipe invalid');local c=u.machine.get_fluid_box_pipe_connections(p.box);check(#c==1 and c[1].target,'saved joint lost') end
    end
    log('TANKS_COMPRESSOR_RELOAD_PASS complete='..tostring(storage.complete))
    loaded=false
  end
  for _,u in ipairs(storage.units) do if u.state=='charge' or u.state=='blocked-item' then fill(u) end end
  if event.tick==1200 then
    local connections=0
    for _,u in ipairs(storage.units) do
      for _,p in ipairs(u.pipes) do
        local c=u.machine.get_fluid_box_pipe_connections(p.box)
        check(#c==1 and c[1].target,'native pipe disconnected '..u.facing..u.state)
        connections=connections+1
      end
      if u.state=='charge' or u.state=='release' then
        log('TANKS_COMPRESSOR_DIAG '..helpers.table_to_json{state=u.state,facing=u.facing,status=u.machine.status,progress=u.machine.crafting_progress,products=count(u),inputs=u.machine.get_inventory(defines.inventory.crafter_input).get_contents(),fluids=u.machine.get_fluid_contents(),fuel=u.machine.get_fuel_inventory().get_contents()})
        check(count(u)>=1,'real recipe no result '..u.facing..u.state)
        if u.state=='release' then
          local steam=0;for _,p in ipairs(u.pipes) do if p.flow=='output' then local f=p.entity.get_fluid_segment_fluid(1);steam=steam+(f and f.amount or 0) end end
          check(steam>0 and steam+(u.machine.get_fluid_contents()['steam'] or 0)>=349,'release failed steam delivery')
        end
        u.machine.disabled_by_script=true;u.stopped_count=count(u);u.stopped_progress=u.machine.crafting_progress
      elseif u.state=='unfuelled' then check(count(u)==0 and u.machine.crafting_progress==0,'no-fuel worked')
      elseif u.state=='idle' then check(count(u)==0 and not u.machine.is_crafting(),'idle worked')
      elseif u.state=='blocked-item' then check(count(u)==u.blocked_count,'blocked item produced')
      elseif u.state=='blocked-fluid' then check(count(u)==0,'blocked fluid produced') end
    end
    storage.connections=connections
    log('TANKS_COMPRESSOR_RECIPES_FUEL_BLOCKED_PASS connections='..connections)
  elseif event.tick==1260 then
    for _,u in ipairs(storage.units) do if u.state=='charge' or u.state=='release' then
      check(count(u)==u.stopped_count and math.abs(u.machine.crafting_progress-u.stopped_progress)<.0001,'disabled machine advanced')
      u.machine.disabled_by_script=false
    end end
    log('TANKS_COMPRESSOR_STOP_PASS')
  elseif event.tick==2400 then
    for _,u in ipairs(storage.units) do
      if u.state=='charge' or u.state=='release' then check(count(u)>u.stopped_count,'restart failed') end
      if u.state=='blocked-item' then u.machine.get_output_inventory().clear();fill(u) end
      if u.state=='blocked-fluid' then
        for _,p in ipairs(u.pipes) do if p.flow=='output' then p.entity.clear_fluid_segment_fluid(1) end end
        u.machine.remove_fluid(1,100000)
      end
    end
    log('TANKS_COMPRESSOR_RESTART_PASS')
  elseif event.tick==3600 then
    for _,u in ipairs(storage.units) do if u.state=='blocked-item' or u.state=='blocked-fluid' then
      log('UNBLOCK_DIAG '..helpers.table_to_json{state=u.state,status=u.machine.status,progress=u.machine.crafting_progress,count=count(u),fluids=u.machine.get_fluid_contents(),input=u.machine.get_inventory(defines.inventory.crafter_input).get_contents(),output=u.machine.get_output_inventory().get_contents()})
      check(count(u)>0,'unblocking failed '..u.state)
    end end
    storage.complete=true
    local receipt={passed=true,machines=24,facings=4,player_grid_connections=storage.connections,real_recipes={'Charged-Canister','UnCharge-Canister'},fuel=true,idle=true,blocked_item=true,blocked_fluid=true,stop_restart=true,unblocking=true,prototype_overrides=false}
    helpers.write_file('steam-compressor-v1/native-runtime.json',helpers.table_to_json(receipt),false)
    log('TANKS_COMPRESSOR_NATIVE_PASS '..helpers.table_to_json(receipt))
    game.auto_save('steam-compressor-operational')
  end
end)
