data:extend(
{  
--shell-brick
	{
    type = "ammo",
    name = "piercing-shotgun-shell-brick",
    icon = "__tanks_for_bob_fork__/graphics/icons/shell-brick.png",
    icon_size = 64,

    ammo_type =
    {
      category = "shotgun-shell",
      target_type = "direction",
      source_effects =
      {
        type = "create-entity",
        entity_name = "explosion-gunshot"
      },
      action =
      {
        type = "direct",
        repeat_count = 12,
        action_delivery =
        {
          type = "projectile",
          projectile = "piercing-shotgun-pellet-2",
          starting_speed = 1,
          direction_deviation = 1,
		  speed_deviation = 0.6,
          range_deviation = 0.6,
          max_range = 25,
        }
      }
    },
    magazine_size = 25,
    subgroup = "tank-ammo-infantry",
    order = "b[tank-ammo]",
    stack_size = 50
  },
--bullet-brick
	{
    type = "ammo",
    name = "ap-bullet-brick",
    icon = "__tanks_for_bob_fork__/graphics/icons/bullet-brick.png",
    icon_size = 64,

    ammo_type =
    {
      category = "bullet",
      action =
      {
        type = "direct",
        action_delivery =
        {
          type = "instant",
          source_effects =
          {
              type = "create-entity",
              entity_name = "explosion-gunshot"
          },
          target_effects =
          {
            {
              type = "create-entity",
              entity_name = "explosion-gunshot"
            },
            {
              type = "damage",
              damage = { amount = 15 , type = "physical"}
            }
          }
        }
      }
    },
    magazine_size = 100,
    subgroup = "tank-ammo-infantry",
    order = "b[tank-ammo]",
    stack_size = 50
  },
--flame-thrower-ammo-tanker
	{
    type = "ammo",
    name = "flame-thrower-ammo-tanker",
    icon = "__tanks_for_bob_fork__/graphics/icons/flame-thrower-ammo-tanker.png",
    icon_size = 64,

    ammo_type =
    {
      category = "tank-spray-ammo",
      target_type = "direction",
      action =
      {
        type = "direct",
        action_delivery =
        {
    			{
    				type = "flame-thrower",
    				explosion = "tank-flame-thrower-explosion",
    				direction_deviation = 0.15,
    				speed_deviation = 0.4,
    				starting_frame_deviation = 0.07,
    				projectile_starting_speed = 0.5,
    				starting_distance = 0.6,
    			},	
        }
      }
    },
    magazine_size = 200,
    subgroup = "tank-ammo",
    order = "b[tank-ammo]",
    stack_size = 10
  },
--flame-thrower-ammo-tanker-2
	{
    type = "ammo",
    name = "flame-thrower-ammo-tanker-2",
    icon = "__tanks_for_bob_fork__/graphics/icons/flame-thrower-ammo-tanker.png",
    icon_size = 64,

    ammo_type =
    {
      category = "tank-spray-ammo-2",
      target_type = "direction",
      action =
      {
        type = "direct",
        action_delivery =
        {
    			{
    				type = "flame-thrower",
    				explosion = "tank-flame-thrower-explosion",
    				direction_deviation = 0.5,
    				speed_deviation = 0.1,
    				starting_frame_deviation = 0.07,
    				projectile_starting_speed = 0.4,
    				starting_distance = 0.7,
    			},	
    			{
    				type = "flame-thrower",
    				explosion = "tank-flame-thrower-explosion",
    				direction_deviation = 0.5,
    				speed_deviation = 0.1,
    				starting_frame_deviation = 0.07,
    				projectile_starting_speed = 0.4,
    				starting_distance = 0.7,
    			},	
    			{
    				type = "flame-thrower",
    				explosion = "tank-flame-thrower-explosion",
    				direction_deviation = 0.5,
    				speed_deviation = 0.1,
    				starting_frame_deviation = 0.07,
    				projectile_starting_speed = 0.3,
    				starting_distance = 0.3,
    			},	
    			{
    				type = "flame-thrower",
    				explosion = "tank-flame-thrower-explosion",
    				direction_deviation = 0.5,
    				speed_deviation = 0.3,
    				starting_frame_deviation = 0.07,
    				projectile_starting_speed = 0.3,
    				starting_distance = 0.6,
    			},	
    			{
    				type = "flame-thrower",
    				explosion = "tank-flame-thrower-explosion",
    				direction_deviation = 0.5,
    				speed_deviation = 0.1,
    				starting_frame_deviation = 0.07,
    				projectile_starting_speed = 0.2,
    				starting_distance = 0.9,
    			},	
    			{
    				type = "flame-thrower",
    				explosion = "tank-flame-thrower-explosion",
    				direction_deviation = 0.5,
    				speed_deviation = 0.1,
    				starting_frame_deviation = 0.07,
    				projectile_starting_speed = 0.2,
    				starting_distance = 0.9,
    			},	
        }
      }
    },
    magazine_size = 300,
    subgroup = "tank-ammo",
    order = "b[tank-ammo]",
    stack_size = 10
  },
--"45mm-auto"
	{
    type = "ammo",
    name = "45mm-auto",
    icon = "__tanks_for_bob_fork__/graphics/icons/cannon-auto-ammo.png",
    icon_size = 64,

    ammo_type =
    {
      category = "auto-cannon-ammo",
      target_type = "direction",
      source_effects =
      {
        type = "create-entity",
        entity_name = "explosion-gunshot"
      },
      action =
      {
        type = "direct",
        action_delivery =
        {
          type = "projectile",
          projectile = "45mm-projectile",
          starting_speed = 3,
          direction_deviation = 0.1,
		  speed_deviation = 0.1,
          range_deviation = 0.1,
          max_range = 75
        }
      },
    },
    magazine_size = 12,
    subgroup = "tank-ammo",
    order = "a[tank-ammo]",
    stack_size = 100
  },
--50mm-mortar
	{
    type = "ammo",
    name = "50mm-mortar",
    icon = "__tanks_for_bob_fork__/graphics/icons/nade_tank_ammo.png",
    icon_size = 64,

    ammo_type =
    {
      category = "tank-nade-ammo",
      target_type = "direction",
      source_effects =
      {
        type = "create-entity",
        entity_name = "explosion-gunshot"
      },
      action =
      {
        type = "direct",
        action_delivery =
        {
          {
            type = "projectile",
            projectile = "50mm-projectile",
            starting_speed = 0.3,
            direction_deviation = 0.5,
			speed_deviation = 0.5,
            range_deviation = 0.1,
            max_range = 90.
          },
          {
            type = "projectile",
            projectile = "50mm-projectile",
            starting_speed = 0.3,
            direction_deviation = 0.4,
			speed_deviation = 0.4,
            range_deviation = 0.2,
            max_range = 90.
          },
          {
            type = "projectile",
            projectile = "50mm-projectile",
            starting_speed = 0.3,
            direction_deviation = 0.3,
			speed_deviation = 0.3,
            range_deviation = 0.3,
            max_range = 90.
          },
          {
            type = "projectile",
            projectile = "50mm-projectile",
            starting_speed = 0.3,
            direction_deviation = 0.2,
			speed_deviation = 0.2,
            range_deviation = 0.4,
            max_range = 90.
          },
          {
            type = "projectile",
            projectile = "50mm-projectile",
            starting_speed = 0.3,
            direction_deviation = 0.1,
			speed_deviation = 0.1,
            range_deviation = 0.5,
            max_range = 90.
          }
        }
      },

    },
    magazine_size = 1,
    subgroup = "tank-ammo",
    order = "a[tank-ammo]",
    stack_size = 5
  },
--50mm-mortar-poison
	{
    type = "ammo",
    name = "50mm-mortar-poison",
    icon = "__tanks_for_bob_fork__/graphics/icons/nade_tank_ammo-poison.png",
    icon_size = 64,

    ammo_type =
    {
      category = "tank-nade-ammo",
      target_type = "direction",
      source_effects =
      {
        type = "create-entity",
        entity_name = "explosion-gunshot"
      },
      action =
      {
        type = "direct",
        action_delivery =
        {
          type = "projectile",
          projectile = "50mm-projectile-poison",
          starting_speed = 1,
          direction_deviation = 0.5,
		  speed_deviation = 0.5,
          range_deviation = 0.5,
          max_range = 90
        }
      },
    },
    magazine_size = 1,
    subgroup = "tank-ammo",
    order = "a[tank-ammo]",
    stack_size = 5
  },
--minepack
	{
    type = "ammo",
    name = "minepack",
    icon = "__tanks_for_bob_fork__/graphics/icons/mine-pack.png",
    icon_size = 64,

    ammo_type =
    {
      category = "tank-mine-ammo",
      target_type = "direction",
      source_effects =
      {
        type = "create-entity",
        entity_name = "explosion-gunshot"
      },
      action =
      {
        type = "direct",
        action_delivery =
        {
          type = "projectile",
          projectile = "tank-mine-projectile",
          starting_speed = 1,
          direction_deviation = 0.1,
          range_deviation = 0.1,
          max_range = 50
        }
      },
    },
    magazine_size = 10,
    subgroup = "tank-ammo",
    order = "a[tank-ammo]",
    stack_size = 10
  },
--minepack-poison
	{
    type = "ammo",
    name = "minepack-poison",
    icon = "__tanks_for_bob_fork__/graphics/icons/mine-pack-poison.png",
    icon_size = 64,

    ammo_type =
    {
      category = "tank-mine-ammo",
      target_type = "direction",
      source_effects =
      {
        type = "create-entity",
        entity_name = "explosion-gunshot"
      },
      action =
      {
        type = "direct",
        action_delivery =
        {
          type = "projectile",
          projectile = "tank-mine-projectile-poison",
          starting_speed = 1,
          direction_deviation = 1,
		  speed_deviation = 0.5,
          range_deviation = 1,
          max_range = 50
        }
      },
    },
    magazine_size = 10,
    subgroup = "tank-ammo",
    order = "a[tank-ammo]",
    stack_size = 10
  },
--rocketpack
  	{
    type = "ammo",
    name = "rocketpack",
    icon = "__tanks_for_bob_fork__/graphics/icons/rocket-pack.png",
    icon_size = 64,

    ammo_type =
    {
      category = "tank-rocket-ammo",
      action =
      {
        type = "direct",
        action_delivery =
        {
          type = "projectile",
          projectile = "tank-rocket",
          starting_speed = 0.1,
		  speed_deviation = 0.5,
		  direction_deviation = 1.0,
          range_deviation = 0.95,
          source_effects =
          {
            type = "create-entity",
            entity_name = "grenade-explosion"
          }
        }
      }
    },
    magazine_size = 4,
	 subgroup = "tank-ammo",
    order = "a[tank-ammo]",
    stack_size = 15
  },
--cannon-shell-2
  {
    type = "ammo",
    name = "cannon-shell-2",
    icon = "__tanks_for_bob_fork__/graphics/icons/tank-ammo-shell2.png",
    icon_size = 64,

    ammo_type =
    {
      category = "cannon-shell",
      target_type = "direction",
      source_effects =
      {
        type = "create-entity",
        entity_name = "medium-explosion"
      },
      action =
      {
        type = "direct",
        action_delivery =
        {
          type = "projectile",
          projectile = "cannon-projectile-2",
          starting_speed = 0.6,
		  speed_deviation = 0.15,
          direction_deviation = 0.1,
          range_deviation = 0.05,
          max_range = 120
        }
      },
    },
    subgroup = "tank-ammo",
    order = "a[tank-ammo]",
    stack_size = 100
  },
  --nuke-artillery-shell2
  {
    type = "ammo",
    name = "wmdartillery-ammo",
    icon = "__tanks_for_bob_fork__/graphics/icons/nuke-artillery-shell2.png",
    icon_size = 64,

    ammo_type =
    {
      category = "artillery-shell",
      target_type = "position",
      source_effects =
      {
        type = "create-entity",
        entity_name = "artillery-cannon-muzzle-flash"
      },
      action =
      {
        type = "direct",
        action_delivery =
        {
          type = "artillery",
          projectile = "wmdartillery-ammo",
          starting_speed = 0.5,
		  speed_deviation = 1.01,
          direction_deviation = 0.11,
          range_deviation = 0.11,
        },
		{
            type = "create-explosion",
            entity_name = "artillery-cannon-muzzle-flash"
          }
      },
    },
    subgroup = "tank-ammo",
    order = "a[tank-ammo]",
    stack_size = 1
  },

 --tank-wmd-ammo
  {
    type = "ammo",
    name = "tank-wmd-ammo",
    icon = "__tanks_for_bob_fork__/graphics/icons/tank-ammo-wmd.png",
    icon_size = 64,

    ammo_type =
    {
      category = "tank-wmd-ammo",
	      subgroup = "tank-ammo-infantry",
      target_type = "direction",
      source_effects =
      {
        type = "create-entity",
        entity_name = "artillery-cannon-muzzle-flash"
      },
      action =
      {
        type = "direct",
        action_delivery =
        {
          type = "projectile",
          projectile = "wmd-projectile",
          starting_speed = 1.5,
		  speed_deviation = 0.15,
          direction_deviation = 0.15,
          range_deviation = 0.15,
          max_range = 105
        }
      },
    },
    subgroup = "tank-ammo",
    order = "a[tank-ammo]",
    stack_size = 1
  },
 }
 )