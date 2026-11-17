# Stone Water Wheel V3 operational delivery

The actual current Tanks machine is an offshore-pump shoreline intake. It creates
water from its native terrain source at 0.5/tick, or 30/second. Its 1x1 tile
placement has shoreline-offset collision/selection bounds; the actual contract
records them. Energy is void, nominal 1 W: there is no player fuel/electrical
input, pipe supply or selectable processing recipe. Four cardinal directions
are native and independently placed/connected in the proof.

The gated Seablock building recipe uses five wood plus ten brick over 35 seconds
for one wheel, with a 5% chance of one industrial-waste item. The actual wheel
technology follows wood-basin and brick, costing ten Seared Fish research units
at ten seconds each. The isolated fixture verifies the unlock and actually crafts
this recipe in a coal-fuelled Workbench, consuming the real wood/bricks. Test
research prerequisites and supplies are seeded; normal prototypes and balance
are unchanged.

Reuses v2-pilot02's saved editable curved timber rims, keyed spokes, through axle,
hollow bronze sleeves, bedded stone piers/feet and exact full-size fixed collar
and throat. V1/V2 and failed V3 studies remain held. Eight independently pivoted
buckets stay upright throughout the entire lift, with their mass below their
retained pins. The open staved bodies fill while submerged and retain water on
the rising half. A fixed overhead cam lifts guided drain gates only at the top;
a short side jet drops into a flared, supported race and sealed plank receiver.
Outboard current paddles explain motion without inventing a fuel engine.
The receiver has a true fitted bore. Raw sweeps exposed and drove repairs to
rod/rim, paddle/pier/receiver and race/wheel crossings before final export.

Saved/reopened source and actual independently reimported GLB: 443 meshes,
130812 triangles, full UVs, no nonfinite/zero-area geometry, eighteen packed
source PBR images and eighteen embedded export images. Oak grain follows fitted
parts and curved segments; masonry uses its authored mineral maps. Wet iron,
worn bronze and carried water have new model-specific image maps. Six geometry
pose comparisons and 385 source/export mechanism samples prove upright buckets,
attached pivots, fixed socket transforms and loop closure. All moving meshes
are swept against the whole assembly at 193 keys and 192 half-frames in each
artifact. Source/export raw pair inventories agree. All 470 moving contacts are
enumerated as rigid fitted joints, actual cam engagement or intended water/bed
contact. This is sampled clearance, not continuous physics simulation.

Four directions each have 32 genuine working timestamps and one captured stopped
pose: 132 camera/state/time samples, with 396 genuine full/upper/submerged passes.
Complementary world-height holdouts are checked for missing or double body pixels
at every sample; 72 atlases retain all three resolutions and archival idle states.
The native main animation uses upper and submerged layers together at eight fps.
Because Factorio underwater_pictures is static, submerged frames use a tinted
translucent object-layer animation to keep lower buckets/paddles attached and
moving. This approximates depth rather than claiming per-tile water occlusion.
The native pump holds its current animation phase when disabled or full; it has
no separate idle-animation field. Native sampled opaque-geometry comparisons
show working motion and zero significant movement in disabled/full-output views.

Actual Factorio 2.1.24 proof uses sixteen machines and sixteen normal grid pipes:
legal shore placement/all four facings, exactly 60 water after 120 ticks, full
300-unit output networks, drain recovery, disabled stop/restart, source landfill
and restoration. Quarter-tile socket/reported target coordinates are preserved;
ordinary one-tile adjacent pipes connect successfully. The saved source mouth is
0.49 tile shoreward, 0.36 high, with 0.49 bore and 0.68 collar diameter; native
registration differs from the ordinary pipe face plane by only 0.01 tile (0.32
pixels at 1x). All four actual placed-pipe closeups were viewed. No gameplay
ports were moved or off-grid pipes spawned to disguise an art mismatch.

Landfill correctly retains the native hidden water source: extraction continues
at 30/second. The proof records landfill, hidden water and source-fluid water,
then restores the visible water tile. It does not invent a required dry shutdown.
After all native operations and Workbench construction, pumps/Workbench are
disabled and allowed sixty ticks before snapshot and completed client save.
Operated-save reload checks network water totals, source tiles, disabled states,
all four directions, every native pipe joint and the crafted building output.
The separate fresh-fixture reload is not substituted for this operated-save proof.
Forty-eight genuine client PNGs and a 32-frame eight-fps native GIF/MP4 are retained;
no interpolated/generated frames replace gameplay. Installed art/code hashes match
the graphical test profile.

Source checkpoint c11469bf64bcfc757dfda766e8762ffd0d44b22b was pushed/read back.
Final immutable source/evidence and canonical FMPL registration are recorded in
remote-delivery.json once verified. Delegated review is operational and close
enough; individual owner approval, full-user-mod-pack installation and Mod Portal
publication are not claimed. Accepted art and concurrent icon work are preserved.
