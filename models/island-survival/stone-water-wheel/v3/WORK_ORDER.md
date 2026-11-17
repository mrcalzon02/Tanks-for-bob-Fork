# Stone Water Wheel V3 — current native contract

The actual current 1.8.104 machine is an offshore-pump shoreline intake, not a
pipe-to-pipe pump. Native Factorio 2.1.24 proves legal shoreline placement in all
four cardinal directions and ordinary player-grid pipe connection in each.
Each output network contains exactly 60 water after 120 ticks: pumping speed
0.5/tick or 30/second. No fuel or electrical input is required (void source,
nominal 1 W). The source fluid offset is (0,-1), native tile dimensions 1x1;
actual collision/selection bounds and socket frames are in contract.json.

Important registration detail: native output is (0,+0.25), and its reported target
is (0,+1.25) relative to the placed origin. An ordinary pipe one tile shoreward
connects successfully at the player grid despite that fractional target. Preserve
the prototype and compare visible mouths against these actual placed pipes;
do not spawn off-grid pipes or move gameplay ports to make art appear aligned.
The full-bore mouth/collar must stay large enough for normal pipes in each view.

The real Seablock building recipe is gated: five wood plus ten brick over 35
seconds produce one wheel, with a 5% industrial-waste byproduct. Technology
stone-water-wheel follows wood-basin and brick and costs ten units of one Seared
Fish at ten seconds/unit. There are no selectable processing recipes. Water is
extracted from shoreline terrain, rather than supplied by a fluid input pipe.

Reuse the held v2-pilot02 editable source. Its curved timber rims, tenoned spokes,
shaped bearing piers, hollow axle sleeves and full-size fixed outlet are useful.
V1/V2 remain held; the owner rejected rough construction, and the rigidly rotating
scoops fail the explicit requirement that lifting buckets remain upright. Replace
those buckets with independent supported pivots and prove upright orientation
throughout the cycle. Provide a coherent pickup, lift and discharge path and
continuous supported receiver/race, with no decorative machinery unrelated to
native water extraction. Repair the known receiver boolean degenerates and all
moving clearances. Preserve accepted assets and all concurrent work.

Delivery remains pending: model-specific surface refinement, saved/reopened source,
actual GLB inspection and source/export sweep, true working/idle directional
shoreline layers, current-mod integration, native placement/grid pipes, extraction,
full output, stop/restart, landfill/source behavior and operated-save reload,
commits, remote readback and canonical FMPL registration. This contract checkpoint
does not promote any held art or claim final native sprite alignment.
