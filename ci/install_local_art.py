"""Install the accepted graphics build into the user's actual Factorio mods."""
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
    p=argparse.ArgumentParser()
    p.add_argument('--package',type=Path,required=True)
    p.add_argument('--backup',type=Path,required=True)
    p.add_argument('--version',required=True)
    p.add_argument('--expected-sha256',required=True)
    a=p.parse_args()
    source=a.package.resolve();backup=a.backup.resolve()
    expected=a.expected_sha256.lower()
    assert len(expected)==64 and all(c in '0123456789abcdef' for c in expected)
    assert sha(source)==expected,'Package differs from the tested accepted build'
    mods=(Path(os.environ['APPDATA'])/'Factorio/mods').resolve()
    assert mods.is_dir()
    root='tanks_for_bob_fork_'+a.version
    target=mods/(root+'.zip')
    assert target.resolve().parent==mods
    required={
      'cooking-fire-v2':'prototypes/generated_graphics/cooking-fire-v2-production.lua',
      'solar-boiler-v8':'prototypes/generated_graphics/solar-boiler-v8-production.lua',
      'fish-pond-v2':'prototypes/generated_graphics/fish-pond-v2-production.lua',
      'primitive-pipe-pump-v3':'prototypes/generated_graphics/primitive-pipe-pump-v3-production.lua'}
    with zipfile.ZipFile(source) as z:
        assert z.testzip() is None
        assert json.loads(z.read(root+'/info.json'))['version']==a.version
        final=z.read(root+'/data-final-fixes.lua').decode()
        for name,path in required.items():
            assert (path[:-4].replace('/','.')) in final
            assert z.read(root+'/'+path)
            assert any(name in n and n.endswith('.png') for n in z.namelist())
        file_count=len(z.namelist())
    listing=json.loads((mods/'mod-list.json').read_text())
    assert any(m['name']=='tanks_for_bob_fork' and m['enabled'] for m in listing['mods'])
    assert all(not m.get('version') or m['version']==a.version for m in listing['mods'] if m['name']=='tanks_for_bob_fork'), 'User mod list pins a different Tanks version'
    backup.mkdir(parents=True,exist_ok=False)
    for name in ('mod-list.json','mod-settings.dat'):
        if (mods/name).is_file():shutil.copy2(mods/name,backup/name)
    old=[]
    for file in mods.glob('tanks_for_bob_fork_*.zip'):
        if file==target and sha(file)==expected:continue
        shutil.copy2(file,backup/file.name)
        old.append({'file':file.name,'sha256':sha(file)})
    if not target.exists() or sha(target)!=expected:
        temporary=mods/(root+'.installing')
        assert temporary.resolve().parent==mods and not temporary.exists()
        shutil.copy2(source,temporary)
        assert sha(temporary)==expected
        temporary.replace(target)
    assert sha(target)==expected
    with zipfile.ZipFile(target) as installed:
        assert installed.testzip() is None and len(installed.namelist())==file_count
    report={'installed':True,'version':a.version,'target':str(target),'sha256':expected,
      'package_files':file_count,'verified_graphics':list(required),'previous_packages_preserved':old,
      'mod_list_changed':False,'saves_modified':False,'runtime_reload_verified':False}
    (backup/'installation-receipt.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
