# Tanks! for Bob Fork v1.8.93

Factorio **2.0** mod with specialized vehicles, turrets/guns, ammunition, intermediary production chains and extra technologies.

## Compatibility and current test evidence

**Verified:** the [official-mod compatibility suite](https://github.com/mrcalzon02/Tanks-for-bob-Fork/actions/workflows/vanilla-factorio.yml) verifies the following **12 Factorio engine configurations** plus a static source audit inside **ONE GitHub Actions job**:

| Engine | Official mod combination (besides `core`) |
| --- | --- |
| 2.0.77 | Base |
| 2.0.77 | Base + Elevated Rails |
| 2.0.77 | Base + Quality |
| 2.0.77 | Base + Elevated Rails + Quality |
| 2.0.77 | Base + Elevated Rails + Quality + Space Age |
| 2.1.23 | Base |
| 2.1.23 | Base + Elevated Rails |
| 2.1.23 | Base + Recycler |
| 2.1.23 | Base + Quality + Recycler |
| 2.1.23 | Base + Elevated Rails + Quality + Recycler |
| 2.1.23 | Base + Elevated Rails + Recycler + Space Age |
| 2.1.23 | Base + Elevated Rails + Quality + Recycler + Space Age |

**Important:** the actual mod in this ZIP declares `factorio_version: "2.0"`. The Factorio 2.1 checks change metadata in **temporary CI copies only**. This ZIP is **not** a separately released 2.1-compatible package. Recycler is a separate official mod in 2.1 and is contained in Quality in 2.0. Official modules other than Base are optional; no third-party mod compatibility is claimed.

### What the headless tests verified

- **210** declared recipes and **88** technologies registered; **0** source-declared disabled recipes lacking a technology unlock.
- **210/210** recipes optimistically reachable via ingredient graph (diagnostic **only**, not evidence of research/factory feasibility).
- **13** tank-vehicle prototypes; **26/26** mounted gun/ammunition-category links; **13/13** ammo prototypes with crafting outputs.
- **8** real vehicles spawned after tick 300; **1,250 → 0** hit points on a vehicle using Factorio's native damage API at tick 600.
- **7/7** surviving tanks accepted assigned ammo at tick 900; the eighth was destroyed in the damage test.
- Deterministic 1,200-tick simulation, real data-stage validation and a private dedicated-server startup in each of 12 profiles.
- Static checks for active Lua imports, graphics paths, recipes, and technologies.

**Not verified:** actual shooting and projectile impacts, player driving, in-client visuals, complete buildable progression, working recall controls, live two-client synchronization, save migration or fleet performance. The recall event handlers in `control.lua` are disabled/commented out as of this version.

**Expanded documentation:** [GitHub repository README](https://github.com/mrcalzon02/Tanks-for-bob-Fork#readme), [official-mod support](https://github.com/mrcalzon02/Tanks-for-bob-Fork/blob/main/docs/compatibility/OFFICIAL_MOD_SUPPORT.md), [full audit](https://github.com/mrcalzon02/Tanks-for-bob-Fork/blob/main/docs/compatibility/CURRENT_STATE_AUDIT.md), and [one-job CI run logs](https://github.com/mrcalzon02/Tanks-for-bob-Fork/actions/workflows/vanilla-factorio.yml).

## Vehicle families and equipment

- Autocannon tank — fast conventional tank with two tiers.
- Flame tank — flamethrower tank in two tiers.
- Super tank — heavy, all-round variant.
- Rocket tank — fast long-range rocket launcher.
- Additional grenade, mine-layer and specialized variants.
- Cannons, autocannons, flamers, rockets, mine launchers and heavy machine guns.

Recall tokens and teleporter-related code are present, but **do not assume recall currently works**.

## Notes on original balance

Designed partly for demanding enemy-overhaul scenarios; may be overpowered in unmodified vanilla. Compatibility with Bob's Enemies, Natural Evolution Expansion, AAI or Mechanicus is **not part of the official-module matrix**.

## Version history (selected)

- **1.8.93:** Factorio 2.0 compatibility fixes, case-correct resources, updated intermediate chains; full official-module CI and runtime audit.
- **1.8.91:** Factorio 2.0 conversion, turret changes, intermediates and technology chain expansion.
- **1.8.86:** Legacy high-resolution asset updates.
- **1.8.84:** Additional recipes and technologies.
