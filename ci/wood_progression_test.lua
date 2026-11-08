-- Focused Lua unit tests for wood discovery and save migration.
-- Run from the repository root: lua ci/wood_progression_test.lua [mod-directory]
-- Lua game objects and events are mocked here. These tests do not substitute
-- for the separate Factorio engine fixtures that mine and craft real wood.
local source = (arg and arg[1]) or "tanks_for_bob_fork_1.8.101"
local checks = 0
local function test(name, run)
  run()
  checks = checks + 1
  print("WOOD_UNIT_PASS " .. name)
end

local declarations = {}
data = {extend = function(_, entries)
  for _, entry in ipairs(entries) do declarations[entry.name] = entry end
end}
dofile(source .. "/prototypes/technology/technology.lua")
local technology = assert(declarations["wood-spear"])

local event_names = {
  "on_player_mined_item", "on_player_crafted_item",
  "on_player_main_inventory_changed", "on_player_cursor_stack_changed",
  "on_player_created", "on_player_joined_game", "on_player_changed_force",
  "on_force_created", "on_force_reset", "on_forces_merged"
}
defines = {events = {}}
for _, name in ipairs(event_names) do defines.events[name] = name end
local handlers, lifecycle = {}, {}
script = {
  on_init = function(callback) lifecycle.init = callback end,
  on_configuration_changed = function(callback) lifecycle.configure = callback end,
  on_event = function(events, callback)
    if type(events) ~= "table" then events = {events} end
    for _, event in ipairs(events) do
      assert(not handlers[event], "Duplicate event registration: " .. event)
      handlers[event] = callback
    end
  end,
  on_nth_tick = function() error("Wood discovery must not poll every N ticks") end
}
local progression = dofile(source .. "/scripts/wood_progression.lua")
progression.register()

local function new_force(researched)
  local force = {
    valid = true,
    players = {},
    trigger_calls = 0,
    technologies = {
      ["wood-spear"] = {researched = researched or false, enabled = true},
      unrelated = {researched = true, enabled = false}
    },
    recipes = {
      ["wood-spear"] = {enabled = false},
      ["Sharp-stick"] = {enabled = true},
      ["unrelated-enabled"] = {enabled = true},
      ["unrelated-disabled"] = {enabled = false}
    }
  }
  force.script_trigger_research = function(name)
    assert(name == "wood-spear", "Unexpected technology completion")
    assert(not force.technologies[name].researched, "Repeated completion")
    force.trigger_calls = force.trigger_calls + 1
    force.technologies[name].researched = true
    -- Model the documented engine effect; use the real prototype's effects.
    for _, effect in ipairs(technology.effects) do
      assert(effect.type == "unlock-recipe")
      force.recipes[effect.recipe].enabled = true
    end
  end
  force.reset_technology_effects = function() error("Broad effect reset is forbidden") end
  force.reset_recipes = function() error("Broad recipe reset is forbidden") end
  return force
end

local function new_player(force, wood)
  local player = {valid = true, force = force, wood = wood or 0, inventory_reads = 0}
  player.cursor_stack = {valid_for_read = false}
  player.get_item_count = function(filter)
    assert(type(filter) == "table" and filter.name == "wood")
    assert(filter.quality == nil, "Discovery must accept every wood quality")
    player.inventory_reads = player.inventory_reads + 1
    return player.wood
  end
  force.players[#force.players + 1] = player
  return player
end

local function world(forces, players)
  game = {forces = forces, players = players or {}}
  game.get_player = function(index) return game.players[index] end
end

local function unchanged(force)
  assert(force.recipes["unrelated-enabled"].enabled)
  assert(not force.recipes["unrelated-disabled"].enabled)
  assert(force.technologies.unrelated.researched)
  assert(not force.technologies.unrelated.enabled)
end

test("root material technology unlocks ammunition without laboratory research", function()
  assert(technology.unit == nil)
  assert(technology.prerequisites == nil or next(technology.prerequisites) == nil)
  assert(technology.research_trigger.type == "scripted")
  assert(technology.research_trigger.trigger_description[1] == "tanks-for-bob-fork.acquire-wood")
  assert(#technology.effects == 1 and technology.effects[1].recipe == "Sharp-stick")
end)

test("registered lifecycle and acquisition callbacks use no periodic scan", function()
  assert(lifecycle.init == progression.on_init)
  assert(lifecycle.configure == progression.on_configuration_changed)
  for _, name in ipairs(event_names) do assert(type(handlers[name]) == "function", name) end
end)

test("fresh force has the weapon and waits for wood before ammunition", function()
  local force = new_force()
  world({force}, {new_player(force)})
  lifecycle.init()
  assert(force.recipes["wood-spear"].enabled)
  assert(not force.recipes["Sharp-stick"].enabled)
  assert(not force.technologies["wood-spear"].researched)
  assert(force.trigger_calls == 0)
  unchanged(force)
end)

test("crafting wood unlocks before its result reaches the inventory", function()
  local force, other = new_force(), new_force()
  local player = new_player(force)
  world({force, other}, {player})
  lifecycle.init()
  handlers.on_player_crafted_item{player_index = 1,
    item_stack = {valid_for_read = true, name = "wood", count = 1}}
  assert(player.wood == 0)
  assert(force.technologies["wood-spear"].researched and force.recipes["Sharp-stick"].enabled)
  assert(not other.technologies["wood-spear"].researched)
  handlers.on_player_crafted_item{player_index = 1,
    item_stack = {valid_for_read = true, name = "wood", count = 1}}
  assert(force.trigger_calls == 1)
end)

test("mined wood uses the plain count record and accepts any quality", function()
  local force = new_force()
  world({force}, {new_player(force)})
  lifecycle.init()
  handlers.on_player_mined_item{player_index = 1,
    item_stack = {name = "wood", count = 4, quality = "uncommon"}}
  assert(force.trigger_calls == 1 and force.recipes["Sharp-stick"].enabled)
end)

test("unrelated results and missing players do not research wood", function()
  local force = new_force()
  world({force}, {new_player(force)})
  lifecycle.init()
  handlers.on_player_mined_item{player_index = 1, item_stack = {name = "stone", count = 1}}
  handlers.on_player_mined_item{player_index = 1, item_stack = {name = "wood", count = 0}}
  handlers.on_player_crafted_item{player_index = 1,
    item_stack = {valid_for_read = true, name = "stone", count = 1}}
  handlers.on_player_crafted_item{player_index = 1, item_stack = {valid_for_read = false}}
  handlers.on_player_mined_item{player_index = 999, item_stack = {name = "wood", count = 1}}
  handlers.on_player_main_inventory_changed{player_index = 999}
  assert(force.trigger_calls == 0 and not force.recipes["Sharp-stick"].enabled)
end)

test("inventory transfers and cursor wood both unlock their own force", function()
  local first, second = new_force(), new_force()
  local a, b = new_player(first), new_player(second)
  world({first, second}, {a, b})
  lifecycle.init()
  a.wood = 1
  handlers.on_player_main_inventory_changed{player_index = 1}
  assert(first.trigger_calls == 1 and second.trigger_calls == 0)
  b.cursor_stack = {valid_for_read = true, name = "wood", count = 1}
  handlers.on_player_cursor_stack_changed{player_index = 2}
  assert(second.trigger_calls == 1)
end)

test("upgrade preserves researched technology and repairs only the weapon pair", function()
  local force = new_force(true)
  force.recipes["Sharp-stick"].enabled = false
  world({force}, {new_player(force)})
  lifecycle.configure()
  assert(force.technologies["wood-spear"].researched)
  assert(force.recipes["wood-spear"].enabled and force.recipes["Sharp-stick"].enabled)
  assert(force.trigger_calls == 0)
  unchanged(force)
end)

test("upgrade discovers existing wood including an offline player's cursor", function()
  local first, second = new_force(), new_force()
  local a, b = new_player(first, 3), new_player(second)
  a.connected, b.connected = false, false
  b.cursor_stack = {valid_for_read = true, name = "wood", count = 1}
  world({first, second}, {a, b})
  lifecycle.configure()
  assert(first.trigger_calls == 1 and second.trigger_calls == 1)
  assert(first.recipes["wood-spear"].enabled and second.recipes["wood-spear"].enabled)
  unchanged(first)
  unchanged(second)
end)

test("upgrade removes old default ammunition access until wood is obtained", function()
  local force = new_force()
  world({force}, {new_player(force)})
  assert(force.recipes["Sharp-stick"].enabled)
  lifecycle.configure()
  assert(force.recipes["wood-spear"].enabled and not force.recipes["Sharp-stick"].enabled)
  assert(not force.technologies["wood-spear"].researched)
  unchanged(force)
end)

test("completed and scenario-disabled technologies are not retriggered", function()
  local completed, disabled = new_force(true), new_force()
  disabled.technologies["wood-spear"].enabled = false
  local a, b = new_player(completed, 2), new_player(disabled, 2)
  world({completed, disabled}, {a, b})
  handlers.on_player_main_inventory_changed{player_index = 1}
  handlers.on_player_main_inventory_changed{player_index = 2}
  handlers.on_player_mined_item{player_index = 2, item_stack = {name = "wood", count = 1}}
  assert(completed.trigger_calls == 0 and disabled.trigger_calls == 0)
  assert(a.inventory_reads == 0 and b.inventory_reads == 0)
end)

test("new forces and force resets initialize the pair and inspect held wood", function()
  local force = new_force()
  local player = new_player(force)
  world({force}, {player})
  handlers.on_force_created{force = force}
  assert(force.recipes["wood-spear"].enabled and not force.recipes["Sharp-stick"].enabled)
  player.wood = 1
  handlers.on_force_reset{force = force}
  assert(force.trigger_calls == 1 and force.recipes["Sharp-stick"].enabled)
  unchanged(force)
end)

test("a player transferring forces teaches the receiving force only", function()
  local old, receiving = new_force(), new_force()
  local player = new_player(old, 1)
  world({old, receiving}, {player})
  player.force = receiving
  receiving.players = {player}
  old.players = {}
  handlers.on_player_changed_force{player_index = 1, force = old}
  assert(receiving.trigger_calls == 1 and old.trigger_calls == 0)
end)

test("force merge preserves existing research and recognizes transferred wood", function()
  local force = new_force()
  world({force}, {new_player(force, 1)})
  handlers.on_forces_merged{destination = force}
  assert(force.recipes["wood-spear"].enabled and force.recipes["Sharp-stick"].enabled)
  assert(force.trigger_calls == 1)
  handlers.on_forces_merged{destination = force}
  assert(force.trigger_calls == 1)
  unchanged(force)
end)

print("WOOD_UNIT_PASS total=" .. checks .. " scope=mocked-Lua-events-and-migration")
