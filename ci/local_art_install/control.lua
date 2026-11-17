-- Only in the disposable verification profile, never the installed user pack.
local alignment=require('alignment_control')
script.on_init(function()
  local sf=game.surfaces[1]
  local names={'cooking-fire','solar-boiler','fish-pond','primitive-steam-powered-pump'}
  local dirs={defines.direction.north,defines.direction.east,defines.direction.south,defines.direction.west}
  storage.checked_art_entities={}
  for d=1,4 do sf.request_to_generate_chunks({d*16,128},1) end
  sf.force_generate_chunk_requests()
  for row,name in ipairs(names) do for d,direction in ipairs(dirs) do
    local p={x=d*16,y=128+row*12}
    for _,e in pairs(sf.find_entities_filtered{area={{p.x-4,p.y-4},{p.x+4,p.y+4}}}) do if e.valid then e.destroy() end end
    local tiles={};for x=-4,4 do for y=-4,4 do tiles[#tiles+1]={name='refined-concrete',position={p.x+x,p.y+y}} end end
    sf.set_tiles(tiles,true)
    local e=sf.create_entity{name=name,position=p,direction=direction,force='player'}
    assert(e and e.valid,'LOCAL_ART_INSTALL placement failed '..name)
    storage.checked_art_entities[#storage.checked_art_entities+1]=e
  end end
  log('LOCAL_ART_INSTALL_PLACEMENT_PASS actual_placeable_entities=16')
  alignment.initialize()
end)
script.on_nth_tick(30,function(event)
  alignment.tick(event)
  if event.tick~=60 then return end
  assert(#storage.checked_art_entities==16)
  for _,e in ipairs(storage.checked_art_entities) do assert(e.valid) end
  log('LOCAL_ART_INSTALL_RUNTIME_PASS four_assets=4 facings=4 entities=16')
end)
