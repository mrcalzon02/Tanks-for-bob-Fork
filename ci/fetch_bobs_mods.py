#!/usr/bin/env python3
"""Download exact Factorio 2.0 Bob-family releases for isolated CI integration.

Public Mod Portal metadata provides versions, dependencies and SHA-1 hashes.
The download endpoint requires a licensed Factorio username + login token.
Never print or persist credentials, and never fall back to 'latest'.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path

PORTAL = "https://mods.factorio.com"
USER_AGENT = "TanksForBobFork-Compatibility-CI/1.0 (GitHub Actions)"
MAX_ZIP_BYTES = 200 * 1024 * 1024


def get_bytes(url: str, *, max_bytes: int) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=90) as response:
                value = response.read(max_bytes + 1)
            if len(value) > max_bytes:
                raise ValueError("Download exceeds size limit")
            return value
        except urllib.error.HTTPError as exc:
            if exc.code not in {408, 429, 500, 502, 503, 504} or attempt == 2:
                # Deliberately avoid printing the URL: it may contain a token.
                raise RuntimeError("HTTP " + str(exc.code)) from None
        except (urllib.error.URLError, TimeoutError) as exc:
            if attempt == 2:
                raise RuntimeError("Network request failed: " + type(exc).__name__) from None
        time.sleep(2 ** attempt + 1)
    raise RuntimeError("Request retries exhausted")


def load_pins(path: Path) -> dict[str, str]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if raw.get("factorio_major") != "2.0" or raw.get("engine") != "2.0.77":
        raise ValueError("Pinned manifest does not target our Factorio 2.0.77 engine")
    mods = raw.get("mods")
    if not isinstance(mods, dict) or len(mods) != 19:
        raise ValueError("Expected exactly 19 Bob-family pinned modules")
    for name, version in mods.items():
        if not re.fullmatch(r"bob[a-z]+", name):
            raise ValueError("Invalid Bob mod identifier")
        if not re.fullmatch(r"\d+\.\d+\.\d+", version):
            raise ValueError("Invalid Bob version pin")
    return mods


def select_release(name: str, version: str) -> dict:
    metadata = json.loads(get_bytes(
        PORTAL + "/api/mods/" + urllib.parse.quote(name) + "/full",
        max_bytes=8 * 1024 * 1024,
    ))
    if metadata.get("name") != name:
        raise ValueError("Portal returned the wrong mod ID")
    matches = [entry for entry in metadata.get("releases", [])
               if entry.get("version") == version]
    if len(matches) != 1:
        raise ValueError("Pinned version missing or ambiguous on Mod Portal")
    release = matches[0]
    info = release.get("info_json") or {}
    if info.get("factorio_version") != "2.0":
        raise ValueError("Pinned release does not target Factorio 2.0")
    if info.get("name", name) != name:
        raise ValueError("Release metadata name does not match pin")
    filename = f"{name}_{version}.zip"
    if release.get("file_name") != filename:
        raise ValueError("Unexpected filename for pinned release")
    if not re.fullmatch(r"[0-9a-fA-F]{40}", release.get("sha1", "")):
        raise ValueError("Portal release does not provide a valid SHA-1")
    path = release.get("download_url", "")
    if not re.fullmatch(r"/download/[A-Za-z0-9_./%-]+", path):
        raise ValueError("Unsafe or missing Mod Portal download path")
    return release


def required_dependencies(info: dict) -> set[str]:
    found = set()
    for entry in info.get("dependencies", []):
        line = entry.strip()
        if line.startswith(("?", "!", "~", "(")):
            continue
        match = re.match(r"^([A-Za-z][A-Za-z0-9_-]*)", line)
        if not match:
            raise ValueError("Unrecognized mod dependency declaration")
        found.add(match.group(1))
    return found


def validate_archive(payload: bytes, *, name: str, version: str) -> dict:
    import io
    with zipfile.ZipFile(io.BytesIO(payload)) as archive:
        if archive.testzip() is not None:
            raise ValueError("Downloaded archive has a broken ZIP member")
        # Mod Portal archives can have a source-defined root name rather
        # than exactly <mod>_<version>. Require a *single* root-level or
        # single-folder info.json and validate its actual mod identity.
        paths = archive.namelist()
        candidates = [p for p in paths
                      if p == "info.json"
                      or (p.endswith("/info.json") and p.count("/") == 1)]
        if len(candidates) != 1:
            sample = [p[:90] for p in paths[:6]]
            raise ValueError(
                f"{name}: ZIP has {len(candidates)} top-level info.json candidates; "
                f"first entries={sample}"
            )
        path = candidates[0]
        meta = json.loads(archive.read(path))
        if not isinstance(meta, dict):
            raise ValueError("ZIP info.json must be a JSON object")
        if meta.get("name") != name or meta.get("version") != version:
            raise ValueError("ZIP does not match the pinned mod identity/version")
        if meta.get("factorio_version") != "2.0":
            raise ValueError("ZIP is not compatible with Factorio 2.0")
        return meta


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lock", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    try:
        pins = load_pins(args.lock)
        username = (os.environ.get("FACTORIO_USERNAME")
                    or os.environ.get("FACTORIO_MOD_DOWNLOAD_USERNAME") or "").strip()
        token = (os.environ.get("FACTORIO_TOKEN")
                 or os.environ.get("FACTORIO_MOD_DOWNLOAD_TOKEN") or "").strip()
        if not username or not token:
            raise ValueError(
                "Licensed Factorio mod downloads require repository Actions secrets "
                "FACTORIO_USERNAME and FACTORIO_TOKEN (or MOD_DOWNLOAD aliases). "
                "An upload API key is not a download login token."
            )
        args.output.mkdir(parents=True, exist_ok=True)
        all_ids = set(pins) | {"base", "core", "elevated-rails", "quality", "space-age"}
        report = {"factorio": "2.0.77", "modules": [], "credential_values_logged": False}
        for name, version in sorted(pins.items()):
            release = select_release(name, version)
            release_info = release.get("info_json", {})
            unknown = required_dependencies(release_info) - all_ids
            if unknown:
                raise ValueError(f"{name} has unstaged required modules: {sorted(unknown)}")
            # Portal download URLs are relative and never accepted from other hosts.
            query = urllib.parse.urlencode({"username": username, "token": token})
            data = get_bytes(PORTAL + release["download_url"] + "?" + query,
                             max_bytes=MAX_ZIP_BYTES)
            sha1 = hashlib.sha1(data).hexdigest()
            if sha1.lower() != release["sha1"].lower():
                raise ValueError(f"{name}: downloaded archive SHA-1 does not match portal")
            actual_meta = validate_archive(data, name=name, version=version)
            unknown_zip = required_dependencies(actual_meta) - all_ids
            if unknown_zip:
                raise ValueError(f"{name}: ZIP requires unstaged mods: {sorted(unknown_zip)}")
            destination = args.output / release["file_name"]
            destination.write_bytes(data)
            rec = {
                "name": name, "version": version, "file": destination.name,
                "factorio_version": "2.0",
                "portal_sha1": sha1,
                "downloaded_sha256": hashlib.sha256(data).hexdigest(),
                "required_dependencies": sorted(required_dependencies(actual_meta)),
            }
            report["modules"].append(rec)
            print(f"[TANKS-BOBS] VERIFIED {name} {version} sha1={sha1}", flush=True)
        if len(report["modules"]) != len(pins):
            raise ValueError("Some pinned modules were not downloaded")
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print(f"[TANKS-BOBS] PINNED_DOWNLOAD_PASS modules={len(pins)}", flush=True)
        return 0
    except (ValueError, RuntimeError, OSError, zipfile.BadZipFile,
            json.JSONDecodeError) as exc:
        # Exceptions originate from validation, and never contain credential URLs.
        print("[TANKS-BOBS] PINNED_DOWNLOAD_FAIL " + str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
