"""Attachment safety: exact source targeting, guarded runtime Lua and opt-in replacement."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import attach_factorio_prototype as attach


class PrototypeAttachTests(unittest.TestCase):
    def setUp(self):
        self.t = tempfile.TemporaryDirectory()
        self.addCleanup(self.t.cleanup)
        self.root = Path(self.t.name)
        self.mod = self.root / 'test_mod'
        (self.mod/'prototypes/entity').mkdir(parents=True)
        (self.mod/'prototypes/item').mkdir(parents=True)
        (self.mod/'info.json').write_text('{"name":"test_mod"}')
        (self.mod/'data.lua').write_text('require("prototypes.entity.entities")\n')
        (self.mod/'prototypes/entity/entities.lua').write_text('''
        -- do not match: {type="assembling-machine",name="campfire"}
        local ignored = "{type='assembling-machine',name='campfire'}"
        data:extend({
          { type="assembling-machine", name="campfire", graphics_set={ animation={north={width=64}} }, crafting_speed=0.3 },
          { type="assembling-machine", name="different", graphics_set={} }
        })
        ''')
        (self.mod/'prototypes/item/item.lua').write_text('data:extend({{type="item", name="campfire", icon="old.png"}})\n')
        self.job = {
            'asset':'campfire','revision':'v13-repro','mod_name':'test_mod',
            'prototype':{'type':'assembling-machine','name':'campfire',
                'source':'test_mod/prototypes/entity/entities.lua',
                'item_icon':{'type':'item','name':'campfire',
                    'source':'test_mod/prototypes/item/item.lua'}}
        }
        self.out=self.root/'product'
        self.out.mkdir()
        (self.out/'prototype-ready.lua').write_text('''-- Previous generated review
-- Complete states, not overlays.
graphics_set = {
  animation = { north = {filename = "__test_mod__/graphics/entity/campfire-v13-repro-burning.png"},
    east={}, south={},west={} },
  idle_animation = {north={},east={},south={},west={}},
  always_draw_idle_animation = false
}
''')

    def test_exact_declaration_distinguishes_comments_strings_other_entity(self):
        item, ent, icon = attach.validate_target(self.job,self.mod,self.root)
        self.assertEqual(ent['declared_name'],'campfire')
        self.assertEqual(ent['declared_type'],'assembling-machine')
        self.assertEqual(icon['declared_type'],'item')

    def test_wrong_name_or_type_fail_closed(self):
        self.job['prototype']['name']='does-not-exist'
        with self.assertRaisesRegex(ValueError,'Expected one declared'):
            attach.validate_target(self.job,self.mod,self.root)
        self.job['prototype']['type']='mining-drill'
        with self.assertRaisesRegex(ValueError,'Unsupported'):
            attach.validate_target(self.job,self.mod,self.root)

    def test_ambiguous_duplicate_declaration_fails(self):
        p=self.mod/'prototypes/entity/entities.lua'
        p.write_text(p.read_text()+'\ndata:extend({{type="assembling-machine",name="campfire"}})')
        with self.assertRaisesRegex(ValueError,'found 2'):
            attach.validate_target(self.job,self.mod,self.root)

    def test_guarded_generated_module_prevents_wrong_type_and_duplicate_overlay(self):
        code = attach.module_code(self.job,(self.out/'prototype-ready.lua').read_text())
        self.assertIn('data.raw["assembling-machine"]',code)
        self.assertIn('"campfire"',code)
        self.assertIn('assert(target.type == "assembling-machine"',code)
        self.assertIn('visual.north_animation',code)
        self.assertIn('replacement_graphics_set.working_visualisations',code)
        self.assertIn('target.graphics_set = replacement_graphics_set',code)
        self.assertIn('data.raw["item"]',code)
        self.assertIn('item.icon = "__test_mod__/graphics/icons/campfire-v13-repro.png"',code)
        self.assertNotIn('table.deepcopy(',code)

    def test_deploy_preview_install_readback_and_rollback_safety(self):
        plan=attach.prepare_attachment(self.job,self.mod,self.root,self.out)
        self.assertFalse((self.mod/'data-final-fixes.lua').exists())
        self.assertTrue(plan['generated'].exists())
        self.assertTrue(plan['stage'].exists())
        installed=attach.install_attachment(plan)
        self.assertEqual(len(installed),2)
        entry=(self.mod/'data-final-fixes.lua').read_text()
        self.assertIn('-- factorio-art-target: assembling-machine/campfire',entry)
        self.assertIn('require("prototypes.generated_graphics.campfire-v13-repro")',entry)
        self.assertEqual(attach.filehash(plan['generated']),attach.filehash(plan['module']))
        # Original prototype source is NOT altered, only late override registration.
        self.assertIn('crafting_speed=0.3',(self.mod/'prototypes/entity/entities.lua').read_text())
        with self.assertRaises(FileExistsError):
            attach.attachment_plan(self.job,self.mod,self.root,self.out)

    def test_explicit_replacement_requires_new_unique_module(self):
        old='-- user content\n-- factorio-art-target: assembling-machine/campfire\nrequire("prototypes.generated_graphics.campfire-v12")\n'
        with self.assertRaises(FileExistsError):
            attach.update_entry(old,self.job)
        changed=attach.update_entry(old,self.job,replace=True)
        self.assertIn('-- user content',changed)
        self.assertNotIn('campfire-v12',changed)
        self.assertEqual(changed.count('factorio-art-target:'),1)
        self.assertEqual(changed.count('require('),1)
        with self.assertRaises(ValueError):
            attach.update_entry(old+'-- factorio-art-target: assembling-machine/campfire\nrequire("x")\n',self.job,replace=True)

    def test_refuses_suspicious_legacy_target_registration(self):
        old='-- factorio-art-target: assembling-machine/campfire\nprint("something else")\n'
        with self.assertRaisesRegex(ValueError,'Unexpected managed'):
            attach.update_entry(old,self.job,replace=True)

    def test_no_files_outside_the_explicit_mod(self):
        self.job['prototype']['source']='outside.lua'
        (self.root/'outside.lua').write_text('data:extend({{type="assembling-machine",name="campfire"}})')
        with self.assertRaisesRegex(ValueError,'inside the target mod'):
            attach.validate_target(self.job,self.mod,self.root)


if __name__ == '__main__':
    unittest.main()
