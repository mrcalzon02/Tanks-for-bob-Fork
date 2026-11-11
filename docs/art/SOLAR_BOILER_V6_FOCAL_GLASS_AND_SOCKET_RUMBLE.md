# Solar Boiler V6 — paired glass focal boilers, whole-machine shudder and locked pipe sockets

- **Immutable V5 donor**: `models/island-survival/solar-boiler/generated-v5/solar-boiler-v5.blend`
- **Editable V6 source**: `models/island-survival/solar-boiler/v6/`
- **Verified native V6**: `models/island-survival/solar-boiler/generated-v6/solar-boiler-v6.blend`
- **Actual Blender 4-way review**: `models/island-survival/solar-boiler/generated-v6/review-four-directions.png`
- **Real 16-frame four-view GIF**: `models/island-survival/solar-boiler/generated-v6/working-four-directions-focal-glass-rumble.gif`
- **Proof commit**: `847514c7e0091543bfd23dfae895c39986837bf1`
- **Passing job**: https://github.com/mrcalzon02/Tanks-for-bob-Fork/actions/runs/42988367558

## Accepted technical constraints

The machine remains 3×2 tiles, with the previously modeled central stave
barrel (18 actual staves), 65 bentwood pipe planks, two polished timber
parabolic concentrators, repaired barrel pipe-junction roof holes and the
Campfire-approved original wood shaders and FMPL concrete.

Two independent transparent glass hot-water tubes with fluid geometry, keyed
roiling surfaces, 24 rising bubbles and tiny steam vents are aligned to the
**optical focal lines** of the west and east concentrators. The erroneous V5
above-barrel glass vessel is retained in the source for inspection but hidden
from the visible V6 model.

The central timber barrel and both solar concentrators are children of a
keyed sub-.022-tile rumble rig. **The main Factorio fluid ports and reference
fittings are NOT children of that rig.** Each of the 33 movable wood planks
at these three junctions retains an entirely fixed four-vertex socket-end
cross-section, followed by 12.5% rigid length and eased deformation closer
to the barrel. All actual native mouth positions remain immobile.

## Real source and verification

Independent Blender reopening verifies the exact V5 source hash; one stable
45-degree camera; world-space socket ring immobility at animation frames
0,1,25,49,73,91 and 97 (drift below 1e-6 Blender tiles); three unchanged
native fluid fitting faces; corrected steam lobe visibility phase at frame 97;
frame-1/97 closure; and every captured PNG hash.

The proof contains 4 idle and 64 working Cycles views at 256px (four
directions × 16 poses at 8 FPS), six same-frame isolation images and
preview-only 64/128/256 idle/working atlases. The recorded 64px
effect-isolation changes are: **23 boiling-water pixels, 7 vent-steam pixels
and 441 body-rumble pixels**. Counts are evidence of render contribution,
not automatic human visual acceptance.

Source history is preserved: the first 68-frame render exposed a single
outermost-vertex anchor rather than a fixed external ring. V6 was rebuilt with
four-vertex root rings and independent evaluated-world-space tests. The
subsequent render found that a modulo-3 steam flutter was not wrapping after
the 16th frame; two frame-97-only visibility keys were corrected in the
reopened .blend. Those changes affect **only the unrendered closing pose**
and were proven not to change any of the 68 captured Blender frames.

**Technical modeling/animation proof: PASSED.**
**Owner visual acceptance: PENDING.**
**Native Factorio 2.1 sprite integration / runtime smoke / Mod Portal
release: NOT PERFORMED.**

The existing one-job Blender production workflow remains reusable through
manual dispatch. Its one-shot V6 push hook was retired after successful
native source publication, without adding new workflows.
