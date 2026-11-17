# Tank Ammunition Assembler V1 operational delivery

The actual current Tanks entity is a 3x3 electric component assembler: speed 1,
175 kW, one module slot, six-ingredient limit and no burner. It has 46 real
`tank-ammo-component` recipes. Ten engine `parameters` placeholders are archived
separately and do not define extra construction functions. The exact contract
contains all real ingredients/results, quantities/probabilities, times and unlocks.

The building recipe consumes Encabulator one, Cradinal-grametter three,
Hydrocoptic-marselvanes ten and Alumatedplate one in 0.5 seconds for one assembler,
with a 10% industrial-waste byproduct chance. Encabulated device integration
unlocks it. The fixture verifies that unlock and actually crafts the building in
a normal base assembling-machine-3 with its real supplied ingredients and power.
Research prerequisites and test supplies are seeded in the isolated proof;
production prototypes, recipes, crafting speed, modules and power are unchanged.

The actual operations cover copper-plate casing forming, explosive/charge loading,
component/encabulator assembly, ore/waste reprocessing and kit/ammunition packing.
Rubberized timber consumes wood ten, universal explosive one and crude oil ten
and returns wood forty plus industrial waste ten. Industrial coke consumes wood
forty and universal explosive ten and returns coal fifty, industrial waste twenty
and crude oil one hundred. Those actual wood/oil recipes define the closed input,
mixing, retort and condensing/collection hardware. No steam/water output, burner
engine or Tech-Priests machinery contract is substituted.

Preserves all eight original OBJ groups: stone-seated factory base, open timber
feeder, retained cylindrical forming/mixing body, charging hopper, both fixed
pipe bodies, output-case tray and protective front rail. New seated posts and
splayed stands carry each part. A cloth-wrapped open wound motor drives a 2:1
press reduction and 1:1 upper transfer/agitator belts. A bored 0.52-tile rigid
connecting rod joins the eccentric and guided press ram; its mandrel enters a
real hollow copper case and forming die. Motor stator/rotor, guide eyes, bearings,
pulley grooves, frame and guards have actual clearance. The hollow clay retort
has a retained through-shaft/contained mixer, charging neck, supported electric
heating bands and true cap ports. Connected crude-oil lines feed it from the
north socket and return through a four-turn coil and seated collector to the
south socket. Fixed reducers/collars/saddles are full bore and grounded.

The packed source was saved/reopened and its actual GLB independently reimported:
272 meshes, 215926 triangles, all UVs, no nonfinite/zero-area geometry, and 33
packed source PBR images/33 embedded runtime images. Per-part oak grain/end cuts,
limestone/clay, winding cloth, leather, copper, bronze and iron retain appropriate
material placement. Actual front/rear/side/clay/press export images were viewed.
Six geometry poses compare, with 385 mechanism samples in each artifact. Actual
rigid link span stays 0.52 tile; authored-key pin deviation is below 0.000001 tile. Half-key interpolation moves pin centres about
0.000018 tile inside the 0.002 radial bore clearance. Guide axes, 2:1 motor ratio,
1:1 transfer phase, fixed socket transforms and loop closure are verified.

Every moving mesh is swept against the whole machine at 193 keys and 192 half
frames independently in source and actual GLB. Raw pair inventories agree.
All 161 animated contacts are enumerated rigid assembly joints or actual belt
running-surface engagement; no unwanted moving crossings remain. This is sampled
clearance, not continuous physics simulation. The fixed belt paths are modeled;
leather grain travel and stock deformation are not simulated. Earlier bad motor,
beam/pulley and support studies remain held.

There are 132 genuine source captures: four directions each with one idle pose
and 32 distinct working timestamps, packed at three resolutions. Native assembler
idle/working frame counts must match; one captured idle pose is repeated explicitly
into 32 idle cells per direction. These are not claimed as 128 captured idle times.
The native adapter uses the current electric prototype and its conditional fluid
ports. Legacy pipe pictures are removed as art only; actual pipe positions remain
unchanged. Both full-size mouths project to ordinary pipe face anchors in all
four directions to within 0.000001 tile. Eight actual input/output placed-pipe
closeups were viewed. Main bore is 0.49 tile, collar outside diameter 0.68 and axis
height 0.36; no off-grid pipes or moved gameplay ports disguise alignment.

Actual Factorio 2.1.24 final proof uses 208 target machines: all 46 recipes in all
four directions (184 real recipe cases), plus power/fluid starvation, item/fluid
blocked output, idle and stop/restart cases. Twenty ordinary grid joints connect
actual input/output recipes and diagnostic states. Even the two 3160-second
recipes run at normal crafting speed and default empty modules for their complete
native durations; only global simulation time is accelerated in the hidden client.
Guaranteed results and actual input consumption pass for every recipe/direction.
Test-only isolated power interfaces/poles supply legitimate electricity; no target
power, crafting speed or module parameters are changed.

Blocked item captures occur after its seven-second craft. The 150-second fluid
recipe waits 160 seconds before release: in every direction it is powered, has
progress 1, status full_output and zero finished products, with 1000 oil in the
machine plus 100 in its pipe. Draining the receiver releases the real outputs.
The native is_crafting flag may stay true while a completed craft awaits output;
status/progress/output counters and sampled visible pose provide the evidence.
Power/fluid resupply, disabled pause/restart, blocked-output release and the actual
building craft pass. Sixty native PNGs and a 32-frame eight-fps genuine GIF/MP4
are retained, without generated/interpolated substitutes. Working opaque machinery
moves; disabled and post-cycle item-blocked sampled views remain stationary.

After complete operation, all target machines and the builder are disabled and
allowed sixty ticks before snapshot and completed client save. Actual operated
reload preserves every input/output inventory, fluid amount/type/temperature,
pipe joint, recipe/progress/products-finished, electrical buffer, direction,
disabled flag and crafted building output. The separate initial-fixture reload
is not substituted for this operated-save proof. Installed code/sprite hashes
match the current graphical profile; Git text normalization is verified separately
from exact source/export/sprite binary bytes when published.

Source checkpoint 13c4696eb0e8677c57ee898af154eb421f343633 was pushed and read back.
Earlier visual timing runs were superseded by the final after-cycle/full-fluid
proof. Final immutable source/evidence publication and canonical FMPL registration
are recorded in remote-delivery.json once verified. Review is delegated operational
and close enough; individual owner approval, full-user-pack installation and Mod
Portal publication are not claimed. Accepted assets/concurrent icon work remain.
