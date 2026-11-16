local function pond(d,row)
  local entities=game.surfaces[1].find_entities_filtered{name="fish-pond",position={d*24+.5,row*24+.5},radius=2}
  if not entities[1] then error("FISH_POND_V2_GUI: missing "..d.."/"..row) end
  return entities[1]
end
local function shot(entity,name,zoom)
  game.take_screenshot{surface=entity.surface,position={entity.position.x,entity.position.y-.2},
    resolution={x=768,y=512},zoom=zoom,path="fish-pond-v2/"..name..".png",
    show_gui=false,show_entity_info=false,anti_alias=true,force_render=true,
    daytime=0,hide_clouds=true,hide_fog=true}
end
script.on_nth_tick(30,function(event)
  if event.tick==30 then
    local surface=game.surfaces[1]
    surface.always_day=true
    surface.daytime=0
    storage.fish_pond_v2_legacy={}
    for d,name in ipairs({"north","east","south","west"}) do
      local entity=pond(d,1)
      shot(entity,name.."-normal",1)
      shot(entity,name.."-close",2.5)
      shot(pond(d,2),name.."-idle-close",2.5)
      shot(pond(d,5),name.."-fluid-close",2.5)
      local center={x=entity.position.x+8,y=entity.position.y}
      local tiles={}
      for x=-5,5 do for y=-5,5 do tiles[#tiles+1]={name="refined-concrete",position={center.x+x,center.y+y}} end end
      surface.set_tiles(tiles,true)
      for _,e in pairs(surface.find_entities_filtered{area={{center.x-5,center.y-5},{center.x+5,center.y+5}},type={"tree","simple-entity","resource"}}) do e.destroy() end
      local legacy=surface.create_entity{name="fish-pond-v2-legacy-reference",position=center,direction=entity.direction,force="player"}
      if not legacy then error("FISH_POND_V2_GUI: missing legacy "..name) end
      legacy.set_recipe("catch-fish")
      legacy.get_fuel_inventory().insert{name="coal",count=5}
      legacy.get_inventory(defines.inventory.crafter_input).insert{name="wood",count=50}
      storage.fish_pond_v2_legacy[d]=legacy
    end
    game.set_wait_for_screenshots_to_finish()
  elseif event.tick==60 then
    for d,name in ipairs({"north","east","south","west"}) do
      shot(pond(d,1),name.."-motion-close",2.5)
      shot(storage.fish_pond_v2_legacy[d],name.."-legacy-close",2.5)
    end
    game.set_wait_for_screenshots_to_finish()
    log("FISH_POND_V2_GUI_QUEUE_COMPLETE count=24")
  end
end)
