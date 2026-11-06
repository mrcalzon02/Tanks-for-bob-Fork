data:extend(
{
  {
    type = "int-setting",
    name = "WMD1",
    setting_type = "startup",
    default_value = 10,
    allowed_values = { 5, 6, 7, 8, 9, 10, 11, 12, 13, 15, 16, 17, 18, 19, 20},
    order = "a1",
  },
 
  -- {
  --   type = "bool-setting",
  --   name = "name",
  --   setting_type = "startup",
  --   default_value = true,
  --   order = "d1",
  -- },
  -- {
  --   type = "bool-setting",
  --   name = "name",
  --   setting_type = "startup",
  --   default_value = false,
  --   order = "d2",
  -- },
  -- {
  --   type = "bool-setting",
  --   name = "name",
  --   setting_type = "startup",
  --   default_value = false,
  --   order = "d3",
  -- },
  
})

-- Optional Bob's integration: no effect without Bob's Vehicle Equipment.
data:extend({
  {
    type = "bool-setting",
    name = "tfbf-bobs-equipment-grids",
    setting_type = "startup",
    default_value = true,
    order = "z[compatibility]-a[bobs-equipment-grids]"
  }
})

-- Bob's Warfare optional advanced hull recipes. No effect without Bob's Warfare.
data:extend({
  {
    type = "bool-setting",
    name = "tfbf-bobs-advanced-hulls",
    setting_type = "startup",
    default_value = true,
    order = "z[compatibility]-b[bobs-advanced-hulls]"
  }
})

-- Optional Bob's Invar substitution in the encabulation materials chain.
data:extend({
  {
    type = "bool-setting",
    name = "tfbf-bobs-metallurgy",
    setting_type = "startup",
    default_value = true,
    order = "z[compatibility]-c[bobs-metallurgy]"
  }
})
