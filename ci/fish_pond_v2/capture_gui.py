"""Capture actual Factorio states and legacy comparison in an isolated client."""
import argparse
import ctypes
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import time

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('pump_png_integrity', HERE.parent/'primitive_pipe_pump_v3/capture_gui.py')
integrity = importlib.util.module_from_spec(spec)
spec.loader.exec_module(integrity)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--native-profile', type=Path, required=True)
    parser.add_argument('--binary', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    profile, binary, out = args.native_profile.resolve(), args.binary.resolve(), args.out.resolve()
    if out.exists():
        raise FileExistsError(out)
    receipt = json.loads((profile/'engine-receipt.json').read_text())
    assert receipt['native_pass'] and receipt['reload_pass']
    session = ctypes.c_ulong()
    ctypes.windll.kernel32.ProcessIdToSessionId(os.getpid(),ctypes.byref(session))
    assert session.value != 0, 'Graphical capture needs the interactive desktop session'
    out.mkdir(parents=True)
    mods = out/'mods'
    shutil.copytree(profile/'mods', mods)
    addon = mods/'fish-pond-v2-capture_0.0.1'
    addon.mkdir()
    (addon/'info.json').write_text(json.dumps({'name':'fish-pond-v2-capture','version':'0.0.1',
        'title':'Temporary graphical pond capture','author':'local proof','factorio_version':'2.1',
        'dependencies':['base','tanks_for_bob_fork','fish-pond-v2-proof']}))
    shutil.copy2(HERE/'gui-control.lua',addon/'control.lua')
    modlist = json.loads((mods/'mod-list.json').read_text())
    modlist['mods'].append({'name':'fish-pond-v2-capture','enabled':True})
    (mods/'mod-list.json').write_text(json.dumps(modlist))
    runtime = out/'runtime'
    runtime.mkdir()
    config = out/'config.ini'
    config.write_text('[path]\nread-data='+str(binary.parents[2]/'data')+'\nwrite-data='+str(runtime)+'\n[graphics]\nfull-screen=false\n')
    (out/'steam_appid.txt').write_text('427520',encoding='ascii')
    command = [str(binary),'--config',str(config),'--mod-directory',str(mods),
        '--load-game',str(profile/'fish-pond-v2-proof.zip'),'--disable-audio','--disable-migration-window']
    labels = ('normal','close','idle-close','fluid-close','motion-close','legacy-close')
    capture = runtime/'script-output/fish-pond-v2'
    expected = [capture/(name+'-'+label+'.png') for name in ('north','east','south','west') for label in labels]
    startup = subprocess.STARTUPINFO()
    startup.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startup.wShowWindow = 0
    logfile = out/'client.log'
    with logfile.open('w') as handle:
        process = subprocess.Popen(command, stdout=handle, stderr=subprocess.STDOUT, startupinfo=startup, cwd=out)
        try:
            deadline = time.monotonic()+90
            while time.monotonic() < deadline:
                if all(integrity.valid_png(path) for path in expected):
                    break
                if process.poll() is not None:
                    break
                log = logfile.read_text(errors='replace')
                if 'non-recoverable error' in log or 'FISH_POND_V2_GUI: missing' in log:
                    break
                time.sleep(.25)
            passed = all(integrity.valid_png(path) for path in expected)
        finally:
            if process.poll() is None:
                process.terminate()
                try:
                    process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait(timeout=10)
    result = {'genuine_factorio_client_capture':passed,'windows_session':session.value,
              'visual_review_passed':False,'owner_visual_approved':False,'candidate_only':True,'screenshots':[]}
    if passed:
        for path in expected:
            shutil.copy2(path,out/path.name)
            result['screenshots'].append({'file':path.name,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
    (out/'capture-receipt.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
    if not passed:
        print(logfile.read_text(errors='replace')[-5000:])
        raise SystemExit(1)


if __name__ == '__main__':
    main()
