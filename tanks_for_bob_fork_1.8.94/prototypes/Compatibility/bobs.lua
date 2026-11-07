-- Optional Bob's vehicle equipment integration for Tanks for Bob Fork.
-- Invoked in data-final-fixes, after Bob's own data-updates and equipment grids.
-- All assignments are restricted to this fork's vehicle prototypes.
if not (mods and mods["bobvehicleequipment"]) then return end

local own_setting = settings.startup["tfbf-bobs-equipment-grids"]
if not own_setting or own_setting.value ~= true then return end

-- Respect Bob's own enable/disable switch; do not recreate grids when off.
local bob_setting = settings.startup["bobmods-vehicleequipment-enablevehiclegrids"]
if not bob_setting or bob_setting.value ~= true then return end

local vehicles = data.raw.car or {}
local grids = data.raw["equipment-grid"] or {}

-- From Bob's actual grid definitions:
-- bob-car: 8x2; bob-tank: 6x8; bob-tank-2: 6x10; bob-tank-3: 6x12.
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
  ["super-tank-wmd"] = "bob-tank-3",
}

for vehicle_name, grid_name in pairs(assignments) do
  local vehicle = vehicles[vehicle_name]
  if vehicle and grids[grid_name] then
    vehicle.equipment_grid = grid_name
  end
end
