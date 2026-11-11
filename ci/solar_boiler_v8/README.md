# Solar Boiler V8 — approved art, Factorio-specific pipe integration

This phase *integrates the user-approved floorless V8* into the existing
2.1 Tanks for Bob fork without altering geometry, tile occupancy, fluids,
recipes, or other approved structures.

- **Source:** verified Blender V8 + 68 frame hashes in
  \`models/island-survival/solar-boiler/generated-v8/\`
- **Target:** \`tanks_for_bob_fork_1.8.102\`, existing \`boiler/solar-boiler\`.
- **Target schema:** Factorio 2.1 \`BoilerPictureSet.pictures[cardinal].structure\`,
  not the generic assembler/furnace \`graphics_set\`.
- **Renderer:** 16 frames per orientation at 8 FPS, 256px original source.
  Exact 8×8 atlas already exists; copy standard 128px, 64px review and 256px
  high-res atlases into mod graphics. Use high-res 256px natively.
- **Scale:** derive from \`32 * camera.ortho_scale / 256\` (~0.55625),
  **shift** from the fixed 45° Blender camera ground-origin projection
  (~(0,-0.65761) tiles). Both are transparent/calibratable in generated
  boiler-only Lua; do not change the three engine fluid-cell coordinates.
- **Directional correction:** Blender authored yaw +90 points west; Factorio
  east-facing picture uses Blender d03 (270°), west uses d01 (90°).
- **Connections:** western (-1,0.5) and eastern (1,0.5) water ports and
  northern (0,-0.5) steam outlet, exactly as the current prototype.
- **No base plate:** all 11 slab/paver objects remain absent.
- **Non-destructive:** unchanged V8 frames and .blend; new versioned graphics.
  Leave existing workbench and cooking-fire modules untouched.

## Tests and explicit boundary

The single existing \`factorio-art-production.yml\` job packages sprites,
checks file/hash/alpha/frame/viewport correspondence, checks projected flange
positions, Lua-compiles the boiler-specific registration, runs pinned official
Factorio 2.1.24 **headless** with four placed boilers and 12 adjacent pipes,
and publishes via normal fast-forward to \`main\` after passing.

This proves *prototype and pipe fluid connectivity*. It **cannot prove visual
alignment**: headless Factorio has no 2D client screenshots. The generated
\`pipe-placement-qa.png\` deliberately distinguishes Blender-projected
socket mouths from native tile-edge pipe positions, reports residual pixels
for every rotation, and is NOT a fake engine screenshot. Actual in-game client
visual acceptance requires placing pipes on the west/east/north ports, rotating
all four directions, checking floor overlays, and inspecting the transition at
normal and zoomed views. If a visible gap is found, change only bounded
sprite scale/shift or author a specific pipe-socket overlay; do not move the
Factorio native fluid connections or rebuild the approved geometry.

A successful CI run is *integration candidate ready for client visual QA*,
not a completed in-game screenshot sign-off.
