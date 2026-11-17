# Steam Compressor V2 — owner-identified barrel source

The owner identified `models/island-survival/steam-condenser/v1/build_steam_condenser_v1.py`
as the intended half-finished compressor. Its saved `v1-production01` Blender
source is preserved unchanged. The V2 derivative preserves 79 original meshes,
the stave pressure vessel, hoops, timber frame, gauge and native socket meshes.
The earlier Tech-Priests compressor derivative was the wrong source and is
quarantined; its native tests are not this asset's completion evidence.

V2 adds a supported four-arm crank, a rigid rod, guided pressure piston, two
clay fireboxes and a removable copper canister. The blue condensate and falling
water effects were removed. The machine uses Tanks' existing chemical burner,
`Charged-Canister` and `UnCharge-Canister` recipes, technology and 3×3 footprint.
There are no balance, recipe or fluidbox changes.

The saved source reopens with packed image materials. The actual animated GLB
reimports with 21 embedded images, no missing UVs or degenerate triangles, and
six matching sampled poses. All 97 source frames pass rigid-rod, attached-joint
and fixed-socket checks. Capture has four genuine idle images plus 64 genuine
working images, packed into six verified sheets; the runtime uses 16 frames
per facing at four frames per second. The item icon uses one canonical idle view.

Actual Factorio 2.1.24 tests use 24 machines in four directions and both real
recipes, with 20 ordinary player-grid pipe connections. Checks cover item
placement, technology unlock, steam charging/recovery, chemical fuel, no-fuel,
idle, full item output, full fluid output, stop/restart and unblocking. A real
client created the completed-state save; its subsequent native reload reports
`complete=true`. Twelve client images cover working, idle and a later working
pose. The tested mod copies match the active Lua and asset inputs by hash.

This is delegated operational close-enough review, not a claim of individual
owner visual approval. Tiny tooling and firebox detail can remain simple.
No Mod Portal release or installation into the user's full mod pack is claimed.
The original condenser-labelled model remains unapproved for the separate
`steam-condenser` prototype.

Source and tooling: `models/island-survival/steam-compressor/v2/`.
Current source/export/frames: `models/island-survival/steam-compressor/candidates/v2-barrel02/`.
Atlas pack: `models/island-survival/steam-compressor/candidates/v2-atlas02/`.
See `FMPL_MODEL.json`, `engine-receipt.json`, `capture-receipt.json`,
`native-runtime.json`, `source-snapshot.json` and `visual-review.json` for receipts.
