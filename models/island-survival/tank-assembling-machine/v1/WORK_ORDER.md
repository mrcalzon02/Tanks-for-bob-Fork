# Tank Assembling Machine V1 — actual current contract

This is the distinct native assembling-machine/tank-assembling-machine in active
1.8.104: 3x3, electric 250 kW, crafting speed 1, four module slots and ingredient
limit six. It has no burner or fluid storage/ports. All four requested placement
directions normalize to north and rotate() returns false. Author one actual north
sprite orientation; do not invent supported rotation, pipes, fuel or oil processes
from the neighbouring ammunition machine. The full contract is in contract.json.

All thirteen real tank-crafting recipes are selectable. Ten generic engine
parameters placeholders are recorded separately and are not construction functions.
The actual work is primarily upgrading existing vehicles: auto/flame/mine/nade/
rocket/super/WMD tank variants consume an existing tank or intermediate vehicle
plus real arms/encabulator/electronics/engine parts. The car-flamer upgrades a car
with steel and DuplexedSpervingArms. Three WLSK conversions combine an existing
auto/flame/nade tank with a light chassis. The light chassis recipe uses processing
units five, electric engines ten, TurboEncabulators five and Alumatedplates six,
returning chassis one plus industrial waste. Longest recipe is super-tank-wmd at
3040 seconds; preserve actual recipe times rather than accelerating machine speed.
Record every full ingredient/result/time/unlock from the native contract.

The building recipe belongs to tank-ammo-component, not tank-crafting. It consumes
Encabulator one, Cradinal-grametter three, Alumatedplate one and an ammunition
assembler one over 0.5 seconds, producing the vehicle assembler plus a 10% waste
chance. Encabulated-device-integration unlocks it after its authorization, at
200 red+green research units/45 seconds. The delivered ammunition assembler and
base assemblers have compatible building categories. Verify an actual normal
building craft and item/place_result without substituting recipes or progression.

Preserve all nine saved groups: foundation, two assembly rails, two gantry supports,
overhead gantry, empty hull jig, welding head and sparks marker. The raw OBJ is
saved with its exact Git bytes. Refine useful geometry into a supported low-tech
vehicle conversion bed: stone/brick seating and fitted timber/iron rails, braced
load-bearing gantry, real hoist/drive/bearings, retained upright hull/module jig,
and an attached working assembly/joining tool. Use primitive electric drive and
appropriate leads/insulators for the real 250 kW input. A welding/joining effect
may refine the existing saved tool/marker, but must issue from its actual tip.
Do not invent a burner/steam process or borrow Tech-Priests machine gameplay.
The machine upgrades existing vehicles; do not portray it as another ammunition
packing plant or assume every recipe builds a tank from loose plate.

Maintain true scale and clear load paths. Moving hoist loads must remain upright,
ropes/pivots/tools attached, links rigid, guards outside all swept mechanisms.
UVs and model-specific image materials must explain timber grain/end cuts,
fired masonry, forged fittings, electric drive and actual assembly tooling.
Save/reopen source and independently inspect/render actual GLB, including all
source/export moving clearances and endpoint/loop checks before sprite promotion.
Finish genuine idle/working north captures and current-mod integration. Verify
all thirteen real recipe operations at normal speed, four requested placements
normalizing north, real electrical starvation/resupply, item blocked output,
stop/restart and actual operated-save reload. Fluids/fuel tests are inapplicable;
do not add gameplay to manufacture them. Commit/push/read back source, export,
sprites, code, evidence and canonical FMPL before moving to the held condenser.
Nineteen accepted structures remain preserved; no routine promotion approval is
needed, and individual owner approval must not be fabricated.
