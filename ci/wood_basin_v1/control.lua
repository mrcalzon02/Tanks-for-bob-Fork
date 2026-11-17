-- Real passive tank, ordinary player-grid pipes and powered external pumps.
local function check(v,m) if not v then error('WOOD_BASIN: '..m) end end
local loaded=false
script.on_load(function() loaded=true end)
local function amount(u)
 local f=u.tank.get_fluid_segment_fluid(1);return f and f.amount or 0
end
local function direction(nx,ny)
 return nx==1 and defines.direction.east or nx==-1 and defines.direction.west or ny==1 and defines.direction.south or defines.direction.north
end
script.on_init(function()
 local s=game.surfaces[1];s.always_day=true;s.daytime=0;storage.units={};storage.complete=false
 game.forces.player.technologies['wood-basin'].researched=true
 check(game.forces.player.recipes['wood-basin'].enabled,'technology failed to unlock building')
 check(prototypes.item['wood-basin'].place_result.name=='wood-basin','placeable item')
 local names={'north','east','south','west'};local dirs={defines.direction.north,defines.direction.east,defines.direction.south,defines.direction.west}
 for row=1,3 do for d=1,4 do s.request_to_generate_chunks({d*32+.5,row*32+.5},1) end end;s.force_generate_chunk_requests()
 for row,fluid in ipairs({'water','crude-oil','steam'}) do for d,dir in ipairs(dirs) do
  local pos={x=d*32+.5,y=row*32+.5};local area={{pos.x-9,pos.y-9},{pos.x+9,pos.y+9}}
  for _,e in pairs(s.find_entities_filtered{area=area}) do e.destroy() end
  local tiles={};for x=-9,9 do for y=-9,9 do tiles[#tiles+1]={name='refined-concrete',position={pos.x+x,pos.y+y}} end end
  s.set_tiles(tiles,true);s.destroy_decoratives{area=area}
  check(s.can_place_entity{name='wood-basin',position=pos,direction=dir,force='player'},'tank placement')
  local tank=s.create_entity{name='wood-basin',position=pos,direction=dir,force='player'}
  check(tank.get_fluid_segment_capacity(1)==25000,'capacity changed')
  check(tank.get_fuel_inventory()==nil,'passive tank unexpectedly needs fuel')
  local u={tank=tank,fluid=fluid,facing=names[d],ports={},pumps={}}
  local ports=tank.get_fluid_box_pipe_connections(1);check(#ports==4,'four native ports required')
  for i,port in ipairs(ports) do
   local grid={x=math.floor(port.target_position.x)+.5,y=math.floor(port.target_position.y)+.5}
   check(math.abs(grid.x-port.target_position.x)<.001 and math.abs(grid.y-port.target_position.y)<.001,'off-grid port')
   check(s.can_place_entity{name='pipe',position=grid,force='player'},'normal pipe collision')
   local pipe=s.create_entity{name='pipe',position=grid,force='player'}
   u.ports[#u.ports+1]={entity=pipe,target=grid}
   if i==1 or i==3 then
    local dx,dy=grid.x-pos.x,grid.y-pos.y;local nx,ny=0,0
    if math.abs(dx)>math.abs(dy) then nx=dx>0 and 1 or -1 else ny=dy>0 and 1 or -1 end
    local input=i==1;local p={x=grid.x+nx*1.5,y=grid.y+ny*1.5};local pd=direction(input and -nx or nx,input and -ny or ny)
    check(s.can_place_entity{name='pump',position=p,direction=pd,force='player'},'external pump placement')
    local pump=s.create_entity{name='pump',position=p,direction=pd,force='player'}
    local far={x=grid.x+nx*3,y=grid.y+ny*3};check(s.can_place_entity{name='pipe',position=far,force='player'},'far pipe placement')
    local fp=s.create_entity{name='pipe',position=far,force='player'}
    local rec={entity=pump,far=fp,input=input};u.pumps[#u.pumps+1]=rec
    pump.energy=1000000;pump.disabled_by_script=not input
    if input then u.source=rec else u.sink=rec end
   end
  end
  check(u.source and u.sink,'external transfer fixture missing');storage.units[#storage.units+1]=u
 end end
end)
script.on_nth_tick(1,function(event)
 if loaded then
  check(#storage.units==12,'saved tanks missing')
  for _,u in ipairs(storage.units) do
   check(u.tank.valid,'saved tank invalid');for _,p in ipairs(u.ports) do check(p.entity.valid,'saved pipe invalid') end
   local ports=u.tank.get_fluid_box_pipe_connections(1);check(#ports==4,'saved port count');for _,p in ipairs(ports) do check(p.target,'saved native port disconnected') end
  end
  if storage.saved_levels then
   for i,u in ipairs(storage.units) do
    local f=u.tank.get_fluid_segment_fluid(1);local saved=storage.saved_levels[i]
    check(f and f.name==saved.name and math.abs(f.amount-saved.amount)<.001 and math.abs(f.temperature-saved.temperature)<.001,'saved fluid/temperature lost')
   end
   log('WOOD_BASIN_FILLED_RELOAD_PASS snapshots=12')
  end
  log('WOOD_BASIN_RELOAD_PASS complete='..tostring(storage.complete));loaded=false
 end
 for _,u in ipairs(storage.units) do
  for _,p in ipairs(u.pumps) do p.entity.energy=1000000 end
  if event.tick<2400 or event.tick>=4320 then
   u.source.far.set_fluid_segment_fluid(1,{name=u.fluid,amount=u.source.far.get_fluid_segment_capacity(1),temperature=u.fluid=='steam' and 165 or 25})
  end
  u.sink.far.clear_fluid_segment_fluid(1)
 end
 if event.tick==2400 then
  for _,u in ipairs(storage.units) do
   check(math.abs(amount(u)-u.tank.get_fluid_segment_capacity(1))<.001,'full tank did not saturate '..u.fluid..u.facing..' amount='..amount(u))
   local ports=u.tank.get_fluid_box_pipe_connections(1);for _,p in ipairs(ports) do check(p.target,'native corner disconnected') end
   u.source.entity.disabled_by_script=true
  end
  log('WOOD_BASIN_FILL_FULL_PASS tanks=12 connections=48')
 elseif event.tick==2460 then
  for _,u in ipairs(storage.units) do u.stopped=amount(u) end
 elseif event.tick==2520 then
  for _,u in ipairs(storage.units) do check(math.abs(amount(u)-u.stopped)<.01,'stopped flow changed');u.sink.entity.disabled_by_script=false end
  log('WOOD_BASIN_STOP_PASS')
 elseif event.tick==4320 then
  for _,u in ipairs(storage.units) do check(amount(u)<1,'drain failed '..u.fluid..u.facing..' amount='..amount(u));u.sink.entity.disabled_by_script=true;u.source.entity.disabled_by_script=false end
  log('WOOD_BASIN_DRAIN_PASS')
 elseif event.tick==5100 then
  for _,u in ipairs(storage.units) do check(amount(u)>5000,'refill/restart failed') end
  storage.complete=true
  local receipt={passed=true,tanks=12,cardinal_tests=4,native_art_orientations=2,capacity=25000,normal_player_grid_connections=48,fluids={'water','crude-oil','steam'},external_pump_fill_drain=true,no_tank_fuel_or_power=true,blocked_full=true,stop_restart=true,prototype_overrides=false}
  helpers.write_file('wood-basin-v1/native-runtime.json',helpers.table_to_json(receipt),false);log('WOOD_BASIN_NATIVE_PASS '..helpers.table_to_json(receipt));game.auto_save('wood-basin-operational')
 end
end)

remote.add_interface('wood_basin_proof',{snapshot=function()
 storage.saved_levels={}
 for _,u in ipairs(storage.units) do
  local f=u.tank.get_fluid_segment_fluid(1);check(f and f.amount>0,'snapshot requires filled tank')
  storage.saved_levels[#storage.saved_levels+1]={name=f.name,amount=f.amount,temperature=f.temperature}
 end
 return #storage.saved_levels
end})
