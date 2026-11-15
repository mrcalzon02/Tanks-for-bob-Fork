-- Disposable native proof: actual connections, water/oil transfer, no-fuel,
-- stop/restart, full output and save/reload. Never loaded by the installed mod.
local function ensure(value,message) if not value then error("PIPE_PUMP_V3: "..message) end end
local reloaded=false
script.on_load(function() reloaded=true end)
local function amount(pipe)
  local fluid=pipe.get_fluid_segment_fluid(1)
  return fluid and fluid.amount or 0
end
local function fill(pipe,name)
  return pipe.set_fluid_segment_fluid(1,{name=name,amount=pipe.get_fluid_segment_capacity(1)})
end
script.on_init(function()
  storage.units={}
  local surface=game.surfaces[1]
  local directions={defines.direction.north,defines.direction.east,defines.direction.south,defines.direction.west}
  local names={"north","east","south","west"}
  for row,state in ipairs({"water","crude-oil","unfuelled"}) do
    for d,direction in ipairs(directions) do
      local center={x=d*24+.5,y=row*24}
      surface.request_to_generate_chunks(center,1)
    end
  end
  surface.force_generate_chunk_requests()
  for row,state in ipairs({"water","crude-oil","unfuelled"}) do
    for d,direction in ipairs(directions) do
      local center={x=d*24+.5,y=row*24}
      local tiles={}
      for x=-5,5 do for y=-5,5 do tiles[#tiles+1]={name="refined-concrete",position={center.x+x,center.y+y}} end end
      surface.set_tiles(tiles,true)
      for _,entity in pairs(surface.find_entities_filtered{area={{center.x-5,center.y-5},{center.x+5,center.y+5}},type={"tree","simple-entity","resource"}}) do entity.destroy() end
      local pump=surface.create_entity{name="primitive-steam-powered-pump",position=center,direction=direction,force="player"}
      ensure(pump and pump.valid,"missing pump "..names[d])
      local unit={pump=pump,state=state,facing=names[d],ports={}}
      local ports=pump.get_fluid_box_pipe_connections(1)
      ensure(ports and #ports==2,"wrong native port count")
      for _,port in ipairs(ports) do
        local pipe=surface.create_entity{name="pipe",position=port.target_position,force="player"}
        ensure(pipe and pipe.valid,"adjacent pipe placement failed")
        if port.flow_direction=="input" then unit.input=pipe elseif port.flow_direction=="output" then unit.output=pipe end
        unit.ports[#unit.ports+1]={flow_direction=port.flow_direction,position=port.position,target_position=port.target_position}
      end
      ensure(unit.input and unit.output,"missing input/output distinction")
      if state~="unfuelled" then ensure(pump.get_fuel_inventory().insert{name="coal",count=5}==5,"fuel rejected") end
      fill(unit.input,state=="crude-oil" and "crude-oil" or "water")
      storage.units[#storage.units+1]=unit
    end
  end
  storage.phase="initial"
end)
script.on_nth_tick(30,function(event)
  if reloaded then
    for _,u in ipairs(storage.units) do
      ensure(u.pump.valid and u.input.valid and u.output.valid,"saved entities missing")
      local ports=u.pump.get_fluid_box_pipe_connections(1)
      ensure(#ports==2 and ports[1].target and ports[2].target,"saved connections missing")
    end
    log("PIPE_PUMP_V3_RELOAD_PASS pumps=12 connections=24")
    reloaded=false
  end
  if event.tick==60 then
    local connections=0
    for _,u in ipairs(storage.units) do
      local ports=u.pump.get_fluid_box_pipe_connections(1)
      for _,p in ipairs(ports) do ensure(p.target and p.target.valid,"native pipe disconnected");connections=connections+1 end
      if u.state=="unfuelled" then ensure(amount(u.output)<.0001,"unfuelled pump transferred fluid")
      else ensure(amount(u.output)>1,"native transfer failed for "..u.state.."/"..u.facing) end
      if u.state=="water" then
        u.pump.disabled_by_script=true
        u.output.clear_fluid_segment_fluid(1)
        fill(u.input,"water")
      end
    end
    ensure(connections==24,"wrong connection total")
    log("PIPE_PUMP_V3_INITIAL_PASS water=4 oil=4 unfuelled=4 connections=24")
    storage.phase="stopped"
  elseif event.tick==90 then
    -- Native output storage may release its already-pumped fluid after stop.
    -- Compare stable amounts after that buffer settles, not an assumed zero.
    for _,u in ipairs(storage.units) do if u.state=="water" then
      u.stopped_input=amount(u.input);u.stopped_output=amount(u.output)
    end end
  elseif event.tick==120 then
    for _,u in ipairs(storage.units) do if u.state=="water" then
      ensure(math.abs(amount(u.output)-u.stopped_output)<.001 and math.abs(amount(u.input)-u.stopped_input)<.001,"disabled pump continued transfer")
      u.output.clear_fluid_segment_fluid(1);fill(u.input,"water")
      u.pump.disabled_by_script=false
    end end
    log("PIPE_PUMP_V3_STOP_PASS pumps=4")
  elseif event.tick==180 then
    for _,u in ipairs(storage.units) do if u.state=="water" then
      ensure(amount(u.output)>1,"restart did not transfer fluid")
      fill(u.output,"water")
      -- A normal pump also owns a 200-unit internal buffer. Fill it as well;
      -- a full downstream pipe alone does not mean the pump is full.
      u.pump.insert_fluid{name="water",amount=1000000}
      fill(u.input,"water")
    end end
    log("PIPE_PUMP_V3_RESTART_PASS pumps=4")
  elseif event.tick==210 then
    for _,u in ipairs(storage.units) do if u.state=="water" then
      u.full_input_before=amount(u.input)
      log("PIPE_PUMP_V3_FULL_DIAG "..helpers.table_to_json{tick=event.tick,facing=u.facing,input=amount(u.input),output=amount(u.output),capacity=u.output.get_fluid_segment_capacity(1),pump_fluid=u.pump.get_fluid_contents()})
    end end
  elseif event.tick==240 then
    for _,u in ipairs(storage.units) do if u.state=="water" then
      log("PIPE_PUMP_V3_FULL_DIAG "..helpers.table_to_json{tick=event.tick,facing=u.facing,input=amount(u.input),output=amount(u.output),capacity=u.output.get_fluid_segment_capacity(1),pump_fluid=u.pump.get_fluid_contents()})
      ensure(math.abs(amount(u.input)-u.full_input_before)<.001,"full output consumed input")
      ensure(math.abs(amount(u.output)-u.output.get_fluid_segment_capacity(1))<.001,"full output changed")
    end end
    local receipt={passed=true,pumps=12,connections=24,facings=4,water_transfer=true,oil_transfer=true,no_fuel_stopped=true,stop_restart=true,full_output=true,units={}}
    for _,u in ipairs(storage.units) do receipt.units[#receipt.units+1]={facing=u.facing,state=u.state,position=u.pump.position,ports=u.ports} end
    helpers.write_file("pipe-pump-v3/native-runtime.json",helpers.table_to_json(receipt),false)
    log("PIPE_PUMP_V3_NATIVE_PASS "..helpers.table_to_json(receipt))
    storage.phase="complete"
  end
end)
