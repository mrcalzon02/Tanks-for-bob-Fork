"""Reopen the actual user profile and verify its log loads the installed build."""
import argparse,json,os,subprocess,time
from pathlib import Path
def main():
    p=argparse.ArgumentParser();p.add_argument('--binary',type=Path,required=True);p.add_argument('--verified-profile',type=Path,required=True)
    a=p.parse_args();profile=a.verified_profile.resolve()
    check=json.loads((profile/'verification-receipt.json').read_text());assert check['passed']
    user=Path(os.environ['APPDATA'])/'Factorio'
    save=user/'saves'/check['source_save_name'];assert save.is_file()
    # CWD's Steam app id prevents Steam relaunch from dropping --load-game.
    launch=profile/'actual-user-launch';launch.mkdir(exist_ok=False)
    (launch/'steam_appid.txt').write_text('427520',encoding='ascii')
    started=time.time()
    process=subprocess.Popen([str(a.binary.resolve()),'--load-game',str(save)],cwd=launch,
        stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    log=user/'factorio-current.log';success=False
    deadline=time.monotonic()+100
    while time.monotonic()<deadline:
        if log.is_file() and log.stat().st_mtime>=started-1:
            text=log.read_text(errors='replace')
            version=('Loading mod tanks_for_bob_fork '+check['installed_tanks_version']+' (data-final-fixes.lua)') in text
            loaded='Loading level.dat:' in text and 'Checksum for script __tanks_for_bob_fork__/control.lua:' in text
            if version and loaded:
                success=True;break
            if 'Error Util.cpp' in text or 'non-recoverable error' in text:break
        if process.poll() is not None:break
        time.sleep(.5)
    receipt={'actual_user_profile':True,'default_mod_directory':str(user/'mods'),
      'loaded_tanks_version':check['installed_tanks_version'] if success else None,'last_user_save':save.name,
      'user_save_backup':check['backup_save'],'save_and_graphics_loaded':success,
      'process_id':process.pid,'test_addon_used':False,'left_running_for_user':process.poll() is None}
    (profile/'actual-user-launch-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))
    if not success:raise SystemExit('Actual client did not confirm updated save load; inspect its log before any retry.')
if __name__=='__main__':main()
