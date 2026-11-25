#!/usr/bin/env python3
"""Verify the exact release ZIP in native Factorio before publication."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

from validate_mod import ROOT, select_mod

ENGINE_VERSION = "2.1.24"
OFFICIAL_MODS = ("base", "elevated-rails", "quality", "recycler", "space-age")


def read_request(path: Path) -> tuple[dict, Path, dict]:
    request = json.loads(path.read_text(encoding="utf-8"))
    source, metadata = select_mod()
    if request.get("schema") != "tanks-for-bob.release-request.v1":
        raise ValueError("Unrecognized release request schema")
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,79}", request.get("request_id", "")):
        raise ValueError("Invalid release request identifier")
    if not re.fullmatch(r"\d+\.\d+\.\d+", request.get("version", "")):
        raise ValueError("Invalid release version")
    if not re.fullmatch(r"[0-9a-f]{64}", request.get("expected_sha256", "")):
        raise ValueError("Release request must pin the exact ZIP SHA-256")
    for key in ("version", "factorio_version"):
        if request.get(key) != metadata[key]:
            raise ValueError("Requested " + key + " differs from selected source")
    if request.get("mod") != metadata["name"] or request.get("source") != source.name:
        raise ValueError("Requested mod/source differs from selected source")
    if metadata["factorio_version"] != "2.1":
        raise ValueError("This native release profile requires Factorio 2.1")
    return request, source, metadata


def sha256(path: Path) -> str:
    with path.open("rb") as source:
        return hashlib.file_digest(source, "sha256").hexdigest()


def verify_archive(archive: Path, source: Path, metadata: dict) -> str:
    if archive.name != source.name + ".zip":
        raise ValueError("Archive filename differs from the requested mod/version")
    expected_files = {
        source.name + "/" + path.relative_to(source).as_posix(): path
        for path in source.rglob("*") if path.is_file()
    }
    with zipfile.ZipFile(archive) as package:
        names = package.namelist()
        if len(names) != len(set(names)) or set(names) != set(expected_files):
            raise ValueError("Archive members differ from the selected source")
        if package.testzip() is not None:
            raise ValueError("Corrupt release ZIP")
        if json.loads(package.read(source.name + "/info.json")) != metadata:
            raise ValueError("Packaged metadata differs from selected source")
        for name, original in expected_files.items():
            if package.read(name) != original.read_bytes():
                raise ValueError("Archive differs from source: " + name)
    digest = sha256(archive)
    checksum = archive.with_suffix(archive.suffix + ".sha256")
    if checksum.read_text(encoding="utf-8").strip() != digest + "  " + archive.name:
        raise ValueError("Release checksum does not match the ZIP")
    return digest


def run(command: list[str], log: Path, timeout: int, markers: tuple[str, ...] = ()) -> None:
    with log.open("w", encoding="utf-8") as output:
        result = subprocess.run(command, cwd=ROOT, stdout=output,
                                stderr=subprocess.STDOUT, timeout=timeout, check=False)
    text = log.read_text(encoding="utf-8", errors="replace")
    if result.returncode != 0 or any(marker not in text for marker in markers):
        print("\n".join(text.splitlines()[-60:]), file=sys.stderr)
        raise RuntimeError("Native release check failed: " + log.name)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--binary", type=Path, required=True)
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--request", type=Path, required=True)
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--work", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if not re.fullmatch(r"[0-9a-f]{40}", args.source_commit):
        raise ValueError("Source commit must be a full immutable Git commit SHA")
    request, source, metadata = read_request(args.request)
    archive, binary = args.archive.resolve(), args.binary.resolve()
    digest = verify_archive(archive, source, metadata)
    if digest != request["expected_sha256"]:
        raise ValueError("Release ZIP differs from the requested SHA-256")
    work, output = args.work.resolve(), args.output.resolve()
    work.mkdir(parents=True, exist_ok=False)
    output.mkdir(parents=True, exist_ok=True)
    mods = work / "mods"
    mods.mkdir()
    installed = mods / archive.name
    shutil.copyfile(archive, installed)
    if sha256(installed) != digest:
        raise ValueError("Disposable installed ZIP differs from the release archive")
    enabled = [*OFFICIAL_MODS, metadata["name"]]
    (mods / "mod-list.json").write_text(json.dumps({"mods": [
        {"name": name, "enabled": True} for name in enabled
    ]}, indent=2) + "\n", encoding="utf-8")
    settings = work / "server-settings.json"
    settings.write_text(json.dumps({
        "name": "Tanks for Bob release verification",
        "description": "Private exact-package smoke test",
        "max_players": 1,
        "visibility": {"public": False, "lan": False},
        "require_user_verification": False,
        "auto_pause": False,
        "autosave_interval": 0,
    }, indent=2) + "\n", encoding="utf-8")
    save = work / "release-world.zip"
    run([str(binary), "--version"], output / "engine-version.txt", 30,
        ("Version: " + ENGINE_VERSION + " (",))
    load_marker = "Loading mod tanks_for_bob_fork " + metadata["version"]
    run([str(binary), "--mod-directory", str(mods), "--create", str(save),
         "--map-gen-seed", "20261124"], output / "release-create.log", 360,
        (load_marker,))
    if not save.is_file():
        raise RuntimeError("Native Factorio did not create a save")
    run([str(binary), "--mod-directory", str(mods), "--benchmark", str(save),
         "--benchmark-ticks", "1200"], output / "release-benchmark.log", 360,
        (load_marker, "Performed 1200 updates"))
    run([sys.executable, str(ROOT / "ci/server_smoke.py"), "--binary", str(binary),
         "--mods", str(mods), "--save", str(save), "--settings", str(settings),
         "--log", str(output / "release-dedicated-server.log"), "--timeout", "120"],
        output / "release-server-check.log", 145, ("TANKS-CI SERVER_PASS",))
    if sha256(installed) != digest or sha256(archive) != digest:
        raise ValueError("Release ZIP changed during native verification")
    receipt = {
        "schema": "tanks-for-bob.release-receipt.v1", "result": "passed",
        "request_id": request["request_id"], "mod": metadata["name"],
        "version": metadata["version"], "factorio_version": metadata["factorio_version"],
        "engine_version": ENGINE_VERSION, "source_commit": args.source_commit,
        "source_directory": source.name, "archive": archive.name,
        "archive_bytes": archive.stat().st_size, "sha256": digest,
        "enabled_mods": enabled, "package_modified": False,
        "checks": {"source_archive_equality": "passed", "native_create": "passed",
                   "save_reload_and_1200_updates": "passed", "private_server_startup": "passed"},
        "workflow_run_url": (
            "https://github.com/mrcalzon02/Tanks-for-bob-Fork/actions/runs/" +
            os.environ.get("GITHUB_RUN_ID", "")
        ) if os.environ.get("GITHUB_RUN_ID") else None,
    }
    (output / "release-receipt.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    summary = [
        "# Tanks for Bob " + metadata["version"] + " — exact package verified",
        "", "- Source commit: `" + args.source_commit + "`",
        "- Package: `" + archive.name + "` (" + str(archive.stat().st_size) + " bytes)",
        "- SHA-256: `" + digest + "`",
        "- Native Factorio " + ENGINE_VERSION + ": " + ", ".join(OFFICIAL_MODS) + ".",
        "- Passed: unchanged ZIP load, save creation/reload, 1,200 updates, private server startup.",
        "- This smoke check does not claim two-client multiplayer or a complete playthrough.",
    ]
    (output / "release-summary.md").write_text("\n".join(summary) + "\n", encoding="utf-8")
    print("TANKS-CI RELEASE_PACKAGE_PASS " + metadata["version"] + " " + digest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
