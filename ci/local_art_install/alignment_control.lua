-- Test normal player-grid pipes, never arbitrary off-grid target spawns.
local function check(v,m) if not v then error('TANKS_ALIGNMENT: '..m) end end
local names={'north','east','south','west'}
local dirs={defines.direction.north,defines.direction.east,defines.direction.south,defines.direction.west}
local kinds={{'pump','primitive-steam-powered-pump',1},{'solar','solar-boiler',2},{'pond','fish-pond',2}}
local function initialize()
  local sf=game.surfaces[1];sf.always_day=true;sf.daytime=0
  storage.alignment_units={}
  for row=1,6 do for d=1,4 do sf.request_to_generate_chunks({128+d*24,128+row*24},1) end end
  sf.force_generate_chunk_requests()
  for k,kind in ipairs(kinds) do for mode_index,mode in ipairs({'pipes','caps'}) do for d,direction in ipairs(dirs) do
    local p={x=128+d*24,y=128+(k*2-2+mode_index)*24}
    for _,e in pairs(sf.find_entities_filtered{area={{p.x-7,p.y-7},{p.x+7,p.y+7}}}) do if e.valid then e.destroy() end end
    local tiles={};for x=-7,7 do for y=-7,7 do tiles[#tiles+1]={name='refined-concrete',position={p.x+x,p.y+y}} end end
    sf.set_tiles(tiles,true);sf.destroy_decoratives{area={{p.x-7,p.y-7},{p.x+7,p.y+7}}}
    local m=sf.create_entity{name=kind[2],position=p,direction=direction,force='player'}
    check(m and m.valid,'machine '..kind[2]..'/'..names[d])
    if kind[1]=='pond' then m.set_recipe('local-alignment-water-proof') end
    local fuel=m.get_fuel_inventory();if fuel then fuel.insert{name='coal',count=5} end
    local u={machine=m,kind=kind[1],facing=names[d],mode=mode,ports={}}
    for box=1,kind[3] do
      for _,port in ipairs(m.get_fluid_box_pipe_connections(box)) do
        local record={box=box,position=port.position,target=port.target_position,flow=port.flow_direction}
        if mode=='pipes' then
          local grid={x=math.floor(port.target_position.x)+.5,y=math.floor(port.target_position.y)+.5}
          check(math.abs(grid.x-port.target_position.x)<.001 and math.abs(grid.y-port.target_position.y)<.001,
            'OFF_GRID '..kind[1]..'/'..names[d]..' '..helpers.table_to_json(record))
          check(sf.can_place_entity{name='pipe',position=grid,force='player'},'player pipe collision')
          local pipe=sf.create_entity{name='pipe',position=grid,force='player'}
          check(pipe and pipe.valid,'grid pipe placement')
          record.pipe=pipe
          if port.flow_direction~='output' then pipe.set_fluid_segment_fluid(1,{name='water',amount=pipe.get_fluid_segment_capacity(1)}) end
        end
        u.ports[#u.ports+1]=record
      end
    end
    storage.alignment_units[#storage.alignment_units+1]=u
  end end end
end
local function tick(ev)
  if ev.tick==120 then
    local connected=0;local result={passed=true,player_grid_pipes=true,units={}}
    for _,u in ipairs(storage.alignment_units) do
      local row={kind=u.kind,facing=u.facing,mode=u.mode,position=u.machine.position,ports={}}
      for _,p in ipairs(u.ports) do
        if p.pipe then
          local actual=u.machine.get_fluid_box_pipe_connections(p.box)
          local found=false;for _,v in ipairs(actual) do if v.target==p.pipe then found=true end end
          check(found,'disconnected player-grid pipe '..u.kind..'/'..u.facing);connected=connected+1
          if u.kind=='pump' and p.flow=='output' then check((p.pipe.get_fluid_contents().water or 0)>.1,'pump did not transfer') end
        end
        row.ports[#row.ports+1]={position=p.position,target=p.target,flow=p.flow,pipe=p.pipe and p.pipe.position or nil}
      end
      result.units[#result.units+1]=row
    end
    check(connected==28,'wrong native pipe total');result.connected_player_grid_pipes=connected
    helpers.write_file('tanks-alignment/native-runtime.json',helpers.table_to_json(result),false)
    log('TANKS_ALIGNMENT_NATIVE_PASS player_grid_pipes=28 machines=24')
  end
  if ev.tick==30 and script.active_mods['local-alignment-capture'] then
    for _,u in ipairs(storage.alignment_units) do
      game.take_screenshot{surface=u.machine.surface,position={u.machine.position.x,u.machine.position.y-.5},
        resolution={768,512},zoom=3,path='tanks-alignment/'..u.kind..'-'..u.facing..'-'..u.mode..'.png',
        show_gui=false,show_entity_info=false,anti_alias=true,force_render=true,daytime=0,hide_clouds=true,hide_fog=true}
    end
    game.set_wait_for_screenshots_to_finish();log('TANKS_ALIGNMENT_SCREENSHOTS_COMPLETE count=24')
  end
end
return {initialize=initialize,tick=tick}
