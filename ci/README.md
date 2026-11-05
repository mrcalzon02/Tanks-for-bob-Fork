# Tanks for Bob: independent vanilla Factorio CI

The workflow in .github/workflows/vanilla-factorio.yml loads the highest
versioned tanks_for_bob_fork_X.Y.Z folder (currently 1.8.93) into a fresh
Factorio 2.0.77 headless instance with **base + tanks_for_bob_fork only**.
No Tech Priests, optional or third-party mods are installed.

The source audit checks package metadata, active literal Lua require paths
(case-sensitive), local asset references and repeated recipe declarations.
The game audit injects a data-final-fixes audit into a disposable installed
copy. It tests technology recipe unlocks, prerequisites, tank recipes,
vehicle entities and machine support for tank crafting categories.

A deterministic save is created, benchmarked for 1200 genuine ticks,
tested for vehicle instantiation, and started as a private dedicated server.
Raw logs and the static JSON audit are retained as workflow artifacts.
Both jobs run independently, so a static failure does not hide an engine
loading failure. Runs are triggered by main pushes, pull requests, manual
dispatch, and a weekly scheduled regression.

Known limitations: this is smoke/prototype testing, not proof of full
recipe production reachability, multiplayer correctness, driving, combat
balance, or visual rendering. Disabled tank recipes without technology
unlocks generate diagnostic warnings rather than a release-blocking fail.
