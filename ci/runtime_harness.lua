-- CI-only runtime harness. Injected into disposable mod folder.
local expected = require("ci_profile")
local vehicle_names = {
  "flame-tank", "auto-tank", "nade-tank", "rocket-tank",
  "mine-tank", "super-tank", "super-tank-alternate", "super-tank-wmd"
}

script.on_init(function()
  local active = script.active_mods
  for name in pairs(active) do
    if name ~= "core" and not expected[name] and name ~= "tanks_for_bob_fork" then
      error("[TANKS-CI] Unexpected enabled mod: " .. name)
    end
  end
  for name in pairs(expected) do
    if not active[name] then
      error("[TANKS-CI] Required official mod not active: " .. name)
    end
  end
  for _, name in ipairs(vehicle_names) do
    if not prototypes.entity[name] then
      error("[TANKS-CI] Missing runtime vehicle entity: " .. name)
    end
    if not prototypes.recipe[name] then
      error("[TANKS-CI] Missing runtime vehicle recipe: " .. name)
    end
  end
  log("[TANKS-CI] INIT_PASS correct official mod profile and vehicle/recipe runtime registries")
end)

script.on_nth_tick(300, function(event)
  local surface = game.surfaces[1]
  if not (surface and surface.valid) then
    error("[TANKS-CI] No valid game surface")
  end
  local count = 0
  for i, name in ipairs(vehicle_names) do
    local position = surface.find_non_colliding_position(name, {x = i * 12, y = 0}, 128, 2)
    if position then
      local vehicle = surface.create_entity{name = name, position = position, force = "player"}
      if not (vehicle and vehicle.valid) then
        error("[TANKS-CI] Cannot spawn vehicle: " .. name)
      end
      count = count + 1
    else
      log("[TANKS-CI] WARNING no clear map location for " .. name)
    end
  end
  if count == 0 then error("[TANKS-CI] Could not spawn any vehicle") end
  log("[TANKS-CI] RUNTIME_PASS tick=" .. event.tick .. " vehicles_spawned=" .. count)
  script.on_nth_tick(300, nil)
end)
