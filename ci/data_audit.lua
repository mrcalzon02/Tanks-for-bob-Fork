-- CI-only data-stage audit; installed in disposable test mod, not released.
local recipes = data.raw.recipe or {}
local technologies = data.raw.technology or {}
local expected = require("ci_profile")
local manifest = require("ci_manifest")
local failures, warnings = {}, {}
local function fail(msg) failures[#failures + 1] = msg end
local function warn(msg) warnings[#warnings + 1] = msg end
for mod_name in pairs(mods) do
  if mod_name ~= "core" and mod_name ~= "tanks_for_bob_fork" and not expected[mod_name] then
    fail("Unexpected mod loaded in data stage: " .. mod_name)
  end
end
for mod_name in pairs(expected) do
  if not mods[mod_name] then fail("Expected official mod not loaded: " .. mod_name) end
end

local vehicles = {
  "flame-tank", "auto-tank", "nade-tank", "flame-tank-wlsk",
  "auto-tank-wlsk", "nade-tank-wlsk", "mine-tank", "rocket-tank",
  "super-tank", "super-tank-alternate", "super-tank-wmd", "car-flamer"
}
for _, name in ipairs(vehicles) do
  if not recipes[name] then fail("Missing required tank recipe: " .. name) end
  if not (data.raw.car or {})[name] then fail("Missing required tank entity: " .. name) end
  if not (data.raw.item or {})[name] then
    warn("Tank entity lacks matching plain item: " .. name)
  end
end

local unlocked, unlock_count, prereq_edges, tech_count = {}, 0, 0, 0
for name, technology in pairs(technologies) do
  tech_count = tech_count + 1
  for _, effect in pairs(technology.effects or {}) do
    if effect.type == "unlock-recipe" then
      unlock_count = unlock_count + 1
      if not recipes[effect.recipe] then
        fail("Technology " .. name .. " unlocks missing recipe " .. tostring(effect.recipe))
      end
      unlocked[effect.recipe] = true
    end
  end
  for _, prerequisite in pairs(technology.prerequisites or {}) do
    prereq_edges = prereq_edges + 1
    if not technologies[prerequisite] then
      fail("Technology " .. name .. " requires missing " .. tostring(prerequisite))
    end
  end
end

-- Explicitly confirm the full source declaration inventory is registered.
local manifest_recipe_count, manifest_tech_count, manifest_missing_unlocks = 0, 0, 0
for name in pairs(manifest.recipes) do
  manifest_recipe_count = manifest_recipe_count + 1
  local recipe = recipes[name]
  if not recipe then
    fail("Declared mod recipe is absent from data.raw.recipe: " .. name)
  elseif recipe.enabled == false and not unlocked[name] then
    manifest_missing_unlocks = manifest_missing_unlocks + 1
    warn("Declared mod recipe is disabled without a technology unlock: " .. name)
  end
end
for name in pairs(manifest.technologies) do
  manifest_tech_count = manifest_tech_count + 1
  if not technologies[name] then
    fail("Declared mod technology is absent from data.raw.technology: " .. name)
  end
end

local visiting, explored = {}, {}
local function walk_tech(name)
  if visiting[name] then
    fail("Cyclic technology prerequisite graph at " .. name)
    return
  end
  if explored[name] or not technologies[name] then return end
  visiting[name] = true
  for _, required in pairs(technologies[name].prerequisites or {}) do
    walk_tech(required)
  end
  visiting[name] = nil
  explored[name] = true
end
for name in pairs(manifest.technologies) do walk_tech(name) end

local producers = {}
for _, kind in ipairs({"assembling-machine", "furnace", "rocket-silo"}) do
  for _, prototype in pairs(data.raw[kind] or {}) do
    for _, category in pairs(prototype.crafting_categories or {}) do
      producers[category] = true
    end
  end
end
local recipes_without_unlock, no_machine, tank_recipes, tank_missing_unlock = 0, 0, 0, 0
local category_count = {}
for name, recipe in pairs(recipes) do
  -- Factorio 2.1 permits several categories. A producer for any one of them
  -- is sufficient; checking only the first would report false dead ends.
  local recipe_categories = recipe.categories or {recipe.category or "crafting"}
  local supported, tank_recipe = false, false
  for _, category in pairs(recipe_categories) do
    category_count[category] = (category_count[category] or 0) + 1
    if producers[category] or category == "crafting" or category == "parameters" then
      supported = true
    end
    if category == "tank-crafting" or category == "tank-ammo-component" then
      tank_recipe = true
    end
  end
  if not supported then
    no_machine = no_machine + 1
    warn("No machine crafts any category " .. table.concat(recipe_categories, ",") ..
      " (recipe " .. name .. ")")
  end
  if recipe.enabled == false and not unlocked[name] then
    recipes_without_unlock = recipes_without_unlock + 1
  end
  if tank_recipe then
    tank_recipes = tank_recipes + 1
    if recipe.enabled == false and not unlocked[name] then
      tank_missing_unlock = tank_missing_unlock + 1
      warn("Disabled tank recipe with no technology unlock: " .. name)
    end
  end
end
for _, name in ipairs({"tank-crafting", "tank-ammo-component"}) do
  if not (data.raw["recipe-category"] or {})[name] then
    fail("Missing recipe category: " .. name)
  end
  if not producers[name] then fail("No machine supports category: " .. name) end
end

-- Cooking Fire V2 exact native production registration.
-- A native Factorio data-final-fixes load must resolve every directional
-- atlas and the game-aligned north steam port; this is not a visual-style gate.
local cf_errors = 0
local function cf_fail(message)
  cf_errors = cf_errors + 1
  fail("COOKING_FIRE_GRAPHICS: " .. message)
end
local cf = (data.raw["assembling-machine"] or {})["cooking-fire"]
local item = (data.raw.item or {})["cooking-fire"]
local prefix = "__tanks_for_bob_fork__/graphics/entity/cooking-fire-v2-production-"
local expected_icon = "__tanks_for_bob_fork__/graphics/icons/cooking-fire-v2-production.png"
if not cf then
  cf_fail("assembling-machine missing")
else
  local set = cf.graphics_set or {}
  if set.always_draw_idle_animation ~= false then
    cf_fail("idle sprites overlap active graphics")
  end
  local dirs = {"north", "east", "south", "west"}
  for _, state in ipairs({"working", "idle"}) do
    local animation = state == "working" and set.animation or set.idle_animation
    for i, direction in ipairs(dirs) do
      local view = animation and animation[direction]
      if type(view) ~= "table" then
        cf_fail(state .. "/" .. direction .. " is absent")
      else
        if view.filename ~= prefix .. state .. ".png" then
          cf_fail(state .. "/" .. direction .. " has wrong atlas")
        end
        if view.width ~= 256 or view.height ~= 256 or
            view.frame_count ~= 16 or view.line_length ~= 8 then
          cf_fail(state .. "/" .. direction .. " has wrong frame layout")
        end
        if view.x ~= 0 or view.y ~= (i - 1) * 512 then
          cf_fail(state .. "/" .. direction .. " has wrong atlas row")
        end
        if math.abs((view.animation_speed or 0) - (8 / 60)) > 0.00001 then
          cf_fail(state .. "/" .. direction .. " has wrong speed")
        end
      end
    end
  end
  if cf.icon ~= expected_icon or cf.icon_size ~= 64 then
    cf_fail("placed entity icon was not promoted")
  end
  if not cf.energy_source or cf.energy_source.type ~= "burner" then
    cf_fail("original burner behavior missing")
  end
  local input = cf.fluid_boxes and cf.fluid_boxes[1]
  local connection = input and input.pipe_connections and input.pipe_connections[1]
  local position = connection and connection.position
  if not input or input.production_type ~= "input" or not connection or
      connection.flow_direction ~= "input" or not position or
      position[1] ~= 0 or position[2] ~= -1 then
    cf_fail("3x3 north steam input position changed")
  end
end
if not item or item.icon ~= expected_icon or item.icon_size ~= 64 then
  cf_fail("item icon was not promoted")
end
if cf_errors == 0 then
  log("[TANKS-CI] COOKING_FIRE_GRAPHICS_PASS directions=4 states=2 frames=16 steam=north")
end

-- Recycling/quality guardrail is applied for Quality, Space Age, and 2.1 Recycler.
local protected_names = {"corporate-waste-reprocessing", "tank-ammo-Reprocessing", "ore-from-waste"}
local no_recycle = 0
for _, name in ipairs(protected_names) do
  local recipe = recipes[name]
  if recipe and recipe.auto_recycle == false then no_recycle = no_recycle + 1 end
  if recipe and (mods["quality"] or mods["space-age"] or mods["recycler"])
      and recipe.auto_recycle ~= false then
    warn("Waste recipe missing auto_recycle=false guard: " .. name)
  end
end

local recipe_total = 0
for _ in pairs(recipes) do recipe_total = recipe_total + 1 end
log(string.format(
  "[TANKS-CI] DATA_AUDIT recipes=%d technologies=%d unlocks=%d prerequisites=%d disabled_without_unlock=%d tank_recipes=%d tank_without_unlock=%d no_machine=%d recycling_guards=%d warnings=%d",
  recipe_total, tech_count, unlock_count, prereq_edges,
  recipes_without_unlock, tank_recipes, tank_missing_unlock,
  no_machine, no_recycle, #warnings))
for i, msg in ipairs(warnings) do
  if i <= 75 then log("[TANKS-CI] WARNING " .. msg) end
end
if #warnings > 75 then
  log("[TANKS-CI] WARNING " .. (#warnings - 75) .. " additional warnings omitted from console")
end
if #failures > 0 then
  for _, msg in ipairs(failures) do log("[TANKS-CI] FAIL " .. msg) end
  error("Tanks for Bob CI data audit detected " .. #failures .. " blocking problems")
end
log(string.format("[TANKS-CI] SOURCE_REGISTRY_PASS declared_recipes=%d declared_technologies=%d recipes_missing_unlock=%d", manifest_recipe_count, manifest_tech_count, manifest_missing_unlocks))
require("ci_progression_audit")
require("ci_weapon_audit")
require("ci_recipe_machine_audit")
require("ci_beach_pump_offshore_audit")
log("[TANKS-CI] DATA_PASS official-mod profile, recipe technology and machine-category registry")
