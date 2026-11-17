-- Actual fixed-orientation burner research lab. Art only; preserve all inputs,
-- research speed, fuel, footprint, progression and native placement behavior.
local hut=assert(data.raw.lab['thinking-hut'])
local prefix='__tanks_for_bob_fork__/graphics/entity/thinking-hut-v1/'
local shift={0,-1.20/math.sqrt(2)}
hut.on_animation={filename=prefix..'working-256.png',width=256,height=256,
  frame_count=16,line_length=8,animation_speed=4/60,scale=32*5.8/256,shift=shift}
hut.off_animation={filename=prefix..'idle-256.png',width=256,height=256,
  frame_count=1,line_length=8,scale=32*5.8/256,shift=shift}
-- Warm lamp light follows the actual projected flame at the study porch.
hut.light={type='basic',intensity=.4,size=3.2,minimum_darkness=.25,
  color={r=1,g=.50,b=.18},shift={-.98,1.32-1.40/math.sqrt(2)}}
-- Hearth smoke leaves the actual saved clay flue, not the old sprite centre.
for _,smoke in ipairs(hut.energy_source.smoke or {}) do
  smoke.position={.82,-.50-3.25/math.sqrt(2)}
  smoke.north_position=smoke.position
  smoke.east_position=smoke.position
  smoke.south_position=smoke.position
  smoke.west_position=smoke.position
  smoke.deviation={.04,.04}
end
local icon='__tanks_for_bob_fork__/graphics/icons/thinking-hut-v1.png'
for _,kind in ipairs({'lab','item','recipe'}) do
  local p=data.raw[kind] and data.raw[kind]['thinking-hut']
  if p then p.icon=icon;p.icon_size=64;p.icons=nil end
end
