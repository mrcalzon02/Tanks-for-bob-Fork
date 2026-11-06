require("prototypes.categories.recipe-category")
require("prototypes.categories.ammo-category")
require("prototypes.entity.entities")
require("prototypes.entity.vehicles")
require("prototypes.entity.explosionsa")
require("prototypes.entity.projectiles")
require("prototypes.item.ammo")
require("prototypes.item.item")
require("prototypes.item.item-groups")
require("prototypes.item.gun")
require("prototypes.item.vehicles")
require("prototypes.item.capsule")
require("prototypes.item.equipment")
-- Factorio 2.1 replaced ItemPrototype.fuel_category with fuel_categories.
-- Only migrate the temporary 2.1 test runtime; retain 2.0 behavior unchanged.
if (mods["base"] or ""):match("^2%.1%.") then
  for _, kind in ipairs({"item", "tool", "ammo", "capsule", "gun", "module", "repair-tool"}) do
    for _, prototype in pairs(data.raw[kind] or {}) do
      if prototype.fuel_category then
        prototype.fuel_categories = prototype.fuel_categories or {prototype.fuel_category}
        prototype.fuel_category = nil
      end
    end
  end
end
-- Record Factorio's existing recipes so the compatibility pass touches only
-- recipes added by this mod, not the base game or official expansion mods.
local recipes_before_tanks = {}
for name in pairs(data.raw.recipe or {}) do recipes_before_tanks[name] = true end

require("prototypes.recipe.ammo")
require("prototypes.recipe.recipe")
require("prototypes.recipe.vehicles")

-- Factorio requires explicit icons for multi-output recipes. Inherit the actual
-- primary item's icon instead of substituting unrelated placeholder artwork.
-- This is deliberately restricted to recipes introduced by this mod.
for name, recipe in pairs(data.raw.recipe or {}) do
  if not recipes_before_tanks[name] and not recipe.icon and not recipe.icons
      and recipe.results and #recipe.results > 1 then
    local first = recipe.results[1]
    local result_name = first.name or first[1]
    local result_type = first.type or "item"
    local item = (data.raw[result_type] or {})[result_name]
    if not item and result_type == "item" then
      -- Research tools, ammunition and equipment can be item-type recipe outputs.
      for _, category in ipairs({
        "tool", "ammo", "capsule", "gun", "module", "repair-tool",
        "item-with-entity-data", "item-with-inventory", "item-with-label",
        "item-with-tags", "rail-planner"
      }) do
        item = (data.raw[category] or {})[result_name]
        if item then break end
      end
    end
    if item then
      if item.icons then
        recipe.icons = table.deepcopy(item.icons)
      elseif item.icon then
        recipe.icon = item.icon
        recipe.icon_size = item.icon_size or 64
        recipe.icon_mipmaps = item.icon_mipmaps
      end
    end
  end
end

-- 2.1 merged RecipePrototype.category/additional_categories into categories.
-- Apply the migration only to recipes introduced by this fork.
if (mods["base"] or ""):match("^2%.1%.") then
  for name, recipe in pairs(data.raw.recipe or {}) do
    if not recipes_before_tanks[name] and
        (recipe.category or recipe.additional_categories) then
      local categories = recipe.categories or {}
      if recipe.category then table.insert(categories, recipe.category) end
      for _, other in ipairs(recipe.additional_categories or {}) do
        table.insert(categories, other)
      end
      recipe.categories = categories
      recipe.category = nil
      recipe.additional_categories = nil
    end
  end
end

-- 2.1 replaced RecipeProduct.probability with independent_probability.
-- Preserve the original probability value without altering the 2.0 schema.
if (mods["base"] or ""):match("^2%.1%.") then
  for name, recipe in pairs(data.raw.recipe or {}) do
    if not recipes_before_tanks[name] then
      for _, product in ipairs(recipe.results or {}) do
        if product.probability ~= nil then
          product.independent_probability = product.probability
          product.probability = nil
        end
      end
    end
  end
end

require("prototypes.technology.technology")
require("prototypes.equipment.equipment")
require("prototypes.fluid.fluid")

-- Optional compatibility patches
if mods["space-age"] or mods["quality"] or mods["recycler"] then
  require("prototypes.Compatibility.space-age")
end

require("prototypes.Compatibility.mechanicus-locale")
