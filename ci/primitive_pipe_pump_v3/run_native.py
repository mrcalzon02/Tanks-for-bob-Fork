"""Run the active mod's pipe-pump integration in an isolated native profile."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent

def main():
    p=argparse.ArgumentParser();p.add_argument('--binary',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    a=p.parse_args();binary=a.binary.resolve();out=a.out.resolve()
    if out.exists():raise FileExistsError(out)
    out.mkdir(parents=True)
    version=subprocess.check_output([str(binary),'--version'],text=True)
    assert '2.1.24' in version
    mods=out/'mods';mods.mkdir()
    shutil.copytree(ROOT/'tanks_for_bob_fork_1.8.103',mods/'tanks_for_bob_fork_1.8.103')
    addon=mods/'pipe-pump-v3-proof_0.0.1';addon.mkdir()
    (addon/'info.json').write_text(json.dumps({'name':'pipe-pump-v3-proof','version':'0.0.1','title':'Temporary pipe-pump proof','author':'local test','factorio_version':'2.1','dependencies':['base','tanks_for_bob_fork']}))
    shutil.copy2(HERE/'control.lua',addon/'control.lua')
    scenario=addon/'scenarios/proof';scenario.mkdir(parents=True);(scenario/'control.lua').write_text('-- Logic in proof add-on.\n')
    (mods/'mod-list.json').write_text(json.dumps({'mods':[{'name':name,'enabled':name in ('base','tanks_for_bob_fork','pipe-pump-v3-proof')} for name in ('base','elevated-rails','quality','recycler','space-age','tanks_for_bob_fork','pipe-pump-v3-proof')]}))
    runtime=out/'runtime';runtime.mkdir()
    config=out/'config.ini';config.write_text('[path]\nread-data='+str(binary.parents[2]/'data')+'\nwrite-data='+str(runtime)+'\n')
    common=[str(binary),'--config',str(config),'--mod-directory',str(mods)]
    logfile=out/'native.log'
    with logfile.open('w') as f:result=subprocess.run(common+['--test-scenario','pipe-pump-v3-proof/proof','--test-ticks','300'],stdout=f,stderr=subprocess.STDOUT,timeout=180)
    log=logfile.read_text(errors='replace');passed=result.returncode==0 and 'PIPE_PUMP_V3_NATIVE_PASS' in log
    receipt={'engine':version.strip(),'exit_code':result.returncode,'native_pass':passed,'reload_pass':False,'visual_alignment_verified':False}
    if passed:
        saves=list((runtime/'saves').glob('*pipe-pump-v3-proof*.zip'))
        if not saves:
            save=out/'pipe-pump-v3-proof.zip'
            with (out/'create-save.log').open('w') as f:created=subprocess.run(common+['--create',str(save)],stdout=f,stderr=subprocess.STDOUT,timeout=180)
            if created.returncode==0 and save.is_file():saves=[save]
        if saves:
            reload_log=out/'reload.log'
            with reload_log.open('w') as f:reload_result=subprocess.run(common+['--test-save',str(saves[-1]),'--test-ticks','300'],stdout=f,stderr=subprocess.STDOUT,timeout=180)
            receipt['reload_pass']=reload_result.returncode==0 and 'PIPE_PUMP_V3_RELOAD_PASS' in reload_log.read_text(errors='replace')
            receipt['saved_fixture']=str(saves[-1])
    (out/'engine-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))
    if not passed:print(log[-6000:]);raise SystemExit(1)
    if not receipt['reload_pass']:raise SystemExit('Native transfer passed; save/reload evidence incomplete')

if __name__=='__main__':main()
