#!/usr/bin/env python3
"""Inventory and auditable static diagnostics for Tanks for Bob's 2.1 source.

This checker intentionally distinguishes imported Lua from dormant legacy files.
Runtime game validation is still required to prove actual prototype validity.
"""
import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PREFIX = "tanks_for_bob_fork_"
FACTORIO_VERSION = "2.1"
ENTRY_POINTS = ("settings.lua", "data.lua", "data-updates.lua", "control.lua")
REQUIRE = re.compile(r"""\brequire\s*(?:\(\s*['"]([^'"]+)['"]\s*\)|['"]([^'"]+)['"])""")
ASSET = re.compile(r"""__tanks_for_bob_fork__/([^\n"']+)""")
RECIPE = re.compile(r"""\btype\s*=\s*['"]recipe['"]\s*,\s*name\s*=\s*['"]([^'"]+)['"]""")
TECH = re.compile(r"""\btype\s*=\s*['"]technology['"]\s*,\s*name\s*=\s*['"]([^'"]+)['"]""")
CATEGORY = re.compile(r"""\btype\s*=\s*['"]recipe-category['"]\s*,\s*name\s*=\s*['"]([^'"]+)['"]""")
SUPPORTED_EXT = (".png", ".jpg", ".jpeg", ".webp", ".ogg", ".wav", ".flac")
OFFICIAL = ("elevated-rails", "quality", "recycler", "space-age")


def versioned_sources():
    folders = []
    for path in ROOT.glob(PREFIX + "*"):
        suffix = path.name[len(PREFIX):]
        if path.is_dir() and re.fullmatch(r"\d+(?:\.\d+)+", suffix):
            folders.append((tuple(map(int, suffix.split("."))), path))
    return sorted(folders)


def select_mod():
    found = versioned_sources()
    if not found:
        raise ValueError("Missing versioned tanks_for_bob_fork source directory")
    # Historical 2.0 packages remain in the repository. Select the newest
    # actual 2.1 package; never retarget an old package just for the test.
    for _, folder in reversed(found):
        info = json.loads((folder / "info.json").read_text(encoding="utf-8"))
        if info.get("factorio_version") == FACTORIO_VERSION:
            break
    else:
        raise ValueError("Missing versioned source declared for Factorio " + FACTORIO_VERSION)
    if info.get("name") != "tanks_for_bob_fork":
        raise ValueError("Incorrect mod name")
    if folder.name != PREFIX + info.get("version", ""):
        raise ValueError("Directory and info.json version mismatch")
    required = []
    for dep in info.get("dependencies", []):
        dep = dep.strip()
        if not dep or dep[0] in "?!~+":
            continue
        name = re.split(r"\s*[<>=]", dep, maxsplit=1)[0].strip()
        if name not in {"core", "base"}:
            required.append(name)
    if required:
        raise ValueError("Test cannot isolate non-official required mods: " + repr(required))
    return folder, info


def stripped(text):
    # Fast lexical check, not a substitute for a Lua parser or the game engine.
    return "\n".join(line.split("--", 1)[0] for line in text.splitlines())


def scan(folder, info):
    errors, warnings = [], []
    graph = defaultdict(list)
    visited = set()
    pending = [folder / name for name in ENTRY_POINTS]
    all_lua = set(folder.rglob("*.lua"))
    recipe_counts, tech_counts, category_counts = Counter(), Counter(), Counter()
    asset_uses = defaultdict(list)
    scanned = 0
    while pending:
        source = pending.pop()
        if source in visited:
            continue
        visited.add(source)
        rel = source.relative_to(folder).as_posix()
        if not source.is_file():
            errors.append({"kind": "missing-active-entrypoint", "file": rel})
            continue
        scanned += 1
        raw = source.read_text(encoding="utf-8-sig")
        clean = stripped(raw)
        recipe_counts.update(RECIPE.findall(clean))
        tech_counts.update(TECH.findall(clean))
        category_counts.update(CATEGORY.findall(clean))
        for lineno, line in enumerate(clean.splitlines(), 1):
            for match in REQUIRE.finditer(line):
                module = match.group(1) or match.group(2)
                if not module.startswith(("prototypes.", "scripts.")):
                    continue
                relative_module = module.replace(".", "/") + ".lua"
                target = folder / relative_module
                graph[rel].append(relative_module)
                if target.is_file():
                    pending.append(target)
                else:
                    errors.append({
                        "kind": "missing-active-module",
                        "file": rel, "line": lineno, "require": module,
                        "expected": relative_module,
                    })
            for match in ASSET.finditer(line):
                asset = match.group(1).rstrip(")}],")
                # Directory-based dynamic sprite paths need runtime validation.
                if not asset.lower().endswith(SUPPORTED_EXT):
                    continue
                asset_uses[asset].append(f"{rel}:{lineno}")
    missing_assets = []
    for asset, references in sorted(asset_uses.items()):
        if not (folder / asset).is_file():
            missing_assets.append({
                "path": asset,
                "references": references[:40],
                "occurrences": len(references)
            })
    if missing_assets:
        errors.append({"kind": "missing-local-assets", "unique_files": len(missing_assets),
                       "total_references": sum(a["occurrences"] for a in missing_assets)})
    duplicate = {name: count for name, count in recipe_counts.items() if count > 1}
    if duplicate:
        warnings.append({"kind": "duplicate-literal-recipes",
                         "names": duplicate, "note": "Confirm data:extend call semantics"})
    dup_categories = {name: count for name, count in category_counts.items() if count > 1}
    if dup_categories:
        errors.append({"kind": "duplicate-recipe-categories", "names": dup_categories})
    inactive = sorted(p.relative_to(folder).as_posix() for p in all_lua - visited)
    if "recipe.lua" in inactive:
        warnings.append({
            "kind": "unreferenced-legacy-root-recipe-file",
            "path": "recipe.lua",
            "note": "Not loaded from data.lua; do not count this as a live duplicate"
        })
    deps = info.get("dependencies", [])
    missing_optional = []
    for name in OFFICIAL:
        if not any(re.fullmatch(r"\?\s*" + re.escape(name) + r"(?:\s.*)?", d.strip())
                   for d in deps):
            missing_optional.append(name)
    if missing_optional:
        warnings.append({"kind": "official-optional-dependencies-not-declared",
                         "names": missing_optional})
    files = [p for p in folder.rglob("*") if p.is_file()]
    ext_counts = Counter(p.suffix.lower() or "(none)" for p in files)
    report = {
        "source_package": folder.name,
        "published_factorio_major": info["factorio_version"],
        "package_versions_present": [p.name for _, p in versioned_sources()],
        "file_count": len(files),
        "package_bytes": sum(p.stat().st_size for p in files),
        "files_by_suffix": dict(sorted(ext_counts.items())),
        "loaded_lua_sources_detected": scanned,
        "all_lua_sources": len(all_lua),
        "unreferenced_lua": inactive,
        "require_graph": dict(graph),
        "literal_recipe_count": sum(recipe_counts.values()),
        "unique_literal_recipes": len(recipe_counts),
        "literal_technology_count": sum(tech_counts.values()),
        "unique_literal_technologies": len(tech_counts),
        "unique_literal_recipe_categories": len(category_counts),
        "graphics_asset_paths_seen": len(asset_uses),
        "missing_graphics": missing_assets,
        "errors": errors,
        "warnings": warnings,
        "engine_proof": "not performed by this static script",
    }
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--select-only", action="store_true")
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    try:
        folder, info = select_mod()
        if args.select_only:
            print(folder.relative_to(ROOT).as_posix())
            return 0
        report = scan(folder, info)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print("[TANKS-CI] AUDIT_SETUP_FAILURE " + str(exc), file=sys.stderr)
        return 2
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print("[TANKS-CI] AUDIT source=%s files=%d lua_active=%d/%d recipes=%d techs=%d missing_unique_assets=%d errors=%d warnings=%d" % (
        report["source_package"], report["file_count"],
        report["loaded_lua_sources_detected"], report["all_lua_sources"],
        report["unique_literal_recipes"], report["unique_literal_technologies"],
        len(report["missing_graphics"]), len(report["errors"]), len(report["warnings"])))
    for error in report["errors"][:20]:
        print("[TANKS-CI] STATIC_ERROR " + json.dumps(error, sort_keys=True))
    for asset in report["missing_graphics"][:20]:
        print("[TANKS-CI] MISSING_ASSET " + asset["path"] + " " + repr(asset["references"][:2]))
    for warning in report["warnings"][:10]:
        print("[TANKS-CI] STATIC_WARNING " + json.dumps(warning, sort_keys=True)[:400])
    if len(report["missing_graphics"]) > 20:
        print("[TANKS-CI] More graphics defects in the JSON artifact")
    return 1 if report["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
