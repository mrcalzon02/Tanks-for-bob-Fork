-- Passive storage: native level/flow visuals, original capacity/ports/directions.
local tank=assert(data.raw['storage-tank']['wood-basin'])
local p='__tanks_for_bob_fork__/graphics/entity/wood-basin-v1/'
local function view(i)
 return {filename=p..'body-256.png',width=256,height=256,x=i*256,scale=32*4.8/256,shift={0,-.75/math.sqrt(2)}}
end
tank.pictures={
 picture={north=view(0),east=view(1),south=view(0),west=view(1)},
 window_background={filename=p..'window-background.png',width=12,height=18},
 fluid_background={filename=p..'fluid-background.png',width=12,height=18},
 flow_sprite={filename='__base__/graphics/entity/pipe/fluid-flow-low-temperature.png',width=160,height=20},
 gas_flow={filename='__base__/graphics/entity/pipe/steam.png',line_length=10,width=48,height=30,frame_count=60,animation_speed=.25,scale=.5}
}
tank.window_bounding_box={{-.19,.27},{.19,.84}}
tank.water_reflection=nil
local icon='__tanks_for_bob_fork__/graphics/icons/wood-basin-v1.png'
for _,kind in ipairs({'item','recipe','technology','storage-tank'}) do
 local target=data.raw[kind] and data.raw[kind]['wood-basin']
 if target then target.icon=icon;target.icon_size=64;target.icons=nil;target.icon_mipmaps=nil end
end
