data:extend(
{
--Alumatedplate
  {
    type = "recipe",
    name = "Alumatedplate",
    enabled = false,
    category = "tank-ammo-component",
	    subgroup = "intermediate-product",
    energy_required = 40.5,
	    icon = "__tanks_for_bob_fork__/graphics/icons/Alumatedplate.png",
    icon_size = 64,
    ingredients =
    {
      {"iron-plate", 1},
      {"Encabulator", 1},
    },
    results =
    {
      {type = "item", name = "Alumatedplate", amount = 2},
    },
	},
-- Sperving arms
  {
    type = "recipe",
    name = "SpervingArm",
    enabled = false,
    category = "tank-ammo-component",
	    subgroup = "intermediate-product",
    energy_required = 40.5,
	    icon = "__tanks_for_bob_fork__/graphics/icons/SpervingArm.png",
    icon_size = 64,
    ingredients =
    {
      {"Encabulator", 2},
      {"Alumatedplate", 5},
    },
    results =
    {
      {type = "item", name = "SpervingArm", amount = 2},
	    {type = "item", name = "tank-ammo-Industrialwaste", amount = 1},
    },
  },
    {
    type = "recipe",
    name = "DuctedSpervingArm",
    enabled = false,
    category = "tank-ammo-component",
	    subgroup = "intermediate-product",
    energy_required = 40.5,
	    icon = "__tanks_for_bob_fork__/graphics/icons/DuctedSpervingArm.png",
    icon_size = 64,
    ingredients =
    {
      {"Encabulator", 1},
      {"SpervingArm", 5},
      {"engine-unit", 2},
    },
    results =
    {
      {type = "item", name = "DuctedSpervingArm", amount = 2},
	    {type = "item", name = "tank-ammo-Industrialwaste", amount = 1},
    },
  },
    {
    type = "recipe",
    name = "DuplexedSpervingArm",
    enabled = false,
    category = "tank-ammo-component",
	    subgroup = "intermediate-product",
    energy_required = 40.5,
	    icon = "__tanks_for_bob_fork__/graphics/icons/DuplexedSpervingArm.png",
    icon_size = 64,
    ingredients =
    {
      {"TurboEncabulator", 1},
      {"DuctedSpervingArm", 5},
    },
    results =
    {
      {type = "item", name = "DuplexedSpervingArm", amount = 2},
	    {type = "item", name = "tank-ammo-Industrialwaste", amount = 1},
    },
  },
-- encabulators
  {
    type = "recipe",
    name = "Encabulator",
    enabled = false,
    category = "tank-ammo-component",
	    subgroup = "intermediate-product",
    energy_required = 0.5,
	    icon = "__tanks_for_bob_fork__/graphics/icons/Encabulator.png",
    icon_size = 64,
    ingredients =
    {
      {"copper-plate", 20},
      {"iron-gear-wheel", 5},
    },
    results =
    {
      {type = "item", name = "Encabulator", amount = 2},
	  {type = "item", name = "tank-ammo-Industrialwaste", amount = 1},
    },
  },
    {
    type = "recipe",
    name = "TurboEncabulator",
    enabled = false,
    category = "tank-ammo-component",
	    subgroup = "intermediate-product",
    energy_required = 0.5,
	    icon = "__tanks_for_bob_fork__/graphics/icons/TurboEncabulator.png",
    icon_size = 64,
    ingredients =
    {
      {"Encabulator", 1},
      {"iron-gear-wheel", 5},
    },
    results =
    {
      {type = "item", name = "TurboEncabulator", amount = 2},
	  {type = "item", name = "tank-ammo-Industrialwaste", amount = 1},
    },
  },
    {
    type = "recipe",
    name = "HyperEncabulator",
    enabled = false,
    category = "tank-ammo-component",
	    subgroup = "intermediate-product",
    energy_required = 0.5,
	    icon = "__tanks_for_bob_fork__/graphics/icons/HyperEncabulator.png",
    icon_size = 64,
    ingredients =
    {
      {"TurboEncabulator", 1},
      {"Alumatedplate", 5},
    },
    results =
    {
      {type = "item", name = "HyperEncabulator", amount = 2},
	  {type = "item", name = "tank-ammo-Industrialwaste", amount = 1},
    },
  },

    {
    type = "recipe",
    name = "FramulatedEncabulator",
    enabled = false,
    category = "tank-ammo-component",
	    subgroup = "intermediate-product",
    energy_required = 10.5,
	    icon = "__tanks_for_bob_fork__/graphics/icons/FramulatedEncabulator.png",
    icon_size = 64,
    ingredients =
    {
      {"HyperEncabulator", 10},
      {"Alumatedplate", 50}
    },
    results =
    {
      {type = "item", name = "FramulatedEncabulator", amount = 2}
    },
  },
  -- tank-assembling-machine
  {
    type = "recipe",
    name = "tank-assembling-machine",
    enabled = false,
    ingredients =
    {
      {"iron-plate", 1},
      {"electronic-circuit", 3},
      {"Alumatedplate", 5},
      {"assembling-machine-1", 1}
    },
    result = "tank-assembling-machine"
  },
  -- tank-ammo-assembling-machine
  {
    type = "recipe",
    name = "tank-ammo-assembling-machine",
    enabled = false,
    ingredients =
    {
      {"Alumatedplate", 1},
      {"electronic-circuit", 3},
      {"TurboEncabulator", 5},
      {"assembling-machine-1", 1}
    },
    result = "tank-ammo-assembling-machine"
  },
  -- tank-light-chassis-wlsk
  {
    type = "recipe",
    name = "tank-light-chasis-wlsk",
    enabled = false,
    category = "tank-crafting",
    ingredients =
    {
      {"TurboEncabulator", 5},
      {"Alumatedplate", 6},
      {"processing-unit", 5},
      {"electric-engine-unit", 10}
    },
    result = "tank-light-chasis-wlsk"
  },
  -- ammo components
  -- tank-ammo-universal-explosive
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
      {"Alumatedplate", 1},
      {"explosives", 1}
    },
    results =
    {
      {type = "item", name = "tank-ammo-universal-explosive", amount = 2},
      {type = "item", name = "tank-ammo-Industrialwaste", amount = 15},
    },
  },
  -- tank-ammo-universal-explosive-synthetic
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
      {"wood", 100},
      {"stone", 100}
    },
    results =
    {
      {type = "item", name = "tank-ammo-universal-explosive", amount = 9},
      {type = "item", name = "tank-ammo-Industrialwaste", amount = 5},
    },
  },
  -- tank-ammo-explosive-synthetic
  {
    type = "recipe",
    name = "tank-ammo-explosive-synthetic",
    enabled = false,
    category = "tank-ammo-component",
    subgroup = "tank-ammo-infantry",
    energy_required = 10,
    emissions_multiplier = 3,
    icon = "__tanks_for_bob_fork__/graphics/icons/universal-explosive.png",
    icon_size = 64,
    ingredients =
    {
      {"tank-ammo-universal-explosive", 1},
      {"wood", 10}
    },
    results =
    {
      {type = "item", name = "explosives", amount = 10},
      {type = "item", name = "tank-ammo-Industrialwaste", amount = 6},
    },
  },
  -- tank-ammo-industrial-coke
  {
    type = "recipe",
    name = "tank-ammo-industrial-coke",
    enabled = false,
    category = "tank-ammo-component",
    subgroup = "intermediate-product",
    icon = "__tanks_for_bob_fork__/graphics/icons/industrial-coke.png",
    icon_size = 64,
    energy_required = 150,
    emissions_multiplier = 3,
    ingredients =
    {
      {"tank-ammo-universal-explosive", 10},
      {"wood", 40}
    },
    results =
    {
      {type = "item", name = "coal", amount = 20},
      {type = "fluid", name = "crude-oil", amount = 20},
      {type = "item", name = "tank-ammo-Industrialwaste", amount = 10},
    },
  },
  -- tank-ammo-Reprocessing
  {
    type = "recipe",
    name = "tank-ammo-Reprocessing",
    enabled = false,
    category = "tank-ammo-component",
    subgroup = "intermediate-product",
    icon = "__tanks_for_bob_fork__/graphics/icons/Radioactivewaste.png",
    icon_size = 64,
    energy_required = 50,
    emissions_multiplier = 3,
    ingredients =
    {
      {"tank-ammo-Industrialwaste", 3},
      {"tank-ammo-Radioactivewaste", 3}
    },
    results =
    {
      {type = "item", name = "uranium-ore", amount = 1},
      {type = "item", name = "tank-ammo-Industrialwaste", amount = 1},
      {type = "item", name = "tank-ammo-Radioactivewaste", amount = 1},
    },
  },
  -- tank-ammo-Explosive Engineering
  {
    type = "recipe",
    name = "tank-ammo-Explosive Engineering",
    enabled = false,
    category = "tank-ammo-component",
    subgroup = "intermediate-product",
    icon = "__tanks_for_bob_fork__/graphics/icons/industrial-coke.png",
    icon_size = 64,
    energy_required = 150,
    ingredients =
    {
      {"tank-ammo-universal-explosive", 1},
      {"wood", 10}
    },
    results =
    {
      {type = "item", name = "stone", amount = 60},
      {type = "fluid", name = "water", amount = 90},
      {type = "item", name = "tank-ammo-Industrialwaste", amount = 13},
    },
  },
  -- Rubberized-timber
  {
    type = "recipe",
    name = "Rubberized-timber",
    enabled = false,
    category = "tank-ammo-component",
    subgroup = "intermediate-product",
    icon = "__tanks_for_bob_fork__/graphics/icons/Rubberized timber.png",
    icon_size = 64,
    energy_required = 60,
    ingredients =
    {
      {"tank-ammo-universal-explosive", 1},
      {"wood", 5},
      {type = "fluid", name = "crude-oil", amount = 20},
    },
    results =
    {
      {type = "item", name = "wood", amount = 20},
      {type = "item", name = "tank-ammo-Industrialwaste", amount = 4},
    },
  },
  -- tank-ammo-ecozone
  {
    type = "recipe",
    name = "tank-ammo-ecozone",
    enabled = false,
    category = "tank-ammo-component",
    subgroup = "tank-ammo-infantry",
    icon = "__tanks_for_bob_fork__/graphics/icons/Industrialwaste2.png",
    icon_size = 64,
    energy_required = 40,
    ingredients =
    {
      {"tank-ammo-Industrialwaste", 1},
      {"stone", 10}
    },
    results =
    {
      {type = "item", name = "stone", amount = 3},
      {type = "item", name = "iron-ore", amount = 3},
      {type = "item", name = "copper-ore", amount = 3},
    },
  },
  -- tank-ammo-casing
  {
    type = "recipe",
    name = "tank-ammo-casing",
    enabled = false,
    category = "tank-ammo-component",
    energy_required = 0.5,
    ingredients =
    {
      {"copper-plate", 1},
    },
    results =
    {
      {type = "item", name = "tank-ammo-casing", amount = 2},
    },
  },
  -- tank-ammo-reinforced-casing
  {
    type = "recipe",
    name = "tank-ammo-reinforced-casing",
    enabled = false,
    category = "tank-ammo-component",
    icon_size = 64,
    energy_required = 2,
    ingredients =
    {
      {"steel-plate", 1},
    },
    results =
    {
      {type = "item", name = "tank-ammo-reinforced-casing", amount = 2},
    },
  },
  -- ore-from-waste
  {
    type = "recipe",
    name = "ore-from-waste",
    enabled = false,
    category = "tank-ammo-component",
    subgroup = "intermediate-product",
    icon = "__tanks_for_bob_fork__/graphics/icons/Industrialwaste2.png",
    icon_size = 64,
    energy_required = 50,
    ingredients =
    {
      {type = "item", name = "SpervingArm", amount = 1},
      {type = "item", name = "tank-ammo-reinforced-casing", amount = 1},
      {type = "item", name = "tank-ammo-Industrialwaste", amount = 1}
    },
    results =
    {
      {type = "item", name = "iron-ore", amount = 4},
      {type = "item", name = "copper-ore", amount = 4}
    }
  },
  -- ore-from-wasteb
  {
    type = "recipe",
    name = "ore-from-wasteb",
    enabled = false,
    category = "tank-ammo-component",
    subgroup = "intermediate-product",
    icon = "__tanks_for_bob_fork__/graphics/icons/Industrialwaste2.png",
    icon_size = 64,
    energy_required = 60,
    ingredients =
    {
      {type = "item", name = "tank-ammo-reinforced-casing", amount = 2},
      {type = "item", name = "SpervingArm", amount = 1},
      {type = "item", name = "tank-ammo-Industrialwaste", amount = 4}
    },
    results =
    {
      {type = "item", name = "iron-ore", amount = 15},
      {type = "item", name = "copper-ore", amount = 15}
    }
  },
    -- ore-from-waster
  {
    type = "recipe",
    name = "ore-from-waster",
    enabled = false,
    category = "tank-ammo-component",
    subgroup = "intermediate-product",
    icon = "__tanks_for_bob_fork__/graphics/icons/Industrialwaste2.png",
    icon_size = 64,
    energy_required = 60,
    ingredients =
    {
      {type = "item", name = "tank-ammo-reinforced-casing", amount = 2},
      {type = "item", name = "tank-ammo-Industrialwaste", amount = 4},
      {type = "item", name = "DuctedSpervingArm", amount = 4}
    },
    results =
    {
      {type = "item", name = "uranium-ore", amount = 10},
      {type = "item", name = "copper-ore", amount = 10}
    }
  },
  -- extras
  {
    type = "recipe",
    name = "land-mine-poison",
    enabled = false,
    energy_required = 5,
    ingredients =
    {
      {"steel-plate", 1},
      {"explosives", 2},
      {"sulfur", 1},
    },
    result = "land-mine-poison",
    result_count = 4
  },
  {
    type = "recipe",
    name = "fish-kit",
    enabled = false,
    category = "tank-ammo-component",
    energy_required = 5,
    ingredients =
    {
      {"raw-fish", 5},
    },
    results =
    {
      {type = "item", name = "fish-kit", amount = 6},
    },
  }
})