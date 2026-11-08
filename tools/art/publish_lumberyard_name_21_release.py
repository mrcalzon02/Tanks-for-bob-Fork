#!/usr/bin/env python3
"""Publish 1.8.100 Lumberyard display/icon correction after official engine test."""
import hashlib,json,os,sys,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/"ci"))
import publish_mod_portal as portal
from build_lumberyard_name_21_release import MOD,VERSION,BASE
def sha(blob):return hashlib.sha256(blob).hexdigest()
def main():
    if len(sys.argv)!=2:raise SystemExit("Usage: publish_lumberyard_name_21_release.py VERIFIED_DIR")
    root=Path(sys.argv[1]).resolve()
    package=root/f"{MOD}_{VERSION}.zip"
    receipt_path=root/"lumberyard-label-receipt.json"
    digest_path=root/(package.name+".sha256")
    ev=[root/n for n in ("engine-version.txt","engine-create.log","engine-benchmark.log")]
    if any(not p.is_file() for p in [package,receipt_path,digest_path,*ev]):
        raise RuntimeError("Missing release or official Factorio 2.1 load evidence")
    if "2.1.23" not in ev[0].read_text(errors="replace"):
        raise RuntimeError("Incorrect official Factorio runtime")
    if "Loading mod tanks_for_bob_fork" not in ev[1].read_text(errors="replace"):
        raise RuntimeError("Mod did not load in actual Factorio")
    bench=ev[2].read_text(errors="replace")
    if not bench.strip() or ("Performed " not in bench and "ticks" not in bench):
        raise RuntimeError("No completed 300-tick test")
    receipt=json.loads(receipt_path.read_text())
    digest=sha(package.read_bytes())
    if digest!=receipt.get("sha256") or digest!=digest_path.read_text().split()[0]:
        raise RuntimeError("Package SHA mismatch")
    allowed={"info.json","prototypes/entity/entities.lua","prototypes/item/item.lua",
       "prototypes/recipe/recipe.lua","prototypes/technology/technology.lua",
       "recipe.lua","locale/en/base.cfg","locale/en/40k.cfg"}
    if (receipt.get("version")!=VERSION or receipt.get("base_version")!=BASE or
        receipt.get("internal_id")!="growing-plot" or receipt.get("display_name")!="Lumberyard" or
        not receipt.get("all_existing_machine_ids_preserved") or
        set(receipt["changed_files"])!=allowed):
        raise RuntimeError("Unapproved release scope")
    with zipfile.ZipFile(package) as z:
        if z.testzip() is not None:raise RuntimeError("Corrupt ZIP")
        root_prefix=f"{MOD}_{VERSION}/"
        meta=json.loads(z.read(root_prefix+"info.json"))
        if meta.get("name")!=MOD or meta.get("version")!=VERSION or meta.get("factorio_version")!="2.1":
            raise RuntimeError("Incorrect version metadata")
        for rel,expected in receipt["art_hashes"].items():
            if sha(z.read(root_prefix+rel))!=expected:
                raise RuntimeError("Previously approved Lumberyard art changed")
        for rel in ("prototypes/entity/entities.lua","prototypes/item/item.lua",
                    "prototypes/recipe/recipe.lua","prototypes/technology/technology.lua"):
            data=z.read(root_prefix+rel).decode()
            if 'localised_name = {"", "Lumberyard"}' not in data:
                raise RuntimeError("Missing user-facing name: "+rel)
    key=os.environ.get("FACTORIO_MOD_UPLOAD_KEY","").strip()
    if not key:raise RuntimeError("Mod Portal API key unavailable")
    print("LUMBERYARD_1_8_100_OFFICIAL_ENGINE_AND_PACKAGE_PASS",digest,flush=True)
    portal.upload(package,VERSION,key)
    published=VERSION in portal.portal_versions()
    status="publicly_indexed" if published else "upload_accepted_index_pending"
    (root/"mod-portal-publication.json").write_text(json.dumps({
        "mod":MOD,"version":VERSION,"sha256":digest,"status":status,
        "url":"https://mods.factorio.com/mod/"+MOD},indent=2)+"\n")
    print("LUMBERYARD_DISPLAY_1_8_100_PORTAL_"+status.upper(),flush=True)
if __name__=="__main__":main()
