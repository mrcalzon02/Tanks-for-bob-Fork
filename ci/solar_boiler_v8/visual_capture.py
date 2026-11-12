#!/usr/bin/env python3
"""Capture *actual* Factorio 2.1 GUI screenshots of V8 with connected pipes.

This is deliberately NOT a Blender render, headless mock or 2D reconstruction.
Uses the Windows graphical Factorio client installed on a trusted runner,
a temporary isolated mod profile, LuaGameScript.take_screenshot and PNG readback.
Refuses success without 16 valid in-game PNGs and native engine log markers.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time
import traceback
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
MOD = ROOT / "tanks_for_bob_fork_1.8.102"
APPROVED = ROOT / "models/island-survival/solar-boiler/generated-v8"
DIRECTIONS = ("north", "east", "south", "west")
GROUNDS = ("natural", "concrete")
ZOOMS = ("normal", "close")
SOURCE_IDS = (0,3,2,1)
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"

def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def require_interactive_desktop() -> int:
    """The Windows Actions service is Session 0: D3D11 GUI output cannot be created there."""
    if os.name != "nt":
        raise RuntimeError("Genuine Factorio GUI capture requires the Windows desktop client")
    import ctypes
    session_id=ctypes.c_ulong(0)
    pid=os.getpid()
    ok=ctypes.windll.kernel32.ProcessIdToSessionId(
        ctypes.c_ulong(pid),ctypes.byref(session_id))
    if not ok:
        raise OSError("Cannot determine Windows desktop session ID")
    if session_id.value == 0:
        raise RuntimeError(
            "INTERACTIVE_DESKTOP_REQUIRED: Windows service Session 0 cannot display "
            "Factorio D3D11: actual engine log showed SDL_DXGIGetOutputInfo failure "
            "and DXGI_ERROR_NOT_CURRENTLY_AVAILABLE (0x887a0022). "
            "Run this exact capture from a logged-on Windows user desktop, not "
            "the GitHub runner service. No in-game screenshot was captured.")
    print("FACTORIO_GRAPHICAL_WINDOWS_SESSION",session_id.value,flush=True)
    return session_id.value

def game_candidates() -> list[Path]:
    """Only known install locations, PATH, and Steam library metadata."""
    found = []
    for name in ("FACTORIO_GUI_EXE", "FACTORIO_CLIENT_PATH", "FACTORIO_EXE"):
        if os.environ.get(name):
            found.append(Path(os.environ[name]).expanduser())
    cmd = shutil.which("factorio.exe") or shutil.which("factorio")
    if cmd:
        found.append(Path(cmd))
    for drive in ("C:", "D:", "E:", "F:"):
        for root in ("Factorio", "Games/Factorio", "SteamLibrary/steamapps/common/Factorio",
                     "Steam/steamapps/common/Factorio",
                     "Program Files (x86)/Steam/steamapps/common/Factorio",
                     "Program Files/Steam/steamapps/common/Factorio",
                     "Program Files/Factorio"):
            found.append(Path(drive + "/" + root + "/bin/x64/factorio.exe"))
    roots = [Path(os.getenv("PROGRAMFILES(X86)", "C:/Program Files (x86)")) / "Steam",
             Path(os.getenv("PROGRAMFILES", "C:/Program Files")) / "Steam"]
    appdata = os.environ.get("LOCALAPPDATA")
    if appdata:
        roots.append(Path(appdata) / "Steam")
    try:
        import winreg
        for key in (r"Software\Valve\Steam",r"Software\WOW6432Node\Valve\Steam"):
            try:
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key) as reg:
                    path,_ = winreg.QueryValueEx(reg, "SteamPath")
                    roots.append(Path(path))
            except OSError:
                pass
    except ImportError:
        pass
    for steam in roots:
        found.append(steam / "steamapps/common/Factorio/bin/x64/factorio.exe")
        libraries = steam / "steamapps/libraryfolders.vdf"
        if not libraries.is_file():
            continue
        try:
            content = libraries.read_text(encoding="utf-8-sig",errors="replace")
        except OSError:
            continue
        for match in re.findall(r'"path"\s+"([^"]+)"', content):
            library = Path(match.replace("\\\\","\\"))
            found.append(library/"steamapps/common/Factorio/bin/x64/factorio.exe")
    # Deterministic and bounded list; do not scan unrelated user directories.
    return list(dict.fromkeys(p.resolve() for p in found))

def find_client(explicit: str | None) -> tuple[Path,str]:
    candidates=([Path(explicit).expanduser().resolve()] if explicit else game_candidates())
    diagnostics=[]
    for path in candidates:
        if not path.is_file():
            continue
        try:
            info=subprocess.run([str(path),"--version"],capture_output=True,text=True,
                                encoding="utf-8",errors="replace",timeout=20)
            version=(info.stdout+"\n"+info.stderr).strip()
            if info.returncode:
                diagnostics.append(f"{path}: --version exit {info.returncode}")
                continue
            if "headless" in version.lower():
                diagnostics.append(f"{path}: HEADLESS BINARY ONLY, graphical screenshots unavailable")
                continue
            match=re.search(r"Version:\s*(\d+)\.(\d+)\.(\d+)",version)
            if not match or tuple(map(int,match.groups()))[:2] != (2,1):
                diagnostics.append(f"{path}: expected graphical Factorio 2.1, got {version[:150]}")
                continue
            data=path.parents[2]/"data"/"base"/"info.json"
            if not data.is_file():
                diagnostics.append(f"{path}: missing Factorio base data at {data}")
                continue
            return path, version
        except Exception as exc:
            diagnostics.append(f"{path}: {exc}")
    raise RuntimeError(
        "NO VERIFIED GRAPHICAL FACTORIO 2.1 CLIENT on this Windows runner. "
        "Set FACTORIO_GUI_EXE to the installed full Factorio.exe. "
        "Checked standard Steam, standalone, and PATH locations. "
        "Diagnostics: "+ "; ".join(diagnostics[-12:]))

def stage_client_profile(exe:Path, temp:Path) -> tuple[Path,Path,list[str]]:
    if temp.exists() and any(temp.iterdir()):
        raise FileExistsError(f"Refuse to mix GUI evidence with an existing run: {temp}")
    temp.mkdir(parents=True, exist_ok=True)
    mods=temp/"mods"
    mods.mkdir()
    assert (MOD/"prototypes/generated_graphics/solar-boiler-v8-production.lua").is_file(), (
        "Solar Boiler V8 production Lua not installed")
    assert (MOD/"graphics/entity/solar-boiler-v8/working-256.png").is_file(), (
        "Solar Boiler V8 production graphic not installed")
    src_native=APPROVED/"solar-boiler-v8.blend"
    receipt=json.loads((APPROVED/"factorio-placement-receipt.json").read_text())
    assert digest(src_native)==receipt["approved_v8_native_sha256"], (
        "Approved Blender V8 source changed")
    shutil.copytree(MOD, mods / "tanks_for_bob_fork_1.8.102")
    addon=mods/"solar-boiler-v8-visual_0.0.1"
    addon.mkdir()
    (addon/"info.json").write_text(json.dumps({
        "name":"solar-boiler-v8-visual","version":"0.0.1",
        "title":"Solar Boiler V8 real graphical pipe screenshots",
        "author":"Tanks CI","factorio_version":"2.1",
        "dependencies":["base >= 2.1.24","tanks_for_bob_fork"]
    },indent=2)+"\n",encoding="utf-8")
    shutil.copy2(HERE/"visual_client_control.lua",addon/"control.lua")
    scenario=addon/"scenarios/pipe-capture"
    scenario.mkdir(parents=True)
    (scenario/"control.lua").write_text(
        "-- Scenario is visually staged by solar-boiler-v8-visual/control.lua.\n",
        encoding="utf-8")
    (scenario/"description.json").write_text(json.dumps({
        "name":"Solar V8 native client four-direction pipe visual comparison"
    })+"\n",encoding="utf-8")
    installed=exe.parents[2]/"data"
    official=("base","elevated-rails","quality","recycler","space-age")
    enabled=[{"name":n,"enabled": (installed/n/"info.json").is_file()} for n in official]
    assert enabled[0]["enabled"],"Missing base game files"
    enabled.extend([{"name":"tanks_for_bob_fork","enabled":True},
                    {"name":"solar-boiler-v8-visual","enabled":True}])
    (mods/"mod-list.json").write_text(json.dumps({"mods":enabled},indent=2)+"\n",
                                       encoding="utf-8")
    userdata=temp/"user-data"
    userdata.mkdir()
    config=temp/"config.ini"
    config.write_text("[path]\nread-data="+str(installed)+
                      "\nwrite-data="+str(userdata)+"\n",encoding="utf-8")
    # Valve-supported development launch: prevent SteamAPI_RestartAppIfNecessary
    # from redirecting our isolated job to Steam and losing CLI scenario args.
    # Write ONLY to per-run scratch; never modify the installed Factorio tree.
    (temp/"steam_appid.txt").write_text("427520",encoding="ascii")
    command=[str(exe),"--config",str(config),"--mod-directory",str(mods),
             "--disable-migration-window",
             "--load-scenario","solar-boiler-v8-visual/pipe-capture"]
    return userdata,config,command

def shot_name(direction:str,ground:str,zoom:str) -> str:
    return f"{direction}-{ground}-{zoom}.png"

def validate_png(path: Path):
    with path.open("rb") as f:
        assert f.read(8)==PNG_SIGNATURE,(path,"bad PNG signature")
    with Image.open(path) as im:
        im.verify()
    with Image.open(path) as im:
        assert im.size == (1152,864), (path,im.size)
        assert im.mode in ("RGB","RGBA"),(path,im.mode)
        small=im.convert("RGB").resize((100,75))
        assert small.getcolors(256) is None,(path,"screenshot almost entirely blank")
    assert path.stat().st_size>15_000,(path,path.stat().st_size)

def crop_capture(path: Path, size=(480,360)) -> Image.Image:
    with Image.open(path) as image:
        pic=image.convert("RGB")
    w,h=pic.size
    # Centered screenshot, no artificial recoloring or geometry generation.
    crop=pic.crop((w//2-430,h//2-320,w//2+430,h//2+320))
    return crop.resize(size,Image.Resampling.LANCZOS)

def make_contact(out:Path,metadata:dict):
    font=ImageFont.load_default()
    bg=(25,29,33)
    def title(draw,x,y,label):
        draw.text((x,y),label,fill=(240,242,232),font=font)
    poster=Image.new("RGB",(2020,910),bg)
    draw=ImageDraw.Draw(poster)
    title(draw,20,12,"SOLAR BOILER V8 | ACTUAL FACTORIO 2.1 GRAPHICAL CLIENT | CONNECTED PIPES")
    title(draw,20,31,"TRUE in-game screenshots (4 rotations x natural/concrete) — not Blender projections")
    for i,d in enumerate(DIRECTIONS):
        x=18+502*i
        title(draw,x+4,55,d.upper())
        for j,g in enumerate(GROUNDS):
            y=80+400*j
            img=crop_capture(out/shot_name(d,g,"close"))
            poster.paste(img,(x,y))
            title(draw,x+5,y+366,g.upper()+"  |  close zoom 2.9  |  genuine engine PNG")
    title(draw,20,887,"Verification: PNG signatures, native engine log markers, 24 connected pipes; visual alignment for human review")
    poster.save(out/"factorio-client-pipes-all-four.png",optimize=True)
    # Exact natural view across four rotations against the approved V8 Blender
    # camera; do NOT calculate a false pixel-difference metric across contexts.
    side=Image.new("RGB",(2020,850),bg)
    d2=ImageDraw.Draw(side)
    title(d2,20,12,"GAME CLIENT V8 vs APPROVED BLENDER V8 | NOT THE SAME CAMERA PIXEL GRID")
    for i,d in enumerate(DIRECTIONS):
        x=18+502*i
        title(d2,x+4,38,d.upper()+" | REAL GAME (connected pipes)")
        game=crop_capture(out/shot_name(d,"natural","close"))
        side.paste(game,(x,62))
        title(d2,x+4,440,d.upper()+" | SOURCE BLENDER (transparent, original V8)")
        with Image.open(APPROVED/f"idle-d{SOURCE_IDS[i]:02d}.png") as base:
            rendered=base.convert("RGBA").resize((300,300),Image.Resampling.LANCZOS)
        dark=Image.new("RGBA",rendered.size,(38,43,47,255))
        dark.alpha_composite(rendered)
        side.paste(dark.convert("RGB"),(x+90,468))
    title(d2,20,818,"Client image and source image are separately labeled; judge pipes visually, not by a fabricated overlay.")
    side.save(out/"client-vs-approved-v8.png",optimize=True)

def capture(exe:Path,version:str,out:Path,temp:Path,max_seconds:int):
    userdata,config,cmd=stage_client_profile(exe,temp)
    target=userdata/"script-output"/"solar-boiler-v8"
    names=[shot_name(d,g,z) for g in GROUNDS for d in DIRECTIONS for z in ZOOMS]
    log=temp/"graphical-factorio.log"
    out.mkdir(parents=True,exist_ok=False)
    start=time.monotonic()
    print("GRAPHICAL_FACTORIO_BINARY",exe,flush=True)
    print("GRAPHICAL_FACTORIO_VERSION",version.splitlines()[0],flush=True)
    print("GUI_SCREENSHOT_SESSION_START",flush=True)
    with log.open("w",encoding="utf-8",errors="replace") as stream:
        process=subprocess.Popen(cmd,stdout=stream,stderr=subprocess.STDOUT,
                                 cwd=str(temp))
        try:
            while time.monotonic()-start<max_seconds:
                finished=all((target/name).is_file() and
                             (target/name).stat().st_size>15_000 for name in names)
                if finished:
                    time.sleep(2) # let the engine finish writing all queued frames
                    break
                # A full GUI binary can remain alive indefinitely in Session 0 while
                # DXGI initialization has already failed. Observe its actual log,
                # report the display failure promptly rather than sleeping 360s.
                stream.flush()
                current=log.read_text(encoding="utf-8",errors="replace")
                if any(m in current for m in (
                    "DXGI_ERROR_NOT_CURRENTLY_AVAILABLE",
                    "Failed to enumerate adapter output",
                    "Failed to get SDL_DXGIGetOutputInfo",
                )):
                    raise RuntimeError(
                        "INTERACTIVE_DESKTOP_REQUIRED: Factorio graphical renderer "
                        "cannot initialize a GPU display in this Windows session; "
                        "see captured native engine log. No screenshots generated.")
                rc=process.poll()
                if rc is not None:
                    early=log.read_text(encoding="utf-8",errors="replace")
                    if "Steam requires game restart" in early:
                        raise RuntimeError("Steam API redirected the test process despite the isolated development app-id; no screenshots")
                    raise RuntimeError(f"GUI client exited before 16 screenshots: exit={rc}; log tail: {early[-1800:]}")
                time.sleep(2)
            else:
                raise TimeoutError("Full Factorio graphical client did not produce all 16 "+
                                   f"screen captures in {max_seconds}s")
            engine_log=log.read_text(encoding="utf-8",errors="replace")
            assert "SOLAR_V8_GUI_WORLD_PASS" in engine_log, "No actual placed-entity log evidence"
            assert "SOLAR_V8_GUI_SCREENSHOT_QUEUE_COMPLETE count=16" in engine_log, (
                "Screenshot event did not complete")
            for name in names:
                path=target/name
                validate_png(path)
                shutil.copy2(path,out/name)
                assert digest(path)==digest(out/name)
            shutil.copy2(log,out/"factorio-gui-client.log")
        finally:
            if process.poll() is None:
                process.terminate() # only the isolated child launched by this script
                try: process.wait(timeout=12)
                except subprocess.TimeoutExpired:
                    process.kill();process.wait(timeout=5)
    screenshots={name:digest(out/name) for name in names}
    assert len(set(screenshots.values()))==len(names),(
        "GUI screenshots unexpectedly identical")
    data={"schema":"tanks.solar-v8.real-graphical-client-qa",
          "passed":True,"factorio_full_client":True,"factorio_headless":False,
          "client_executable":str(exe),"client_version":version.splitlines()[0],
          "target_prototype":"boiler/solar-boiler",
          "native_boilers":8,"native_connected_pipes":24,
          "directions":list(DIRECTIONS),"ground_tiles":list(GROUNDS),
          "zooms":{"normal":1.6,"close":2.9},
          "screen_capture_count":len(screenshots),"engine_log_marker":"SOLAR_V8_GUI_WORLD_PASS",
          "screenshots_sha256":screenshots,"visual_alignment_human_approved":False}
    make_contact(out,data)
    data["contact_sha256"]=digest(out/"factorio-client-pipes-all-four.png")
    data["comparison_sha256"]=digest(out/"client-vs-approved-v8.png")
    (out/"client-capture-qa.json").write_text(json.dumps(data,indent=2)+"\n",encoding="utf-8")
    print("SOLAR_V8_ACTUAL_GAME_CLIENT_SCREENSHOTS_PASS captures=16 boilers=8 pipes=24",
          flush=True)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",type=Path,required=True)
    parser.add_argument("--working",type=Path,required=True)
    parser.add_argument("--client")
    parser.add_argument("--max-seconds",type=int,default=360)
    a=parser.parse_args()
    out=a.output.resolve();temp=a.working.resolve()
    if out.exists():
        raise FileExistsError("Do not overwrite existing in-game screenshots: "+str(out))
    try:
        require_interactive_desktop()
        exe,version=find_client(a.client)
        capture(exe,version,out,temp,a.max_seconds)
    except Exception as err:
        out.mkdir(parents=True,exist_ok=True)
        log=temp/"graphical-factorio.log"
        detail={"passed":False,"reason":str(err),"graphical_client_required":True,
                "no_fake_screenshots":True,"traceback":traceback.format_exc()}
        (out/"client-capture-error.json").write_text(json.dumps(detail,indent=2)+"\n")
        if log.exists():shutil.copy2(log,out/"factorio-gui-client-failure.log")
        print("SOLAR_V8_GRAPHICAL_CLIENT_BLOCKED",str(err),flush=True)
        raise

if __name__=="__main__":main()
