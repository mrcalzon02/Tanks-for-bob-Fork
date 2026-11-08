--data:extend(
--{
---- Make assembling-machine 3 able to craft tank components
----	{
--		type = "assembling-machine",
--		name = "assembling-machine-3",
--		crafting_categories = {"crafting", "advanced-crafting", "crafting-with-fluid"},
--	}
--}
--if data.raw.assembling-machine["assembling-machine-3"] then
--	table.insert(data.raw.assembling-machine["assembling-machine-3"].crafting_categories, { "tank-crafting","tank-ammo-component"} )
--	table.insert(data.raw.unit["small-spitter"].loot, {  item = "small-alien-artifact",  count_min = 1,  count_max = 1,  probability = 0.5 } )
--end

function TableConcat(t1,t2)
    for i=1,#t2 do
        t1[#t1+1] = t2[i]
    end
    return t1
end

data.raw["assembling-machine"]["assembling-machine-1"].crafting_categories = TableConcat( data.raw["assembling-machine"]["assembling-machine-1"].crafting_categories, {"tank-crafting","tank-ammo-component"} )
data.raw["assembling-machine"]["assembling-machine-2"].crafting_categories = TableConcat( data.raw["assembling-machine"]["assembling-machine-2"].crafting_categories, {"tank-crafting","tank-ammo-component"} )
data.raw["assembling-machine"]["assembling-machine-3"].crafting_categories = TableConcat( data.raw["assembling-machine"]["assembling-machine-3"].crafting_categories, {"tank-crafting","tank-ammo-component"} )

-- Material recovery must be able to start refining on maps without oil wells.
-- Keep Oil Gathering and every downstream vanilla prerequisite. Both a
-- pumpjack and a Workbench can satisfy the native crude-oil production trigger.
-- Respect another mod's replacement research method instead of overwriting it.
local oil_processing = data.raw.technology["oil-processing"]
local oil_trigger = oil_processing and oil_processing.research_trigger
if oil_trigger and oil_trigger.type == "mine-entity" then
    local entities = oil_trigger.entities or {oil_trigger.entity}
    if #entities == 1 and entities[1] == "crude-oil" then
        oil_processing.research_trigger = {
            type = "craft-fluid", fluid = "crude-oil", amount = 1
        }
    end
end
