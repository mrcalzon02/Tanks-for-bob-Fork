-- Root material discovery for the starting wooden weapon. The technology ID is
-- retained so saves that already researched it keep their ammunition unlock.
local wood_progression = {}
local technology_name = "wood-spear"

local function pending_technology(force)
  if not (force and force.valid) then return nil end
  local technology = force.technologies[technology_name]
  if technology and technology.enabled and not technology.researched then
    return technology
  end
end

local function acquire_wood(force)
  if pending_technology(force) then
    force.script_trigger_research(technology_name)
  end
end

local function check_player(player)
  if not (player and player.valid and pending_technology(player.force)) then return end
  -- An ItemFilter without a quality restriction accepts wood of any quality.
  local cursor = player.cursor_stack
  if player.get_item_count({name = "wood"}) > 0
      or (cursor and cursor.valid_for_read and cursor.name == "wood") then
    acquire_wood(player.force)
  end
end

local function synchronize_force(force)
  if not (force and force.valid) then return end
  local weapon = force.recipes["wood-spear"]
  if weapon then weapon.enabled = true end
  local technology = force.technologies[technology_name]
  local ammunition = force.recipes["Sharp-stick"]
  if technology and ammunition then
    -- Only these two recipes need migration. Resetting all technology effects
    -- would discard unrelated recipe overrides from scenarios or other mods.
    ammunition.enabled = technology.researched
  end
end

function wood_progression.on_init()
  for _, force in pairs(game.forces) do synchronize_force(force) end
  -- Includes offline players when this mod is added to an existing save.
  for _, player in pairs(game.players) do check_player(player) end
end

function wood_progression.on_configuration_changed()
  wood_progression.on_init()
end

function wood_progression.on_player_mined_item(event)
  -- Mining supplies ItemWithQualityCount, not a LuaItemStack.
  local stack = event.item_stack
  if stack and stack.name == "wood" and stack.count > 0 then
    local player = game.get_player(event.player_index)
    if player and player.valid then acquire_wood(player.force) end
  end
end

function wood_progression.on_player_crafted_item(event)
  -- This event precedes inventory insertion, so inspect its result directly.
  local stack = event.item_stack
  if stack and stack.valid_for_read and stack.name == "wood" then
    local player = game.get_player(event.player_index)
    if player and player.valid then acquire_wood(player.force) end
  end
end

function wood_progression.on_player_inventory_changed(event)
  check_player(game.get_player(event.player_index))
end

function wood_progression.on_force_created_or_reset(event)
  synchronize_force(event.force)
  for _, player in pairs(event.force.players) do check_player(player) end
end

function wood_progression.on_forces_merged(event)
  synchronize_force(event.destination)
  for _, player in pairs(event.destination.players) do check_player(player) end
end

function wood_progression.register()
  script.on_init(wood_progression.on_init)
  script.on_configuration_changed(wood_progression.on_configuration_changed)
  script.on_event(defines.events.on_player_mined_item, wood_progression.on_player_mined_item)
  script.on_event(defines.events.on_player_crafted_item, wood_progression.on_player_crafted_item)
  script.on_event({
    defines.events.on_player_main_inventory_changed,
    defines.events.on_player_cursor_stack_changed,
    defines.events.on_player_created,
    defines.events.on_player_joined_game,
    defines.events.on_player_changed_force
  }, wood_progression.on_player_inventory_changed)
  script.on_event({defines.events.on_force_created, defines.events.on_force_reset},
    wood_progression.on_force_created_or_reset)
  script.on_event(defines.events.on_forces_merged, wood_progression.on_forces_merged)
end

return wood_progression
