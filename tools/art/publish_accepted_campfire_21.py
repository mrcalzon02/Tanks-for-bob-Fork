#!/usr/bin/env python3
"""Publish only the user-accepted, engine-tested Tanks for Bob 1.8.96 / Factorio 2.1 release.

Reuses the existing Mod Portal API uploader, without widening the legacy 2.0
uploader's package guard. Never uploads an unvalidated or differently named ZIP.
"""
import hashlib
import json
import os
from pathlib import Path
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "ci"))
import publish_mod_portal as portal
from build_accepted_campfire_21 import ACCEPTED, TARGET_NAME, TARGET_VERSION


def sha256(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python3 tools/art/publish_accepted_campfire_21.py PATH_TO_VERIFIED_OUTPUT_DIR")
    folder = Path(sys.argv[1]).resolve()
    archive = folder / (TARGET_NAME + ".zip")
    receipt_path = folder / "campfire-21-promotion-receipt.json"
    checksum = folder / (archive.name + ".sha256")
    engine_version = folder / "engine-version.txt"
    engine_create = folder / "engine-create.log"
    engine_benchmark = folder / "engine-benchmark.log"
    for path in (archive, receipt_path, checksum, engine_version, engine_create, engine_benchmark):
        if not path.is_file():
            raise RuntimeError(f"Missing release or engine-validation evidence: {path.name}")
    if "2.1.23" not in engine_version.read_text(errors="replace"):
        raise RuntimeError("Official Factorio 2.1.23 engine evidence missing")
    create_log = engine_create.read_text(errors="replace")
    bench_log = engine_benchmark.read_text(errors="replace")
    if "Loading mod tanks_for_bob_fork" not in create_log:
        raise RuntimeError("Actual full-mod engine load evidence missing")
    if not bench_log.strip() or "Performed " not in bench_log and "ticks" not in bench_log:
        raise RuntimeError("Engine benchmark evidence missing")
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    actual_hash = sha256(archive.read_bytes())
    if (receipt.get("sha256") != actual_hash or
            checksum.read_text(encoding="utf-8").split()[0] != actual_hash):
        raise RuntimeError("Release checksum verification failed")
    if receipt.get("mod_version") != TARGET_VERSION or receipt.get("factorio_version") != "2.1":
        raise RuntimeError("This is not the approved Factorio 2.1 release")
    if receipt.get("accepted_art_hashes") != ACCEPTED:
        raise RuntimeError("Accepted-art manifest differs from approved source")
    with zipfile.ZipFile(archive) as z:
        if z.testzip() is not None:
            raise RuntimeError("Corrupt ZIP")
        root = TARGET_NAME + "/"
        meta = json.loads(z.read(root+"info.json"))
        if (meta.get("name") != portal.MOD or meta.get("version") != TARGET_VERSION or
                meta.get("factorio_version") != "2.1" or
                "base >= 2.1" not in meta.get("dependencies", [])):
            raise RuntimeError("Unexpected release identity, version, or Factorio requirement")
        for path,digest in ACCEPTED.items():
            if sha256(z.read(root+path)) != digest:
                raise RuntimeError("Approved sprite byte mismatch: " + path)
    secret = os.environ.get("FACTORIO_MOD_UPLOAD_KEY", "").strip()
    if not secret:
        raise RuntimeError("FACTORIO_MOD_UPLOAD_KEY secret is unavailable; cannot publish")
    print("[TANKS-PUBLISH-21] ENGINE_AND_ACCEPTED_ART_VERIFIED " + actual_hash, flush=True)
    portal.upload(archive, TARGET_VERSION, secret)
    public = TARGET_VERSION in portal.portal_versions()
    status = "publicly_indexed" if public else "accepted_index_pending"
    (folder / "mod-portal-publication.json").write_text(json.dumps({
        "mod_name": portal.MOD,
        "version": TARGET_VERSION,
        "factorio_version": "2.1",
        "sha256": actual_hash,
        "status": status,
        "portal_url": "https://mods.factorio.com/mod/" + portal.MOD
    }, indent=2) + "\n", encoding="utf-8")
    print("[TANKS-PUBLISH-21] " + status.upper(), flush=True)
    if not public:
        print("::warning title=Mod Portal publication::Upload may be accepted but public indexing is not yet confirmed.",flush=True)


if __name__ == "__main__":
    main()
