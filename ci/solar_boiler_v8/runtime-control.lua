-- Solar Boiler V8 native Factorio 2.1.24 runtime fixture.
-- Tests real engine fluid connections for all four rotations; no screenshot claims.
local checked=false
local units={}
local function ensure(v,msg) if not v then error("SOLAR_V8_PIPE_ERROR: "..msg) end end
script.on_init(function()
  local surface=game.surfaces[1]
  local dirs={defines.direction.north,defines.direction.east,defines.direction.south,defines.direction.west}
  for d=1,4 do
    local pos={x=32*(d-1),y=32}
    surface.request_to_generate_chunks(pos,2)
  end
  surface.force_generate_chunk_requests()
  for d,dir in ipairs(dirs) do
    local pos={x=32*(d-1),y=32}
    local boiler=surface.create_entity{name="solar-boiler",position=pos,force="player",direction=dir}
    ensure(boiler and boiler.valid, "missing solar-boiler in direction "..d)
    local water=boiler.get_fluid_box_pipe_connections(1) or {}
    local steam=boiler.get_fluid_box_pipe_connections(2) or {}
    ensure(#water==2 and #steam==1,"wrong fluid connector count in direction "..d)
    local pipes={}
    for _,conn in ipairs(water) do
      ensure(conn.target_position,"water port has no target position")
      local pipe=surface.create_entity{name="pipe",position=conn.target_position,force="player"}
      ensure(pipe and pipe.valid, "water adjacency placement failed in direction "..d)
      table.insert(pipes,pipe)
    end
    for _,conn in ipairs(steam) do
      ensure(conn.target_position,"steam port has no target position")
      local pipe=surface.create_entity{name="pipe",position=conn.target_position,force="player"}
      ensure(pipe and pipe.valid, "steam adjacency placement failed in direction "..d)
      table.insert(pipes,pipe)
    end
    units[d]={boiler=boiler,pipes=pipes,direction=dir}
  end
end)
script.on_nth_tick(30,function()
  if checked then return end
  checked=true
  local connected=0
  for d,record in ipairs(units) do
    local bo=record.boiler
    ensure(bo and bo.valid,"missing boiler at test time in direction "..d)
    local water=bo.get_fluid_box_pipe_connections(1) or {}
    local steam=bo.get_fluid_box_pipe_connections(2) or {}
    ensure(#water==2 and #steam==1,"connections disappeared in direction "..d)
    for _,conn in ipairs(water) do
      ensure(conn.target and conn.target.valid and conn.target.name=="pipe",
             "water port not connected in direction "..d)
      connected=connected+1
    end
    for _,conn in ipairs(steam) do
      ensure(conn.target and conn.target.valid and conn.target.name=="pipe",
             "steam port not connected in direction "..d)
      connected=connected+1
    end
  end
  ensure(connected==12,"expected 12 total pipe connections, got "..connected)
  log("SOLAR_BOILER_V8_NATIVE_ENGINE_PIPE_PASS direction_count=4 pipe_connections=12")
  game.write_file("solar-boiler-v8-native-runtime.txt","SOLAR_BOILER_V8_NATIVE_ENGINE_PIPE_PASS connections=12\n",false)
end)
