-- CI-only Bob's full-family integration diagnostics, never in release ZIP.
-- Executes at the end of data-final-fixes, after compatibility adapters.
if not mods["boblibrary"] then return end

local vehicles = data.raw.car or {}
local grids = data.raw["equipment-grid"] or {}
local machines = data.raw["assembling-machine"] or {}
local technologies = data.raw.technology or {}
local recipes = data.raw.recipe or {}

local assignments = {
  ["car-flamer"] = "bob-car",
  ["modular-tank"] = "bob-tank",
  ["flame-tank"] = "bob-tank",
  ["auto-tank"] = "bob-tank",
  ["nade-tank"] = "bob-tank",
  ["flame-tank-wlsk"] = "bob-tank-2",
  ["auto-tank-wlsk"] = "bob-tank-2",
  ["nade-tank-wlsk"] = "bob-tank-2",
  ["mine-tank"] = "bob-tank-2",
  ["rocket-tank"] = "bob-tank-2",
  ["super-tank"] = "bob-tank-3",
  ["super-tank-alternate"] = "bob-tank-3",
  ["super-tank-wmd"] = "bob-tank-3"
}

local own = settings.startup["tfbf-bobs-equipment-grids"]
local bob = settings.startup["bobmods-vehicleequipment-enablevehiclegrids"]
local expect_grids = mods["bobvehicleequipment"] and own and own.value
    and bob and bob.value
local grid_checks, grid_matches = 0, 0
for name, expected in pairs(assignments) do
  local prototype = vehicles[name]
  grid_checks = grid_checks + 1
  if not prototype then
    log("[TANKS-BOBS] DIAGNOSTIC missing fork car " .. name)
  elseif expect_grids then
    local actual = prototype.equipment_grid or "(none)"
    if not grids[expected] then
      log("[TANKS-BOBS] DIAGNOSTIC missing Bob equipment grid " .. expected)
    elseif actual == expected then
      grid_matches = grid_matches + 1
    else
      log("[TANKS-BOBS] DIAGNOSTIC grid mismatch " .. name ..
          " expected=" .. expected .. " actual=" .. actual)
    end
  end
end

local machine_checks, category_matches = 0, 0
for _, machine_name in ipairs({
  "bob-assembling-machine-4", "bob-assembling-machine-5",
  "bob-assembling-machine-6"
}) do
  local machine = machines[machine_name]
  if machine then
    machine_checks = machine_checks + 1
    local registered = {}
    for _, category in pairs(machine.crafting_categories or {}) do
      registered[category] = true
    end
    for _, category in ipairs({"tank-crafting", "tank-ammo-component"}) do
      if registered[category] then
        category_matches = category_matches + 1
      else
        log("[TANKS-BOBS] DIAGNOSTIC " .. machine_name ..
            " missing recipe category " .. category)
      end
    end
  else
    log("[TANKS-BOBS] DIAGNOSTIC missing Bob machine " .. machine_name)
  end
end

local branch_techs = {
  "modular-tank-research", "modular-tank-research2",
  "modular-tank-research3", "new-munitions",
  "super-tank-research", "super-tank-research2"
}
local missing_tech = 0
for _, name in ipairs(branch_techs) do
  if not technologies[name] then
    missing_tech = missing_tech + 1
    log("[TANKS-BOBS] DIAGNOSTIC missing fork technology " .. name)
  end
end
for _, name in ipairs({"bob-tanks-2", "bob-tanks-3"}) do
  if mods["bobwarfare"] and not technologies[name] then
    log("[TANKS-BOBS] DIAGNOSTIC missing warfare technology " .. name)
  end
end
for _, name in ipairs({"bob-tank-2", "bob-tank-3"}) do
  if mods["bobwarfare"] and not recipes[name] then
    log("[TANKS-BOBS] DIAGNOSTIC missing warfare recipe " .. name)
  end
end

local custom_labs = 0
for _, name in ipairs({"pondering-hovel", "thinking-hut"}) do
  local lab = (data.raw.lab or {})[name]
  if lab then
    custom_labs = custom_labs + 1
    log("[TANKS-BOBS] CUSTOM_LAB " .. name ..
        " accepted_science_types=" .. #(lab.inputs or {}))
  else
    log("[TANKS-BOBS] DIAGNOSTIC missing fork lab " .. name)
  end
end

log(string.format(
  "[TANKS-CI] BOBS_AUDIT_CHECKED modules=yes fork_vehicles=%d mapped_grids=%d " ..
  "expected_grids=%s bob_assemblers=%d craft_category_matches=%d/6 " ..
  "custom_labs=%d missing_fork_tech=%d",
  grid_checks, grid_matches, tostring(not not expect_grids),
  machine_checks, category_matches, custom_labs, missing_tech))

-- Actual final research/lab combination audit. A technology is researchable
-- only when a lab accepts its complete science-pack set, not just each pack
-- independently. This is a registry check, NOT proof of pack manufacturing or
-- cost/tech progression. Keep unsupported cases as diagnostics.
local manifest = require("ci_manifest")
local labs = data.raw.lab or {}
local techs_checked, lab_supported, no_lab, missing_science = 0, 0, 0, 0
local function check_technology(name)
  local technology = technologies[name]
  if not technology or not technology.unit or not technology.unit.ingredients
      or #technology.unit.ingredients == 0 then
    return
  end
  techs_checked = techs_checked + 1
  local required = {}
  for _, pack in pairs(technology.unit.ingredients) do
    local science_name = pack.name or pack[1]
    if science_name then
      required[science_name] = true
      if not (data.raw.tool or {})[science_name] then
        missing_science = missing_science + 1
        log("[TANKS-BOBS] TECH_DIAGNOSTIC " .. name ..
            " missing science item " .. science_name)
      end
    end
  end
  local available = false
  for _, lab in pairs(labs) do
    local accepted = {}
    for _, pack in pairs(lab.inputs or {}) do accepted[pack] = true end
    local all_supported = true
    for pack in pairs(required) do
      if not accepted[pack] then all_supported = false; break end
    end
    if all_supported then available = true; break end
  end
  if available then
    lab_supported = lab_supported + 1
  else
    no_lab = no_lab + 1
    log("[TANKS-BOBS] TECH_DIAGNOSTIC no lab accepts complete science set for " .. name)
  end
end

local ordered = {}
for name in pairs(manifest.technologies) do ordered[#ordered + 1] = name end
table.sort(ordered)
for _, name in ipairs(ordered) do check_technology(name) end
if mods["bobwarfare"] then
  check_technology("bob-tanks-2")
  check_technology("bob-tanks-3")
end

-- The actual Bob Mk2/Mk3 advanced-hull integration must not strand recipes
-- behind nonexistent technology unlocks or break original vanilla paths.
local advanced_setting = settings.startup["tfbf-bobs-advanced-hulls"]
if mods["bobwarfare"] and advanced_setting and advanced_setting.value then
  local specifications = {
    {"tfbf-bobs-super-tank-mk2", "super-tank", "bob-tank-2", "tfbf-bobs-hulls-mk2"},
    {"tfbf-bobs-super-tank-alternate-mk2", "super-tank-alternate", "bob-tank-2", "tfbf-bobs-hulls-mk2"},
    {"tfbf-bobs-super-tank-wmd-mk3", "super-tank-wmd", "bob-tank-3", "tfbf-bobs-hulls-mk3"},
  }
  local required_tech = {
    ["tfbf-bobs-hulls-mk2"] = {"bob-tanks-2", "super-tank-research"},
    ["tfbf-bobs-hulls-mk3"] = {"bob-tanks-3", "super-tank-research2"},
  }
  for tech_name, requirements in pairs(required_tech) do
    local technology = technologies[tech_name]
    if not technology then error("[TANKS-BOBS] Missing integration technology " .. tech_name) end
    local prereqs = {}
    for _, name in pairs(technology.prerequisites or {}) do prereqs[name] = true end
    for _, name in ipairs(requirements) do
      if not prereqs[name] then
        error("[TANKS-BOBS] " .. tech_name .. " lacks required prerequisite " .. name)
      end
    end
  end
  for _, spec in ipairs(specifications) do
    local recipe_name, output_name, hull, tech_name =
      spec[1], spec[2], spec[3], spec[4]
    local recipe, technology = recipes[recipe_name], technologies[tech_name]
    if not recipe then error("[TANKS-BOBS] Missing Bob alternative recipe " .. recipe_name) end
    if recipe.enabled ~= false or recipe.category ~= "tank-crafting" then
      error("[TANKS-BOBS] Invalid advanced-hull recipe availability/category " .. recipe_name)
    end
    local hull_found, output_found, tech_unlock_found = false, false, false
    for _, ingredient in pairs(recipe.ingredients or {}) do
      local ingredient_name = ingredient.name or ingredient[1]
      if ingredient_name == hull then hull_found = true end
      if ingredient_name == "tank" then
        error("[TANKS-BOBS] Alternative recipe still consumes vanilla hull " .. recipe_name)
      end
    end
    for _, result in pairs(recipe.results or {}) do
      if (result.name or result[1]) == output_name then output_found = true end
    end
    for _, effect in pairs(technology.effects or {}) do
      if effect.type == "unlock-recipe" and effect.recipe == recipe_name then
        tech_unlock_found = true
      end
    end
    if not (hull_found and output_found and tech_unlock_found) then
      error("[TANKS-BOBS] Advanced-hull recipe/technology chain mismatch " .. recipe_name)
    end
    if not recipes[output_name] then
      error("[TANKS-BOBS] Original tank recipe was removed " .. output_name)
    end
  end
  check_technology("tfbf-bobs-hulls-mk2")
  check_technology("tfbf-bobs-hulls-mk3")
  log("[TANKS-CI] BOBS_WARFARE_ALTERNATES_PASS recipes=3 technologies=2 base_recipes_preserved=3")
end

-- Invar alternative must preserve the fork's original production byproducts,
-- not just the primary alloy output. No base recipe is replaced.
local invar_setting = settings.startup["tfbf-bobs-metallurgy"]
if mods["bobplates"] and invar_setting and invar_setting.value then
  local name = "tfbf-bobs-encabuloy-invar"
  local alt, base_recipe, tech =
    recipes[name], recipes["encabuloy-alloy"], technologies[name]
  if not (alt and base_recipe and tech) then
    error("[TANKS-BOBS] Missing Invar alternate recipe or technology")
  end
  if alt.enabled ~= false or alt.category ~= base_recipe.category then
    error("[TANKS-BOBS] Invar alternate recipe has wrong availability/category")
  end
  local has_invar, has_iron, has_copper, kept_materials = false, false, false, 0
  for _, ingredient in ipairs(alt.ingredients or {}) do
    local id = ingredient.name or ingredient[1]
    if id == "bob-invar-alloy" then has_invar = true end
    if id == "iron-plate" then has_iron = true end
    if id == "copper-plate" then has_copper = true end
    if id == "hydrocoptic-crystal" or id == "bioceramic-grit" then
      kept_materials = kept_materials + 1
    end
  end
  if not has_invar or has_iron or has_copper or kept_materials ~= 2 then
    error("[TANKS-BOBS] Invar alternate input material substitution failed")
  end
  if #alt.results ~= #base_recipe.results then
    error("[TANKS-BOBS] Invar alternate changed number of waste/byproduct outputs")
  end
  for index, result in ipairs(base_recipe.results) do
    local actual = alt.results[index]
    if (result.name or result[1]) ~= (actual.name or actual[1])
        or (result.amount or result[2]) ~= (actual.amount or actual[2])
        or result.probability ~= actual.probability then
      error("[TANKS-BOBS] Invar alternative changed waste/output product " .. index)
    end
  end
  local prerequisites, unlocked = {}, false
  for _, id in ipairs(tech.prerequisites or {}) do prerequisites[id] = true end
  for _, effect in ipairs(tech.effects or {}) do
    if effect.type == "unlock-recipe" and effect.recipe == name then
      unlocked = true
    end
  end
  if not (prerequisites["bob-invar-processing"]
      and prerequisites["pre-encabulation-materials"] and unlocked) then
    error("[TANKS-BOBS] Invar alternative research chain incomplete")
  end
  check_technology(name)
  log("[TANKS-CI] BOBS_METALLURGY_ALTERNATE_PASS recipes=1 technologies=1 waste_outputs_preserved=" ..
      #alt.results)
end

-- Full final prototype research acceptance includes the adapter technologies,
-- not just the 88 baseline fork research definitions and Bob tank tiers.
if no_lab > 0 or missing_science > 0 then
  error("[TANKS-BOBS] Science/lab coverage failed: missing_labs=" ..
      no_lab .. " missing_science=" .. missing_science)
end
log(string.format(
  "[TANKS-CI] BOBS_TECH_LAB_AUDIT technologies=%d lab_supported=%d " ..
  "no_lab=%d missing_science=%d",
  techs_checked, lab_supported, no_lab, missing_science))
