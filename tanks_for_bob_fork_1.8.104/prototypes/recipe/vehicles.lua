data:extend({

-- flame-tank
{
  type = "recipe",
  name = "flame-tank",
  enabled = false,
  category = "tank-crafting",
  energy_required = 145,
  ingredients =
  {
    {type = "item", name = "DuplexedSpervingArm", amount = 15},
    {type = "item", name = "Encabulator", amount = 15},
    {type = "item", name = "tank", amount = 1},
    {type = "item", name = "advanced-circuit", amount = 15}
  },
  results = {{type = "item", name = "flame-tank", amount = 1}}
},

-- auto-tank
{
  type = "recipe",
  name = "auto-tank",
  enabled = false,
  category = "tank-crafting",
  energy_required = 145,
  ingredients =
  {
    {type = "item", name = "Encabulator", amount = 30},
    {type = "item", name = "tank", amount = 1},
    {type = "item", name = "SpervingArm", amount = 10},
    {type = "item", name = "advanced-circuit", amount = 25}
  },
  results = {{type = "item", name = "auto-tank", amount = 1}}
},

-- nade-tank
{
  type = "recipe",
  name = "nade-tank",
  enabled = false,
  category = "tank-crafting",
  energy_required = 45,
  ingredients =
  {
    {type = "item", name = "engine-unit", amount = 25},
    {type = "item", name = "tank", amount = 1},
    {type = "item", name = "SpervingArm", amount = 80},
    {type = "item", name = "advanced-circuit", amount = 15}
  },
  results = {{type = "item", name = "nade-tank", amount = 1}}
},

-- flame-tank-wlsk
{
  type = "recipe",
  name = "flame-tank-wlsk",
  enabled = false,
  category = "tank-crafting",
  energy_required = 105,
  ingredients =
  {
    {type = "item", name = "tank-light-chasis-wlsk", amount = 1},
    {type = "item", name = "flame-tank", amount = 1}
  },
  results = {{type = "item", name = "flame-tank-wlsk", amount = 1}}
},

-- auto-tank-wlsk
{
  type = "recipe",
  name = "auto-tank-wlsk",
  enabled = false,
  category = "tank-crafting",
  energy_required = 105,
  ingredients =
  {
    {type = "item", name = "tank-light-chasis-wlsk", amount = 1},
    {type = "item", name = "auto-tank", amount = 1}
  },
  results = {{type = "item", name = "auto-tank-wlsk", amount = 1}}
},

-- nade-tank-wlsk
{
  type = "recipe",
  name = "nade-tank-wlsk",
  enabled = false,
  category = "tank-crafting",
  energy_required = 105,
  ingredients =
  {
    {type = "item", name = "tank-light-chasis-wlsk", amount = 1},
    {type = "item", name = "nade-tank", amount = 1}
  },
  results = {{type = "item", name = "nade-tank-wlsk", amount = 1}}
},

-- mine-tank
{
  type = "recipe",
  name = "mine-tank",
  enabled = false,
  category = "tank-crafting",
  energy_required = 600,
  ingredients =
  {
    {type = "item", name = "tank", amount = 1},
    {type = "item", name = "SpervingArm", amount = 70},
    {type = "item", name = "DuctedSpervingArm", amount = 40},
    {type = "item", name = "advanced-circuit", amount = 25}
  },
  results = {{type = "item", name = "mine-tank", amount = 1}}
},

-- rocket-tank
{
  type = "recipe",
  name = "rocket-tank",
  enabled = false,
  category = "tank-crafting",
  energy_required = 260,
  ingredients =
  {
    {type = "item", name = "tank", amount = 1},
    {type = "item", name = "SpervingArm", amount = 35},
    {type = "item", name = "DuctedSpervingArm", amount = 20},
    {type = "item", name = "advanced-circuit", amount = 45}
  },
  results = {{type = "item", name = "rocket-tank", amount = 1}}
},

-- super-tank A
{
  type = "recipe",
  name = "super-tank",
  enabled = false,
  category = "tank-crafting",
  energy_required = 2500,
  ingredients =
  {
    {type = "item", name = "tank", amount = 1},
    {type = "item", name = "SpervingArm", amount = 75},
    {type = "item", name = "DuplexedSpervingArm", amount = 40},
    {type = "item", name = "advanced-circuit", amount = 15}
  },
  results = {{type = "item", name = "super-tank", amount = 1}}
},

-- super-tank B
{
  type = "recipe",
  name = "super-tank-alternate",
  enabled = false,
  category = "tank-crafting",
  energy_required = 1000,
  ingredients =
  {
    {type = "item", name = "electric-engine-unit", amount = 30},
    {type = "item", name = "DuctedSpervingArm", amount = 75},
    {type = "item", name = "tank", amount = 1},
    {type = "item", name = "advanced-circuit", amount = 15}
  },
  results = {{type = "item", name = "super-tank-alternate", amount = 1}}
},

-- super-tank C
{
  type = "recipe",
  name = "super-tank-wmd",
  enabled = false,
  category = "tank-crafting",
  energy_required = 3040,
  ingredients =
  {
    {type = "item", name = "electric-engine-unit", amount = 30},
    {type = "item", name = "DuplexedSpervingArm", amount = 25},
    {type = "item", name = "tank", amount = 1},
    {type = "item", name = "advanced-circuit", amount = 15}
  },
  results = {{type = "item", name = "super-tank-wmd", amount = 1}}
},

-- car-flamer
{
  type = "recipe",
  name = "car-flamer",
  enabled = false,
  category = "tank-crafting",
  energy_required = 125,
  ingredients =
  {
    {type = "item", name = "car", amount = 1},
    {type = "item", name = "DuplexedSpervingArm", amount = 20},
    {type = "item", name = "steel-plate", amount = 10}
  },
  results = {{type = "item", name = "car-flamer", amount = 1}}
}

})