script.on_init(function()
 local p=prototypes.entity['tank-ammo-assembling-machine'];local categories=p.crafting_categories;local recipes={};local parameter_recipes={};local unlocks={}
 for n,t in pairs(prototypes.technology) do for _,effect in ipairs(t.effects or {}) do if effect.type=='unlock-recipe' then unlocks[effect.recipe]=unlocks[effect.recipe] or {};table.insert(unlocks[effect.recipe],n) end end end
 local input_recipe=nil;local output_recipe=nil
 for n,q in pairs(prototypes.recipe) do
  local valid=q.has_category('tank-ammo-component');if not valid and q.has_category('parameters') then parameter_recipes[#parameter_recipes+1]=n end
  if valid then recipes[#recipes+1]={name=n,categories=q.categories,ingredients=q.ingredients,products=q.products,energy=q.energy,enabled_initially=game.forces.player.recipes[n].enabled,unlocked_by=unlocks[n] or {}};for _,i in ipairs(q.ingredients) do if i.type=='fluid' then input_recipe=n end end;for _,i in ipairs(q.products) do if i.type=='fluid' then output_recipe=n end end end
 end;table.sort(recipes,function(a,b)return a.name<b.name end)
 local s=game.surfaces[1];s.request_to_generate_chunks({20,0},3);s.force_generate_chunk_requests();local directions={}
 for i,d in ipairs({0,4,8,12}) do
  local pos={x=i*12+.5,y=.5};for _,e in pairs(s.find_entities_filtered{area={{pos.x-4,-4},{pos.x+4,4}}}) do e.destroy() end;local tiles={};for x=-4,4 do for y=-4,4 do tiles[#tiles+1]={name='grass-1',position={pos.x+x,pos.y+y}} end end;s.set_tiles(tiles,true)
  local legal=s.can_place_entity{name=p.name,position=pos,direction=d,force='player'};local e=s.create_entity{name=p.name,position=pos,direction=d,force='player'};local row={requested=d,placed=e.direction,normal_placement=legal,recipe_ports={}}
  if i==1 then for _,q in ipairs(recipes) do e.set_recipe(q.name);q.native_recipe_selectable=e.get_recipe() and e.get_recipe().name==q.name or false end end
  for _,q in ipairs({input_recipe,output_recipe}) do
   e.set_recipe(q);local record={recipe=q,ports={}}
   for box=1,e.fluids_count do for _,port in ipairs(e.get_fluid_box_pipe_connections(box)) do
    local grid={x=math.floor(port.target_position.x)+.5,y=math.floor(port.target_position.y)+.5};local pipe=s.find_entity('pipe',grid);if not pipe and s.can_place_entity{name='pipe',position=grid,force='player'} then pipe=s.create_entity{name='pipe',position=grid,force='player'} end
    record.ports[#record.ports+1]={box=box,position=port.position,target_position=port.target_position,flow_direction=port.flow_direction,grid=grid,actual_pipe_connected=pipe and e.get_fluid_box_pipe_connections(box)[1].target==pipe or false}
   end end;row.recipe_ports[#row.recipe_ports+1]=record
  end;directions[#directions+1]=row
 end
 local building=prototypes.recipe[p.name];local builders={};for n,e in pairs(prototypes.entity) do if e.crafting_categories then for _,cat in ipairs(building.categories) do if e.crafting_categories[cat] then builders[#builders+1]=n;break end end end end;table.sort(builders)
 local techs={};for _,n in ipairs(unlocks[p.name] or {}) do local t=prototypes.technology[n];local prereqs={};for name,_ in pairs(t.prerequisites) do prereqs[#prereqs+1]=name end;table.sort(prereqs);techs[#techs+1]={name=n,prerequisites=prereqs,ingredients=t.research_unit_ingredients,unit_count=t.research_unit_count,unit_energy_ticks=t.research_unit_energy} end
 local report={entity={name=p.name,type=p.type,collision_box=p.collision_box,selection_box=p.selection_box,tile_width=p.tile_width,tile_height=p.tile_height,crafting_categories=categories,crafting_speed=p.get_crafting_speed(),max_energy_usage_per_tick=p.get_max_energy_usage(),electric=not not p.electric_energy_source_prototype,burner=not not p.burner_prototype,ingredient_count=p.ingredient_count,module_inventory_size=p.module_inventory_size},building={item={name=p.name,place_result=prototypes.item[p.name].place_result.name,stack_size=prototypes.item[p.name].stack_size},recipe={name=building.name,categories=building.categories,ingredients=building.ingredients,products=building.products,energy=building.energy,enabled_initially=game.forces.player.recipes[p.name].enabled},technology_unlocks=techs,category_compatible_builders=builders},processing_recipes=recipes,engine_parameter_recipe_names=parameter_recipes,directions=directions,fluid_probe_recipes={input=input_recipe,output=output_recipe}}
 helpers.write_file('tank-ammo-assembler-v1/contract.json',helpers.table_to_json(report),false);log('TANK_AMMO_ASSEMBLER_CONTRACT_PASS recipes='..#recipes)
end)
