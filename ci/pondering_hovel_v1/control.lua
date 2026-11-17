local function check(v,m) if not v then error('PONDERING_HOVEL_V1: '..m) end end
local function prerequisites(force,name,seen)
 seen=seen or {};if seen[name] then return end;seen[name]=true
 for n,_ in pairs(force.technologies[name].prerequisites) do prerequisites(force,n,seen);force.technologies[n].researched=true end
end
local function inventory(u)
 local result={};local inv=u.lab.get_inventory(defines.inventory.lab_input)
 for _,n in ipairs(prototypes.entity['pondering-hovel'].lab_inputs) do result[n]=inv.get_item_count(n) end
 return result
end
local function same(a,b) for n,count in pairs(a) do if b[n]~=count then return false end end;return true end
local function progress(u) return u.force.technologies[u.technology].researched or u.force.research_progress>0 end
local function snapshot(u)
 return {inputs=inventory(u),coal=u.lab.get_fuel_inventory().get_item_count('coal'),remaining_fuel=u.lab.burner.remaining_burning_fuel,research=u.force.current_research and u.force.current_research.name or false,progress=u.force.research_progress,direction=u.lab.direction,target_researched=u.force.technologies[u.technology].researched}
end
local loaded=false
script.on_load(function() loaded=true end)
script.on_init(function()
 if remote.interfaces.freeplay and remote.interfaces.freeplay.set_skip_intro then remote.call('freeplay','set_skip_intro',true) end
 local proto=prototypes.entity['pondering-hovel'];check(proto.get_researching_speed()==.8,'actual lab speed');check(math.abs(proto.get_max_energy_usage()*60-100000)<.01,'actual burner power');check(prototypes.item['pondering-hovel'].place_result.name=='pondering-hovel','item binding');check(not game.forces.player.recipes['pondering-hovel'].enabled,'building recipe gated');prerequisites(game.forces.player,'pondering-hovel');game.forces.player.technologies['pondering-hovel'].researched=true;check(game.forces.player.recipes['pondering-hovel'].enabled,'actual building technology unlock');check(proto.burner_prototype.effectivity==.5,'actual burner efficiency')
 local accepted={};for _,n in ipairs(proto.lab_inputs) do accepted[n]=true end
 local groups={};local eligible=0
 for name,t in pairs(prototypes.technology) do
  local ingredients=t.research_unit_ingredients;local valid=ingredients and #ingredients>0;local names={}
  for _,i in ipairs(ingredients or {}) do if not accepted[i.name] then valid=false end;names[#names+1]=i.name end
  if valid then
   eligible=eligible+1;table.sort(names);local key=table.concat(names,'|');local old=groups[key]
   if not old or t.research_unit_energy*t.research_unit_count<old.cost or (t.research_unit_energy*t.research_unit_count==old.cost and name<old.name) then groups[key]={name=name,cost=t.research_unit_energy*t.research_unit_count} end
  end
 end
 local keys={};for k,_ in pairs(groups) do keys[#keys+1]=k end;table.sort(keys)
 check(#keys==19 and eligible==75,'actual research contract changed; revisit coverage')
 local cases={};for _,k in ipairs(keys) do cases[#cases+1]={state='real-research',technology=groups[k].name} end
 for _,pair in ipairs({{'no-fuel','beachpump'},{'missing-meal','pondering-hovel'},{'idle','beachpump'},{'stop-restart','beachpump'},{'completed-idle','beachpump'}}) do cases[#cases+1]={state=pair[1],technology=pair[2]} end
 local s=game.surfaces[1];s.always_day=true;s.daytime=0;storage.units={};storage.complete=false;storage.eligible=eligible;storage.sets=#keys
 for i,c in ipairs(cases) do
  local p={x=4.5+(i-1)%5*16,y=4.5+math.floor((i-1)/5)*16};s.request_to_generate_chunks(p,1)
 end;s.force_generate_chunk_requests()
 for i,c in ipairs(cases) do
  local p={x=4.5+(i-1)%5*16,y=4.5+math.floor((i-1)/5)*16};local area={{p.x-3,p.y-3},{p.x+3,p.y+3}};for _,e in pairs(s.find_entities_filtered{area=area}) do e.destroy() end
  local tiles={};for x=-3,3 do for y=-3,3 do tiles[#tiles+1]={name='grass-1',position={p.x+x,p.y+y}} end end;s.set_tiles(tiles,true);s.destroy_decoratives{area=area}
  local force=game.create_force('hut-proof-'..i);prerequisites(force,c.technology)
  local requested=({0,4,8,12})[(i-1)%4+1];check(s.can_place_entity{name='pondering-hovel',position=p,force=force,direction=requested},'normal placement')
  local lab=s.create_entity{name='pondering-hovel',position=p,force=force,direction=requested};check(lab.direction==0 and not lab.rotate(),'native fixed orientation')
  local u={state=c.state,technology=c.technology,force=force,lab=lab,position=p,requested=requested}
  local inv=lab.get_inventory(defines.inventory.lab_input)
  for _,ingredient in ipairs(prototypes.technology[c.technology].research_unit_ingredients) do
   if not (c.state=='missing-meal' and ingredient.name=='meal') then check(inv.insert{name=ingredient.name,count=ingredient.amount*20}==ingredient.amount*20,'actual lab input '..ingredient.name) end
  end
  check(inv.insert{name='automation-science-pack',count=1}==0,'unsupported science rejected')
  if c.state~='no-fuel' then lab.get_fuel_inventory().insert{name='coal',count=20} end
  if c.state~='idle' then check(force.add_research(c.technology),'actual research queued '..c.technology) end
  u.initial=inventory(u);storage.units[#storage.units+1]=u
 end
 local bp={84.5,4.5};s.request_to_generate_chunks(bp,1);s.force_generate_chunk_requests()
 for _,e in pairs(s.find_entities_filtered{area={{81,1},{88,8}}}) do e.destroy() end
 local tiles={};for x=81,88 do for y=1,8 do tiles[#tiles+1]={name='grass-1',position={x,y}} end end;s.set_tiles(tiles,true)
 storage.builder=s.create_entity{name='workbench',position=bp,force='player'};check(storage.builder.set_recipe('pondering-hovel')~=nil,'actual Seablock building recipe selected')
 local inv=storage.builder.get_inventory(defines.inventory.crafter_input);check(inv.insert{name='thinking-hut',count=1}==1 and inv.insert{name='brick',count=10}==10,'real building ingredients');storage.builder.get_fuel_inventory().insert{name='coal',count=20}
 log('PONDERING_HOVEL_V1_FIXTURE machines='..#storage.units..' input_sets='..#keys..' eligible_technology_contracts='..eligible)
end)
script.on_nth_tick(60,function(e)
 if loaded then
  for i,u in ipairs(storage.units) do
   check(u.lab.valid and u.lab.direction==0,'saved fixed lab')
   if storage.saved then
    local old=storage.saved[i];local new=snapshot(u)
    check(same(old.inputs,new.inputs) and old.coal==new.coal,'saved research/fuel inventories')
    check(math.abs(old.remaining_fuel-new.remaining_fuel)<.1,'saved remaining fuel')
    check(old.research==new.research and old.target_researched==new.target_researched and math.abs(old.progress-new.progress)<1e-10,'saved research progress and unlock')
   end
  end
  if storage.saved_builder_output then check(storage.builder.valid and storage.builder.get_output_inventory().get_item_count('pondering-hovel')==storage.saved_builder_output,'saved actual building output') end
  log('PONDERING_HOVEL_V1_RELOAD_PASS complete='..tostring(storage.complete)..' stored_research='..tostring(storage.saved~=nil));loaded=false
 end
 if storage.frozen then return end
 local function state(n) for _,u in ipairs(storage.units) do if u.state==n then return u end end end
 local restart=state('stop-restart')
 if e.tick==1800 then check(restart.force.research_progress>0,'progress before stop');restart.lab.disabled_by_script=true;storage.stopped=snapshot(restart)
 elseif e.tick==1920 then check(math.abs(restart.force.research_progress-storage.stopped.progress)<1e-10 and same(inventory(restart),storage.stopped.inputs),'stopped research stable');restart.lab.disabled_by_script=false;log('PONDERING_HOVEL_V1_STOP_PASS')
 elseif e.tick==9000 then
  check(storage.builder.get_output_inventory().get_item_count('pondering-hovel')==1,'actual upgraded building crafted in workbench');check(storage.builder.get_inventory(defines.inventory.crafter_input).get_item_count('thinking-hut')==0 and storage.builder.get_inventory(defines.inventory.crafter_input).get_item_count('brick')==0,'building ingredients consumed')
  local covered={};local actual={}
  for _,u in ipairs(storage.units) do
   if u.state=='real-research' then
    check(progress(u),'real technology advanced '..u.technology);local inv=inventory(u)
    for _,i in ipairs(prototypes.technology[u.technology].research_unit_ingredients) do check(inv[i.name]<u.initial[i.name],'real research consumed '..i.name..' for '..u.technology);covered[i.name]=true end
    actual[#actual+1]=u.technology
   end
  end
  local count=0;for _,n in ipairs(prototypes.entity['pondering-hovel'].lab_inputs) do check(covered[n],'research input not exercised '..n);count=count+1 end
  check(state('no-fuel').force.research_progress==0,'no fuel blocks research');check(state('missing-meal').force.research_progress==0,'missing meal blocks research');check(not state('idle').force.current_research,'idle without research')
  check(state('completed-idle').force.technologies.beachpump.researched and not state('completed-idle').force.current_research,'completed real technology returns to idle')
  check(restart.force.technologies.beachpump.researched,'stopped research subsequently completed')
  state('no-fuel').lab.get_fuel_inventory().insert{name='coal',count=20};state('missing-meal').lab.get_inventory(defines.inventory.lab_input).insert{name='meal',count=20}
  check(restart.force.add_research('wood-basin'),'subsequent real research restart')
  storage.covered=count;storage.actual=actual;log('PONDERING_HOVEL_V1_ALL_INPUT_SETS_PASS '..helpers.table_to_json{tested_technologies=actual,distinct_input_sets=storage.sets,covered_input_items=count,eligible_technology_contracts=storage.eligible})
 elseif e.tick==10800 then
  check(state('no-fuel').force.research_progress>0,'refuel resumed research');check(state('missing-meal').force.research_progress>0,'missing ingredient resupply resumed research');check(restart.force.research_progress>0,'new research progressed')
  storage.complete=true;local report={passed=true,machines=#storage.units,distinct_native_research_input_sets=storage.sets,actual_technologies_tested=storage.actual,all_accepted_input_items_consumed=storage.covered,eligible_technology_contracts=storage.eligible,fuel_starvation_and_resupply=true,ingredient_starvation_and_resupply=true,idle_completed_technology_and_restart=true,script_deactivation_stop_restart=true,native_fixed_orientation=true,processing_recipes_and_output_blocking='not applicable: native lab research, no manufactured output or fluid connections',gameplay_overrides=false}
  report.construction_recipe_crafted_in_workbench=true
  helpers.write_file('pondering-hovel-v1/native-runtime.json',helpers.table_to_json(report),false);log('PONDERING_HOVEL_V1_NATIVE_PASS '..helpers.table_to_json(report))
 end
end)
remote.add_interface('pondering_hovel_proof',{
 layout=function() local units={};for i,u in ipairs(storage.units) do units[i]={state=u.state,technology=u.technology,position=u.position} end;return {units=units,machines=#units,complete=storage.complete} end,
 freeze=function() check(storage.complete,'freeze only after real operation');storage.frozen=true;for _,u in ipairs(storage.units) do u.lab.disabled_by_script=true end;storage.builder.disabled_by_script=true end,
 snapshot=function() check(storage.frozen,'snapshot only while frozen');storage.saved={};for i,u in ipairs(storage.units) do storage.saved[i]=snapshot(u) end;storage.saved_builder_output=storage.builder.get_output_inventory().get_item_count('pondering-hovel');return #storage.saved end
})
