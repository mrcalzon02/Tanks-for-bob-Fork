#!/usr/bin/env python3
"""Offline contact-sheet regression; synthetic inputs are NOT game evidence."""
from __future__ import annotations
import importlib.util
from pathlib import Path
import tempfile
import unittest
from PIL import Image

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("solar_v8_visual_capture", HERE / "visual_capture.py")
assert spec and spec.loader
capture = importlib.util.module_from_spec(spec)
spec.loader.exec_module(capture)

class SolarV8ContactSheetTests(unittest.TestCase):
    def test_all_sixteen_cases_represented_in_contact_sheet(self):
        self.assertEqual(capture.DIRECTIONS, ("north", "east", "south", "west"))
        self.assertEqual(capture.GROUNDS, ("natural", "concrete"))
        self.assertEqual(capture.ZOOMS, ("normal", "close"))
        rows = [(g,z) for g in capture.GROUNDS for z in capture.ZOOMS]
        self.assertEqual(len(rows) * len(capture.DIRECTIONS), 16)
        with tempfile.TemporaryDirectory(prefix="solar-v8-contact-test-") as folder:
            root = Path(folder)
            colors = {}
            for i, d in enumerate(capture.DIRECTIONS):
                for j, (ground, zoom) in enumerate(rows):
                    # Test colors are synthetic QA markers, never engine proof.
                    color = (25 + 35*i, 30 + 45*j, 45 + 19*i + 13*j)
                    colors[d,ground,zoom] = color
                    Image.new("RGB", (1152,864), color).save(
                        root / capture.shot_name(d,ground,zoom))
            capture.make_contact(root, {})
            with Image.open(root/"factorio-client-pipes-all-four.png") as im:
                self.assertEqual(im.size, (2020,1710))
                for i,d in enumerate(capture.DIRECTIONS):
                    for j,(ground,zoom) in enumerate(rows):
                        with self.subTest(direction=d,ground=ground,zoom=zoom):
                            self.assertEqual(
                                im.getpixel((18+502*i+240,80+402*j+180)),
                                colors[d,ground,zoom])
            self.assertTrue((root/"client-vs-approved-v8.png").is_file())

    def test_native_scenario_uses_actual_100_percent_zoom(self):
        lua = (HERE/"visual_client_control.lua").read_text(encoding="utf-8")
        self.assertIn('local ZOOMS={{"normal",1.0},{"close",2.9}}', lua)
        self.assertIn('game.take_screenshot{', lua)
        self.assertIn('SOLAR_V8_GUI_SCREENSHOT_QUEUE_COMPLETE count=16', lua)

if __name__ == "__main__":
    unittest.main()
