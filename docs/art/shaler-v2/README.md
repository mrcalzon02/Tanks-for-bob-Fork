# Shaler V2 operational delivery

The current Tanks Shaler is a 3x3 chemical-burner processor with 17 actual
recipes, four directions, north steam/water input and south acid output.
Its building uses crude glass and brick and unlocks after Calcifier.
The complete native recipe/ingredient/result contract and explicit technology
bindings are in `models/island-survival/shaler/v1/contract.json`.

Preserved the tracked starter base, body, jaw supports, hopper and chute as
useful editable geometry. V1 was owner-held as a good rough structure, requiring
substantially more working machinery, pipework/hoses and a supported chimney.
V2 adds a keyed drive shaft, equal 18-tooth miter gears, an 18:54 front reduction,
a second rigid piston/connecting arm and wet-process recirculation loop. The
original engine piston, moving belt and cam-driven canister press remain linked.
The extra hoses are lagged copper flexures with reinforced ends. All exterior
fluid sockets stay fixed. The chimney now has four lower bonded courses,
a continuous broad footing on the paving and hearth corbels with an open flue.

Final packed editable source/GLB: `models/island-survival/shaler/candidates/v2-mechanisms02`.
The source was saved and reopened; the actual export was independently reimported
and inspected in six poses, front/rear/clay and machinery close views. All 193
frames pass rigid endpoint, guided-piston, cam contact, gear-ratio, fixed-socket
and loop checks. The current export has 36 embedded PBR images, complete UVs
and no nonfinite or zero-area triangles. Genuine 68-frame captures and six
verified atlases are retained. V1 and superseded studies remain held.

Actual Factorio 2.1.24 operation: 88 machines cover all 17 real recipes in four
directions plus fuel-free, steam-free, idle, blocked item and blocked fluid cases.
All guaranteed results are checked; random byproducts need not roll. Includes
canister packing/unpacking, industrial and radioactive recovery, water washing,
and other actual steam separation/synthesis operations. Eighty-eight direct
normal player-grid pipe connections and 136 additional ordinary feed-buffer
pipes supply the large 20,000-steam batch without prototype/balance changes.
Stop/restart and item/fluid unblocking pass.

Thirty-six genuine client PNGs include all directions and working/idle states.
`working-loop.gif` and `.mp4` encode sixteen actual client frames at four fps,
without interpolated poses or generated replacements. Smoke positions are
measured from the real flue outlet for every facing. The operated save is included.
Only after actual operational completion, the fixture freezes machines, stops
resupply and observes fluid settling before snapshot/save. Reload verifies all
88 output inventories, machine/pipe fluid amounts/types/temperatures and pipe
connections. Headless and client logs/receipts are adjacent. A Freeplay welcome
pause in the final capture was dismissed through the real client; it did not
require restarting the run or changing gameplay.

Delegated judgment: operational and close enough; no individual owner visual
approval is claimed. No recipe, throughput, fuel, footprint, direction or socket
behavior changed. No full-user-mod-pack installation or Mod Portal publication.
