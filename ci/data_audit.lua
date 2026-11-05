-- CI only: injected into disposable mod install as data-final-fixes.lua.
local recipes = data.raw.recipe or {}
local technologies = data.raw.technology or {}
local failures = {}
local function check(test, reason)
  if not test then failures[#failures + 1] = reason end
end
local vehicles = {
  "flame-tank", "auto-tank", "nade-tank", "flame-tank-wlsk",
  "auto-tank-wlsk", "nade-tank-wlsk", "mine-tank", "rocket-tank",
  "super-tank", "super-tank-alternate", "super-tank-wmd", "car-flamer"
}
for _, name in ipairs(vehicles) do
  check(recipes[name] ~= nil, "Missing vehicle recipe: " .. name)
  check((data.raw.car or {})[name] ~= nil, "Missing vehicle entity: " .. name)
end
local unlocked = {}
local unlock_count = 0
for name, technology in pairs(technologies) do
  for _, effect in pairs(technology.effects or {}) do
    if effect.type == "unlock-recipe" then
      unlock_count = unlock_count + 1
      check(recipes[effect.recipe] ~= nil,
        "Technology " .. name .. " unlocks missing recipe " .. tostring(effect.recipe))
      unlocked[effect.recipe] = true
    end
  end
  for _, prerequisite in pairs(technology.prerequisites or {}) do
    check(technologies[prerequisite] ~= nil,
      "Technology " .. name .. " requires missing technology " .. tostring(prerequisite))
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
for _, category in ipairs({"tank-crafting", "tank-ammo-component"}) do
  check((data.raw["recipe-category"] or {})[category] ~= nil,
    "Missing recipe category " .. category)
  check(producers[category] == true,
    "No machine supports crafting category " .. category)
end
local missing_unlocks = 0
local tank_recipes = 0
for name, recipe in pairs(recipes) do
  if recipe.category == "tank-crafting" or recipe.category == "tank-ammo-component" then
    tank_recipes = tank_recipes + 1
    if recipe.enabled == false and not unlocked[name] then
      missing_unlocks = missing_unlocks + 1
      log("[TANKS-CI] WARNING disabled recipe has no technology unlock: " .. name)
    end
  end
end
log(string.format("[TANKS-CI] DATA_AUDIT tank_recipes=%d technology_unlocks=%d unlock_warnings=%d",
  tank_recipes, unlock_count, missing_unlocks))
if #failures > 0 then
  for _, message in ipairs(failures) do log("[TANKS-CI] FAIL " .. message) end
  error("Tanks for Bob data audit failed: " .. #failures .. " problems")
end
log("[TANKS-CI] DATA_PASS isolated vanilla and tanks prototype audit")
