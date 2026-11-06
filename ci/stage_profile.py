#!/usr/bin/env python3
"""Stage one Tanks for Bob package with only a chosen set of official Factorio mods.

The staged copy is disposable; Factorio 2.1 testing changes metadata only in CI.
"""
import argparse
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OFFICIAL_20 = {"base", "elevated-rails", "quality", "space-age"}
OFFICIAL_21 = OFFICIAL_20 | {"recycler"}
PROFILES = {
    "base": {"base"},
    "rails": {"base", "elevated-rails"},
    "quality": {"base", "quality"},
    "rails-quality": {"base", "elevated-rails", "quality"},
    "recycler": {"base", "recycler"},
    "space-age": {"base", "elevated-rails", "quality", "space-age"},
    "space-age-no-quality": {"base", "elevated-rails", "recycler", "space-age"},
    "space-age-full": {"base", "elevated-rails", "quality", "recycler", "space-age"},
}
def selected_source():
    versions = []
    for path in ROOT.glob("tanks_for_bob_fork_*"):
        m = re.fullmatch(r"tanks_for_bob_fork_(\d+(?:\.\d+)+)", path.name)
        if path.is_dir() and m:
            versions.append((tuple(int(p) for p in m.group(1).split(".")), path))
    if not versions:
        raise ValueError("No versioned Tanks for Bob mod source folder")
    return max(versions)[1]

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--engine", choices=["2.0.77", "2.1.23"], required=True)
    p.add_argument("--profile", choices=sorted(PROFILES), required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--bobs-mods-dir", type=Path, default=None)
    args = p.parse_args()
    enabled = set(PROFILES[args.profile])
    is_21 = args.engine.startswith("2.1.")
    available = OFFICIAL_21 if is_21 else OFFICIAL_20
    if not enabled <= available:
        raise SystemExit("Invalid engine/profile pair: " + args.engine + " / " + args.profile)
    if is_21 and "quality" in enabled:
        enabled.add("recycler")
    if is_21 and "space-age" in enabled:
        enabled.update(["recycler", "elevated-rails"])
    if not is_21 and "space-age" in enabled:
        enabled.update(["quality", "elevated-rails"])
    source = selected_source()
    dest = args.output / "tanks_for_bob_fork"
    args.output.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(source, dest)
    bob_versions = {}
    if args.bobs_mods_dir is not None:
        # This directory must have been downloaded and hash-verified by
        # ci/fetch_bobs_mods.py in the very same CI run.
        lock = json.loads((ROOT / "ci" / "bobs_versions.json").read_text(encoding="utf-8"))
        if lock["factorio_major"] != "2.0" or lock["engine"] != args.engine:
            raise ValueError("Bob pin manifest / selected engine mismatch")
        bob_versions = lock["mods"]
        found = list(args.bobs_mods_dir.glob("*.zip"))
        if len(found) != len(bob_versions):
            raise ValueError("Incomplete pinned Bob-family ZIP staging directory")
        for mod_name, version in sorted(bob_versions.items()):
            archive = args.bobs_mods_dir / f"{mod_name}_{version}.zip"
            if not archive.is_file():
                raise ValueError("Required pinned Bob ZIP absent: " + archive.name)
            shutil.copy2(archive, args.output / archive.name)
        enabled.update(bob_versions)
    metadata_path = dest / "info.json"
    info = json.loads(metadata_path.read_text(encoding="utf-8"))
    if info["name"] != "tanks_for_bob_fork":
        raise ValueError("Wrong source mod identity")
    if is_21:
        # Factorio refuses to load a 2.0-declared mod on a 2.1 engine.
        # CI probes 2.1 without falsely claiming the released 2.0 package works.
        info["factorio_version"] = "2.1"
        info["dependencies"] = [
            dep.replace("base >= 2.0", "base >= 2.1")
            for dep in info.get("dependencies", [])
        ]
        metadata_path.write_text(json.dumps(info, indent=2) + "\n", encoding="utf-8")
    # Keep the real mod's data-final-fixes.lua (e.g. Bob compatibility
    # adapters) active in CI. Stage the audit as a separate module instead of
    # overwriting the production file and silently disabling compatibility.
    (dest / "ci_data_audit.lua").write_text(
        (ROOT / "ci" / "data_audit.lua").read_text(encoding="utf-8"),
        encoding="utf-8"
    )
    final_fixes = dest / "data-final-fixes.lua"
    original_final_fixes = (
        final_fixes.read_text(encoding="utf-8") if final_fixes.exists() else ""
    )
    final_fixes.write_text(
        original_final_fixes.rstrip() + '\n\nrequire("ci_data_audit")\n',
        encoding="utf-8"
    )
    (dest / "ci_runtime_harness.lua").write_text(
        (ROOT / "ci" / "runtime_harness.lua").read_text(encoding="utf-8"),
        encoding="utf-8"
    )
    for audit in ("progression_audit.lua", "weapon_audit.lua", "recipe_machine_audit.lua"):
        (dest / ("ci_" + audit)).write_text(
            (ROOT / "ci" / audit).read_text(encoding="utf-8"),
            encoding="utf-8",
        )
    quoted = ", ".join('["' + mod + '"]=true' for mod in sorted(enabled))
    (dest / "ci_profile.lua").write_text("return {" + quoted + "}\n", encoding="utf-8")
    # Manifest of literal declarations from the three active recipe modules.
    # Factorio then verifies each declaration actually reached data.raw.
    def names(kind, relative_files):
        pattern = re.compile(r'type\s*=\s*"' + kind + r'"\s*,\s*name\s*=\s*"([^"]+)"')
        found = set()
        for relative in relative_files:
            content = (dest / relative).read_text(encoding="utf-8")
            content = "\n".join(line.split("--", 1)[0] for line in content.splitlines())
            found.update(pattern.findall(content))
        return found
    declared_recipes = names("recipe", [
        "prototypes/recipe/ammo.lua",
        "prototypes/recipe/recipe.lua",
        "prototypes/recipe/vehicles.lua",
    ])
    declared_technologies = names("technology", [
        "prototypes/technology/technology.lua",
    ])
    declared_ammo = names("ammo", ["prototypes/item/ammo.lua"])
    def lua_set(entries):
        return "{" + ",".join("[" + json.dumps(v) + "]=true"
                              for v in sorted(entries)) + "}"
    (dest / "ci_manifest.lua").write_text(
        "return {recipes=" + lua_set(declared_recipes) +
        ", technologies=" + lua_set(declared_technologies) +
        ", ammo=" + lua_set(declared_ammo) + "}\n",
        encoding="utf-8",
    )
    print("[TANKS-CI] MANIFEST %d recipes, %d technologies, %d ammo prototypes" %
          (len(declared_recipes), len(declared_technologies), len(declared_ammo)))
    with (dest / "control.lua").open("a", encoding="utf-8") as handle:
        handle.write('\nrequire("ci_runtime_harness")\n')
    (args.output / "mod-list.json").write_text(
        json.dumps({"mods": [
            {"name": mod, "enabled": mod in enabled}
            for mod in sorted(available | set(bob_versions) | {"tanks_for_bob_fork"})
        ]}, indent=2) + "\n", encoding="utf-8"
    )
    details = {
        "source": str(source.relative_to(ROOT)),
        "version": info["version"],
        "engine": args.engine,
        "factorio_version_in_staged_info": info["factorio_version"],
        "profile": args.profile,
        "enabled_official_mods": sorted(enabled),
        "disabled_official_mods": sorted(available - enabled),
        "probe_only": is_21,
        "has_extra_mods": bool(bob_versions),
        "enabled_bob_modules": sorted(bob_versions.items()),
        "profile_is_single_combined_environment": True
    }
    (args.output / "ci-profile.json").write_text(
        json.dumps(details, indent=2) + "\n", encoding="utf-8"
    )
    print("[TANKS-CI] STAGED", json.dumps(details, sort_keys=True))

if __name__ == "__main__":
    main()
