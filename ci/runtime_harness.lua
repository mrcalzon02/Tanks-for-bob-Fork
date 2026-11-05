-- CI only: installed in temporary mod copy; not part of the published mod.
local vehicles = {"flame-tank", "auto-tank", "rocket-tank", "super-tank"}
local allowed = {core = true, base = true, tanks_for_bob_fork = true}
script.on_init(function()
  for name in pairs(script.active_mods) do
    if not allowed[name] then error("[TANKS-CI] Unexpected enabled mod: " .. name) end
  end
  for _, name in ipairs(vehicles) do
    if not prototypes.entity[name] then
      error("[TANKS-CI] Missing runtime vehicle: " .. name)
    end
    if not prototypes.recipe[name] then
      error("[TANKS-CI] Missing runtime recipe: " .. name)
    end
  end
  log("[TANKS-CI] INIT_PASS no third-party mods; vehicle and recipe registry valid")
end)
script.on_nth_tick(300, function(event)
  local surface = game.surfaces[1]
  if not (surface and surface.valid) then
    error("[TANKS-CI] No valid runtime surface")
  end
  local spawned = 0
  for i, name in ipairs(vehicles) do
    local position = surface.find_non_colliding_position(name, {x = i * 12, y = 0}, 128, 2)
    if position then
      local vehicle = surface.create_entity{name = name, position = position, force = "player"}
      if not (vehicle and vehicle.valid) then
        error("[TANKS-CI] Failed to create vehicle: " .. name)
      end
      spawned = spawned + 1
    else
      log("[TANKS-CI] WARNING no safe placement for " .. name)
    end
  end
  if spawned == 0 then error("[TANKS-CI] No test vehicles could be placed") end
  log("[TANKS-CI] RUNTIME_PASS tick=" .. event.tick .. " vehicles_spawned=" .. spawned)
  script.on_nth_tick(300, nil)
end)
