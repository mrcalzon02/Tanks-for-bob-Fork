-- Preserve historical ammunition access only when its newly explicit weapon
-- prerequisites are complete. Factorio runs this versioned migration once per
-- save; no control-stage lifecycle handlers or broad recipe resets are needed.
local split_unlocks = {
  {
    previous_technology = "new-munitions",
    technology = "poison-mine-ammunition",
    recipe = "minepack-poison"
  },
  {
    previous_technology = "super-tank-research2",
    technology = "wmd-artillery-ammunition",
    recipe = "wmdartillery-ammo"
  }
}

local function prerequisites_researched(technology)
  for _, prerequisite in pairs(technology.prerequisites) do
    if not prerequisite.researched then return false end
  end
  return true
end

for _, force in pairs(game.forces) do
  for _, split in ipairs(split_unlocks) do
    local previous = force.technologies[split.previous_technology]
    local technology = force.technologies[split.technology]
    local recipe = force.recipes[split.recipe]
    if technology and recipe then
      local preserve = previous ~= nil and previous.researched
        and prerequisites_researched(technology)
      technology.researched = preserve
      -- Also remove obsolete recipe access when the old shared technology was
      -- finished before the required vehicle, land mines, or artillery.
      recipe.enabled = preserve
    end
  end
end
