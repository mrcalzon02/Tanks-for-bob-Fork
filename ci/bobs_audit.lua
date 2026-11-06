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
log(string.format(
  "[TANKS-CI] BOBS_TECH_LAB_AUDIT technologies=%d lab_supported=%d " ..
  "no_lab=%d missing_science=%d",
  techs_checked, lab_supported, no_lab, missing_science))
