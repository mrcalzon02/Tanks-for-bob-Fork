"""Read actual current actual Tanks condenser contract before refining its asset."""
import argparse,json,shutil,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[2];H=Path(__file__).resolve().parent
sys.path.insert(0,str(R/'ci'))
from validate_mod import select_mod
p=argparse.ArgumentParser();p.add_argument('--binary',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();out=a.out.resolve();binary=a.binary.resolve()
if out.exists():raise FileExistsError(out)
out.mkdir(parents=True);mods=out/'mods';mods.mkdir();source,_=select_mod();shutil.copytree(source,mods/source.name)
addon=mods/'steam-condenser-proof_0.0.1';addon.mkdir();(addon/'info.json').write_text(json.dumps(dict(name='steam-condenser-proof',version='0.0.1',title='Temporary native Tanks Steam Condenser contract',author='local proof',factorio_version='2.1',dependencies=['base','tanks_for_bob_fork'])))
shutil.copy2(H/'contract-control.lua',addon/'control.lua');scenario=addon/'scenarios/proof';scenario.mkdir(parents=True);(scenario/'control.lua').write_text('-- Contract logic in temporary add-on.\n')
(mods/'mod-list.json').write_text(json.dumps({'mods':[{'name':n,'enabled':n in ['base','tanks_for_bob_fork','steam-condenser-proof']} for n in ['base','elevated-rails','quality','recycler','space-age','tanks_for_bob_fork','steam-condenser-proof']]}));runtime=out/'runtime';runtime.mkdir();config=out/'config.ini';config.write_text('[path]\nread-data='+str(binary.parents[2]/'data')+'\nwrite-data='+str(runtime)+'\n')
with (out/'native.log').open('w') as f:result=subprocess.run([str(binary),'--config',str(config),'--mod-directory',str(mods),'--test-scenario','steam-condenser-proof/proof','--test-ticks','1'],stdout=f,stderr=subprocess.STDOUT,timeout=180)
log=(out/'native.log').read_text(errors='replace')
if result.returncode or 'STEAM_CONDENSER_CONTRACT_PASS' not in log:print(log[-5000:]);raise SystemExit(1)
d=json.loads((runtime/'script-output/steam-condenser-v2/contract.json').read_text());print(json.dumps({'entity':d['entity'],'processing_recipes':len(d['processing_recipes']),'fluid_recipes':[x['name'] for x in d['processing_recipes'] if any(i['type']=='fluid' for i in list(x['ingredients'])+list(x['products']))],'building':d['building'],'directions':d['directions']},indent=2))
