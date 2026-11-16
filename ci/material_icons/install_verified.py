"""Install the verified icon package, preserving the previous installed package."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import zipfile


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--package', type=Path, required=True)
    parser.add_argument('--verification', type=Path, required=True)
    parser.add_argument('--backup', type=Path, required=True)
    args = parser.parse_args()
    proof = json.loads(args.verification.read_text())
    assert proof['passed'] and proof['direct_icons'] == 107 and proof['research_icons'] == 10
    assert proof['non_icon_record_changes'] == 0
    assert sha(args.package) == proof['package_sha256']
    root = 'tanks_for_bob_fork_1.8.103'
    with zipfile.ZipFile(args.package) as archive:
        assert archive.testzip() is None
        final = archive.read(root + '/data-final-fixes.lua').decode('utf-8-sig')
        for module in ('material-icons-v01', 'primitive-pipe-pump-v3-production', 'fish-pond-v2-production'):
            assert 'require("prototypes.generated_graphics.' + module + '")' in final
        for icon in proof['icons']:
            rel = icon['icon'].split('__tanks_for_bob_fork__/', 1)[1]
            assert hashlib.sha256(archive.read(root + '/' + rel)).hexdigest() == icon['sha256']
    mods = (Path(os.environ['APPDATA']) / 'Factorio/mods').resolve()
    target = mods / (root + '.zip')
    temporary = mods / (root + '.icons-installing')
    assert target.is_file() and target.resolve().parent == mods and not temporary.exists()
    listing = (mods / 'mod-list.json').read_bytes()
    assert any(m['name'] == 'tanks_for_bob_fork' and m['enabled'] for m in json.loads(listing)['mods'])
    args.backup.mkdir(parents=True, exist_ok=False)
    previous = sha(target)
    shutil.copy2(target, args.backup / target.name)
    for name in ('mod-list.json', 'mod-settings.dat'):
        if (mods / name).is_file():
            shutil.copy2(mods / name, args.backup / name)
    shutil.copy2(args.package, temporary)
    assert sha(temporary) == proof['package_sha256']
    temporary.replace(target)
    assert sha(target) == proof['package_sha256'] and (mods / 'mod-list.json').read_bytes() == listing
    receipt = {'installed': True, 'target': str(target), 'sha256': sha(target), 'previous_sha256': previous, 'previous_package_backup': str((args.backup / target.name).resolve()), 'direct_icons': 107, 'research_icons': 10, 'mod_list_changed': False, 'saves_modified': False, 'restart_required': True}
    (args.backup / 'installation-receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
