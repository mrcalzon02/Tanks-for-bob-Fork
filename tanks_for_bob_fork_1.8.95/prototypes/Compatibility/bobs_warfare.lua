-- Bob's Warfare alternate hull construction for Tanks for Bob Fork.
-- Conditional data-final-fixes adapter; the original recipes and technologies
-- remain unchanged for Bob-free, partial-Bob, and full-Bob installations.
if not (mods and mods["bobwarfare"]) then return end

local option = settings.startup["tfbf-bobs-advanced-hulls"]
if not option or not option.value then return end

local recipes = data.raw.recipe or {}
local techs = data.raw.technology or {}
local hull_items = data.raw["item-with-entity-data"] or {}

-- Bob's published 2.x Warfare tanks are actual vehicle items and their
-- research includes production science (Mk2) and utility science (Mk3).
-- If another combination removes those definitions, don't add dangling
-- alternative recipes or missing technology prerequisites.
if not (hull_items["bob-tank-2"] and hull_items["bob-tank-3"]
    and techs["bob-tanks-2"] and techs["bob-tanks-3"]
    and techs["super-tank-research"] and techs["super-tank-research2"]
    and recipes["super-tank"] and recipes["super-tank-alternate"]
    and recipes["super-tank-wmd"]) then
  log("[TANKS-BOBS] WARFARE_ALTERNATES_SKIPPED missing hull/tech/recipe prototypes")
  return
end

local alternates = {
  {
    name = "tfbf-bobs-super-tank-mk2",
    original = "super-tank",
    hull = "bob-tank-2",
    adjusted_component = "DuplexedSpervingArm",
    adjusted_amount = 30,
  },
  {
    name = "tfbf-bobs-super-tank-alternate-mk2",
    original = "super-tank-alternate",
    hull = "bob-tank-2",
    adjusted_component = "DuctedSpervingArm",
    adjusted_amount = 60,
  },
  {
    name = "tfbf-bobs-super-tank-wmd-mk3",
    original = "super-tank-wmd",
    hull = "bob-tank-3",
    adjusted_component = "DuplexedSpervingArm",
    adjusted_amount = 20,
  },
}

local added = {}
for _, spec in ipairs(alternates) do
  -- Copy the final recipe after Bob's other data-stage adjustments. Only the
  -- tank hull and one component amount change; original recipes are preserved.
  if not recipes[spec.name] then
    local recipe = table.deepcopy(recipes[spec.original])
    recipe.name = spec.name
    recipe.enabled = false
    recipe.auto_recycle = false
    recipe.localised_name = {"recipe-name." .. spec.name}
    local replaced_hull, adjusted_part = false, false
    for _, ingredient in ipairs(recipe.ingredients or {}) do
      local ingredient_name = ingredient.name or ingredient[1]
      if ingredient_name == "tank" then
        ingredient.name = spec.hull
        ingredient[1] = nil
        replaced_hull = true
      elseif ingredient_name == spec.adjusted_component then
        ingredient.amount = spec.adjusted_amount
        ingredient[2] = nil
        adjusted_part = true
      end
    end
    if replaced_hull and adjusted_part then
      added[#added + 1] = recipe
    else
      log("[TANKS-BOBS] WARFARE_ALTERNATES_SKIPPED changed source recipe " .. spec.original)
      return
    end
  end
end

local function integration_technology(name, source, prerequisites, recipes_unlocked, count, order)
  local science = techs[source]
  local icon_source = techs["super-tank-research"]
  if not (science.unit and science.unit.ingredients) then
    return nil
  end
  local effects = {}
  for _, recipe_name in ipairs(recipes_unlocked) do
    effects[#effects + 1] = {type = "unlock-recipe", recipe = recipe_name}
  end
  local result = {
    type = "technology",
    name = name,
    prerequisites = prerequisites,
    effects = effects,
    unit = table.deepcopy(science.unit),
    order = order,
  }
  result.unit.count = count
  if icon_source.icons then
    result.icons = table.deepcopy(icon_source.icons)
  else
    result.icon = icon_source.icon
    result.icon_size = icon_source.icon_size
  end
  return result
end

local new_techs = {}
if not techs["tfbf-bobs-hulls-mk2"] then
  local proto = integration_technology(
    "tfbf-bobs-hulls-mk2", "bob-tanks-2",
    {"bob-tanks-2", "super-tank-research"},
    {"tfbf-bobs-super-tank-mk2", "tfbf-bobs-super-tank-alternate-mk2"},
    60, "ak-z[bobs-mk2]")
  if proto then new_techs[#new_techs + 1] = proto end
end
if not techs["tfbf-bobs-hulls-mk3"] then
  local proto = integration_technology(
    "tfbf-bobs-hulls-mk3", "bob-tanks-3",
    {"bob-tanks-3", "super-tank-research2"},
    {"tfbf-bobs-super-tank-wmd-mk3"},
    100, "ak-z[bobs-mk3]")
  if proto then new_techs[#new_techs + 1] = proto end
end

-- Don't partially register disabled recipes without an unlocking technology.
if (#new_techs > 0 or
    (techs["tfbf-bobs-hulls-mk2"] and techs["tfbf-bobs-hulls-mk3"]))
    and techs["bob-tanks-2"].unit and techs["bob-tanks-3"].unit then
  for _, recipe in ipairs(added) do data:extend({recipe}) end
  for _, technology in ipairs(new_techs) do data:extend({technology}) end
  log("[TANKS-BOBS] WARFARE_ALTERNATES_ADDED recipes=" .. #added ..
      " technologies=" .. #new_techs)
end
