data:extend(
{
-- tank-cannon-2
  {
    type = "gun",
    name = "tank-cannon-2",
    icon = "__base__/graphics/icons/tank-cannon.png",
    icon_size = 64,
    flags = {"hidden"},
    subgroup = "gun",
    order = "z[tank]-a[cannon]",
    attack_parameters =
    {
      type = "projectile",
      ammo_category = "cannon-shell",
      cooldown = 80,
      movement_slow_down_factor = 0,
      projectile_creation_distance = 0.6,
      range = 55,
      sound =
      {
        {
          filename = "__base__/sound/fight/tank-cannon.ogg",
          volume = 0.3
        }
      }
    },
    stack_size = 5
  },
--tank-flamer
  {
    type = "gun",
    name = "tank-flamer",
    icon = "__base__/graphics/icons/flamethrower.png",
    icon_size = 64,

    subgroup = "gun",
    order = "e[flame-thrower]",
    attack_parameters =
    {
  		type = "projectile",
  		ammo_category = "tank-spray-ammo",
  		cooldown = 1,
  		movement_slow_down_factor = 0.6,
  		projectile_creation_distance = 3.7,
  		range = 40,

      cyclic_sound =
      {
        begin_sound =
        {
          {
            filename = "__base__/sound/fight/flamethrower-start.ogg",
            volume = 0.7
          }
        },
        middle_sound =
        {
          {
            filename = "__base__/sound/fight/flamethrower-mid.ogg",
            volume = 0.7
          }
        },
        end_sound =
        {
          {
            filename = "__base__/sound/fight/flamethrower-end.ogg",
            volume = 0.7
          }
        }
      }
    },
    stack_size = 1
  },
--tank-flamer-2
  {
    type = "gun",
    name = "tank-flamer-2",
    icon = "__base__/graphics/icons/flamethrower.png",
    icon_size = 64,

    subgroup = "gun",
    order = "e[flame-thrower]",
    attack_parameters =
    {
  		type = "projectile",
  		ammo_category = "tank-spray-ammo-2",
  		cooldown = 3,
  		movement_slow_down_factor = 0.6,
  		projectile_creation_distance = 3.7,
  		range = 40,
      cyclic_sound =
      {
        begin_sound =
        {
          {
            filename = "__base__/sound/fight/flamethrower-start.ogg",
            volume = 0.7
          }
        },
        middle_sound =
        {
          {
            filename = "__base__/sound/fight/flamethrower-mid.ogg",
            volume = 0.7
          }
        },
        end_sound =
        {
          {
            filename = "__base__/sound/fight/flamethrower-end.ogg",
            volume = 0.7
          }
        }
      }
    },
    stack_size = 1
  },
--tank-auto-cannon
	{
    type = "gun",
    name = "tank-auto-cannon",
    icon = "__base__/graphics/icons/tank-cannon.png",
    icon_size = 64,

    subgroup = "gun",
    order = "z[tank]-a[cannon]",
    attack_parameters =
    {
      type = "projectile",
	    ammo_category = "auto-cannon-ammo",
      cooldown = 9,
      movement_slow_down_factor = 0,
      projectile_creation_distance = 3.6,
      range = 55,
      sound =
      {
        {
          filename = "__tanks_for_bob_fork__/sound/fight/auto-cannon.ogg",
          volume = 0.5
        }
      }
    },
    stack_size = 1
    },
--tank-nade-cannon
	{
    type = "gun",
    name = "tank-nade-cannon",
    icon = "__base__/graphics/icons/tank-cannon.png",
    icon_size = 64,

    subgroup = "gun",
    order = "z[tank]-a[cannon]",
    attack_parameters =
    {
      type = "projectile",
	    ammo_category = "tank-nade-ammo",
      cooldown = 50,
      movement_slow_down_factor = 0.2,
      projectile_creation_distance = 3,
      range = 45,
      sound =
      {
        {
          filename = "__tanks_for_bob_fork__/sound/fight/heavy-artillery-3.ogg",
          volume = 1
        }
      }
    },
    stack_size = 1
  },
--tank-artillery
  {
    type = "gun",
    name = "tank-artillery",
    icon = "__base__/graphics/icons/tank-cannon.png",
    icon_size = 64,

    subgroup = "gun",
    order = "z[tank]-a[cannon]",
    attack_parameters =
    {
      type = "beam",
      ammo_category = "tank-nade-ammo",
      cooldown = 50,
      movement_slow_down_factor = 0.2,
      projectile_creation_distance = 3,
      range = 45,
      sound =
      {
        {
          filename = "__tanks_for_bob_fork__/sound/fight/heavy-artillery-3.ogg",
          volume = 1
        }
      }
    },
    stack_size = 1
  },  
--tank-mine-cannon
	{
    type = "gun",
    name = "tank-mine-cannon",
    icon = "__base__/graphics/icons/tank-cannon.png",
    icon_size = 64,

    subgroup = "gun",
    order = "z[tank]-a[cannon]",
    attack_parameters =
    {
      type = "projectile",
	    ammo_category = "tank-mine-ammo",
      cooldown = 30,
      movement_slow_down_factor = 0.2,
      projectile_creation_distance = 3,
      range = 45,
      sound =
      {
        {
          filename = "__base__/sound/fight/tank-cannon.ogg",
          volume = 0.2
        }
      }
    },
    stack_size = 1
    },
--machinegun-array
  {
    type = "gun",
    name = "tank-machinegun-turret",
    icon = "__base__/graphics/icons/submachine-gun.png",
    icon_size = 64,

    subgroup = "gun",
    order = "a[basic-clips]-b[submachine-gun]",
    attack_parameters =
    {
      type = "projectile",
      ammo_category = "bullet",
      cooldown = 6.5,
      movement_slow_down_factor = 2,
      shell_particle =
      {
        name = "shell-particle",
        direction_deviation = 1,
        speed = 0.5,
        speed_deviation = 1,
        center = {0, 0.6},
        creation_distance = 2.9,
        starting_frame_speed = 0.4,
        starting_frame_speed_deviation = 0.1
      },
      projectile_creation_distance = 2.6,
      range = 45,
      sound =
      {
        {
          filename = "__base__/sound/fight/heavy-gunshot-1.ogg",
          volume = 0.2
        }
      }
    },
    stack_size = 1
  },
--tank-wmd-cannon
	{
    type = "gun",
    name = "tank-wmd-cannon",
    icon = "__base__/graphics/icons/tank-cannon.png",
    icon_size = 64,

    subgroup = "gun",
    order = "z[tank]-a[cannon]",
    attack_parameters =
    {
      type = "projectile",
	    ammo_category = "tank-wmd-ammo",
      cooldown = 468,
	  speed = 0.01,
      movement_slow_down_factor = 0.1,
      projectile_creation_distance = 5,
      range = 105,
      sound =
      {
        {
          filename = "__base__/sound/fight/rocket-launcher.ogg",
          volume = 1.5
        }
      }
    },
    stack_size = 1
    },
--tank-rocket-cannon
  {
    type = "gun",
    name = "tank-rocket-cannon",
    icon = "__base__/graphics/icons/rocket-launcher.png",
    icon_size = 64,

    subgroup = "gun",
    order =  "z[tank]-a[cannon]",
    attack_parameters =
    {
      type = "projectile",
	    ammo_category = "tank-rocket-ammo",
      movement_slow_down_factor = 0.3,
      cooldown = 22.5,
      projectile_creation_distance = 1.6,
      range = 105,
	  sound =
      {
        {
          filename = "__base__/sound/fight/rocket-launcher.ogg",
          volume = 1
        }
      }
    },
    stack_size = 1
  },
 }
)
