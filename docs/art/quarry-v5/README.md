# Quarry V5 operational delivery

The tracked starter quarry was developed into a supported timber excavation
hoist with bored bearings, a winding drum and continuous taut rope, upright
lifting bucket, rigid engine crank/rod/piston, travelling belt and a contained
brick firebox/copper pressure jacket. Added useful material handling and tools.
Owner feedback drove detailed construction, softer natural edges and continuous
terrain roots instead of placed boulders. The excavation floor is nearly flush
with native ground; deliberate worked cleavage remains distinct from the slope.

Final editable source and inspected GLB are in
`models/island-survival/quarry/candidates/v5-rooted04`. The source is packed,
saved/reopened and has one canonical camera. Six source/export pose comparisons
and all 193 mechanism frames pass. Exported ground alpha is preserved in COLOR_0;
older export studies remain held. Fresh 17-frame capture/atlas receipts are in
v5-rooted04 and v5-atlas02. They are byte-identical to the sprites tested natively.

The real quarry is a fixed-north 3x3 chemical-burner assembling machine with no
fluid connections. All six current quarrying recipes were tested in 36 machines:
stone, stone-with-tools (tool returned in output), iron/copper from brick, and
iron/copper from stone-brick. Ordinary placement, fuel/no fuel, no recipe, blocked
output, stop/restart and unblocking passed. The actual native blocked assembler
may report progress=1 and is_crafting=true; unchanged outputs/progress are checked
before unblocking, without changing gameplay.

Twelve genuine Factorio 2.1.24 client screenshots show current graphics on grass,
actual recipe operation, idle, no fuel, blocked and restarted states. The legacy
middle-of-sprite smoke emitter was corrected to the measured firebox flue outlet.
The completed operated save is included; its 36 frozen inventory snapshots survive
reload. Freeze occurs only after operational tests, to verify exact persistence.
Headless native engine/reload receipts, graphical log and operated reload receipt
are adjacent. The earlier baseline receipt applies to old graphics and remains
explicitly labelled baseline.

Delegated review: operational and close enough, not individual owner approval.
No recipe, progression, fuel balance, footprint or rotation behavior changed.
No full-user-mod-pack installation or Mod Portal publication claimed.
