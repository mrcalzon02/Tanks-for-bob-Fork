"""Quick native grid proof and genuine captures for the three affected assets."""
import argparse,hashlib,importlib.util,json,shutil,subprocess,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
import sys
sys.path.insert(0,str(ROOT/'ci'))
from validate_mod import select_mod
spec=importlib.util.spec_from_file_location('png_integrity',ROOT/'ci/primitive_pipe_pump_v3/capture_gui.py')
integrity=importlib.util.module_from_spec(spec);spec.loader.exec_module(integrity)
def main():
    p=argparse.ArgumentParser();p.add_argument('--binary',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--capture',action='store_true');a=p.parse_args()
    out=a.out.resolve();binary=a.binary.resolve()
    if out.exists():raise FileExistsError(out)
    out.mkdir(parents=True);mods=out/'mods';mods.mkdir()
    source,metadata=select_mod()
    shutil.copytree(source,mods/source.name)
    addon=mods/'local-alignment-proof_0.0.1';addon.mkdir()
    (addon/'info.json').write_text(json.dumps({'name':'local-alignment-proof','version':'0.0.1','title':'Temporary native grid alignment proof','author':'local proof','factorio_version':'2.1','dependencies':['base','tanks_for_bob_fork']}))
    shutil.copy2(HERE/'alignment_control.lua',addon/'alignment_control.lua')
    (addon/'control.lua').write_text("local f=require('alignment_control')\nscript.on_init(f.initialize)\nscript.on_nth_tick(30,f.tick)\n")
    (addon/'data.lua').write_text('data:extend{{type="recipe",name="local-alignment-water-proof",categories={"fishery"},enabled=true,energy_required=.5,ingredients={{type="fluid",name="water",amount=2}},results={{type="fluid",name="water",amount=2}}}}\n')
    scenario=addon/'scenarios/proof';scenario.mkdir(parents=True);(scenario/'control.lua').write_text('-- Proof logic in addon.\n')
    listing={'mods':[{'name':n,'enabled':n in ('base','tanks_for_bob_fork','local-alignment-proof')} for n in ('base','elevated-rails','quality','recycler','space-age','tanks_for_bob_fork','local-alignment-proof')]}
    runtime=out/'runtime';runtime.mkdir();config=out/'config.ini'
    config.write_text('[path]\nread-data='+str(binary.parents[2]/'data')+'\nwrite-data='+str(runtime)+'\n[graphics]\nfull-screen=false\n')
    (mods/'mod-list.json').write_text(json.dumps(listing));common=[str(binary),'--config',str(config),'--mod-directory',str(mods)]
    with (out/'native.log').open('w') as f:r=subprocess.run(common+['--test-scenario','local-alignment-proof/proof','--test-ticks','150'],stdout=f,stderr=subprocess.STDOUT,timeout=120)
    text=(out/'native.log').read_text(errors='replace');passed=r.returncode==0 and 'TANKS_ALIGNMENT_NATIVE_PASS' in text
    if not passed:print(text[-4000:]);raise SystemExit(1)
    receipt={'source_version':metadata['version'],'native_grid_connections_passed':True,'player_grid_connections':28,'graphical_captured':False,'visual_review_passed':False}
    if a.capture:
        save=out/'alignment.zip'
        with (out/'create.log').open('w') as f:r=subprocess.run(common+['--create',str(save)],stdout=f,stderr=subprocess.STDOUT,timeout=120)
        assert r.returncode==0
        cap=mods/'local-alignment-capture_0.0.1';cap.mkdir()
        (cap/'info.json').write_text(json.dumps({'name':'local-alignment-capture','version':'0.0.1','title':'Temporary graphical alignment capture','author':'local proof','factorio_version':'2.1','dependencies':['local-alignment-proof']}))
        listing['mods'].append({'name':'local-alignment-capture','enabled':True});(mods/'mod-list.json').write_text(json.dumps(listing))
        (out/'steam_appid.txt').write_text('427520')
        expected=[runtime/f'script-output/tanks-alignment/{kind}-{d}-{mode}.png' for kind in ('pump','solar','pond') for d in ('north','east','south','west') for mode in ('pipes','caps')]
        startup=subprocess.STARTUPINFO();startup.dwFlags|=subprocess.STARTF_USESHOWWINDOW;startup.wShowWindow=0
        with (out/'client.log').open('w') as f:
            process=subprocess.Popen(common+['--load-game',str(save),'--disable-audio','--disable-migration-window'],cwd=out,stdout=f,stderr=subprocess.STDOUT,startupinfo=startup)
            try:
                deadline=time.monotonic()+90
                while time.monotonic()<deadline:
                    if all(integrity.valid_png(x) for x in expected):break
                    if process.poll() is not None or 'non-recoverable error' in (out/'client.log').read_text(errors='replace'):break
                    time.sleep(.25)
                receipt['graphical_captured']=all(integrity.valid_png(x) for x in expected)
            finally:
                if process.poll() is None:
                    process.terminate()
                    try:process.wait(timeout=8)
                    except subprocess.TimeoutExpired:process.kill();process.wait(timeout=8)
        if receipt['graphical_captured']:
            receipt['screenshots']=[]
            for file in expected:
                shutil.copy2(file,out/file.name);receipt['screenshots'].append({'file':file.name,'sha256':hashlib.sha256(file.read_bytes()).hexdigest()})
    (out/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps({k:v for k,v in receipt.items() if k!='screenshots'},indent=2))
    if a.capture and not receipt['graphical_captured']:raise SystemExit('Graphical capture incomplete')
if __name__=='__main__':main()
