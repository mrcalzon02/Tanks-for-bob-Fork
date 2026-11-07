#!/usr/bin/env python3
"""Package the USER-ACCEPTED four-way campfire into a Factorio 2.1 Tanks for Bob build.

Releases an independent 2.1 package while retaining the 2.0 source untouched.
The seven accepted PNGs must be byte-identical to the successful 0.1.1 test.
No model rerender, no automatic portal publication, and no force-push.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[2]
SOURCE_NAME = "tanks_for_bob_fork_1.8.95"
TARGET_VERSION = "1.8.96"
TARGET_NAME = f"tanks_for_bob_fork_{TARGET_VERSION}"
ACCEPTED_TEST_ZIP_SHA256 = "e909566e2d5da51b64d9f7a1affb683b0a9f5802ad4687791f5bcb4c81d229df"
# Test package factorio_campfire_pipeline_test_0.1.1.zip, visually and in-game accepted.
ACCEPTED = {
    "graphics/entity/campfire-v12-burning.png": "3e8235f2035319a16e0f928d972173565f68f08811bbeb646d9943d1ac3cca0f",
    "graphics/entity/campfire-v12-idle.png": "bfe7d05754a0f7a3918ce40eeb20be42f48da0510091dc88ee2aae3fcb907719",
    "graphics/entity/campfire-v12-burning-64.png": "80ec5f3fff9536bf5207718e776982f517c76d30db8b994055e1847a907b9650",
    "graphics/entity/campfire-v12-idle-64.png": "18a9b444a173fdb39ffa52d22d574b2b77f27f15acef76b6b5002c232341c8eb",
    "graphics/icons/campfire-v12.png": "197f6285c1334ea6225579f3e2e7829136869e0283f56f70fb4ca23cf8b1ac3e",
}
# The approved test's primary 128px atlases and item icon use these exact hashes.
EXPECTED_ORIGINAL = ("graphics/entity/campfire.png", "graphics/entity/campfire-w.png")
COLLISION_OLD = "collision_box = {{-1.2, -1.2}, {1.2, 1.2}}"
COLLISION_NEW = "collision_box = {{-1.2, -1.1}, {1.2, 1.1}}"


def sha256(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def validate_source(source):
    info = json.loads((source / "info.json").read_text(encoding="utf-8"))
    if (info.get("name") != "tanks_for_bob_fork" or info.get("version") != "1.8.95"
            or info.get("factorio_version") != "2.0"):
        raise RuntimeError("Expected source is the preserved 2.0 version 1.8.95")
    for rel, expected in ACCEPTED.items():
        path = source / rel
        if not path.is_file() or sha256(path) != expected:
            raise RuntimeError(f"Approved sprite hash mismatch: {rel}")
    for rel in EXPECTED_ORIGINAL:
        if not (source / rel).is_file():
            raise RuntimeError(f"Missing original rollback graphic: {rel}")
    lua = (source / "prototypes/entity/entities.lua").read_text(encoding="utf-8")
    section = lua.split("    --campfire", 1)
    if len(section) != 2:
        raise RuntimeError("Unique campfire declaration absent")
    section = section[1].split("-- tank-assembly", 1)[0]
    if (section.count('name = "campfire"') != 1 or
            section.count(COLLISION_OLD) != 1 or
            section.count("campfire-v12-burning.png") != 4 or
            section.count("campfire-v12-idle.png") != 4 or
            "always_draw_idle_animation = false" not in section):
        raise RuntimeError("Production campfire graphics or collision layout changed unexpectedly")
    for direction in ("north", "east", "south", "west"):
        if not re.search(r"\b" + direction + r"\s*=\s*\{\s*filename\s*=", section):
            raise RuntimeError(f"Missing {direction} animation")
    return info


def stage(source, dest, metadata):
    shutil.copytree(source, dest)
    info = dict(metadata)
    info["version"] = TARGET_VERSION
    info["factorio_version"] = "2.1"
    info["dependencies"] = [
        dep.replace("base >= 2.0", "base >= 2.1")
        for dep in info.get("dependencies", [])
    ]
    if "base >= 2.1" not in info["dependencies"]:
        raise RuntimeError("2.1 required base dependency missing")
    (dest / "info.json").write_text(json.dumps(info, indent=2) + "\n", encoding="utf-8")
    path = dest / "prototypes/entity/entities.lua"
    lua = path.read_text(encoding="utf-8")
    before, remainder = lua.split("    --campfire", 1)
    campfire, after = remainder.split("-- tank-assembly", 1)
    if campfire.count(COLLISION_OLD) != 1:
        raise RuntimeError("Cannot safely locate exact campfire collision box")
    campfire = campfire.replace(COLLISION_OLD, COLLISION_NEW, 1)
    path.write_text(before + "    --campfire" + campfire + "-- tank-assembly" + after, encoding="utf-8")
    # No rendering changes, no recipe changes, no energy/source changes; we only
    # set the tested rotation condition and 2.1 metadata in the staged release.
    return info


def archive(stage_dir, output):
    target = output / (TARGET_NAME + ".zip")
    if target.exists():
        raise FileExistsError(f"Refusing to overwrite existing release: {target}")
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for f in sorted(stage_dir.rglob("*")):
            if f.is_file():
                z.write(f, f.relative_to(stage_dir.parent).as_posix())
    with zipfile.ZipFile(target) as z:
        if z.testzip() is not None:
            raise RuntimeError("Archive CRC verification failed")
        names = set(z.namelist())
        for path in ("info.json", "data.lua", "prototypes/entity/entities.lua",
                     "graphics/entity/campfire-v12-burning.png",
                     "graphics/entity/campfire-v12-idle.png",
                     "graphics/icons/campfire-v12.png"):
            if TARGET_NAME + "/" + path not in names:
                raise RuntimeError(f"Release ZIP missing {path}")
        for rel, expected in ACCEPTED.items():
            data = z.read(TARGET_NAME + "/" + rel)
            if hashlib.sha256(data).hexdigest() != expected:
                raise RuntimeError("Approved art changed inside ZIP: " + rel)
        packaged = json.loads(z.read(TARGET_NAME + "/info.json"))
        if packaged.get("factorio_version") != "2.1" or packaged.get("version") != TARGET_VERSION:
            raise RuntimeError("Incorrect Factorio 2.1 release metadata")
        c = z.read(TARGET_NAME + "/prototypes/entity/entities.lua").decode("utf-8")
        s = c.split("    --campfire", 1)[1].split("-- tank-assembly", 1)[0]
        if s.count(COLLISION_NEW) != 1 or COLLISION_OLD in s:
            raise RuntimeError("Four-way rotation-enabling collision configuration absent")
        return target, len(names)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    source = ROOT / SOURCE_NAME
    meta = validate_source(source)
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="campfire-approved-21-") as work:
        staged = Path(work) / TARGET_NAME
        info = stage(source, staged, meta)
        release, count = archive(staged, output)
    digest = sha256(release)
    (output / (release.name + ".sha256")).write_text(digest + "  " + release.name + "\n")
    receipt = {
        "package": release.name, "sha256": digest, "bytes": release.stat().st_size,
        "file_count": count, "mod_version": TARGET_VERSION, "factorio_version": "2.1",
        "accepted_test_mod": "factorio_campfire_pipeline_test_0.1.1.zip",
        "accepted_test_sha256": ACCEPTED_TEST_ZIP_SHA256,
        "accepted_art_hashes": ACCEPTED, "rotation": "four-way, 2.4 x 2.2 collision box",
        "source_2_0_intact": True, "runtime_proven": False,
        "notes": "Full mod load on official Factorio 2.1 is a separate CI gate."
    }
    (output / "campfire-21-promotion-receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print("ACCEPTED_CAMPFIRE_21_PACKAGE_CREATED", json.dumps(receipt, sort_keys=True))


if __name__ == "__main__":
    main()
