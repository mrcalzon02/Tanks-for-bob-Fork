data:extend(
{
--flame-tank
  {
    type = "recipe",
    name = "flame-tank",
    enabled = "false",
    category = "tank-crafting",
    energy_required = 145,
    ingredients =
    {
      {"DuplexedSpervingArm", 15},
      {"Encabulator", 15},
      {"tank", 1},
      {"advanced-circuit", 15}
    },
    result = "flame-tank"
  },
--auto-tank
  {
    type = "recipe",
    name = "auto-tank",
    enabled = "false",
    category = "tank-crafting",
    energy_required = 145,
    ingredients =
    {
      {"Encabulator", 30},
      {"tank", 1},
      {"SpervingArm", 10},
      {"advanced-circuit", 25}
    },
    result = "auto-tank"
  },
--nade-tank
  {
    type = "recipe",
    name = "nade-tank",
    enabled = "false",
  category = "tank-crafting",

  energy_required = 45,
    ingredients =
    {
      {"engine-unit", 25},
      {"tank", 1},
      {"SpervingArm", 80},
      {"advanced-circuit", 15}
    },
    result = "nade-tank"
  },
--flame-tank-wlsk
  {
    type = "recipe",
    name = "flame-tank-wlsk",
    enabled = "false",
  category = "tank-crafting",

  energy_required = 105,
    ingredients =
    {
      {"tank-light-chasis-wlsk", 1},
      {"flame-tank", 1}
    },
    result = "flame-tank-wlsk"
  },
--auto-tank-wlsk
  {
    type = "recipe",
    name = "auto-tank-wlsk",
    enabled = "false",
  category = "tank-crafting",

  energy_required = 105,
    ingredients =
    {
      {"tank-light-chasis-wlsk", 1},
      {"auto-tank", 1}
      --{"iron-gear-wheel", 1},
      --{"electronic-circuit", 1}
    },
    result = "auto-tank-wlsk"
  },
--nade-tank-wlsk
  {
    type = "recipe",
    name = "nade-tank-wlsk",
    enabled = "false",
  category = "tank-crafting",
  energy_required = 105,
    ingredients =
    {
      {"tank-light-chasis-wlsk", 1},
      {"nade-tank", 1}
      --{"iron-gear-wheel", 1},
      --{"electronic-circuit", 1}
    },
    result = "nade-tank-wlsk"
  },
--mine-tank
  {
    type = "recipe",
    name = "mine-tank",
    enabled = "false",
  category = "tank-crafting",
  energy_required = 600,
    ingredients =
    {
      {"tank", 1},
      {"SpervingArm", 70},
      {"DuctedSpervingArm", 40},
      {"advanced-circuit", 25}
    },
    result = "mine-tank"
  },
--rocket-tank
  {
    type = "recipe",
    name = "rocket-tank",
    enabled = "false",
  category = "tank-crafting",
  energy_required = 260,
    ingredients =
    {
      {"tank", 1},
      {"SpervingArm", 35},
      {"DuctedSpervingArm", 20},
      {"advanced-circuit", 45}
    },
    result = "rocket-tank"
  },
--super-tank A
  {
    type = "recipe",
    name = "super-tank",
    enabled = "false",
  category = "tank-crafting",
  energy_required = 2500,
    ingredients =
    {
      {"tank", 1},
      {"SpervingArm", 75},
      {"DuplexedSpervingArm", 40},
      {"advanced-circuit", 15}
    },
    result = "super-tank"
  },
--super-tank B
  {
    type = "recipe",
    name = "super-tank-alternate",
    enabled = "false",
  category = "tank-crafting",
  energy_required = 1000,
    ingredients =
    {
      {"electric-engine-unit", 30},
      {"DuctedSpervingArm", 75},
      {"tank", 1},
      {"advanced-circuit", 15}
    },
    result = "super-tank-alternate"
  },
--super-tank C
  {
    type = "recipe",
    name = "super-tank-wmd",
    enabled = "false",
  category = "tank-crafting",
  energy_required = 3040,
    ingredients =
    {
      {"electric-engine-unit", 30},
      {"DuplexedSpervingArm", 25},
      {"tank",1},
      {"advanced-circuit", 15}
    },
    result = "super-tank-wmd"
  },
-- Car flamer  
  {
    type = "recipe",
    name = "car-flamer",
    enabled = "false",
  category = "tank-crafting",
  energy_required = 125,
    ingredients =
    {
      {"car", 1},
      {"DuplexedSpervingArm", 20},
      {"steel-plate", 10}
    },
    result = "car-flamer"
  }
 }
)