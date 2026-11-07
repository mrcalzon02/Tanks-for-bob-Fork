# Pit Kiln V6 — final motion correction: inward slide and tipping pitch

The user specified **lateral motion INTO the pit with a slight downward pitch**,
not a spinning-top yaw. Preserve the entire wooden tray and all four wet bricks
as ONE rigid moving group. No per-brick animation, no rotation about vertical Z.

V6 reuses the full V5 Blender scene and all six real Campfire V9 flame meshes,
their authored animations, the additional V4 crackles and two embers.
The ten bricks placed along the inner firing bank remain still.

The existing shared tray controller is reset to remove V5's faulty Z spin.
The board slides up to **0.165 Blender units along the vector from the board
toward the center of the pit**, moves down 0.018 units and rotates **6.4°
around the horizontal tangent to the pit lip** so its inner edge dips.
The envelope is 0→1→0 in 16 frames, 8 FPS, exact seam closure at frame 97.

The build fails unless all four cardinal orientations have:
- Actual center shift inward of >=0.12 model units and >=5.5 pixels at 256px.
- The inner edge at least 0.018 model units lower relative to the outer edge.
- Near-zero unwanted transverse drift and absolutely no local yaw.
- Five actual children on the one keyed rig: board + four bricks.
- No independent brick animation actions.
- Original keyed campfire fire, all 68 RGBA frames and 16-frame loop preserved.

This final pass runs in `.github/workflows/pit-kiln-v6.yml`.
It saves an editable Blender master and all four GIF previews at
`models/island-survival/pit-kiln/generated-v6/`, and packages the 64/128/256px
Factorio-ready atlases, icon candidate and Lua graphics_set at
`models/island-survival/pit-kiln/production-v6/`.

No live Factorio prototype or Mod Portal release is modified without art approval.
All earlier revisions remain preserved and immutable.
