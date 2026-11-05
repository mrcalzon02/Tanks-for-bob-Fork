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
    (dest / "data-final-fixes.lua").write_text(
        (ROOT / "ci" / "data_audit.lua").read_text(encoding="utf-8"),
        encoding="utf-8"
    )
    (dest / "ci_runtime_harness.lua").write_text(
        (ROOT / "ci" / "runtime_harness.lua").read_text(encoding="utf-8"),
        encoding="utf-8"
    )
    quoted = ", ".join('["' + mod + '"]=true' for mod in sorted(enabled))
    (dest / "ci_profile.lua").write_text("return {" + quoted + "}\n", encoding="utf-8")
    with (dest / "control.lua").open("a", encoding="utf-8") as handle:
        handle.write('\nrequire("ci_runtime_harness")\n')
    (args.output / "mod-list.json").write_text(
        json.dumps({"mods": [
            {"name": mod, "enabled": mod in enabled} for mod in sorted(available)
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
        "has_extra_mods": False
    }
    (args.output / "ci-profile.json").write_text(
        json.dumps(details, indent=2) + "\n", encoding="utf-8"
    )
    print("[TANKS-CI] STAGED", json.dumps(details, sort_keys=True))

if __name__ == "__main__":
    main()
