# Calcifier V2 operational delivery

The current Tanks `calcifier` is a 3x3, four-direction chemical-burner assembler,
using 1 kW at crafting speed 0.60. Its eight actual recipes consume stone,
water/steam, mineral fractions or precursor/preform items and produce solid
stone, scum, sediment, crystals and waste. The complete item/building recipe,
technology, ingredients/results and fluid contract is in
`models/island-survival/calcifier/v2/contract.json`, with actual native recipe
records adjacent here. No invented lime/CO2 process, electrical demand or new
external connection was added. The south output remains unused by every actual
recipe and is visibly capped.

Preserved all six useful tracked OBJ groups: base, kiln drum, mineral hopper,
furnace door, exhaust and coal rake. Added the supported brick hearth/flue,
braced timber frame, open wet mineral bed, geared paddles, belt-driven engine,
rigid connecting rod, settling/sieve chest and wet two-cavity preform die.
The former straight shaker-to-wheel rail is held. Its replacement is a rigid
offset arm from the upper pulley, routed in front of the forming mechanism,
with retained spherical ends and a guided follower. The die's ram is rigidly
linked to the engine crosshead; its bearing pad carries the load to the base.

Owner clearance corrections were checked against the actual geometry. All
fixed mesh pairs are inventoried, and all moving meshes are checked against
the complete assembly at 193 authored keys plus 192 half-frames, independently
in the source and reimported GLB. Raw reports retain every triangle contact.
The review separately enumerates intentional rigid joints, pinned endpoints,
belt seating, stylized gear engagement and immersion in process material.
Unwanted moving intersections are resolved; this is a sampled game-asset check,
not a continuous collision solver or manufacturing-grade gear analysis.
Guides, die cavities, ram stroke, axle/pedestal recesses and all attachment
endpoints also receive explicit dimensional checks.

The owner also required actual full-size pipe attachments. Both mouth planes
remain at +/-1.5 tiles. The visible bore is now 0.56 tile across with a 0.84-tile
flange, reducing into the smaller internal process plumbing. Seated cast feet,
packing and retained bolts replace the undersized fittings. A measured native
sprite registration offset aligns the 0.36-tile-high axes with standard pipe
art. Four genuine placed-pipe close screenshots and numerical projection
checks accompany the revision. Native ports, footprint and gameplay stay fixed.
The die feed was rerouted above the enlarged capped outlet and rechecked
against the offset drive throughout the cycle.

Final editable source and actual FMPL GLB:
`models/island-survival/calcifier/candidates/v2-sockets08`. The source was saved
and reopened; the export was independently reimported, compared in six poses
and rendered front/rear/clay/close. It has 39 embedded model-specific PBR maps,
complete UVs and no nonfinite or zero-area triangles. All 193 keys pass the
engine/offset-arm endpoint, gear-ratio, guide, seating, fixed-socket and loop
checks. Retained 68 genuine source captures feed six verified sprite atlases;
the sixteen native idle cells explicitly repeat one real idle capture per facing.

Actual Factorio 2.1.24 verification uses 48 machines: all eight recipes in all
four directions plus no-fuel, no-fluid, idle and blocked-item cases. Forty-four
normal player-grid pipe connections pass. All guaranteed products, fuel/fluid
starvation, blocking, stop/restart and unblocking pass without balance overrides.
Fluid output blocking does not apply to these item-only recipes. After full
operation, the fixture stops resupply, freezes and waits for pipe fluid to
settle before saving. The operated save reload checks inventories, machine/pipe
fluid quantities/types/temperatures, directions and connections.

Thirty-eight genuine client PNGs include four inlet-joint closeups and sixteen
working-motion frames. The GIF/MP4 encode those actual client frames at four fps,
without interpolated poses or generated replacements. Smoke positions are
projected from the actual flue for each facing, including the registration offset.

Delegated judgment: operational and close enough after the requested machinery,
clearance and socket corrections. Individual owner visual approval is not
claimed. Earlier studies remain held; concurrent material-icon work is preserved.
No full-user-mod-pack installation or Mod Portal publication is claimed.
