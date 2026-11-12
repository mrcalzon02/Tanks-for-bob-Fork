-- Real GUI Factorio 2.1 capture fixture for approved floorless Solar Boiler V8.
-- Screenshot output is produced ONLY by game.take_screenshot in a graphical client.
-- A headless engine produces no screenshot and fails the external verification.
local DIRECTIONS={
  {"north",defines.direction.north},
  {"east",defines.direction.east},
  {"south",defines.direction.south},
  {"west",defines.direction.west}
}
local GROUNDS={"natural","concrete"}
local ZOOMS={{"normal",1.6},{"close",2.9}}
local shots={}
local locations={}
local function ensure(ok,message)
  if not ok then error("SOLAR_V8_CLIENT_FIXTURE: "..message) end
end
local function populate_area(surface,center,tile)
  local tiles={}
  for yy=-10,10 do
    for xx=-11,11 do
      tiles[#tiles+1]={name=tile,position={x=center.x+xx,y=center.y+yy}}
    end
  end
  surface.set_tiles(tiles,true)
  local found=surface.find_entities_filtered{
    area={{center.x-12,center.y-11},{center.x+12,center.y+11}},
    type={"tree","simple-entity","resource"}
  }
  for _,item in pairs(found) do
    if item.valid then item.destroy() end
  end
end
script.on_init(function()
  local surface=game.surfaces[1]
  ensure(surface~=nil,"missing Nauvis/first test surface")
  -- Distinct areas avoid overlapping neighboring boiler/pipe collision boxes.
  for ground_index,ground in ipairs(GROUNDS) do
    for d,orientation in ipairs(DIRECTIONS) do
      local center={x=40*(d-1),y=40*ground_index}
      surface.request_to_generate_chunks(center,2)
      locations[ground..":"..orientation[1]]=center
    end
  end
  surface.force_generate_chunk_requests()
  for ground_index,ground in ipairs(GROUNDS) do
    for d,orientation in ipairs(DIRECTIONS) do
      local center={x=40*(d-1),y=40*ground_index}
      populate_area(surface,center,ground=="concrete" and "concrete" or "dirt-7")
      local boiler=surface.create_entity{
        name="solar-boiler",position=center,force="player",direction=orientation[2]
      }
      ensure(boiler and boiler.valid,"failed to place "..orientation[1].." boiler on "..ground)
      -- The engine, not a guessed graphic offset, gives the actual native pipes.
      local attached=0
      for box_id=1,2 do
        local ports=boiler.get_fluid_box_pipe_connections(box_id) or {}
        for _,port in ipairs(ports) do
          ensure(port.target_position,"missing native target position")
          local pipe=surface.create_entity{
            name="pipe",position=port.target_position,force="player"
          }
          ensure(pipe and pipe.valid,"native pipe placement failed")
          attached=attached+1
        end
      end
      ensure(attached==3,"wrong pipe count for "..orientation[1])
      for _,zoom in ipairs(ZOOMS) do
        shots[#shots+1]={
          center=center,ground=ground,facing=orientation[1],
          zoom_name=zoom[1],zoom=zoom[2],
          path="solar-boiler-v8/"..orientation[1].."-"..ground.."-"..zoom[1]..".png"
        }
      end
    end
  end
  ensure(#shots==16,"expected exactly sixteen graphical captures")
  storage.solar_v8_shot=0
  storage.solar_v8_locations={}
  for _,shot in ipairs(shots) do
    storage.solar_v8_locations[#storage.solar_v8_locations+1]=shot
  end
  log("SOLAR_V8_GUI_WORLD_PASS boilers=8 physically_connected_pipes=24 screenshots=16")
end)
-- Separate capture requests prevent queue-burst graphics lag on older hardware.
script.on_nth_tick(45,function()
  local i=(storage.solar_v8_shot or 0)+1
  local s=storage.solar_v8_locations
  if i>#s then return end
  local shot=s[i]
  game.take_screenshot{
    surface=game.surfaces[1],
    position=shot.center,
    resolution={x=1152,y=864},
    zoom=shot.zoom,
    path=shot.path,
    show_gui=false,
    show_entity_info=false,
    anti_alias=true,
    force_render=true,
    daytime=0.5,
    hide_clouds=true,
    hide_fog=true
  }
  storage.solar_v8_shot=i
  log("SOLAR_V8_GUI_SCREENSHOT_REQUEST "..i.."/16 "..shot.path)
  if i==#s then
    game.set_wait_for_screenshots_to_finish()
    log("SOLAR_V8_GUI_SCREENSHOT_QUEUE_COMPLETE count=16")
  end
end)
