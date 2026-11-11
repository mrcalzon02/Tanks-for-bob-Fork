-- Approved native Blender V8 / graphics-only Factorio 2.1 integration.
-- 3x2 footprint, native fluid boxes and collision unchanged.
local boiler = assert(data.raw["boiler"] and data.raw["boiler"]["solar-boiler"], "Solar Boiler prototype not found")
assert(boiler.type=="boiler", "Solar Boiler is not a boiler prototype")
assert(boiler.selection_box[1][1]==-1.5 and boiler.selection_box[2][1]==1.5, "Solar Boiler footprint unexpectedly changed")
local water = assert(boiler.fluid_box, "Solar Boiler water fluid box missing")
local steam = assert(boiler.output_fluid_box, "Solar Boiler steam fluid box missing")
assert(#water.pipe_connections==2 and #steam.pipe_connections==1, "Boiler pipe connector count changed")
local function port(p,x,y,direction)
  assert(p.position[1]==x and p.position[2]==y and p.direction==direction, "Boiler native pipe position changed")
end
port(water.pipe_connections[1],-1,0.5,defines.direction.west)
port(water.pipe_connections[2],1,0.5,defines.direction.east)
port(steam.pipe_connections[1],0,-0.5,defines.direction.north)
-- Captures are 256px, 4 directions x 16 frames in one 8x8 atlas.
-- Camera 45deg ground-center correction; see pipe-placement QA.
-- Blender +90 is Factorio WEST, so east/west source rows are swapped.
local texture="__tanks_for_bob_fork__/graphics/entity/solar-boiler-v8/working-256.png"
local pictures={}
pictures.north={structure={
  filename=texture,priority="high",width=256,height=256,
  x=0,y=0,frame_count=16,line_length=8,
  animation_speed=0.133333333,scale=0.556249976,
  shift={-0.000000000,-0.657609174}
}}
pictures.east={structure={
  filename=texture,priority="high",width=256,height=256,
  x=0,y=1536,frame_count=16,line_length=8,
  animation_speed=0.133333333,scale=0.556249976,
  shift={-0.000000000,-0.657609174}
}}
pictures.south={structure={
  filename=texture,priority="high",width=256,height=256,
  x=0,y=1024,frame_count=16,line_length=8,
  animation_speed=0.133333333,scale=0.556249976,
  shift={-0.000000000,-0.657609174}
}}
pictures.west={structure={
  filename=texture,priority="high",width=256,height=256,
  x=0,y=512,frame_count=16,line_length=8,
  animation_speed=0.133333333,scale=0.556249976,
  shift={-0.000000000,-0.657609174}
}}
boiler.pictures=pictures
-- Suppress legacy independent boiler layers; full-object V8 art includes all details.
boiler.structure=nil; boiler.patch=nil; boiler.fire=nil; boiler.fire_glow=nil
-- No inventory icon, energy, collision, recipes, fluidboxes or prototypes changed.
