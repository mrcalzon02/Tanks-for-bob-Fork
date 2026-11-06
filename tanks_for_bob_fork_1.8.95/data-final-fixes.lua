-- Bob adapters run after the other mods' data updates/final fixes.
-- Optional dependencies in info.json establish integration load order.
if mods["bobvehicleequipment"] then
  require("prototypes.Compatibility.bobs")
end

-- Optional Bob's Warfare alternative hull recipes and staged research.
if mods["bobwarfare"] then
  require("prototypes.Compatibility.bobs_warfare")
end

-- Optional Bob's Metals alternative route; no impact without Bob's Metals.
if mods["bobplates"] then
  require("prototypes.Compatibility.bobs_metallurgy")
end
