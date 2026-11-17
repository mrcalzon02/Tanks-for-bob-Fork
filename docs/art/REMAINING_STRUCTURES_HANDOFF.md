# Tanks remaining structures — saved handoff, 2026-11-16

The previous enduring goal is **paused**. This handoff preserves work and
prepares a new discussion; it does not resume modeling by itself.

**Continuation checkpoint:** the new enduring goal is active. The corrected
barrel-source Steam Compressor, Wood Basin, Quarry, refined Shaler and Calcifier have
since reached operational integration. Read the current JSON ledger for delivery receipts and remaining
scope; the counts below describe the original saved baseline.

## Current state

- Repository: `mrcalzon02/Tanks-for-bob-Fork`.
- Working checkout: `C:/Users/Admin/Documents/ChatGPT/Tech priests/tanks-structure-production`.
- Current versioned source: `tanks_for_bob_fork_1.8.104/`. Select the actual
  current source on resume; do not hard-code 1.8.103 from older proof scripts.
- The [ledger](STRUCTURE_COMPLETION_LEDGER.md) contains 21 actual structure
  IDs: 10 accepted/integrated and 11 unfinished. FMPL/archive receipt debt is
  tracked separately; operational acceptance does not invent missing exports.
- The 1.8.104 source is byte-identical to its saved native alignment-test copy:
  28 player-grid pipe connections passed and genuine graphical captures exist.
  The checkpoint does not infer a visual pass from file presence. The older
  full-user-pack/install receipts refer to 1.8.103, not proof that the user is
  currently running 1.8.104. See [verification](checkpoint-2026-11-16/verification.json).
- Accepted work to preserve: Campfire V12, Clay Pit V4c, Pit Kiln V6,
  Lumberyard V2b (`growing-plot`), Workbench V8, Cooking Fire V2, Solar Boiler
  V8, Beach Pump V12, Primitive Steam-Powered Pump V3, and Fish Pond V2.
- Beach Pump's underwater occlusion is deferred by explicit owner decision:
  it works, is animated, is close enough, and is not the next polish task.
- All pilot/rejected studies are preserved under their original candidate
  directories. Directory names containing `production` are not approval.
- The recently generated **Steam Condenser V1** is held, unapproved, and not
  installed. Preserve its source/export/68 frames/atlases without silently
  promoting it or mislabeling it as the compressor.

## Actual machine identities and compressor reuse

### Owner correction, 2026-11-16 — authoritative source

The owner identified `models/island-survival/steam-condenser/v1/build_steam_condenser_v1.py`
as the intended half-finished compressor. Reuse its saved barrel/frame model
from `models/island-survival/steam-condenser/candidates/v1-production01/steam-condenser-v1.blend`
as a separate derivative for `Steam-Compressor`. Its existing condenser naming
and water-output assumptions are historical misidentification, not the Tanks
compressor contract. The hydrogen compressor listed below is explicitly the
wrong source. A derivative made from it in this chat was rejected and removed
from active Tanks integration; preserve it only as rejected work.

This source identification does not approve the old candidate as a
`steam-condenser` or establish completion of that separate machine.

The owner confirmed: **“Our compressor is the correct one for the tanks for
Bob purposes.”** Reuse the existing half-finished compressor; do not start a
replacement merely because its asset is inconvenient to find.

The actual Tanks target is `assembling-machine/Steam-Compressor`, with a
placeable item and crafting recipe named `Steam-Compressor`. It is a 3×3 burner
machine using category `Steam-Compressor`; its actual operations include
`Charged-Canister` and `UnCharge-Canister`. The building recipe uses a shaler
and two cooking fires. `Steam-Charge` belongs to **shaler**, so do not confuse
that recipe with the compressor's operation.

Known saved source locations to reconcile before editing:

- Tanks starter: `models/island-survival/obj/Steam-Compressor.obj`.
- **Rejected source — do not use:** a separate Tech-Priests compressor is in the sibling
  `model-production/art/source-to-3d/metallic-hydrogen-chain/hydrogen-compressor/v05-slow-and-audio/compressor-v05.blend`,
  with its V06 native fitting checkpoint in the adjacent
  `v06-owner-accepted-native/` directory. The saved V06 record pins source SHA256
  `29e62716acc5fa52bb4cedc8f3b4f713ac3fb857cb42b46714749910da4013ad`.
  The owner explicitly rejected this model as the wrong compressor in the new
  chat. Preserve that project's source; use the barrel/frame source identified
  in the authoritative correction above for Tanks.
- The owner has now identified the barrel-shaped
  `steam-condenser/candidates/v1-production01` as the intended compressor source.
  Its Tanks derivative must implement the existing canister operations and
  burner construction. The old candidate remains unapproved as a condenser.

The actual Tanks `steam-condenser` also exists as a craftable/placeable machine,
unlocked after primitive pump and crude glass. `Steam-condenserA` consumes wood
and steam and produces stone and industrial waste. Its output fluid socket
does not prove a water-output recipe. Tech-Priests atmospheric condenser V24
is a different 2×2, one-output prototype and is not Tanks completion evidence.

## Remaining roster

Start with the existing compressor, then work through this exact roster using
actual native function and available source to choose the next finishable asset:

| Prototype ID | Structure |
| --- | --- |
| `Steam-Compressor` | Steam Compressor — reuse existing work first |
| `steam-condenser` | Steam Condenser — candidate held; actual function above |
| `stone-water-wheel` | Stone Water Wheel — held studies; buckets must stay upright |
| `wood-basin` | Wood Basin |
| `quarry` | Quarry |
| `shaler` | Shaler |
| `calcifier` | Calcifier |
| `thinking-hut` | Thinking Hut |
| `pondering-hovel` | Pondering Hovel |
| `tank-ammo-assembling-machine` | Tank Ammunition Assembler |
| `tank-assembling-machine` | Tank Assembling Machine |

Reconcile this list against live prototypes and the ledger before modeling;
names and old design blurbs are not proof of a machine's recipe or purpose.

## Prompt for the new discussion

```text
Create an enduring goal to finish the remaining structures in my
mrcalzon02/Tanks-for-bob-Fork mod: model/refine, texture, animate, export through
FMPL, commit, integrate, and verify them as real operational placeable machines.

Start by reading docs/art/REMAINING_STRUCTURES_HANDOFF.md,
STRUCTURE_COMPLETION_LEDGER.json, OPERATIONAL_FINISH_POLICY.md, and the current
repository instructions. Use the actual current source (currently 1.8.104),
preserve concurrent work, and verify the branch before changing it.

Begin with OUR HALF-FINISHED COMPRESSOR. I confirm our compressor is intended
for Tanks for Bob. Locate and inspect its saved editable source, preserve the
useful geometry and mechanism, and finish it for the existing Steam-Compressor
prototype. Do not restart from scratch, substitute an unrelated machine, copy
another mod's gameplay, or rename the held condenser candidate into a compressor.

Before modeling EACH structure, prove that it is used: identify its actual
entity, place_result item, building recipe, technology unlock, crafting
categories, real processing recipes, inputs/results, power/fuel, footprint,
placement rules, ports and directions. If it is not an actual used/placeable
Tanks machine, do not invent it. Read recipes; do not infer function from names.
Fix required wiring that prevents an intended existing machine from working,
with an explicit explanation. Preserve balance/progression unless necessary
for that intended function.

Art direction: PRIMITIVISTIC, LOW-TECH CONSTRUCTION suited to the real operation.
Use timber frames, rough stone/brick/clay, staves and hoops, simple iron/copper/
brass fittings, ropes, levers, cranks, belts, primitive furnaces and practical
pressure vessels where appropriate. Show how input is handled, processed and
discharged. Materials and construction must explain the machine. Avoid generic
modern factory boxes, unexplained sci-fi hardware and decorative mechanisms
unrelated to the recipe. Do not force a concrete platform onto every building.

Use existing assets and the authored-3d-production/FMPL tools. Give each machine
a coherent silhouette, supported construction, usable openings and correctly
sized fixed native fittings. Animate the few parts that explain its work.
Keep rigid links rigid, joints attached, ports stationary, and lifting buckets
upright. Match actual game footprints and pipe positions, including all native
facings; verify pipes on the player placement grid rather than only spawning
entities through scripts.

Complete one machine through delivery before moving on: editable Blender source,
appropriate UV/image materials, a genuinely inspected runtime export, real
Blender idle/working frames, atlas/Lua registration, and native Factorio proof
of placement, recipes, fuel/power, working/idle, blocked output, stop/restart,
connections and reload where relevant. Use existing isolated test tools and
the fixed 45-degree capture workflow. Verify the actual active source/package,
not just a temporary graphics override or a nice render.

Commit useful checkpoints, source, exports, sprites, code and honest evidence;
push normally, verify remote delivery, and update the ledger and FMPL records.
Separate technical validation, owner review, installation and release status.
Do not claim unreviewed drafts or missing receipts as completed work.

Prioritize FUNCTIONAL, ANIMATED, OPERATIONAL AND CLOSE ENOUGH. Be thorough about
function, mechanism, integration and preservation; defer cosmetic perfection.
Use judgment and continue within this authorization instead of repeatedly asking
for routine promotion permission. Do not spend the session polishing accepted
machines, chasing old attachments, creating extra workflows, or merely writing
plans. Beach Pump V12 and the other accepted structures stay preserved.

After the compressor, finish the other ten unfinished machines in the handoff
(eleven unfinished machines total, including the compressor). Continue until each
remaining intended machine is integrated and operational, with its source and
export/registration work accounted for. Keep updates short, show representative
real evidence, and give the next concrete result rather than unrelated designs.
```
