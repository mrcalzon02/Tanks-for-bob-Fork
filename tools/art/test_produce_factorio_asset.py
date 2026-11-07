"""Fail-closed regression checks for repeatable directional Factorio packaging."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from PIL import Image, ImageDraw

import produce_factorio_asset as prod


class FourWayProductionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.capture = self.root/'capture'
        self.capture.mkdir()
        self.job = {'asset':'campfire','revision':'test','primary_size':32,
                    'sizes':[32], 'active_state':'burning',
                    'mod_name':'example_mod','scale':0.5,'shift':[0,0]}
        self.cfg = {'fps':8,'states':{'idle':[0],'burning':[1,2]},
                    'directions':[0,90,180,270],
                    'camera_override':{'elevation_deg':45,'azimuth_deg':0,'ortho_scale':2.2}}

    def sheet(self, count, size=32):
        cols = min(8,count)
        rows = (count+cols-1)//cols
        img = Image.new('RGBA',(cols*size,4*rows*size))
        for d in range(4):
            for frame in range(count):
                x = (frame%cols)*size
                y = (d*rows+frame//cols)*size
                ImageDraw.Draw(img).ellipse((x+6,y+6,x+22,y+22),
                    fill=(40+d*40,40+frame*50,55,255))
        path=self.capture/f'source-{count}.png'
        img.save(path)
        return {'path':path.name,'columns':cols,'rows_per_direction':rows}

    def test_static_idle_repeats_to_animation_frame_count(self):
        src=self.sheet(1)
        sheet, cols, rows=prod.atlas(self.capture,src,1,16,32)
        self.assertEqual(sheet.size,(256,256))
        self.assertEqual((cols,rows),(8,2))
        self.assertEqual(sheet.crop((0,0,32,32)).tobytes(),
                         sheet.crop((32,0,64,32)).tobytes())
        self.assertNotEqual(sheet.crop((0,0,32,32)).tobytes(),
                            sheet.crop((0,64,32,96)).tobytes())

    def test_each_view_has_distinct_animation(self):
        src=self.sheet(2)
        sheet, cols, rows=prod.atlas(self.capture,src,2,2,32)
        self.assertEqual((cols,rows),(2,1))
        self.assertEqual(sheet.size,(64,128))
        self.assertNotEqual(sheet.crop((0,0,32,32)).tobytes(),
                            sheet.crop((32,0,64,32)).tobytes())
        self.assertNotEqual(sheet.crop((0,0,32,32)).tobytes(),
                            sheet.crop((0,32,32,64)).tobytes())

    def test_directional_lua_coordinates_and_animation_speed(self):
        code = prod.directional_lua(self.job,self.cfg,'asset.png',32,16,8,2)
        self.assertIn('north =',code)
        self.assertIn('east =',code)
        self.assertIn('south =',code)
        self.assertIn('west =',code)
        for offset in (0,64,128,192):
            self.assertIn(f'y = {offset}',code)
        self.assertIn('frame_count = 16',code)
        self.assertIn('animation_speed = 0.13333333',code)
        self.assertIn('scale = 0.5',code)

    def test_bad_frame_count_rejected(self):
        src=self.sheet(2)
        with self.assertRaises(ValueError):
            prod.atlas(self.capture,src,2,3,32)

    def test_no_sprite_overwrites(self):
        mod=self.root/'mod'
        (mod/'graphics/entity').mkdir(parents=True)
        old=mod/'graphics/entity/campfire-test-idle.png'
        old.write_bytes(b'original must not change')
        with self.assertRaises(FileExistsError):
            prod.preflight(self.job,self.root/'newrun',mod,True)
        self.assertEqual(old.read_bytes(),b'original must not change')

    def test_bad_output_path_rejected(self):
        with patch.object(prod,'ROOT',self.root):
            with self.assertRaises(ValueError):
                prod.in_repo('../escape')

    def test_wrong_source_profile_rejected(self):
        with patch.object(prod,'ROOT',self.root):
            mod=self.root/'mod'
            mod.mkdir()
            (mod/'info.json').write_text('{"name":"example_mod"}')
            profile=self.root/'profile.json'
            profile.write_text(json.dumps({'directions':[0,90], 'states':{'idle':[0]},
                 'camera_override':{'elevation_deg':45,'azimuth_deg':0,'ortho_scale':2.2},
                 'sizes':[32], 'fps':8}))
            job=dict(self.job, schema=1, capture_profile='profile.json',mod_root='mod')
            p=self.root/'job.json'
            p.write_text(json.dumps(job))
            with self.assertRaisesRegex(ValueError,'cardinal'):
                prod.load_job('job.json')


if __name__=='__main__':
    unittest.main()
