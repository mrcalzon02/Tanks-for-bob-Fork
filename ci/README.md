# Tanks for Bob — one current compatibility profile

The existing manually dispatched workflow runs **one job and one Factorio
2.1.24 profile**: Base + Elevated Rails + Recycler + Quality + Space Age,
plus the latest versioned Tanks for Bob source. Ordinary commits do not start
this workflow. The audit workflow does not publish releases.

The source selector validates the highest versioned source folder against its
info.json. Staging preserves the actual Factorio 2.1 metadata, copies the source
into a disposable directory, and adds diagnostic instrumentation there. It
preserves production data-final-fixes and startup initialization.

## Run the same suite locally

```bash
python3 ci/run_official_suite.py \
  --binary-21 /path/to/factorio/bin/x64/factorio \
  --work /tmp/tanks-suite \
  --output /tmp/tanks-evidence
```

The runner performs source/asset validation, real data-stage recipe and
technology checks, save creation, 1,200 simulation updates, damage/ammunition
inventory checks, native player progression tests and private server startup.
Evidence is collected in one result directory and one workflow artifact.

## Progression coverage

- Source-driven inventory includes all active ammunition declarations,
  including Sharp-stick in item.lua. New declarations can expand the manifest;
  the test does not impose a maximum recipe or ammunition count.
- The starting wooden weapon must be handcraftable. Ammunition starts locked
  and its technology is a root scripted material discovery without lab cost.
- Native Factorio 2.1.24 test mode supplies a real player for tree mining,
  driftwood handcrafting, spear crafting and wood-quality acquisition checks.
  A separate diagnostic mod observes events without replacing production
  handlers.
- Eleven named machine/category/ingredient/fluid regression cases cover the
  original Workbench, Cooking Fire and ammunition assembler repairs plus the
  saline and bioceramic kiln recipes. The native fixture also operates the
  two kilns with seeded materials and fuel and checks their actual products.
- Broader ingredient closure, prototype relationships and graph findings remain
  diagnostics; they do not certify driving/firing all vehicles, a complete
  factory playthrough, two-client multiplayer, terrain or balance.

## Optional historical save upgrade test

The normal job needs no old artifact download or Mod Portal credentials. When
an exact previously published 1.8.100 ZIP is available, pass it explicitly:

```bash
python3 ci/run_official_suite.py \
  --binary-21 /path/to/factorio/bin/x64/factorio \
  --baseline-package /path/to/tanks_for_bob_fork_1.8.100.zip \
  --work /tmp/tanks-suite \
  --output /tmp/tanks-evidence
```

The independent fixture can also be run with
`ci/progression_runtime_runner.py --binary ... --source ... --output ...`;
its optional old-package argument is `--legacy-package`. Source may be the
current directory or an exact installable ZIP. Test receipts identify the
engine, package/source fingerprint, enabled modules and observed assertions.

The legacy fixture serializes a normal scenario save with completed,
unresearched and partly completed wooden research, then upgrades it. Saved
wood is held in a real character inventory and discovered when the native
test player joins that character. This proves saved inventory and joining;
offline-player discovery during configuration change remains a focused unit
test. The fixture reports this distinction explicitly.

## Complete progression map

`ci/progression_order_audit.py` consumes a real Factorio `--dump-data` JSON
snapshot and the selected source declaration manifest. It records every custom
recipe's ingredients, products, unlocks and compatible crafters, plus every
custom technology's costs/triggers, prerequisites and effects. The custom
research-material ancestry check explicitly excludes proof of vanilla
manufacturing, machine construction, power and logistics.

The classified 8 November audit and before/after inventories are in
[docs/compatibility](../docs/compatibility/PROGRESSION_ORDER_AUDIT_2026-11-08.md).

## Packaging

`python3 ci/package_mod.py --output dist` builds the same selected source into
a deterministic versioned ZIP and a SHA-256 file. It verifies archive contents
against source and refuses to overwrite an existing package. It does not
upload, retag or publish anything.
