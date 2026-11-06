-- CI-only vehicle weapon, ammunition and item-placement topology audit.
-- This inspects prototypes, not actual firing, damage, or graphical animation.
local car = data.raw.car or {}
local guns = data.raw.gun or {}
local ammo = data.raw.ammo or {}
local recipes = data.raw.recipe or {}
local categories = data.raw["ammo-category"] or {}
local target_names = {
  "modular-tank", "flame-tank", "auto-tank", "nade-tank",
  "flame-tank-wlsk", "auto-tank-wlsk", "nade-tank-wlsk",
  "mine-tank", "rocket-tank", "super-tank", "super-tank-alternate",
  "super-tank-wmd", "car-flamer"
}
local warnings, weapon_count, linked_ammo, supported = {}, 0, 0, 0
local used_categories = {}
local ammo_by_category = {}
local craftable_ammo = {}
for _, recipe in pairs(recipes) do
  for _, product in pairs(recipe.results or {}) do
    if (product.type or "item") == "item" then
      craftable_ammo[product.name or product[1]] = true
    end
  end
  if recipe.result then craftable_ammo[recipe.result] = true end
end
for name, prototype in pairs(ammo) do
  local types = prototype.ammo_type
  if types then
    local records = (types.category and {types}) or types
    for _, record in pairs(records) do
      if type(record) == "table" and record.category then
        ammo_by_category[record.category] = ammo_by_category[record.category] or {}
        table.insert(ammo_by_category[record.category], name)
      end
    end
  end
end
local function flag(what)
  if #warnings < 160 then warnings[#warnings+1] = what end
end
for _, name in ipairs(target_names) do
  local vehicle = car[name]
  if not vehicle then
    flag("missing vehicle prototype " .. name)
  else
    supported = supported + 1
    local guns_on_vehicle = vehicle.guns or {}
    if #guns_on_vehicle == 0 then flag("vehicle has no gun: " .. name) end
    local item = (data.raw.item or {})[name] or (data.raw["item-with-entity-data"] or {})[name]
    if not item then
      flag("vehicle has no placeable item prototype: " .. name)
    elseif item.place_result ~= name then
      flag("vehicle item place_result differs: " .. name)
    end
    if vehicle.minable and vehicle.minable.result and vehicle.minable.result ~= name then
      flag("vehicle mining result is unexpected: " .. name .. " => " .. vehicle.minable.result)
    end
    for _, gun_name in pairs(guns_on_vehicle) do
      weapon_count = weapon_count + 1
      local gun = guns[gun_name]
      if not gun then
        flag("vehicle references missing gun: " .. name .. " => " .. tostring(gun_name))
      else
        local p = gun.attack_parameters or {}
        local category = p.ammo_category
        if not category then
          flag("gun has no ammo category: " .. gun_name)
        else
          used_categories[category] = true
          if not categories[category] then
            flag("gun category unregistered: " .. gun_name .. " => " .. category)
          end
          if not ammo_by_category[category] or #ammo_by_category[category] == 0 then
            flag("no ammo prototype available for gun " .. gun_name .. " / category " .. category)
          else
            linked_ammo = linked_ammo + 1
          end
        end
      end
    end
  end
end
local ammo_count, ammo_with_craft_recipe = 0, 0
for name in pairs(ammo) do
  if name:find("tank") or name:find("mm%-") or name:find("rocketpack")
     or name:find("minepack") or name:find("flame%-thrower%-ammo%-tanker") then
    ammo_count = ammo_count + 1
    if craftable_ammo[name] then
      ammo_with_craft_recipe = ammo_with_craft_recipe + 1
    else
      flag("mod-named ammo has no detected crafting output: " .. name)
    end
  end
end
local category_count = 0
for _ in pairs(used_categories) do category_count = category_count + 1 end
log(("[TANKS-CI] WEAPON_AUDIT vehicles=%d gun_slots=%d supported_categories=%d ammo_links=%d named_ammo=%d named_ammo_craftable=%d warnings=%d"):format(
  supported, weapon_count, category_count, linked_ammo, ammo_count, ammo_with_craft_recipe, #warnings))
for i, message in ipairs(warnings) do
  if i > 80 then break end
  log("[TANKS-CI] WEAPON_WARNING " .. message)
end
if #warnings > 80 then log("[TANKS-CI] WEAPON_WARNINGS_ADDITIONAL " .. (#warnings - 80)) end
-- True firing compatibility requires runtime driver, ammo and target scenarios.
log("[TANKS-CI] WEAPON_AUDIT_PASS data-stage registry inspected (shots not yet fired)")
