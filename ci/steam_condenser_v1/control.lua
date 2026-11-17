-- Native test of the actual Tanks recipe, without inventing water production.
local function check(v,m) if not v then error('TANKS_CONDENSER_V1: '..m) end end
local function count(u) return u.machine.get_output_inventory().get_item_count('stone') end
local reloaded=false
script.on_load(function() reloaded=true end)
script.on_init(function()
  storage.units={}
  local sf=game.surfaces[1]
  local names={'north','east','south','west'}
  local dirs={defines.direction.north,defines.direction.east,defines.direction.south,defines.direction.west}
  for row=1,3 do for d=1,4 do sf.request_to_generate_chunks({d*24+.5,row*24+.5},1) end end
  sf.force_generate_chunk_requests()
  for row,state in ipairs({'working','unfuelled','blocked'}) do for d,direction in ipairs(dirs) do
    local p={x=d*24+.5,y=row*24+.5}
    for _,e in pairs(sf.find_entities_filtered{area={{p.x-5,p.y-5},{p.x+5,p.y+5}},type={'tree','simple-entity','resource'}}) do e.destroy() end
    local tiles={};for x=-5,5 do for y=-5,5 do tiles[#tiles+1]={name='refined-concrete',position={p.x+x,p.y+y}} end end
    sf.set_tiles(tiles,true);sf.destroy_decoratives{area={{p.x-5,p.y-5},{p.x+5,p.y+5}}}
    local m=sf.create_entity{name='steam-condenser',position=p,direction=direction,force='player'}
    check(m and m.valid,'placement '..names[d]);m.set_recipe('Steam-condenserA')
    check(m.get_inventory(defines.inventory.crafter_input).insert{name='wood',count=50}==50,'wood input')
    if state~='unfuelled' then m.get_fuel_inventory().insert{name='coal',count=5} end
    local u={machine=m,facing=names[d],state=state,pipes={}}
    for box=1,2 do
      local ports=m.get_fluid_box_pipe_connections(box);check(#ports==1,'port count')
      local port=ports[1];local pipe=sf.create_entity{name='pipe',position=port.target_position,force='player'}
      check(pipe and pipe.valid,'pipe placement');u.pipes[#u.pipes+1]=pipe
      if port.flow_direction=='input' then
        pipe.set_fluid_segment_fluid(1,{name='steam',temperature=165,amount=pipe.get_fluid_segment_capacity(1)})
      end
    end
    if state=='blocked' then
      m.get_output_inventory().insert{name='stone',count=100000}
      m.get_output_inventory().insert{name='tank-ammo-Industrialwaste',count=100000}
      u.full=count(u)
    end
    storage.units[#storage.units+1]=u
  end end
end)
script.on_nth_tick(60,function(ev)
  if reloaded then
    check(#storage.units==12,'saved fixture count')
    for _,u in ipairs(storage.units) do check(u.machine.valid,'saved machine') end
    log('FISH_POND_V2_RELOAD_PASS TANKS_CONDENSER_V1 ponds=12');reloaded=false
  end
  if ev.tick==3600 then
    for _,u in ipairs(storage.units) do
      for box=1,2 do check(u.machine.get_fluid_box_pipe_connections(box)[1].target,'native disconnected pipe') end
      if u.state=='working' then
        check(count(u)>=10,'real recipe did not produce stone '..u.facing)
        check(u.machine.get_output_inventory().get_item_count('tank-ammo-Industrialwaste')>=1,'missing actual waste result')
        u.machine.disabled_by_script=true;u.stopped=count(u);u.progress=u.machine.crafting_progress
      elseif u.state=='unfuelled' then check(count(u)==0,'unfuelled production')
      else check(count(u)==u.full,'blocked output changed') end
    end
  elseif ev.tick==3900 then
    for _,u in ipairs(storage.units) do if u.state=='working' then
      check(count(u)==u.stopped and math.abs(u.machine.crafting_progress-u.progress)<1e-6,'disabled machine worked')
      u.machine.disabled_by_script=false
    end end
  elseif ev.tick==7500 then
    local receipt={passed=true,machines=12,connections=24,facings=4,real_recipe='Steam-condenserA',
      consumes={'wood','steam'},produces={'stone','tank-ammo-Industrialwaste'},water_output_recipe=false,
      unfuelled_stops=true,blocked_output=true,stop_restart=true}
    for _,u in ipairs(storage.units) do if u.state=='working' then check(count(u)>u.stopped,'restart') end end
    helpers.write_file('steam-condenser-v1/native-runtime.json',helpers.table_to_json(receipt),false)
    -- Preserve the shared runner's success protocol while naming the actual asset.
    log('FISH_POND_V2_NATIVE_PASS TANKS_CONDENSER_V1 '..helpers.table_to_json(receipt))
  end
end)
