"""Integrity regressions: corruption, clipping, ordering and multi-view static/animation."""
import copy
import json
from pathlib import Path
import tempfile
import unittest

from PIL import Image, ImageDraw

from export_sprites import digest, pack, validate_config


class ExportIntegrity(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.out = Path(self.temp.name)
        self.cfg = {'schema': 1, 'source_size': 32, 'sizes': [16,32], 'samples': 1,
                    'columns': 2, 'fps': 8, 'seed': 1, 'pivot': [0,0,0],
                    'directions': [0,90], 'states': {'idle': [0], 'working': [1,7,13]}}
        (self.out/'master.blend').write_bytes(b'test master hash fixture')
        self.manifest = {'config': self.cfg, 'master_sha256': digest(self.out/'master.blend'), 'frames': []}
        for state, frames in self.cfg['states'].items():
            for direction in range(2):
                for index, frame in enumerate(frames):
                    image = Image.new('RGBA', (32,32))
                    ImageDraw.Draw(image).rectangle((8+index,8,20,20+direction), fill=(90+index*40,80,45,210))
                    path = f'{state}-{direction}-{index}.png'
                    image.save(self.out/path)
                    self.manifest['frames'].append({'state': state, 'direction': direction,
                        'index': index, 'timeline_frame': frame, 'path': path, 'sha256': digest(self.out/path)})
        self.save()

    def save(self):
        (self.out/'capture.json').write_text(json.dumps(self.manifest))

    def test_static_and_animated_multiple_directions_roundtrip(self):
        result = pack(self.out)
        self.assertTrue(result['passed'])
        self.assertEqual(result['capture_count'], 8)
        working = next(s for s in result['sheets'] if s['state']=='working' and s['cell_size']==32)
        self.assertEqual(working['dimensions'], [64,128])
        self.assertEqual(working['cells'][3]['rect'], [0,64,32,32])

    def test_corrupt_frame_rejected(self):
        (self.out/self.manifest['frames'][0]['path']).write_bytes(b'corrupt')
        with self.assertRaisesRegex(ValueError, 'checksum'):
            pack(self.out)

    def test_missing_frame_rejected(self):
        self.manifest['frames'].pop(); self.save()
        with self.assertRaisesRegex(ValueError, 'count/order'):
            pack(self.out)

    def test_reordered_frame_rejected(self):
        self.manifest['frames'].reverse(); self.save()
        with self.assertRaisesRegex(ValueError, 'count/order'):
            pack(self.out)

    def replace_first(self, image):
        record = self.manifest['frames'][0]
        image.save(self.out/record['path'])
        record['sha256'] = digest(self.out/record['path']); self.save()

    def test_opaque_rectangle_rejected(self):
        self.replace_first(Image.new('RGBA', (32,32), (90,80,70,255)))
        with self.assertRaisesRegex(ValueError, 'Opaque rectangle'):
            pack(self.out)

    def test_clipping_rejected(self):
        image = Image.new('RGBA', (32,32))
        ImageDraw.Draw(image).rectangle((0,5,20,20), fill=(255,0,0,255))
        self.replace_first(image)
        with self.assertRaisesRegex(ValueError, 'Clipped'):
            pack(self.out)

    def test_duplicate_animation_rejected(self):
        a, b = self.manifest['frames'][2:4]
        (self.out/b['path']).write_bytes((self.out/a['path']).read_bytes())
        b['sha256'] = digest(self.out/b['path']); self.save()
        with self.assertRaisesRegex(ValueError, 'Duplicate animation'):
            pack(self.out)

    def test_bad_config_rejected(self):
        cfg = copy.deepcopy(self.cfg); cfg['states'] = {'../unsafe': [0]}
        with self.assertRaises(ValueError): validate_config(cfg)
        cfg = copy.deepcopy(self.cfg); cfg['sizes'] = [512]
        with self.assertRaises(ValueError): validate_config(cfg)


if __name__ == '__main__':
    unittest.main()
