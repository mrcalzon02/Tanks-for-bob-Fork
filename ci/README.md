# Tanks for Bob — one compatibility profile

Exactly **one GitHub Actions job** and **one Factorio 2.0.77 profile**:
Base + Elevated Rails + Quality + Space Age + `tanks_for_bob_fork`.

The single job runs source/asset validation, live recipe/technology audits,
vehicle and ammunition checks, 1,200 engine ticks, real damage response,
ammunition insertion, and private dedicated-server startup. All evidence
is collected in one diagnostic artifact.

`ci/run_official_suite.py` is the runner; `ci/stage_profile.py` stages
an isolated mod copy. This is the currently supported release's Factorio 2.0
full-expansion smoke test, **not a complete cross-version compatibility
matrix**. Historical Factorio 2.1 checks remain documented but are not run.

Only genuine engine/test-harness failures block release checks; optimistic
progression and weapon registration findings remain diagnostic until validated
as engine failures. Publishing is gated on the same successful job and uploads the separately versioned v1.8.95 ZIP to the official Factorio Mod Portal and GitHub release using the Actions secret `FACTORIO_MOD_UPLOAD_KEY`. Earlier v1.8.93 and v1.8.94 release assets remain unchanged.

## Manufacturing feasibility checks (v1.8.95)

The existing data-stage audit now includes `ci/recipe_machine_audit.lua`
inside the **same one job, one profile**, validating nine recipe selections
across the Workbench, Cooking Fire and Tank Ammunition Assembler. It checks
machine ingredient limits, exact recipe category and fluid-port directions.
This does not substitute for a player-paced production/research playthrough.
