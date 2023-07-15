data:extend(
{ 
  {
    type = "technology",
    name = "Encabulation-research",
    icon = "__tanks_for_bob_fork__/graphics/icons/Encabulator.png",
    icon_size = 64,
    effects =
    {
      {
        type = "unlock-recipe",
        recipe = "tank-ammo-casing"
      },
       {
        type = "unlock-recipe",
        recipe = "Alumatedplate"
      },
      {
        type = "unlock-recipe",
        recipe = "tank-ammo-reinforced-casing"
      },
   {
        type = "unlock-recipe",
        recipe = "Encabulator"
      },
	     {
        type = "unlock-recipe",
        recipe = "SpervingArm"
      },
       {
        type = "unlock-recipe",
        recipe = "ore-from-waste"
      },
    },
    prerequisites = {"automation"},
    unit =
    {
      count = 10,
      ingredients = {{"automation-science-pack", 1}},
      time = 10
    },
    ignore_tech_cost_multiplier = true,
    order = "a-b-a"
  },
  {
    type = "technology",
    name = "Turbo-Encabulation-research",
    icon = "__tanks_for_bob_fork__/graphics/icons/TurboEncabulator.png",
    icon_size = 64,
    effects =
    {
      {
        type = "unlock-recipe",
        recipe = "tank-ammo-Explosive Engineering"
      },
     {
        type = "unlock-recipe",
        recipe = "TurboEncabulator"
      },
	       {
        type = "unlock-recipe",
        recipe = "DuctedSpervingArm"
      },
      {
        type = "unlock-recipe",
        recipe = "tank-ammo-universal-explosive"
      },
    },
    prerequisites = {"Encabulation-research","oil-processing"},
    unit =
    {
      count = 10*1,
      ingredients = {{"automation-science-pack", 1}},
      time = 10
    },
    order = "a-b-c"
  },
  {
    type = "technology",
    name = "organic-explosives",
    icon = "__tanks_for_bob_fork__/graphics/icons/universal-explosive.png",
    icon_size = 64,
    effects =
    {
      {
        type = "unlock-recipe",
        recipe = "tank-ammo-universal-explosive-synthetic"
      },
      {
        type = "unlock-recipe",
        recipe = "tank-ammo-explosive-synthetic"
      },
      {
        type = "unlock-recipe",
        recipe = "tank-ammo-ecozone"
      },
    },
    prerequisites = {"Turbo-Encabulation-research","explosives"},
    unit =
    {
      count = 10*1,
      ingredients = {{"automation-science-pack", 1}},
      time = 10
    },
    order = "a-b-c"
  },
  {
    type = "technology",
    name = "Hyper-Encabulation-research",
    icon = "__tanks_for_bob_fork__/graphics/icons/HyperEncabulator.png",
    icon_size = 64,
    effects =
    {
      {
        type = "unlock-recipe",
        recipe = "Rubberized-timber"
      },
       {
        type = "unlock-recipe",
        recipe = "HyperEncabulator"
      },
         {
        type = "unlock-recipe",
        recipe = "FramulatedEncabulator"
      },
         {
        type = "unlock-recipe",
        recipe = "DuplexedSpervingArm"
      },
      {
        type = "unlock-recipe",
        recipe = "tank-ammo-industrial-coke"
      },
        {
        type = "unlock-recipe",
        recipe = "ore-from-wasteb"
      },
        {
        type = "unlock-recipe",
        recipe = "ore-from-waster"
      },
    },
    prerequisites = {"organic-explosives"},
    unit =
    {
      count = 30*1,
      ingredients = {{"automation-science-pack", 1}},
      time = 15
    },
    ignore_tech_cost_multiplier = true,
    order = "a-b-c"
  },
  {
    type = "technology",
    name = "modular-tank-research",
    icon = "__tanks_for_bob_fork__/graphics/icons/modular-tank-research.png",
    icon_size = 64,
    effects =
    {
      {
        type = "unlock-recipe",
        recipe = "tank-assembling-machine"
      },
      {
        type = "unlock-recipe",
        recipe = "tank-ammo-assembling-machine"
      },    
      {
        type = "unlock-recipe",
        recipe = "flame-thrower-ammo-tanker"
      },
      {
        type = "unlock-recipe",
        recipe = "flame-thrower-ammo-tanker-2"
      },
      {
        type = "unlock-recipe",
        recipe = "45mm-auto"
      },
      {
        type = "unlock-recipe",
        recipe = "50mm-mortar"
      },
      {
        type = "unlock-recipe",
        recipe = "cannon-shell-2"
      },
      {
        type = "unlock-recipe",
        recipe = "cannon-shell-convert"
      },
      {
        type = "unlock-recipe",
        recipe = "flame-tank"
      },
      {
        type = "unlock-recipe",
        recipe = "auto-tank"
      },
      {
        type = "unlock-recipe",
        recipe = "nade-tank"
      },
      {
        type = "unlock-recipe",
        recipe = "car-flamer"
      }
    },
    prerequisites = {"tank","Encabulation-research"},
    unit =
    {
      count = 40*1,
      ingredients = {{"automation-science-pack", 2}, {"logistic-science-pack", 2}, {"military-science-pack", 3}},
      time = 105
    },
    ignore_tech_cost_multiplier = true,
    order = "a-b-c"
  },
  {
    type = "technology",
    name = "modular-tank-research2",
    icon = "__tanks_for_bob_fork__/graphics/icons/modular-tank-research.png",
    icon_size = 64,
    effects =
    {
      {
        type = "unlock-recipe",
        recipe = "tank-light-chasis-wlsk"
      },
      {
        type = "unlock-recipe",
        recipe = "flame-tank-wlsk"
      },
      {
        type = "unlock-recipe",
        recipe = "auto-tank-wlsk"
      },
      {
        type = "unlock-recipe",
        recipe = "nade-tank-wlsk"
      },
    },
    prerequisites = {"automation-2", "modular-tank-research"},
    unit =
    {
      count = 40*1,
      ingredients = {{"automation-science-pack", 3}, {"logistic-science-pack", 3}, {"military-science-pack", 3}},
      time = 105
    },
    ignore_tech_cost_multiplier = true,
    order = "a-b-c"
  },
  {
    type = "technology",
    name = "modular-tank-research3",
    icon = "__tanks_for_bob_fork__/graphics/icons/modular-tank-research.png",
    icon_size = 64,
    effects =
    {
      {
        type = "unlock-recipe",
        recipe = "mine-tank"
      },
      {
        type = "unlock-recipe",
        recipe = "minepack"
      },
      {
        type = "unlock-recipe",
        recipe = "rocket-tank"
      },
      {
        type = "unlock-recipe",
        recipe = "rocketpack"
      },
    },
    prerequisites = {"land-mine", "explosive-rocketry", "modular-tank-research"},
    unit =
    {
      count = 40*1,
      ingredients = {{"automation-science-pack", 3}, {"logistic-science-pack", 3}, {"military-science-pack", 3}},
      time = 105
    },
    ignore_tech_cost_multiplier = true,
    order = "a-b-c"
  },
  {
    type = "technology",
    name = "mechanized-infantry-research",
    icon = "__tanks_for_bob_fork__/graphics/icons/mech-inf.png",
    icon_size = 64,
    effects =
    {
      {
        type = "unlock-recipe",
        recipe = "fish-kit"
      },
      {
        type = "unlock-recipe",
        recipe = "piercing-shotgun-shell-brick"
      },
      {
        type = "unlock-recipe",
        recipe = "ap-bullet-brick"
      },
    },
    prerequisites = {"modular-tank-research"},
    unit =
    {
      count = 30*1,
      ingredients = {{"automation-science-pack", 3}, {"logistic-science-pack", 1}, {"military-science-pack", 1}},
      time = 15
    },
    ignore_tech_cost_multiplier = true,
    order = "a-b-c"
  },
  {
    type = "technology",
    name = "new-munitions",
    icon = "__tanks_for_bob_fork__/graphics/icons/chemical-tank-research.png",
    icon_size = 64,
    effects =
    {
      {
        type = "unlock-recipe",
        recipe = "50mm-mortar-poison"
      },
      {
        type = "unlock-recipe",
        recipe = "minepack-poison"
      },
    },
    prerequisites = { "modular-tank-research2", "military-3" },
    unit =
    {
      count = 40*1,
      ingredients = {{"automation-science-pack", 3}, {"logistic-science-pack", 2}, {"military-science-pack", 3}},
      time = 10
    },
    ignore_tech_cost_multiplier = true,
    order = "a-b-c"
  },
  {
    type = "technology",
    name = "organic-explosives2",
    icon = "__tanks_for_bob_fork__/graphics/icons/universal-explosive.png",
    icon_size = 64,
    effects =
    {
      {
        type = "ammo-damage",
        ammo_category = "tank-nade-ammo",
        modifier = 0.2
      },
      {
        type = "gun-speed",
        ammo_category = "tank-nade-ammo",
        modifier = 0.2
      },
      {
        type = "ammo-damage",
        ammo_category = "tank-rocket-ammo",
        modifier = 0.2
      },
      {
        type = "gun-speed",
        ammo_category = "tank-rocket-ammo",
        modifier = 0.2
      },
    },
    prerequisites = { "modular-tank-research2", "organic-explosives" },
    unit =
    {
      count = 40*1,
      ingredients = {{"automation-science-pack", 1}, {"logistic-science-pack", 1}, {"military-science-pack", 1}},
      time = 150
    },
    ignore_tech_cost_multiplier = true,
    order = "a-b-c"
  },
  {
    type = "technology",
    name = "organic-explosives3",
    icon = "__tanks_for_bob_fork__/graphics/icons/universal-explosive.png",
    icon_size = 64,
    effects =
    {
      {
        type = "ammo-damage",
        ammo_category = "tank-wmd-ammo",
        modifier = 0.2
      },
      {
        type = "ammo-damage",
        ammo_category = "tank-nade-ammo",
        modifier = 0.2
      },
      {
        type = "ammo-damage",
        ammo_category = "tank-rocket-ammo",
        modifier = 0.2
      },
      {
        type = "unlock-recipe",
        recipe = "wmdartillery-ammo"
      },
    },
    prerequisites = { "modular-tank-research2","organic-explosives2" },
    unit =
    {
      count = 40*1,
      ingredients = {{"automation-science-pack", 1}, {"logistic-science-pack", 1}, {"military-science-pack", 1}},
      time = 150
    },
    ignore_tech_cost_multiplier = true,
    order = "a-b-c"
  },
  {
    type = "technology",
    name = "super-tank-research",
    icon = "__tanks_for_bob_fork__/graphics/icons/super-tank-research.png",
    icon_size = 64,
    effects =
    {
      {
        type = "unlock-recipe",
        recipe = "super-tank"
      },
      {
        type = "unlock-recipe",
        recipe = "super-tank-alternate"
      },
      {
        type = "unlock-recipe",
        recipe = "tank-ammo-Reprocessing"
      },
    },
    prerequisites = { "modular-tank-research2", "military-3" },
    unit =
    {
      count = 50,
      ingredients = {{"automation-science-pack", 5}, {"logistic-science-pack", 2}, {"military-science-pack", 6}},
      time = 10
    },
    order = "a-b-c"
  },
  {
    type = "technology",
    name = "super-tank-research2",
    icon = "__tanks_for_bob_fork__/graphics/icons/super-tank-research.png",
    icon_size = 64,
    effects =
    {
      {
        type = "unlock-recipe",
        recipe = "super-tank-wmd"
      },
      {
        type = "unlock-recipe",
        recipe = "tank-wmd-ammo"
      },
    },
    prerequisites = { "super-tank-research", "new-munitions" },
    unit =
    {
      count = 100,
      ingredients = {{"automation-science-pack", 12}, {"logistic-science-pack", 6}, {"military-science-pack", 6}},
      time = 15
    },
    ignore_tech_cost_multiplier = true,
    order = "a-b-c"
  },
}
)