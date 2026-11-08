-- CI-only runtime harness. Injected into disposable mod folder.
local expected = require("ci_profile")
local wood_progression = require("scripts.wood_progression")
local vehicle_names = {
  "flame-tank", "auto-tank", "nade-tank", "rocket-tank",
  "mine-tank", "super-tank", "super-tank-alternate", "super-tank-wmd"
}

script.on_init(function()
  -- Factorio has one on_init callback per mod. Compose production startup
  -- instead of silently replacing it when this CI-only harness is appended.
  wood_progression.on_init()
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
  -- Factorio may invoke nth-tick handlers at tick zero. Require real
  -- simulation advancement before claiming a runtime proof.
  if event.tick < 300 then return end
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


-- Actual Factorio engine damage-response probe. Tests vehicle health/resistance
-- and destruction, not firing, ammunition depletion, targeting, or visual FX.
script.on_nth_tick(600, function(event)
  if event.tick < 600 then return end
  local surface = game.surfaces[1]
  if not (surface and surface.valid) then
    error("[TANKS-CI] No valid surface for damage response")
  end
  local found = surface.find_entities_filtered{name=vehicle_names, force="player"}
  if #found == 0 then
    error("[TANKS-CI] No surviving CI-created vehicles for engine damage test")
  end
  local vehicle = found[1]
  local before = vehicle.health or 0
  if before <= 0 then error("[TANKS-CI] Damage test vehicle has no health") end
  local dealt = vehicle.damage(100000, game.forces.enemy, "physical")
  local after = vehicle.valid and (vehicle.health or 0) or 0
  if after >= before then
    error("[TANKS-CI] Actual engine physical damage did not reduce vehicle health")
  end
  log("[TANKS-CI] DAMAGE_RESPONSE_PASS tick=" .. event.tick ..
    " before=" .. before .. " after=" .. after .. " engine_damage=" .. tostring(dealt))
  script.on_nth_tick(600, nil)
end)


-- Diagnostic vehicle-ammo inventory probe. Engine-verified insertion is NOT
-- proof that a driver can fire, that projectiles hit, or that ammo is consumed.
local ammo_pairs = {
  ["flame-tank"] = "flame-thrower-ammo-tanker",
  ["auto-tank"] = "45mm-auto",
  ["nade-tank"] = "50mm-mortar",
  ["mine-tank"] = "minepack",
  ["rocket-tank"] = "rocketpack",
  ["super-tank"] = "cannon-shell-2",
  ["super-tank-alternate"] = "minepack",
  ["super-tank-wmd"] = "tank-wmd-ammo",
}
script.on_nth_tick(900, function(event)
  if event.tick < 900 then return end
  local surface = game.surfaces[1]
  local tested, accepted, skipped = 0, 0, 0
  if not (surface and surface.valid) then
    log("[TANKS-CI] AMMO_INVENTORY_DIAG missing test surface")
    log("[TANKS-CI] AMMO_INVENTORY_CHECKED tick=" .. event.tick .. " attempted=0 accepted=0 skipped=8")
    script.on_nth_tick(900, nil)
    return
  end
  for name, ammo_name in pairs(ammo_pairs) do
    local entities = surface.find_entities_filtered{name=name, force="player"}
    local entity = entities[1]
    if entity and entity.valid then
      local inventory = entity.get_inventory(defines.inventory.car_ammo)
      if inventory and inventory.valid then
        tested = tested + 1
        local inserted = inventory.insert{name=ammo_name, count=5}
        if inserted > 0 and inventory.get_item_count(ammo_name) > 0 then
          accepted = accepted + 1
        else
          log("[TANKS-CI] AMMO_INVENTORY_DIAG rejected ammo=" .. ammo_name .. " vehicle=" .. name)
        end
      else
        skipped = skipped + 1
        log("[TANKS-CI] AMMO_INVENTORY_DIAG no ammo inventory on " .. name)
      end
    else
      skipped = skipped + 1
      log("[TANKS-CI] AMMO_INVENTORY_DIAG vehicle unavailable " .. name)
    end
  end
  log("[TANKS-CI] AMMO_INVENTORY_CHECKED tick=" .. event.tick ..
    " attempted=" .. tested .. " accepted=" .. accepted .. " skipped=" .. skipped)
  script.on_nth_tick(900, nil)
end)
