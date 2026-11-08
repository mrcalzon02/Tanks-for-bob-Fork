data:extend({

-- =========================================================
-- EARLY SEABLOCK FOUNDATION / THREE-PATH ESCAPE LADDER
-- =========================================================
-- Structure:
--   1. Water path: beachpump -> wood-basin -> water wheel -> boiler -> pump -> condenser -> calcifier -> shaler
--   2. Wood/food path: growing plot -> cooking fire -> meal -> stone tools -> pondering hovel -> quarry
-- The wooden weapon is a starting handcraft; its independent root technology
-- discovers wooden ammunition when the player first acquires wood.
--   3. Clay/kiln path: clay pit -> fish pond branch + kiln -> brick -> crude glass
-- These paths are deliberately flatter than the old ladder so early SeaBlock can be researched more freely.
-- The three paths rejoin at Steam-Compressor, where meal becomes the continuing research baseline.
    {
        type = "technology",
        name = "beachpump",
        icon = "__tanks_for_bob_fork__/graphics/icons/beachpump.png",
        icon_size = 64,
        effects = {
            { type = "unlock-recipe", recipe = "beachpump" },
        },
        prerequisites = {},
        unit = {
            count = 5,
            ingredients = {{"Seared-fish", 1}},
            time = 10
        },
        order = "aa-a"
    },

-- =========================================================
-- WATER HANDLING PATH
-- =========================================================
    {
        type = "technology",
        name = "wood-basin",
        icon = "__tanks_for_bob_fork__/graphics/icons/wood-basin.png",
        icon_size = 64,
        effects = {
            { type = "unlock-recipe", recipe = "wood-basin" },
        },
        prerequisites = {"beachpump"},
        unit = {
            count = 5,
            ingredients = {{"Seared-fish", 1}},
            time = 10
        },
        order = "aa-wa"
    },
    {
        type = "technology",
        name = "stone-water-wheel",
        icon = "__tanks_for_bob_fork__/graphics/icons/stone-water-wheel.png",
        icon_size = 64,
        effects = {
            { type = "unlock-recipe", recipe = "stone-water-wheel" },
        },
        prerequisites = {"wood-basin", "brick"},
        unit = {
            count = 10,
            ingredients = {{"Seared-fish", 1}},
            time = 10
        },
        order = "aa-wb"
    },
    {
        type = "technology",
        name = "solar-boiler",
        icon = "__tanks_for_bob_fork__/graphics/icons/solar-boiler.png",
        icon_size = 64,
        effects = {
            { type = "unlock-recipe", recipe = "solar-boiler" },
        },
        prerequisites = {"stone-water-wheel"},
        unit = {
            count = 10,
            ingredients = {{"Seared-fish", 1}},
            time = 10
        },
        order = "aa-wc"
    },
    {
        type = "technology",
        name = "primitive-steam-powered-pump",
        icon = "__tanks_for_bob_fork__/graphics/icons/primitive-steam-powered-pump.png",
        icon_size = 64,
        effects = {
            { type = "unlock-recipe", recipe = "primitive-steam-powered-pump" },
        },
        prerequisites = {"solar-boiler"},
        unit = {
            count = 10,
            ingredients = {{"Seared-fish", 1}},
            time = 10
        },
        order = "aa-wd"
    },
    {
        type = "technology",
        name = "steam-condenser",
        icon = "__tanks_for_bob_fork__/graphics/icons/steam-condenser.png",
        icon_size = 64,
        effects = {
            { type = "unlock-recipe", recipe = "steam-condenser" },
        },
        prerequisites = {"primitive-steam-powered-pump", "crude-glass"},
        unit = {
            count = 10,
            ingredients = {{"Seared-fish", 1}},
            time = 10
        },
        order = "aa-we"
    },
    {
        type = "technology",
        name = "calcifier",
        icon = "__tanks_for_bob_fork__/graphics/icons/calcifier.png",
        icon_size = 64,
        effects = {
            { type = "unlock-recipe", recipe = "calcifier" },
        },
        prerequisites = {"steam-condenser"},
        unit = {
            count = 10,
            ingredients = {{"Seared-fish", 1}},
            time = 10
        },
        order = "aa-wf"
    },
    {
        type = "technology",
        name = "shaler",
        icon = "__tanks_for_bob_fork__/graphics/icons/shaler.png",
        icon_size = 64,
        effects = {
            { type = "unlock-recipe", recipe = "shaler" },
        },
        prerequisites = {"calcifier"},
        unit = {
            count = 10,
            ingredients = {{"Seared-fish", 1}},
            time = 10
        },
        order = "aa-wg"
    },

-- =========================================================
-- WOOD, FOOD, AND PRIMITIVE TOOLING PATH
-- =========================================================
    {
        type = "technology",
        name = "growing-plot",
        localised_name = {"", "Lumberyard"},
        localised_description = {"", "Unlocks the Lumberyard, a primitive steam-driven timber saw."},
        icon = "__tanks_for_bob_fork__/graphics/icons/lumberyard-v2b.png",
        icon_size = 64,
        effects = {
            { type = "unlock-recipe", recipe = "growing-plot" },
        },
        prerequisites = {"beachpump"},
        unit = {
            count = 5,
            ingredients = {{"Seared-fish", 1}},
            time = 10
        },
        order = "aa-ta"
    },
    {
        type = "technology",
        name = "wood-spear",
        icon = "__tanks_for_bob_fork__/graphics/icons/wood-spear.png",
        icon_size = 64,
        effects = {
            { type = "unlock-recipe", recipe = "Sharp-stick" },
        },
        research_trigger = {
            type = "scripted",
            trigger_description = {"tanks-for-bob-fork.acquire-wood"}
        },
        order = "aa-a"
    },
    {
        type = "technology",
        name = "cooking-fire",
        icon = "__tanks_for_bob_fork__/graphics/icons/cooking-fire.png",
        icon_size = 64,
        effects = {
            { type = "unlock-recipe", recipe = "cooking-fire" },
        },
        prerequisites = {"growing-plot", "brick"},
        unit = {
            count = 5,
            ingredients = {{"Seared-fish", 1}},
            time = 10
        },
        order = "aa-tc"
    },
    {
        type = "technology",
        name = "meal",
        icon = "__tanks_for_bob_fork__/graphics/icons/meal.png",
        icon_size = 64,
        effects = {
            { type = "unlock-recipe", recipe = "meal" },
        },
        prerequisites = {"cooking-fire"},
        unit = {
            count = 10,
            ingredients = {{"Seared-fish", 1}},
            time = 10
        },
        order = "aa-td"
    },
    {
        type = "technology",
        name = "stone-tools",
        icon = "__tanks_for_bob_fork__/graphics/icons/stone-tools.png",
        icon_size = 64,
        effects = {
            { type = "unlock-recipe", recipe = "stone-tools" },
        },
        prerequisites = {"meal"},
        unit = {
            count = 10,
            ingredients = {{"Seared-fish", 1}, {"meal", 1}},
            time = 10
        },
        order = "aa-te"
    },
    {
        type = "technology",
        name = "pondering-hovel",
        icon = "__tanks_for_bob_fork__/graphics/icons/pondering-hovel.png",
        icon_size = 64,
        effects = {
            { type = "unlock-recipe", recipe = "pondering-hovel" },
        },
        prerequisites = {"stone-tools", "brick"},
        unit = {
            count = 5,
            ingredients = {{"Seared-fish", 1}, {"meal", 1}},
            time = 10
        },
        order = "aa-tf"
    },
    {
        type = "technology",
        name = "quarry",
        icon = "__tanks_for_bob_fork__/graphics/icons/quarry.png",
        icon_size = 64,
        effects = {
            { type = "unlock-recipe", recipe = "quarry" },
        },
        prerequisites = {"pondering-hovel"},
        unit = {
            count = 10,
            ingredients = {{"Seared-fish", 1}, {"meal", 1}},
            time = 10
        },
        order = "aa-tg"
    },

-- =========================================================
-- CLAY, KILN, CRUDE GLASS, AND FISH-POND PATH
-- =========================================================
    {
        type = "technology",
        name = "clay-pit",
        icon = "__tanks_for_bob_fork__/graphics/icons/clay-pit-v4c.png",
        icon_size = 64,
        effects = {
            { type = "unlock-recipe", recipe = "clay-pit" },
        },
        prerequisites = {"beachpump"},
        unit = {
            count = 5,
            ingredients = {{"Seared-fish", 1}},
            time = 10
        },
        order = "aa-ca"
    },
    {
        type = "technology",
        name = "fish-pond",
        icon = "__tanks_for_bob_fork__/graphics/icons/fish-pond.png",
        icon_size = 64,
        effects = {
            { type = "unlock-recipe", recipe = "fish-pond" },
        },
        prerequisites = {"clay-pit", "growing-plot", "brick"},
        unit = {
            count = 10,
            ingredients = {{"Seared-fish", 1}},
            time = 10
        },
        order = "aa-cb"
    },
    {
        type = "technology",
        name = "pit-kiln",
        icon = "__tanks_for_bob_fork__/graphics/icons/pit-kiln-v6-icon-64.png",
        icon_size = 64,
        effects = {
            { type = "unlock-recipe", recipe = "pit-kiln" },
        },
        prerequisites = {"clay-pit"},
        unit = {
            count = 5,
            ingredients = {{"Seared-fish", 1}},
            time = 10
        },
        order = "aa-cc"
    },
    {
        type = "technology",
        name = "brick",
        icon = "__tanks_for_bob_fork__/graphics/icons/brick.png",
        icon_size = 64,
        effects = {
            { type = "unlock-recipe", recipe = "brick" },
        },
        prerequisites = {"pit-kiln"},
        unit = {
            count = 5,
            ingredients = {{"Seared-fish", 1}},
            time = 10
        },
        order = "aa-cd"
    },
    {
        type = "technology",
        name = "crude-glass",
        icon = "__tanks_for_bob_fork__/graphics/icons/crude-glass.png",
        icon_size = 64,
        effects = {
            { type = "unlock-recipe", recipe = "crude-glass" },
        },
        prerequisites = {"brick"},
        unit = {
            count = 5,
            ingredients = {{"Seared-fish", 1}},
            time = 10
        },
        order = "aa-ce"
    },

-- =========================================================
-- EARLY SEABLOCK EXIT / FIRST CONSOLIDATED INDUSTRIAL STEP
-- =========================================================
    {
        type = "technology",
        name = "Steam-Compressor",
        icon = "__tanks_for_bob_fork__/graphics/icons/Steam-Compressor.png",
        icon_size = 64,
        effects = {
            { type = "unlock-recipe", recipe = "Steam-Compressor" },
            { type = "unlock-recipe", recipe = "Charged-Canister" },
            { type = "unlock-recipe", recipe = "UnCharge-Canister" },
            { type = "unlock-recipe", recipe = "stone-tools-iron" },
        },
        prerequisites = {"shaler", "quarry", "fish-pond", "meal"},
        unit = {
            count = 10,
            ingredients = {{"Seared-fish", 1}, {"meal", 1}},
            time = 10
        },
        order = "aa-z"
    },

-- =========================================================
-- CORPORATE COMPLIANCE / PAPERWORK PARASITE LADDER
-- =========================================================
    {
        type = "technology",
        name = "charcoal-processing",
        icon = "__tanks_for_bob_fork__/graphics/icons/charcoal.png",
        icon_size = 64,
        effects = {
            { type = "unlock-recipe", recipe = "charcoal" },
        },
        prerequisites = {"beachpump"},
        unit = {
            count = 10,
            ingredients = {{"Seared-fish", 1}},
            time = 10
        },
        order = "ab-ca"
    },
    {
        type = "technology",
        name = "wood-pulp-processing",
        icon = "__tanks_for_bob_fork__/graphics/icons/wood-pulp.png",
        icon_size = 64,
        effects = {
            { type = "unlock-recipe", recipe = "wood-pulp" },
        },
        prerequisites = {"charcoal-processing", "growing-plot"},
        unit = {
            count = 10,
            ingredients = {{"Seared-fish", 1}},
            time = 10
        },
        order = "ab-cb"
    },
    {
        type = "technology",
        name = "crude-paperwork",
        icon = "__tanks_for_bob_fork__/graphics/icons/crude-paper.png",
        icon_size = 64,
        effects = {
            { type = "unlock-recipe", recipe = "crude-paper" },
            { type = "unlock-recipe", recipe = "ink" },
        },
        prerequisites = {"wood-pulp-processing"},
        unit = {
            count = 15,
            ingredients = {{"Seared-fish", 1}},
            time = 10
        },
        order = "ab-cc"
    },
    {
        type = "technology",
        name = "basic-requisitioning",
        icon = "__tanks_for_bob_fork__/graphics/icons/requisition-slip.png",
        icon_size = 64,
        effects = {
            { type = "unlock-recipe", recipe = "requisition-slip" },
            { type = "unlock-recipe", recipe = "staples" },
            { type = "unlock-recipe", recipe = "stamps" },
            { type = "unlock-recipe", recipe = "folder" },
            { type = "unlock-recipe", recipe = "clipboard" },
        },
        prerequisites = {"crude-paperwork", "meal", "crude-glass"},
        unit = {
            count = 20,
            ingredients = {{"Seared-fish", 1}, {"meal", 1}},
            time = 10
        },
        order = "ab-cd"
    },
    {
        type = "technology",
        name = "work-order-generation",
        icon = "__tanks_for_bob_fork__/graphics/icons/work-order-slip.png",
        icon_size = 64,
        effects = {
            { type = "unlock-recipe", recipe = "work-order-slip" },
        },
        prerequisites = {"basic-requisitioning"},
        unit = {
            count = 25,
            ingredients = {{"Seared-fish", 1}, {"meal", 1}, {"requisition-slip", 1}},
            time = 12
        },
        order = "ab-ce"
    },
    {
        type = "technology",
        name = "work-order-certification",
        icon = "__tanks_for_bob_fork__/graphics/icons/certified-work-order.png",
        icon_size = 64,
        effects = {
            { type = "unlock-recipe", recipe = "certified-work-order" },
        },
        prerequisites = {"work-order-generation"},
        unit = {
            count = 30,
            ingredients = {{"Seared-fish", 1}, {"meal", 1}, {"work-order-slip", 1}},
            time = 12
        },
        order = "ab-cf"
    },
    {
        type = "technology",
        name = "evaluation-submission",
        icon = "__tanks_for_bob_fork__/graphics/icons/submitted-evaluation.png",
        icon_size = 64,
        effects = {
            { type = "unlock-recipe", recipe = "submitted-evaluation" },
            { type = "unlock-recipe", recipe = "decompose-certified-work-order" },
        },
        prerequisites = {"work-order-certification", "crude-glass"},
        unit = {
            count = 35,
            ingredients = {{"Seared-fish", 1}, {"meal", 1}, {"certified-work-order", 1}},
            time = 14
        },
        order = "ab-cg"
    },
    {
        type = "technology",
        name = "preliminary-risk-assessment",
        icon = "__tanks_for_bob_fork__/graphics/icons/risk-assessment.png",
        icon_size = 64,
        effects = {
            { type = "unlock-recipe", recipe = "risk-assessment" },
            { type = "unlock-recipe", recipe = "decompose-submitted-evaluation" },
        },
        prerequisites = {"evaluation-submission", "waste-processing-2", "mineral-fractionation"},
        unit = {
            count = 45,
            ingredients = {{"Seared-fish", 1}, {"meal", 1}, {"submitted-evaluation", 1}},
            time = 15
        },
        order = "ab-ch"
    },
	{
  type = "technology",
  name = "toxic-sludge-condensation",
  icon = "__tanks_for_bob_fork__/graphics/icons/toxic-sludge.png",
  icon_size = 64,
  effects =
  {
    { type = "unlock-recipe", recipe = "industrial-waste-to-toxic-sludge" },
    { type = "unlock-recipe", recipe = "radioactive-waste-to-toxic-sludge" },
    { type = "unlock-recipe", recipe = "corporate-waste-to-toxic-sludge" },
    { type = "unlock-recipe", recipe = "compress-toxic-sludge" },
  },
  prerequisites = {"risk-assessed-authorization"},
  unit =
  {
    count = 80,
    ingredients =
    {
      {"Seared-fish", 1},
      {"meal", 1},
      {"risk-assessed-work-order", 1}
    },
    time = 25
  },
  order = "cf-a"
},
    {
        type = "technology",
        name = "risk-assessed-authorization",
        icon = "__tanks_for_bob_fork__/graphics/icons/risk-assessed-work-order.png",
        icon_size = 64,
        effects = {
            { type = "unlock-recipe", recipe = "risk-assessed-work-order" },
            { type = "unlock-recipe", recipe = "corporate-waste-reprocessing" },
            { type = "unlock-recipe", recipe = "decompose-risk-assessed-work-order" },
        },
        prerequisites = {"preliminary-risk-assessment"},
        unit = {
            count = 55,
            ingredients = {{"Seared-fish", 1}, {"meal", 1}, {"risk-assessment", 1}},
            time = 18
        },
        order = "ab-ci"
    },
    {
        type = "technology",
        name = "compliance-packetization",
        icon = "__tanks_for_bob_fork__/graphics/icons/compliance-packet.png",
        icon_size = 64,
        effects = {
            { type = "unlock-recipe", recipe = "compliance-packet" },
        },
        prerequisites = {"risk-assessed-authorization", "ionic-phase-conditioning"},
        unit = {
            count = 70,
            ingredients = {{"Seared-fish", 1}, {"meal", 1}, {"risk-assessed-work-order", 1}},
            time = 20
        },
        order = "ab-cj"
    },
    {
        type = "technology",
        name = "audit-ready-deliverables",
        icon = "__tanks_for_bob_fork__/graphics/icons/audit-ready-deliverable.png",
        icon_size = 64,
        effects = {
            { type = "unlock-recipe", recipe = "audit-ready-deliverable" },
            { type = "unlock-recipe", recipe = "decompose-audit-ready-deliverable" },
        },
        prerequisites = {"compliance-packetization"},
        unit = {
            count = 80,
            ingredients = {{"Seared-fish", 1}, {"meal", 1}, {"compliance-packet", 1}},
            time = 22
        },
        order = "ab-ck"
    },
    {
        type = "technology",
        name = "stakeholder-review-process",
        icon = "__tanks_for_bob_fork__/graphics/icons/stakeholder-review-summary.png",
        icon_size = 64,
        effects = {
            { type = "unlock-recipe", recipe = "stakeholder-review-summary" },
        },
        prerequisites = {"audit-ready-deliverables", "pre-encabulation-materials"},
        unit = {
            count = 90,
            ingredients = {{"Seared-fish", 1}, {"meal", 1}, {"audit-ready-deliverable", 1}},
            time = 25
        },
        order = "ab-cl"
    },
    {
        type = "technology",
        name = "liability-containment",
        icon = "__tanks_for_bob_fork__/graphics/icons/liability-contained-report.png",
        icon_size = 64,
        effects = {
            { type = "unlock-recipe", recipe = "liability-contained-report" },
        },
        prerequisites = {"stakeholder-review-process"},
        unit = {
            count = 110,
            ingredients = {{"Seared-fish", 1}, {"meal", 1}, {"stakeholder-review-summary", 1}},
            time = 28
        },
        order = "ab-cm"
    },
    {
        type = "technology",
        name = "board-review-procedure",
        icon = "__tanks_for_bob_fork__/graphics/icons/board-review-docket.png",
        icon_size = 64,
        effects = {
            { type = "unlock-recipe", recipe = "board-review-docket" },
        },
        prerequisites = {"liability-containment", "advanced-encabulation-substrates"},
        unit = {
            count = 130,
            ingredients = {{"Seared-fish", 1}, {"meal", 1}, {"liability-contained-report", 1}},
            time = 30
        },
        order = "ab-cn"
    },
    {
        type = "technology",
        name = "board-advisory-risk-assessment",
        icon = "__tanks_for_bob_fork__/graphics/icons/board-advisory-risk-assessment.png",
        icon_size = 64,
        effects = {
            { type = "unlock-recipe", recipe = "board-advisory-risk-assessment" },
        },
        prerequisites = {"board-review-procedure", "Hyper-Encabulation-research", "framulated-encabulator-research"},
        unit = {
            count = 160,
            ingredients = {{"Seared-fish", 1}, {"meal", 1}, {"board-review-docket", 1}, {"liability-contained-report", 1}},
            time = 35
        },
        order = "ab-co"
    },

-- =========================================================
-- WASTE, CALCIFIER, SHALER, AND RADIOACTIVE REFINING
-- =========================================================
    {
        type = "technology",
        name = "waste-processing-2",
        icon = "__tanks_for_bob_fork__/graphics/icons/shaler.png",
        icon_size = 64,
        effects = {
            { type = "unlock-recipe", recipe = "Calcifier-pro-2" },
            { type = "unlock-recipe", recipe = "shaler2" },
            { type = "unlock-recipe", recipe = "radio-refine-2" },
        },
        prerequisites = {"shaler", "work-order-generation"},
        unit = {
            count = 25,
            ingredients = {{"Seared-fish", 1}, {"meal", 1}, {"work-order-slip", 1}},
            time = 10
        },
        order = "ab-a"
    },
    {
        type = "technology",
        name = "waste-processing-3",
        icon = "__tanks_for_bob_fork__/graphics/icons/shaler.png",
        icon_size = 64,
        effects = {
            { type = "unlock-recipe", recipe = "Calcifier-pro-3" },
            { type = "unlock-recipe", recipe = "shaler4" },
            { type = "unlock-recipe", recipe = "radio-refine-3" },
        },
        prerequisites = {"waste-processing-2", "mineral-fractionation", "work-order-certification"},
        unit = {
            count = 50,
            ingredients = {{"Seared-fish", 1}, {"meal", 1}, {"certified-work-order", 1}},
            time = 15
        },
        order = "ab-b"
    },

-- =========================================================
-- FOUR MATERIAL BRANCHES FOR PRE-ENCABULATION
-- =========================================================

-- BRANCH 1: Mineral / ceramic feedstock ladder
    {
        type = "technology",
        name = "mineral-fractionation",
        icon = "__tanks_for_bob_fork__/graphics/icons/Placeholder.png",
        icon_size = 64,
        effects = {
            { type = "unlock-recipe", recipe = "saline-particulate" },
            { type = "unlock-recipe", recipe = "ionic-scum" },
            { type = "unlock-recipe", recipe = "heavy-brine-fraction" },
            { type = "unlock-recipe", recipe = "microcrystal-sediment" },
        },
        prerequisites = {"shaler", "waste-processing-2", "basic-requisitioning", "work-order-generation"},
        unit = {
            count = 25,
            ingredients = {{"Seared-fish", 1}, {"meal", 1}, {"work-order-slip", 1}},
            time = 15
        },
        order = "ac-a"
    },
    {
        type = "technology",
        name = "ceramic-lattice-conditioning",
        icon = "__tanks_for_bob_fork__/graphics/icons/Placeholder.png",
        icon_size = 64,
        effects = {
            { type = "unlock-recipe", recipe = "crystalline-agglomerate" },
            { type = "unlock-recipe", recipe = "fractured-lattice-mass" },
            { type = "unlock-recipe", recipe = "ceramic-seed-grain" },
            { type = "unlock-recipe", recipe = "mineral-phase-fragments" },
            { type = "unlock-recipe", recipe = "ceramic-lattice-core" },
            { type = "unlock-recipe", recipe = "compressed-crystal-bed" },
            { type = "unlock-recipe", recipe = "bioceramic-preform" },
        },
        prerequisites = {"mineral-fractionation", "calcifier", "evaluation-submission", "bio-reactive-processing"},
        unit = {
            count = 45,
            ingredients = {{"Seared-fish", 1}, {"meal", 1}, {"submitted-evaluation", 1}},
            time = 15
        },
        order = "ac-b"
    },

-- BRANCH 2: Biological / organic rendering ladder
    {
        type = "technology",
        name = "bio-reactive-processing",
        icon = "__tanks_for_bob_fork__/graphics/icons/Placeholder.png",
        icon_size = 64,
        effects = {
            { type = "unlock-recipe", recipe = "protein-slurry" },
            { type = "unlock-recipe", recipe = "calcified-bone-dust" },
            { type = "unlock-recipe", recipe = "rendered-organics" },
            { type = "unlock-recipe", recipe = "enzyme-paste" },
        },
        prerequisites = {"fish-pond", "Steam-Compressor", "work-order-certification"},
        unit = {
            count = 35,
            ingredients = {{"Seared-fish", 1}, {"meal", 1}, {"certified-work-order", 1}},
            time = 15
        },
        order = "ad-a"
    },
    {
        type = "technology",
        name = "organic-substrate-conditioning",
        icon = "__tanks_for_bob_fork__/graphics/icons/Placeholder.png",
        icon_size = 64,
        effects = {
            { type = "unlock-recipe", recipe = "denatured-organic-base" },
            { type = "unlock-recipe", recipe = "enzyme-saturated-mass" },
            { type = "unlock-recipe", recipe = "lipid-carrier-gel" },
            { type = "unlock-recipe", recipe = "bio-reactive-slurry" },
            { type = "unlock-recipe", recipe = "catalytic-organic-medium" },
            { type = "unlock-recipe", recipe = "reactive-enzyme-binder" },
            { type = "unlock-recipe", recipe = "bio-synthetic-precursor" },
        },
        prerequisites = {"bio-reactive-processing", "evaluation-submission"},
        unit = {
            count = 45,
            ingredients = {{"Seared-fish", 1}, {"meal", 1}, {"submitted-evaluation", 1}},
            time = 15
        },
        order = "ad-b"
    },

-- BRANCH 3: Brine / emulsion conditioning ladder
    {
        type = "technology",
        name = "brine-conditioning",
        icon = "__tanks_for_bob_fork__/graphics/icons/Placeholder.png",
        icon_size = 64,
        effects = {
            { type = "unlock-recipe", recipe = "hydrolyzed-suspension" },
            { type = "unlock-recipe", recipe = "phase-diluted-brine" },
            { type = "unlock-recipe", recipe = "osmotic-residue" },
            { type = "unlock-recipe", recipe = "gradient-saline-matrix" },
            { type = "unlock-recipe", recipe = "biphasic-brine-gel" },
            { type = "unlock-recipe", recipe = "salinity-locked-emulsion" },
            { type = "unlock-recipe", recipe = "hydrocoptic-precursor" },
        },
        prerequisites = {"mineral-fractionation", "Steam-Compressor", "preliminary-risk-assessment"},
        unit = {
            count = 40,
            ingredients = {{"Seared-fish", 1}, {"meal", 1}, {"risk-assessment", 1}},
            time = 15
        },
        order = "ae-a"
    },
    {
        type = "technology",
        name = "stabilized-emulsion-systems",
        icon = "__tanks_for_bob_fork__/graphics/icons/Placeholder.png",
        icon_size = 64,
        effects = {
            { type = "unlock-recipe", recipe = "oscillated-lubricant" },
            { type = "unlock-recipe", recipe = "stabilized-brine-gel" },
            { type = "unlock-recipe", recipe = "dielectric-chowder" },
            { type = "unlock-recipe", recipe = "pre-turbulated-emulsion" },
            { type = "unlock-recipe", recipe = "viscoelastic-froth" },
        },
        prerequisites = {"brine-conditioning", "organic-substrate-conditioning", "audit-ready-deliverables", "biomineral-synthesis"},
        unit = {
            count = 65,
            ingredients = {{"Seared-fish", 1}, {"meal", 1}, {"audit-ready-deliverable", 1}},
            time = 20
        },
        order = "ae-b"
    },

-- BRANCH 4: Ionic / biomineral synthesis ladder
    {
        type = "technology",
        name = "ionic-phase-conditioning",
        icon = "__tanks_for_bob_fork__/graphics/icons/Placeholder.png",
        icon_size = 64,
        effects = {
            { type = "unlock-recipe", recipe = "charged-ionic-matrix" },
            { type = "unlock-recipe", recipe = "dielectric-suspension" },
            { type = "unlock-recipe", recipe = "conductive-residue" },
            { type = "unlock-recipe", recipe = "phase-unstable-granulate" },
            { type = "unlock-recipe", recipe = "balanced-reactive-medium" },
            { type = "unlock-recipe", recipe = "phase-primed-carrier" },
            { type = "unlock-recipe", recipe = "electro-phase-precursor" },
        },
        prerequisites = {"organic-substrate-conditioning", "ceramic-lattice-conditioning", "risk-assessed-authorization"},
        unit = {
            count = 50,
            ingredients = {{"Seared-fish", 1}, {"meal", 1}, {"risk-assessed-work-order", 1}},
            time = 20
        },
        order = "af-a"
    },
    {
        type = "technology",
        name = "biomineral-synthesis",
        icon = "__tanks_for_bob_fork__/graphics/icons/Placeholder.png",
        icon_size = 64,
        effects = {
            { type = "unlock-recipe", recipe = "marseline-compound" },
            { type = "unlock-recipe", recipe = "bioceramic-grit" },
            { type = "unlock-recipe", recipe = "hydrocoptic-crystal" },
            { type = "unlock-recipe", recipe = "amulite-flakes" },
            { type = "unlock-recipe", recipe = "phase-reactive-granules" },
        },
        prerequisites = {"ionic-phase-conditioning", "ceramic-lattice-conditioning", "compliance-packetization", "brine-conditioning"},
        unit = {
            count = 50,
            ingredients = {{"Seared-fish", 1}, {"meal", 1}, {"compliance-packet", 1}},
            time = 20
        },
        order = "af-b"
    },

-- =========================================================
-- PRE-ENCABULATION MATERIAL INTEGRATION
-- =========================================================
    {
        type = "technology",
        name = "pre-encabulation-materials",
        icon = "__tanks_for_bob_fork__/graphics/icons/Placeholder.png",
        icon_size = 64,
        effects = {
            { type = "unlock-recipe", recipe = "executive-marseline-resin" },
            { type = "unlock-recipe", recipe = "encabuloy-alloy" },
        },
        prerequisites = {"biomineral-synthesis", "stabilized-emulsion-systems", "audit-ready-deliverables"},
        unit = {
            count = 80,
            ingredients = {{"Seared-fish", 1}, {"meal", 1}, {"audit-ready-deliverable", 1}},
            time = 25
        },
        order = "ag-a"
    },
    {
        type = "technology",
        name = "advanced-encabulation-substrates",
        icon = "__tanks_for_bob_fork__/graphics/icons/Placeholder.png",
        icon_size = 64,
        effects = {
            { type = "unlock-recipe", recipe = "hyperphase-matrix" },
            { type = "unlock-recipe", recipe = "retrograde-polymer-sheet" },
            { type = "unlock-recipe", recipe = "duplexed-substrate" },
        },
        prerequisites = {"pre-encabulation-materials", "ionic-phase-conditioning", "stakeholder-review-process"},
        unit = {
            count = 100,
            ingredients = {{"Seared-fish", 1}, {"meal", 1}, {"stakeholder-review-summary", 1}},
            time = 30
        },
        order = "ag-b"
    },
    {
        type = "technology",
        name = "alumated-plate-research",
        icon = "__tanks_for_bob_fork__/graphics/icons/Alumatedplate.png",
        icon_size = 64,
        effects = {
            { type = "unlock-recipe", recipe = "Alumatedplate" },
        },
        prerequisites = {"pre-encabulation-materials", "compliance-packetization"},
        unit = {
            count = 80,
            ingredients = {{"Seared-fish", 1}, {"meal", 1}, {"compliance-packet", 1}},
            time = 20
        },
        order = "ag-c"
    },
    {
        type = "technology",
        name = "tank-casing-research",
        icon = "__tanks_for_bob_fork__/graphics/icons/casing.png",
        icon_size = 64,
        effects = {
            { type = "unlock-recipe", recipe = "tank-ammo-casing" },
            { type = "unlock-recipe", recipe = "tank-ammo-reinforced-casing" },
        },
        prerequisites = {"alumated-plate-research", "risk-assessed-authorization"},
        unit = {
            count = 85,
            ingredients = {{"Seared-fish", 1}, {"meal", 1}, {"risk-assessed-work-order", 1}},
            time = 20
        },
        order = "ag-d"
    },


    {
        type = "technology",
        name = "encabulator-support-componentry",
        icon = "__tanks_for_bob_fork__/graphics/icons/Hydrocoptic-marselvanes.png",
        icon_size = 64,
        effects = {
            { type = "unlock-recipe", recipe = "Hydrocoptic-marselvanes" },
            { type = "unlock-recipe", recipe = "PhaseDetractor" },
            { type = "unlock-recipe", recipe = "Cradinal-grametter" },
        },
        prerequisites = {"biomineral-synthesis", "stabilized-emulsion-systems", "compliance-packetization"},
        unit = {
            count = 90,
            ingredients = {{"Seared-fish", 1}, {"meal", 1}, {"compliance-packet", 1}},
            time = 20
        },
        order = "ag-e"
    },

-- =========================================================
-- ENCABULATOR DEVICE FAMILY LADDER
-- Each major device level is separated into its own research node.
-- =========================================================
    {
        type = "technology",
        name = "retro-encabulator-research",
        icon = "__tanks_for_bob_fork__/graphics/icons/Retro-Encabulator.png",
        icon_size = 64,
        effects = {
            { type = "unlock-recipe", recipe = "Retro-Encabulator" },
        },
        prerequisites = {"advanced-encabulation-substrates", "encabulator-support-componentry", "compliance-packetization"},
        unit = {
            count = 100,
            ingredients = {{"Seared-fish", 1}, {"meal", 1}, {"compliance-packet", 1}},
            time = 25
        },
        order = "ah-a"
    },
    {
        type = "technology",
        name = "Encabulation-research",
        icon = "__tanks_for_bob_fork__/graphics/icons/Encabulator.png",
        icon_size = 64,
        effects = {
            { type = "unlock-recipe", recipe = "Encabulator" },
        },
        prerequisites = {"retro-encabulator-research", "alumated-plate-research", "audit-ready-deliverables"},
        unit = {
            count = 125,
            ingredients = {{"Seared-fish", 1}, {"meal", 1}, {"audit-ready-deliverable", 1}},
            time = 25
        },
        ignore_tech_cost_multiplier = true,
        order = "ah-b"
    },
    {
        type = "technology",
        name = "Turbo-Encabulation-research",
        icon = "__tanks_for_bob_fork__/graphics/icons/TurboEncabulator.png",
        icon_size = 64,
        effects = {
            { type = "unlock-recipe", recipe = "TurboEncabulator" },
        },
        prerequisites = {"Encabulation-research", "stabilized-emulsion-systems", "stakeholder-review-process"},
        unit = {
            count = 150,
            ingredients = {{"Seared-fish", 1}, {"meal", 1}, {"stakeholder-review-summary", 1}},
            time = 30
        },
        order = "ah-c"
    },
    {
        type = "technology",
        name = "Hyper-Encabulation-research",
        icon = "__tanks_for_bob_fork__/graphics/icons/HyperEncabulator.png",
        icon_size = 64,
        effects = {
            { type = "unlock-recipe", recipe = "HyperEncabulator" },
        },
        prerequisites = {"Turbo-Encabulation-research", "advanced-encabulation-substrates", "liability-containment"},
        unit = {
            count = 175,
            ingredients = {{"Seared-fish", 1}, {"meal", 1}, {"liability-contained-report", 1}},
            time = 35
        },
        ignore_tech_cost_multiplier = true,
        order = "ah-d"
    },
    {
        type = "technology",
        name = "framulated-encabulator-research",
        icon = "__tanks_for_bob_fork__/graphics/icons/FramulatedEncabulator.png",
        icon_size = 64,
        effects = {
            { type = "unlock-recipe", recipe = "FramulatedEncabulator" },
        },
        prerequisites = {"Hyper-Encabulation-research", "alumated-plate-research", "board-review-procedure"},
        unit = {
            count = 200,
            ingredients = {{"Seared-fish", 1}, {"meal", 1}, {"board-review-docket", 1}},
            time = 40
        },
        ignore_tech_cost_multiplier = true,
        order = "ah-e"
    },

-- =========================================================
-- SPERVING ARM DEVICE FAMILY LADDER
-- Each Sperving Arm level now has a matching recipe prototype.
-- =========================================================

    {
        type = "technology",
        name = "sperving-arm-research",
        icon = "__tanks_for_bob_fork__/graphics/icons/SpervingArm.png",
        icon_size = 64,
        effects = {
            { type = "unlock-recipe", recipe = "SpervingArm" },
        },
        prerequisites = {"Encabulation-research", "encabulator-support-componentry", "audit-ready-deliverables"},
        unit = {
            count = 100,
            ingredients = {{"Seared-fish", 1}, {"meal", 1}, {"audit-ready-deliverable", 1}},
            time = 25
        },
        order = "ai-a"
    },
    {
        type = "technology",
        name = "ducted-sperving-arm-research",
        icon = "__tanks_for_bob_fork__/graphics/icons/DuctedSpervingArm.png",
        icon_size = 64,
        effects = {
            { type = "unlock-recipe", recipe = "DuctedSpervingArm" },
        },
        prerequisites = {"sperving-arm-research", "Encabulation-research", "stabilized-emulsion-systems", "stakeholder-review-process"},
        unit = {
            count = 125,
            ingredients = {{"Seared-fish", 1}, {"meal", 1}, {"stakeholder-review-summary", 1}},
            time = 30
        },
        order = "ai-b"
    },

    {
        type = "technology",
        name = "duplexed-sperving-arm-research",
        icon = "__tanks_for_bob_fork__/graphics/icons/DuplexedSpervingArm.png",
        icon_size = 64,
        effects = {
            { type = "unlock-recipe", recipe = "DuplexedSpervingArm" },
        },
        prerequisites = {"ducted-sperving-arm-research", "Hyper-Encabulation-research", "liability-containment"},
        unit = {
            count = 175,
            ingredients = {{"Seared-fish", 1}, {"meal", 1}, {"liability-contained-report", 1}},
            time = 35
        },
        order = "ai-c"
    },

-- =========================================================
-- ENCABULATED EXPLOSIVES, BYPRODUCT RECOVERY, AND INDUSTRIAL SUPPORT
-- =========================================================
    {
        type = "technology",
        name = "organic-explosives",
        icon = "__tanks_for_bob_fork__/graphics/icons/universal-explosive.png",
        icon_size = 64,
        effects = {
            { type = "unlock-recipe", recipe = "tank-ammo-universal-explosive-synthetic" },
            { type = "unlock-recipe", recipe = "tank-ammo-explosive-synthetic" },
            { type = "unlock-recipe", recipe = "tank-ammo-ecozone" },
        },
        prerequisites = {"stabilized-emulsion-systems", "tank-casing-research", "evaluation-submission"},
        unit = {
            count = 100,
            ingredients = {{"Seared-fish", 1}, {"meal", 1}, {"submitted-evaluation", 1}},
            time = 20
        },
        order = "aj-a"
    },
    {
        type = "technology",
        name = "explosive-encabulation-engineering",
        icon = "__tanks_for_bob_fork__/graphics/icons/universal-explosive.png",
        icon_size = 64,
        effects = {
            { type = "unlock-recipe", recipe = "tank-ammo-universal-explosive" },
            { type = "unlock-recipe", recipe = "tank-ammo-Explosive-Engineering" },
        },
        prerequisites = {"Turbo-Encabulation-research", "organic-explosives", "stakeholder-review-process"},
        unit = {
            count = 125,
            ingredients = {{"Seared-fish", 1}, {"meal", 1}, {"stakeholder-review-summary", 1}},
            time = 25
        },
        order = "aj-b"
    },
    {
        type = "technology",
        name = "industrial-coke-processing",
        icon = "__tanks_for_bob_fork__/graphics/icons/universal-explosive.png",
        icon_size = 64,
        effects = {
            { type = "unlock-recipe", recipe = "tank-ammo-industrial-coke" },
            { type = "unlock-recipe", recipe = "Rubberized-timber" },
        },
        prerequisites = {"Hyper-Encabulation-research", "explosive-encabulation-engineering", "liability-containment"},
        unit = {
            count = 150,
            ingredients = {{"Seared-fish", 1}, {"meal", 1}, {"liability-contained-report", 1}},
            time = 30
        },
        order = "aj-c"
    },
    {
        type = "technology",
        name = "encabulated-waste-recovery",
        icon = "__tanks_for_bob_fork__/graphics/icons/Radioactivewaste.png",
        icon_size = 64,
        effects = {
            { type = "unlock-recipe", recipe = "ore-from-waste" },
            { type = "unlock-recipe", recipe = "ore-from-wasteb" },
            { type = "unlock-recipe", recipe = "ore-from-waster" },
            { type = "unlock-recipe", recipe = "tank-ammo-Reprocessing" },
        },
        prerequisites = {"ducted-sperving-arm-research", "tank-casing-research", "waste-processing-3", "liability-containment"},
        unit = {
            count = 150,
            ingredients = {{"Seared-fish", 1}, {"meal", 1}, {"liability-contained-report", 1}},
            time = 30
        },
        order = "aj-d"
    },
    {
        type = "technology",
        name = "waste-processing-4-authorization",
        icon = "__tanks_for_bob_fork__/graphics/icons/stakeholder-review-summary.png",
        icon_size = 64,
        effects = {},
        prerequisites = {"waste-processing-3", "Turbo-Encabulation-research", "stakeholder-review-process"},
        unit = {
            count = 75,
            ingredients = {{"meal", 1}, {"stakeholder-review-summary", 1}},
            time = 20
        },
        order = "aj-d1"
    },

    {
        type = "technology",
        name = "waste-processing-4",
        icon = "__tanks_for_bob_fork__/graphics/icons/Radioactivewaste.png",
        icon_size = 64,
        effects = {
            { type = "unlock-recipe", recipe = "Calcifier-pro-4" },
            { type = "unlock-recipe", recipe = "shaler5" },
            { type = "unlock-recipe", recipe = "radio-refine-4" },
        },
        prerequisites = {"waste-processing-3", "Turbo-Encabulation-research", "waste-processing-4-authorization"},
        unit = {
            count = 75,
            ingredients = {{"automation-science-pack", 1}, {"logistic-science-pack", 1}},
            time = 20
        },
        order = "aj-e"
    },
    {
        type = "technology",
        name = "waste-processing-5-authorization",
        icon = "__tanks_for_bob_fork__/graphics/icons/board-advisory-risk-assessment.png",
        icon_size = 64,
        effects = {},
        prerequisites = {"waste-processing-4", "Hyper-Encabulation-research", "super-tank-research", "board-advisory-risk-assessment"},
        unit = {
            count = 100,
            ingredients = {{"meal", 1}, {"board-advisory-risk-assessment", 1}},
            time = 30
        },
        order = "aj-e1"
    },

    {
        type = "technology",
        name = "waste-processing-5",
        icon = "__tanks_for_bob_fork__/graphics/icons/Radioactivewaste.png",
        icon_size = 64,
        effects = {
            { type = "unlock-recipe", recipe = "Calcifier-pro-5" },
            { type = "unlock-recipe", recipe = "shaler6" },
            { type = "unlock-recipe", recipe = "radio-refine-5" },
        },
        prerequisites = {"waste-processing-4", "Hyper-Encabulation-research", "super-tank-research", "waste-processing-5-authorization"},
        unit = {
            count = 100,
            ingredients = {{"automation-science-pack", 2}, {"logistic-science-pack", 2}, {"military-science-pack", 2}},
            time = 30
        },
        ignore_tech_cost_multiplier = true,
        order = "aj-f"
    },

-- =========================================================
-- DEVICE INTEGRATION INTO TANK TECHNOLOGY
-- =========================================================
    {
        type = "technology",
        name = "encabulated-device-integration-authorization",
        icon = "__tanks_for_bob_fork__/graphics/icons/board-review-docket.png",
        icon_size = 64,
        effects = {},
        prerequisites = {"framulated-encabulator-research", "duplexed-sperving-arm-research", "explosive-encabulation-engineering", "board-review-procedure"},
        unit = {
            count = 200,
            ingredients = {{"meal", 1}, {"board-review-docket", 1}},
            time = 45
        },
        order = "ak-a0"
    },

    {
        type = "technology",
        name = "encabulated-device-integration",
        icon = "__tanks_for_bob_fork__/graphics/icons/tank-ammo-assembling-machine.png",
        icon_size = 64,
        effects = {
            { type = "unlock-recipe", recipe = "tank-ammo-assembling-machine" },
            { type = "unlock-recipe", recipe = "tank-assembling-machine" },
        },
        prerequisites = {"encabulated-device-integration-authorization"},
        unit = {
            count = 200,
            ingredients = {{"automation-science-pack", 1}, {"logistic-science-pack", 1}},
            time = 45
        },
        ignore_tech_cost_multiplier = true,
        order = "ak-a"
    },
    {
        type = "technology",
        name = "modular-tank-research-authorization",
        icon = "__tanks_for_bob_fork__/graphics/icons/board-review-docket.png",
        icon_size = 64,
        effects = {},
        prerequisites = {"encabulated-device-integration", "board-review-procedure"},
        unit = {
            count = 80,
            ingredients = {{"meal", 1}, {"board-review-docket", 1}},
            time = 45
        },
        order = "ak-b0"
    },

    {
        type = "technology",
        name = "modular-tank-research",
        icon = "__tanks_for_bob_fork__/graphics/icons/modular-tank-research.png",
        icon_size = 64,
        effects = {
            { type = "unlock-recipe", recipe = "flame-thrower-ammo-tanker" },
            { type = "unlock-recipe", recipe = "flame-thrower-ammo-tanker-2" },
            { type = "unlock-recipe", recipe = "45mm-auto" },
            { type = "unlock-recipe", recipe = "50mm-mortar" },
            { type = "unlock-recipe", recipe = "cannon-shell-2" },
            { type = "unlock-recipe", recipe = "cannon-shell-convert" },
            { type = "unlock-recipe", recipe = "flame-tank" },
            { type = "unlock-recipe", recipe = "auto-tank" },
            { type = "unlock-recipe", recipe = "nade-tank" },
            { type = "unlock-recipe", recipe = "car-flamer" },
        },
        prerequisites = {"tank", "modular-tank-research-authorization"},
        unit = {
            count = 40,
            ingredients = {{"automation-science-pack", 2}, {"logistic-science-pack", 2}, {"military-science-pack", 3}},
            time = 105
        },
        ignore_tech_cost_multiplier = true,
        order = "ak-b"
    },
    {
        type = "technology",
        name = "modular-tank-research2-authorization",
        icon = "__tanks_for_bob_fork__/graphics/icons/liability-contained-report.png",
        icon_size = 64,
        effects = {},
        prerequisites = {"modular-tank-research", "liability-containment"},
        unit = {
            count = 90,
            ingredients = {{"meal", 1}, {"liability-contained-report", 1}},
            time = 45
        },
        order = "ak-c0"
    },

    {
        type = "technology",
        name = "modular-tank-research2",
        icon = "__tanks_for_bob_fork__/graphics/icons/modular-tank-research.png",
        icon_size = 64,
        effects = {
            { type = "unlock-recipe", recipe = "tank-light-chasis-wlsk" },
            { type = "unlock-recipe", recipe = "flame-tank-wlsk" },
            { type = "unlock-recipe", recipe = "auto-tank-wlsk" },
            { type = "unlock-recipe", recipe = "nade-tank-wlsk" },
        },
        prerequisites = {"automation-2", "modular-tank-research2-authorization"},
        unit = {
            count = 40,
            ingredients = {{"automation-science-pack", 3}, {"logistic-science-pack", 3}, {"military-science-pack", 3}},
            time = 105
        },
        ignore_tech_cost_multiplier = true,
        order = "ak-c"
    },
    {
        type = "technology",
        name = "modular-tank-research3-authorization",
        icon = "__tanks_for_bob_fork__/graphics/icons/liability-contained-report.png",
        icon_size = 64,
        effects = {},
        prerequisites = {"modular-tank-research", "liability-containment"},
        unit = {
            count = 90,
            ingredients = {{"meal", 1}, {"liability-contained-report", 1}},
            time = 45
        },
        order = "ak-d0"
    },

    {
        type = "technology",
        name = "modular-tank-research3",
        icon = "__tanks_for_bob_fork__/graphics/icons/modular-tank-research.png",
        icon_size = 64,
        effects = {
            { type = "unlock-recipe", recipe = "mine-tank" },
            { type = "unlock-recipe", recipe = "minepack" },
            { type = "unlock-recipe", recipe = "rocket-tank" },
            { type = "unlock-recipe", recipe = "rocketpack" },
        },
        prerequisites = {"land-mine", "explosive-rocketry", "modular-tank-research3-authorization"},
        unit = {
            count = 40,
            ingredients = {{"automation-science-pack", 3}, {"logistic-science-pack", 3}, {"military-science-pack", 3}},
            time = 105
        },
        ignore_tech_cost_multiplier = true,
        order = "ak-d"
    },
    {
        type = "technology",
        name = "mechanized-infantry-authorization",
        icon = "__tanks_for_bob_fork__/graphics/icons/risk-assessed-work-order.png",
        icon_size = 64,
        effects = {},
        prerequisites = {"modular-tank-research", "risk-assessed-authorization"},
        unit = {
            count = 60,
            ingredients = {{"meal", 1}, {"risk-assessed-work-order", 1}},
            time = 30
        },
        order = "ak-e0"
    },

    {
        type = "technology",
        name = "mechanized-infantry-research",
        icon = "__tanks_for_bob_fork__/graphics/icons/mech-inf.png",
        icon_size = 64,
        effects = {
            { type = "unlock-recipe", recipe = "fish-kit" },
            { type = "unlock-recipe", recipe = "piercing-shotgun-shell-brick" },
            { type = "unlock-recipe", recipe = "ap-bullet-brick" },
        },
        prerequisites = {"mechanized-infantry-authorization"},
        unit = {
            count = 30,
            ingredients = {{"automation-science-pack", 3}, {"logistic-science-pack", 1}, {"military-science-pack", 1}},
            time = 15
        },
        ignore_tech_cost_multiplier = true,
        order = "ak-e"
    },
    {
        type = "technology",
        name = "new-munitions-authorization",
        icon = "__tanks_for_bob_fork__/graphics/icons/board-review-docket.png",
        icon_size = 64,
        effects = {},
        prerequisites = {"modular-tank-research2", "board-review-procedure"},
        unit = {
            count = 80,
            ingredients = {{"meal", 1}, {"board-review-docket", 1}},
            time = 30
        },
        order = "ak-f0"
    },

    {
        type = "technology",
        name = "new-munitions",
        icon = "__tanks_for_bob_fork__/graphics/icons/chemical-tank-research.png",
        icon_size = 64,
        effects = {
            { type = "unlock-recipe", recipe = "50mm-mortar-poison" },
            { type = "unlock-recipe", recipe = "minepack-poison" },
            { type = "unlock-recipe", recipe = "land-mine-poison" },
        },
        prerequisites = {"modular-tank-research2", "military-3", "new-munitions-authorization"},
        unit = {
            count = 40,
            ingredients = {{"automation-science-pack", 3}, {"logistic-science-pack", 2}, {"military-science-pack", 3}},
            time = 10
        },
        ignore_tech_cost_multiplier = true,
        order = "ak-f"
    },
    {
        type = "technology",
        name = "organic-explosives2-authorization",
        icon = "__tanks_for_bob_fork__/graphics/icons/stakeholder-review-summary.png",
        icon_size = 64,
        effects = {},
        prerequisites = {"modular-tank-research2", "organic-explosives", "stakeholder-review-process"},
        unit = {
            count = 80,
            ingredients = {{"meal", 1}, {"stakeholder-review-summary", 1}},
            time = 30
        },
        order = "ak-g0"
    },

    {
        type = "technology",
        name = "organic-explosives2",
        icon = "__tanks_for_bob_fork__/graphics/icons/universal-explosive.png",
        icon_size = 64,
        effects = {
            { type = "ammo-damage", ammo_category = "tank-nade-ammo", modifier = 0.2 },
            { type = "gun-speed", ammo_category = "tank-nade-ammo", modifier = 0.2 },
            { type = "ammo-damage", ammo_category = "tank-rocket-ammo", modifier = 0.2 },
            { type = "gun-speed", ammo_category = "tank-rocket-ammo", modifier = 0.2 },
        },
        prerequisites = {"modular-tank-research2", "organic-explosives", "organic-explosives2-authorization"},
        unit = {
            count = 40,
            ingredients = {{"automation-science-pack", 1}, {"logistic-science-pack", 1}, {"military-science-pack", 1}},
            time = 150
        },
        ignore_tech_cost_multiplier = true,
        order = "ak-g"
    },
    {
        type = "technology",
        name = "organic-explosives3-authorization",
        icon = "__tanks_for_bob_fork__/graphics/icons/board-review-docket.png",
        icon_size = 64,
        effects = {},
        prerequisites = {"modular-tank-research2", "organic-explosives2", "board-review-procedure"},
        unit = {
            count = 100,
            ingredients = {{"meal", 1}, {"board-review-docket", 1}},
            time = 40
        },
        order = "ak-h0"
    },

    {
        type = "technology",
        name = "organic-explosives3",
        icon = "__tanks_for_bob_fork__/graphics/icons/universal-explosive.png",
        icon_size = 64,
        effects = {
            { type = "ammo-damage", ammo_category = "tank-wmd-ammo", modifier = 0.2 },
            { type = "ammo-damage", ammo_category = "tank-nade-ammo", modifier = 0.2 },
            { type = "ammo-damage", ammo_category = "tank-rocket-ammo", modifier = 0.2 },
        },
        prerequisites = {"modular-tank-research2", "organic-explosives2", "organic-explosives3-authorization"},
        unit = {
            count = 40,
            ingredients = {{"automation-science-pack", 1}, {"logistic-science-pack", 1}, {"military-science-pack", 1}},
            time = 150
        },
        ignore_tech_cost_multiplier = true,
        order = "ak-h"
    },
    {
        type = "technology",
        name = "super-tank-authorization",
        icon = "__tanks_for_bob_fork__/graphics/icons/board-advisory-risk-assessment.png",
        icon_size = 64,
        effects = {},
        prerequisites = {"modular-tank-research2", "encabulated-waste-recovery", "board-advisory-risk-assessment"},
        unit = {
            count = 125,
            ingredients = {{"meal", 1}, {"board-advisory-risk-assessment", 1}},
            time = 45
        },
        order = "ak-i0"
    },

    {
        type = "technology",
        name = "super-tank-research",
        icon = "__tanks_for_bob_fork__/graphics/icons/super-tank-research.png",
        icon_size = 64,
        effects = {
            { type = "unlock-recipe", recipe = "super-tank" },
            { type = "unlock-recipe", recipe = "super-tank-alternate" },
        },
        prerequisites = {"modular-tank-research2", "military-3", "encabulated-waste-recovery", "super-tank-authorization"},
        unit = {
            count = 50,
            ingredients = {{"automation-science-pack", 5}, {"logistic-science-pack", 2}, {"military-science-pack", 6}},
            time = 10
        },
        order = "ak-i"
    },
    {
        type = "technology",
        name = "super-tank-wmd-authorization",
        icon = "__tanks_for_bob_fork__/graphics/icons/board-advisory-risk-assessment.png",
        icon_size = 64,
        effects = {},
        prerequisites = {"super-tank-research", "new-munitions", "board-advisory-risk-assessment"},
        unit = {
            count = 175,
            ingredients = {{"meal", 1}, {"board-advisory-risk-assessment", 2}},
            time = 60
        },
        order = "ak-j0"
    },

    {
        type = "technology",
        name = "super-tank-research2",
        icon = "__tanks_for_bob_fork__/graphics/icons/super-tank-research.png",
        icon_size = 64,
        effects = {
            { type = "unlock-recipe", recipe = "super-tank-wmd" },
            { type = "unlock-recipe", recipe = "tank-wmd-ammo" },
            { type = "unlock-recipe", recipe = "wmdartillery-ammo" },
        },
        prerequisites = {"super-tank-research", "new-munitions", "super-tank-wmd-authorization"},
        unit = {
            count = 100,
            ingredients = {{"automation-science-pack", 12}, {"logistic-science-pack", 6}, {"military-science-pack", 6}},
            time = 15
        },
        ignore_tech_cost_multiplier = true,
        order = "ak-j"
    },
})
