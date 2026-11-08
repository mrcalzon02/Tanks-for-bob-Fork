#!/usr/bin/env python3
"""Stage one Tanks for Bob package with only a chosen set of official Factorio mods.

The staged copy is disposable; the selected 2.1 package metadata is preserved.
"""
import argparse
import json
import re
import shutil
from pathlib import Path
from validate_mod import select_mod

ROOT = Path(__file__).resolve().parents[1]
OFFICIAL_21 = {"base", "elevated-rails", "quality", "recycler", "space-age"}
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

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--engine", choices=["2.1.23", "2.1.24"], required=True)
    p.add_argument("--profile", choices=sorted(PROFILES), required=True)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    enabled = set(PROFILES[args.profile])
    available = OFFICIAL_21
    if not enabled <= available:
        raise SystemExit("Invalid engine/profile pair: " + args.engine + " / " + args.profile)
    if "quality" in enabled:
        enabled.add("recycler")
    if "space-age" in enabled:
        enabled.update(["recycler", "elevated-rails"])
    source, info = select_mod()
    if info["factorio_version"] != ".".join(args.engine.split(".")[:2]):
        raise ValueError("Selected source metadata does not match the requested engine")
    dest = args.output / "tanks_for_bob_fork"
    args.output.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(source, dest)
    if (dest / "info.json").read_bytes() != (source / "info.json").read_bytes():
        raise ValueError("Staging changed the selected package metadata")
    (dest / "ci_data_audit.lua").write_text(
        (ROOT / "ci" / "data_audit.lua").read_text(encoding="utf-8"),
        encoding="utf-8"
    )
    # Preserve any release data-final-fixes logic before adding CI assertions.
    with (dest / "data-final-fixes.lua").open("a", encoding="utf-8") as handle:
        handle.write('\nrequire("ci_data_audit")\n')
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
    # Manifest of literal declarations from the active recipe, technology and
    # ammunition modules. Wooden ammunition lives in item.lua, not ammo.lua.
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
    declared_ammo = names("ammo", [
        "prototypes/item/ammo.lua",
        "prototypes/item/item.lua",
    ])
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
            {"name": mod, "enabled": mod in enabled or mod == "tanks_for_bob_fork"}
            for mod in sorted(available | {"tanks_for_bob_fork"})
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
        "probe_only": False,
        "metadata_modified": False,
        "has_extra_mods": False
    }
    (args.output / "ci-profile.json").write_text(
        json.dumps(details, indent=2) + "\n", encoding="utf-8"
    )
    print("[TANKS-CI] STAGED", json.dumps(details, sort_keys=True))

if __name__ == "__main__":
    main()
