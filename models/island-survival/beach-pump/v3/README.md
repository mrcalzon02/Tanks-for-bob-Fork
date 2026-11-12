# Beach Pump V3 — independent visual and animation rework

Audited against the actual SHA-published V2 Blender four-facing contact proof. V2
was technically validated but looked chunky: a dense 8-plank dock grid, cuboid
wheel paddles, oversized hubs, rigid cylinder trough water and bead cylinders
that reset during the water loop.

V3 is a candidate-only, reproducible *editable Blender* source, based on V2's
actual source builder and V1's pinned FMPL materials, camera and native fitting.

Changes:
- Eight **20-vertex concave/tapered timber bucket meshes** replace cube paddles.
- Reduce deck grille to five spaced boards (four independent footings preserved).
- Less oversized hub/gear casing; larger readable wheel rims.
- Finer continuous rolled edge around actual 580-vertex screw.
- Thin mesh water stream, four moving glints and round falling water beads.
- Water pockets fade out/in near their wrap; linear shaft and water keyframes.
- Four-direction real Blender idle/working contact sheet and full 16-pose
  **8 FPS** motion-review.gif, derived strictly from native rendered frames.
- Native .blend reopen, 68 frame checks, stationary output connector,
  8 curved buckets, moving crank, moving stream, loop seam and six atlas QA.

**No Factorio game graphics changed or approved.** The source prototype
remains shoreline-pulling `offshore-pump/beachpump`, 0.01 water/tick,
north water source, one south pipe connection (0,+0.25), and no energy cost.

Run: build_beach_pump_v3.py, verify_beach_pump_v3.py,
make_proof_sheet.py, pack_verified_atlases.py. Compare with V2 source/art
before approving. Human visual review and actual Factorio client checks
still outstanding.
