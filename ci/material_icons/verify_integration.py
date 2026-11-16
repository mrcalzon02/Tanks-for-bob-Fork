"""Verify the current Tanks source against the user's mod pack in isolation."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import struct
import subprocess

ROOT = Path(__file__).resolve().parents[2]
MOD = ROOT / 'tanks_for_bob_fork_1.8.103'
HOOK = 'require("prototypes.generated_graphics.material-icons-v01")'
ICON_FIELDS = {'icon', 'icons', 'icon_size', 'icon_mipmaps'}


def snapshot(source, target):
    if source.is_dir():
        target.mkdir(parents=True, exist_ok=True)
        for child in source.iterdir():
            snapshot(child, target / child.name)
    elif source.suffix.lower() in {'.png', '.ogg', '.wav', '.zip'}:
        try:
            os.link(source, target)
        except OSError:
            shutil.copy2(source, target)
    else:
        shutil.copy2(source, target)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--binary', type=Path, required=True)
    parser.add_argument('--user-mods', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=False)
    mods = out / 'mods'
    mods.mkdir()
    # Snapshot the real enabled pack, retaining settings without touching it.
    for p in args.user_mods.iterdir():
        if p.name.startswith('tanks_for_bob_fork_'):
            continue
        if p.is_dir() or p.suffix == '.zip' or p.name in {'mod-list.json', 'mod-settings.dat'}:
            snapshot(p, mods / p.name)
    target = mods / MOD.name
    snapshot(MOD, target)
    listing = json.loads((mods / 'mod-list.json').read_text())
    assert any(m['name'] == 'tanks_for_bob_fork' and m['enabled'] for m in listing['mods'])
    final = target / 'data-final-fixes.lua'
    original = final.read_text(encoding='utf-8-sig')
    assert original.count(HOOK) == 1
    runtime = out / 'runtime'
    runtime.mkdir()
    config = out / 'config.ini'
    config.write_text('[path]\nread-data=' + str(args.binary.resolve().parents[2] / 'data') + '\nwrite-data=' + str(runtime) + '\n')
    dumps = {}
    for stage in ('before', 'after'):
        final.write_text(original.replace(HOOK, '-- icon hook omitted for matched baseline') if stage == 'before' else original)
        with (out / (stage + '.log')).open('w') as log:
            result = subprocess.run([str(args.binary), '--config', str(config), '--mod-directory', str(mods), '--disable-audio', '--dump-data'], cwd=out, stdout=log, stderr=subprocess.STDOUT, timeout=240)
        assert result.returncode == 0, f'{stage} native load failed; inspect {out / (stage + ".log")}'
        dump = runtime / 'script-output/data-raw-dump.json'
        dumps[stage] = json.loads(dump.read_text())
        shutil.copy2(dump, out / (stage + '-data-raw.json'))
    before, after = dumps['before'], dumps['after']
    icon_changes = []
    assert before.keys() == after.keys()
    for kind in before:
        assert before[kind].keys() == after[kind].keys(), kind
        for name, old in before[kind].items():
            new = after[kind][name]
            if old == new:
                continue
            assert {k:v for k,v in old.items() if k not in ICON_FIELDS} == {k:v for k,v in new.items() if k not in ICON_FIELDS}, (kind, name, 'non-icon delta')
            icon_changes.append({'type': kind, 'name': name})
    assets = json.loads((ROOT / 'tools/art/material_icons/assets.json').read_text())
    checked = []
    for asset, spec in assets.items():
        proto = after[spec['type']][spec['name']]
        expected = '__tanks_for_bob_fork__/graphics/icons/material-icons-v01/' + asset + '.png'
        assert proto['icon'] == expected and proto['icon_size'] == 64 and not proto.get('icons'), (asset, proto.get('icon'))
        path = target / 'graphics/icons/material-icons-v01' / (asset + '.png')
        image = path.read_bytes()
        assert image[:8] == b'\x89PNG\r\n\x1a\n' and struct.unpack('>II', image[16:24]) == (64, 64)
        checked.append({'type': spec['type'], 'name': spec['name'], 'icon': expected, 'sha256': hashlib.sha256(image).hexdigest()})
    assert len(checked) == 107
    adapter = (target / 'prototypes/generated_graphics/material-icons-v01.lua').read_text()
    research = re.findall(r'if data.raw.technology\["([^"]+)"\].*?root\.\."([^"]+\.png)"', adapter)
    assert len(research) == 10
    for name, image in research:
        assert after['technology'][name]['icon'] == '__tanks_for_bob_fork__/graphics/icons/material-icons-v01/' + image
    # Both newer structure hooks must survive the icon integration.
    for module in ('primitive-pipe-pump-v3-production', 'fish-pond-v2-production'):
        assert 'require("prototypes.generated_graphics.' + module + '")' in original
    receipt = {'passed': True, 'full_user_mod_pack': True, 'matched_current_source': True, 'native_loads': 2, 'direct_icons': len(checked), 'research_icons': len(research), 'icon_record_changes': len(icon_changes), 'non_icon_record_changes': 0, 'newer_structure_hooks_preserved': True, 'actual_user_profile_modified': False, 'icons': checked, 'icon_changes': icon_changes}
    (out / 'verification.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps({k:v for k,v in receipt.items() if k not in {'icons', 'icon_changes'}}, indent=2))


if __name__ == '__main__':
    main()
