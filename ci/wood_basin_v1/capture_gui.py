"""Capture native empty/filling/full/drained/flow tank screenshots, in an isolated hidden client."""
import argparse
import ctypes
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import struct
import time
import zlib

HERE=Path(__file__).resolve().parent

def valid_png(file):
    if not file.is_file():return False
    data=file.read_bytes()
    if not data.startswith(b'\x89PNG\r\n\x1a\n'):return False
    pos=8
    while pos+12<=len(data):
        length=struct.unpack_from('>I',data,pos)[0];kind=data[pos+4:pos+8]
        end=pos+12+length
        if end>len(data):return False
        if zlib.crc32(data[pos+4:pos+8+length])!=struct.unpack_from('>I',data,pos+8+length)[0]:return False
        if kind==b'IEND':return end==len(data)
        pos=end
    return False

def main():
    p=argparse.ArgumentParser();p.add_argument('--native-profile',type=Path,required=True);p.add_argument('--binary',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    a=p.parse_args();profile=a.native_profile.resolve();out=a.out.resolve();binary=a.binary.resolve()
    if out.exists():raise FileExistsError(out)
    session=ctypes.c_ulong();ctypes.windll.kernel32.ProcessIdToSessionId(os.getpid(),ctypes.byref(session))
    assert session.value!=0,'Graphical capture needs the interactive desktop session'
    out.mkdir(parents=True);mods=out/'mods';shutil.copytree(profile/'mods',mods)
    addon=mods/'wood-basin-v1-capture_0.0.1';addon.mkdir()
    (addon/'info.json').write_text(json.dumps({'name':'wood-basin-v1-capture','version':'0.0.1','title':'Temporary graphical pump capture','author':'local proof','factorio_version':'2.1','dependencies':['base','tanks_for_bob_fork','wood-basin-v1-proof']}))
    shutil.copy2(HERE/'gui-control.lua',addon/'control.lua')
    modlist=json.loads((mods/'mod-list.json').read_text());modlist['mods'].append({'name':'wood-basin-v1-capture','enabled':True})
    (mods/'mod-list.json').write_text(json.dumps(modlist))
    runtime=out/'runtime';runtime.mkdir()
    config=out/'config.ini';config.write_text('[path]\nread-data='+str(binary.parents[2]/'data')+'\nwrite-data='+str(runtime)+'\n[graphics]\nfull-screen=false\n')
    save=profile/'wood-basin-v1-proof.zip'
    assert save.is_file()
    (out/'steam_appid.txt').write_text('427520',encoding='ascii')
    args=[str(binary),'--config',str(config),'--mod-directory',str(mods),'--load-game',str(save),'--disable-audio','--disable-migration-window']
    startup=subprocess.STARTUPINFO();startup.dwFlags|=subprocess.STARTF_USESHOWWINDOW;startup.wShowWindow=0
    capture=runtime/'script-output/wood-basin-v1'
    expected=[capture/(name+'-'+zoom+'.png') for name in ('north','east','south','west') for zoom in ('empty','filling','full','full-later','drained','refill','oil','steam')]
    log=out/'client.log'
    with log.open('w') as handle:
        process=subprocess.Popen(args,stdout=handle,stderr=subprocess.STDOUT,startupinfo=startup,cwd=out)
        try:
            deadline=time.monotonic()+90
            while time.monotonic()<deadline:
                if all(valid_png(f) for f in expected) and list((runtime/'saves').glob('*wood-basin-complete-client*.zip')) and log.read_text(errors='replace').rfind('Saving finished') > log.read_text(errors='replace').rfind('Saving to _autosave-wood-basin-complete-client'):break
                if process.poll() is not None:break
                current=log.read_text(errors='replace')
                if 'non-recoverable error' in current or 'WOOD_BASIN_GUI: missing' in current:break
                time.sleep(.25)
            passed=all(valid_png(f) for f in expected)
        finally:
            if process.poll() is None:
                process.terminate()
                try:process.wait(timeout=10)
                except subprocess.TimeoutExpired:process.kill();process.wait(timeout=10)
    receipt={'genuine_factorio_client_capture':passed,'windows_session':session.value,'screenshots':[],'visual_review_passed':False,'completed_save':[str(p) for p in (runtime/'saves').glob('*wood-basin-complete-client*.zip')]}
    if passed:
        for file in expected:
            shutil.copy2(file,out/file.name)
            receipt['screenshots'].append({'file':file.name,'sha256':hashlib.sha256(file.read_bytes()).hexdigest()})
    (out/'capture-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))
    if not passed:print(log.read_text(errors='replace')[-5000:]);raise SystemExit(1)

if __name__=='__main__':main()
