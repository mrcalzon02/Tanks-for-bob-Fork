#!/usr/bin/env python3
"""Native Factorio 2.1.24 player and saved-game progression integration fixture.

Runs a separate diagnostic addon. No production handlers or prototypes are
replaced. Target machinery receives seeded resources; this is not a playthrough.
Supply an exact published 1.8.100 ZIP for the optional real upgrade-save check.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import zipfile

ROOT=Path(__file__).resolve().parents[1]
ADDON="tanks-progression-runtime"
OFFICIAL=("base","elevated-rails","quality","recycler","space-age")

def digest_tree(path: Path) -> str:
    result=hashlib.sha256()
    for file in sorted(path.rglob("*")):
        if file.is_file():
            result.update(file.relative_to(path).as_posix().encode()+b"\0")
            result.update(hashlib.sha256(file.read_bytes()).digest())
    return result.hexdigest()

def main() -> int:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--binary",type=Path,required=True)
    p.add_argument("--source",type=Path,required=True,help="Current mod directory or exact release ZIP")
    p.add_argument("--output",type=Path,required=True)
    p.add_argument("--legacy-package",type=Path)
    p.add_argument("--profile",choices=["space-age","base"],default="space-age")
    a=p.parse_args()
    binary,source,out=a.binary.resolve(),a.source.resolve(),a.output.resolve()
    source_is_zip=source.is_file()
    if source_is_zip:
        with zipfile.ZipFile(source) as archive:
            metadata=[name for name in archive.namelist() if name.endswith("/info.json") and name.count("/")==1]
            if len(metadata)!=1: raise ValueError("Expected one mod root and info.json in current ZIP")
            info=json.loads(archive.read(metadata[0]))
    else:
        info=json.loads((source/"info.json").read_text())
    if info["name"]!="tanks_for_bob_fork" or info["factorio_version"]!="2.1":
        raise ValueError("Expected Tanks for Bob mod targeting Factorio 2.1")
    version=subprocess.check_output([str(binary),"--version"],text=True)
    help_text=subprocess.check_output([str(binary),"--help"],text=True)
    if "--test-scenario" not in help_text or "--test-save" not in help_text:
        raise ValueError("Native player test mode requires Factorio 2.1.24 or later")
    out.mkdir(parents=True,exist_ok=True)
    (out/"engine-version.txt").write_text(version)
    source_snapshot=out/("source-snapshot.zip" if source_is_zip else "source-snapshot")
    if source_snapshot.is_dir(): shutil.rmtree(source_snapshot)
    elif source_snapshot.exists(): source_snapshot.unlink()
    if source_is_zip:
        shutil.copy2(source,source_snapshot)
        source_hash=hashlib.sha256(source_snapshot.read_bytes()).hexdigest()
    else:
        shutil.copytree(source,source_snapshot)
        source_hash=digest_tree(source_snapshot)
    receipt={"engine":version.strip(),"source":str(source),"source_fingerprint_sha256":source_hash,"source_form":"archive" if source_is_zip else "directory","source_version":info["version"],
             "profile":a.profile,"commands":[],"reports":{},"scope":"Native player event integration plus seeded machine and historical-save states; not a complete playthrough."}
    if a.legacy_package:
        receipt["legacy_package_sha256"]=hashlib.sha256(a.legacy_package.read_bytes()).hexdigest()
    def stage(label: str,legacy: bool=False):
        folder=out/label
        mods=folder/"mods"
        if mods.exists(): shutil.rmtree(mods)
        mods.mkdir(parents=True)
        runtime=folder/"runtime"
        runtime.mkdir(parents=True,exist_ok=True)
        if legacy:
            assert a.legacy_package
            shutil.copy2(a.legacy_package,mods/a.legacy_package.name)
        elif source_is_zip:
            shutil.copy2(source_snapshot,mods/(info["name"]+"_"+info["version"]+".zip"))
        else:
            shutil.copytree(source_snapshot,mods/(info["name"]+"_"+info["version"]))
        addon=mods/(ADDON+"_0.0.1")
        addon.mkdir()
        (addon/"info.json").write_text(json.dumps({"name":ADDON,"version":"0.0.1","title":"Progression integration fixture","author":"Tanks for Bob CI","factorio_version":"2.1","dependencies":["base >= 2.1.24","tanks_for_bob_fork"]},indent=2)+"\n")
        shutil.copy2(ROOT/"ci/progression_runtime_fixture.lua",addon/"control.lua")
        (addon/"fixture_config.lua").write_text("return {target_version="+json.dumps(info["version"])+",fixture_mode="+json.dumps("seed-legacy" if legacy else "fresh")+"}\n")
        scenario=addon/"scenarios/progression"
        scenario.mkdir(parents=True)
        (scenario/"control.lua").write_text('''-- The old map stores a real character inventory. Native test mode supplies
-- a player on load; attach that saved character before mod player-created
-- handlers run. This tests saved inventory + joining, not an offline player.
script.on_event(defines.events.on_player_created,function(event)
  local force=game.forces.legacy_existing_wood
  if not force then return end
  local player=game.get_player(event.player_index)
  local character=game.surfaces[1].find_entities_filtered{name="character",force=force}[1]
  if character then
    local previous=player.character
    player.force=force
    player.set_controller{type=defines.controllers.character,character=character}
    if previous and previous.valid and previous~=character then previous.destroy() end
  end
end)
''')
        (scenario/"description.json").write_text(json.dumps({"name":"Progression runtime fixture"})+"\n")
        mods_list=[{"name":name,"enabled":name=="base" or a.profile=="space-age"} for name in OFFICIAL]
        mods_list += [{"name":"tanks_for_bob_fork","enabled":True},{"name":ADDON,"enabled":True}]
        (mods/"mod-list.json").write_text(json.dumps({"mods":mods_list},indent=2)+"\n")
        config=folder/"config.ini"
        config.write_text("[path]\nread-data="+str(binary.parents[2]/"data")+"\nwrite-data="+str(runtime)+"\n")
        return folder,runtime,[str(binary),"--config",str(config),"--mod-directory",str(mods)]
    def run(label: str,mode: str,command: list[str],folder: Path,runtime: Path):
        logfile=folder/(mode+".log")
        reportfile=runtime/"script-output/progression-runtime"/(mode+".json")
        reportfile.unlink(missing_ok=True)
        print("TANKS-CI PROGRESSION_RUNTIME RUN",mode,flush=True)
        with logfile.open("w") as log:
            result=subprocess.run(command,stdout=log,stderr=subprocess.STDOUT,timeout=180)
        receipt["commands"].append({"mode":mode,"command":command,"exit_code":result.returncode,"log":str(logfile)})
        report=json.loads(reportfile.read_text()) if reportfile.exists() else {}
        receipt["reports"][mode]=report
        (out/"receipt.json").write_text(json.dumps(receipt,indent=2)+"\n")
        if result.returncode or not report.get("complete") or not report.get("checks") or any(not c["passed"] for c in report["checks"]):
            print(logfile.read_text(errors="replace")[-16000:])
            raise RuntimeError("Native progression fixture failed or never completed: "+mode)
    folder,runtime,common=stage("fresh")
    run("fresh","fresh",common+["--test-scenario",ADDON+"/progression","--test-arg","fresh","--test-ticks","15000"],folder,runtime)
    if a.legacy_package:
        folder,runtime,common=stage("legacy",True)
        save=runtime/"saves"/ADDON/"progression.zip"
        save.unlink(missing_ok=True)
        run("legacy","seed-legacy",common+["--scenario2map",ADDON+"/progression"],folder,runtime)
        if not save.exists(): raise RuntimeError("Legacy engine did not write the required historical save")
        receipt["legacy_save_sha256"]=hashlib.sha256(save.read_bytes()).hexdigest()
        folder,runtime,common=stage("migration")
        run("migration","migration",common+["--test-save",str(save),"--test-arg","migration","--test-ticks","120"],folder,runtime)
    receipt["passed"]=True
    (out/"receipt.json").write_text(json.dumps(receipt,indent=2)+"\n")
    print("TANKS-CI PROGRESSION_RUNTIME_PASS fresh=yes migration="+("yes" if a.legacy_package else "not-requested"))
    return 0

if __name__=="__main__":
    sys.exit(main())
