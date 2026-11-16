-- Disposable native state/production/port/reload proof; never installed.
local function ensure(value, message) if not value then error("FISH_POND_V2: "..message) end end
local loaded = false
script.on_load(function() loaded = true end)
local names = {"north", "east", "south", "west"}
local directions = {defines.direction.north,defines.direction.east,defines.direction.south,defines.direction.west}
local function count(u)
  local inventory=u.entity.get_output_inventory()
  return inventory and inventory.get_item_count("raw-fish") or 0
end
local function record(u)
  return {facing=u.facing,state=u.state,position=u.entity.position,fish=count(u),
    crafting_progress=u.entity.crafting_progress,status=u.entity.status}
end
script.on_init(function()
  storage.units = {}
  local surface = game.surfaces[1]
  for row=1,5 do for d=1,4 do surface.request_to_generate_chunks({d*24+.5,row*24+.5},1) end end
  surface.force_generate_chunk_requests()
  for row,state in ipairs({"catch", "unfuelled", "harvest", "blocked", "fluid-contract"}) do
    for d,direction in ipairs(directions) do
      local center={x=d*24+.5,y=row*24+.5}
      local tiles={}
      for x=-5,5 do for y=-5,5 do tiles[#tiles+1]={name="refined-concrete",position={center.x+x,center.y+y}} end end
      surface.set_tiles(tiles,true)
      for _,e in pairs(surface.find_entities_filtered{area={{center.x-5,center.y-5},{center.x+5,center.y+5}},type={"tree","simple-entity","resource"}}) do e.destroy() end
      local entity=surface.create_entity{name="fish-pond",position=center,direction=direction,force="player"}
      ensure(entity and entity.valid,"missing pond "..names[d])
      local u={entity=entity,state=state,facing=names[d]}
      entity.set_recipe(state=="harvest" and "harvest-fish" or state=="fluid-contract" and "fish-pond-v2-fluid-proof" or "catch-fish")
      if state~="unfuelled" then ensure(entity.get_fuel_inventory().insert{name="coal",count=5}==5,"fuel rejected") end
      if state=="catch" or state=="unfuelled" or state=="blocked" then
        ensure(entity.get_inventory(defines.inventory.crafter_input).insert{name="wood",count=50}==50,"wood rejected")
      end
      if state=="blocked" then
        local output=entity.get_output_inventory()
        output.insert{name="raw-fish",count=100000}
        u.blocked_count=count(u)
      elseif state=="fluid-contract" then
        u.pipes={}
        for box=1,2 do
          for _,port in ipairs(entity.get_fluid_box_pipe_connections(box)) do
            local pipe=surface.create_entity{name="pipe",position=port.target_position,force="player"}
            ensure(pipe and pipe.valid,"adjacent pipe creation")
            u.pipes[#u.pipes+1]={entity=pipe,flow=port.flow_direction}
            if port.flow_direction=="input" then pipe.set_fluid_segment_fluid(1,{name="water",amount=pipe.get_fluid_segment_capacity(1)}) end
          end
        end
        ensure(#u.pipes==2,"expected two enabled test-recipe fluid joints")
      end
      storage.units[#storage.units+1]=u
    end
  end
end)
script.on_nth_tick(60,function(event)
  if loaded then
    ensure(#storage.units==20,"saved fixture lost entities")
    for _,u in ipairs(storage.units) do ensure(u.entity.valid,"saved pond invalid") end
    log("FISH_POND_V2_RELOAD_PASS ponds=20")
    loaded=false
  end
  if event.tick==600 then
    for _,u in ipairs(storage.units) do
      if u.state=="catch" then
        ensure(count(u)>=8,"catch-fish produced no fish "..u.facing)
        u.entity.disabled_by_script=true
        u.stopped_count=count(u)
        u.stopped_progress=u.entity.crafting_progress
      elseif u.state=="unfuelled" then ensure(count(u)==0,"unfuelled pond produced fish")
      elseif u.state=="blocked" then ensure(count(u)==u.blocked_count,"blocked output changed")
      elseif u.state=="fluid-contract" then
        for box=1,2 do
          local ports=u.entity.get_fluid_box_pipe_connections(box)
          ensure(#ports==1 and ports[1].target,"fluid joint disconnected "..u.facing)
        end
        for _,p in ipairs(u.pipes) do if p.flow=="output" then
          local fluid=p.entity.get_fluid_segment_fluid(1)
          ensure(fluid and fluid.amount>0,"test-recipe output did not reach native pipe")
        end end
      end
    end
    log("FISH_POND_V2_INITIAL_PASS catch=4 unfuelled=4 blocked=4 fluid_contract=4")
  elseif event.tick==900 then
    for _,u in ipairs(storage.units) do if u.state=="catch" then
      ensure(count(u)==u.stopped_count and math.abs(u.entity.crafting_progress-u.stopped_progress)<1e-6,"disabled pond kept working")
      u.entity.disabled_by_script=false
    end end
    log("FISH_POND_V2_STOP_PASS ponds=4")
  elseif event.tick==1500 then
    for _,u in ipairs(storage.units) do if u.state=="catch" then ensure(count(u)>u.stopped_count,"restart failed") end end
    log("FISH_POND_V2_RESTART_PASS ponds=4")
  elseif event.tick==6000 then
    local receipt={passed=true,ponds=20,facings=4,production=true,unfuelled_stopped=true,
      stop_restart=true,blocked_output=true,harvest_fish=true,test_only_fluid_contract=true,
      production_recipes_use_fluids=false,units={}}
    for _,u in ipairs(storage.units) do
      if u.state=="harvest" then ensure(count(u)>=2,"55-second harvest-fish failed "..u.facing) end
      receipt.units[#receipt.units+1]=record(u)
    end
    helpers.write_file("fish-pond-v2/native-runtime.json",helpers.table_to_json(receipt),false)
    log("FISH_POND_V2_NATIVE_PASS "..helpers.table_to_json(receipt))
  end
end)
