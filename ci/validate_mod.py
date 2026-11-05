#!/usr/bin/env python3
"""Audit the latest checked-in Tanks for Bob package."""
import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PREFIX = "tanks_for_bob_fork_"
REQUIRE = re.compile(r"""\brequire\s*(?:\(\s*['"]([^'"]+)['"]\s*\)|['"]([^'"]+)['"])""")
ASSET = re.compile(r"""__tanks_for_bob_fork__/([^"'\s]+)""")
RECIPE = re.compile(r"""\btype\s*=\s*['"]recipe['"]\s*,\s*name\s*=\s*['"]([^'"]+)['"]""")
OPTIONAL = {"prototypes.compatibility.space-age"}

def select_mod():
    found = []
    for folder in ROOT.glob(PREFIX + "*"):
        suffix = folder.name[len(PREFIX):]
        if folder.is_dir() and re.fullmatch(r"\d+(?:\.\d+)+", suffix):
            found.append((tuple(map(int, suffix.split("."))), folder))
    if not found:
        raise ValueError("No versioned Tanks for Bob package")
    _, folder = max(found)
    info = json.loads((folder / "info.json").read_text(encoding="utf-8"))
    if info.get("name") != "tanks_for_bob_fork":
        raise ValueError("Unexpected mod name")
    if folder.name != PREFIX + info.get("version", ""):
        raise ValueError("Package directory and info.json version disagree")
    if info.get("factorio_version") != "2.0":
        raise ValueError("Workflow requires Factorio 2.0 mod API")
    required = []
    for declaration in info.get("dependencies", []):
        declaration = declaration.strip()
        if not declaration or declaration[0] in "?!~":
            continue
        name = re.split(r"\s*[<>=]", declaration, maxsplit=1)[0].strip()
        if name not in {"base", "core"}:
            required.append(name)
    if required:
        raise ValueError("Non-vanilla required dependencies: " + ", ".join(required))
    return folder, info

def audit(folder, info):
    errors, warnings, recipe_names = [], [], []
    sources = sorted(folder.rglob("*.lua"))
    for source in sources:
        relative = source.relative_to(folder).as_posix()
        for number, raw in enumerate(source.read_text(encoding="utf-8-sig").splitlines(), 1):
            line = raw.split("--", 1)[0]
            for hit in REQUIRE.finditer(line):
                module = hit.group(1) or hit.group(2)
                if module.startswith(("prototypes.", "scripts.")):
                    target = folder / (module.replace(".", "/") + ".lua")
                    if not target.is_file():
                        message = f"{relative}:{number}: missing Lua require {module}"
                        (warnings if module in OPTIONAL else errors).append(message)
            for hit in ASSET.finditer(line):
                asset = hit.group(1).rstrip(")}],")
                if not (folder / asset).is_file():
                    errors.append(f"{relative}:{number}: missing local asset {asset}")
            recipe_names.extend(RECIPE.findall(line))
    duplicates = {n: c for n, c in Counter(recipe_names).items() if c > 1}
    if duplicates:
        warnings.append(f"Repeated literal recipe declarations: {duplicates}")
    return dict(package=folder.name, version=info["version"],
                lua_files=len(sources), literal_recipes=len(recipe_names),
                errors=errors, warnings=warnings)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--select-only", action="store_true")
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    try:
        folder, info = select_mod()
        if args.select_only:
            print(folder.relative_to(ROOT))
            return 0
        result = audit(folder, info)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print("TANKS-CI SETUP ERROR:", exc, file=sys.stderr)
        return 2
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"TANKS-CI STATIC {result['package']}: {result['lua_files']} Lua files, "
          f"{result['literal_recipes']} literal recipes, "
          f"{len(result['errors'])} errors, {len(result['warnings'])} warnings")
    for issue in result["errors"][:60]:
        print("ERROR", issue)
    for issue in result["warnings"][:20]:
        print("WARNING", issue)
    if len(result["errors"]) > 60:
        print("Full error list is preserved in the audit artifact")
    return 1 if result["errors"] else 0

if __name__ == "__main__":
    sys.exit(main())
