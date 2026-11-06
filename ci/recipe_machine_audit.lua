-- Factorio 2.0 data-stage machine/recipe feasibility checks.
-- All checks run inside the existing single official Factorio test profile.
-- Unlike ingredient-only supply closure, these validate real machine
-- item-ingredient capacity and the required fluid directions.
local recipes = data.raw.recipe or {}
local machines = data.raw["assembling-machine"] or {}
local problems = {}
local checked = 0
local function problem(s) problems[#problems + 1] = s end
local function accepts(machine, category)
  for _, v in pairs(machine.crafting_categories or {}) do
    if v == category then return true end
  end
  return false
end
local function has_port(machine, wanted)
  for _, box in pairs(machine.fluid_boxes or {}) do
    if type(box) == "table" then
      local direction = box.production_type
      if direction == wanted or direction == "input-output" then
        for _, connection in pairs(box.pipe_connections or {}) do
          if connection.flow_direction == wanted or
              connection.flow_direction == "input-output" then
            return true
          end
        end
      end
    end
  end
  return false
end
local function verify(name, category, machine_name)
  checked = checked + 1
  local recipe, machine = recipes[name], machines[machine_name]
  if not recipe then problem("missing recipe " .. name) return end
  if not machine then problem("missing machine " .. machine_name) return end
  if (recipe.category or "crafting") ~= category or not accepts(machine, category) then
    problem(name .. " category cannot be selected on " .. machine_name)
    return
  end
  local item_kinds = 0
  local needs_input, needs_output = false, false
  for _, ingredient in pairs(recipe.ingredients or {}) do
    if ingredient.type == "fluid" then needs_input = true else item_kinds = item_kinds + 1 end
  end
  for _, result in pairs(recipe.results or {}) do
    if result.type == "fluid" then needs_output = true end
  end
  if item_kinds > (machine.ingredient_count or 0) then
    problem(name .. " requires " .. item_kinds .. " item types, " .. machine_name ..
      " only supports " .. tostring(machine.ingredient_count))
  end
  if needs_input and not has_port(machine, "input") then
    problem(name .. " fluid input missing from " .. machine_name)
  end
  if needs_output and not has_port(machine, "output") then
    problem(name .. " fluid output missing from " .. machine_name)
  end
end
for _, name in ipairs({
  "clay-pit", "wood-basin", "fish-pond", "quarry",
  "primitive-steam-powered-pump"
}) do verify(name, "Seablock", "workbench") end
for _, name in ipairs({"rendered-organics", "steam-meal"}) do
  verify(name, "advcooking", "cooking-fire")
end
for _, name in ipairs({"tank-ammo-industrial-coke", "Rubberized-timber"}) do
  verify(name, "tank-ammo-component", "tank-ammo-assembling-machine")
end
if #problems > 0 then
  for _, message in ipairs(problems) do log("[TANKS-CI] RECIPE_MACHINE_FAIL " .. message) end
  error("[TANKS-CI] " .. #problems .. " verified recipe/machine design problems")
end
log("[TANKS-CI] RECIPE_MACHINE_PASS audited=" .. checked ..
  " workbench=5 advcooking=2 tank_ammo=2")
