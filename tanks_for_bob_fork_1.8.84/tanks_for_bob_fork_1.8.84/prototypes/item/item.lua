data:extend(
{

-- alumated plateing
  {
    type = "item",
    name = "Alumatedplate",
    icon = "__tanks_for_bob_fork__/graphics/icons/Alumatedplate.png",
    icon_size = 64,
    subgroup = "tank-ammo-components",
    order = "a[tank-ammo-components]-a[casing]",
    stack_size = 10,
	},
--Buildings/Components
  {
    type = "item",
    name = "tank-assembling-machine",
    icon = "__tanks_for_bob_fork__/graphics/icons/tank-assembling-machine.png",
    icon_size = 64,
    subgroup = "production-machine",
    order = "y[assembling-machine-2]",
    place_result = "tank-assembling-machine",
    stack_size = 10,
  },
  {
    type = "item",
    name = "tank-ammo-assembling-machine",
    icon = "__tanks_for_bob_fork__/graphics/icons/tank-ammo-assembling-machine.png",
    icon_size = 64,
    subgroup = "production-machine",
    order = "z[assembling-machine-2]",
    place_result = "tank-ammo-assembling-machine",
    stack_size = 10
  },
  {
    type = "item",
    name = "tank-light-chasis-wlsk",
    icon = "__tanks_for_bob_fork__/graphics/icons/tank-light-chasis-wlsk.png",
    icon_size = 64,
 
    subgroup = "tank-vehicle-upgrades",
	  order = "a[tank-vehicle-upgrades]-a[tank-light-chasis-wlsk]",
    stack_size = 1
  },
  -- SperveingArm
  {
    type = "module",
    name = "SpervingArm",
    icon = "__tanks_for_bob_fork__/graphics/icons/SpervingArm.png",
    icon_size = 64,
    subgroup = "module",
    category = "effectivity",
    tier = 1,
    order = "a[tank-ammo-components]-a[casing]",
    stack_size = 10,
	effect = { consumption = {bonus = -0.5}},
	},
	  {
    type = "module",
    name = "DuctedSpervingArm",
    icon = "__tanks_for_bob_fork__/graphics/icons/DuctedSpervingArm.png",
    icon_size = 64,
    subgroup = "module",
    category = "effectivity",
    tier = 2,
    order = "a[tank-ammo-components]-a[casing]",
    stack_size = 10,
	effect = { consumption = {bonus = -0.6}},
	},
	  {
    type = "module",
    name = "DuplexedSpervingArm",
    icon = "__tanks_for_bob_fork__/graphics/icons/DuplexedSpervingArm.png",
    icon_size = 64,
    subgroup = "module",
    category = "effectivity",
    tier = 3,
    order = "a[tank-ammo-components]-a[casing]",
    stack_size = 10,
	effect = { consumption = {bonus = -0.7}},
	},
-- encabulators
  {
    type = "item",
    name = "Encabulator",
    icon = "__tanks_for_bob_fork__/graphics/icons/Encabulator.png",
    icon_size = 64,
	    fuel_category = "chemical",
    fuel_value = "2MJ",

    subgroup = "tank-ammo-components",
    order = "a[tank-ammo-components]-a[casing]",
    stack_size = 10,
	effect = { consumption = {bonus = -0.5}},
	},
	  {
    type = "item",
    name = "TurboEncabulator",
    icon = "__tanks_for_bob_fork__/graphics/icons/TurboEncabulator.png",
    icon_size = 64,
	    fuel_category = "chemical",
    fuel_value = "4MJ",

    subgroup = "tank-ammo-components",
    order = "a[tank-ammo-components]-a[casing]",
    stack_size = 10,
	},
	  {
    type = "item",
    name = "HyperEncabulator",
    icon = "__tanks_for_bob_fork__/graphics/icons/HyperEncabulator.png",
    icon_size = 64,
	    fuel_category = "chemical",
    fuel_value = "10MJ",

    subgroup = "tank-ammo-components",
    order = "a[tank-ammo-components]-a[casing]",
    stack_size = 10,
	},
		  {
    type = "item",
    name = "FramulatedEncabulator",
    icon = "__tanks_for_bob_fork__/graphics/icons/FramulatedEncabulator.png",
    icon_size = 64,
	    fuel_category = "nuclear",
    fuel_value = "10MJ",

    subgroup = "tank-ammo-components",
    order = "a[tank-ammo-components]-a[casing]",
    stack_size = 10,
	},
--Tank Ammo Components
	{
    type = "item",
    name = "tank-ammo-casing",
    icon = "__tanks_for_bob_fork__/graphics/icons/casing.png",
    icon_size = 64,

    subgroup = "tank-ammo-components",
    order = "a[tank-ammo-components]-a[casing]",
    stack_size = 10
	},
  {
    type = "item",
    name = "tank-ammo-reinforced-casing",
    icon = "__tanks_for_bob_fork__/graphics/icons/reinforced-casing.png",
    icon_size = 64,

    subgroup = "tank-ammo-components",
    order = "a[tank-ammo-components]-a[reinforced-casing]",
    stack_size = 10
  },
	{
    type = "item",
    name = "tank-ammo-Industrialwaste",
    icon = "__tanks_for_bob_fork__/graphics/icons/Industrialwaste.png",
    icon_size = 64,
    subgroup = "tank-ammo-components",
    order = "a[tank-ammo-components]-b[Industrialwaste]",
	fuel_value = "1MJ",
    fuel_category = "chemical",
    subgroup = "raw-resource",
	fuel_acceleration_multiplier = 0.6,
    fuel_top_speed_multiplier = 0.65,
	fuel_emissions_multiplier = 3.7,
	fuel_glow_color = {94,28,13,1},
    stack_size = 50
	},
	{
    type = "item",
    name = "tank-ammo-Radioactivewaste",
    icon = "__tanks_for_bob_fork__/graphics/icons/Radioactivewaste.png",
	fuel_value = "1MJ",
    fuel_category = "chemical",
	fuel_acceleration_multiplier = 0.7,
    fuel_top_speed_multiplier = 0.75,
	fuel_emissions_multiplier = 4.9,
	fuel_glow_color = {64,160,38,1},
    subgroup = "raw-resource",
    icon_size = 64,

    subgroup = "tank-ammo-components",
    order = "a[tank-ammo-components]-b[Radioactivewaste]",
    stack_size = 10
	},
	{
    type = "item",
    name = "tank-ammo-universal-explosive",
    icon = "__tanks_for_bob_fork__/graphics/icons/universal-explosive.png",
    icon_size = 64,

    subgroup = "tank-ammo-components",
    order = "a[tank-ammo-components]-b[universal-explosive]",
    stack_size = 10
	},
    {
    type = "item",
    name = "land-mine-poison",
    icon = "__base__/graphics/icons/land-mine.png",
    icon_size = 64,
    damage_radius = 15,
    subgroup = "gun",
    order = "f[land-mine]",
    place_result = "land-mine-poison",
    stack_size = 20,
    trigger_radius = 2
  },
--fish-kit
  {
    type = "capsule",
    name = "fish-kit",
    icon = "__tanks_for_bob_fork__/graphics/icons/fish-kit.png",
    icon_size = 64,

    capsule_action =
    {
      type = "use-on-self",
      attack_parameters =
      {
        type = "projectile",
		    ammo_category = "capsule",
        cooldown = 10,
        range = 0,
        ammo_type =
        {
          category = "capsule",
          target_type = "position",
          action =
          {
            type = "direct",
            action_delivery =
            {
              type = "instant",
              target_effects = 
              {
                type = "damage",
                damage = {type = "physical", amount = -30}
              }
            }
          }
        }
      }
    },
    subgroup = "tank-ammo-infantry",
    order = "z[tank-ammo]",
    stack_size = 100
  },
}
)