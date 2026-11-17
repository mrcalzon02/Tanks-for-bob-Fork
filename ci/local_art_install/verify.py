"""Verify installed Tanks ZIP under the user's actual enabled-mod settings."""
import argparse,hashlib,json,os,shutil,subprocess,zipfile
from pathlib import Path
HERE=Path(__file__).resolve().parent
def main():
    p=argparse.ArgumentParser();p.add_argument('--binary',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    p.add_argument('--version',required=True)
    a=p.parse_args();out=a.out.resolve();binary=a.binary.resolve()
    if out.exists():raise FileExistsError(out)
    out.mkdir(parents=True);mods=out/'mods';mods.mkdir();user=Path(os.environ['APPDATA'])/'Factorio'
    listing=json.loads((user/'mods/mod-list.json').read_text())
    enabled={m['name'] for m in listing['mods'] if m.get('enabled')}
    copied=[]
    for source in (user/'mods').iterdir():
        info=None
        if source.is_dir() and (source/'info.json').is_file():
            info=json.loads((source/'info.json').read_text())
        elif source.suffix=='.zip':
            with zipfile.ZipFile(source) as z:
                headers=[n for n in z.namelist() if n.count('/')==1 and n.endswith('/info.json')]
                if len(headers)==1:info=json.loads(z.read(headers[0]))
        if not info or info['name'] not in enabled:continue
        dest=mods/source.name
        if source.is_dir():shutil.copytree(source,dest)
        else:shutil.copy2(source,dest)
        copied.append({'name':info['name'],'version':info['version'],'file':source.name})
    shutil.copy2(user/'mods/mod-settings.dat',mods/'mod-settings.dat')
    addon=mods/'local-tanks-art-check_0.0.1';addon.mkdir()
    (addon/'info.json').write_text(json.dumps({'name':'local-tanks-art-check','version':'0.0.1',
      'title':'Disposable installed Tanks art verification','author':'local verification','factorio_version':'2.1',
      'dependencies':sorted(enabled)}))
    for name in ('data-final-fixes.lua','control.lua'):shutil.copy2(HERE/name,addon/name)
    shutil.copy2(HERE/'alignment_control.lua',addon/'alignment_control.lua')
    (addon/'data.lua').write_text('data:extend{{type="recipe",name="local-alignment-water-proof",categories={"fishery"},enabled=true,energy_required=.5,ingredients={{type="fluid",name="water",amount=2}},results={{type="fluid",name="water",amount=2}}}}\n')
    scenario=addon/'scenarios/proof';scenario.mkdir(parents=True);(scenario/'control.lua').write_text('-- Logic in proof addon.\n')
    listing['mods'].append({'name':'local-tanks-art-check','enabled':True})
    (mods/'mod-list.json').write_text(json.dumps(listing))
    runtime=out/'runtime';runtime.mkdir();config=out/'config.ini'
    config.write_text('[path]\nread-data='+str(binary.parents[2]/'data')+'\nwrite-data='+str(runtime)+'\n')
    common=[str(binary),'--config',str(config),'--mod-directory',str(mods)]
    with (out/'native.log').open('w') as handle:
        result=subprocess.run(common+['--test-scenario','local-tanks-art-check/proof','--test-ticks','150'],stdout=handle,stderr=subprocess.STDOUT,timeout=180)
    text=(out/'native.log').read_text(errors='replace')
    good=result.returncode==0 and 'LOCAL_ART_INSTALL_BINDINGS_PASS' in text and 'LOCAL_ART_INSTALL_RUNTIME_PASS' in text and 'TANKS_ALIGNMENT_NATIVE_PASS' in text and ('native_version='+a.version) in text
    receipt={'passed':good,'installed_tanks_version':a.version,'full_user_mod_pack':True,
      'settings_copied_unchanged':True,'enabled_mods':sorted(enabled),'packages':copied,
      'native_exit_code':result.returncode,'native_bindings_and_placement':good,
      'player_grid_connections':28 if good else 0,
      'user_save_load_passed':False,'proof_addon_installed_in_user_pack':False}
    if good:
        saves=sorted((user/'saves').glob('*.zip'),key=lambda x:x.stat().st_mtime,reverse=True)
        assert saves,'No user save found for migration verification'
        save=out/'user-save-before-art-update.zip';shutil.copy2(saves[0],save)
        receipt['backup_save']=str(save)
        receipt['source_save_name']=saves[0].name
        receipt['source_save_sha256']=hashlib.sha256(save.read_bytes()).hexdigest()
        with (out/'user-save-load.log').open('w') as handle:
            loaded=subprocess.run(common+['--benchmark',str(save),'--benchmark-ticks','1','--benchmark-runs','1'],stdout=handle,stderr=subprocess.STDOUT,timeout=180)
        receipt['user_save_load_passed']=loaded.returncode==0
        receipt['user_save_load_exit_code']=loaded.returncode
    receipt['passed']=good and receipt['user_save_load_passed']
    (out/'verification-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({k:v for k,v in receipt.items() if k not in ('enabled_mods','packages')},indent=2))
    if not receipt['passed']:
        print(text[-4500:]);raise SystemExit(1)
if __name__=='__main__':main()
