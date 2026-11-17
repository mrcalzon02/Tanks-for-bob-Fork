local function read(o,k) local ok,v=pcall(function() return o[k] end);if ok then return v end;return 'unsupported runtime field '..k end
script.on_init(function()
 local p=prototypes.entity['thinking-hut'];local names=p.lab_inputs;local accepted={};for _,n in ipairs(names) do accepted[n]=true end
 local techs={};local use={}
 for name,t in pairs(prototypes.technology) do
  local ingredients=t.research_unit_ingredients;local eligible=ingredients and #ingredients>0
  for _,i in pairs(ingredients or {}) do if not accepted[i.name] then eligible=false end end
  if eligible then
   local prereqs={};for key,_ in pairs(t.prerequisites) do prereqs[#prereqs+1]=key end;table.sort(prereqs)
   techs[#techs+1]={name=name,ingredients=ingredients,unit_count=t.research_unit_count,unit_energy=t.research_unit_energy,prerequisites=prereqs}
   for _,i in ipairs(ingredients) do use[i.name]=(use[i.name] or 0)+1 end
  end
 end
 table.sort(techs,function(a,b)return a.name<b.name end)
 local s=game.surfaces[1];s.request_to_generate_chunks({0,0},1);s.force_generate_chunk_requests();local directions={}
 for i,d in ipairs({defines.direction.north,defines.direction.east,defines.direction.south,defines.direction.west}) do
  local pos={i*8+.5,.5};local tiles={};for x=-2,2 do for y=-2,2 do tiles[#tiles+1]={name='grass-1',position={pos[1]+x,pos[2]+y}} end end;s.set_tiles(tiles,true)
  local e=s.create_entity{name='thinking-hut',position=pos,force='player',direction=d};local before=e.direction;local rotated=e.rotate();directions[#directions+1]={requested=d,placed=before,rotatable=e.rotatable,rotate_result=rotated,after=e.direction}
 end
 local unlocks={};for name,t in pairs(prototypes.technology) do for _,effect in ipairs(t.effects or {}) do if effect.type=='unlock-recipe' and effect.recipe=='thinking-hut' then unlocks[#unlocks+1]=name end end end
 local report={entity={name=p.name,type=p.type,collision_box=p.collision_box,selection_box=p.selection_box,lab_inputs=names,researching_speed=read(p,'lab_researching_speed'),max_energy_usage_per_tick=read(p,'max_energy_usage'),module_inventory_size=read(p,'module_inventory_size')},building={recipe={ingredients=prototypes.recipe['thinking-hut'].ingredients,products=prototypes.recipe['thinking-hut'].products,energy=prototypes.recipe['thinking-hut'].energy,enabled=game.forces.player.recipes['thinking-hut'].enabled},technology_unlocks=unlocks,item_place_result=prototypes.item['thinking-hut'].place_result.name},processing_recipes='not applicable: lab performs technology research',fluid_connections='none',directions=directions,eligible_technologies=techs,input_technology_counts=use}
 -- LuaBurnerPrototype is a LuaObject, so materialize only the actual fuel contract.
 report.entity.researching_speed=p.get_researching_speed()
 report.entity.max_energy_usage_per_tick=p.get_max_energy_usage()
 local burner=p.burner_prototype;report.entity.burner={fuel_categories=burner.fuel_categories,effectivity=burner.effectivity,fuel_inventory_size=burner.fuel_inventory_size}
 helpers.write_file('thinking-hut-v1/contract.json',helpers.table_to_json(report),false);log('THINKING_HUT_CONTRACT_PASS technologies='..#techs)
end)
