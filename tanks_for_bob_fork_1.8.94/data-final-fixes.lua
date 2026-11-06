-- Bob adapters run after the other mods' data updates/final fixes.
-- Optional dependencies in info.json establish integration load order.
if mods["bobvehicleequipment"] then
  require("prototypes.Compatibility.bobs")
end
