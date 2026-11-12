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

## Genuine client screenshots — Windows graphical session

The user-approved floorless Blender V8 is integrated and the official Factorio
2.1.24 headless connectivity smoke **passed** (four rotations, twelve
physically connected fluid pipes). This is not equivalent to a native graphics
comparison: `game.take_screenshot` requires the **full graphical client**.

**Confirmed block on OLD-CORE30-homebrew:** the GitHub Actions runner is a
Windows service in Session 0. Native Factorio 2.1.24 GUI startup returned
`Failed to get SDL_DXGIGetOutputInfo` and
`DXGI_ERROR_NOT_CURRENTLY_AVAILABLE (0x887a0022)` despite detecting the
NVIDIA GeForce GTX 1660 SUPER. Steamworks `steam_appid.txt` in isolated
per-run scratch eliminated the preliminary Steam relaunch but cannot create
a Direct3D output in Session 0. These are real engine logs, and **zero of
sixteen screenshots** exist from that attempt. See
[the worker run](https://github.com/mrcalzon02/Dens-Mortis/actions/runs/43133825717)
and [tracking issue #4](https://github.com/mrcalzon02/Tanks-for-bob-Fork/issues/4).

### One-shot interactive capture

Sign in to an **ordinary visible Windows desktop on OLD-CORE30** and open
PowerShell there (not inside the GitHub runner service). Within a current
Tanks-for-bob-Fork clone on `main`, use:

```powershell
git pull --ff-only
powershell -NoProfile -ExecutionPolicy Bypass -File .\ci\solar_boiler_v8\launch_from_interactive_desktop.ps1 -FactorioExe 'D:\SteamLibrary B\steamapps\common\Factorio\bin\x64\factorio.exe'
```

The one-shot launcher:
- checks the process is **not Session 0**, refuses to interfere with an
  already running Factorio client, and verifies source/graphics presence;
- uses the actual full installed Factorio 2.1 client with a temporary
  mod directory, Steamworks app-id and user-data directory (not production
  saves or installed mods);
- places eight boilers and 24 real pipes in the engine, takes sixteen
  true game PNGs across four rotations, two terrain types and two zooms
  (true 1.0x/100% game scale and 2.9x inspection close-up);
- verifies PNG headers, sizes, render variation, engine log markers and
  file SHA-256 values before marking the screenshot capture successful;
- writes `factorio-client-pipes-all-four.png` **containing all sixteen actual screenshots**,
  `client-vs-approved-v8.png` and a provenance receipt into a unique
  `generated-v8/visual-client-<UTC timestamp>` directory.

If the interactive process reports a client startup, scenario, Lua,
screenshot or connection failure, the launcher preserves that actual
error and **does not** generate artificial evidence. Publication of real
screenshots and human visual pipe-alignment acceptance remain pending
until these files exist and are reviewed. The native 3×2 tile footprint
and all three actual fluid-box coordinates remain locked.
