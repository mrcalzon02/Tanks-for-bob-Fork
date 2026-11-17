data:extend({
  -- Main Seablock production group
  {
    type = "item-group",
    name = "Seablock",
    icon = "__tanks_for_bob_fork__/graphics/icons/placeholder-org.png",
    icon_size = 64,
    order = "y",
    inventory_order = "y"
  },

  -- Seablock subgroups ordered from raw/basic processing to advanced intermediates
  {
    type = "item-subgroup",
    name = "Seablock",
    group = "Seablock",
    order = "a[seablock-base]",
  },
  {
    type = "item-subgroup",
    name = "fishery",
    group = "Seablock",
    order = "b[fishery]",
  },
  {
    type = "item-subgroup",
    name = "growing",
    group = "Seablock",
    order = "c[growing]",
  },
  {
    type = "item-subgroup",
    name = "clay",
    group = "Seablock",
    order = "d[clay]",
  },
  {
    type = "item-subgroup",
    name = "quarrying",
    group = "Seablock",
    order = "e[quarrying]",
  },
  {
    type = "item-subgroup",
    name = "pit-kiln",
    group = "Seablock",
    order = "f[pit-kiln]",
  },
  {
    type = "item-subgroup",
    name = "cooking",
    group = "Seablock",
    order = "g[cooking]",
  },
  {
    type = "item-subgroup",
    name = "advcooking",
    group = "Seablock",
    order = "h[advanced-cooking]",
  },
  {
    type = "item-subgroup",
    name = "Steam",
    group = "Seablock",
    order = "i[steam]",
  },
  {
    type = "item-subgroup",
    name = "Steam-Compressor",
    group = "Seablock",
    order = "j[steam-compressor]",
  },
  {
    type = "item-subgroup",
    name = "Calcifier",
    group = "Seablock",
    order = "k[calcifier]",
  },
  {
    type = "item-subgroup",
    name = "shaler",
    group = "Seablock",
    order = "l[shaler]",
  },

  -- Tank and vehicle group
  {
    type = "item-group",
    name = "tanks",
    icon = "__tanks_for_bob_fork__/graphics/icons/tank-group.png",
    icon_size = 64,
    order = "z",
    inventory_order = "z"
  },

  -- Tank subgroups ordered from components to vehicles and upgrades
  {
    type = "item-subgroup",
    name = "tank-ammo-components",
    group = "tanks",
    order = "a[ammo-components]",
  },
  {
    type = "item-subgroup",
    name = "tank-ammo",
    group = "tanks",
    order = "b[tank-ammo]",
  },
  {
    type = "item-subgroup",
    name = "tank-ammo-infantry",
    group = "tanks",
    order = "c[infantry-ammo]",
  },
  {
    type = "item-subgroup",
    name = "tank-vehicle",
    group = "tanks",
    order = "d[tank-vehicles]",
  },
  {
    type = "item-subgroup",
    name = "support-vehicles",
    group = "tanks",
    order = "e[support-vehicles]",
  },
  {
    type = "item-subgroup",
    name = "tank-vehicle-upgrades",
    group = "tanks",
    order = "f[vehicle-upgrades]",
  },
  {
    type = "item-subgroup",
    name = "super-tank-vehicle",
    group = "tanks",
    order = "z[super-tank-vehicles]",
  },
})
