data:extend(
{
--flame-thrower-ammo-tanker
  {
    type = "recipe",
    name = "flame-thrower-ammo-tanker",
    enabled = "false",
	  category = "tank-ammo-component",
    energy_required = 10,
    ingredients =
    {
       {"tank-ammo-casing", 4},
	     {"flamethrower-ammo", 15}
    },
    result = "flame-thrower-ammo-tanker",
  },
--flame-thrower-ammo-tanker-2
  {
    type = "recipe",
    name = "flame-thrower-ammo-tanker-2",
    enabled = "false",
	  category = "tank-ammo-component",
    energy_required = 10,
    ingredients =
    {
      {"flame-thrower-ammo-tanker", 7},
    },
    result = "flame-thrower-ammo-tanker-2",
  },
--ap-bullet-brick
  {
    type = "recipe",
    name = "ap-bullet-brick",
    enabled = "false",
	category = "tank-ammo-component",
    energy_required = 15,
    ingredients =
    {
      {"tank-ammo-casing", 3},
      {"tank-ammo-universal-explosive", 3}
    },
    result = "ap-bullet-brick",
  },
--ap-bullet-brick
  {
    type = "recipe",
    name = "piercing-shotgun-shell-brick",
    enabled = "false",
	category = "tank-ammo-component",
    energy_required = 15,
    ingredients =
    {
      {"tank-ammo-casing", 4},
      {"tank-ammo-universal-explosive", 4}
    },
     result = "piercing-shotgun-shell-brick",
  },
--45mm-auto
  {
    type = "recipe",
    name = "45mm-auto",
    enabled = "false",
	category = "tank-ammo-component",
    energy_required = 7,
    ingredients =
    {
      {"tank-ammo-casing", 6},
      {"tank-ammo-universal-explosive", 2}
    },
    result = "45mm-auto"
  },  
--50mm-mortar
  {
    type = "recipe",
    name = "50mm-mortar",
    enabled = "false",
	category = "tank-ammo-component",
    energy_required = 10,
    ingredients =
    {
      {"tank-ammo-casing", 2},
      {"tank-ammo-universal-explosive", 6}
    },
    result = "50mm-mortar"
  },
--50mm-mortar-poison
  {
    type = "recipe",
    name = "50mm-mortar-poison",
    enabled = "false",
	category = "tank-ammo-component",
    energy_required = 15,
    ingredients =
    {
	  {"electronic-circuit", 5},
      {"tank-ammo-casing", 2},
      {"tank-ammo-universal-explosive", 3}
    },
    result = "50mm-mortar-poison"
  },
--tank-mine-ammo
  {
    type = "recipe",
    name = "minepack",
    enabled = "false",
	category = "tank-ammo-component",
    energy_required = 20,
    ingredients =
    {
      {"tank-ammo-casing", 5},
      {"tank-ammo-universal-explosive", 5}
    },
    result = "minepack"
  }, 
--tank-mine-ammo-poison
  {
    type = "recipe",
    name = "minepack-poison",
    enabled = "false",
	category = "tank-ammo-component",
    energy_required = 30,
    ingredients =
    {
      {"tank-ammo-casing", 6},
      {"tank-ammo-universal-explosive", 6}
    },
    result = "minepack-poison"
  }, 
--rocketpack
  {
    type = "recipe",
    name = "rocketpack",
    enabled = "false",
	category = "tank-ammo-component",
    energy_required = 20,
    ingredients =
    {
	  {"electronic-circuit", 15},
      {"tank-ammo-casing", 8},
      {"tank-ammo-universal-explosive", 8}
    },
    result = "rocketpack"
  }, 
--cannon-shell-2
  {
    type = "recipe",
    name = "cannon-shell-2",
    enabled = "false",
	category = "tank-ammo-component",
    energy_required = 5,
    ingredients =
    {
      {"tank-ammo-casing", 2},
      {"tank-ammo-universal-explosive", 2}
    },
     result = "cannon-shell-2"
  }, 
  --wmdartillery-ammo
  {
    type = "recipe",
    name = "wmdartillery-ammo",
    enabled = "false",
	category = "tank-ammo-component",
    energy_required = 3160,
	icon = "__tanks_for_bob_fork__/graphics/icons/nuke-artillery-shell2.png",
	icon_size = 64,
	emissions_multiplier = 9,
    ingredients =
    {
	  {"processing-unit", 15},
      {"tank-wmd-ammo", 1},
      {"tank-ammo-reinforced-casing", 25},
      {"tank-ammo-universal-explosive", 30},
        },
    results=
    {
	  {type="item", name="wmdartillery-ammo", amount=8},
    },
   },
--tank-wmd-ammo
  {
    type = "recipe",
    name = "tank-wmd-ammo",
    enabled = "false",
	category = "tank-ammo-component",
	    subgroup = "tank-ammo-infantry",
    energy_required = 3160,
	icon = "__tanks_for_bob_fork__/graphics/icons/tank-ammo-wmd.png",
	icon_size = 64,
	emissions_multiplier = 9,
    ingredients =
    {
	  {"processing-unit", 15},
      {"tank-ammo-casing", 25},
      {"tank-ammo-reinforced-casing", 25},
      {"tank-ammo-universal-explosive", 30},
	  {"uranium-ore", 15},
        },
    results=
    {
      {type="item", name="tank-wmd-ammo", amount=2},
	  {type="item", name="tank-ammo-Radioactivewaste", amount=14},
    },
  },
  --convert shell
  {
    type = "recipe",
    name = "cannon-shell-convert",
    enabled = "false",
	category = "tank-ammo-component",
    energy_required = 5.5,
    ingredients =
    {
      {"cannon-shell", 1},
    },
     result = "cannon-shell-2"
	
  },
 }
)