-- Optional Bob's Metals route for the fork's first encabulation alloy.
-- Clones the final native recipe to preserve custom inputs and waste outputs.
-- Original vanilla/island-survival production remains intact.
if not (mods and mods["bobplates"]) then return end
local option = settings.startup["tfbf-bobs-metallurgy"]
if not option or not option.value then return end

local recipe_base = (data.raw.recipe or {})["encabuloy-alloy"]
local bob_item = (data.raw.item or {})["bob-invar-alloy"]
local bob_technology = (data.raw.technology or {})["bob-invar-processing"]
local fork_technology = (data.raw.technology or {})["pre-encabulation-materials"]
if not (recipe_base and bob_item and bob_technology and fork_technology
    and bob_technology.unit and bob_technology.unit.ingredients) then
  log("[TANKS-BOBS] INVAR_ALTERNATIVE_SKIPPED missing metallurgy prototype")
  return
end

local name = "tfbf-bobs-encabuloy-invar"
local recipe_exists = (data.raw.recipe or {})[name]
local technology_exists = (data.raw.technology or {})[name]
if recipe_exists or technology_exists then
  -- Respect external integrations; never override prototypes with same IDs.
  log("[TANKS-BOBS] INVAR_ALTERNATIVE_SKIPPED integration identifier already used")
  return
end

local recipe = table.deepcopy(recipe_base)
local ingredients = {}
local removed_iron, removed_copper = false, false
for _, ingredient in ipairs(recipe.ingredients or {}) do
  local item = ingredient.name or ingredient[1]
  if item == "iron-plate" then
    removed_iron = true
  elseif item == "copper-plate" then
    removed_copper = true
  else
    ingredients[#ingredients + 1] = ingredient
  end
end
if not (removed_iron and removed_copper) then
  log("[TANKS-BOBS] INVAR_ALTERNATIVE_SKIPPED unexpected original ingredient structure")
  return
end
ingredients[#ingredients + 1] = {
  type = "item", name = "bob-invar-alloy", amount = 2,
}
recipe.name = name
recipe.ingredients = ingredients
recipe.enabled = false
recipe.auto_recycle = false
recipe.localised_name = {"recipe-name." .. name}

-- Use Bob's own final research science requirements, and require the fork's
-- existing materials unlock too. Thus this path can never strand early items.
local technology = {
  type = "technology",
  name = name,
  prerequisites = {"bob-invar-processing", "pre-encabulation-materials"},
  effects = {{type = "unlock-recipe", recipe = name}},
  unit = table.deepcopy(bob_technology.unit),
  order = "ak-z[bobs-invar]",
}
technology.unit.count = 60
if bob_technology.icons then
  technology.icons = table.deepcopy(bob_technology.icons)
else
  technology.icon = bob_technology.icon
  technology.icon_size = bob_technology.icon_size
end

data:extend({recipe, technology})
log("[TANKS-BOBS] INVAR_ALTERNATIVE_ADDED recipes=1 technologies=1")
