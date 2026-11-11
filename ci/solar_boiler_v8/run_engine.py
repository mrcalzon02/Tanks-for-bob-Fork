#!/usr/bin/env python3
"""Pinned official Factorio 2.1.24 no-video runtime test of all Solar V8 ports."""
from __future__ import annotations
import argparse,json,shutil,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
MOD=ROOT/"tanks_for_bob_fork_1.8.102"
OFFICIAL=("base","elevated-rails","quality","recycler","space-age")
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--binary",type=Path,required=True)
    p.add_argument("--out",type=Path,required=True)
    a=p.parse_args()
    binary=a.binary.resolve();out=a.out.resolve()
    version=subprocess.check_output([str(binary),"--version"],text=True)
    assert "2.1.24" in version,version
    out.mkdir(parents=True,exist_ok=True)
    mods=out/"mods";mods.mkdir(exist_ok=True)
    shutil.copytree(MOD,mods/"tanks_for_bob_fork_1.8.102")
    addon=mods/"solar-boiler-v8-ci_0.0.1"
    addon.mkdir()
    shutil.copy2(HERE/"runtime-info.json",addon/"info.json")
    shutil.copy2(HERE/"runtime-control.lua",addon/"control.lua")
    scenario=addon/"scenarios/pipe-check";scenario.mkdir(parents=True)
    (scenario/"control.lua").write_text("-- Runtime test logic runs in the diagnostic add-on control.lua.\n")
    (scenario/"description.json").write_text('{"name":"Solar Boiler V8 4-way physical pipe fit"}\n')
    (mods/"mod-list.json").write_text(json.dumps({"mods":[{"name":n,"enabled":True}
        for n in OFFICIAL]+[{"name":"tanks_for_bob_fork","enabled":True},
        {"name":"solar-boiler-v8-ci","enabled":True}]},indent=2)+"\n")
    config=out/"config.ini"
    runtime=out/"runtime";runtime.mkdir()
    config.write_text("[path]\nread-data="+str(binary.parents[2]/"data")+
                      "\nwrite-data="+str(runtime)+"\n")
    cmd=[str(binary),"--config",str(config),"--mod-directory",str(mods),
         "--test-scenario","solar-boiler-v8-ci/pipe-check",
         "--test-arg","pipes","--test-ticks","90"]
    logfile=out/"factorio-pipe-smoke.log"
    with logfile.open("w") as f:
        result=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT,timeout=200)
    log=logfile.read_text(errors="replace")
    marker="SOLAR_BOILER_V8_NATIVE_ENGINE_PIPE_PASS"
    passed=result.returncode==0 and marker in log
    receipt={"engine":version.strip(),"exit_code":result.returncode,
             "marker_present":marker in log,"passed":passed,
             "validated_directions":4,"expected_connections":12,
             "visual_client_screenshot_tested":False}
    (out/"engine-qa.json").write_text(json.dumps(receipt,indent=2)+"\n")
    print("SOLAR_BOILER_V8_NATIVE_ENGINE_PASS" if passed else
        "SOLAR_BOILER_V8_NATIVE_ENGINE_FAIL",receipt,flush=True)
    if not passed:
        print(log[-8000:],flush=True)
        raise SystemExit(1)
if __name__=="__main__":main()
