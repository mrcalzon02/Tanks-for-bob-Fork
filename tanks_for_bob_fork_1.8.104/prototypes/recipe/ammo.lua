data:extend({

-- flame-thrower-ammo-tanker
{
  type = "recipe",
  name = "flame-thrower-ammo-tanker",
  enabled = false,
  category = "tank-ammo-component",
  energy_required = 10,
  ingredients =
  {
    {type="item", name="tank-ammo-casing", amount=4},
    {type="item", name="flamethrower-ammo", amount=15}
  },
  results =
  {
    {type="item", name="flame-thrower-ammo-tanker", amount=1}
  }
},

-- flame-thrower-ammo-tanker-2
{
  type = "recipe",
  name = "flame-thrower-ammo-tanker-2",
  enabled = false,
  category = "tank-ammo-component",
  energy_required = 10,
  ingredients =
  {
    {type="item", name="flame-thrower-ammo-tanker", amount=7}
  },
  results =
  {
    {type="item", name="flame-thrower-ammo-tanker-2", amount=1}
  }
},

-- ap-bullet-brick
{
  type = "recipe",
  name = "ap-bullet-brick",
  enabled = false,
  category = "tank-ammo-component",
  energy_required = 15,
  ingredients =
  {
    {type="item", name="tank-ammo-casing", amount=3},
    {type="item", name="tank-ammo-universal-explosive", amount=3}
  },
  results = {{type="item", name="ap-bullet-brick", amount=1}}
},

-- piercing-shotgun-shell-brick
{
  type = "recipe",
  name = "piercing-shotgun-shell-brick",
  enabled = false,
  category = "tank-ammo-component",
  energy_required = 15,
  ingredients =
  {
    {type="item", name="tank-ammo-casing", amount=4},
    {type="item", name="tank-ammo-universal-explosive", amount=4}
  },
  results = {{type="item", name="piercing-shotgun-shell-brick", amount=1}}
},

-- 45mm-auto
{
  type = "recipe",
  name = "45mm-auto",
  enabled = false,
  category = "tank-ammo-component",
  energy_required = 7,
  ingredients =
  {
    {type="item", name="tank-ammo-casing", amount=6},
    {type="item", name="tank-ammo-universal-explosive", amount=2}
  },
  results = {{type="item", name="45mm-auto", amount=1}}
},

-- 50mm-mortar
{
  type = "recipe",
  name = "50mm-mortar",
  enabled = false,
  category = "tank-ammo-component",
  energy_required = 10,
  ingredients =
  {
    {type="item", name="tank-ammo-casing", amount=2},
    {type="item", name="tank-ammo-universal-explosive", amount=6}
  },
  results = {{type="item", name="50mm-mortar", amount=1}}
},

-- 50mm-mortar-poison
{
  type = "recipe",
  name = "50mm-mortar-poison",
  enabled = false,
  category = "tank-ammo-component",
  energy_required = 15,
  ingredients =
  {
    {type="item", name="electronic-circuit", amount=5},
    {type="item", name="tank-ammo-casing", amount=2},
    {type="item", name="tank-ammo-universal-explosive", amount=3}
  },
  results = {{type="item", name="50mm-mortar-poison", amount=1}}
},

-- minepack
{
  type = "recipe",
  name = "minepack",
  enabled = false,
  category = "tank-ammo-component",
  energy_required = 20,
  ingredients =
  {
    {type="item", name="tank-ammo-casing", amount=5},
    {type="item", name="tank-ammo-universal-explosive", amount=5}
  },
  results = {{type="item", name="minepack", amount=1}}
},

-- minepack-poison
{
  type = "recipe",
  name = "minepack-poison",
  enabled = false,
  category = "tank-ammo-component",
  energy_required = 30,
  ingredients =
  {
    {type="item", name="tank-ammo-casing", amount=6},
    {type="item", name="tank-ammo-universal-explosive", amount=6}
  },
  results = {{type="item", name="minepack-poison", amount=1}}
},

-- rocketpack
{
  type = "recipe",
  name = "rocketpack",
  enabled = false,
  category = "tank-ammo-component",
  energy_required = 20,
  ingredients =
  {
    {type="item", name="electronic-circuit", amount=15},
    {type="item", name="tank-ammo-casing", amount=8},
    {type="item", name="tank-ammo-universal-explosive", amount=8}
  },
  results = {{type="item", name="rocketpack", amount=1}}
},

-- cannon-shell-2
{
  type = "recipe",
  name = "cannon-shell-2",
  enabled = false,
  category = "tank-ammo-component",
  energy_required = 5,
  ingredients =
  {
    {type="item", name="tank-ammo-casing", amount=2},
    {type="item", name="tank-ammo-universal-explosive", amount=2}
  },
  results = {{type="item", name="cannon-shell-2", amount=1}}
},

-- wmdartillery-ammo
{
  type = "recipe",
  name = "wmdartillery-ammo",
  enabled = false,
  category = "tank-ammo-component",
  energy_required = 3160,
  icon = "__tanks_for_bob_fork__/graphics/icons/nuke-artillery-shell2.png",
  icon_size = 64,
  emissions_multiplier = 9,
  ingredients =
  {
    {type="item", name="processing-unit", amount=15},
    {type="item", name="tank-wmd-ammo", amount=1},
    {type="item", name="tank-ammo-reinforced-casing", amount=25},
    {type="item", name="tank-ammo-universal-explosive", amount=30}
  },
  results =
  {
    {type="item", name="wmdartillery-ammo", amount=8}
  }
},

-- tank-wmd-ammo
{
  type = "recipe",
  name = "tank-wmd-ammo",
  enabled = false,
  category = "tank-ammo-component",
  subgroup = "tank-ammo-infantry",
  energy_required = 3160,
  icon = "__tanks_for_bob_fork__/graphics/icons/tank-ammo-wmd.png",
  icon_size = 64,
  emissions_multiplier = 9,
  ingredients =
  {
    {type="item", name="processing-unit", amount=15},
    {type="item", name="tank-ammo-casing", amount=25},
    {type="item", name="tank-ammo-reinforced-casing", amount=25},
    {type="item", name="tank-ammo-universal-explosive", amount=30},
    {type="item", name="uranium-ore", amount=15}
  },
  results =
  {
    {type="item", name="tank-wmd-ammo", amount=2},
    {type="item", name="tank-ammo-Radioactivewaste", amount=14}
  }
},

-- cannon-shell-convert
{
  type = "recipe",
  name = "cannon-shell-convert",
  enabled = false,
  category = "tank-ammo-component",
  energy_required = 5.5,
  ingredients =
  {
    {type="item", name="cannon-shell", amount=1}
  },
  results =
  {
    {type="item", name="cannon-shell-2", amount=1}
  }
}

})