#!/usr/bin/env python3
"""Offline contract tests for the single-job Bob's Mods integration lane.

No Factorio credentials, archive downloads, or extra CI jobs are required.
These tests do NOT claim to replace the actual combined game runtime test.
"""
import contextlib
import hashlib
import io
import json
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest import mock

from ci import fetch_bobs_mods
from ci import stage_profile

REPO = Path(__file__).resolve().parents[1]


def fake_zip(name="bobassembly", version="2.1.0", major="2.0"):
    data = io.BytesIO()
    with zipfile.ZipFile(data, "w") as z:
        z.writestr(f"{name}_{version}/info.json", json.dumps({
            "name": name, "version": version, "factorio_version": major,
            "dependencies": ["base >= 2.0"]
        }))
    return data.getvalue()


class PinTests(unittest.TestCase):
    def test_all_modules_are_pinned(self):
        pins = fetch_bobs_mods.load_pins(REPO / "ci" / "bobs_versions.json")
        self.assertEqual(19, len(pins))
        self.assertEqual("2.0.1", pins["boblocale"])
        self.assertEqual("2.1.2", pins["bobores"])

    def test_wrong_major_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "bad.json"
            path.write_text(json.dumps({
                "engine": "2.1.23", "factorio_major": "2.1",
                "mods": {"bobassembly": "3.0.0"}
            }))
            with self.assertRaises(ValueError):
                fetch_bobs_mods.load_pins(path)

    def test_exact_portal_release_selection(self):
        releases = {
            "name": "bobassembly",
            "releases": [
                {"version": "3.0.0", "file_name": "bobassembly_3.0.0.zip",
                 "info_json": {"factorio_version": "2.1"}},
                {"version": "2.1.0", "file_name": "bobassembly_2.1.0.zip",
                 "info_json": {"factorio_version": "2.0"},
                 "download_url": "/download/bobassembly/abcd1234",
                 "sha1": "f" * 40},
            ],
        }
        with mock.patch.object(fetch_bobs_mods, "get_bytes",
                               return_value=json.dumps(releases).encode()):
            chosen = fetch_bobs_mods.select_release("bobassembly", "2.1.0")
        self.assertEqual("2.1.0", chosen["version"])
        with mock.patch.object(fetch_bobs_mods, "get_bytes",
                               return_value=json.dumps(releases).encode()):
            with self.assertRaises(ValueError):
                fetch_bobs_mods.select_release("bobassembly", "3.0.0")

    def test_zip_identity_rejected(self):
        with self.assertRaises(ValueError):
            fetch_bobs_mods.validate_archive(
                fake_zip(major="2.1"), name="bobassembly", version="2.1.0"
            )

    def test_optional_dependency_not_promoted_to_required(self):
        self.assertEqual(
            {"boblibrary", "base"},
            fetch_bobs_mods.required_dependencies({
                "dependencies": ["base >= 2.0", "boblibrary >= 2.1.0",
                                 "? bobplates >= 2.1.0", "(?) other",
                                 "! incompatible-mod"]
            }),
        )

    def test_valid_mocked_download_and_checksum_mismatch(self):
        payload = fake_zip()
        sha1 = hashlib.sha1(payload).hexdigest()
        portal = {
            "name": "bobassembly", "releases": [{
                "version": "2.1.0", "file_name": "bobassembly_2.1.0.zip",
                "info_json": {"factorio_version": "2.0",
                              "dependencies": ["base >= 2.0"]},
                "download_url": "/download/bobassembly/test",
                "sha1": sha1,
            }]
        }
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            def mocked_fetch(url, *, max_bytes):
                if "/api/mods/" in url:
                    return json.dumps(portal).encode()
                self.assertIn("/download/bobassembly/test?", url)
                return payload
            argv = ["fetch_bobs_mods.py", "--lock", "mock",
                    "--output", str(base / "mods"), "--report", str(base / "report.json")]
            with mock.patch.object(fetch_bobs_mods, "load_pins",
                                   return_value={"bobassembly": "2.1.0"}), \
                 mock.patch.object(fetch_bobs_mods, "get_bytes",
                                   side_effect=mocked_fetch), \
                 mock.patch.object(fetch_bobs_mods.sys, "argv", argv), \
                 mock.patch.dict(fetch_bobs_mods.os.environ, {
                     "FACTORIO_USERNAME": "test-user",
                     "FACTORIO_TOKEN": "unit-test-token"
                 }):
                self.assertEqual(0, fetch_bobs_mods.main())
            self.assertEqual(payload, (base / "mods" / "bobassembly_2.1.0.zip").read_bytes())
            report = json.loads((base / "report.json").read_text())
            self.assertEqual(hashlib.sha256(payload).hexdigest(),
                             report["modules"][0]["downloaded_sha256"])

            portal["releases"][0]["sha1"] = "0" * 40
            with mock.patch.object(fetch_bobs_mods, "load_pins",
                                   return_value={"bobassembly": "2.1.0"}), \
                 mock.patch.object(fetch_bobs_mods, "get_bytes",
                                   side_effect=mocked_fetch), \
                 mock.patch.object(fetch_bobs_mods.sys, "argv", argv), \
                 mock.patch.dict(fetch_bobs_mods.os.environ, {
                     "FACTORIO_USERNAME": "test-user",
                     "FACTORIO_TOKEN": "unit-test-token"
                 }):
                with contextlib.redirect_stderr(io.StringIO()):
                    self.assertEqual(1, fetch_bobs_mods.main())


class StageTests(unittest.TestCase):
    def test_stage_includes_all_bob_mods_without_overwriting_final_fixes(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "tanks_for_bob_fork_1.8.95"
            source.mkdir()
            (source / "info.json").write_text(json.dumps({
                "name": "tanks_for_bob_fork", "version": "1.8.95",
                "factorio_version": "2.0",
                "dependencies": ["base >= 2.0"]
            }))
            (source / "data-final-fixes.lua").write_text(
                'require("prototypes.Compatibility.bobs")\n'
            )
            (source / "control.lua").write_text("-- fixture control\n")
            for kind, path in (
                ("recipe", "prototypes/recipe/ammo.lua"),
                ("recipe", "prototypes/recipe/recipe.lua"),
                ("recipe", "prototypes/recipe/vehicles.lua"),
                ("technology", "prototypes/technology/technology.lua"),
                ("ammo", "prototypes/item/ammo.lua")
            ):
                target = source / path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text('data:extend({{type="%s",name="test-fixture"}})\n' % kind)
            ci = root / "ci"
            ci.mkdir()
            for name in ("data_audit.lua", "runtime_harness.lua",
                         "progression_audit.lua", "weapon_audit.lua",
                         "recipe_machine_audit.lua", "bobs_audit.lua"):
                (ci / name).write_text("-- test fixture\n")
            pins = fetch_bobs_mods.load_pins(REPO / "ci" / "bobs_versions.json")
            (ci / "bobs_versions.json").write_text(json.dumps({
                "factorio_major": "2.0", "engine": "2.0.77", "mods": pins
            }))
            archives = root / "bob-zips"
            archives.mkdir()
            for name, version in pins.items():
                (archives / f"{name}_{version}.zip").write_bytes(b"preverified-mock-zip")
            output = root / "test" / "mods"
            argv = ["stage_profile.py", "--engine", "2.0.77",
                    "--profile", "space-age", "--output", str(output),
                    "--bobs-mods-dir", str(archives)]
            with mock.patch.object(stage_profile, "ROOT", root), \
                 mock.patch.object(stage_profile.sys, "argv", argv):
                stage_profile.main()
            final = (output / "tanks_for_bob_fork" / "data-final-fixes.lua").read_text()
            self.assertIn('require("prototypes.Compatibility.bobs")', final)
            self.assertIn('require("ci_data_audit")', final)
            mods = json.loads((output / "mod-list.json").read_text())
            enabled = {m["name"] for m in mods["mods"] if m["enabled"]}
            self.assertTrue(set(pins).issubset(enabled))
            self.assertIn("tanks_for_bob_fork", enabled)
            self.assertIn("space-age", enabled)
            self.assertEqual(19, len(list(output.glob("bob*.zip"))))


if __name__ == "__main__":
    unittest.main()
