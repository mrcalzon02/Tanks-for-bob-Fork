#!/usr/bin/env python3
"""One Factorio 2.1 headless compatibility profile and static audit.

Tests the latest declared 2.1 source with Base + Elevated Rails + Quality +
Recycler + Space Age in a single GitHub Actions job, without retargeting it.
"""
from __future__ import annotations
import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROFILES = (("2.1.24", "space-age-full"),)
DATA_MARKERS = (
    "[TANKS-CI] DATA_PASS",
    "[TANKS-CI] SOURCE_REGISTRY_PASS",
    "[TANKS-CI] SUPPLY_GRAPH_PASS",
    "[TANKS-CI] WEAPON_AUDIT_PASS",
    "[TANKS-CI] AMMO_REGISTRY_PASS",
    "[TANKS-CI] HANDHELD_UNLOCK_PASS",
    "[TANKS-CI] WEAPON_PROGRESSION_PASS",
    "[TANKS-CI] RECIPE_MACHINE_PASS",
)
RUNTIME_MARKERS = (
    "[TANKS-CI] RUNTIME_PASS",
    "[TANKS-CI] DAMAGE_RESPONSE_PASS",
    "[TANKS-CI] AMMO_INVENTORY_CHECKED",
)

def run_command(args: list[str], logfile: Path, timeout: int = 420) -> tuple[bool, str]:
    logfile.parent.mkdir(parents=True, exist_ok=True)
    with logfile.open("w", encoding="utf-8") as output:
        try:
            result = subprocess.run(
                args, cwd=ROOT, stdout=output, stderr=subprocess.STDOUT,
                timeout=timeout, check=False
            )
            if result.returncode:
                return False, f"command exited {result.returncode}: {args[0]}"
        except subprocess.TimeoutExpired:
            return False, f"command timed out after {timeout}s: {args[0]}"
        except OSError as err:
            return False, f"command could not start: {err}"
    return True, "ok"

def check_markers(logfile: Path, markers: tuple[str, ...]) -> tuple[bool, str]:
    content = logfile.read_text(encoding="utf-8", errors="replace")
    absent = [marker for marker in markers if marker not in content]
    if absent:
        return False, "missing required engine evidence: " + ", ".join(absent)
    return True, "verified"

def tail(logfile: Path, max_lines: int = 18) -> str:
    if not logfile.is_file():
        return "(log absent)"
    return "\n".join(logfile.read_text(encoding="utf-8", errors="replace").splitlines()[-max_lines:])

def preserve_progression_evidence(source: Path, destination: Path) -> None:
    # The native fixture also creates disposable mod copies and saves. Keep
    # its reports and logs in the consolidated artifact, not those work files.
    files = [source / "receipt.json", source / "engine-version.txt"]
    files.extend(source.glob("*/*.log"))
    files.extend(source.glob("*/runtime/script-output/progression-runtime/*.json"))
    for file in files:
        if file.is_file():
            target = destination / file.relative_to(source)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(file.read_bytes())

def run_profile(engine: str, profile: str, binary: Path, work: Path, output: Path,
                baseline_package: Path | None = None) -> dict:
    name = f"{engine}-{profile}"
    artifacts = output / "profiles" / name
    artifacts.mkdir(parents=True, exist_ok=True)
    mod_folder = work / name / "mods"
    save = work / name / "world.zip"
    settings = work / name / "server-settings.json"
    progression_work = work / name / "progression-runtime"
    progression_command = [
        sys.executable, str(ROOT / "ci/progression_runtime_runner.py"),
        "--binary", str(binary), "--profile", "space-age",
        "--output", str(progression_work),
    ]
    if baseline_package:
        progression_command.extend(["--legacy-package", str(baseline_package)])
    progression_marker = "TANKS-CI PROGRESSION_RUNTIME_PASS fresh=yes migration=" + (
        "yes" if baseline_package else "not-requested")
    save.parent.mkdir(parents=True, exist_ok=True)
    settings.write_text(json.dumps({
        "name": "Tanks for Bob Official Mod Compatibility CI",
        "description": "Local CI multiplayer server smoke",
        "max_players": 1,
        "visibility": {"public": False, "lan": False},
        "require_user_verification": False,
        "auto_pause": False,
        "autosave_interval": 10,
        "autosave_slots": 2,
    }, indent=2) + "\n", encoding="utf-8")
    stages = [
        ("engine-version", [str(binary), "--version"], 30, ("Version: " + engine + " (",)),
        ("stage", [
            sys.executable, str(ROOT / "ci/stage_profile.py"),
            "--engine", engine, "--profile", profile, "--output", str(mod_folder)
        ], 90, ()),
        ("create", [
            str(binary), "--mod-directory", str(mod_folder),
            "--create", str(save), "--map-gen-seed", "907260"
        ], 360, DATA_MARKERS),
        ("benchmark", [
            str(binary), "--mod-directory", str(mod_folder),
            "--benchmark", str(save), "--benchmark-ticks", "1200"
        ], 360, RUNTIME_MARKERS),
        ("progression-runtime", progression_command,
         660 if baseline_package else 240, (progression_marker,)),
        ("server", [
            sys.executable, str(ROOT / "ci/server_smoke.py"),
            "--binary", str(binary), "--mods", str(mod_folder),
            "--save", str(save), "--settings", str(settings),
            "--log", str(artifacts / "factorio-dedicated-server.log"),
            "--timeout", "120"
        ], 145, ("TANKS-CI SERVER_PASS",)),
    ]
    result = {"engine": engine, "profile": profile, "name": name,
              "result": "passed", "failure": None, "stages": {}}
    for stage, command, timeout, markers in stages:
        if stage == "progression-runtime":
            # Use the same selected source recorded by staging. The native
            # player fixture loads it with its own addon, without replacing
            # production event handlers with the general smoke harness.
            staged = json.loads((mod_folder / "ci-profile.json").read_text(encoding="utf-8"))
            command.extend(["--source", str(ROOT / staged["source"])])
        logfile = artifacts / f"{stage}.log"
        ok, message = run_command(command, logfile, timeout)
        if ok and markers:
            ok, message = check_markers(logfile, markers)
        result["stages"][stage] = {"passed": ok, "detail": message}
        if stage == "stage" and ok:
            for filename in ("ci-profile.json", "mod-list.json"):
                (artifacts / filename).write_bytes((mod_folder / filename).read_bytes())
            staged = json.loads((mod_folder / "ci-profile.json").read_text(encoding="utf-8"))
            result["source"] = staged["source"]
            result["source_version"] = staged["version"]
            result["metadata_modified"] = staged["metadata_modified"]
        if stage == "progression-runtime":
            preserve_progression_evidence(progression_work, artifacts / "progression-runtime")
        if not ok:
            result["result"] = "failed"
            result["failure"] = stage + ": " + message
            print(f"::error title={name}::{result['failure']}", flush=True)
            print(tail(logfile), flush=True)
            break
    if result["result"] == "passed":
        create_log = (artifacts / "create.log").read_text(encoding="utf-8", errors="replace")
        bench_log = (artifacts / "benchmark.log").read_text(encoding="utf-8", errors="replace")
        progression_log = (artifacts / "progression-runtime.log").read_text(encoding="utf-8", errors="replace")
        interesting = ("SOURCE_REGISTRY_PASS", "SUPPLY_GRAPH rounds", "WEAPON_AUDIT vehicles",
                       "AMMO_REGISTRY_PASS", "HANDHELD_UNLOCK_PASS", "WEAPON_PROGRESSION_PASS", "RECIPE_MACHINE_PASS",
                       "RUNTIME_PASS tick", "DAMAGE_RESPONSE_PASS tick", "AMMO_INVENTORY_CHECKED tick")
        evidence = []
        for line in (create_log + "\n" + bench_log).splitlines():
            if "[TANKS-CI]" in line and any(key in line for key in interesting):
                msg = line.split("[TANKS-CI]", 1)[1].strip()
                if msg not in evidence:
                    evidence.append(msg)
        result["evidence"] = evidence
        for line in progression_log.splitlines():
            if line.startswith("TANKS-CI PROGRESSION_RUNTIME_PASS"):
                evidence.append(line)
        print(f"[TANKS-CI] PROFILE_PASS {name}", flush=True)
    return result

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--binary-21", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--work", type=Path, required=True)
    parser.add_argument("--baseline-package", type=Path,
                        help="Optional exact previous 2.1 ZIP for the native saved-game migration check")
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    args.work.mkdir(parents=True, exist_ok=True)
    print("[TANKS-CI] ONE_JOB_BEGIN: 1 job, 1 Factorio 2.1 profile", flush=True)
    static_log = args.output / "static-audit.log"
    static_ok, static_detail = run_command([
        sys.executable, str(ROOT / "ci/validate_mod.py"),
        "--report", str(args.output / "current-source-audit.json")
    ], static_log, 90)
    if not static_ok:
        print("::error title=Source audit::" + static_detail, flush=True)
        print(tail(static_log), flush=True)
    else:
        print("[TANKS-CI] STATIC_PASS", flush=True)
    tests = []
    binaries = {"2.1.24": args.binary_21}
    for index, (engine, profile) in enumerate(PROFILES, start=1):
        print(f"[TANKS-CI] CHECK {index}/1 {engine} {profile}", flush=True)
        try:
            tests.append(run_profile(engine, profile, binaries[engine], args.work, args.output,
                                     args.baseline_package))
        except Exception as exc:
            tests.append({
                "engine": engine, "profile": profile, "name": f"{engine}-{profile}",
                "result": "failed", "failure": f"unhandled harness error: {exc}",
                "stages": {},
            })
            print(f"::error title=Harness {engine}-{profile}::{exc}", flush=True)
    passed = sum(p["result"] == "passed" for p in tests)
    completed = len(tests)
    verified = static_ok and passed == 1 and completed == 1
    report = {
        "test_system": "one-job official Factorio compatibility and auditing suite",
        "engine_versions": sorted(binaries),
        "total_jobs": 1,
        "static_audit": "passed" if static_ok else "failed",
        "static_detail": static_detail,
        "expected_profiles": 1,
        "completed_profiles": completed,
        "passed_profiles": passed,
        "failed_profiles": [p["name"] for p in tests if p["result"] != "passed"],
        "result": "passed" if verified else "failed",
        "profiles": tests,
        "two_one_is_metadata_probe_only": False,
    }
    (args.output / "suite-results.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    summary = [
        "# Tanks for Bob — one-job compatibility audit",
        "",
        f"**Overall:** {'PASS' if verified else 'FAIL'}",
        f"**Single Actions job:** one, with {passed}/1 runtime profile passing",
        f"**Static audit:** {'PASS' if static_ok else 'FAIL'}",
        "",
        "| Engine | Profile | Result |",
        "| --- | --- | --- |",
    ]
    for test in tests:
        summary.append(
            f"| {test['engine']} | {test['profile']} | {test['result'].upper()} |"
        )
    summary += [
        "",
        "Only Factorio 2.1.24 Base + Elevated Rails + Quality + Recycler + Space Age is checked in this run.",
        "The latest declared 2.1 source is staged with its release metadata unchanged.",
        "Native player wood acquisition and seeded kiln production are checked in the same official-mod profile.",
        ("Legacy-save migration is checked against the explicitly supplied baseline package."
         if args.baseline_package else
         "Legacy-save migration was not requested; this CI run checks the fresh-start path."),
        "Ingredient supply is optimistic; ammo checks are inventory/registry checks, not actual firing.",
    ]
    (args.output / "suite-summary.md").write_text("\n".join(summary) + "\n", encoding="utf-8")
    print(f"[TANKS-CI] ONE_JOB_RESULT static={'PASS' if static_ok else 'FAIL'} "
          f"profiles={passed}/1 result={'PASS' if verified else 'FAIL'}", flush=True)
    return 0 if verified else 1

if __name__ == "__main__":
    raise SystemExit(main())
