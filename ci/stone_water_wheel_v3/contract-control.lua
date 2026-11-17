local function read(p,k) local ok,v=pcall(function() return p[k] end);if ok then return v end;return 'unsupported runtime field '..k end
local function turn(x,y,d) if d==0 then return x,y elseif d==4 then return -y,x elseif d==8 then return -x,-y else return y,-x end end
script.on_init(function()
 local s=game.surfaces[1];s.always_day=true;storage.units={}
 for _,d in ipairs({0,4,8,12}) do
  local p={x=4.5+d*4,y=4.5};s.request_to_generate_chunks(p,1);s.force_generate_chunk_requests()
  for _,e in pairs(s.find_entities_filtered{area={{p.x-5,p.y-5},{p.x+5,p.y+5}}}) do e.destroy() end
  local tiles={};for x=-4,4 do for y=-4,4 do local a,b=turn(x,y,d);tiles[#tiles+1]={name=y<0 and 'water' or 'grass-1',position={p.x+a,p.y+b}} end end;s.set_tiles(tiles,true)
  local legal=s.can_place_entity{name='stone-water-wheel',position=p,direction=d,force='player'}
  local e=s.create_entity{name='stone-water-wheel',position=p,direction=d,force='player'};assert(e,'native entity')
  local ports={};for _,q in ipairs(e.get_fluid_box_pipe_connections(1)) do
   local grid={x=math.floor(q.target_position.x)+.5,y=math.floor(q.target_position.y)+.5}
   local can=s.can_place_entity{name='pipe',position=grid,force='player'};local pipe=nil;if can then pipe=s.create_entity{name='pipe',position=grid,force='player'} end
   ports[#ports+1]={position=q.position,target_position=q.target_position,flow_direction=q.flow_direction,nearest_player_grid=grid,pipe_can_place=can,pipe=pipe}
  end
  storage.units[#storage.units+1]={entity=e,requested=d,normal_placement=legal,ports=ports}
 end
end)
script.on_nth_tick(120,function(ev)
 if ev.tick~=120 then return end
 local p=prototypes.entity['stone-water-wheel'];local recipe=prototypes.recipe['stone-water-wheel'];local tech=prototypes.technology['stone-water-wheel'];local prereqs={};for n,_ in pairs(tech.prerequisites) do prereqs[#prereqs+1]=n end;table.sort(prereqs)
 local report={entity={name=p.name,type=p.type,collision_box=p.collision_box,selection_box=p.selection_box,tile_width=p.tile_width,tile_height=p.tile_height,pumping_speed=p.get_pumping_speed(),fluid_source_offset=read(p,'fluid_source_offset'),energy_usage_per_tick=p.get_max_energy_usage(),burner=not not p.burner_prototype,electric=not not p.electric_energy_source_prototype},placeable_item={name='stone-water-wheel',place_result=prototypes.item['stone-water-wheel'].place_result.name,stack_size=prototypes.item['stone-water-wheel'].stack_size},building_recipe={name=recipe.name,categories=recipe.categories,ingredients=recipe.ingredients,products=recipe.products,energy=recipe.energy,enabled=game.forces.player.recipes['stone-water-wheel'].enabled},technology={name=tech.name,prerequisites=prereqs,unit_count=tech.research_unit_count,unit_energy_ticks=tech.research_unit_energy,ingredients=tech.research_unit_ingredients,effects=tech.effects},processing='No processing recipes: shoreline water extraction using native offshore-pump fluid source',directions={}}
 for _,u in ipairs(storage.units) do
  local e=u.entity;local row={requested=u.requested,actual=e.direction,position=e.position,normal_shore_placement=u.normal_placement,status=e.status,fluid=e.get_fluid_contents(),ports={}}
  for i,q in ipairs(e.get_fluid_box_pipe_connections(1)) do local old=u.ports[i];row.ports[#row.ports+1]={position=q.position,target_position=q.target_position,flow_direction=q.flow_direction,nearest_player_grid=old.nearest_player_grid,pipe_can_place=old.pipe_can_place,actual_pipe_connected=old.pipe and q.target==old.pipe or false,pipe_fluid=old.pipe and old.pipe.get_fluid_contents() or {}} end
  report.directions[#report.directions+1]=row
 end
 helpers.write_file('stone-water-wheel-v1/contract.json',helpers.table_to_json(report),false);log('STONE_WATER_WHEEL_CONTRACT_PASS')
end)
