-- Tank flamethrower stream prototype.
-- The ammo entries below fire the stream named "tank-flame-thrower-explosion".
-- Define it by cloning the vanilla flamethrower stream instead of hardcoding sprite paths.
-- This avoids missing-file crashes such as nonexistent *-spine-shadow.png paths.

local tank_flamer_stream = table.deepcopy(data.raw.stream["flamethrower-fire-stream"])
tank_flamer_stream.name = "tank-flame-thrower-explosion"
tank_flamer_stream.flags = {"not-on-map"}

-- Tank-tuned behavior while preserving all vanilla-valid flame graphics.
tank_flamer_stream.particle_buffer_size = 90
tank_flamer_stream.particle_spawn_interval = 2
tank_flamer_stream.particle_spawn_timeout = 8

-- Damage / ground-fire behavior. Visual fields are deliberately inherited from vanilla.
tank_flamer_stream.action =
{
  type = "direct",
  action_delivery =
  {
    type = "instant",
    target_effects =
    {
      {
        type = "create-fire",
        entity_name = "fire-flame",
        initial_ground_flame_count = 1
      },
      {
        type = "nested-result",
        action =
        {
          type = "area",
          radius = 2.5,
          action_delivery =
          {
            type = "instant",
            target_effects =
            {
              {
                type = "damage",
                damage = {amount = 13, type = "fire"}
              }
            }
          }
        }
      }
    }
  }
}

data:extend({ tank_flamer_stream })

data:extend({
  {
    type = "ammo",
    name = "piercing-shotgun-shell-brick",
    icon = "__tanks_for_bob_fork__/graphics/icons/shell-brick.png",
    icon_size = 64,
    ammo_category = "shotgun-shell",
    ammo_type =
    {
      target_type = "direction",
      source_effects =
      {
        {
          type = "create-entity",
          entity_name = "explosion-gunshot"
        }
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
          max_range = 25
        }
      }
    },
    magazine_size = 25,
    subgroup = "tank-ammo-infantry",
    order = "b[tank-ammo]",
    stack_size = 50
  },

  {
    type = "ammo",
    name = "ap-bullet-brick",
    icon = "__tanks_for_bob_fork__/graphics/icons/bullet-brick.png",
    icon_size = 64,
    ammo_category = "bullet",
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
              type = "create-entity",
              entity_name = "explosion-gunshot"
            }
          },
          target_effects =
          {
            {
              type = "create-entity",
              entity_name = "explosion-gunshot"
            },
            {
              type = "damage",
              damage = {amount = 15, type = "physical"}
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

  {
    type = "ammo",
    name = "flame-thrower-ammo-tanker",
    icon = "__tanks_for_bob_fork__/graphics/icons/flame-thrower-ammo-tanker.png",
    icon_size = 64,
    ammo_category = "tank-spray-ammo",
    ammo_type =
{
  target_type = "direction",
  action =
  {
    type = "direct",
    action_delivery =
    {
      type = "stream",
      stream = "tank-flame-thrower-explosion",
      source_offset = {0, -0.5},
      max_length = 15,
      duration = 160
    }
  }
},
direction_deviation = 1,
          speed_deviation = 0.6,
          range_deviation = 0.6,
          max_range = 25,
    magazine_size = 200,
    subgroup = "tank-ammo",
    order = "b[tank-ammo]",
    stack_size = 10
  },

  {
    type = "ammo",
    name = "flame-thrower-ammo-tanker-2",
    icon = "__tanks_for_bob_fork__/graphics/icons/flame-thrower-ammo-tanker.png",
    icon_size = 64,
    ammo_category = "tank-spray-ammo-2",
    ammo_type =
{
  target_type = "direction",
  action =
  {
    type = "direct",
    action_delivery =
    {
      {
        type = "stream",
        stream = "tank-flame-thrower-explosion",
        source_offset = {0, -0.5},
        max_length = 15,
        duration = 160
      },
      {
        type = "stream",
        stream = "tank-flame-thrower-explosion",
        source_offset = {0, -0.5},
        max_length = 15,
        duration = 160
      },
      {
        type = "stream",
        stream = "tank-flame-thrower-explosion",
        source_offset = {0, -0.25},
        max_length = 12,
        duration = 160
      },
      {
        type = "stream",
        stream = "tank-flame-thrower-explosion",
        source_offset = {0, -0.4},
        max_length = 14,
        duration = 160
      },
      {
        type = "stream",
        stream = "tank-flame-thrower-explosion",
        source_offset = {0, -0.65},
        max_length = 18,
        duration = 160
      },
      {
        type = "stream",
        stream = "tank-flame-thrower-explosion",
        source_offset = {0, -0.65},
        max_length = 18,
        duration = 160
      }
    }
  }
},
direction_deviation = 1,
          speed_deviation = 0.6,
          range_deviation = 0.6,
          max_range = 25,
    magazine_size = 300,
    subgroup = "tank-ammo",
    order = "b[tank-ammo]",
    stack_size = 10
  },

  {
    type = "ammo",
    name = "45mm-auto",
    icon = "__tanks_for_bob_fork__/graphics/icons/cannon-auto-ammo.png",
    icon_size = 64,
    ammo_category = "auto-cannon-ammo",
    ammo_type =
    {
      target_type = "direction",
      source_effects =
      {
        {
          type = "create-entity",
          entity_name = "explosion-gunshot"
        }
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
      }
    },
    magazine_size = 12,
    subgroup = "tank-ammo",
    order = "a[tank-ammo]",
    stack_size = 100
  },

  {
    type = "ammo",
    name = "50mm-mortar",
    icon = "__tanks_for_bob_fork__/graphics/icons/nade_tank_ammo.png",
    icon_size = 64,
    ammo_category = "tank-nade-ammo",
    ammo_type =
    {
      target_type = "direction",
      source_effects =
      {
        {
          type = "create-entity",
          entity_name = "explosion-gunshot"
        }
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
            max_range = 90
          },
          {
            type = "projectile",
            projectile = "50mm-projectile",
            starting_speed = 0.3,
            direction_deviation = 0.4,
            speed_deviation = 0.4,
            range_deviation = 0.2,
            max_range = 90
          },
          {
            type = "projectile",
            projectile = "50mm-projectile",
            starting_speed = 0.3,
            direction_deviation = 0.3,
            speed_deviation = 0.3,
            range_deviation = 0.3,
            max_range = 90
          },
          {
            type = "projectile",
            projectile = "50mm-projectile",
            starting_speed = 0.3,
            direction_deviation = 0.2,
            speed_deviation = 0.2,
            range_deviation = 0.4,
            max_range = 90
          },
          {
            type = "projectile",
            projectile = "50mm-projectile",
            starting_speed = 0.3,
            direction_deviation = 0.1,
            speed_deviation = 0.1,
            range_deviation = 0.5,
            max_range = 90
          }
        }
      }
    },
    magazine_size = 1,
    subgroup = "tank-ammo",
    order = "a[tank-ammo]",
    stack_size = 5
  },

  {
    type = "ammo",
    name = "50mm-mortar-poison",
    icon = "__tanks_for_bob_fork__/graphics/icons/nade_tank_ammo-poison.png",
    icon_size = 64,
    ammo_category = "tank-nade-ammo",
    ammo_type =
    {
      target_type = "direction",
      source_effects =
      {
        {
          type = "create-entity",
          entity_name = "explosion-gunshot"
        }
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
      }
    },
    magazine_size = 1,
    subgroup = "tank-ammo",
    order = "a[tank-ammo]",
    stack_size = 5
  },

  {
    type = "ammo",
    name = "minepack",
    icon = "__tanks_for_bob_fork__/graphics/icons/mine-pack.png",
    icon_size = 64,
    ammo_category = "tank-mine-ammo",
    ammo_type =
    {
      target_type = "direction",
      source_effects =
      {
        {
          type = "create-entity",
          entity_name = "explosion-gunshot"
        }
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
      }
    },
    magazine_size = 10,
    subgroup = "tank-ammo",
    order = "a[tank-ammo]",
    stack_size = 10
  },

  {
    type = "ammo",
    name = "minepack-poison",
    icon = "__tanks_for_bob_fork__/graphics/icons/mine-pack-poison.png",
    icon_size = 64,
    ammo_category = "tank-mine-ammo",
    ammo_type =
    {
      target_type = "direction",
      source_effects =
      {
        {
          type = "create-entity",
          entity_name = "explosion-gunshot"
        }
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
      }
    },
    magazine_size = 10,
    subgroup = "tank-ammo",
    order = "a[tank-ammo]",
    stack_size = 10
  },

  {
    type = "ammo",
    name = "rocketpack",
    icon = "__tanks_for_bob_fork__/graphics/icons/rocket-pack.png",
    icon_size = 64,
    ammo_category = "tank-rocket-ammo",
    ammo_type =
    {
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
            {
              type = "create-entity",
              entity_name = "grenade-explosion"
            }
          }
        }
      }
    },
    magazine_size = 4,
    subgroup = "tank-ammo",
    order = "a[tank-ammo]",
    stack_size = 15
  },

  {
    type = "ammo",
    name = "cannon-shell-2",
    icon = "__tanks_for_bob_fork__/graphics/icons/tank-ammo-shell2.png",
    icon_size = 64,
    ammo_category = "cannon-shell",
    ammo_type =
    {
      target_type = "direction",
      source_effects =
      {
        {
          type = "create-entity",
          entity_name = "medium-explosion"
        }
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
      }
    },
    subgroup = "tank-ammo",
    order = "a[tank-ammo]",
    stack_size = 100
  },

  {
    type = "ammo",
    name = "wmdartillery-ammo",
    icon = "__tanks_for_bob_fork__/graphics/icons/nuke-artillery-shell2.png",
    icon_size = 64,
    ammo_category = "artillery-shell",
    ammo_type =
    {
      target_type = "position",
      source_effects =
      {
        {
          type = "create-entity",
          entity_name = "artillery-cannon-muzzle-flash"
        }
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
          range_deviation = 0.11
        }
      }
    },
    subgroup = "tank-ammo",
    order = "a[tank-ammo]",
    stack_size = 1
  },

  {
    type = "ammo",
    name = "tank-wmd-ammo",
    icon = "__tanks_for_bob_fork__/graphics/icons/tank-ammo-wmd.png",
    icon_size = 64,
    ammo_category = "tank-wmd-ammo",
    ammo_type =
    {
      target_type = "direction",
      source_effects =
      {
        {
          type = "create-entity",
          entity_name = "artillery-cannon-muzzle-flash"
        }
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
      }
    },
    subgroup = "tank-ammo",
    order = "a[tank-ammo]",
    stack_size = 1
  }
})