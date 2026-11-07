# Accepted campfire — Factorio 2.1 production promotion

**User acceptance (2026-11-06, Sitka local):** the standalone `factorio_campfire_pipeline_test_0.1.1.zip` was installed under Factorio 2.1; user explicitly reported visual acceptance and successful in-game operation, including the four placement directions and idle/active states.

**The exact accepted 128px sprite bytes already exist in V12:** production `campfire-v12-idle.png` and `campfire-v12-burning.png` match SHA-256 values from the user's successful standalone test. They are not regenerated or stylized during promotion. The accepted icon is also byte-identical.

**Existing source:** `tanks_for_bob_fork_1.8.95/` is retained as the historical Factorio 2.0 release. It already references the accepted V12 art, but has a square collision box so it does not provide the four R-rotations observed in the separate test. Mod metadata still declares 2.0, correctly preventing it from being installed directly on 2.1.

**Production implementation:** run `python3 tools/art/build_accepted_campfire_21.py --output /tmp/tanks-campfire-21`. This stages a complete `tanks_for_bob_fork_1.8.96` 2.1 package from the versioned source, updating *only* metadata and the campfire's collision box to the non-square `{{-1.2,-1.1},{1.2,1.1}}`. It preserves the recipe, original burner energy source, operating sounds, icon, animated four-view graphics, and all other gameplay prototypes. No existing source or game sprite is overwritten. The original image files remain available for rollback.

**Explicit 2.1 validation gate:** `.github/workflows/campfire-approved-21.yml` builds this actual package and attempts to load it in the official Factorio 2.1.23 headless engine and run a short benchmark. If a wider 2.1 schema incompatibility in unrelated Tanks for Bob prototypes is found, preserve the package and diagnostics but do **not** claim a successful full-mod 2.1 runtime or publish to Mod Portal until corrected.

**Distribution:** GitHub Actions uploads `tanks_for_bob_fork_1.8.96.zip`, its SHA256 receipt and the engine logs as a production-candidate artifact. An accepted standalone test is not automatically equivalent to a successful whole-mod runtime test. No tag is rewritten; publication to the Factorio Mod Portal remains a separate approval and release action.

## Verified production implementation receipt — 2026-11-06 Alaska

- **User acceptance:** In-game Factorio 2.1 visual and functionality test of `factorio_campfire_pipeline_test_0.1.1.zip` passed, as explicitly reported by the user. This is evidence for the tested standalone mod and its exact sprite assets; it is not a claim that the user also tested the full Tanks package.
- **Promotion implementation commit:** [`ed8b6e76dbdd5c2e9778d610888e64b9328ea71b`](https://github.com/mrcalzon02/Tanks-for-bob-Fork/commit/ed8b6e76dbdd5c2e9778d610888e64b9328ea71b).
- **Official full-mod engine test:** [GitHub Actions run 42351190717](https://github.com/mrcalzon02/Tanks-for-bob-Fork/actions/runs/42351190717) **SUCCESS** on Factorio headless `2.1.23`. The actual `tanks_for_bob_fork` mod version `1.8.96` loaded during map creation and loaded again during the 300-tick benchmark. This confirms engine data-stage and headless runtime smoke success, not graphical rendering inside the full mod.
- **Distribution archive:** `tanks_for_bob_fork_1.8.96.zip`, SHA-256 `8ed3a4ddebeddef3811a8d1dd99ee9387701b993f493fe8aa82d3e43f0ce6ff3`. The build verifies the exact previously user-accepted 128px idle/burning atlas bytes and icon bytes before packaging and after extraction.
- **GitHub CI artifact:** `tanks-for-bob-1.8.96-factorio-2.1-accepted-campfire` (workflow run above) contains the installable ZIP, hash receipt, map-creation and benchmark logs, engine version and promotion receipt.
- **Rollback:** `tanks_for_bob_fork_1.8.95/` is preserved for 2.0. No release tag was moved, and no claim of automatic Factorio Mod Portal publication is made.
- **Remaining distinction:** Full-mod GUI/visual inspection should be performed with the 1.8.96 archive. The user already accepted the visually identical standalone test sprites on 2.1, and the entire production mod passed headless engine loading.
