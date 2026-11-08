-- Runs as a separate diagnostic mod, so production event handlers stay intact.
-- Requires Factorio 2.1.24 native --test-scenario / --test-save support.
local expected = require("fixture_config")
local decisions = require("progression_decisions")
local mode = script.test_arg or expected.fixture_mode
local PREFIX = "TANKS-CI PROGRESSION_RUNTIME "
local function flush(complete)
  storage.report.complete = complete
  storage.report.tick = game.tick
  helpers.write_file("progression-runtime/" .. mode .. ".json",
    helpers.table_to_json(storage.report), false)
end
local function check(name, condition, detail)
  storage.report.checks[#storage.report.checks+1] = {name=name, passed=not not condition, detail=detail}
  if not condition then
    flush(false)
    error(PREFIX .. "FAIL " .. name .. " " .. helpers.table_to_json(detail or {}))
  end
  log(PREFIX .. "PASS " .. name)
end
local function new_report()
  storage.report = {mode=mode, complete=false, checks={}, active_mods=script.active_mods,
    scope="Native player mining and handcrafting events, plus seeded kiln production and seeded historical-save migration; not a full progression playthrough."}
end
local function force_state(force)
  return {weapon=force.recipes["wood-spear"].enabled, ammunition=force.recipes["Sharp-stick"].enabled,
    researched=force.technologies["wood-spear"].researched,
    unrelated_recipe=force.recipes["iron-gear-wheel"].enabled,
    unrelated_research=force.technologies.automation.researched}
end
local function wood_count(player, quality)
  return player.get_item_count({name="wood", quality=quality})
end
local function player_ready()
  local player = game.players[1]
  check("native test player exists", player and player.valid and player.is_player())
  local surface = game.surfaces[1]
  surface.request_to_generate_chunks({0,0}, 2)
  surface.force_generate_chunk_requests()
  for _, ent in pairs(surface.find_entities_filtered{area={{-48,-48},{48,48}}}) do
    if ent.type ~= "character" then ent.destroy() end
  end
  local tiles = {}
  for x=-48,48 do for y=-48,48 do tiles[#tiles+1]={name="grass-1",position={x,y}} end end
  surface.set_tiles(tiles, true)
  player.teleport({0,0}, surface)
  if not player.character then check("native test character created", player.create_character()) end
  check("native character attached", player.character and player.character.valid)
  player.clear_items_inside()
  return player, surface
end
local function is_discovered(force)
  return force.technologies["wood-spear"].researched and force.recipes["Sharp-stick"].enabled
end
local function machine_refill(test)
  local inv = test.entity.get_inventory(defines.inventory.crafter_input)
  for _, ingredient in pairs(test.entity.force.recipes[test.recipe].ingredients) do
    assert(ingredient.type == "item")
    inv.insert{name=ingredient.name,count=10000}
  end
  test.entity.get_fuel_inventory().insert{name="coal",count=10000}
end
local function machine_drain(test)
  local inv = test.entity.get_output_inventory()
  for i=1,#inv do
    local stack = inv[i]
    if stack.valid_for_read then
      test.products[stack.name] = (test.products[stack.name] or 0) + stack.count
    end
  end
  inv.clear()
end
local function initialize_machines(surface)
  local force = game.create_force("fixture_industry")
  storage.machines = {}
  for index, name in ipairs({"saline-particulate", "bioceramic-grit"}) do
    -- Enables only the fixture targets; it does not claim their technology
    -- prerequisites or ingredients were acquired through progression.
    force.recipes[name].enabled = true
    local ent = surface.create_entity{name="pit-kiln",position={-16+index*10,24},force=force}
    check(name .. " kiln created", ent and ent.valid)
    ent.set_recipe(name)
    local selected = ent.get_recipe()
    check(name .. " selectable in actual kiln", selected and selected.name == name)
    local test = {entity=ent,recipe=name,products={}}
    machine_refill(test)
    storage.machines[#storage.machines+1] = test
  end
end
local function initialize_fresh()
  new_report()
  local player, surface = player_ready()
  storage.player = player.index
  storage.native_events = {mined_wood=0,crafted_wood=0,crafted_weapon=0}
  storage.mining_force = game.create_force("fixture_mining")
  storage.crafting_force = game.create_force("fixture_crafting")
  storage.quality_force = game.create_force("fixture_quality")
  for _, force in ipairs({game.forces.player,storage.mining_force,storage.crafting_force,storage.quality_force}) do
    local state = force_state(force)
    check(force.name .. " starting weapon available", state.weapon, state)
    check(force.name .. " ammunition awaits wood", not state.ammunition and not state.researched, state)
  end
  local recipe = player.force.recipes["wood-spear"]
  check("starting weapon is handcraftable category", #recipe.categories == 1 and recipe.categories[1] == "crafting", recipe.categories)
  local tech = player.force.technologies["wood-spear"].prototype
  check("wood discovery is root scripted technology", next(tech.prerequisites) == nil and tech.research_trigger and tech.research_trigger.type == "scripted")
  player.force = storage.mining_force
  local tree = surface.create_entity{name="tree-01",position={3,0}}
  check("real tree created", tree and tree.valid)
  check("native player mined real tree", player.mine_entity(tree))
  storage.phase = "mined"
  initialize_machines(surface)
  decisions.initialize(surface, check)
end
local function fresh_tick()
  if not storage.phase then initialize_fresh() return end
  local player = game.get_player(storage.player)
  if storage.phase == "mined" then
    check("native mining event carried wood", storage.native_events.mined_wood > 0, storage.native_events)
    check("harvesting wood researched ammunition", wood_count(player)>0 and is_discovered(storage.mining_force), force_state(storage.mining_force))
    check("starting weapon queues in player hands", player.begin_crafting{count=1,recipe="wood-spear"} == 1)
    storage.phase = "weapon_crafting"
  elseif storage.phase == "weapon_crafting" and storage.native_events.crafted_weapon > 0 then
    check("starting weapon actually hand-crafted", player.get_item_count("wood-spear")>0)
    player.clear_items_inside()
    player.force = storage.crafting_force
    check("driftwood force remains undiscovered", not is_discovered(storage.crafting_force) and wood_count(player)==0)
    check("native driftwood handcraft queues", player.begin_crafting{count=1,recipe="desperation-scrape-driftwood"}==1)
    storage.phase = "driftwood_crafting"
  elseif storage.phase == "driftwood_crafting" and storage.native_events.crafted_wood > 0 then
    check("actual driftwood craft produced wood", wood_count(player)>0)
    check("native crafting discovered ammunition", is_discovered(storage.crafting_force), force_state(storage.crafting_force))
    player.clear_items_inside()
    player.force = storage.quality_force
    check("quality force remains undiscovered", not is_discovered(storage.quality_force))
    if prototypes.quality.rare then
      check("rare wood inserted into actual player", player.insert{name="wood",quality="rare",count=1}==1)
      check("name-only item filter counts rare wood", wood_count(player)==1 and wood_count(player,"rare")==1)
      storage.phase="quality_wood"
    else
      storage.report.quality_case="Not applicable: quality prototype absent in base-only profile"
      storage.phase="player_complete"
    end
  elseif storage.phase == "quality_wood" then
    check("quality wood inventory event discovers ammunition", is_discovered(storage.quality_force), force_state(storage.quality_force))
    storage.phase="player_complete"
  end
  if game.tick % 120 == 0 then
    for _, test in ipairs(storage.machines) do machine_drain(test); machine_refill(test) end
    decisions.update(check)
  end
  if game.tick >= 12000 then
    check("native player acquisition sequence completed", storage.phase=="player_complete", {phase=storage.phase})
    storage.report.native_events=storage.native_events
    storage.report.machine_results={}
    for _, test in ipairs(storage.machines) do
      machine_drain(test)
      local selected=test.entity.get_recipe()
      check(test.recipe .. " actually manufactured", selected and selected.name==test.recipe and (test.products[test.recipe] or 0)>0, test.products)
      storage.report.machine_results[#storage.report.machine_results+1]={recipe=test.recipe,products=test.products,crafts=test.entity.products_finished}
    end
    storage.report.progression_decisions = decisions.finish(check)
    flush(true)
    log(PREFIX .. "FRESH_PASS")
    script.finish_test(true)
  end
end
local function initialize_legacy_save()
  new_report()
  check("legacy save created with supplied previous package", script.active_mods.tanks_for_bob_fork==expected.legacy_version)
  local researched=game.create_force("legacy_researched")
  local existing=game.create_force("legacy_existing_wood")
  local empty=game.create_force("legacy_empty")
  local partial=game.create_force("legacy_in_progress")
  researched.technologies["wood-spear"].researched=true
  researched.technologies.automation.researched=true
  local lab_wood_research = partial.technologies["wood-spear"].prototype.research_trigger == nil
  if lab_wood_research then
    partial.technologies["growing-plot"].researched=true
    check("historical spear research queued",partial.add_research("wood-spear"))
    partial.research_progress=0.4
  end
  for _, force in ipairs({researched,existing,empty,partial}) do force.recipes["iron-gear-wheel"].enabled=false end
  local surface=game.surfaces[1]
  surface.request_to_generate_chunks({0,0},1)
  surface.force_generate_chunk_requests()
  local tiles={}
  for x=-4,4 do for y=-4,4 do tiles[#tiles+1]={name="grass-1",position={x,y}} end end
  surface.set_tiles(tiles,true)
  for _, entity in pairs(surface.find_entities_filtered{area={{-4,-4},{4,4}}}) do entity.destroy() end
  local character=surface.create_entity{name="character",position={0,0},force=existing}
  check("historical character created",character and character.valid)
  check("historical wood inventory seeded",character.insert{name="wood",count=3}==3)
  storage.legacy_character=character
  storage.legacy_snapshot={version=script.active_mods.tanks_for_bob_fork,wood=wood_count(character),
    researched=force_state(researched),existing=force_state(existing),empty=force_state(empty),
    in_progress=force_state(partial),research_queue_head=partial.current_research and partial.current_research.name or false,
    research_progress=partial.research_progress,lab_wood_research=lab_wood_research}
  check("legacy researched state seeded",storage.legacy_snapshot.researched.researched and storage.legacy_snapshot.researched.ammunition)
  local empty_state = storage.legacy_snapshot.empty
  check("legacy unresearched state reproduced",not empty_state.researched and empty_state.ammunition==lab_wood_research and empty_state.weapon~=lab_wood_research)
  if lab_wood_research then
    check("legacy partial research state reproduced",storage.legacy_snapshot.research_queue_head=="wood-spear" and storage.legacy_snapshot.research_progress==0.4)
  end
  decisions.seed_legacy(check)
  storage.report.legacy_snapshot=storage.legacy_snapshot
  storage.report.saved_player_limitation="The normal headless converter has no player. Its real saved character inventory is attached to the native test player on joining the upgraded save; offline-player configuration-time discovery is not claimed."
  flush(true)
  log(PREFIX .. "LEGACY_SAVE_PASS")
end
local function migration_tick()
  if storage.migration_done then return end
  new_report()
  check("loaded saved historical state",storage.legacy_snapshot and storage.legacy_snapshot.version==expected.legacy_version)
  check("upgraded to corrected package",script.active_mods.tanks_for_bob_fork==expected.target_version)
  local change=storage.configuration_change and storage.configuration_change.mod_changes and storage.configuration_change.mod_changes.tanks_for_bob_fork
  check("real configuration change observed",change and change.old_version==expected.legacy_version and change.new_version==expected.target_version,change)
  local researched=game.forces.legacy_researched
  local existing=game.forces.legacy_existing_wood
  local empty=game.forces.legacy_empty
  local partial=game.forces.legacy_in_progress
  for _, force in ipairs({researched,existing,empty,partial}) do
    check(force.name .. " default weapon available after migration",force.recipes["wood-spear"].enabled)
  end
  check("researched ammunition preserved",is_discovered(researched),force_state(researched))
  check("unrelated research preserved",researched.technologies.automation.researched)
  local player=game.players[1]
  check("native player attached saved character",player and player.character==storage.legacy_character)
  check("existing wood inventory preserved",wood_count(player)==storage.legacy_snapshot.wood,{before=storage.legacy_snapshot.wood,after=wood_count(player)})
  check("saved wood discovered on native player joining",is_discovered(existing),force_state(existing))
  check("empty unresearched force remains gated",not empty.technologies["wood-spear"].researched and not empty.recipes["Sharp-stick"].enabled,force_state(empty))
  check("additional unresearched force remains gated",not is_discovered(partial) and partial.recipes["wood-spear"].enabled,force_state(partial))
  if storage.legacy_snapshot.lab_wood_research then
    check("old lab research leaves the queue",not partial.current_research or partial.current_research.name~="wood-spear",{current=partial.current_research and partial.current_research.name or false})
  end
  storage.report.progression_decisions = decisions.verify_migration(check)
  storage.report.engine_recipe_reset_note="Factorio reapplies recipe effects before configuration handlers during prototype migration. Unrelated enabled-state overrides are observed, not promised preserved by this fixture."
  storage.report.before=storage.legacy_snapshot
  storage.report.after={researched=force_state(researched),existing=force_state(existing),empty=force_state(empty),in_progress=force_state(partial)}
  storage.report.configuration_change=change
  storage.report.before_player_join=storage.before_player_join
  storage.report.saved_player_limitation="Historical wood was serialized in a real character inventory and discovered when the native test player attached on join. Offline-player on_configuration_changed discovery remains unit-tested, not demonstrated by this native saved-map fixture."
  storage.migration_done=true
  flush(true)
  log(PREFIX .. "MIGRATION_PASS")
  script.finish_test(true)
end
script.on_init(function()
  storage.phase=nil
  if mode=="seed-legacy" then initialize_legacy_save() end
end)
script.on_configuration_changed(function(event)
  storage.configuration_change=event
  if game.forces.legacy_existing_wood then
    storage.before_player_join={players=#game.players,existing=force_state(game.forces.legacy_existing_wood)}
  end
end)
script.on_event(defines.events.on_player_mined_item,function(event)
  if storage.native_events and event.item_stack.name=="wood" then
    storage.native_events.mined_wood=storage.native_events.mined_wood+event.item_stack.count
    storage.native_events.mined_payload={name=event.item_stack.name,count=event.item_stack.count,player_index=event.player_index}
  end
end)
script.on_event(defines.events.on_player_crafted_item,function(event)
  if not storage.native_events then return end
  if event.recipe.name=="wood-spear" then storage.native_events.crafted_weapon=storage.native_events.crafted_weapon+1 end
  if event.item_stack.valid_for_read and event.item_stack.name=="wood" then
    storage.native_events.crafted_wood=storage.native_events.crafted_wood+event.item_stack.count
    storage.native_events.crafted_payload={recipe=event.recipe.name,name=event.item_stack.name,count=event.item_stack.count,
      player_index=event.player_index,valid_for_read=event.item_stack.valid_for_read,
      research_during_crafted_event=game.get_player(event.player_index).force.technologies["wood-spear"].researched}
  end
end)
script.on_event(defines.events.on_tick,function()
  if mode=="fresh" then fresh_tick()
  elseif mode=="seed-legacy" then return
  elseif mode=="migration" then migration_tick()
  else error(PREFIX .. "unknown --test-arg " .. tostring(mode)) end
end)
