# Tanks! for Bob Fork 1.8.94

This is a **Factorio 2.0** release of the existing Tanks for Bob Fork mod.
It includes the accumulated compatibility repairs, dedicated tank variants,
special weapons, ammunition, recipes and technology chains.

## Current automated compatibility check

**One GitHub Actions job, one real Factorio 2.0.77 headless installation:**
Base + Elevated Rails + Quality + Space Age + this mod.

The test performs real data-stage loading, source and graphics checks,
recipe and technology registry diagnostics, ammunition/weapon compatibility
checks, deterministic save creation, 1,200 simulated ticks, tank spawning,
real hit-point damage, tank ammo insertion, and private server startup.

Latest test runs: https://github.com/mrcalzon02/Tanks-for-bob-Fork/actions/workflows/vanilla-factorio.yml

Earlier tests of other official-module combinations and Factorio 2.1
used temporary CI metadata; they are preserved in the repository audit,
**not** repeated in the current workflow. This ZIP declares
`factorio_version: 2.0` and is not a Factorio 2.1 release.

Test limitations: real weapon firing and ammo consumption, manual driving,
rendering in a graphical client, full research progression, recall controls,
live two-player synchronization, and save migration remain unverified.
Current recall event registrations are commented out.

## Contents

- Fast autocannon, flame, grenade, rocket, mine and super-tank variants.
- Custom weapons and 13 ammo prototypes; 26 weapon-slot ammo-category links.
- 210 declared recipes and 88 technologies.
- Compatibility with Base and optional official Factorio 2.0 expansions.

For full diagnostics, see:
https://github.com/mrcalzon02/Tanks-for-bob-Fork/blob/main/docs/compatibility/CURRENT_STATE_AUDIT.md

This version increments **1.8.93 → 1.8.94** for Mod Portal
distribution. It does not claim newly repaired gameplay features.

## Previous versions

- **1.8.93**: official-module compatibility repairs and testing foundation.
- **1.8.91**: Factorio 2.0 conversion and intermediary-chain expansion.
