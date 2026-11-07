# Accepted campfire — Factorio 2.1 production promotion

**User acceptance (2026-11-06, Sitka local):** the standalone `factorio_campfire_pipeline_test_0.1.1.zip` was installed under Factorio 2.1; user explicitly reported visual acceptance and successful in-game operation, including the four placement directions and idle/active states.

**The exact accepted 128px sprite bytes already exist in V12:** production `campfire-v12-idle.png` and `campfire-v12-burning.png` match SHA-256 values from the user's successful standalone test. They are not regenerated or stylized during promotion. The accepted icon is also byte-identical.

**Existing source:** `tanks_for_bob_fork_1.8.95/` is retained as the historical Factorio 2.0 release. It already references the accepted V12 art, but has a square collision box so it does not provide the four R-rotations observed in the separate test. Mod metadata still declares 2.0, correctly preventing it from being installed directly on 2.1.

**Production implementation:** run `python3 tools/art/build_accepted_campfire_21.py --output /tmp/tanks-campfire-21`. This stages a complete `tanks_for_bob_fork_1.8.96` 2.1 package from the versioned source, updating *only* metadata and the campfire's collision box to the non-square `{{-1.2,-1.1},{1.2,1.1}}`. It preserves the recipe, original burner energy source, operating sounds, icon, animated four-view graphics, and all other gameplay prototypes. No existing source or game sprite is overwritten. The original image files remain available for rollback.

**Explicit 2.1 validation gate:** `.github/workflows/campfire-approved-21.yml` builds this actual package and attempts to load it in the official Factorio 2.1.23 headless engine and run a short benchmark. If a wider 2.1 schema incompatibility in unrelated Tanks for Bob prototypes is found, preserve the package and diagnostics but do **not** claim a successful full-mod 2.1 runtime or publish to Mod Portal until corrected.

**Distribution:** GitHub Actions uploads `tanks_for_bob_fork_1.8.96.zip`, its SHA256 receipt and the engine logs as a production-candidate artifact. An accepted standalone test is not automatically equivalent to a successful whole-mod runtime test. No tag is rewritten; publication to the Factorio Mod Portal remains a separate approval and release action.
