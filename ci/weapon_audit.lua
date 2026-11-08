-- CI-only vehicle/handheld weapon, ammunition and item-placement audit.
-- This inspects prototypes, not actual firing, damage, or graphical animation.
local car = data.raw.car or {}
local guns = data.raw.gun or {}
local ammo = data.raw.ammo or {}
local recipes = data.raw.recipe or {}
local technologies = data.raw.technology or {}
local categories = data.raw["ammo-category"] or {}
local manifest = require("ci_manifest")
-- Explicit inventory from the progression audit. Keep these known ammunition
-- families covered even if a future manifest edit misses a declaration file.
local required_ammo = {
  ["Sharp-stick"] = "wood",
  ["flame-thrower-ammo-tanker"] = "tank-spray-ammo",
  ["flame-thrower-ammo-tanker-2"] = "tank-spray-ammo-2",
  ["45mm-auto"] = "auto-cannon-ammo",
  ["50mm-mortar"] = "tank-nade-ammo",
  ["cannon-shell-2"] = "cannon-shell",
  ["minepack"] = "tank-mine-ammo",
  ["rocketpack"] = "tank-rocket-ammo",
  ["50mm-mortar-poison"] = "tank-nade-ammo",
  ["minepack-poison"] = "tank-mine-ammo",
  ["piercing-shotgun-shell-brick"] = "shotgun-shell",
  ["ap-bullet-brick"] = "bullet",
  ["tank-wmd-ammo"] = "tank-wmd-ammo",
  ["wmdartillery-ammo"] = "artillery-shell",
}
local target_names = {
  "modular-tank", "flame-tank", "auto-tank", "nade-tank",
  "flame-tank-wlsk", "auto-tank-wlsk", "nade-tank-wlsk",
  "mine-tank", "rocket-tank", "super-tank", "super-tank-alternate",
  "super-tank-wmd", "car-flamer"
}
local warnings, failures, weapon_count, linked_ammo, supported = {}, {}, 0, 0, 0
local used_categories = {}
local ammo_by_category = {}
local craftable_ammo = {}
for _, recipe in pairs(recipes) do
  for _, product in pairs(recipe.results or {}) do
    if (product.type or "item") == "item" then
      craftable_ammo[product.name or product[1]] = true
    end
  end
  if recipe.result then craftable_ammo[recipe.result] = true end
end
-- In Factorio 2.0/2.1, AmmoItemPrototype.ammo_category is on the
-- prototype itself, not inside its action payload (ammo_type).
for name, prototype in pairs(ammo) do
  local category = prototype.ammo_category
  if category then
    ammo_by_category[category] = ammo_by_category[category] or {}
    table.insert(ammo_by_category[category], name)
  end
end
local function flag(what)
  if #warnings < 160 then warnings[#warnings+1] = what end
end
local function fail(what) failures[#failures+1] = what end
for _, name in ipairs(target_names) do
  local vehicle = car[name]
  if not vehicle then
    flag("missing vehicle prototype " .. name)
  else
    supported = supported + 1
    local guns_on_vehicle = vehicle.guns or {}
    if #guns_on_vehicle == 0 then flag("vehicle has no gun: " .. name) end
    local item = (data.raw.item or {})[name] or (data.raw["item-with-entity-data"] or {})[name]
    if not item then
      flag("vehicle has no placeable item prototype: " .. name)
    elseif item.place_result ~= name then
      flag("vehicle item place_result differs: " .. name)
    end
    if vehicle.minable and vehicle.minable.result and vehicle.minable.result ~= name then
      flag("vehicle mining result is unexpected: " .. name .. " => " .. vehicle.minable.result)
    end
    for _, gun_name in pairs(guns_on_vehicle) do
      weapon_count = weapon_count + 1
      local gun = guns[gun_name]
      if not gun then
        flag("vehicle references missing gun: " .. name .. " => " .. tostring(gun_name))
      else
        local p = gun.attack_parameters or {}
        local category = p.ammo_category
        if not category then
          flag("gun has no ammo category: " .. gun_name)
        else
          used_categories[category] = true
          if not categories[category] then
            flag("gun category unregistered: " .. gun_name .. " => " .. category)
          end
          if not ammo_by_category[category] or #ammo_by_category[category] == 0 then
            flag("no ammo prototype available for gun " .. gun_name .. " / category " .. category)
          else
            linked_ammo = linked_ammo + 1
          end
        end
      end
    end
  end
end
local ammo_count, ammo_with_craft_recipe = 0, 0
for name in pairs(manifest.ammo or {}) do
  ammo_count = ammo_count + 1
  if not ammo[name] then
    flag("source-declared ammo prototype is missing from registry: " .. name)
  elseif not ammo[name].ammo_category then
    flag("source-declared ammo has no ammo category: " .. name)
  end
  if craftable_ammo[name] then
    ammo_with_craft_recipe = ammo_with_craft_recipe + 1
  else
    flag("source-declared ammo has no detected crafting output: " .. name)
  end
end
local required_ammo_count = 0
for name, category in pairs(required_ammo) do
  required_ammo_count = required_ammo_count + 1
  if not (manifest.ammo or {})[name] then
    fail("audited ammunition is missing from the source manifest: " .. name)
  end
  local prototype = ammo[name]
  if not prototype then
    fail("audited ammunition is missing from the live registry: " .. name)
  elseif prototype.ammo_category ~= category or not categories[category] then
    fail("audited ammunition category changed or is unregistered: " .. name .. " / " .. category)
  end
  if not craftable_ammo[name] then
    fail("audited ammunition has no crafting output: " .. name)
  end
end

-- The user's starting-weapon regression is an explicit contract, separate
-- from the broader diagnostic vehicle topology above. Runtime tests must
-- additionally prove that wood acquisition completes this scripted research.
local weapon_recipe, ammunition_recipe = recipes["wood-spear"], recipes["Sharp-stick"]
local wood_technology = technologies["wood-spear"]
local character = (data.raw.character or {}).character
local function handcraftable(recipe)
  if not (recipe and character) then return false end
  for _, ingredient in pairs(recipe.ingredients or {}) do
    if ingredient.type == "fluid" then return false end
  end
  for _, category in pairs(recipe.categories or {recipe.category or "crafting"}) do
    for _, allowed in pairs(character.crafting_categories or {}) do
      if category == allowed then return true end
    end
  end
  return false
end
local function produces(recipe, item_name)
  for _, product in pairs((recipe or {}).results or {}) do
    if (product.type or "item") == "item" and (product.name or product[1]) == item_name then
      return true
    end
  end
  return recipe and recipe.result == item_name
end
if not weapon_recipe or weapon_recipe.enabled == false or not handcraftable(weapon_recipe)
    or not produces(weapon_recipe, "wood-spear") then
  fail("wood-spear must be an initially enabled handcraft recipe for the wooden weapon")
end
if not ammunition_recipe or ammunition_recipe.enabled ~= false or not handcraftable(ammunition_recipe)
    or not produces(ammunition_recipe, "Sharp-stick") then
  fail("Sharp-stick must start locked and remain handcraftable after its material discovery")
end
local wooden_gun = guns["wood-spear"]
if not wooden_gun or (wooden_gun.attack_parameters or {}).ammo_category ~= "wood" then
  fail("wood-spear must accept the wooden ammunition category")
end
if not wood_technology then
  fail("missing wooden-ammunition discovery technology")
else
  if next(wood_technology.prerequisites or {}) or wood_technology.unit or
      wood_technology.enabled == false or
      (wood_technology.research_trigger or {}).type ~= "scripted" then
    fail("wood-spear technology must be a root scripted material discovery without science-pack research")
  end
  local unlocks_ammunition = false
  for _, effect in pairs(wood_technology.effects or {}) do
    if effect.type == "unlock-recipe" and effect.recipe == "Sharp-stick" then
      unlocks_ammunition = true
    end
  end
  if not unlocks_ammunition then fail("wood-spear discovery must unlock Sharp-stick ammunition") end
end

-- Check every unlocking technology, so a second research path cannot silently
-- reintroduce ammunition before the platform that fires it. An ancestor must
-- be completed first; unlocking ammunition in the platform technology itself
-- does not satisfy these dedicated upgrade branches.
local function has_ancestor(name, wanted, visited)
  visited = visited or {}
  if visited[name] then return false end
  visited[name] = true
  for _, prerequisite in pairs((technologies[name] or {}).prerequisites or {}) do
    if prerequisite == wanted or has_ancestor(prerequisite, wanted, visited) then
      return true
    end
  end
  return false
end
for _, gate in ipairs({
  {recipe = "minepack-poison", prerequisites = {"new-munitions", "modular-tank-research3", "land-mine"}},
  {recipe = "wmdartillery-ammo", prerequisites = {"super-tank-research2", "artillery"}}
}) do
  local recipe = recipes[gate.recipe]
  if not recipe or recipe.enabled ~= false then
    fail(gate.recipe .. " must start locked behind its weapon prerequisites")
  end
  local unlockers = 0
  for name, technology in pairs(technologies) do
    for _, effect in pairs(technology.effects or {}) do
      if effect.type == "unlock-recipe" and effect.recipe == gate.recipe then
        unlockers = unlockers + 1
        for _, prerequisite in ipairs(gate.prerequisites) do
          if not has_ancestor(name, prerequisite) then
            fail(name .. " unlocks " .. gate.recipe .. " without prerequisite ancestry: " .. prerequisite)
          end
        end
      end
    end
  end
  if unlockers == 0 then fail(gate.recipe .. " has no research unlock") end
end

if technologies["stone-tools"] then
  fail("stone-tools technology must be removed; basic tools are a starting recipe")
end
local starter_tools = recipes["stone-tools"]
if not starter_tools or starter_tools.enabled == false or not handcraftable(starter_tools)
    or not produces(starter_tools, "stone-tools") then
  fail("stone-tools must remain an initially enabled handcraft recipe")
end

local category_count = 0
for _ in pairs(used_categories) do category_count = category_count + 1 end
log(("[TANKS-CI] WEAPON_AUDIT vehicles=%d gun_slots=%d supported_categories=%d ammo_links=%d declared_ammo=%d declared_ammo_craftable=%d warnings=%d"):format(
  supported, weapon_count, category_count, linked_ammo, ammo_count, ammo_with_craft_recipe, #warnings))
for i, message in ipairs(warnings) do
  if i > 80 then break end
  log("[TANKS-CI] WEAPON_WARNING " .. message)
end
if #warnings > 80 then log("[TANKS-CI] WEAPON_WARNINGS_ADDITIONAL " .. (#warnings - 80)) end
if #failures > 0 then
  for _, message in ipairs(failures) do log("[TANKS-CI] WEAPON_FAIL " .. message) end
  error("[TANKS-CI] " .. #failures .. " ammunition registry or progression regressions")
end
log(("[TANKS-CI] AMMO_REGISTRY_PASS audited=%d declared=%d craftable=%d"):format(
  required_ammo_count, ammo_count, ammo_with_craft_recipe))
log("[TANKS-CI] HANDHELD_UNLOCK_PASS weapon=starting_handcraft ammo=locked discovery=root_scripted")
log("[TANKS-CI] WEAPON_PROGRESSION_PASS poison_mine=vehicle_and_land_mine artillery=wmd_and_artillery stone_tools=starting_only")
-- True firing compatibility requires runtime driver, ammo and target scenarios.
log("[TANKS-CI] WEAPON_AUDIT_PASS data-stage registry inspected (shots not yet fired)")
