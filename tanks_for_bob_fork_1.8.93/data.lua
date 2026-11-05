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

require("prototypes.technology.technology")
require("prototypes.equipment.equipment")
require("prototypes.fluid.fluid")

-- Optional compatibility patches
if mods["space-age"] or mods["quality"] or mods["recycler"] then
  require("prototypes.Compatibility.space-age")
end

require("prototypes.Compatibility.mechanicus-locale")
