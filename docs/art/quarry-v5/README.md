# Quarry terrain correction checkpoint

The owner rejected the initial quarry as ultra rough, then rejected sharp natural
rock edges and boulder-like bases perched on the terrain. V5-rooted02 replaces
those formations with one continuous excavated landform, a nearly flush floor,
irregular fading ground boundary and sloped rock roots. Deliberately worked
cleavage remains distinct from the natural outer bank.

Editable source: `models/island-survival/quarry/candidates/v5-rooted02/quarry-v5.blend`.
The adjacent GLB was independently reimported and inspected. The native source
was saved and reopened before export. `runtime-inspection.json` passes six pose
comparisons, embedded images, UV coverage, finite/nondegenerate triangles, static
terrain and exact animation loop. `mechanical-inspection.json` checks attachments,
rope payout and upright bucket across all 193 frames (maximum error <0.000001 m).
The outer ground boundary is intentionally open; buried foundation anchors extend
below the ground plane. This is a terrain surface, not a watertight vessel.

Disposition: reviewed candidate, not owner-approved, not integrated. Previous
studies are preserved as superseded/held. No sprite promotion or native visual
acceptance is claimed. Actual baseline native tests exercised the six current
quarry recipes, fuel, blocked output, stop/restart and fixed north orientation;
those tests used the existing installed graphics. They must be rerun after the
new sprites are integrated. See copied baseline receipts; build logs remain local.

Next: genuine fixed-facing idle/working captures, current-mod integration,
actual graphical ground/idle/working evidence and operated-save reload, then
verified operational delivery and FMPL registration.
