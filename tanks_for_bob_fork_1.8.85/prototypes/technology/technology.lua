data:extend(
{ 
--new tech recipes that need adjustment
{
        type = "technology",
        name = "campfire",
        icon = "__tanks_for_bob_fork__/graphics/icons/campfire.png",
        icon_size = 64,
        effects = {        
        },
        prerequisites = {},
        unit = {
            count = 10,
            ingredients = {{"cooked-fish", 1}},
            time = 10
        },
        order = "a"
    },
    {
        type = "technology",
        name = "beachpump",
        icon = "__tanks_for_bob_fork__/graphics/icons/beachpump.png",
        icon_size = 64,
        effects = {
            {
                type = "unlock-recipe",
                recipe = "beachpump"
            }
        },
        prerequisites = {"campfire"},
        unit = {
            count = 10,
            ingredients = {{"cooked-fish", 1}},
            time = 10
        },
        order = "b"
    },
    {
        type = "technology",
        name = "wood-pipes",
        icon = "__tanks_for_bob_fork__/graphics/icons/wood-pipes.png",
        icon_size = 64,
        effects = {
            {
                type = "unlock-recipe",
                recipe = "wood-pipes"
            }
        },
        prerequisites = {"beachpump"},
        unit = {
            count = 10,
            ingredients = {{"cooked-fish", 1}},
            time = 10
        },
        order = "c"
    },
    {
        type = "technology",
        name = "wood-basin",
        icon = "__tanks_for_bob_fork__/graphics/icons/wood-basin.png",
        icon_size = 64,
        effects = {
            {
                type = "unlock-recipe",
                recipe = "wood-basin"
            }
        },
        prerequisites = {"wood-pipes"},
        unit = {
            count = 10,
            ingredients = {{"cooked-fish", 1}},
            time = 10
        },
        order = "d"
    },
    {
        type = "technology",
        name = "workbench",
        icon = "__tanks_for_bob_fork__/graphics/icons/workbench.png",
        icon_size = 64,
        effects = {
            {
                type = "unlock-recipe",
                recipe = "workbench"
            }
        },
        prerequisites = {"wood-basin"},
        unit = {
            count = 10,
            ingredients = {{"cooked-fish", 1}},
            time = 10
        },
        order = "e"
    },
    {
        type = "technology",
        name = "clay-pit",
        icon = "__tanks_for_bob_fork__/graphics/icons/clay-pit.png",
        icon_size = 64,
        effects = {
            {
                type = "unlock-recipe",
                recipe = "clay-pit"
            }
        },
        prerequisites = {"thinking-hut"},
        unit = {
            count = 10,
            ingredients = {{"cooked-fish", 1}},
            time = 10
        },
        order = "g"
    },
    {
        type = "technology",
        name = "pit-kiln",
        icon = "__tanks_for_bob_fork__/graphics/icons/pit-kiln.png",
        icon_size = 64,
        effects = {
            {
                type = "unlock-recipe",
                recipe = "pit-kiln"
            }
        },
        prerequisites = {"clay-pit"},
        unit = {
            count = 10,
            ingredients = {{"cooked-fish", 1}},
            time = 10
        },
        order = "h"
    },
    {
        type = "technology",
        name = "growing-plot",
        icon = "__tanks_for_bob_fork__/graphics/icons/growing-plot.png",
        icon_size = 64,
        effects = {
            {
                type = "unlock-recipe",
                recipe = "growing-plot"
            }
        },
        prerequisites = {"pit-kiln"},
        unit = {
            count = 10,
            ingredients = {{"cooked-fish", 1}},
            time = 10
        },
        order = "i"
    },
    {
        type = "technology",
        name = "clay",
        icon = "__tanks_for_bob_fork__/graphics/icons/clay.png",
        icon_size = 64,
        effects = {
            {
                type = "unlock-recipe",
                recipe = "clay"
            }
        },
        prerequisites = {"growing-plot"},
        unit = {
            count = 10,
            ingredients = {{"cooked-fish", 1}},
            time = 10
        },
        order = "k"
    },
    {
        type = "technology",
        name = "brick",
        icon = "__tanks_for_bob_fork__/graphics/icons/brick.png",
        icon_size = 64,
        effects = {
            {
                type = "unlock-recipe",
                recipe = "brick"
            }
        },
        prerequisites = {"clay"},
        unit = {
            count = 10,
            ingredients = {{"cooked-fish", 1}},
            time = 10
        },
        order = "l"
    },
    {
        type = "technology",
        name = "crude-glass",
        icon = "__tanks_for_bob_fork__/graphics/icons/crude-glass.png",
        icon_size = 64,
        effects = {
            {
                type = "unlock-recipe",
                recipe = "crude-glass"
            }
        },
        prerequisites = {"brick"},
        unit = {
            count = 10,
            ingredients = {{"cooked-fish", 1}},
            time = 10
        },
        order = "m"
    },
    {
        type = "technology",
        name = "wood-spear",
        icon = "__tanks_for_bob_fork__/graphics/icons/wood-spear.png",
        icon_size = 64,
        effects = {
            {
                type = "unlock-recipe",
                recipe = "wood-spear"
            }
        },
        prerequisites = {"crude-glass"},
        unit = {
            count = 10,
            ingredients = {{"cooked-fish", 1}},
            time = 10
        },
        order = "n"
    },
    {
        type = "technology",
        name = "cooking-fire",
        icon = "__tanks_for_bob_fork__/graphics/icons/cooking-fire.png",
        icon_size = 64,
        effects = {
            {
                type = "unlock-recipe",
                recipe = "cooking-fire"
            }
        },
        prerequisites = {"wood-spear"},
        unit = {
            count = 10,
            ingredients = {{"cooked-fish", 1}},
            time = 10
        },
        order = "o"
    },
    {
        type = "technology",
        name = "stone-water-wheel",
        icon = "__tanks_for_bob_fork__/graphics/icons/stone-water-wheel.png",
        icon_size = 64,
        effects = {
            {
                type = "unlock-recipe",
                recipe = "stone-water-wheel"
            }
        },
        prerequisites = {"cooking-fire"},
        unit = {
            count = 10,
            ingredients = {{"cooked-fish", 1}},
            time = 10
        },
        order = "p"
    },
    {
        type = "technology",
        name = "aqueduct",
        icon = "__tanks_for_bob_fork__/graphics/icons/aqueduct1.png",
        icon_size = 64,
        effects = {
            {
                type = "unlock-recipe",
                recipe = "aqueduct"
            }
        },
        prerequisites = {"stone-water-wheel"},
        unit = {
            count = 10,
            ingredients = {{"cooked-fish", 1}},
            time = 10
        },
        order = "q"
    },
    {
        type = "technology",
        name = "stone-basin",
        icon = "__tanks_for_bob_fork__/graphics/icons/stone-basin.png",
        icon_size = 64,
        effects = {
            {
                type = "unlock-recipe",
                recipe = "stone-basin"
            }
        },
        prerequisites = {"aqueduct"},
        unit = {
            count = 10,
            ingredients = {{"cooked-fish", 1}},
            time = 10
        },
        order = "r"
    },
    {
        type = "technology",
        name = "shack",
        icon = "__tanks_for_bob_fork__/graphics/icons/shack.png",
        icon_size = 64,
        effects = {
            {
                type = "unlock-recipe",
                recipe = "shack"
            }
        },
        prerequisites = {"stone-basin"},
        unit = {
            count = 10,
            ingredients = {{"cooked-fish", 1}},
            time = 10
        },
        order = "s"
    },
    {
        type = "technology",
        name = "pondering-hovel",
        icon = "__tanks_for_bob_fork__/graphics/icons/pondering-hovel.png",
        icon_size = 64,
        effects = {
            {
                type = "unlock-recipe",
                recipe = "pondering-hovel"
            }
        },
        prerequisites = {"shack"},
        unit = {
            count = 10,
            ingredients = {{"cooked-fish", 1}},
            time = 10
        },
        order = "t"
    },
    {
        type = "technology",
        name = "quarry",
        icon = "__tanks_for_bob_fork__/graphics/icons/quarry.png",
        icon_size = 64,
        effects = {
            {
                type = "unlock-recipe",
                recipe = "quarry"
            }
        },
        prerequisites = {"pondering-hovel"},
        unit = {
            count = 10,
            ingredients = {{"cooked-fish", 1}},
            time = 10
        },
        order = "u"
    },
    {
        type = "technology",
        name = "solar-boiler",
        icon = "__tanks_for_bob_fork__/graphics/icons/solar-boiler.png",
        icon_size = 64,
        effects = {
            {
                type = "unlock-recipe",
                recipe = "solar-boiler"
            }
        },
        prerequisites = {"quarry"},
        unit = {
            count = 10,
            ingredients = {{"cooked-fish", 1}},
            time = 10
        },
        order = "v"
    },
    {
        type = "technology",
        name = "fish-pond",
        icon = "__tanks_for_bob_fork__/graphics/icons/fish-pond.png",
        icon_size = 64,
        effects = {
            {
                type = "unlock-recipe",
                recipe = "fish-pond"
            }
        },
        prerequisites = {"solar-boiler"},
        unit = {
            count = 10,
            ingredients = {{"cooked-fish", 1}},
            time = 10
        },
        order = "w"
    },
    {
        type = "technology",
        name = "meal",
        icon = "__tanks_for_bob_fork__/graphics/icons/meal.png",
        icon_size = 64,
        effects = {
            {
                type = "unlock-recipe",
                recipe = "meal"
            }
        },
        prerequisites = {"fish-pond"},
        unit = {
            count = 10,
            ingredients = {{"cooked-fish", 1}},
            time = 10
        },
        order = "x"
    },
    {
        type = "technology",
        name = "stone-tools",
        icon = "__tanks_for_bob_fork__/graphics/icons/stone-tools.png",
        icon_size = 64,
        effects = {
            {
                type = "unlock-recipe",
                recipe = "stone-tools"
            }
        },
        prerequisites = {"meal"},
        unit = {
            count = 10,
            ingredients = {{"cooked-fish", 1}},
            time = 10
        },
        order = "y"
    },
    {
        type = "technology",
        name = "primitive-steam-powered-pump",
        icon = "__tanks_for_bob_fork__/graphics/icons/primitive-steam-powered-pump.png",
        icon_size = 64,
        effects = {
            {
                type = "unlock-recipe",
                recipe = "primitive-steam-powered-pump"
            }
        },
        prerequisites = {"stone-tools"},
        unit = {
            count = 10,
            ingredients = {{"cooked-fish", 1}},
            time = 10
        },
        order = "z"
    },
    {
        type = "technology",
        name = "steam-condenser",
        icon = "__tanks_for_bob_fork__/graphics/icons/steam-condenser.png",
        icon_size = 64,
        effects = {
            {
                type = "unlock-recipe",
                recipe = "steam-condenser"
            }
        },
        prerequisites = {"primitive-steam-powered-pump"},
        unit = {
            count = 10,
            ingredients = {{"cooked-fish", 1}},
            time = 10
        },
        order = "aa"
    },
    {
        type = "technology",
        name = "calcifier",
        icon = "__tanks_for_bob_fork__/graphics/icons/calcifier.png",
        icon_size = 64,
        effects = {
            {
                type = "unlock-recipe",
                recipe = "calcifier"
            }
        },
        prerequisites = {"steam-condenser"},
        unit = {
            count = 10,
            ingredients = {{"cooked-fish", 1}},
            time = 10
        },
        order = "ab"
    },
    {
        type = "technology",
        name = "shaler",
        icon = "__tanks_for_bob_fork__/graphics/icons/shaler.png",
        icon_size = 64,
        effects = {
            {
                type = "unlock-recipe",
                recipe = "shaler"
            }
        },
        prerequisites = {"calcifier"},
        unit = {
            count = 10,
            ingredients = {{"cooked-fish", 1}},
            time = 10
        },
        order = "ac"
    },


  --encabulation
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