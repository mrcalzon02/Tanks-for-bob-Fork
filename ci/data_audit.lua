-- CI-only data-stage audit; installed in disposable test mod, not released.
local recipes = data.raw.recipe or {}
local technologies = data.raw.technology or {}
local expected = require("ci_profile")
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
  local category = recipe.category or "crafting"
  category_count[category] = (category_count[category] or 0) + 1
  if not producers[category] and category ~= "crafting" and category ~= "parameters" then
    no_machine = no_machine + 1
    warn("No machine crafts category " .. category .. " (recipe " .. name .. ")")
  end
  if recipe.enabled == false and not unlocked[name] then
    recipes_without_unlock = recipes_without_unlock + 1
  end
  if category == "tank-crafting" or category == "tank-ammo-component" then
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
log("[TANKS-CI] DATA_PASS official-mod profile, recipe technology and machine-category registry")
