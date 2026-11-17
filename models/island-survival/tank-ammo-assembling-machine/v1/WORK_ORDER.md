# Tank Ammunition Assembler V1 — actual construction brief

Current 1.8.104 native entity: assembling-machine/tank-ammo-assembling-machine,
3x3, speed 1, electric 175 kW, one module slot, ingredient limit six, no burner.
Item places that entity and stacks to ten. All four cardinal directions place
normally. Rubberized-timber activates the north crude-oil input; industrial coke
activates the south crude-oil output. Both are independently connected to ordinary
player-grid pipes in all four directions. Inactive fluid connections are hidden
by the native off_when_no_fluid_recipe behavior; preserve it and the fixed ports.

The gated building recipe is in tank-ammo-component: Encabulator one,
Cradinal-grametter three, Hydrocoptic-marselvanes ten and Alumatedplate one,
0.5 seconds -> assembler one, with a 10% industrial-waste item chance.
Technology encabulated-device-integration follows its authorization technology,
costing 200 units of red and green science at 45 seconds each. Base assemblers
1/2/3 and this machine have compatible categories; actual construction operation
still needs testing. Do not replace this electric contract with a burner engine.

There are 46 real tank-ammo-component recipes, all selectable in the native
machine. Full ingredients/results, quantities, times, probabilities and unlocks
are saved in contract.json. Factorio also supplies ten generic parameters recipes;
they are explicitly archived separately as engine placeholders and do not define
additional construction functions. Selection/connection probes are not yet
claims that all 46 recipes have completed real operations.

The actual operations are broader than ammunition loading. Copper plate is drawn
into casings; iron plate/resin/alloy become Alumatedplate; explosives and plate
make universal explosive; casings plus charge become gun/mortar ammunition.
Existing encabulator components are assembled with resin/alloy/granules, producing
industrial/radioactive wastes. Waste is reprocessed into ores; kits, minepacks,
rocketpacks and tanker ammunition are packaged. Do not infer fictional uses from
component names or borrow Tech-Priests machinery contracts.

The two actual fluid recipes matter. Rubberized-timber uses wood ten, universal
explosive one and crude oil ten -> wood forty + industrial waste ten. Industrial
coke uses wood forty + universal explosive ten -> coal fifty + industrial waste
twenty + crude oil one hundred. The output is crude oil, not steam, water or a
made-up drain fluid. Model supported feed/closed mixing, thermal separation and
collection hardware consistent with these transformations and electric power.

Preserve all eight saved starter OBJ groups: base, feeder, case former, loading
hopper, north inlet, south outlet, output cases and safety cage. Reuse useful
volume/layout while refining the rough boxes/cylinder into low-tech supported
construction: stone/brick seating, timber framing and bins, forged line shaft,
geared crank and guided press/packing ram, case-forming die/mandrel, contained
mixing and electric-driven retort/condensate hardware. These are visual mechanisms
for the documented real recipes, not new gameplay. Keep material flows and load
paths understandable. Fixed full-bore pipe mouths must meet actual ordinary
pipes at the native face planes in every direction; old rough inlet diameter and
placement are not proof of correct final fittings. Safety rails must clear all
moving sweeps. Preserve fixed sockets, attached joints, rigid links and any
upright containers; do not add unrelated machinery merely as decoration.

Next deliver this machine completely before another structure: model-specific
UV/image materials, meaningful attached animation, packed/reopened source,
independently inspected GLB, source/export sweep, true idle/working facing sprites,
actual current-mod integration, all real recipe operations, player-grid input AND
output fluid connections, electric starvation/resupply, blocked item/fluid output,
stop/restart and operated-save reload. Then commit/push/read back source, exports,
sprites/code/evidence and canonical FMPL. No individual owner visual approval is
claimed by this contract checkpoint. Preserve the eighteen accepted structures;
the unfamiliar Tanks condenser candidate remains held until reconciled.
