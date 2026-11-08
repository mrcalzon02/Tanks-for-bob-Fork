"""Cross-repository portability and schema contract smoke checks."""
import json
from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
import export_sprites
import produce_factorio_asset

class PortableContract(unittest.TestCase):
    def test_engine_files_are_vendored(self):
        for name in ("produce_factorio_asset.py","export_sprites.py","render_sprite_frames.py",
                     "verify_sprite_master.py","attach_factorio_prototype.py"):
            self.assertTrue((ROOT/"scripts"/name).exists(),name)
        producer=(ROOT/"scripts/produce_factorio_asset.py").read_text()
        self.assertIn("factorio-output/scripts/export_sprites.py",producer)
        self.assertNotIn("tools/art/export_sprites.py",producer)
        self.assertEqual(produce_factorio_asset.ROOT,ROOT.parent)
    def test_valid_four_way_example(self):
        cfg=json.loads((ROOT/"examples/demo-profile.json").read_text())
        export_sprites.validate_config(cfg)
        self.assertEqual(cfg["directions"],[0,90,180,270])
        self.assertEqual(cfg["camera_override"]["elevation_deg"],45)
        job=json.loads((ROOT/"examples/demo-job.json").read_text())
        self.assertEqual(job["capture_profile"],"factorio-output/examples/demo-profile.json")
        self.assertEqual(job["mod_root"],"factorio-output/examples/demo-mod")
        self.assertEqual(json.loads((ROOT/"examples/demo-mod/info.json").read_text())["name"],job["mod_name"])
    def test_copyable_workflow_matches_installed(self):
        installed=(ROOT.parent/".github/workflows/factorio-output.yml").read_text()
        self.assertEqual((ROOT/"workflow.template.yml").read_text(),installed)
        for part in ("workflow_call:","workflow_dispatch:","actions/upload-artifact@v4",
                     "--deploy","--publish"):
            self.assertIn(part,installed)

if __name__=="__main__":unittest.main()
