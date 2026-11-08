-- Narrow native checks for the progression decisions following the first audit.
-- Prerequisites, lab supplies and machine inputs are seeded; production is real.
local fixture = {}
local function fluid_amount(entity, name)
  return entity.get_fluid_count(name)
end
local function fuel(entity)
  local inventory = entity.get_fuel_inventory()
  if inventory then inventory.insert{name="wood", count=50} end
end
local function machine(surface, force, name, position, direction, check)
  local entity = surface.create_entity{name=name, position=position, direction=direction, force=force}
  check(name .. " recovery fixture created", entity and entity.valid)
  fuel(entity)
  return entity
end
local function select_recipe(entity, name, check)
  check(name .. " unlocked for fixture force", entity.force.recipes[name].enabled)
  entity.set_recipe(name)
  local selected = entity.get_recipe()
  check(name .. " selected on " .. entity.name, selected and selected.name == name)
end
function fixture.initialize(surface, check)
  local force = game.create_force("fixture_recovery")
  local state = {force=force, carbon={}, oil={}, labs={}, started=false}
  storage.decisions = state
  check("redundant stone-tools technology removed", not force.technologies["stone-tools"])
  check("stone tools remain a starting recipe", force.recipes["stone-tools"].enabled)
  check("recovery recipes await mid-tier research", not force.recipes["fish-carbonization"].enabled and not force.recipes["fish-oil-extraction"].enabled)
  check("ash recovery retains its existing industrial gate", not force.recipes["fish-ash-processing"].enabled)
  force.technologies["fish-pond"].researched = true
  force.technologies.meal.researched = true
  check("mid-tier recovery research queues", force.add_research("fish-resource-recovery"))
  for index=1,4 do
    local lab = machine(surface, force, "thinking-hut", {-42+index*8,38}, defines.direction.north, check)
    local inventory = lab.get_inventory(defines.inventory.lab_input)
    inventory.insert{name="Seared-fish", count=10}
    inventory.insert{name="meal", count=10}
    state.labs[#state.labs+1] = lab
  end
  for index,name in ipairs({"campfire","cooking-fire"}) do
    state.carbon[#state.carbon+1] = machine(surface, force, name, {-38+index*8,-24}, defines.direction.north, check)
  end
  state.basic_cooking = machine(surface, force, "cooking-fire", {28,-24}, defines.direction.north, check)
  select_recipe(state.basic_cooking, "Seared-fish", check)
  state.basic_cooking.get_inventory(defines.inventory.crafter_input).insert{name="raw-fish",count=20}
  state.ash_cooking = machine(surface, force, "cooking-fire", {28,-16}, defines.direction.north, check)
  local directions = {
    {name="north", value=defines.direction.north, outlet={0,1}},
    {name="east", value=defines.direction.east, outlet={-1,0}},
    {name="south", value=defines.direction.south, outlet={0,-1}},
    {name="west", value=defines.direction.west, outlet={1,0}}
  }
  for index,direction in ipairs(directions) do
    local position = {-16+index*8,-24}
    local bench = machine(surface, force, "workbench", position, direction.value, check)
    local pipe = surface.create_entity{name="pipe",position={position[1]+direction.outlet[1],position[2]+direction.outlet[2]},force=force}
    check(direction.name .. " workbench outlet pipe created", pipe and pipe.valid)
    state.oil[#state.oil+1] = {entity=bench,pipe=pipe,direction=direction.name,
      requested_direction=direction.value,placed_direction=bench.direction}
  end
  local pumping = game.create_force("fixture_pumpjack")
  pumping.technologies["oil-gathering"].researched = true
  local resource = surface.create_entity{name="crude-oil",position={30,24},amount=100000}
  check("native crude oil resource created", resource and resource.valid)
  state.pumpjack = surface.create_entity{name="pumpjack",position={30,24},force=pumping}
  check("native pumpjack created", state.pumpjack and state.pumpjack.valid)
  state.pumpjack.energy = 10000000
end
function fixture.update(check)
  local state = storage.decisions
  state.pumpjack.energy = 10000000
  if state.force.technologies["fish-resource-recovery"].researched and not state.started then
    check("custom burner labs completed resource research", true)
    state.research_tick = game.tick
    for _,entity in ipairs(state.carbon) do
      select_recipe(entity,"fish-carbonization",check)
      entity.get_inventory(defines.inventory.crafter_input).insert{name="raw-fish",count=80}
    end
    for _,test in ipairs(state.oil) do
      select_recipe(test.entity,"fish-oil-extraction",check)
      -- Assemblers with inactive fluid boxes may normalize their placement
      -- direction before a fluid recipe is chosen. Rotate the configured
      -- machine, as a player would after selecting its recipe.
      test.direction_after_recipe = test.entity.direction
      test.entity.direction = test.requested_direction
      check(test.direction .. " workbench can rotate after recipe selection",
        test.entity.rotatable and test.entity.direction==test.requested_direction,
        {placed_direction=test.placed_direction,after_recipe=test.direction_after_recipe,configured_direction=test.entity.direction})
      test.entity.get_inventory(defines.inventory.crafter_input).insert{name="raw-fish",count=100}
    end
    state.started = true
  end
  if state.started and not state.oil_gate_checked and fluid_amount(state.oil[1].pipe,"crude-oil") > 0 then
    check("workbench oil does not bypass Oil Gathering", not state.force.technologies["oil-processing"].researched)
    check("vanilla Oil Gathering prerequisite retained", state.force.technologies["oil-processing"].prerequisites["oil-gathering"] ~= nil)
    state.force.technologies["oil-gathering"].researched = true
    state.oil_gate_checked = true
  end
  local ash_source = state.carbon[2].get_output_inventory()
  if not state.ash_started and ash_source.get_item_count("fish-ash") >= 3 then
    check("mid-tier fish recovery does not grant advanced ash processing",not state.force.recipes["fish-ash-processing"].enabled)
    state.force.technologies["bio-reactive-processing"].researched = true
    select_recipe(state.ash_cooking,"fish-ash-processing",check)
    local removed = ash_source.remove{name="fish-ash",count=3}
    check("manufactured ash moved into mineral recovery", removed==3 and state.ash_cooking.get_inventory(defines.inventory.crafter_input).insert{name="fish-ash",count=removed}==3)
    state.ash_started = true
  end
end
function fixture.finish(check)
  local state = storage.decisions
  check("mid-tier recovery research completed using its real lab inputs", state.started and state.force.technologies["fish-resource-recovery"].researched)
  check("Cooking Fire still cooks ordinary fish without steam", state.basic_cooking.get_output_inventory().get_item_count("Seared-fish") > 0)
  local report = {research_completed_tick=state.research_tick,carbon={},oil={}}
  for index,entity in ipairs(state.carbon) do
    local inventory = entity.get_output_inventory()
    local coal = inventory.get_item_count("coal")
    local ash = inventory.get_item_count("fish-ash") + ((index==2 and state.ash_started) and 3 or 0)
    check(entity.name .. " manufactured actual coal and ash with wood fuel", coal>0 and ash>0,{coal=coal,ash=ash})
    report.carbon[#report.carbon+1] = {machine=entity.name,coal=coal,ash=ash,crafts=entity.products_finished}
  end
  for _,test in ipairs(state.oil) do
    local amount = fluid_amount(test.pipe,"crude-oil")
    check(test.direction .. " workbench exports manufactured crude oil to pipe", amount>0,{pipe_crude_oil=amount,crafts=test.entity.products_finished,direction=test.entity.direction,placed_direction=test.placed_direction,after_recipe=test.direction_after_recipe})
    report.oil[#report.oil+1] = {direction=test.direction,pipe_crude_oil=amount,crafts=test.entity.products_finished}
  end
  check("fish oil completes Oil Processing after Oil Gathering", state.oil_gate_checked and state.force.technologies["oil-processing"].researched)
  local pumped = fluid_amount(state.pumpjack,"crude-oil")
  check("ordinary pumpjack still produces crude oil", pumped>0,{crude_oil=pumped})
  check("ordinary pumpjack still completes Oil Processing", state.pumpjack.force.technologies["oil-processing"].researched)
  local dust = state.ash_cooking.get_output_inventory().get_item_count("calcified-bone-dust")
  check("actual recovered ash becomes useful mineral material", dust>0,{calcified_bone_dust=dust})
  report.pumpjack_crude_oil = pumped
  report.ash_recovered_as_bone_dust = dust
  return report
end
local legacy_cases = {
  {name="legacy_poison_ready",old="new-munitions",new="poison-mine-ammunition",recipe="minepack-poison",parents={"modular-tank-research3","land-mine"},preserve=true},
  {name="legacy_poison_no_mine",old="new-munitions",new="poison-mine-ammunition",recipe="minepack-poison",parents={"modular-tank-research3"},preserve=false},
  {name="legacy_poison_no_vehicle",old="new-munitions",new="poison-mine-ammunition",recipe="minepack-poison",parents={"land-mine"},preserve=false},
  {name="legacy_wmd_ready",old="super-tank-research2",new="wmd-artillery-ammunition",recipe="wmdartillery-ammo",parents={"artillery"},preserve=true},
  {name="legacy_wmd_no_artillery",old="super-tank-research2",new="wmd-artillery-ammunition",recipe="wmdartillery-ammo",parents={},preserve=false}
}
function fixture.seed_legacy(check)
  storage.legacy_decisions = {}
  for _,case in ipairs(legacy_cases) do
    local force = game.create_force(case.name)
    force.technologies[case.old].researched = true
    for _,parent in ipairs(case.parents) do force.technologies[parent].researched = true end
    check(case.name .. " old shared ammunition unlock seeded", force.recipes[case.recipe].enabled)
  end
  local force = game.forces.legacy_poison_ready
  force.technologies["stone-tools"].researched = true
  force.technologies["wood-basin"].researched = true
  local bench = game.surfaces[1].create_entity{name="workbench",position={-10,0},force=force}
  check("historical workbench created", bench and bench.valid)
  bench.set_recipe("wood-basin")
  local inventory = bench.get_inventory(defines.inventory.crafter_input)
  local contents = {}
  for _,ingredient in pairs(force.recipes["wood-basin"].ingredients) do
    assert(ingredient.type=="item")
    local inserted = inventory.insert{name=ingredient.name,count=ingredient.amount*2}
    contents[ingredient.name] = inserted
  end
  storage.legacy_decisions.bench = bench
  storage.legacy_decisions.contents = contents
end
function fixture.verify_migration(check)
  local result = {}
  for _,case in ipairs(legacy_cases) do
    local force = game.forces[case.name]
    local tech = force.technologies[case.new]
    local state = {researched=tech and tech.researched,recipe=force.recipes[case.recipe].enabled}
    check(case.name .. " obeys the new prerequisite boundary", state.researched==case.preserve and state.recipe==case.preserve,state)
    result[case.name] = state
  end
  local force = game.forces.legacy_poison_ready
  check("obsolete researched stone-tools node removed safely", not force.technologies["stone-tools"] and force.recipes["stone-tools"].enabled)
  local bench = storage.legacy_decisions.bench
  local recipe = bench and bench.valid and bench.get_recipe()
  check("existing workbench keeps ordinary crafting recipe", recipe and recipe.name=="wood-basin")
  for name,count in pairs(storage.legacy_decisions.contents) do
    check("existing workbench keeps " .. name,bench.get_inventory(defines.inventory.crafter_input).get_item_count(name)==count)
  end
  force.technologies["fish-resource-recovery"].researched = true
  bench.set_recipe("fish-oil-extraction")
  check("existing workbench receives its oil output",bench.get_fluid_capacity(1)>0)
  return result
end
return fixture
