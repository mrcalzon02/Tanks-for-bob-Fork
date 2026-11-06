# Tanks for Bob — official Factorio matrix

This repository runs **ONE GitHub Actions job** (`.github/workflows/vanilla-factorio.yml`) which executes all 12 isolated compatibility profiles sequentially for
vanilla, Elevated Rails, Quality, Recycler (Factorio 2.1), and Space Age.
See `docs/compatibility/OFFICIAL_MOD_SUPPORT.md` for the full 12-profile
matrix and engine-version differences.

A clean isolated mod list contains only the selected official engine mods
plus `tanks_for_bob_fork`. There are no third-party mod downloads and
no dependency on Tech Priests.

**Testing tools**

- `ci/validate_mod.py`: scans latest source package, active Lua requires,
  210 recipe and 88 technology declarations, assets, dormant files and
  duplicate definitions. Records JSON artifact even on failure.
- `ci/stage_profile.py`: creates disposable per-engine test install,
  exact official allowlist, CI-only Lua harness, and a source manifest.
  2.1 tests temporarily set `factorio_version` to 2.1 in this staged copy.
- `ci/data_audit.lua`: verifies declared recipes/technologies are present
  in Factorio, technology prerequisites, cycles, unlock gaps, crafting
  categories and recycling guardrails.
- `ci/runtime_harness.lua`: checks enabled mod profile, runtime vehicle
  registry and real vehicle instantiation after simulation ticks advance.
- `ci/server_smoke.py`: boots a real private headless multiplayer server.

CI uploads every test's Factorio create/benchmark/server logs, mod list,
profile summary and the independent static source audit.

Tests pass at most **smoke-test release criteria**: actual client rendering,
combat simulation, complete resource/progression reachability and two-client
join/migration tests still require separate acceptance.

Artifacts and workflow:
https://github.com/mrcalzon02/Tanks-for-bob-Fork/actions/workflows/vanilla-factorio.yml

## Single-job suite (replaces the 13-job fanout)

`ci/run_official_suite.py` runs the static source audit plus all 12
headless Factorio profiles in one Actions job. The two pinned engine
distributions are downloaded once per run and reused across profiles.
Individual profile mod lists, logs, benchmark results, private-server
startup checks and warnings are isolated under a **single artifact**:
`tanks-official-factorio-one-job-audit`.

All 12 profiles are attempted even if another fails; the one job fails
if **any** required profile or the source audit fails. This removes the
13-job Actions clutter without reducing compatibility checks.
Quality/Recycler/Space Age combinations and 2.1 metadata caveats remain.
