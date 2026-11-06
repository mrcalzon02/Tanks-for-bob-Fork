-- CI-only optimistic recipe supply graph diagnostic.
-- Runs in Factorio's data-final-fixes after the live recipe registry is built.
-- Ignoring research, machine construction, fuel/power, fluids requiring special
-- production, product probabilities and surfaces means reachable != manufacturable.
local recipes = data.raw.recipe or {}
local manifest = require("ci_manifest")
local available = {}
local source_items, source_fluids = {}, {}
local function add(kind, name)
  if not name then return false end
  local key = (kind == "fluid" and "fluid:" or "item:") .. name
  if available[key] then return false end
  available[key] = true
  return true
end

-- Natural resources are attainable in an ordinary world (not a one-tile
-- challenge map); this deliberately does NOT validate every map preset.
for _, resource in pairs(data.raw.resource or {}) do
  local mined = resource.minable
  if mined then
    if mined.result then
      if add("item", mined.result) then source_items[mined.result] = true end
    end
    for _, result in pairs(mined.results or {}) do
      if add(result.type, result.name or result[1]) then
        (result.type == "fluid" and source_fluids or source_items)[result.name or result[1]] = true
      end
    end
  end
end
for _, source in ipairs({"wood", "raw-fish", "stone", "coal"}) do
  if add("item", source) then source_items[source] = true end
end
for _, source in ipairs({"water", "steam"}) do
  -- Steam is an optimistic baseline for recipes using a boiler.
  if add("fluid", source) then source_fluids[source] = true end
end

local function ingredients(recipe)
  if recipe.ingredients then return recipe.ingredients end
  if recipe.normal and recipe.normal.ingredients then return recipe.normal.ingredients end
  return {}
end
local function products(recipe)
  if recipe.results then return recipe.results end
  if recipe.result then return {{type="item",name=recipe.result,amount=recipe.result_count or 1}} end
  if recipe.normal then
    if recipe.normal.results then return recipe.normal.results end
    if recipe.normal.result then return {{type="item",name=recipe.normal.result}} end
  end
  return {}
end
local function fields(record)
  if type(record) ~= "table" then return "item", nil end
  return record.type or "item", record.name or record[1]
end

local reachable, rounds = {}, 0
local changed = true
while changed and rounds < 500 do
  changed = false
  rounds = rounds + 1
  for name, recipe in pairs(recipes) do
    if not reachable[name] then
      local satisfied = true
      for _, ingredient in pairs(ingredients(recipe)) do
        local kind, value = fields(ingredient)
        if value and not available[(kind=="fluid" and "fluid:" or "item:") .. value] then
          satisfied = false
          break
        end
      end
      if satisfied then
        reachable[name] = true
        changed = true
        for _, result in pairs(products(recipe)) do
          local kind, value = fields(result)
          if add(kind, value) then changed = true end
        end
      end
    end
  end
end

local inaccessible, all_recipes, declared, reachable_declared = {}, 0, 0, 0
for _ in pairs(recipes) do all_recipes = all_recipes + 1 end
for name in pairs(manifest.recipes) do
  declared = declared + 1
  if reachable[name] then
    reachable_declared = reachable_declared + 1
  else
    local unresolved = {}
    for _, ingredient in pairs(ingredients(recipes[name] or {})) do
      local kind, value = fields(ingredient)
      if value and not available[(kind=="fluid" and "fluid:" or "item:") .. value] then
        unresolved[#unresolved+1] = kind .. ":" .. value
      end
    end
    table.sort(unresolved)
    inaccessible[#inaccessible+1] = {name=name, missing=table.concat(unresolved, ",")}
  end
end
table.sort(inaccessible, function(a,b) return a.name < b.name end)
local unavailable = declared - reachable_declared
log(("[TANKS-CI] SUPPLY_GRAPH rounds=%d recipes=%d mod_recipes=%d optimistic_reachable=%d optimistic_blocked=%d"):format(
  rounds, all_recipes, declared, reachable_declared, unavailable))
for i, row in ipairs(inaccessible) do
  if i > 80 then break end
  log("[TANKS-CI] SUPPLY_UNREACHABLE " .. row.name .. " missing=" .. row.missing)
end
if #inaccessible > 80 then
  log("[TANKS-CI] SUPPLY_UNREACHABLE_ADDITIONAL " .. (#inaccessible - 80))
end
-- This check is intentionally diagnostic; a detailed vanilla/SeaBlock
-- production fixture must be built before hard failing supply reachability.
log("[TANKS-CI] SUPPLY_GRAPH_PASS diagnostic closure computed (research and machinery not proven)")
