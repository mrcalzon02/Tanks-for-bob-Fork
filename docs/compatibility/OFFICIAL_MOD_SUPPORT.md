# Official Factorio compatibility policy — Tanks for Bob Fork

Updated: 2026-11-05. Source mod: `tanks_for_bob_fork_1.8.93`.

## Supported first-party mod IDs

| Official mod | Factorio 2.0.77 | Factorio 2.1.23 | Default integration policy |
| --- | --- | --- | --- |
| `core` | Bundled | Bundled | Always built in, cannot be disabled |
| `base` | Bundled, required | Bundled, required | Required dependency |
| `elevated-rails` | Optional | Optional | Supported when enabled |
| `quality` | Optional; contains the original recycler | Optional | Supported when enabled |
| `recycler` | Not a separate bundled mod | Optional, independent official mod | Supported when enabled |
| `space-age` | Official expansion, includes necessary components | Official expansion; Quality optional | Supported when enabled |

The first-party modules are **optional integrations**, not mandatory DLC purchases.
The `info.json` dependency list declares the official ones as optional, preserving
the vanilla base-game-only installation. The fork's original incompatible ancestor
(`tanks_for_bob_`) remains excluded.

In Factorio 2.1, the recycler was split out from Quality. Both Space Age without
Quality and the full Space Age installation are included in the testing matrix.

## Reproducible headless profile matrix

The workflow `.github/workflows/vanilla-factorio.yml` checks 12 isolated profiles:

| Engine | Profile | Official modules explicitly enabled |
| --- | --- | --- |
| 2.0.77 | base | base |
| 2.0.77 | rails | base, elevated-rails |
| 2.0.77 | quality | base, quality |
| 2.0.77 | rails-quality | base, elevated-rails, quality |
| 2.0.77 | space-age | base, elevated-rails, quality, space-age |
| 2.1.23 | base | base |
| 2.1.23 | rails | base, elevated-rails |
| 2.1.23 | recycler | base, recycler |
| 2.1.23 | quality | base, quality, recycler |
| 2.1.23 | rails-quality | base, elevated-rails, quality, recycler |
| 2.1.23 | space-age-no-quality | base, elevated-rails, recycler, space-age |
| 2.1.23 | space-age-full | base, elevated-rails, quality, recycler, space-age |

The `core` module is implicit. No Tech Priests, Bob's Enemies, AAI,
Mechanicus or other third-party mod is loaded by these tests.

## What every runtime job checks

1. Exact pinned binary and strict official mod allowlist.
2. Real Factorio data-stage validation; declared recipes and technologies,
   missing unlocks, prerequisites, category and crafting-machine coverage.
3. Deterministic map creation from seed `907260`.
4. 1,200 actual simulation ticks, mod-specific entity and recipe runtime
   registries, vehicle instantiation.
5. Real private headless multiplayer server reaching hosting-ready status.
6. Logs, mod-list, static audit and profile summary retained on every run.

The standalone source audit additionally counts active vs dormant Lua, checks
case-sensitive modules and graphics paths and lists unique missing artwork.

## Versioning and release truthfulness

The checked-in version 1.8.93 still **declares `factorio_version: 2.0`**.
Factorio rejects a 2.0-tagged mod as a 2.1 release without updating metadata.
To audit 2.1 API behavior, the workflow changes `info.json` *only inside a
disposable CI copy*; this must not be presented as a released 2.1 package.
Once the 2.1 profiles pass, a separately versioned 2.1-targeting package
can be prepared for release. Do not silently retag 1.8.93.

A green headless test is not a substitute for manual sprite rendering,
driving controls, projectile combat, every recipe's full production path,
or real multiplayer with multiple connected clients.

## References

- Official Factorio 2.1 stable announcement: https://factorio.com/blog/post/fff-449
- Factorio official mod metadata: https://lua-api.factorio.com/latest/auxiliary/mod-structure.html
- CI workflow: https://github.com/mrcalzon02/Tanks-for-bob-Fork/actions/workflows/vanilla-factorio.yml
- Detailed current-state audit: [CURRENT_STATE_AUDIT.md](CURRENT_STATE_AUDIT.md)


## Current verified headless compatibility result (2026-11-05)

All **12 of 12** runtime matrix jobs passed against the pinned engines
2.0.77 and 2.1.23 in:
https://github.com/mrcalzon02/Tanks-for-bob-Fork/actions/runs/42133070510

This includes 210 source-declared recipes, 88 source-declared
technologies, 0 source recipes disabled without a tech unlock,
and 8 instantiated vehicles per runtime harness. It is a headless proof,
not a claim of client graphics or complete gameplay correctness.

The original missing high-resolution turret image was subsequently
restored from a prior package version containing the identical XCF source.
The current-state audit records the remaining client and progression
coverage gaps.
