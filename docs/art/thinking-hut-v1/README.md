# Thinking Hut V1 operational delivery

The current Tanks `thinking-hut` is a 3x3 chemical-burner research lab, using
20 kW at research speed 0.5, with no module slots, processing recipes, item
outputs or fluid sockets. Its building is enabled initially: ten wood and
35 seconds produce one placeable hut. Four requested placement directions
normalize to north and native rotation returns false, so there is one actual
art orientation. The complete runtime contract is saved in
`models/island-survival/thinking-hut/v1/contract.json`.

The lab accepts fourteen food/document research items, from Seared Fish and
Meal through requisition, assessment and board paperwork. Seventy-five current
technologies use supported inputs in nineteen distinct combinations. This
delivery exercises one actual technology for every combination and consumes
all fourteen accepted inputs; it does not claim completing all 75 technologies.

Preserved/refined all six tracked OBJ groups: timber floor, wall shell, thatched
gable, doorway, lantern backing and smoke vent. The shelter now has separate
floorboards, seated posts, inward knee braces, rafters/bearing seats, bound
staggered round reeds, real window openings and a clear entry. An open study
porch contains written records, food support, ink/stylus and a sensitive balance.
Its bored bronze trunnion turns on a fixed pin; both suspended pans remain
upright and attached to the retained beam eyes. A grounded stone/clay hearth,
hood and continuous flue pass through an actual heat-clearance roof opening.

The owner called out the original dark lantern box. The final lantern has a
mounted iron bracket, connected bail/legs, bellied oil reservoir, wick, open
guards, curved reflector and vented hood. Its warm translucent outer flame and
hot core survive the actual GLB export. The hood/cage was lengthened after the
native camera hid the first flame. Working and idle captures, night views,
native warm active light and a close export view demonstrate the correction.
The flame is extinguished in the genuine idle pose. Hearth smoke positions
are projected from the actual clay flue, with fixed-direction offsets explicit.

Final packed editable source and inspected runtime:
`models/island-survival/thinking-hut/candidates/v1-lantern08`. The source was
saved/reopened; the actual GLB was independently reimported and compared in six
poses, with front/rear/clay/bench/lantern views actually inspected. There are
39 embedded model-specific PBR images, full UV coverage, and no nonfinite or
zero-area triangles. All 193 keys pass suspension-endpoint, upright-pan,
trunnion-fit, table-clearance, static-structure and loop checks. Every moving
mesh is tested against the entire shelter at 193 keys plus 192 half-frames in
both source and GLB. Raw static/moving contacts remain recorded; intentional
cord ties and rigid joints are enumerated. This is sampled clearance rather
than continuous rigid-body simulation.

Seventeen genuine source captures comprise one idle and sixteen working
timestamps. Six verified atlases are retained. Repeated idle cells are explicit;
the native lab uses the first idle cell. Actual Factorio 2.1.24 tests use 24 labs:
all nineteen input combinations, missing fuel, missing meal, no research queued,
script deactivation/restart, completed early research and subsequent new research.
Fuel/ingredient resupply resumes progress. Prerequisites/supplies are seeded in
the isolated proof, without changing normal prototypes or balance. Output and
pipe-blocking cases do not apply to a research lab.

Thirty-three genuine client PNGs include day/night lantern and working/idle
views. The GIF/MP4 encode sixteen real client frames at four fps without generated
or interpolated replacements. After full operation, labs are deactivated through
the native `disabled_by_script` flag, allowed sixty ticks, snapshotted and saved.
The operated-save reload preserves all research inventories, coal and remaining
burning fuel, current research/progress, target unlocks and fixed directions.

The source checkpoint was pushed before final integration. Earlier rough roof
and dark/occluded lantern studies remain held. Delegated judgment is operational
and close enough; individual owner visual approval is not claimed. Concurrent
material-icon changes remain separate. No full-user-mod-pack installation or
Mod Portal publication is claimed.
