data:extend(
{
-- new items
--done
  {
        type = "item",
        name = "campfire",
        icon = "__tanks_for_bob_fork__/graphics/icons/campfire.png",
        icon_size = 64,
        subgroup = "production-machine",
        order = "a[campfire]",
        place_result = "campfire",
        stack_size = 50
    },
    --done
    {
        type = "item",
        name = "beachpump",
        icon = "__tanks_for_bob_fork__/graphics/icons/beachpump.png",
        icon_size = 64,
        subgroup = "Seablock",
        order = "b[beachpump]",
        place_result = "beachpump",
        stack_size = 50
    },
    --done now  ish, need more info still places basic pipes.
  --  {
   --     type = "item",
   --     name = "wood-pipes",
   --     icon = "__tanks_for_bob_fork__/graphics/icons/wood-pipes.png",
   --     icon_size = 64,
   --     subgroup = "Seablock",
   --     order = "a[wood-pipes]",
   --     place_result = "pipe",
   --     stack_size = 100
   -- },
    --done
    {
        type = "item",
        name = "wood-basin",
        icon = "__tanks_for_bob_fork__/graphics/icons/wood-basin.png",
        icon_size = 64,
        subgroup = "Seablock",
        order = "c[wood-basin]",
        place_result = "wood-basin",
        stack_size = 50
    },
    --done
    {
        type = "item",
        name = "workbench",
        icon = "__tanks_for_bob_fork__/graphics/icons/workbench.png",
        icon_size = 64,
        subgroup = "production-machine",
        order = "d[workbench]",
        place_result = "workbench",
        stack_size = 10
    },
    --done
    {
        type = "item",
        name = "thinking-hut",
        icon = "__tanks_for_bob_fork__/graphics/icons/thinking-hut.png",
        icon_size = 64,
        subgroup = "production-machine",
        order = "e[thinking-hut]",
        place_result = "thinking-hut",
        stack_size = 10
    },
    --done?
    {
        type = "item",
        name = "clay-pit",
        icon = "__tanks_for_bob_fork__/graphics/icons/clay-pit.png",
        icon_size = 64,
        subgroup = "Seablock",
        order = "f[clay-pit]",
        place_result = "clay-pit",
        stack_size = 50
    },
    --done?
    {
        type = "item",
        name = "pit-kiln",
        icon = "__tanks_for_bob_fork__/graphics/icons/pit-kiln.png",
        icon_size = 64,
        subgroup = "Seablock",
        order = "g[pit-kiln]",
        place_result = "pit-kiln",
        stack_size = 50
    },
    --done?
    {
        type = "item",
        name = "growing-plot",
        icon = "__tanks_for_bob_fork__/graphics/icons/growing-plot.png",
        icon_size = 64,
        subgroup = "Seablock",
        order = "h[growing-plot]",
        place_result = "growing-plot",
        stack_size = 50
    },
    {
        type = "tool",
        name = "Seared-fish",
        icon = "__tanks_for_bob_fork__/graphics/icons/Seared-fish.png",
        icon_size = 64,
subgroup = "science-pack",
        order = "i[Seared-fish]",
        stack_size = 100,
            durability = 1,
    durability_description_key = "description.science-pack-remaining-amount-key",
    durability_description_value = "description.science-pack-remaining-amount-value"
    },
    {
        type = "item",
        name = "clay",
        icon = "__tanks_for_bob_fork__/graphics/icons/clay.png",
        icon_size = 64,
        subgroup = "Seablock",
        order = "a[clay]",
        stack_size = 100
    },
    {
        type = "item",
        name = "brick",
        icon = "__tanks_for_bob_fork__/graphics/icons/brick.png",
        icon_size = 64,
        subgroup = "Seablock",
        order = "b[brick]",
        stack_size = 100
    },
    {
        type = "item",
        name = "crude-glass",
        icon = "__tanks_for_bob_fork__/graphics/icons/crude-glass.png",
        icon_size = 64,
        subgroup = "Seablock",
        order = "j[crude-glass]",
        stack_size = 100
    },
    {
        type = "gun",
        name = "wood-spear",
        icon = "__tanks_for_bob_fork__/graphics/icons/wood-spear.png",
        icon_size = 64,
        subgroup = "Seablock",
        order = "a[wood-spear]",
        attack_parameters =
    {
      type = "projectile",
      ammo_category = "wood",
      cooldown = 15,
      movement_slow_down_factor = 0.0,
      shell_particle =
      {
        name = "shell-particle",
        direction_deviation = 0.1,
        speed = 0.1,
        speed_deviation = 0.03,
        center = {0, 0.1},
        creation_distance = -0.5,
        starting_frame_speed = 0.4,
        starting_frame_speed_deviation = 0.1
      },
      projectile_creation_distance = 1.125,
      range = 20,
    },
        stack_size = 10
    },

  -- spearammo
{
  type = "ammo",
  name = "Sharp-stick",
  icon = "__tanks_for_bob_fork__/graphics/icons/wood-spear-a.png",
  icon_size = 64,
  icon_mipmaps = 4,

  ammo_category = "wood",

  ammo_type =
  {
    action =
    {
      type = "direct",
      action_delivery =
      {
        type = "instant",
        source_effects =
        {
          {
            type = "create-explosion",
            entity_name = "explosion-gunshot"
          }
        },
        target_effects =
        {
          {
            type = "create-entity",
            entity_name = "explosion-hit",
            offsets = {{0, 1}},
            offset_deviation = {{-0.5, -0.5}, {0.5, 0.5}}
          },
          {
            type = "damage",
            damage = {amount = 5, type = "physical"}
          }
        }
      }
    }
  },

  magazine_size = 55,
  subgroup = "ammo",
  order = "a[basic-clips]-a[firearm-magazine]",
  stack_size = 200
},
    {
        type = "item",
        name = "cooking-fire",
        icon = "__tanks_for_bob_fork__/graphics/icons/cooking-fire.png",
        icon_size = 64,
        subgroup = "Seablock",
        order = "k[cooking-fire]",
        place_result = "cooking-fire",
        stack_size = 10
    },
    {
        type = "item",
        name = "stone-water-wheel",
        icon = "__tanks_for_bob_fork__/graphics/icons/stone-water-wheel.png",
        icon_size = 64,
        subgroup = "Seablock",
        order = "l[stone-water-wheel]",
        place_result = "stone-water-wheel",
        stack_size = 10
    },
    --done
    {
        type = "item",
        name = "pondering-hovel",
        icon = "__tanks_for_bob_fork__/graphics/icons/pondering-hovel.png",
        icon_size = 64,
        subgroup = "Seablock",
        order = "p[pondering-hovel]",
        place_result = "pondering-hovel",
        stack_size = 10
    },
    {
        type = "item",
        name = "quarry",
        icon = "__tanks_for_bob_fork__/graphics/icons/quarry.png",
        icon_size = 64,
        subgroup = "Seablock",
        order = "q[quarry]",
        place_result = "quarry",
        stack_size = 50
    },
    --done
    {
        type = "item",
        name = "solar-boiler",
        icon = "__tanks_for_bob_fork__/graphics/icons/solar-boiler.png",
        icon_size = 64,
        subgroup = "Seablock",
        order = "r[solar-boiler]",
        place_result = "solar-boiler",
        stack_size = 10
    },
    --done
    {
        type = "item",
        name = "fish-pond",
        icon = "__tanks_for_bob_fork__/graphics/icons/fish-pond.png",
        icon_size = 64,
        subgroup = "Seablock",
        order = "s[fish-pond]",
        place_result = "fish-pond",
        stack_size = 10
    },
    {
        type = "tool",
        name = "meal",
        icon = "__tanks_for_bob_fork__/graphics/icons/meal.png",
        icon_size = 64,
subgroup = "science-pack",
        order = "t[meal]",
        stack_size = 100,
            durability = 1,
    durability_description_key = "description.science-pack-remaining-amount-key",
    durability_description_value = "description.science-pack-remaining-amount-value"
    },
    {
        type = "item",
        name = "stone-tools",
        icon = "__tanks_for_bob_fork__/graphics/icons/stone-tools.png",
        icon_size = 64,
        subgroup = "Seablock",
        order = "u[stone-tools]",
        stack_size = 50
    },
    --done
    {
        type = "item",
        name = "primitive-steam-powered-pump",
        icon = "__tanks_for_bob_fork__/graphics/icons/primitive-steam-powered-pump.png",
        icon_size = 64,
        subgroup = "Seablock",
        order = "v[primitive-steam-powered-pump]",
        place_result = "primitive-steam-powered-pump",
        stack_size = 10
    },
    --done
    {
        type = "item",
        name = "steam-condenser",
        icon = "__tanks_for_bob_fork__/graphics/icons/steam-condenser.png",
        icon_size = 64,
        subgroup = "Seablock",
        order = "w[steam-condenser]",
        place_result = "steam-condenser",
        stack_size = 10
    },
    --
    {
        type = "item",
        name = "calcifier",
        icon = "__tanks_for_bob_fork__/graphics/icons/calcifier.png",
        icon_size = 64,
        subgroup = "Seablock",
        order = "x[calcifier]",
        place_result = "calcifier",
        stack_size = 10
    },
    {
        type = "item",
        name = "shaler",
        icon = "__tanks_for_bob_fork__/graphics/icons/shaler.png",
        icon_size = 64,
        subgroup = "Seablock",
        order = "y[shaler]",
        place_result = "shaler",
        stack_size = 50
    },
     {
        type = "item",
        name = "Steam-Compressor",
        icon = "__tanks_for_bob_fork__/graphics/icons/Steam-Compressor.png",
        icon_size = 64,
        subgroup = "Seablock",
        order = "y[shaler]",
        place_result = "Steam-Compressor",
        stack_size = 50
    },


-- Corporate Compliance item subgroup and paperwork chain
-- These are the administrative feedstocks and approval artifacts for the corporate compliance technology parasite layer.
  {
    type = "item-subgroup",
    name = "corporate-compliance",
    group = "intermediate-products",
    order = "z-corporate"
  },

-- Corporate Compliance: paper base
  {
    type = "item",
    name = "charcoal",
    icon = "__tanks_for_bob_fork__/graphics/icons/placeholder.png",
    icon_size = 64,
    subgroup = "corporate-compliance",
    order = "a[paper-base]-a[charcoal]",
    stack_size = 100,
    fuel_category = "chemical",
    fuel_value = "1MJ",
    fuel_emissions_multiplier = 1.5
  },
  {
    type = "item",
    name = "wood-pulp",
    icon = "__tanks_for_bob_fork__/graphics/icons/placeholder.png",
    icon_size = 64,
    subgroup = "corporate-compliance",
    order = "a[paper-base]-b[wood-pulp]",
    stack_size = 100
  },
  {
    type = "item",
    name = "crude-paper",
    icon = "__tanks_for_bob_fork__/graphics/icons/placeholder.png",
    icon_size = 64,
    subgroup = "corporate-compliance",
    order = "a[paper-base]-c[crude-paper]",
    stack_size = 100
  },
  {
    type = "tool",
    name = "requisition-slip",
    icon = "__tanks_for_bob_fork__/graphics/icons/placeholder.png",
    icon_size = 64,
    subgroup = "corporate-compliance",
    order = "a[paper-base]-d[requisition-slip]",
    stack_size = 100,
    durability = 1,
    durability_description_key = "description.science-pack-remaining-amount-key",
    durability_description_value = "description.science-pack-remaining-amount-value"
  },

-- Corporate Compliance: clerical binding supplies
  {
    type = "item",
    name = "staples",
    icon = "__tanks_for_bob_fork__/graphics/icons/placeholder.png",
    icon_size = 64,
    subgroup = "corporate-compliance",
    order = "b[clerical-supplies]-a[staples]",
    stack_size = 200
  },
  {
    type = "item",
    name = "ink",
    icon = "__tanks_for_bob_fork__/graphics/icons/placeholder.png",
    icon_size = 64,
    subgroup = "corporate-compliance",
    order = "b[clerical-supplies]-b[ink]",
    stack_size = 100
  },
  {
    type = "item",
    name = "stamps",
    icon = "__tanks_for_bob_fork__/graphics/icons/placeholder.png",
    icon_size = 64,
    subgroup = "corporate-compliance",
    order = "b[clerical-supplies]-c[stamps]",
    stack_size = 100
  },
  {
    type = "item",
    name = "folder",
    icon = "__tanks_for_bob_fork__/graphics/icons/placeholder.png",
    icon_size = 64,
    subgroup = "corporate-compliance",
    order = "b[clerical-supplies]-d[folder]",
    stack_size = 100
  },
  {
    type = "item",
    name = "clipboard",
    icon = "__tanks_for_bob_fork__/graphics/icons/placeholder.png",
    icon_size = 64,
    subgroup = "corporate-compliance",
    order = "b[clerical-supplies]-e[clipboard]",
    stack_size = 50
  },

-- Corporate Compliance: work order escalation
  {
    type = "tool",
    name = "work-order-slip",
    icon = "__tanks_for_bob_fork__/graphics/icons/placeholder.png",
    icon_size = 64,
    subgroup = "corporate-compliance",
    order = "c[work-order-escalation]-a[work-order-slip]",
    stack_size = 100,
    durability = 1,
    durability_description_key = "description.science-pack-remaining-amount-key",
    durability_description_value = "description.science-pack-remaining-amount-value"
  },
  {
    type = "tool",
    name = "certified-work-order",
    icon = "__tanks_for_bob_fork__/graphics/icons/placeholder.png",
    icon_size = 64,
    subgroup = "corporate-compliance",
    order = "c[work-order-escalation]-b[certified-work-order]",
    stack_size = 100,
    durability = 1,
    durability_description_key = "description.science-pack-remaining-amount-key",
    durability_description_value = "description.science-pack-remaining-amount-value"
  },
  {
    type = "tool",
    name = "submitted-evaluation",
    icon = "__tanks_for_bob_fork__/graphics/icons/placeholder.png",
    icon_size = 64,
    subgroup = "corporate-compliance",
    order = "c[work-order-escalation]-c[submitted-evaluation]",
    stack_size = 100,
    durability = 1,
    durability_description_key = "description.science-pack-remaining-amount-key",
    durability_description_value = "description.science-pack-remaining-amount-value"
  },
  {
    type = "tool",
    name = "risk-assessment",
    icon = "__tanks_for_bob_fork__/graphics/icons/placeholder.png",
    icon_size = 64,
    subgroup = "corporate-compliance",
    order = "c[work-order-escalation]-d[risk-assessment]",
    stack_size = 100,
    durability = 1,
    durability_description_key = "description.science-pack-remaining-amount-key",
    durability_description_value = "description.science-pack-remaining-amount-value"
  },
  {
    type = "tool",
    name = "risk-assessed-work-order",
    icon = "__tanks_for_bob_fork__/graphics/icons/placeholder.png",
    icon_size = 64,
    subgroup = "corporate-compliance",
    order = "c[work-order-escalation]-e[risk-assessed-work-order]",
    stack_size = 100,
    durability = 1,
    durability_description_key = "description.science-pack-remaining-amount-key",
    durability_description_value = "description.science-pack-remaining-amount-value"
  },
  {
    type = "item",
    name = "corporate-waste",
    icon = "__tanks_for_bob_fork__/graphics/icons/placeholder.png",
    icon_size = 64,
    subgroup = "corporate-compliance",
    order = "c[work-order-escalation]-z[corporate-waste]",
    stack_size = 200,
    fuel_category = "chemical",
    fuel_value = "500kJ",
    fuel_emissions_multiplier = 10
  },

-- Corporate Compliance: advanced validation artifacts
  {
    type = "tool",
    name = "compliance-packet",
    icon = "__tanks_for_bob_fork__/graphics/icons/placeholder.png",
    icon_size = 64,
    subgroup = "corporate-compliance",
    order = "d[advanced-validation]-a[compliance-packet]",
    stack_size = 100,
    durability = 1,
    durability_description_key = "description.science-pack-remaining-amount-key",
    durability_description_value = "description.science-pack-remaining-amount-value"
  },
  {
    type = "tool",
    name = "audit-ready-deliverable",
    icon = "__tanks_for_bob_fork__/graphics/icons/placeholder.png",
    icon_size = 64,
    subgroup = "corporate-compliance",
    order = "d[advanced-validation]-b[audit-ready-deliverable]",
    stack_size = 100,
    durability = 1,
    durability_description_key = "description.science-pack-remaining-amount-key",
    durability_description_value = "description.science-pack-remaining-amount-value"
  },
  {
    type = "tool",
    name = "stakeholder-review-summary",
    icon = "__tanks_for_bob_fork__/graphics/icons/placeholder.png",
    icon_size = 64,
    subgroup = "corporate-compliance",
    order = "d[advanced-validation]-c[stakeholder-review-summary]",
    stack_size = 100,
    durability = 1,
    durability_description_key = "description.science-pack-remaining-amount-key",
    durability_description_value = "description.science-pack-remaining-amount-value"
  },
  {
    type = "tool",
    name = "liability-contained-report",
    icon = "__tanks_for_bob_fork__/graphics/icons/placeholder.png",
    icon_size = 64,
    subgroup = "corporate-compliance",
    order = "d[advanced-validation]-d[liability-contained-report]",
    stack_size = 100,
    durability = 1,
    durability_description_key = "description.science-pack-remaining-amount-key",
    durability_description_value = "description.science-pack-remaining-amount-value"
  },
  {
    type = "tool",
    name = "board-review-docket",
    icon = "__tanks_for_bob_fork__/graphics/icons/placeholder.png",
    icon_size = 64,
    subgroup = "corporate-compliance",
    order = "d[advanced-validation]-e[board-review-docket]",
    stack_size = 50,
    durability = 1,
    durability_description_key = "description.science-pack-remaining-amount-key",
    durability_description_value = "description.science-pack-remaining-amount-value"
  },
  {
    type = "tool",
    name = "board-advisory-risk-assessment",
    icon = "__tanks_for_bob_fork__/graphics/icons/placeholder.png",
    icon_size = 64,
    subgroup = "corporate-compliance",
    order = "d[advanced-validation]-f[board-advisory-risk-assessment]",
    stack_size = 25,
    durability = 1,
    durability_description_key = "description.science-pack-remaining-amount-key",
    durability_description_value = "description.science-pack-remaining-amount-value"
  },
    -- more e-tech
  {
    type = "module",
    name = "Cradinal-grametter",
    icon = "__tanks_for_bob_fork__/graphics/icons/Cradinal-grametter.png",
    icon_size = 64,
    subgroup = "module",
    category = "productivity",
    tier = 1,
    order = "c[productivity]-a[Cradinal-grametter]",
    stack_size = 10,
    effect = { productivity = 0.02, consumption = 0.15, speed = -0.02, pollution = 0.02 },
    },
  {
    type = "module",
    name = "Hydrocoptic-marselvanes",
    icon = "__tanks_for_bob_fork__/graphics/icons/Hydrocoptic-marselvanes.png",
    icon_size = 64,
    subgroup = "module",
    category = "productivity",
    tier = 2,
    order = "c[productivity]-b[Hydrocoptic-marselvanes]",
    stack_size = 10,
    effect = { productivity = 0.03, consumption = 0.25, speed = -0.035, pollution = 0.035 },
    },
  {
    type = "module",
    name = "Retro-Encabulator",
    icon = "__tanks_for_bob_fork__/graphics/icons/Retro-Encabulator.png",
    icon_size = 64,
    subgroup = "module",
    category = "productivity",
    tier = 3,
    order = "c[productivity]-c[Retro-Encabulator]",
    stack_size = 10,
    effect = { productivity = 0.04, consumption = 0.40, speed = -0.05, pollution = 0.05 },
    },
        {
    type = "item",
    name = "PhaseDetractor",
    icon = "__tanks_for_bob_fork__/graphics/icons/PhaseDetractor.png",
    icon_size = 64,
    subgroup = "tank-ammo-components",
    order = "a[tank-ammo-components]-a[casing]",
    stack_size = 10,
    },
    {
    type = "item",
    name = "Canister-waste",
    icon = "__tanks_for_bob_fork__/graphics/icons/Canister-waste.png",
    icon_size = 64,
    subgroup = "tank-ammo-components",
    order = "a[tank-ammo-components]-a[casing]",
    stack_size = 100,
    },
    {
    type = "item",
    name = "Canister-Radioactivewaste",
    icon = "__tanks_for_bob_fork__/graphics/icons/Canister-Radioactivewaste.png",
    icon_size = 64,
    subgroup = "tank-ammo-components",
    order = "a[tank-ammo-components]-a[casing]",
    stack_size = 100,
    },
     {
    type = "item",
    name = "Canister",
    icon = "__tanks_for_bob_fork__/graphics/icons/Canister.png",
    icon_size = 64,
    subgroup = "tank-ammo-components",
    order = "a[tank-ammo-components]-a[casing]",
    stack_size = 100,
    },
    --Charged-Canister
     {
    type = "item",
    name = "Charged-Canister",
    icon = "__tanks_for_bob_fork__/graphics/icons/Charged-Canister.png",
    icon_size = 64,
    subgroup = "tank-ammo-components",
    order = "a[tank-ammo-components]-a[casing]",
    stack_size = 10,
     fuel_category = "chemical",
     fuel_acceleration_multiplier = 0.6,
    fuel_top_speed_multiplier = 0.6,
    fuel_emissions_multiplier = 0.6,
    fuel_value = "68.5MJ",
    },

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

-- Seablock encabulation intermediary products
  {
    type = "item",
    name = "trace-mineral-slurry",
    icon = "__tanks_for_bob_fork__/graphics/icons/Trace Mineral Slurry.png",
    icon_size = 128,
    subgroup = "Seablock",
    order = "z-a[trace-mineral-slurry]",
    stack_size = 10
  },
  {
    type = "item",
    name = "saline-particulate",
    icon = "__tanks_for_bob_fork__/graphics/icons/Saline Particulate.png",
    icon_size = 128,
    subgroup = "Seablock",
    order = "z-b[saline-particulate]",
    stack_size = 10
  },
  {
    type = "item",
    name = "ionic-scum",
    icon = "__tanks_for_bob_fork__/graphics/icons/Ionic Scum.png",
    icon_size = 128,
    subgroup = "Seablock",
    order = "z-c[ionic-scum]",
    stack_size = 10
  },
  {
    type = "item",
    name = "heavy-brine-fraction",
    icon = "__tanks_for_bob_fork__/graphics/icons/Heavy Brine Fraction.png",
    icon_size = 128,
    subgroup = "Seablock",
    order = "z-d[heavy-brine-fraction]",
    stack_size = 10
  },
  {
    type = "item",
    name = "microcrystal-sediment",
    icon = "__tanks_for_bob_fork__/graphics/icons/Microcrystal Sediment.png",
    icon_size = 128,
    subgroup = "Seablock",
    order = "z-e[microcrystal-sediment]",
    stack_size = 10
  },
  {
    type = "item",
    name = "fish-oil-residue",
    icon = "__tanks_for_bob_fork__/graphics/icons/Fish Oil Residue.png",
    icon_size = 128,
    subgroup = "Seablock",
    order = "z-f[fish-oil-residue]",
    stack_size = 10
  },
  {
    type = "item",
    name = "protein-slurry",
    icon = "__tanks_for_bob_fork__/graphics/icons/Protein Slurry.png",
    icon_size = 128,
    subgroup = "Seablock",
    order = "z-g[protein-slurry]",
    stack_size = 10
  },
  {
    type = "item",
    name = "calcified-bone-dust",
    icon = "__tanks_for_bob_fork__/graphics/icons/Calcified Bone Dust.png",
    icon_size = 128,
    subgroup = "Seablock",
    order = "z-h[calcified-bone-dust]",
    stack_size = 10
  },
  {
    type = "item",
    name = "enzyme-paste",
    icon = "__tanks_for_bob_fork__/graphics/icons/Enzyme Paste.png",
    icon_size = 128,
    subgroup = "Seablock",
    order = "z-i[enzyme-paste]",
    stack_size = 10
  },
  {
    type = "item",
    name = "rendered-organics",
    icon = "__tanks_for_bob_fork__/graphics/icons/Rendered Organics.png",
    icon_size = 128,
    subgroup = "Seablock",
    order = "z-j[rendered-organics]",
    stack_size = 10
  },
-- Preencabulation intermediary products
  {
    type = "item",
    name = "hydrolyzed-suspension",
    icon = "__tanks_for_bob_fork__/graphics/icons/hydrolyzed-suspension.png",
    icon_size = 128,
    subgroup = "Preencabulation",
    order = "a[hydro-phase]-a[hydrolyzed-suspension]",
    stack_size = 10
  },
  {
    type = "item",
    name = "phase-diluted-brine",
    icon = "__tanks_for_bob_fork__/graphics/icons/phase-diluted-brine.png",
    icon_size = 128,
    subgroup = "Preencabulation",
    order = "a[hydro-phase]-b[phase-diluted-brine]",
    stack_size = 10
  },
  {
    type = "item",
    name = "osmotic-residue",
    icon = "__tanks_for_bob_fork__/graphics/icons/osmotic-residue.png",
    icon_size = 128,
    subgroup = "Preencabulation",
    order = "a[hydro-phase]-c[osmotic-residue]",
    stack_size = 10
  },
  {
    type = "item",
    name = "gradient-saline-matrix",
    icon = "__tanks_for_bob_fork__/graphics/icons/gradient-saline-matrix.png",
    icon_size = 128,
    subgroup = "Preencabulation",
    order = "a[hydro-phase]-d[gradient-saline-matrix]",
    stack_size = 10
  },
  {
    type = "item",
    name = "biphasic-brine-gel",
    icon = "__tanks_for_bob_fork__/graphics/icons/biphasic-brine-gel.png",
    icon_size = 128,
    subgroup = "Preencabulation",
    order = "a[hydro-phase]-e[biphasic-brine-gel]",
    stack_size = 10
  },
  {
    type = "item",
    name = "salinity-locked-emulsion",
    icon = "__tanks_for_bob_fork__/graphics/icons/salinity-locked-emulsion.png",
    icon_size = 128,
    subgroup = "Preencabulation",
    order = "a[hydro-phase]-f[salinity-locked-emulsion]",
    stack_size = 10
  },
  {
    type = "item",
    name = "hydrocoptic-precursor",
    icon = "__tanks_for_bob_fork__/graphics/icons/hydrocoptic-precursor.png",
    icon_size = 128,
    subgroup = "Preencabulation",
    order = "a[hydro-phase]-g[hydrocoptic-precursor]",
    stack_size = 10
  },
  {
    type = "item",
    name = "denatured-organic-base",
    icon = "__tanks_for_bob_fork__/graphics/icons/denatured-organic-base.png",
    icon_size = 128,
    subgroup = "Preencabulation",
    order = "b[bio-organic]-a[denatured-organic-base]",
    stack_size = 10
  },
  {
    type = "item",
    name = "enzyme-saturated-mass",
    icon = "__tanks_for_bob_fork__/graphics/icons/enzyme-saturated-mass.png",
    icon_size = 128,
    subgroup = "Preencabulation",
    order = "b[bio-organic]-b[enzyme-saturated-mass]",
    stack_size = 10
  },
  {
    type = "item",
    name = "lipid-carrier-gel",
    icon = "__tanks_for_bob_fork__/graphics/icons/lipid-carrier-gel.png",
    icon_size = 128,
    subgroup = "Preencabulation",
    order = "b[bio-organic]-c[lipid-carrier-gel]",
    stack_size = 10
  },
  {
    type = "item",
    name = "bio-reactive-slurry",
    icon = "__tanks_for_bob_fork__/graphics/icons/bio-reactive-slurry.png",
    icon_size = 128,
    subgroup = "Preencabulation",
    order = "b[bio-organic]-d[bio-reactive-slurry]",
    stack_size = 10
  },
  {
    type = "item",
    name = "catalytic-organic-medium",
    icon = "__tanks_for_bob_fork__/graphics/icons/catalytic-organic-medium.png",
    icon_size = 128,
    subgroup = "Preencabulation",
    order = "b[bio-organic]-e[catalytic-organic-medium]",
    stack_size = 10
  },
  {
    type = "item",
    name = "reactive-enzyme-binder",
    icon = "__tanks_for_bob_fork__/graphics/icons/reactive-enzyme-binder.png",
    icon_size = 128,
    subgroup = "Preencabulation",
    order = "b[bio-organic]-f[reactive-enzyme-binder]",
    stack_size = 10
  },
  {
    type = "item",
    name = "bio-synthetic-precursor",
    icon = "__tanks_for_bob_fork__/graphics/icons/bio-synthetic-precursor.png",
    icon_size = 128,
    subgroup = "Preencabulation",
    order = "b[bio-organic]-g[bio-synthetic-precursor]",
    stack_size = 10
  },
  {
    type = "item",
    name = "crystalline-agglomerate",
    icon = "__tanks_for_bob_fork__/graphics/icons/crystalline-agglomerate.png",
    icon_size = 128,
    subgroup = "Preencabulation",
    order = "c[mineral-crystalline]-a[crystalline-agglomerate]",
    stack_size = 10
  },
  {
    type = "item",
    name = "fractured-lattice-mass",
    icon = "__tanks_for_bob_fork__/graphics/icons/fractured-lattice-mass.png",
    icon_size = 128,
    subgroup = "Preencabulation",
    order = "c[mineral-crystalline]-b[fractured-lattice-mass]",
    stack_size = 10
  },
  {
    type = "item",
    name = "ceramic-seed-grain",
    icon = "__tanks_for_bob_fork__/graphics/icons/ceramic-seed-grain.png",
    icon_size = 128,
    subgroup = "Preencabulation",
    order = "c[mineral-crystalline]-c[ceramic-seed-grain]",
    stack_size = 10
  },
  {
    type = "item",
    name = "mineral-phase-fragments",
    icon = "__tanks_for_bob_fork__/graphics/icons/mineral-phase-fragments.png",
    icon_size = 128,
    subgroup = "Preencabulation",
    order = "c[mineral-crystalline]-d[mineral-phase-fragments]",
    stack_size = 10
  },
  {
    type = "item",
    name = "ceramic-lattice-core",
    icon = "__tanks_for_bob_fork__/graphics/icons/ceramic-lattice-core.png",
    icon_size = 128,
    subgroup = "Preencabulation",
    order = "c[mineral-crystalline]-e[ceramic-lattice-core]",
    stack_size = 10
  },
  {
    type = "item",
    name = "compressed-crystal-bed",
    icon = "__tanks_for_bob_fork__/graphics/icons/compressed-crystal-bed.png",
    icon_size = 128,
    subgroup = "Preencabulation",
    order = "c[mineral-crystalline]-f[compressed-crystal-bed]",
    stack_size = 10
  },
  {
    type = "item",
    name = "bioceramic-preform",
    icon = "__tanks_for_bob_fork__/graphics/icons/bioceramic-preform.png",
    icon_size = 128,
    subgroup = "Preencabulation",
    order = "c[mineral-crystalline]-g[bioceramic-preform]",
    stack_size = 10
  },
  {
    type = "item",
    name = "charged-ionic-matrix",
    icon = "__tanks_for_bob_fork__/graphics/icons/charged-ionic-matrix.png",
    icon_size = 128,
    subgroup = "Preencabulation",
    order = "d[electro-reactive]-a[charged-ionic-matrix]",
    stack_size = 10
  },
  {
    type = "item",
    name = "dielectric-suspension",
    icon = "__tanks_for_bob_fork__/graphics/icons/dielectric-suspension.png",
    icon_size = 128,
    subgroup = "Preencabulation",
    order = "d[electro-reactive]-b[dielectric-suspension]",
    stack_size = 10
  },
  {
    type = "item",
    name = "conductive-residue",
    icon = "__tanks_for_bob_fork__/graphics/icons/conductive-residue.png",
    icon_size = 128,
    subgroup = "Preencabulation",
    order = "d[electro-reactive]-c[conductive-residue]",
    stack_size = 10
  },
  {
    type = "item",
    name = "phase-unstable-granulate",
    icon = "__tanks_for_bob_fork__/graphics/icons/phase-unstable-granulate.png",
    icon_size = 128,
    subgroup = "Preencabulation",
    order = "d[electro-reactive]-d[phase-unstable-granulate]",
    stack_size = 10
  },
  {
    type = "item",
    name = "balanced-reactive-medium",
    icon = "__tanks_for_bob_fork__/graphics/icons/balanced-reactive-medium.png",
    icon_size = 128,
    subgroup = "Preencabulation",
    order = "d[electro-reactive]-e[balanced-reactive-medium]",
    stack_size = 10
  },
  {
    type = "item",
    name = "phase-primed-carrier",
    icon = "__tanks_for_bob_fork__/graphics/icons/phase-primed-carrier.png",
    icon_size = 128,
    subgroup = "Preencabulation",
    order = "d[electro-reactive]-f[phase-primed-carrier]",
    stack_size = 10
  },
  {
    type = "item",
    name = "electro-phase-precursor",
    icon = "__tanks_for_bob_fork__/graphics/icons/electro-phase-precursor.png",
    icon_size = 128,
    subgroup = "Preencabulation",
    order = "d[electro-reactive]-g[electro-phase-precursor]",
    stack_size = 10
  },
  {
    type = "item",
    name = "marseline-compound",
    icon = "__tanks_for_bob_fork__/graphics/icons/Marseline Compound.png",
    icon_size = 128,
    subgroup = "tank-ammo-components",
    order = "b[encabulation-intermediates]-a[marseline-compound]",
    stack_size = 10
  },
  {
    type = "item",
    name = "bioceramic-grit",
    icon = "__tanks_for_bob_fork__/graphics/icons/Bioceramic Grit.png",
    icon_size = 128,
    subgroup = "tank-ammo-components",
    order = "b[encabulation-intermediates]-b[bioceramic-grit]",
    stack_size = 10
  },
  {
    type = "item",
    name = "hydrocoptic-crystal",
    icon = "__tanks_for_bob_fork__/graphics/icons/Hydrocoptic Crystal.png",
    icon_size = 128,
    subgroup = "tank-ammo-components",
    order = "b[encabulation-intermediates]-c[hydrocoptic-crystal]",
    stack_size = 10
  },
  {
    type = "item",
    name = "amulite-flakes",
    icon = "__tanks_for_bob_fork__/graphics/icons/Amulite Flakes.png",
    icon_size = 128,
    subgroup = "tank-ammo-components",
    order = "b[encabulation-intermediates]-d[amulite-flakes]",
    stack_size = 10
  },
  {
    type = "item",
    name = "phase-reactive-granules",
    icon = "__tanks_for_bob_fork__/graphics/icons/Phase Reactive Granules.png",
    icon_size = 128,
    subgroup = "tank-ammo-components",
    order = "b[encabulation-intermediates]-e[phase-reactive-granules]",
    stack_size = 10
  },
  {
    type = "item",
    name = "oscillated-lubricant",
    icon = "__tanks_for_bob_fork__/graphics/icons/Oscillated Lubricant.png",
    icon_size = 128,
    subgroup = "tank-ammo-components",
    order = "b[encabulation-intermediates]-f[oscillated-lubricant]",
    stack_size = 10
  },
  {
    type = "item",
    name = "stabilized-brine-gel",
    icon = "__tanks_for_bob_fork__/graphics/icons/Stabilized Brine Gel.png",
    icon_size = 128,
    subgroup = "tank-ammo-components",
    order = "b[encabulation-intermediates]-g[stabilized-brine-gel]",
    stack_size = 10
  },
  {
    type = "item",
    name = "dielectric-chowder",
    icon = "__tanks_for_bob_fork__/graphics/icons/Dielectric Chowder.png",
    icon_size = 128,
    subgroup = "tank-ammo-components",
    order = "b[encabulation-intermediates]-h[dielectric-chowder]",
    stack_size = 10
  },
  {
    type = "item",
    name = "pre-turbulated-emulsion",
    icon = "__tanks_for_bob_fork__/graphics/icons/Pre Turbulated Emulsion.png",
    icon_size = 128,
    subgroup = "tank-ammo-components",
    order = "b[encabulation-intermediates]-i[pre-turbulated-emulsion]",
    stack_size = 10
  },
  {
    type = "item",
    name = "viscoelastic-froth",
    icon = "__tanks_for_bob_fork__/graphics/icons/Viscoelastic Froth.png",
    icon_size = 128,
    subgroup = "tank-ammo-components",
    order = "b[encabulation-intermediates]-j[viscoelastic-froth]",
    stack_size = 10
  },
  {
    type = "item",
    name = "executive-marseline-resin",
    icon = "__tanks_for_bob_fork__/graphics/icons/Executive Marseline Resin.png",
    icon_size = 128,
    subgroup = "tank-ammo-components",
    order = "b[encabulation-intermediates]-k[executive-marseline-resin]",
    stack_size = 10
  },
  {
    type = "item",
    name = "encabuloy-alloy",
    icon = "__tanks_for_bob_fork__/graphics/icons/Encabuloy Alloy.png",
    icon_size = 128,
    subgroup = "tank-ammo-components",
    order = "b[encabulation-intermediates]-l[encabuloy-alloy]",
    stack_size = 10
  },
  {
    type = "item",
    name = "hyperphase-matrix",
    icon = "__tanks_for_bob_fork__/graphics/icons/Hyperphase Matrix.png",
    icon_size = 128,
    subgroup = "tank-ammo-components",
    order = "b[encabulation-intermediates]-m[hyperphase-matrix]",
    stack_size = 10
  },
  {
    type = "item",
    name = "retrograde-polymer-sheet",
    icon = "__tanks_for_bob_fork__/graphics/icons/Retrograde Polymer Sheet.png",
    icon_size = 128,
    subgroup = "tank-ammo-components",
    order = "b[encabulation-intermediates]-n[retrograde-polymer-sheet]",
    stack_size = 10
  },
  {
    type = "item",
    name = "duplexed-substrate",
    icon = "__tanks_for_bob_fork__/graphics/icons/Duplexed Substrate.png",
    icon_size = 128,
    subgroup = "tank-ammo-components",
    order = "b[encabulation-intermediates]-o[duplexed-substrate]",
    stack_size = 10
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
    subgroup = "tank-ammo-components",
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
    category = "efficiency",
    tier = 1,
    order = "a[tank-ammo-components]-a[casing]",
    stack_size = 10,
	effect = { consumption = -0.1},
	},
	  {
    type = "module",
    name = "DuctedSpervingArm",
    icon = "__tanks_for_bob_fork__/graphics/icons/DuctedSpervingArm.png",
    icon_size = 64,
    subgroup = "module",
    category = "efficiency",
    tier = 2,
    order = "a[tank-ammo-components]-a[casing]",
    stack_size = 10,
	effect = { consumption = -0.2 },
	},
	  {
    type = "module",
    name = "DuplexedSpervingArm",
    icon = "__tanks_for_bob_fork__/graphics/icons/DuplexedSpervingArm.png",
    icon_size = 64,
    subgroup = "module",
    category = "efficiency",
    tier = 3,
    order = "a[tank-ammo-components]-a[casing]",
    stack_size = 10,
	effect = { consumption = -0.3 },
	},
-- encabulators
  {
    type = "module",
    name = "Encabulator",
    icon = "__tanks_for_bob_fork__/graphics/icons/Encabulator.png",
    icon_size = 64,
    subgroup = "module",
    category = "speed",
    tier = 1,
    order = "b[speed]-a[Encabulator]",
    stack_size = 10,
    effect = { speed = 0.08, consumption = 0.20 },
    },
  {
    type = "module",
    name = "TurboEncabulator",
    icon = "__tanks_for_bob_fork__/graphics/icons/TurboEncabulator.png",
    icon_size = 64,
    subgroup = "module",
    category = "speed",
    tier = 2,
    order = "b[speed]-b[TurboEncabulator]",
    stack_size = 10,
    effect = { speed = 0.14, consumption = 0.35 },
    },
  {
    type = "module",
    name = "HyperEncabulator",
    icon = "__tanks_for_bob_fork__/graphics/icons/HyperEncabulator.png",
    icon_size = 64,
    subgroup = "module",
    category = "speed",
    tier = 3,
    order = "b[speed]-c[HyperEncabulator]",
    stack_size = 10,
    effect = { speed = 0.20, consumption = 0.50 },
    },
  {
    type = "module",
    name = "FramulatedEncabulator",
    icon = "__tanks_for_bob_fork__/graphics/icons/FramulatedEncabulator.png",
    icon_size = 64,
    subgroup = "module",
    category = "productivity",
    tier = 2,
    order = "d[framulated-encabulator]",
    stack_size = 5,
    effect =
    {
      speed = 0.20,
      productivity = 0.06,
      consumption = 0.40,
      pollution = 0.075
    },
    limitation_message_key = "production-module-usable-only-on-intermediates"
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
    stack_size = 50,
    fuel_category = "chemical",
    fuel_value = "2MJ",
    fuel_acceleration_multiplier = 0.5,
    fuel_top_speed_multiplier = 0.5,
    fuel_emissions_multiplier = 50
	},
	{
    type = "item",
    name = "tank-ammo-Radioactivewaste",
    icon = "__tanks_for_bob_fork__/graphics/icons/Radioactivewaste.png",
    icon_size = 64,

    subgroup = "tank-ammo-components",
    order = "a[tank-ammo-components]-b[Radioactivewaste]",
    stack_size = 10,
    fuel_category = "chemical",
    fuel_value = "500kJ",
    fuel_acceleration_multiplier = 0.25,
    fuel_top_speed_multiplier = 0.25,
    fuel_emissions_multiplier = 500
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
    damage_radius = 25,
    subgroup = "gun",
    order = "f[land-mine]",
    place_result = "land-mine-poison",
    stack_size = 20,
    trigger_radius = 5
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
    stack_size = 50
  },
  {
    type = "item",
    name = "compressed-biohazard-waste",
  icon = "__tanks_for_bob_fork__/graphics/icons/compressed-biohazard-waste.png",
  icon_size = 64,
  subgroup = "corporate-compliance",
  order = "z[compressed-biohazard-waste]",
  stack_size = 50,

  fuel_category = "chemical",
  fuel_value = "7MJ",
  fuel_acceleration_multiplier = 0.25,
  fuel_top_speed_multiplier = 0.25,

  -- Horrible, but not quite radioactive waste levels of obscene.
  fuel_emissions_multiplier = 220
}
}
)
