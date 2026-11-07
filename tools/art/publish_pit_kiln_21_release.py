#!/usr/bin/env python3
"""Upload only fully engine-tested Pit Kiln V6 version 1.8.98."""
import hashlib,json,os,sys,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/"ci"))
import publish_mod_portal as portal
from build_pit_kiln_21_release import MOD,NEW_VERSION,PREFIX
def sha(data):return hashlib.sha256(data).hexdigest()
def main():
    if len(sys.argv)!=2:raise SystemExit("Usage: publish_pit_kiln_21_release.py OUTPUT")
    out=Path(sys.argv[1]).resolve()
    zip_file=out/(MOD+"_"+NEW_VERSION+".zip")
    manifest=out/"pit-kiln-19898-receipt.json"
    check=out/(zip_file.name+".sha256")
    logs=[out/x for x in ("engine-version.txt","engine-create.log","engine-benchmark.log")]
    if any(not p.is_file() for p in (zip_file,manifest,check,*logs)):
        raise RuntimeError("Release or official engine logs missing")
    if "2.1.23" not in logs[0].read_text():raise RuntimeError("Wrong game engine")
    if "Loading mod tanks_for_bob_fork" not in logs[1].read_text():
        raise RuntimeError("Mod did not load")
    bench=logs[2].read_text()
    if "Performed " not in bench and "ticks" not in bench:
        raise RuntimeError("No Factorio runtime benchmark evidence")
    receipt=json.loads(manifest.read_text())
    hashvalue=sha(zip_file.read_bytes())
    if receipt.get("version")!=NEW_VERSION or receipt.get("source_revision")!="v6-final-inward-lateral-slide-with-forward-pitch":
        raise RuntimeError("Unapproved source")
    if hashvalue!=receipt["sha256"] or hashvalue!=check.read_text().split()[0]:
        raise RuntimeError("Release SHA differs")
    if not receipt.get("campfire_and_clay_pit_preserved") or len(receipt["new_art_hashes"])!=7:
        raise RuntimeError("Missing preserved content or approved art")
    with zipfile.ZipFile(zip_file) as z:
        if z.testzip() is not None:raise RuntimeError("Corrupt ZIP")
        root=MOD+"_"+NEW_VERSION+"/"
        info=json.loads(z.read(root+"info.json"))
        if info.get("name")!=MOD or info.get("version")!=NEW_VERSION or info.get("factorio_version")!="2.1":
            raise RuntimeError("Wrong release identity")
        for path,expected in receipt["new_art_hashes"].items():
            if sha(z.read(root+path))!=expected:raise RuntimeError("Approved PNG mutated")
        lua=z.read(root+"prototypes/entity/entities.lua").decode()
        kiln=lua[lua.index("--pit-kiln"):lua.index("--workbench",lua.index("--pit-kiln"))]
        if kiln.count(PREFIX+"-idle-128.png")!=4 or kiln.count(PREFIX+"-burning-128.png")!=4:
            raise RuntimeError("Prototype not wired to correct art")
    secret=os.getenv("FACTORIO_MOD_UPLOAD_KEY","").strip()
    if not secret:raise RuntimeError("Portal upload secret missing")
    print("PIT_KILN_V6_RELEASE_GATES_PASSED",hashvalue,flush=True)
    portal.upload(zip_file,NEW_VERSION,secret)
    public=NEW_VERSION in portal.portal_versions()
    status="publicly_indexed" if public else "accepted_index_pending"
    (out/"mod-portal-publication.json").write_text(json.dumps({
        "mod":MOD,"version":NEW_VERSION,"factorio_version":"2.1",
        "sha256":hashvalue,"status":status,
        "url":"https://mods.factorio.com/mod/"+MOD},indent=2)+"\n")
    print("PIT_KILN_V6_PORTAL_"+status.upper(),flush=True)
if __name__=="__main__":main()
