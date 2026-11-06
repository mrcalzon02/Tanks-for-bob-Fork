data:extend({


-- =========================================================
-- TIER 00 - Natural gathering / zero-input primitives
-- =========================================================

{
        type = "recipe",
        name = "stone",
        enabled = true,
        category = "quarrying",
        energy_required = 55,
        ingredients = {},
        results = {{type = "item", name = "stone", amount = 8}}}
,

{
        type = "recipe",
        name = "Trees",
        enabled = true,
        category = "growing",
        energy_required = 20,
        ingredients = {},
        results = {{type = "item", name = "wood", amount = 15}}}
,

{
        type = "recipe",
        name = "harvest-fish",
        enabled = true,
        category = "fishery",
        subgroup = "Seablock",
        energy_required = 55,
        ingredients = {},
        results = {{type = "item", name = "raw-fish", amount = 2}}}
,

-- =========================================================
-- TIER 00-A - Absolute desperation hand bootstraps
-- These recipes are intentionally terrible. They exist so a
-- literal one-tile SeaBlock start can still recover by hand.
-- =========================================================

{
    type = "recipe",
    name = "desperation-gather-fish",
    enabled = true,
    category = "crafting",
    subgroup = "Seablock",
    icon = "__base__/graphics/icons/fish.png",
    icon_size = 64,
    energy_required = 180,
    ingredients = {},
    results = {{type = "item", name = "raw-fish", amount = 1}}
}
,

{
    type = "recipe",
    name = "desperation-scrape-driftwood",
    enabled = true,
    category = "crafting",
    subgroup = "Seablock",
    icon = "__base__/graphics/icons/wood.png",
    icon_size = 64,
    energy_required = 90,
    ingredients = {},
    results = {{type = "item", name = "wood", amount = 1}}
}
,

{
    type = "recipe",
    name = "desperation-pick-stone",
    enabled = true,
    category = "crafting",
    subgroup = "Seablock",
    icon = "__base__/graphics/icons/stone.png",
    icon_size = 64,
    energy_required = 60,
    ingredients = {},
    results = {{type = "item", name = "stone", amount = 1}}
}
,

{
    type = "recipe",
    name = "desperation-landfill",
    enabled = true,
    category = "crafting",
    subgroup = "Seablock",
    icon = "__base__/graphics/icons/landfill.png",
    icon_size = 64,
    energy_required = 30,
    ingredients = {{type = "item", name = "stone", amount = 20}},
    results = {{type = "item", name = "landfill", amount = 1}}
}
,


-- =========================================================
-- TIER 01 - First manual survival outputs
-- =========================================================

{
    type = "recipe",
    name = "catch-fish",
    enabled = true,
    category = "fishery",
    subgroup = "Seablock",
    energy_required = 5,
    ingredients = {
        {type = "item", name = "wood", amount = 1}
    },
    results = {{type = "item", name = "raw-fish", amount = 8}}}
,

{
    type = "recipe",
    name = "Sharp-stick",
    enabled = true,
    category = "crafting",
    subgroup = "Seablock",
    energy_required = 10,
    ingredients = {{type = "item", name = "wood", amount = 5}},
    results = {{type = "item", name = "Sharp-stick", amount = 10}}}
,


-- =========================================================
-- TIER 02 - First tools and tool-assisted gathering
-- =========================================================

{
        type = "recipe",
        name = "stone-tools",
        enabled = true,
        category = "crafting",
        energy_required = 6,
        ingredients = {{type = "item", name = "stone", amount = 3},{type = "item", name = "wood", amount = 1}},
        results = {{type = "item", name = "stone-tools", amount = 1}}}
,

{
        type = "recipe",
        name = "Trees-with-tools",
        enabled = true,
        category = "growing",
        subgroup = "Seablock",
        icon = "__base__/graphics/icons/wood.png",
        icon_size = 64,
        energy_required = 15,
        ingredients = {{type = "item", name = "stone-tools", amount = 1}},
        results = {
            {type = "item", name = "wood", amount = 35},
            {type = "item", name = "stone-tools", amount = 1}
        }
    }
,

{
        type = "recipe",
        name = "stone-with-tools",
        enabled = true,
        category = "quarrying",
        subgroup = "Seablock",
        icon = "__base__/graphics/icons/stone.png",
        icon_size = 64,
        energy_required = 35,
        ingredients = {{type = "item", name = "stone-tools", amount = 1}},
        results = {
            {type = "item", name = "stone", amount = 20},
            {type = "item", name = "stone-tools", amount = 1}
        }
    }
,

{
    type = "recipe",
    name = "catch-fish-with-tools",
    enabled = true,
    category = "fishery",
    subgroup = "Seablock",
    icon = "__base__/graphics/icons/fish.png",
    icon_size = 64,
    energy_required = 5,
    ingredients = {
        {type = "item", name = "wood", amount = 1},
        {type = "item", name = "stone-tools", amount = 1}
    },
    results = {
        {type = "item", name = "raw-fish", amount = 20},
        {type = "item", name = "stone-tools", amount = 1}
    }
}
,


-- =========================================================
-- TIER 03 - Basic food, clay, and low processing
-- =========================================================

{
        type = "recipe",
        name = "Seared-fish",
        enabled = true,
        category = "cooking",
        subgroup = "Seablock",
        energy_required = 5,
        ingredients = {{type = "item", name = "raw-fish", amount = 1}},
        results = {{type = "item", name = "Seared-fish", amount = 2}}}
,

{
        type = "recipe",
        name = "clay",
        enabled = true,
        category = "clay",
        energy_required = 4.5,
        ingredients = {{type = "item", name = "stone", amount = 2},{type = "fluid", name = "water", amount = 500}},
        results = {{type = "item", name = "clay", amount = 4}}}
,

{
        type = "recipe",
        name = "clay-with-tools",
        enabled = true,
        category = "clay",
        subgroup = "Seablock",
        icon = "__tanks_for_bob_fork__/graphics/icons/clay.png",
        icon_size = 64,
        energy_required = 4,
        ingredients = {
            {type = "item", name = "stone", amount = 2},
            {type = "item", name = "stone-tools", amount = 1},
            {type = "fluid", name = "water", amount = 500}
        },
        results = {
            {type = "item", name = "clay", amount = 8},
            {type = "item", name = "stone-tools", amount = 1}
        }
    }
,

{
    type = "recipe",
    name = "fish-kit",
    enabled = false,
    category = "tank-ammo-component",
    energy_required = 5,
    ingredients =
    {
      {type = "item", name = "raw-fish", amount = 5},
    },
    results =
    {
      {type = "item", name = "fish-kit", amount = 6},
    }
  }
,


-- =========================================================
-- TIER 04 - Basic wooden structures and first stations
-- =========================================================

{
        type = "recipe",
        name = "campfire",
        enabled = true,
        category = "crafting",
        subgroup = "Seablock",
        energy_required = 35,
        ingredients = {{type = "item", name = "wood", amount = 5}},
        results = {{type = "item", name = "campfire", amount = 1}}}
,

{
        type = "recipe",
        name = "workbench",
        enabled = true,
        category = "crafting",
       subgroup = "Seablock",
        energy_required = 35,
        ingredients = {{type = "item", name = "wood", amount = 4}},
        results = {{type = "item", name = "workbench", amount = 1}}}
,

{
        type = "recipe",
        name = "thinking-hut",
        enabled = true,
        category = "crafting",
        subgroup = "Seablock",
        energy_required = 35,
        ingredients = {{type = "item", name = "wood", amount = 10}},
        results = {{type = "item", name = "thinking-hut", amount = 1}}}
,

{
        type = "recipe",
        name = "beachpump",
        enabled = false,
        category = "Seablock",
        energy_required = 25,
        ingredients = {
            {type = "item", name = "wood", amount = 6},
            {type = "item", name = "stone", amount = 4}
        },
        results = {{type = "item", name = "beachpump", amount = 1}}}
,

{
        type = "recipe",
        name = "growing-plot",
        enabled = false,
        category = "Seablock",
        energy_required = 5,
        ingredients = {
            {type = "item", name = "wood", amount = 3},
            {type = "item", name = "stone", amount = 4}
        },
        results = {{type = "item", name = "growing-plot", amount = 1}}}
,

{
        type = "recipe",
        name = "wood-spear",
        enabled = false,
        category = "Seablock",
        energy_required = 10,
        ingredients = {{type = "item", name = "wood", amount = 2}},
        results = {{type = "item", name = "wood-spear", amount = 1}}}
,


-- =========================================================
-- TIER 05 - Clay/brick foundation and primitive industry
-- =========================================================

{
        type = "recipe",
        name = "clay-pit",
        enabled = false,
        category = "Seablock",
        energy_required = 25,
        ingredients = {
            {type = "item", name = "wood", amount = 3},
            {type = "item", name = "stone", amount = 6},
            {type = "item", name = "stone-tools", amount = 1}
        },
        results = {{type = "item", name = "clay-pit", amount = 1}}}
,

{
        type = "recipe",
        name = "brick",
        enabled = false,
        category = "pit-kiln",
		icon = "__tanks_for_bob_fork__/graphics/icons/brick.png",
    icon_size = 64,
        energy_required = 30,
        ingredients = {{type = "item", name = "clay", amount = 6}},
        results =
        {
            {type = "item", name = "brick", amount = 2},
            {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.06},
        }
    }
,

{
        type = "recipe",
        name = "pit-kiln",
        enabled = false,
        category = "Seablock",
        energy_required = 35,
        ingredients = {{type = "item", name = "clay-pit", amount = 1},{type = "item", name = "campfire", amount = 1}},
        results = {{type = "item", name = "pit-kiln", amount = 1}}}
,

{
        type = "recipe",
        name = "crude-glass",
        enabled = false,
        category = "pit-kiln",
        energy_required = 50,
        ingredients = {{type = "item", name = "wood", amount = 5}},
        results =
        {
            {type = "item", name = "crude-glass", amount = 5},
            {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.08},
        }
    }
,


-- =========================================================
-- TIER 06 - Tool-dependent early structures
-- =========================================================

{
        type = "recipe",
        name = "wood-basin",
        enabled = false,
        category = "Seablock",
        energy_required = 25,
        ingredients = {
            {type = "item", name = "wood", amount = 18},
            {type = "item", name = "stone", amount = 8},
            {type = "item", name = "stone-tools", amount = 1}
        },
        results =
        {
            {type = "item", name = "wood-basin", amount = 1},
            {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.05},
        }
    }
,

{
        type = "recipe",
        name = "fish-pond",
        enabled = false,
        category = "Seablock",
        energy_required = 35,
        ingredients = {
            {type = "item", name = "brick", amount = 5},
            {type = "item", name = "wood", amount = 8},
            {type = "item", name = "stone-tools", amount = 1}
        },
        results =
        {
            {type = "item", name = "fish-pond", amount = 1},
            {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.04},
        }
    }
,

{
        type = "recipe",
        name = "quarry",
        enabled = false,
        category = "Seablock",
        energy_required = 35,
        ingredients = {
            {type = "item", name = "brick", amount = 12},
            {type = "item", name = "wood", amount = 5},
            {type = "item", name = "stone-tools", amount = 2}
        },
        results =
        {
            {type = "item", name = "quarry", amount = 1},
            {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.10},
        }
    }
,

{
        type = "recipe",
        name = "primitive-steam-powered-pump",
        enabled = false,
        category = "Seablock",
        energy_required = 35,
        ingredients = {
            {type = "item", name = "brick", amount = 5},
            {type = "item", name = "wood", amount = 4},
            {type = "item", name = "stone-tools", amount = 1}
        },
        results =
        {
            {type = "item", name = "primitive-steam-powered-pump", amount = 1},
            {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.06},
        }
    }
,


-- =========================================================
-- TIER 07 - Heat, steam, and basic mechanical infrastructure
-- =========================================================

{
        type = "recipe",
        name = "cooking-fire",
        enabled = false,
        category = "Seablock",
        energy_required = 10,
        ingredients = {{type = "item", name = "brick", amount = 5}, {type = "item", name = "campfire", amount = 1}},
        results =
        {
            {type = "item", name = "cooking-fire", amount = 1},
            {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.04},
        }
    }
,

{
        type = "recipe",
        name = "stone-water-wheel",
        enabled = false,
        category = "Seablock",
        energy_required = 35,
        ingredients = {{type = "item", name = "brick", amount = 10}, {type = "item", name = "wood", amount = 5}},
        results =
        {
            {type = "item", name = "stone-water-wheel", amount = 1},
            {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.05},
        }
    }
,

{
        type = "recipe",
        name = "solar-boiler",
        enabled = false,
        category = "Seablock",
        energy_required = 35,
        ingredients = {{type = "item", name = "brick", amount = 15}, {type = "item", name = "wood", amount = 15}},
        results =
        {
            {type = "item", name = "solar-boiler", amount = 1},
            {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.07},
        }
    }
,

{
        type = "recipe",
        name = "steam-condenser",
        enabled = false,
        category = "Seablock",
        energy_required = 35,
        ingredients = {{type = "item", name = "crude-glass", amount = 10}, {type = "item", name = "brick", amount = 5}},
        results =
        {
            {type = "item", name = "steam-condenser", amount = 1},
            {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.06},
        }
    }
,

{
    type = "recipe",
    name = "Steam-condenserA",
    enabled = true,
    category = "Steam",
    subgroup = "Seablock",
    icon = "__base__/graphics/icons/stone.png",
    icon_size = 64,
    energy_required = 35,
    ingredients =
    {
      {type = "item", name = "wood", amount = 5},
      {type = "fluid", name = "steam", amount = 200},
    },
    results =
    {
      {type = "item", name = "stone", amount = 10},
      {type = "item", name = "tank-ammo-Industrialwaste", amount = 1},
    },
    }
,

{
        type = "recipe",
        name = "pondering-hovel",
        enabled = false,
        category = "Seablock",
        energy_required = 35,
        ingredients = {{type = "item", name = "thinking-hut", amount = 1}, {type = "item", name = "brick", amount = 10}},
        results = {{type = "item", name = "pondering-hovel", amount = 1}}}
,


-- =========================================================
-- TIER 08 - Quarry ore routes and metal-entry support
-- =========================================================


-- Miserable hand fallback: one tool + one rock -> one ore
{
    type = "recipe",
    name = "hand-chip-iron-ore",
    enabled = true,
    category = "crafting",
    subgroup = "Seablock",
    icon = "__base__/graphics/icons/iron-ore.png",
    icon_size = 64,
    energy_required = 120,
    ingredients =
    {
      {type = "item", name = "stone-tools", amount = 1},
      {type = "item", name = "stone", amount = 1},
    },
    results =
    {
      {type = "item", name = "iron-ore", amount = 1},
    },
}
,

-- Miserable hand fallback: one tool -> one wood
{
    type = "recipe",
    name = "hand-scrape-wood",
    enabled = true,
    category = "crafting",
    subgroup = "Seablock",
    icon = "__base__/graphics/icons/wood.png",
    icon_size = 64,
    energy_required = 120,
    ingredients =
    {
      {type = "item", name = "stone-tools", amount = 1},
    },
    results =
    {
      {type = "item", name = "wood", amount = 1},
    },
}
,

-- Miserable hand fallback: one fish + one tool -> five rocks
{
    type = "recipe",
    name = "hand-break-fish-for-stone",
    enabled = true,
    category = "crafting",
    subgroup = "Seablock",
    icon = "__base__/graphics/icons/stone.png",
    icon_size = 64,
    energy_required = 120,
    ingredients =
    {
      {type = "item", name = "raw-fish", amount = 1},
      {type = "item", name = "stone-tools", amount = 1},
    },
    results =
    {
      {type = "item", name = "stone", amount = 5},
    },
}
,

{
        type = "recipe",
        name = "quarry-iron-ore",
        enabled = true,
        category = "quarrying",
        energy_required = 9,
        ingredients = {{type = "item", name = "stone-tools", amount = 1}, {type = "item", name = "brick", amount = 5}},
        results =
        {
            {type = "item", name = "iron-ore", amount = 10},
            {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.08},
        }
    }
,

{
        type = "recipe",
        name = "quarry-copper-ore",
        enabled = true,
        category = "quarrying",
        energy_required = 9,
        ingredients = {{type = "item", name = "stone-tools", amount = 1}, {type = "item", name = "brick", amount = 5}},
        results =
        {
            {type = "item", name = "copper-ore", amount = 10},
            {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.08},
        }
    }
,

{
        type = "recipe",
        name = "quarry-iron-orea",
        enabled = true,
        category = "quarrying",
        energy_required = 9,
        ingredients = {{type = "item", name = "stone-tools", amount = 2}, {type = "item", name = "stone-brick", amount = 15}},
        results =
        {
            {type = "item", name = "iron-ore", amount = 20},
            {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.11},
        }
    }
,

{
        type = "recipe",
        name = "quarry-copper-oreb",
        enabled = true,
        category = "quarrying",
        energy_required = 9,
        ingredients = {{type = "item", name = "stone-tools", amount = 2}, {type = "item", name = "stone-brick", amount = 15}},
        results =
        {
            {type = "item", name = "copper-ore", amount = 20},
            {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.11},
        }
    }
,

{
        type = "recipe",
        name = "workbenchA",
        enabled = true,
        category = "crafting",
        subgroup = "Seablock",
        energy_required = 35,
        ingredients = {{type = "item", name = "iron-plate", amount = 2}},
        results = {{type = "item", name = "workbench", amount = 1}}}
,

{
        type = "recipe",
        name = "stone-tools-iron",
        enabled = false,
        category = "crafting",
        energy_required = 5,
        ingredients = {{type = "item", name = "stone-brick", amount = 1},{type = "item", name = "iron-stick", amount = 1}},
        results = {{type = "item", name = "stone-tools", amount = 5}}}
,

{
        type = "recipe",
        name = "Canister",
        enabled = true,
        category = "crafting",
        subgroup = "Seablock",
        energy_required = 35,
        ingredients = {{type = "item", name = "stone-tools", amount = 1},{type = "item", name = "iron-ore", amount = 1}},
        results =
        {
            {type = "item", name = "Canister", amount = 2},
            {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.07},
        }
    }
,


-- =========================================================
-- TIER 09 - Calcifier, shaler, and steam-compression infrastructure
-- =========================================================

{
        type = "recipe",
        name = "calcifier",
        enabled = false,
        category = "Seablock",
        energy_required = 35,
        ingredients = {{type = "item", name = "brick", amount = 10}, {type = "item", name = "stone-tools", amount = 5}},
        results =
        {
            {type = "item", name = "calcifier", amount = 1},
            {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.07},
        }
    }
,

{
        type = "recipe",
        name = "Calcifier-pro",
        enabled = true,
        category = "Calcifier",
        icon = "__base__/graphics/icons/stone.png",
        icon_size = 64,
        energy_required = 35,
        ingredients = {{type = "item", name = "stone", amount = 2}, {type = "fluid", name = "water", amount = 250}},
        results =
        {
            {type = "item", name = "stone", amount = 8},
            {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.04},
        }
    }
,

{
        type = "recipe",
        name = "shaler",
        enabled = false,
        category = "Seablock",
        energy_required = 35,
        ingredients = {{type = "item", name = "crude-glass", amount = 5}, {type = "item", name = "brick", amount = 20}},
        results =
        {
            {type = "item", name = "shaler", amount = 1},
            {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.09},
        }
    }
,

{
        type = "recipe",
        name = "Steam-Compressor",
        enabled = false,
        category = "Seablock",
        energy_required = 35,
        ingredients = {{type = "item", name = "shaler", amount = 1}, {type = "item", name = "cooking-fire", amount = 2}},
        results =
        {
            {type = "item", name = "Steam-Compressor", amount = 1},
            {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.10},
        }
    }
,

{
    type = "recipe",
    name = "Steam-Charge",
    enabled = true,
    category = "shaler",
    subgroup = "Seablock",
    icon = "__base__/graphics/icons/iron-ore.png",
    icon_size = 64,
    energy_required = 20,
    ingredients =
    {
      {type = "item", name = "tank-ammo-Industrialwaste", amount = 1},
      {type = "fluid", name = "steam", amount = 250},
    },
    results =
    {
      {type = "item", name = "iron-ore", amount = 1},
    },
    }
,

{
        type = "recipe",
        name = "Charged-Canister",
        enabled = false,
        category = "Steam-Compressor",
        subgroup = "Seablock",
        energy_required = 15,
        ingredients = {{type = "item", name = "Canister", amount = 1},{type = "fluid", name = "steam", amount = 350}},
        results =
        {
            {type = "item", name = "Charged-Canister", amount = 1},
            {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.05},
        }
    }
,

{
    type = "recipe",
    name = "UnCharge-Canister",
    enabled = false,
    category = "Steam-Compressor",
     subgroup = "Seablock",
    energy_required = 15,
    icon = "__tanks_for_bob_fork__/graphics/icons/Canister.png",
    icon_size = 64,
    ingredients = {{type = "item", name = "Charged-Canister", amount = 1}},
    results =
    {
        {type = "item", name = "Canister", amount = 1},
        {type = "fluid", name = "steam", amount = 350},
        {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.05},
    },
    }
,


-- =========================================================
-- TIER 10 - Calcifier throughput expansion
-- =========================================================

{
    type = "recipe",
    name = "Calcifier-pro-2",
    enabled = false,
    category = "Calcifier",
    icon = "__base__/graphics/icons/stone.png",
    icon_size = 64,
    energy_required = 25,
    ingredients = {
        {type="item", name="stone", amount=10},
        {type="fluid", name="water", amount=500}
    },
    results =
    {
        {type="item", name="stone", amount=40},
        {type="item", name="tank-ammo-Industrialwaste", amount=2},
        {type = "item", name = "tank-ammo-Radioactivewaste", amount = 1, probability = 0.01},
    }
}
,

{
    type = "recipe",
    name = "Calcifier-pro-3",
    enabled = false,
    category = "Calcifier",
    icon = "__base__/graphics/icons/stone.png",
    icon_size = 64,
    energy_required = 20,
    ingredients = {
        {type="item", name="stone", amount=25},
        {type="fluid", name="water", amount=1000}
    },
    results =
    {
        {type="item", name="stone", amount=120},
        {type="item", name="tank-ammo-Industrialwaste", amount=8},
        {type = "item", name = "tank-ammo-Radioactivewaste", amount = 1, probability = 0.02},
    }
}
,

{
    type = "recipe",
    name = "Calcifier-pro-4",
    enabled = false,
    category = "Calcifier",
    icon = "__base__/graphics/icons/stone.png",
    icon_size = 64,
    energy_required = 18,
    ingredients = {
        {type="item", name="stone", amount=50},
        {type="fluid", name="steam", amount=1500}
    },
    results =
    {
        {type="item", name="stone", amount=300},
        {type="item", name="tank-ammo-Industrialwaste", amount=20},
        {type = "item", name = "tank-ammo-Radioactivewaste", amount = 1, probability = 0.03},
    }
}
,

{
    type = "recipe",
    name = "Calcifier-pro-5",
    enabled = false,
    category = "Calcifier",
    icon = "__base__/graphics/icons/stone.png",
    icon_size = 64,
    energy_required = 15,
    ingredients = {
        {type="item", name="stone", amount=100},
        {type="fluid", name="steam", amount=3000}
    },
    results =
    {
        {type="item", name="stone", amount=800},
        {type="item", name="tank-ammo-Industrialwaste", amount=60},
        {type = "item", name = "tank-ammo-Radioactivewaste", amount = 1, probability = 0.04},
    }
}
,


-- =========================================================
-- TIER 11 - Shaler entry and canister loops
-- =========================================================

{
    type = "recipe",
    name = "shaler1",
    enabled = true,
    category = "shaler",
    subgroup = "Seablock",
    icon = "__base__/graphics/icons/iron-ore.png",
    icon_size = 64,
    energy_required = 35,
    ingredients =
    {
      {type = "item", name = "tank-ammo-Industrialwaste", amount = 1},
      {type = "fluid", name = "steam", amount = 500},
    },
    results =
    {
      {type = "item", name = "iron-ore", amount = 2},
    },
    }
,

{
    type = "recipe",
    name = "shalera",
    enabled = true,
    category = "shaler",
    subgroup = "Seablock",
    icon = "__tanks_for_bob_fork__/graphics/icons/Canister-waste.png",
    icon_size = 64,
    energy_required = 85,
    ingredients =
    {
      {type = "item", name = "tank-ammo-Industrialwaste", amount = 100},
      {type = "item", name = "Canister", amount = 1},
    },
    results =
    {
      {type = "item", name = "Canister-waste", amount = 1},
    },
    }
,

{
    type = "recipe",
    name = "shalerb",
    enabled = true,
    category = "shaler",
    subgroup = "Seablock",
    icon = "__tanks_for_bob_fork__/graphics/icons/Canister.png",
    icon_size = 64,
    energy_required = 85,
    ingredients =
    {
      {type = "item", name = "Canister-waste", amount = 1}
    },
    results =
    {
      {type = "item", name = "Canister", amount = 1},
      {type = "item", name = "tank-ammo-Industrialwaste", amount = 100}
    },
        }
,

{
    type = "recipe",
    name = "shalerc",
    enabled = true,
    category = "shaler",
    subgroup = "Seablock",
    icon = "__tanks_for_bob_fork__/graphics/icons/Canister-Radioactivewaste.png",
    icon_size = 64,
    energy_required = 85,
    ingredients =
    {
      {type = "item", name = "tank-ammo-Radioactivewaste", amount = 100},
      {type = "item", name = "Canister", amount = 1},
    },
    results =
    {
      {type = "item", name = "Canister-Radioactivewaste", amount = 1},
    },
    }
,

{
    type = "recipe",
    name = "shaler3",
    enabled = true,
    category = "shaler",
    subgroup = "Seablock",
    icon = "__tanks_for_bob_fork__/graphics/icons/Canister.png",
    icon_size = 64,
    energy_required = 85,
    ingredients =
    {
      {type = "item", name = "Canister-Radioactivewaste", amount = 1}
    },
    results =
    {
      {type = "item", name = "Canister", amount = 1},
      {type = "item", name = "tank-ammo-Radioactivewaste", amount = 100}
    },
    }
,


-- =========================================================
-- TIER 12 - Shaler ore production scaling
-- =========================================================

{
    type = "recipe",
    name = "shaler2",
    enabled = false,
    category = "shaler",
    icon = "__base__/graphics/icons/iron-ore.png",
    icon_size = 64,
    energy_required = 20,
    ingredients = {
        {type="item", name="tank-ammo-Industrialwaste", amount=10},
        {type="fluid", name="steam", amount=1000}
    },
    results =
    {
        {type="item", name="iron-ore", amount=25},
        {type="item", name="copper-ore", amount=25},
        {type = "item", name = "tank-ammo-Radioactivewaste", amount = 1, probability = 0.02},
    }
}
,

{
    type = "recipe",
    name = "shaler4",
    enabled = false,
    category = "shaler",
    icon = "__base__/graphics/icons/iron-ore.png",
    icon_size = 64,
    energy_required = 18,
    ingredients = {
        {type="item", name="tank-ammo-Industrialwaste", amount=25},
        {type="fluid", name="steam", amount=2500}
    },
    results = {
        {type="item", name="iron-ore", amount=80},
        {type="item", name="copper-ore", amount=80},
        {type="item", name="tank-ammo-Radioactivewaste", amount=2}
    }
}
,

{
    type = "recipe",
    name = "shaler5",
    enabled = false,
    category = "shaler",
    icon = "__base__/graphics/icons/iron-ore.png",
    icon_size = 64,
    energy_required = 15,
    ingredients = {
        {type="item", name="tank-ammo-Industrialwaste", amount=50},
        {type="fluid", name="steam", amount=5000}
    },
    results = {
        {type="item", name="iron-ore", amount=200},
        {type="item", name="copper-ore", amount=200},
        {type="item", name="tank-ammo-Radioactivewaste", amount=8}
    }
}
,

{
    type = "recipe",
    name = "shaler6",
    enabled = false,
    category = "shaler",
    icon = "__base__/graphics/icons/iron-ore.png",
    icon_size = 64,
    energy_required = 12,
    ingredients = {
        {type="item", name="tank-ammo-Industrialwaste", amount=100},
        {type="fluid", name="steam", amount=10000}
    },
    results = {
        {type="item", name="iron-ore", amount=500},
        {type="item", name="copper-ore", amount=500},
        {type="item", name="tank-ammo-Radioactivewaste", amount=20}
    }
}
,


-- =========================================================
-- TIER 13 - Radioactive refining and waste conversion
-- =========================================================

{
    type = "recipe",
    name = "radio-refine-2",
    enabled = false,
    category = "shaler",
    icon = "__base__/graphics/icons/uranium-ore.png",
    icon_size = 64,
    energy_required = 25,
    ingredients = {
        {type="item", name="tank-ammo-Radioactivewaste", amount=10},
        {type="fluid", name="steam", amount=2000}
    },
    results =
    {
        {type="item", name="uranium-ore", amount=15},
        {type="fluid", name="sulfuric-acid", amount=25},
        {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.08},
    }
}
,

{
    type = "recipe",
    name = "radio-refine-3",
    enabled = false,
    category = "shaler",
    icon = "__base__/graphics/icons/uranium-ore.png",
    icon_size = 64,
    energy_required = 20,
    ingredients = {
        {type="item", name="tank-ammo-Radioactivewaste", amount=25},
        {type="fluid", name="steam", amount=5000}
    },
    results =
    {
        {type="item", name="uranium-ore", amount=45},
        {type="fluid", name="sulfuric-acid", amount=75},
        {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.10},
    }
}
,

{
    type = "recipe",
    name = "radio-refine-4",
    enabled = false,
    category = "shaler",
    icon = "__base__/graphics/icons/uranium-ore.png",
    icon_size = 64,
    energy_required = 16,
    ingredients = {
        {type="item", name="tank-ammo-Radioactivewaste", amount=50},
        {type="fluid", name="steam", amount=10000}
    },
    results =
    {
        {type="item", name="uranium-ore", amount=110},
        {type="fluid", name="sulfuric-acid", amount=180},
        {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.12},
    }
}
,

{
    type = "recipe",
    name = "radio-refine-5",
    enabled = false,
    category = "shaler",
    icon = "__base__/graphics/icons/uranium-ore.png",
    icon_size = 64,
    energy_required = 12,
    ingredients = {
        {type="item", name="tank-ammo-Radioactivewaste", amount=100},
        {type="fluid", name="steam", amount=20000}
    },
    results =
    {
        {type="item", name="uranium-ore", amount=260},
        {type="fluid", name="sulfuric-acid", amount=450},
        {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.14},
    }
}
,

{
    type = "recipe",
    name = "ore-from-waste",
    enabled = false,
    category = "tank-ammo-component",
    subgroup = "Seablock",
    icon = "__base__/graphics/icons/iron-ore.png",
    icon_size = 64,
    energy_required = 50,
    ingredients =
    {
      {type = "item", name = "SpervingArm", amount = 1},
      {type = "item", name = "tank-ammo-reinforced-casing", amount = 1},
      {type = "item", name = "tank-ammo-Industrialwaste", amount = 10}
    },
    results =
    {
      {type = "item", name = "iron-ore", amount = 40},
      {type = "item", name = "copper-ore", amount = 40}
    }
  }
,

{
    type = "recipe",
    name = "ore-from-wasteb",
    enabled = false,
    category = "tank-ammo-component",
    subgroup = "Seablock",
    icon = "__base__/graphics/icons/iron-ore.png",
    icon_size = 64,
    energy_required = 60,
    ingredients =
    {
      {type = "item", name = "tank-ammo-reinforced-casing", amount = 1},
      {type = "item", name = "tank-ammo-Industrialwaste", amount = 1}
    },
    results =
    {
      {type = "item", name = "iron-ore", amount = 1},
      {type = "item", name = "copper-ore", amount = 1}
    }
  }
,

{
    type = "recipe",
    name = "ore-from-waster",
    enabled = false,
    category = "tank-ammo-component",
    subgroup = "Seablock",
    icon = "__base__/graphics/icons/uranium-ore.png",
    icon_size = 64,
    energy_required = 60,
    ingredients =
    {
      {type = "item", name = "tank-ammo-reinforced-casing", amount = 20},
      {type = "item", name = "tank-ammo-Industrialwaste", amount = 40},
      {type = "item", name = "DuctedSpervingArm", amount = 10}
    },
    results =
    {
      {type = "item", name = "uranium-ore", amount = 10},
      {type = "item", name = "copper-ore", amount = 10}
    }
  }
,

{
    type = "recipe",
    name = "tank-ammo-Reprocessing",
    enabled = false,
    category = "tank-ammo-component",
    subgroup = "Seablock",
    icon = "__base__/graphics/icons/uranium-ore.png",
    icon_size = 64,
    energy_required = 50,
    emissions_multiplier = 3,
    ingredients =
    {
      {type = "item", name = "tank-ammo-Industrialwaste", amount = 10},
      {type = "item", name = "tank-ammo-Radioactivewaste", amount = 10}
    },
    results =
    {
      {type = "item", name = "uranium-ore", amount = 10},
      {type = "item", name = "tank-ammo-Industrialwaste", amount = 1},
      {type = "item", name = "tank-ammo-Radioactivewaste", amount = 1},
    },
  }
,

{
    type = "recipe",
    name = "tank-ammo-ecozone",
    enabled = false,
    category = "tank-ammo-component",
    subgroup = "Seablock",
    icon = "__base__/graphics/icons/stone.png",
    icon_size = 64,
    energy_required = 40,
    ingredients =
    {
      {type = "item", name = "tank-ammo-Industrialwaste", amount = 50},
      {type = "item", name = "stone", amount = 50}
    },
    results =
    {
      {type = "item", name = "stone", amount = 10},
      {type = "item", name = "iron-ore", amount = 15},
      {type = "item", name = "copper-ore", amount = 15},
    },
  }
,


-- =========================================================
-- TIER 14 - Mineral slurry / brine chemistry chain
-- =========================================================

{
    type = "recipe",
    name = "trace-mineral-slurry",
    enabled = true,
    category = "clay",
    subgroup = "Seablock",
    icon = "__tanks_for_bob_fork__/graphics/icons/Trace mineral slurry.png",
    icon_size = 128,
    energy_required = 8,
    ingredients =
    {
      {type = "fluid", name = "water", amount = 500},
      {type = "item", name = "clay", amount = 10},
    },
    results =
    {
        {type = "item", name = "trace-mineral-slurry", amount = 5},
        {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.05},
    },
  }
,

{
    type = "recipe",
    name = "saline-particulate",
    enabled = false,
    category = "smelting",
    subgroup = "Seablock",
    icon = "__tanks_for_bob_fork__/graphics/icons/Saline particulate.png",
    icon_size = 128,
    energy_required = 6,
    ingredients =
    {
      {type = "item", name = "trace-mineral-slurry", amount = 15},
    },
    results =
    {
        {type = "item", name = "saline-particulate", amount = 3},
        {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.07},
    },
  }
,

{
    type = "recipe",
    name = "ionic-scum",
    enabled = false,
    category = "Calcifier",
    subgroup = "Seablock",
    icon = "__tanks_for_bob_fork__/graphics/icons/Ionic scum.png",
    icon_size = 128,
    energy_required = 10,
    ingredients =
    {
      {type = "item", name = "saline-particulate", amount = 15},
      {type = "fluid", name = "water", amount = 250},
    },
    results =
    {
      {type = "item", name = "ionic-scum", amount = 2},
      {type = "item", name = "tank-ammo-Industrialwaste", amount = 1},
    },
  }
,

{
    type = "recipe",
    name = "heavy-brine-fraction",
    enabled = false,
    category = "shaler",
    subgroup = "Seablock",
    icon = "__tanks_for_bob_fork__/graphics/icons/Heavy brine fraction.png",
    icon_size = 128,
    energy_required = 12,
    ingredients =
    {
      {type = "item", name = "saline-particulate", amount = 15},
      {type = "fluid", name = "steam", amount = 300},
    },
    results =
    {
        {type = "item", name = "heavy-brine-fraction", amount = 2},
        {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.09},
    },
  }
,

{
    type = "recipe",
    name = "microcrystal-sediment",
    enabled = false,
    category = "Calcifier",
    subgroup = "Seablock",
    icon = "__tanks_for_bob_fork__/graphics/icons/Microcrystal sediment.png",
    icon_size = 128,
    energy_required = 14,
    ingredients =
    {
      {type = "item", name = "heavy-brine-fraction", amount = 12},
      {type = "item", name = "stone", amount = 5},
      {type = "fluid", name = "water", amount = 250},
    },
    results =
    {
        {type = "item", name = "microcrystal-sediment", amount = 2},
        {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.08},
        {type = "item", name = "tank-ammo-Radioactivewaste", amount = 1, probability = 0.01},
    },
  }
,


-- =========================================================
-- TIER 15 - Biological rendering and fish chemistry
-- =========================================================

{
    type = "recipe",
    name = "fish-oil-residue",
    enabled = true,
    category = "cooking",
    subgroup = "Seablock",
    icon = "__tanks_for_bob_fork__/graphics/icons/Fish oil residue.png",
    icon_size = 128,
    energy_required = 9,
    ingredients =
    {
      {type = "item", name = "raw-fish", amount = 2},
    },
    results =
    {
        {type = "item", name = "fish-oil-residue", amount = 3},
        {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.04},
    },
  }
,

{
    type = "recipe",
    name = "protein-slurry",
    enabled = false,
    category = "advcooking",
    subgroup = "Seablock",
    icon = "__tanks_for_bob_fork__/graphics/icons/Protein slurry.png",
    icon_size = 128,
    energy_required = 10,
    ingredients =
    {
      {type = "item", name = "raw-fish", amount = 2},
      {type = "item", name = "fish-oil-residue", amount = 4},
    },
    results =
    {
        {type = "item", name = "protein-slurry", amount = 4},
        {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.04},
    },
  }
,

{
    type = "recipe",
    name = "calcified-bone-dust",
    enabled = false,
    category = "advcooking",
    subgroup = "Seablock",
    icon = "__tanks_for_bob_fork__/graphics/icons/Calcified bone dust.png",
    icon_size = 128,
    energy_required = 7,
    ingredients =
    {
      {type = "item", name = "raw-fish", amount = 8},
    },
    results =
    {
        {type = "item", name = "calcified-bone-dust", amount = 3},
        {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.03},
    },
  }
,

{
    type = "recipe",
    name = "rendered-organics",
    enabled = false,
    category = "advcooking",
    subgroup = "Seablock",
    icon = "__tanks_for_bob_fork__/graphics/icons/Rendered organics.png",
    icon_size = 128,
    energy_required = 12,
    ingredients =
    {
      {type = "item", name = "raw-fish", amount = 3},
      {type = "fluid", name = "steam", amount = 150},
    },
    results =
    {
        {type = "item", name = "rendered-organics", amount = 4},
        {type = "item", name = "fish-oil-residue", amount = 1},
        {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.06},
    },
  }
,

{
    type = "recipe",
    name = "enzyme-paste",
    enabled = false,
    category = "advcooking",
    subgroup = "Seablock",
    icon = "__tanks_for_bob_fork__/graphics/icons/Enzyme paste.png",
    icon_size = 128,
    energy_required = 8,
    ingredients =
    {
      {type = "item", name = "protein-slurry", amount = 2},
      {type = "item", name = "rendered-organics", amount = 1},
    },
    results =
    {
        {type = "item", name = "enzyme-paste", amount = 2},
        {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.05},
    },
  }
,

{
        type = "recipe",
        name = "meal",
        enabled = false,
        category = "advcooking",
        energy_required = 35,
        ingredients = {{type = "item", name = "Seared-fish",amount = 2}},
        results = {{type = "item", name = "meal", amount = 2}}}
,

{
        type = "recipe",
        name = "steam-meal",
        enabled = true,
        category = "advcooking",
        energy_required = 35,
        ingredients = {{type = "item", name = "Seared-fish",amount = 5},{type = "fluid", name = "steam", amount = 500}},
        results =
        {
            {type = "item", name = "meal", amount = 10},
            {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.03},
        }
    }
,




-- =========================================================
-- TIER 15-C - Corporate Compliance paperwork parasite chain
-- Board-validated administrative intermediates inserted before
-- pre-encabulation so later technologies can legally pretend
-- the factory has been authorized to continue existing.
-- =========================================================

{
    type = "recipe",
    name = "charcoal",
    enabled = false,
    category = "crafting",
    subgroup = "corporate-compliance",
    icon = "__tanks_for_bob_fork__/graphics/icons/charcoal.png",
    icon_size = 64,
    energy_required = 4,
    ingredients = {
        {type = "item", name = "wood", amount = 2}
    },
    results =
    {
        {type = "item", name = "charcoal", amount = 3},
        {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.06},
    }
}
,

{
    type = "recipe",
    name = "wood-pulp",
    enabled = false,
    category = "crafting",
    subgroup = "corporate-compliance",
    icon = "__tanks_for_bob_fork__/graphics/icons/wood-pulp.png",
    icon_size = 64,
    energy_required = 5,
    ingredients = {
        {type = "item", name = "wood", amount = 5},
		{type = "item", name = "stone-tools", amount = 1}
    },
    results =
    {
        {type = "item", name = "wood-pulp", amount = 6},
        {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.05},
    }
}
,

{
    type = "recipe",
    name = "crude-paper",
    enabled = false,
    category = "crafting",
    subgroup = "corporate-compliance",
    icon = "__tanks_for_bob_fork__/graphics/icons/crude-paper.png",
    icon_size = 64,
    energy_required = 6,
    ingredients = {
        {type = "item", name = "wood-pulp", amount = 4},
        {type = "item", name = "charcoal", amount = 1}
    },
    results =
    {
        {type = "item", name = "crude-paper", amount = 3},
        {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.04},
    }
}
,

{
    type = "recipe",
    name = "ink",
    enabled = false,
    category = "crafting",
    subgroup = "corporate-compliance",
    icon = "__tanks_for_bob_fork__/graphics/icons/ink.png",
    icon_size = 64,
    energy_required = 4,
    ingredients = {
        {type = "item", name = "charcoal", amount = 1},
        {type = "item", name = "fish-oil-residue", amount = 1}
    },
    results =
    {
        {type = "item", name = "ink", amount = 2},
        {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.05},
    }
}
,

{
    type = "recipe",
    name = "staples",
    enabled = false,
    category = "crafting",
    subgroup = "corporate-compliance",
    icon = "__tanks_for_bob_fork__/graphics/icons/staples.png",
    icon_size = 64,
    energy_required = 5,
    ingredients = {
        {type = "item", name = "iron-ore", amount = 2},
        {type = "item", name = "stone-tools", amount = 1}
    },
    results =
    {
        {type = "item", name = "staples", amount = 12},
        {type = "item", name = "stone-tools", amount = 1},
        {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.07},
    }
}
,

{
    type = "recipe",
    name = "stamps",
    enabled = false,
    category = "crafting",
    subgroup = "corporate-compliance",
    icon = "__tanks_for_bob_fork__/graphics/icons/stamps.png",
    icon_size = 64,
    energy_required = 6,
    ingredients = {
        {type = "item", name = "wood", amount = 2},
        {type = "item", name = "crude-glass", amount = 1},
        {type = "item", name = "ink", amount = 1}
    },
    results =
    {
        {type = "item", name = "stamps", amount = 2},
        {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.04},
    }
}
,

{
    type = "recipe",
    name = "folder",
    enabled = false,
    category = "crafting",
    subgroup = "corporate-compliance",
    icon = "__tanks_for_bob_fork__/graphics/icons/folder.png",
    icon_size = 64,
    energy_required = 5,
    ingredients = {
        {type = "item", name = "crude-paper", amount = 3},
        {type = "item", name = "wood-pulp", amount = 2}
    },
    results =
    {
        {type = "item", name = "folder", amount = 1},
        {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.03},
    }
}
,

{
    type = "recipe",
    name = "clipboard",
    enabled = false,
    category = "crafting",
    subgroup = "corporate-compliance",
    icon = "__tanks_for_bob_fork__/graphics/icons/clipboard.png",
    icon_size = 64,
    energy_required = 6,
    ingredients = {
        {type = "item", name = "wood", amount = 2},
        {type = "item", name = "crude-paper", amount = 2},
        {type = "item", name = "staples", amount = 2}
    },
    results =
    {
        {type = "item", name = "clipboard", amount = 1},
        {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.05},
    }
}
,

{
    type = "recipe",
    name = "requisition-slip",
    enabled = false,
    category = "crafting",
    subgroup = "corporate-compliance",
    icon = "__tanks_for_bob_fork__/graphics/icons/requisition-slip.png",
    icon_size = 64,
    energy_required = 7,
    ingredients = {
        {type = "item", name = "crude-paper", amount = 2},
        {type = "item", name = "ink", amount = 1},
        {type = "item", name = "fish-oil-residue", amount = 1}
    },
    results =
    {
        {type = "item", name = "requisition-slip", amount = 2},
        {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.04},
    }
}
,

{
    type = "recipe",
    name = "work-order-slip",
    enabled = false,
    category = "crafting",
    subgroup = "corporate-compliance",
    icon = "__tanks_for_bob_fork__/graphics/icons/work-order-slip.png",
    icon_size = 64,
    energy_required = 10,
    ingredients = {
        {type = "item", name = "requisition-slip", amount = 10},
        {type = "item", name = "meal", amount = 1},
        {type = "item", name = "staples", amount = 2},
        {type = "item", name = "ink", amount = 1}
    },
    results = {
        {type = "item", name = "work-order-slip", amount = 1, probability = 0.72},
        {type = "item", name = "corporate-waste", amount = 1, probability = 0.55}
    },
    allow_decomposition = false
}
,

{
    type = "recipe",
    name = "certified-work-order",
    enabled = false,
    category = "crafting",
    subgroup = "corporate-compliance",
    icon = "__tanks_for_bob_fork__/graphics/icons/certified-work-order.png",
    icon_size = 64,
    energy_required = 14,
    ingredients = {
        {type = "item", name = "work-order-slip", amount = 10},
        {type = "item", name = "trace-mineral-slurry", amount = 4},
        {type = "item", name = "Seared-fish", amount = 2},
        {type = "item", name = "stamps", amount = 2},
        {type = "item", name = "staples", amount = 4}
    },
    results = {
        {type = "item", name = "certified-work-order", amount = 1, probability = 0.68},
        {type = "item", name = "corporate-waste", amount = 2, probability = 0.65}
    },
    allow_decomposition = false
}
,

{
    type = "recipe",
    name = "submitted-evaluation",
    enabled = false,
    category = "crafting",
    subgroup = "corporate-compliance",
    icon = "__tanks_for_bob_fork__/graphics/icons/submitted-evaluation.png",
    icon_size = 64,
    energy_required = 18,
    ingredients = {
        {type = "item", name = "certified-work-order", amount = 10},
        {type = "item", name = "crude-glass", amount = 4},
        {type = "item", name = "fish-oil-residue", amount = 3},
        {type = "item", name = "clipboard", amount = 1},
        {type = "item", name = "staples", amount = 6}
    },
    results = {
        {type = "item", name = "submitted-evaluation", amount = 1, probability = 0.62},
        {type = "item", name = "corporate-waste", amount = 3, probability = 0.75}
    },
    allow_decomposition = false
}
,

{
    type = "recipe",
    name = "risk-assessment",
    enabled = false,
    category = "crafting",
    subgroup = "corporate-compliance",
    icon = "__tanks_for_bob_fork__/graphics/icons/risk-assessment.png",
    icon_size = 64,
    energy_required = 22,
    ingredients = {
        {type = "item", name = "submitted-evaluation", amount = 10},
        {type = "item", name = "ionic-scum", amount = 3},
        {type = "item", name = "tank-ammo-Industrialwaste", amount = 5},
        {type = "item", name = "staples", amount = 8},
        {type = "item", name = "ink", amount = 2}
    },
    results = {
        {type = "item", name = "risk-assessment", amount = 1, probability = 0.55},
        {type = "item", name = "corporate-waste", amount = 4, probability = 0.85}
    },
    allow_decomposition = false
}
,

{
    type = "recipe",
    name = "risk-assessed-work-order",
    enabled = false,
    category = "crafting",
    subgroup = "corporate-compliance",
    icon = "__tanks_for_bob_fork__/graphics/icons/risk-assessed-work-order.png",
    icon_size = 64,
    energy_required = 26,
    ingredients = {
        {type = "item", name = "risk-assessment", amount = 10},
        {type = "item", name = "certified-work-order", amount = 10},
        {type = "item", name = "meal", amount = 2},
        {type = "item", name = "folder", amount = 1},
        {type = "item", name = "staples", amount = 10}
    },
    results = {
        {type = "item", name = "risk-assessed-work-order", amount = 1, probability = 0.50},
        {type = "item", name = "corporate-waste", amount = 5, probability = 0.95}
    },
    allow_decomposition = false
}
,

{
    type = "recipe",
    name = "corporate-waste-reprocessing",
    enabled = false,
    category = "shaler",
    subgroup = "corporate-compliance",
    icon = "__tanks_for_bob_fork__/graphics/icons/corporate-waste.png",
    icon_size = 64,
    energy_required = 30,
    ingredients = {
        {type = "item", name = "corporate-waste", amount = 12},
        {type = "fluid", name = "water", amount = 500}
    },
    results = {
        {type = "item", name = "wood-pulp", amount = 1},
        {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.50}
    },
    allow_decomposition = false
}
,

-- Lossy corporate document decomposition. These recover a little material but deliberately
-- do not return enough paperwork to create an infinite loop.
{
    type = "recipe",
    name = "decompose-certified-work-order",
    enabled = false,
    category = "crafting",
    subgroup = "corporate-compliance",
    icon = "__tanks_for_bob_fork__/graphics/icons/certified-work-order.png",
    icon_size = 64,
    energy_required = 12,
    ingredients = {
        {type = "item", name = "certified-work-order", amount = 1}
    },
    results = {
        {type = "item", name = "work-order-slip", amount = 2},
        {type = "item", name = "stamps", amount = 1},
        {type = "item", name = "corporate-waste", amount = 2}
    },
    allow_decomposition = false
}
,
{
    type = "recipe",
    name = "decompose-submitted-evaluation",
    enabled = false,
    category = "crafting",
    subgroup = "corporate-compliance",
    icon = "__tanks_for_bob_fork__/graphics/icons/submitted-evaluation.png",
    icon_size = 64,
    energy_required = 16,
    ingredients = {
        {type = "item", name = "submitted-evaluation", amount = 1}
    },
    results = {
        {type = "item", name = "certified-work-order", amount = 1, probability = 0.35},
        {type = "item", name = "clipboard", amount = 1, probability = 0.50},
        {type = "item", name = "corporate-waste", amount = 3}
    },
    allow_decomposition = false
}
,
{
    type = "recipe",
    name = "decompose-risk-assessed-work-order",
    enabled = false,
    category = "crafting",
    subgroup = "corporate-compliance",
    icon = "__tanks_for_bob_fork__/graphics/icons/risk-assessed-work-order.png",
    icon_size = 64,
    energy_required = 20,
    ingredients = {
        {type = "item", name = "risk-assessed-work-order", amount = 1}
    },
    results = {
        {type = "item", name = "risk-assessment", amount = 1, probability = 0.25},
        {type = "item", name = "folder", amount = 1, probability = 0.50},
        {type = "item", name = "corporate-waste", amount = 5}
    },
    allow_decomposition = false
}
,
{
    type = "recipe",
    name = "decompose-audit-ready-deliverable",
    enabled = false,
    category = "crafting",
    subgroup = "corporate-compliance",
    icon = "__tanks_for_bob_fork__/graphics/icons/audit-ready-deliverable.png",
    icon_size = 64,
    energy_required = 24,
    ingredients = {
        {type = "item", name = "audit-ready-deliverable", amount = 1}
    },
    results = {
        {type = "item", name = "compliance-packet", amount = 1, probability = 0.20},
        {type = "item", name = "clipboard", amount = 1, probability = 0.35},
        {type = "item", name = "corporate-waste", amount = 6}
    },
    allow_decomposition = false
}
,

{
    type = "recipe",
    name = "compliance-packet",
    enabled = false,
    category = "crafting",
    subgroup = "corporate-compliance",
    icon = "__tanks_for_bob_fork__/graphics/icons/compliance-packet.png",
    icon_size = 64,
    energy_required = 28,
    ingredients = {
        {type = "item", name = "risk-assessed-work-order", amount = 4},
        {type = "item", name = "balanced-reactive-medium", amount = 2},
        {type = "item", name = "folder", amount = 2},
        {type = "item", name = "stamps", amount = 2}
    },
    results =
    {
        {type = "item", name = "compliance-packet", amount = 1},
        {type = "item", name = "corporate-waste", amount = 2, probability = 0.35},
        {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.08},
    },
    allow_decomposition = false
}
,

{
    type = "recipe",
    name = "audit-ready-deliverable",
    enabled = false,
    category = "crafting",
    subgroup = "corporate-compliance",
    icon = "__tanks_for_bob_fork__/graphics/icons/audit-ready-deliverable.png",
    icon_size = 64,
    energy_required = 32,
    ingredients = {
        {type = "item", name = "compliance-packet", amount = 3},
        {type = "item", name = "phase-primed-carrier", amount = 2},
        {type = "item", name = "electro-phase-precursor", amount = 2},
        {type = "item", name = "clipboard", amount = 1}
    },
    results =
    {
        {type = "item", name = "audit-ready-deliverable", amount = 1},
        {type = "item", name = "corporate-waste", amount = 3, probability = 0.40},
        {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.09},
        {type = "item", name = "tank-ammo-Radioactivewaste", amount = 1, probability = 0.01},
    },
    allow_decomposition = false
}
,

{
    type = "recipe",
    name = "stakeholder-review-summary",
    enabled = false,
    category = "crafting",
    subgroup = "corporate-compliance",
    icon = "__tanks_for_bob_fork__/graphics/icons/stakeholder-review-summary.png",
    icon_size = 64,
    energy_required = 36,
    ingredients = {
        {type = "item", name = "audit-ready-deliverable", amount = 3},
        {type = "item", name = "executive-marseline-resin", amount = 1},
        {type = "item", name = "meal", amount = 4},
        {type = "item", name = "ink", amount = 4}
    },
    results =
    {
        {type = "item", name = "stakeholder-review-summary", amount = 1},
        {type = "item", name = "corporate-waste", amount = 4, probability = 0.45},
        {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.10},
        {type = "item", name = "tank-ammo-Radioactivewaste", amount = 1, probability = 0.01},
    },
    allow_decomposition = false
}
,

{
    type = "recipe",
    name = "liability-contained-report",
    enabled = false,
    category = "crafting",
    subgroup = "corporate-compliance",
    icon = "__tanks_for_bob_fork__/graphics/icons/liability-contained-report.png",
    icon_size = 64,
    energy_required = 40,
    ingredients = {
        {type = "item", name = "stakeholder-review-summary", amount = 2},
        {type = "item", name = "tank-ammo-Industrialwaste", amount = 10},
        {type = "item", name = "Canister", amount = 1},
        {type = "item", name = "folder", amount = 4}
    },
    results =
    {
        {type = "item", name = "liability-contained-report", amount = 1},
        {type = "item", name = "corporate-waste", amount = 5, probability = 0.50},
        {type = "item", name = "tank-ammo-Radioactivewaste", amount = 1, probability = 0.02},
    },
    allow_decomposition = false
}
,

{
    type = "recipe",
    name = "board-review-docket",
    enabled = false,
    category = "crafting",
    subgroup = "corporate-compliance",
    icon = "__tanks_for_bob_fork__/graphics/icons/board-review-docket.png",
    icon_size = 64,
    energy_required = 45,
    ingredients = {
        {type = "item", name = "liability-contained-report", amount = 2},
        {type = "item", name = "hyperphase-matrix", amount = 1},
        {type = "item", name = "retrograde-polymer-sheet", amount = 1},
        {type = "item", name = "stamps", amount = 6}
    },
    results =
    {
        {type = "item", name = "board-review-docket", amount = 1},
        {type = "item", name = "corporate-waste", amount = 6, probability = 0.55},
        {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.12},
        {type = "item", name = "tank-ammo-Radioactivewaste", amount = 1, probability = 0.02},
    },
    allow_decomposition = false
}
,

{
    type = "recipe",
    name = "board-advisory-risk-assessment",
    enabled = false,
    category = "crafting",
    subgroup = "corporate-compliance",
    icon = "__tanks_for_bob_fork__/graphics/icons/board-advisory-risk-assessment.png",
    icon_size = 64,
    energy_required = 60,
    ingredients = {
        {type = "item", name = "board-review-docket", amount = 2},
        {type = "item", name = "HyperEncabulator", amount = 1},
        {type = "item", name = "FramulatedEncabulator", amount = 1},
        {type = "item", name = "tank-ammo-Radioactivewaste", amount = 20},
        {type = "item", name = "liability-contained-report", amount = 1}
    },
    results =
    {
        {type = "item", name = "board-advisory-risk-assessment", amount = 1},
        {type = "item", name = "corporate-waste", amount = 10, probability = 0.75},
        {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.14},
        {type = "item", name = "tank-ammo-Radioactivewaste", amount = 1, probability = 0.04},
    },
    allow_decomposition = false
}
,

-- =========================================================
-- TIER 16 - Preencabulation conditioning layer / punishing basic-material sinks
-- =========================================================

{
    type = "recipe",
    name = "hydrolyzed-suspension",
    enabled = false,
    category = "crafting",
    subgroup = "Preencabulation",
    icon = "__tanks_for_bob_fork__/graphics/icons/hydrolyzed-suspension.png",
    icon_size = 128,
    energy_required = 10,
    ingredients =
        {
      {type = "item", name = "saline-particulate", amount = 2},
      {type = "item", name = "trace-mineral-slurry", amount = 2},
      {type = "item", name = "stone", amount = 40},
      {type = "item", name = "wood", amount = 20},
    },
    results =
    {
        {type = "item", name = "hydrolyzed-suspension", amount = 2},
        {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.06},
    },
  }
,

{
    type = "recipe",
    name = "phase-diluted-brine",
    enabled = false,
    category = "crafting",
    subgroup = "Preencabulation",
    icon = "__tanks_for_bob_fork__/graphics/icons/phase-diluted-brine.png",
    icon_size = 128,
    energy_required = 8,
    ingredients =
        {
      {type = "item", name = "hydrolyzed-suspension", amount = 1},
      {type = "item", name = "stone", amount = 35},
      {type = "item", name = "iron-ore", amount = 18},
      {type = "item", name = "copper-ore", amount = 12},
    },
    results =
    {
        {type = "item", name = "phase-diluted-brine", amount = 2},
        {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.07},
    },
  }
,

{
    type = "recipe",
    name = "osmotic-residue",
    enabled = false,
    category = "crafting",
    subgroup = "Preencabulation",
    icon = "__tanks_for_bob_fork__/graphics/icons/osmotic-residue.png",
    icon_size = 128,
    energy_required = 8,
    ingredients =
        {
      {type = "item", name = "hydrolyzed-suspension", amount = 1},
      {type = "item", name = "stone", amount = 45},
      {type = "item", name = "brick", amount = 12},
      {type = "item", name = "iron-ore", amount = 12},
    },
    results =
    {
      {type = "item", name = "osmotic-residue", amount = 2},
      {type = "item", name = "tank-ammo-Industrialwaste", amount = 1},
    },
  }
,

{
    type = "recipe",
    name = "gradient-saline-matrix",
    enabled = false,
    category = "crafting",
    subgroup = "Preencabulation",
    icon = "__tanks_for_bob_fork__/graphics/icons/gradient-saline-matrix.png",
    icon_size = 128,
    energy_required = 10,
    ingredients =
        {
      {type = "item", name = "hydrolyzed-suspension", amount = 1},
      {type = "item", name = "crude-glass", amount = 8},
      {type = "item", name = "copper-ore", amount = 22},
      {type = "item", name = "stone", amount = 25},
    },
    results =
    {
        {type = "item", name = "gradient-saline-matrix", amount = 2},
        {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.08},
    },
  }
,

{
    type = "recipe",
    name = "biphasic-brine-gel",
    enabled = false,
    category = "crafting",
    subgroup = "Preencabulation",
    icon = "__tanks_for_bob_fork__/graphics/icons/biphasic-brine-gel.png",
    icon_size = 128,
    energy_required = 12,
    ingredients =
        {
      {type = "item", name = "phase-diluted-brine", amount = 1},
      {type = "item", name = "osmotic-residue", amount = 1},
      {type = "item", name = "brick", amount = 22},
      {type = "item", name = "iron-ore", amount = 22},
    },
    results =
    {
        {type = "item", name = "biphasic-brine-gel", amount = 2},
        {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.08},
    },
  }
,

{
    type = "recipe",
    name = "salinity-locked-emulsion",
    enabled = false,
    category = "crafting",
    subgroup = "Preencabulation",
    icon = "__tanks_for_bob_fork__/graphics/icons/salinity-locked-emulsion.png",
    icon_size = 128,
    energy_required = 12,
    ingredients =
        {
      {type = "item", name = "gradient-saline-matrix", amount = 1},
      {type = "item", name = "osmotic-residue", amount = 1},
      {type = "item", name = "crude-glass", amount = 10},
      {type = "item", name = "copper-ore", amount = 26},
    },
    results =
    {
        {type = "item", name = "salinity-locked-emulsion", amount = 2},
        {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.09},
    },
  }
,

{
    type = "recipe",
    name = "hydrocoptic-precursor",
    enabled = false,
    category = "crafting",
    subgroup = "Preencabulation",
    icon = "__tanks_for_bob_fork__/graphics/icons/hydrocoptic-precursor.png",
    icon_size = 128,
    energy_required = 16,
    ingredients =
        {
      {type = "item", name = "biphasic-brine-gel", amount = 1},
      {type = "item", name = "salinity-locked-emulsion", amount = 1},
      {type = "item", name = "iron-gear-wheel", amount = 20},
      {type = "item", name = "stone", amount = 80},
    },
    results =
    {
        {type = "item", name = "hydrocoptic-precursor", amount = 1},
        {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.10},
        {type = "item", name = "tank-ammo-Radioactivewaste", amount = 1, probability = 0.01},
    },
  }
,

{
    type = "recipe",
    name = "denatured-organic-base",
    enabled = false,
    category = "crafting",
    subgroup = "Preencabulation",
    icon = "__tanks_for_bob_fork__/graphics/icons/denatured-organic-base.png",
    icon_size = 128,
    energy_required = 10,
    ingredients =
        {
      {type = "item", name = "protein-slurry", amount = 2},
      {type = "item", name = "rendered-organics", amount = 1},
      {type = "item", name = "wood", amount = 45},
      {type = "item", name = "stone", amount = 30},
    },
    results =
    {
        {type = "item", name = "denatured-organic-base", amount = 2},
        {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.07},
    },
  }
,

{
    type = "recipe",
    name = "enzyme-saturated-mass",
    enabled = false,
    category = "crafting",
    subgroup = "Preencabulation",
    icon = "__tanks_for_bob_fork__/graphics/icons/enzyme-saturated-mass.png",
    icon_size = 128,
    energy_required = 8,
    ingredients =
        {
      {type = "item", name = "denatured-organic-base", amount = 1},
      {type = "item", name = "enzyme-paste", amount = 1},
      {type = "item", name = "wood", amount = 30},
      {type = "item", name = "copper-ore", amount = 12},
    },
    results =
    {
        {type = "item", name = "enzyme-saturated-mass", amount = 2},
        {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.08},
    },
  }
,

{
    type = "recipe",
    name = "lipid-carrier-gel",
    enabled = false,
    category = "crafting",
    subgroup = "Preencabulation",
    icon = "__tanks_for_bob_fork__/graphics/icons/lipid-carrier-gel.png",
    icon_size = 128,
    energy_required = 8,
    ingredients =
        {
      {type = "item", name = "denatured-organic-base", amount = 1},
      {type = "item", name = "fish-oil-residue", amount = 1},
      {type = "item", name = "wood", amount = 35},
      {type = "item", name = "stone", amount = 25},
    },
    results =
    {
        {type = "item", name = "lipid-carrier-gel", amount = 2},
        {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.07},
    },
  }
,

{
    type = "recipe",
    name = "bio-reactive-slurry",
    enabled = false,
    category = "crafting",
    subgroup = "Preencabulation",
    icon = "__tanks_for_bob_fork__/graphics/icons/bio-reactive-slurry.png",
    icon_size = 128,
    energy_required = 10,
    ingredients =
        {
      {type = "item", name = "denatured-organic-base", amount = 1},
      {type = "item", name = "fish-oil-residue", amount = 1},
      {type = "item", name = "copper-ore", amount = 20},
      {type = "item", name = "wood", amount = 25},
    },
    results =
    {
        {type = "item", name = "bio-reactive-slurry", amount = 2},
        {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.09},
    },
  }
,

{
    type = "recipe",
    name = "catalytic-organic-medium",
    enabled = false,
    category = "crafting",
    subgroup = "Preencabulation",
    icon = "__tanks_for_bob_fork__/graphics/icons/catalytic-organic-medium.png",
    icon_size = 128,
    energy_required = 12,
    ingredients =
        {
      {type = "item", name = "enzyme-saturated-mass", amount = 1},
      {type = "item", name = "lipid-carrier-gel", amount = 1},
      {type = "item", name = "copper-cable", amount = 30},
      {type = "item", name = "brick", amount = 18},
    },
    results =
    {
        {type = "item", name = "catalytic-organic-medium", amount = 2},
        {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.10},
        {type = "item", name = "tank-ammo-Radioactivewaste", amount = 1, probability = 0.01},
    },
  }
,

{
    type = "recipe",
    name = "reactive-enzyme-binder",
    enabled = false,
    category = "crafting",
    subgroup = "Preencabulation",
    icon = "__tanks_for_bob_fork__/graphics/icons/reactive-enzyme-binder.png",
    icon_size = 128,
    energy_required = 12,
    ingredients =
        {
      {type = "item", name = "bio-reactive-slurry", amount = 1},
      {type = "item", name = "enzyme-saturated-mass", amount = 1},
      {type = "item", name = "iron-plate", amount = 16},
      {type = "item", name = "iron-stick", amount = 16},
    },
    results =
    {
        {type = "item", name = "reactive-enzyme-binder", amount = 2},
        {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.08},
    },
  }
,

{
    type = "recipe",
    name = "bio-synthetic-precursor",
    enabled = false,
    category = "crafting",
    subgroup = "Preencabulation",
    icon = "__tanks_for_bob_fork__/graphics/icons/bio-synthetic-precursor.png",
    icon_size = 128,
    energy_required = 16,
    ingredients =
        {
      {type = "item", name = "catalytic-organic-medium", amount = 1},
      {type = "item", name = "reactive-enzyme-binder", amount = 1},
      {type = "item", name = "iron-gear-wheel", amount = 20},
      {type = "item", name = "copper-cable", amount = 40},
      {type = "item", name = "wood", amount = 80},
    },
    results =
    {
        {type = "item", name = "bio-synthetic-precursor", amount = 1},
        {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.11},
        {type = "item", name = "tank-ammo-Radioactivewaste", amount = 1, probability = 0.01},
    },
  }
,

{
    type = "recipe",
    name = "crystalline-agglomerate",
    enabled = false,
    category = "crafting",
    subgroup = "Preencabulation",
    icon = "__tanks_for_bob_fork__/graphics/icons/crystalline-agglomerate.png",
    icon_size = 128,
    energy_required = 10,
    ingredients =
        {
      {type = "item", name = "microcrystal-sediment", amount = 2},
      {type = "item", name = "calcified-bone-dust", amount = 2},
      {type = "item", name = "stone", amount = 80},
      {type = "item", name = "brick", amount = 25},
    },
    results =
    {
        {type = "item", name = "crystalline-agglomerate", amount = 2},
        {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.08},
    },
  }
,

{
    type = "recipe",
    name = "fractured-lattice-mass",
    enabled = false,
    category = "crafting",
    subgroup = "Preencabulation",
    icon = "__tanks_for_bob_fork__/graphics/icons/fractured-lattice-mass.png",
    icon_size = 128,
    energy_required = 8,
    ingredients =
        {
      {type = "item", name = "crystalline-agglomerate", amount = 1},
      {type = "item", name = "stone", amount = 70},
      {type = "item", name = "iron-ore", amount = 18},
      {type = "item", name = "copper-ore", amount = 12},
    },
    results =
    {
        {type = "item", name = "fractured-lattice-mass", amount = 2},
        {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.09},
    },
  }
,

{
    type = "recipe",
    name = "ceramic-seed-grain",
    enabled = false,
    category = "crafting",
    subgroup = "Preencabulation",
    icon = "__tanks_for_bob_fork__/graphics/icons/ceramic-seed-grain.png",
    icon_size = 128,
    energy_required = 8,
    ingredients =
        {
      {type = "item", name = "crystalline-agglomerate", amount = 1},
      {type = "item", name = "brick", amount = 35},
      {type = "item", name = "stone", amount = 40},
      {type = "item", name = "iron-stick", amount = 8},
    },
    results =
    {
        {type = "item", name = "ceramic-seed-grain", amount = 2},
        {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.08},
    },
  }
,

{
    type = "recipe",
    name = "mineral-phase-fragments",
    enabled = false,
    category = "crafting",
    subgroup = "Preencabulation",
    icon = "__tanks_for_bob_fork__/graphics/icons/mineral-phase-fragments.png",
    icon_size = 128,
    energy_required = 10,
    ingredients =
        {
      {type = "item", name = "crystalline-agglomerate", amount = 1},
      {type = "item", name = "stone", amount = 65},
      {type = "item", name = "iron-ore", amount = 25},
      {type = "item", name = "brick", amount = 20},
    },
    results =
    {
        {type = "item", name = "mineral-phase-fragments", amount = 2},
        {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.10},
        {type = "item", name = "tank-ammo-Radioactivewaste", amount = 1, probability = 0.01},
    },
  }
,

{
    type = "recipe",
    name = "ceramic-lattice-core",
    enabled = false,
    category = "crafting",
    subgroup = "Preencabulation",
    icon = "__tanks_for_bob_fork__/graphics/icons/ceramic-lattice-core.png",
    icon_size = 128,
    energy_required = 12,
    ingredients =
        {
      {type = "item", name = "fractured-lattice-mass", amount = 1},
      {type = "item", name = "ceramic-seed-grain", amount = 1},
      {type = "item", name = "brick", amount = 45},
      {type = "item", name = "iron-plate", amount = 18},
    },
    results =
    {
        {type = "item", name = "ceramic-lattice-core", amount = 2},
        {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.11},
    },
  }
,

{
    type = "recipe",
    name = "compressed-crystal-bed",
    enabled = false,
    category = "crafting",
    subgroup = "Preencabulation",
    icon = "__tanks_for_bob_fork__/graphics/icons/compressed-crystal-bed.png",
    icon_size = 128,
    energy_required = 12,
    ingredients =
        {
      {type = "item", name = "mineral-phase-fragments", amount = 1},
      {type = "item", name = "fractured-lattice-mass", amount = 1},
      {type = "item", name = "stone", amount = 90},
      {type = "item", name = "copper-plate", amount = 18},
    },
    results =
    {
        {type = "item", name = "compressed-crystal-bed", amount = 2},
        {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.12},
        {type = "item", name = "tank-ammo-Radioactivewaste", amount = 1, probability = 0.02},
    },
  }
,

{
    type = "recipe",
    name = "bioceramic-preform",
    enabled = false,
    category = "crafting",
    subgroup = "Preencabulation",
    icon = "__tanks_for_bob_fork__/graphics/icons/bioceramic-preform.png",
    icon_size = 128,
    energy_required = 16,
    ingredients =
        {
      {type = "item", name = "ceramic-lattice-core", amount = 1},
      {type = "item", name = "compressed-crystal-bed", amount = 1},
      {type = "item", name = "brick", amount = 70},
      {type = "item", name = "stone", amount = 120},
      {type = "item", name = "iron-gear-wheel", amount = 24},
    },
    results =
    {
        {type = "item", name = "bioceramic-preform", amount = 1},
        {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.10},
    },
  }
,

{
    type = "recipe",
    name = "charged-ionic-matrix",
    enabled = false,
    category = "crafting",
    subgroup = "Preencabulation",
    icon = "__tanks_for_bob_fork__/graphics/icons/charged-ionic-matrix.png",
    icon_size = 128,
    energy_required = 10,
    ingredients =
        {
      {type = "item", name = "ionic-scum", amount = 2},
      {type = "item", name = "copper-ore", amount = 35},
      {type = "item", name = "iron-ore", amount = 15},
      {type = "item", name = "stone", amount = 35},
    },
    results =
    {
        {type = "item", name = "charged-ionic-matrix", amount = 2},
        {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.11},
        {type = "item", name = "tank-ammo-Radioactivewaste", amount = 1, probability = 0.02},
    },
  }
,

{
    type = "recipe",
    name = "dielectric-suspension",
    enabled = false,
    category = "crafting",
    subgroup = "Preencabulation",
    icon = "__tanks_for_bob_fork__/graphics/icons/dielectric-suspension.png",
    icon_size = 128,
    energy_required = 8,
    ingredients =
        {
      {type = "item", name = "charged-ionic-matrix", amount = 1},
      {type = "item", name = "copper-cable", amount = 40},
      {type = "item", name = "copper-plate", amount = 12},
      {type = "item", name = "stone", amount = 20},
    },
    results =
    {
        {type = "item", name = "dielectric-suspension", amount = 2},
        {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.10},
    },
  }
,

{
    type = "recipe",
    name = "conductive-residue",
    enabled = false,
    category = "crafting",
    subgroup = "Preencabulation",
    icon = "__tanks_for_bob_fork__/graphics/icons/conductive-residue.png",
    icon_size = 128,
    energy_required = 8,
    ingredients =
        {
      {type = "item", name = "charged-ionic-matrix", amount = 1},
      {type = "item", name = "iron-plate", amount = 16},
      {type = "item", name = "copper-plate", amount = 12},
      {type = "item", name = "iron-stick", amount = 12},
    },
    results =
    {
        {type = "item", name = "conductive-residue", amount = 2},
        {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.12},
        {type = "item", name = "tank-ammo-Radioactivewaste", amount = 1, probability = 0.02},
    },
  }
,

{
    type = "recipe",
    name = "phase-unstable-granulate",
    enabled = false,
    category = "crafting",
    subgroup = "Preencabulation",
    icon = "__tanks_for_bob_fork__/graphics/icons/phase-unstable-granulate.png",
    icon_size = 128,
    energy_required = 10,
    ingredients =
        {
      {type = "item", name = "charged-ionic-matrix", amount = 1},
      {type = "item", name = "saline-particulate", amount = 2},
      {type = "item", name = "iron-ore", amount = 30},
      {type = "item", name = "copper-ore", amount = 30},
    },
    results =
    {
        {type = "item", name = "phase-unstable-granulate", amount = 2},
        {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.13},
        {type = "item", name = "tank-ammo-Radioactivewaste", amount = 1, probability = 0.03},
    },
  }
,

{
    type = "recipe",
    name = "balanced-reactive-medium",
    enabled = false,
    category = "crafting",
    subgroup = "Preencabulation",
    icon = "__tanks_for_bob_fork__/graphics/icons/balanced-reactive-medium.png",
    icon_size = 128,
    energy_required = 12,
    ingredients =
        {
      {type = "item", name = "dielectric-suspension", amount = 1},
      {type = "item", name = "conductive-residue", amount = 1},
      {type = "item", name = "iron-gear-wheel", amount = 16},
      {type = "item", name = "copper-cable", amount = 35},
    },
    results =
    {
        {type = "item", name = "balanced-reactive-medium", amount = 2},
        {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.12},
        {type = "item", name = "tank-ammo-Radioactivewaste", amount = 1, probability = 0.02},
    },
  }
,

{
    type = "recipe",
    name = "phase-primed-carrier",
    enabled = false,
    category = "crafting",
    subgroup = "Preencabulation",
    icon = "__tanks_for_bob_fork__/graphics/icons/phase-primed-carrier.png",
    icon_size = 128,
    energy_required = 12,
    ingredients =
        {
      {type = "item", name = "phase-unstable-granulate", amount = 1},
      {type = "item", name = "dielectric-suspension", amount = 1},
      {type = "item", name = "copper-plate", amount = 24},
      {type = "item", name = "iron-stick", amount = 18},
    },
    results =
    {
        {type = "item", name = "phase-primed-carrier", amount = 2},
        {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.13},
        {type = "item", name = "tank-ammo-Radioactivewaste", amount = 1, probability = 0.03},
    },
  }
,

{
    type = "recipe",
    name = "electro-phase-precursor",
    enabled = false,
    category = "crafting",
    subgroup = "Preencabulation",
    icon = "__tanks_for_bob_fork__/graphics/icons/electro-phase-precursor.png",
    icon_size = 128,
    energy_required = 16,
    ingredients =
        {
      {type = "item", name = "balanced-reactive-medium", amount = 1},
      {type = "item", name = "phase-primed-carrier", amount = 1},
      {type = "item", name = "iron-gear-wheel", amount = 28},
      {type = "item", name = "copper-cable", amount = 60},
      {type = "item", name = "brick", amount = 40},
    },
    results =
    {
        {type = "item", name = "electro-phase-precursor", amount = 1},
        {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.14},
        {type = "item", name = "tank-ammo-Radioactivewaste", amount = 1, probability = 0.04},
    },
  }
,

-- =========================================================
-- TIER 17 - Hybrid mineral-biological intermediates
-- =========================================================

{
    type = "recipe",
    name = "marseline-compound",
    enabled = false,
    category = "crafting",
    subgroup = "tank-ammo-components",
    icon = "__tanks_for_bob_fork__/graphics/icons/Marseline compound.png",
    icon_size = 128,
    energy_required = 12,
    ingredients =
    {
      {type = "item", name = "hydrocoptic-precursor", amount = 1},
      {type = "item", name = "bio-synthetic-precursor", amount = 1},
      {type = "item", name = "trace-mineral-slurry", amount = 2},
    },
    results =
    {
        {type = "item", name = "marseline-compound", amount = 2},
        {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.10},
    },
  }
,

{
    type = "recipe",
    name = "bioceramic-grit",
    enabled = false,
    category = "smelting",
    subgroup = "tank-ammo-components",
    icon = "__tanks_for_bob_fork__/graphics/icons/Bioceramic grit.png",
    icon_size = 128,
    energy_required = 8,
    ingredients =
    {
      {type = "item", name = "bioceramic-preform", amount = 1},
      {type = "item", name = "calcified-bone-dust", amount = 1},
    },
    results =
    {
        {type = "item", name = "bioceramic-grit", amount = 1},
        {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.08},
    },
  }
,

{
    type = "recipe",
    name = "hydrocoptic-crystal",
    enabled = false,
    category = "Calcifier",
    subgroup = "tank-ammo-components",
    icon = "__tanks_for_bob_fork__/graphics/icons/Hydrocoptic crystal.png",
    icon_size = 128,
    energy_required = 16,
    ingredients =
    {
      {type = "item", name = "hydrocoptic-precursor", amount = 1},
      {type = "item", name = "bioceramic-preform", amount = 1},
      {type = "fluid", name = "water", amount = 150},
    },
    results =
    {
        {type = "item", name = "hydrocoptic-crystal", amount = 2},
        {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.11},
        {type = "item", name = "tank-ammo-Radioactivewaste", amount = 1, probability = 0.02},
    },
  }
,

{
    type = "recipe",
    name = "amulite-flakes",
    enabled = false,
    category = "shaler",
    subgroup = "tank-ammo-components",
    icon = "__tanks_for_bob_fork__/graphics/icons/Amulite flakes.png",
    icon_size = 128,
    energy_required = 18,
    ingredients =
    {
      {type = "item", name = "marseline-compound", amount = 2},
      {type = "item", name = "hydrocoptic-crystal", amount = 1},
      {type = "fluid", name = "steam", amount = 250},
    },
    results =
    {
      {type = "item", name = "amulite-flakes", amount = 2},
      {type = "item", name = "tank-ammo-Industrialwaste", amount = 1},
    },
  }
,

{
    type = "recipe",
    name = "phase-reactive-granules",
    enabled = false,
    category = "crafting",
    subgroup = "tank-ammo-components",
    icon = "__tanks_for_bob_fork__/graphics/icons/Phase reactive granules.png",
    icon_size = 128,
    energy_required = 14,
    ingredients =
    {
      {type = "item", name = "electro-phase-precursor", amount = 1},
      {type = "item", name = "bioceramic-preform", amount = 1},
      {type = "item", name = "copper-plate", amount = 1},
    },
    results =
    {
        {type = "item", name = "phase-reactive-granules", amount = 2},
        {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.12},
        {type = "item", name = "tank-ammo-Radioactivewaste", amount = 1, probability = 0.02},
    },
  }
,


-- =========================================================
-- TIER 18 - Stabilized material intermediates
-- =========================================================

{
    type = "recipe",
    name = "oscillated-lubricant",
    enabled = false,
    category = "crafting",
    subgroup = "tank-ammo-components",
    icon = "__tanks_for_bob_fork__/graphics/icons/Oscillated lubricant.png",
    icon_size = 128,
    energy_required = 12,
    ingredients =
    {
      {type = "item", name = "bio-synthetic-precursor", amount = 1},
      {type = "item", name = "electro-phase-precursor", amount = 1},
      {type = "item", name = "fish-oil-residue", amount = 1},
    },
    results =
    {
        {type = "item", name = "oscillated-lubricant", amount = 2},
        {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.09},
    },
  }
,

{
    type = "recipe",
    name = "stabilized-brine-gel",
    enabled = false,
    category = "crafting",
    subgroup = "tank-ammo-components",
    icon = "__tanks_for_bob_fork__/graphics/icons/Stabilized brine gel.png",
    icon_size = 128,
    energy_required = 12,
    ingredients =
    {
      {type = "item", name = "hydrocoptic-precursor", amount = 1},
      {type = "item", name = "bio-synthetic-precursor", amount = 1},
    },
    results =
    {
        {type = "item", name = "stabilized-brine-gel", amount = 2},
        {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.10},
    },
  }
,

{
    type = "recipe",
    name = "dielectric-chowder",
    enabled = false,
    category = "crafting",
    subgroup = "tank-ammo-components",
    icon = "__tanks_for_bob_fork__/graphics/icons/Dielectric chowder.png",
    icon_size = 128,
    energy_required = 16,
    ingredients =
    {
      {type = "item", name = "electro-phase-precursor", amount = 1},
      {type = "item", name = "bio-synthetic-precursor", amount = 1},
      {type = "item", name = "copper-cable", amount = 2},
    },
    results =
    {
        {type = "item", name = "dielectric-chowder", amount = 2},
        {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.11},
        {type = "item", name = "tank-ammo-Radioactivewaste", amount = 1, probability = 0.02},
    },
  }
,

{
    type = "recipe",
    name = "pre-turbulated-emulsion",
    enabled = false,
    category = "crafting",
    subgroup = "tank-ammo-components",
    icon = "__tanks_for_bob_fork__/graphics/icons/Pre turbulated Emulsion.png",
    icon_size = 128,
    energy_required = 18,
    ingredients =
    {
      {type = "item", name = "oscillated-lubricant", amount = 1},
      {type = "item", name = "stabilized-brine-gel", amount = 1},
      {type = "item", name = "phase-reactive-granules", amount = 1},
    },
    results =
    {
        {type = "item", name = "pre-turbulated-emulsion", amount = 2},
        {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.12},
        {type = "item", name = "tank-ammo-Radioactivewaste", amount = 1, probability = 0.02},
    },
  }
,

{
    type = "recipe",
    name = "viscoelastic-froth",
    enabled = false,
    category = "crafting",
    subgroup = "tank-ammo-components",
    icon = "__tanks_for_bob_fork__/graphics/icons/Viscoelastic froth.png",
    icon_size = 128,
    energy_required = 18,
    ingredients =
    {
      {type = "item", name = "rendered-organics", amount = 2},
      {type = "item", name = "stabilized-brine-gel", amount = 1},
      {type = "item", name = "crude-glass", amount = 1},
    },
    results =
    {
        {type = "item", name = "viscoelastic-froth", amount = 2},
        {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.09},
    },
  }
,

-- =========================================================
-- Toxic Sludge Condensation / Waste Liquefaction
-- =========================================================
{
  type = "recipe",
  name = "compress-toxic-sludge",
  enabled = false,
  category = "crafting-with-fluid",
  subgroup = "corporate-compliance",
  icon = "__tanks_for_bob_fork__/graphics/icons/compressed-biohazard-waste.png",
  icon_size = 64,
  energy_required = 15,
  ingredients =
  {
    {type = "fluid", name = "toxic-sludge", amount = 50},
    {type = "item", name = "Canister", amount = 1}
  },
  results =
  {
    {type = "item", name = "compressed-biohazard-waste", amount = 1}
  },
  allow_decomposition = false
}
,
{
  type = "recipe",
  name = "industrial-waste-to-toxic-sludge",
  enabled = false,
  category = "crafting-with-fluid",
  subgroup = "corporate-compliance",
  icon = "__tanks_for_bob_fork__/graphics/icons/toxic-sludge.png",
  icon_size = 64,
  energy_required = 8,
  ingredients =
  {
    {type = "item", name = "tank-ammo-Industrialwaste", amount = 25},
    {type = "fluid", name = "water", amount = 100}
  },
  results =
  {
    {type = "fluid", name = "toxic-sludge", amount = 100}
  },
  allow_decomposition = false
}
,

{
  type = "recipe",
  name = "radioactive-waste-to-toxic-sludge",
  enabled = false,
  category = "crafting-with-fluid",
  subgroup = "corporate-compliance",
  icon = "__tanks_for_bob_fork__/graphics/icons/toxic-sludge.png",
  icon_size = 64,
  energy_required = 12,
  ingredients =
  {
    {type = "item", name = "tank-ammo-Radioactivewaste", amount = 5},
    {type = "fluid", name = "water", amount = 100}
  },
  results =
  {
    {type = "fluid", name = "toxic-sludge", amount = 15}
  },
  allow_decomposition = false
}
,

{
  type = "recipe",
  name = "corporate-waste-to-toxic-sludge",
  enabled = false,
  category = "crafting-with-fluid",
  subgroup = "corporate-compliance",
  icon = "__tanks_for_bob_fork__/graphics/icons/toxic-sludge.png",
  icon_size = 64,
  energy_required = 10,
  ingredients =
  {
    {type = "item", name = "corporate-waste", amount = 40},
    {type = "fluid", name = "water", amount = 100}
  },
  results =
  {
    {type = "fluid", name = "toxic-sludge", amount = 50}
  },
  allow_decomposition = false
}
,
-- =========================================================
-- TIER 19 - Advanced encabulation feedstocks
-- =========================================================

{
    type = "recipe",
    name = "executive-marseline-resin",
    enabled = false,
    category = "tank-ammo-component",
    subgroup = "tank-ammo-components",
    icon = "__tanks_for_bob_fork__/graphics/icons/Executive Marseline Resin.png",
    icon_size = 128,
    energy_required = 24,
    ingredients =
    {
      {type = "item", name = "marseline-compound", amount = 2},
      {type = "item", name = "oscillated-lubricant", amount = 1},
      {type = "item", name = "amulite-flakes", amount = 1},
    },
    results =
    {
        {type = "item", name = "executive-marseline-resin", amount = 2},
        {type = "item", name = "tank-ammo-Industrialwaste", amount = 1},
        {type = "item", name = "tank-ammo-Radioactivewaste", amount = 1, probability = 0.02},
    },
  }
,

{
    type = "recipe",
    name = "encabuloy-alloy",
    enabled = false,
    category = "crafting",
    subgroup = "tank-ammo-components",
    icon = "__tanks_for_bob_fork__/graphics/icons/encabuloy alloy.png",
    icon_size = 128,
    energy_required = 22,
    ingredients =
    {
      {type = "item", name = "iron-plate", amount = 2},
      {type = "item", name = "copper-plate", amount = 2},
      {type = "item", name = "hydrocoptic-crystal", amount = 1},
      {type = "item", name = "bioceramic-grit", amount = 1},
    },
    results =
    {
        {type = "item", name = "encabuloy-alloy", amount = 2},
        {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.12},
        {type = "item", name = "tank-ammo-Radioactivewaste", amount = 1, probability = 0.02},
    },
  }
,

{
    type = "recipe",
    name = "hyperphase-matrix",
    enabled = false,
    category = "tank-ammo-component",
    subgroup = "tank-ammo-components",
    icon = "__tanks_for_bob_fork__/graphics/icons/Hyperphase matrix.png",
    icon_size = 128,
    energy_required = 30,
    ingredients =
    {
      {type = "item", name = "phase-reactive-granules", amount = 2},
      {type = "item", name = "dielectric-chowder", amount = 1},
      {type = "item", name = "advanced-circuit", amount = 1},
    },
    results =
    {
        {type = "item", name = "hyperphase-matrix", amount = 1},
        {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.13},
        {type = "item", name = "tank-ammo-Radioactivewaste", amount = 1, probability = 0.03},
    },
  }
,

{
    type = "recipe",
    name = "retrograde-polymer-sheet",
    enabled = false,
    category = "crafting",
    subgroup = "tank-ammo-components",
    icon = "__tanks_for_bob_fork__/graphics/icons/Retrograde polymer sheet.png",
    icon_size = 128,
    energy_required = 20,
    ingredients =
    {
      {type = "item", name = "viscoelastic-froth", amount = 2},
      {type = "item", name = "executive-marseline-resin", amount = 1},
      {type = "item", name = "plastic-bar", amount = 1},
    },
    results =
    {
        {type = "item", name = "retrograde-polymer-sheet", amount = 2},
        {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.12},
    },
  }
,

{
    type = "recipe",
    name = "duplexed-substrate",
    enabled = false,
    category = "tank-ammo-component",
    subgroup = "tank-ammo-components",
    icon = "__tanks_for_bob_fork__/graphics/icons/Duplexed substrate.png",
    icon_size = 128,
    energy_required = 28,
    ingredients =
    {
      {type = "item", name = "retrograde-polymer-sheet", amount = 1},
      {type = "item", name = "hyperphase-matrix", amount = 1},
      {type = "item", name = "processing-unit", amount = 1},
    },
    results =
    {
        {type = "item", name = "duplexed-substrate", amount = 1},
        {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.13},
        {type = "item", name = "tank-ammo-Radioactivewaste", amount = 1, probability = 0.03},
    },
  }
,


-- =========================================================
-- TIER 20 - Encabulator support components
-- These are no longer free-floating enabled recipes. They are
-- unlocked by encabulator-support-componentry so the device-family
-- ladder has a clean material-to-device handoff.
-- =========================================================

{
    type = "recipe",
    name = "Hydrocoptic-marselvanes",
    enabled = false,
    category = "tank-ammo-component",
    subgroup = "tank-ammo-components",
    icon = "__tanks_for_bob_fork__/graphics/icons/Hydrocoptic-marselvanes.png",
    icon_size = 64,
    energy_required = 16.5,
    ingredients =
    {
      {type = "item", name = "hydrocoptic-crystal", amount = 1},
      {type = "item", name = "stabilized-brine-gel", amount = 1},
      {type = "item", name = "copper-plate", amount = 1},
    },
    results =
    {
        {type = "item", name = "Hydrocoptic-marselvanes", amount = 2},
        {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.13},
        {type = "item", name = "tank-ammo-Radioactivewaste", amount = 1, probability = 0.03},
    },
  }
,

{
    type = "recipe",
    name = "PhaseDetractor",
    enabled = false,
    category = "tank-ammo-component",
    subgroup = "tank-ammo-components",
    icon = "__tanks_for_bob_fork__/graphics/icons/PhaseDetractor.png",
    icon_size = 64,
    energy_required = 18.5,
    ingredients =
    {
      {type = "item", name = "dielectric-chowder", amount = 1},
      {type = "item", name = "iron-gear-wheel", amount = 2},
      {type = "item", name = "copper-cable", amount = 2},
    },
    results =
    {
        {type = "item", name = "PhaseDetractor", amount = 1},
        {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.14},
        {type = "item", name = "tank-ammo-Radioactivewaste", amount = 1, probability = 0.04},
    },
  }
,

{
    type = "recipe",
    name = "Cradinal-grametter",
    enabled = false,
    category = "tank-ammo-component",
    subgroup = "tank-ammo-components",
    icon = "__tanks_for_bob_fork__/graphics/icons/Cradinal-grametter.png",
    icon_size = 64,
    energy_required = 28.5,
    ingredients =
    {
      {type = "item", name = "marseline-compound", amount = 1},
      {type = "item", name = "phase-reactive-granules", amount = 1},
      {type = "item", name = "Hydrocoptic-marselvanes", amount = 1},
      {type = "item", name = "iron-plate", amount = 1},
    },
    results =
    {
        {type = "item", name = "Cradinal-grametter", amount = 2},
        {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.14},
        {type = "item", name = "tank-ammo-Radioactivewaste", amount = 1, probability = 0.04},
    },
  }
,

{
    type = "recipe",
    name = "Alumatedplate",
    enabled = false,
    category = "tank-ammo-component",
    subgroup = "tank-ammo-components",
    icon = "__tanks_for_bob_fork__/graphics/icons/Alumatedplate.png",
    icon_size = 64,
    energy_required = 12.5,
    ingredients =
    {
      {type = "item", name = "iron-plate", amount = 1},
      {type = "item", name = "encabuloy-alloy", amount = 1},
      {type = "item", name = "executive-marseline-resin", amount = 1},
    },
    results =
    {
        {type = "item", name = "Alumatedplate", amount = 2},
        {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.12},
    },
  }
,


-- =========================================================
-- TIER 21 - Encabulator and Sperving Arm device-family progression
-- Each major device level now has a real recipe that corresponds
-- to a matching research technology node.
-- =========================================================

{
    type = "recipe",
    name = "Retro-Encabulator",
    enabled = false,
    category = "tank-ammo-component",
    subgroup = "tank-ammo-components",
    icon = "__tanks_for_bob_fork__/graphics/icons/Retro-Encabulator.png",
    icon_size = 64,
    energy_required = 24.5,
    ingredients =
    {
      {type = "item", name = "PhaseDetractor", amount = 1},
      {type = "item", name = "Hydrocoptic-marselvanes", amount = 1},
      {type = "item", name = "retrograde-polymer-sheet", amount = 1},
      {type = "item", name = "marseline-compound", amount = 1},
    },
    results =
    {
        {type = "item", name = "Retro-Encabulator", amount = 1},
        {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.13},
        {type = "item", name = "tank-ammo-Radioactivewaste", amount = 1, probability = 0.03},
    },
  }
,

{
    type = "recipe",
    name = "Encabulator",
    enabled = false,
    category = "tank-ammo-component",
    subgroup = "tank-ammo-components",
    icon = "__tanks_for_bob_fork__/graphics/icons/Encabulator.png",
    icon_size = 64,
    energy_required = 20.5,
    ingredients =
    {
      {type = "item", name = "Retro-Encabulator", amount = 1},
      {type = "item", name = "executive-marseline-resin", amount = 1},
      {type = "item", name = "encabuloy-alloy", amount = 1},
      {type = "item", name = "phase-reactive-granules", amount = 1},
    },
    results =
    {
        {type = "item", name = "Encabulator", amount = 1},
        {type = "item", name = "tank-ammo-Industrialwaste", amount = 5},
        {type = "item", name = "tank-ammo-Radioactivewaste", amount = 1, probability = 0.04},
    },
  }
,

{
    type = "recipe",
    name = "SpervingArm",
    enabled = false,
    category = "tank-ammo-component",
    subgroup = "tank-ammo-components",
    icon = "__tanks_for_bob_fork__/graphics/icons/SpervingArm.png",
    icon_size = 64,
    energy_required = 28.5,
    ingredients =
    {
      {type = "item", name = "PhaseDetractor", amount = 1},
      {type = "item", name = "Hydrocoptic-marselvanes", amount = 2},
      {type = "item", name = "Alumatedplate", amount = 1},
      {type = "item", name = "oscillated-lubricant", amount = 1},
    },
    results =
    {
        {type = "item", name = "SpervingArm", amount = 1},
        {type = "item", name = "tank-ammo-Industrialwaste", amount = 4},
        {type = "item", name = "tank-ammo-Radioactivewaste", amount = 1, probability = 0.02},
    },
  }
,

{
    type = "recipe",
    name = "DuctedSpervingArm",
    enabled = false,
    category = "tank-ammo-component",
    subgroup = "tank-ammo-components",
    icon = "__tanks_for_bob_fork__/graphics/icons/DuctedSpervingArm.png",
    icon_size = 64,
    energy_required = 44.5,
    ingredients =
    {
      {type = "item", name = "SpervingArm", amount = 2},
      {type = "item", name = "Encabulator", amount = 1},
      {type = "item", name = "pre-turbulated-emulsion", amount = 1},
      {type = "item", name = "Cradinal-grametter", amount = 1},
    },
    results =
    {
        {type = "item", name = "DuctedSpervingArm", amount = 1},
        {type = "item", name = "tank-ammo-Industrialwaste", amount = 10},
        {type = "item", name = "tank-ammo-Radioactivewaste", amount = 1, probability = 0.03},
    },
  }
,

{
    type = "recipe",
    name = "TurboEncabulator",
    enabled = false,
    category = "tank-ammo-component",
    subgroup = "tank-ammo-components",
    icon = "__tanks_for_bob_fork__/graphics/icons/TurboEncabulator.png",
    icon_size = 64,
    energy_required = 28.5,
    ingredients =
    {
      {type = "item", name = "Encabulator", amount = 1},
      {type = "item", name = "pre-turbulated-emulsion", amount = 2},
      {type = "item", name = "oscillated-lubricant", amount = 1},
      {type = "item", name = "amulite-flakes", amount = 2},
    },
    results =
    {
        {type = "item", name = "TurboEncabulator", amount = 1},
        {type = "item", name = "tank-ammo-Industrialwaste", amount = 8},
        {type = "item", name = "tank-ammo-Radioactivewaste", amount = 1, probability = 0.04},
    },
  }
,

{
    type = "recipe",
    name = "HyperEncabulator",
    enabled = false,
    category = "tank-ammo-component",
    subgroup = "tank-ammo-components",
    icon = "__tanks_for_bob_fork__/graphics/icons/HyperEncabulator.png",
    icon_size = 64,
    energy_required = 36.5,
    ingredients =
    {
      {type = "item", name = "TurboEncabulator", amount = 1},
      {type = "item", name = "duplexed-substrate", amount = 4},
      {type = "item", name = "encabuloy-alloy", amount = 2},
      {type = "item", name = "Alumatedplate", amount = 2},
    },
    results =
    {
        {type = "item", name = "HyperEncabulator", amount = 1},
        {type = "item", name = "tank-ammo-Industrialwaste", amount = 10},
        {type = "item", name = "tank-ammo-Radioactivewaste", amount = 1, probability = 0.05},
    },
  }
,

{
    type = "recipe",
    name = "DuplexedSpervingArm",
    enabled = false,
    category = "tank-ammo-component",
    subgroup = "tank-ammo-components",
    icon = "__tanks_for_bob_fork__/graphics/icons/DuplexedSpervingArm.png",
    icon_size = 64,
    energy_required = 52.5,
    ingredients =
    {
      {type = "item", name = "DuctedSpervingArm", amount = 2},
      {type = "item", name = "duplexed-substrate", amount = 1},
      {type = "item", name = "hyperphase-matrix", amount = 1},
      {type = "item", name = "Cradinal-grametter", amount = 2},
    },
    results =
    {
        {type = "item", name = "DuplexedSpervingArm", amount = 1},
        {type = "item", name = "tank-ammo-Radioactivewaste", amount = 1},
        {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.14},
    },
  }
,

{
    type = "recipe",
    name = "FramulatedEncabulator",
    enabled = false,
    category = "tank-ammo-component",
    subgroup = "tank-ammo-components",
    icon = "__tanks_for_bob_fork__/graphics/icons/FramulatedEncabulator.png",
    icon_size = 64,
    energy_required = 48.5,
    ingredients =
    {
      {type = "item", name = "HyperEncabulator", amount = 1},
      {type = "item", name = "executive-marseline-resin", amount = 2},
      {type = "item", name = "Alumatedplate", amount = 5},
      {type = "item", name = "Cradinal-grametter", amount = 2},
    },
    results =
    {
        {type = "item", name = "FramulatedEncabulator", amount = 1},
        {type = "item", name = "tank-ammo-Radioactivewaste", amount = 1},
        {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.14},
    },
  }
,


-- =========================================================
-- TIER 22 - Tank assembly and vehicle infrastructure
-- =========================================================

{
    type = "recipe",
    name = "tank-ammo-assembling-machine",
    enabled = false,
     category = "tank-ammo-component",
      subgroup = "tank-ammo-infantry",
    ingredients =
    {
      {type = "item", name = "Alumatedplate", amount = 1},
      {type = "item", name = "Cradinal-grametter", amount = 3},
      {type = "item", name = "Encabulator", amount = 1},
      {type = "item", name = "Hydrocoptic-marselvanes", amount = 10}
    },
    results =
    {
        {type = "item", name = "tank-ammo-assembling-machine", amount = 1},
        {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.10},
    }
}
,

{
    type = "recipe",
    name = "tank-assembling-machine",
    enabled = false,
     category = "tank-ammo-component",
      subgroup = "tank-ammo-infantry",
    ingredients =
    {
      {type = "item", name = "Alumatedplate", amount = 1},
      {type = "item", name = "Cradinal-grametter", amount = 3},
      {type = "item", name = "Encabulator", amount = 1},
      {type = "item", name = "tank-ammo-assembling-machine", amount = 1}
    },
    results =
    {
        {type = "item", name = "tank-assembling-machine", amount = 1},
        {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.10},
    }
}
,

{
    type = "recipe",
    name = "tank-light-chasis-wlsk",
    enabled = false,
     category = "tank-crafting",
      subgroup = "tank-ammo-components",
    ingredients =
    {
      {type = "item", name = "TurboEncabulator", amount = 5},
      {type = "item", name = "Alumatedplate", amount = 6},
      {type = "item", name = "processing-unit", amount = 5},
      {type = "item", name = "electric-engine-unit", amount = 10}
    },
    results =
    {
        {type = "item", name = "tank-light-chasis-wlsk", amount = 1},
        {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.12},
    }
}
,


-- =========================================================
-- TIER 23 - Explosives, casing, and industrial byproduct chains
-- =========================================================

{
    type = "recipe",
    name = "tank-ammo-universal-explosive",
    enabled = false,
    category = "tank-ammo-component",
    subgroup = "tank-ammo-infantry",
    energy_required = 0.5,
    icon = "__tanks_for_bob_fork__/graphics/icons/universal-explosive.png",
    icon_size = 64,
    emissions_multiplier = 3,
    ingredients =
    {
      {type = "item", name = "Alumatedplate", amount = 1},
      {type = "item", name = "explosives", amount = 1}
    },
    results =
    {
      {type = "item", name = "tank-ammo-universal-explosive", amount = 5},
      {type = "item", name = "tank-ammo-Industrialwaste", amount = 5},
    },
  }
,

{
    type = "recipe",
    name = "tank-ammo-universal-explosive-synthetic",
    enabled = false,
    category = "tank-ammo-component",
    subgroup = "tank-ammo-infantry",
    energy_required = 30,
    icon = "__tanks_for_bob_fork__/graphics/icons/universal-explosive.png",
    icon_size = 64,
    emissions_multiplier = 3,
    ingredients =
    {
      {type = "item", name = "wood", amount = 100},
      {type = "item", name = "stone", amount = 100}
    },
    results =
    {
        {type = "item", name = "tank-ammo-universal-explosive", amount = 20},
        {type = "item", name = "tank-ammo-Industrialwaste", amount = 20},
        {type = "item", name = "tank-ammo-Radioactivewaste", amount = 1, probability = 0.02},
    },
  }
,

{
    type = "recipe",
    name = "tank-ammo-explosive-synthetic",
    enabled = false,
    category = "tank-ammo-component",
    subgroup = "tank-ammo-infantry",
    energy_required = 10,
    emissions_multiplier = 3,
    icon = "__base__/graphics/icons/explosives.png",
    icon_size = 64,
    ingredients =
    {
      {type = "item", name = "tank-ammo-universal-explosive", amount = 1},
      {type = "item", name = "wood", amount = 10}
    },
    results =
    {
        {type = "item", name = "explosives", amount = 3},
        {type = "item", name = "tank-ammo-Industrialwaste", amount = 5},
        {type = "item", name = "tank-ammo-Radioactivewaste", amount = 1, probability = 0.03},
    },
  }
,

{
    type = "recipe",
    name = "tank-ammo-industrial-coke",
    enabled = false,
    category = "tank-ammo-component",
    subgroup = "Seablock",
    icon = "__base__/graphics/icons/coal.png",
    icon_size = 64,
    energy_required = 150,
    emissions_multiplier = 3,
    ingredients =
    {
      {type = "item", name = "tank-ammo-universal-explosive", amount = 10},
      {type = "item", name = "wood", amount = 40}
    },
    results =
    {
      {type = "item", name = "coal", amount = 50},
      {type = "fluid", name = "crude-oil", amount = 100},
      {type = "item", name = "tank-ammo-Industrialwaste", amount = 20},
    },
  }
,

{
    type = "recipe",
    name = "tank-ammo-Explosive-Engineering",
    enabled = false,
    category = "tank-ammo-component",
    subgroup = "Seablock",
    icon = "__base__/graphics/icons/stone.png",
    icon_size = 64,
    energy_required = 150,
    ingredients =
    {
      {type = "item", name = "tank-ammo-universal-explosive", amount = 1},
      {type = "item", name = "wood", amount = 10}
    },
    results =
    {
      {type = "item", name = "stone", amount = 50},
      {type = "item", name = "fish-oil-residue", amount = 1},
      {type = "item", name = "tank-ammo-Industrialwaste", amount = 20},
    },
  }
,

{
    type = "recipe",
    name = "Rubberized-timber",
    enabled = false,
    category = "tank-ammo-component",
    subgroup = "Seablock",
    icon = "__base__/graphics/icons/wood.png",
    icon_size = 64,
    energy_required = 60,
    ingredients =
    {
      {type = "item", name = "tank-ammo-universal-explosive", amount = 1},
      {type = "item", name = "wood", amount = 10},
      {type = "fluid", name = "crude-oil", amount = 10},
    },
    results =
    {
      {type = "item", name = "wood", amount = 40},
      {type = "item", name = "tank-ammo-Industrialwaste", amount = 10},
    },
  }
,

{
    type = "recipe",
    name = "tank-ammo-casing",
    enabled = false,
    category = "tank-ammo-component",
    energy_required = 0.5,
    ingredients =
    {
      {type = "item", name = "copper-plate", amount = 1},
    },
    results =
    {
        {type = "item", name = "tank-ammo-casing", amount = 2},
        {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.08},
    },
  }
,

{
    type = "recipe",
    name = "tank-ammo-reinforced-casing",
    enabled = false,
    category = "tank-ammo-component",
    icon_size = 64,
    energy_required = 2,
    ingredients =
    {
      {type = "item", name = "steel-plate", amount = 1},
    },
    results =
    {
        {type = "item", name = "tank-ammo-reinforced-casing", amount = 2},
        {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.10},
    },
  }
,

{
    type = "recipe",
    name = "land-mine-poison",
    enabled = false,
    category = "tank-ammo-component",
    energy_required = 5,
    ingredients =
    {
      {type = "item", name = "steel-plate", amount = 1},
      {type = "item", name = "explosives", amount = 2},
      {type = "item", name = "sulfur", amount = 1},
    },
    results =
    {
        {type = "item", name = "land-mine-poison", amount = 4},
        {type = "item", name = "tank-ammo-Industrialwaste", amount = 1, probability = 0.12},
        {type = "item", name = "tank-ammo-Radioactivewaste", amount = 1, probability = 0.02},
    }
}
,


})
