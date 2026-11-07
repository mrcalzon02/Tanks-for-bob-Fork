#!/usr/bin/env python3
"""Promote approved Pit Kiln V6 to full Tanks for Bob 1.8.98 / Factorio 2.1 ZIP.

Uses proven full 1.8.97 release. Copies published V6 atlas bytes without
rerendering. Only kiln entity graphics/icon/rotation are modified.
"""
import argparse,hashlib,json,tempfile,zipfile,shutil
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[2]
MOD="tanks_for_bob_fork"
BASE_VERSION="1.8.97"
NEW_VERSION="1.8.98"
PREFIX="pit-kiln-v6"
ART=ROOT/"models/island-survival/pit-kiln/production-v6"

def sha(blob):return hashlib.sha256(blob).hexdigest()
def guard_replace(s,old,new):
    if s.count(old)!=1:raise RuntimeError("Ambiguous prototype anchor: "+old)
    return s.replace(old,new,1)
def icon_patch(full):
    at=full.index('name = "pit-kiln"')
    a=full.rfind("{",0,at);b=full.index("}",at)+1
    return full[:a]+guard_replace(full[a:b],"graphics/icons/pit-kiln.png",
        "graphics/icons/"+PREFIX+"-icon-64.png")+full[b:]
def kiln_section(full,lua):
    start=full.index("--pit-kiln")
    end=full.index("--workbench",start)
    sec=full[start:end]
    if sec.count('name = "pit-kiln"')!=1 or sec.count("pit-kiln-w.png")!=1:
        raise RuntimeError("Wrong kiln section or already replaced")
    a=sec.index("    graphics_set =")
    b=sec.index("    crafting_categories =",a)
    # Full animated entity frames, never old base + a second full fire overlay.
    gfx=lua[lua.index("graphics_set ="):].strip()
    gfx=guard_replace(gfx,"graphics_set = {",
        "graphics_set = {\n    working_visualisations = {{ light = {intensity = 0.4, size = 6} }},")
    sec=sec[:a]+"    -- Approved Pit Kiln V6, full 4-way idle/working alternatives.\n    "+gfx+",\n"+sec[b:]
    sec=guard_replace(sec,"graphics/icons/pit-kiln.png","graphics/icons/"+PREFIX+"-icon-64.png")
    sec=guard_replace(sec,"collision_box = {{-1.2, -1.2}, {1.2, 1.2}}",
                      "collision_box = {{-1.2, -1.1}, {1.2, 1.1}}")
    sec=guard_replace(sec,"    crafting_speed = 0.30,",
                      "    crafting_speed = 0.30,\n    match_animation_speed_to_activity = false,")
    if sec.count(PREFIX+"-burning-128.png")!=4 or sec.count(PREFIX+"-idle-128.png")!=4:
        raise RuntimeError("Four directions missing")
    if "pit-kiln-w.png" in sec:raise RuntimeError("Old duplicate working overlay retained")
    return full[:start]+sec+full[end:]
def source_files():
    qa=json.loads((ART/"production-qa.json").read_text())
    if (not qa.get("passed") or qa.get("revision")!="v6" or
        qa.get("source_rgba_frames")!=68 or
        not qa.get("inward_pitch_not_yaw_verified") or
        not qa.get("whole_tray_motion_verified") or
        qa.get("model_rotations")!=[0,90,180,270] or qa.get("fps")!=8):
        raise RuntimeError("Approved V6 source QA rejected")
    expected={f"{PREFIX}-{state}-{size}.png" for state in ("idle","burning") for size in (64,128,256)}
    expected.add(PREFIX+"-icon-64.png")
    if set(qa["files"])!=expected:raise RuntimeError("Missing or extra sprite files")
    for name in expected:
        data=(ART/name).read_bytes()
        if sha(data)!=qa["files"][name]["sha256"]:
            raise RuntimeError("Published V6 sprite has changed: "+name)
        with Image.open(ART/name) as im:
            if im.mode!="RGBA" or list(im.size)!=qa["files"][name]["dimensions"]:
                raise RuntimeError("Source atlas type/dimensions changed")
    lua=(ART/"prototype-ready.lua").read_text()
    if lua.count(PREFIX+"-burning-128.png")!=4 or lua.count(PREFIX+"-idle-128.png")!=4:
        raise RuntimeError("Prototype-ready four-direction Lua incomplete")
    return qa,lua,expected
def build(base,out):
    qa,lua,assets=source_files()
    if base.name!=MOD+"_"+BASE_VERSION+".zip":
        raise RuntimeError("Requires prior official 1.8.97 full mod ZIP")
    out.mkdir(parents=True,exist_ok=True)
    zip_path=out/(MOD+"_"+NEW_VERSION+".zip")
    if zip_path.exists():raise FileExistsError("Release exists, no overwrite")
    with tempfile.TemporaryDirectory() as temp:
        temp=Path(temp)
        with zipfile.ZipFile(base) as z:
            if z.testzip() is not None:raise RuntimeError("Corrupt 1.8.97 base")
            for name in z.namelist():
                if not name.startswith(MOD+"_"+BASE_VERSION+"/") or not (temp/name).resolve().is_relative_to(temp.resolve()):
                    raise RuntimeError("Unexpected archive path: "+name)
            z.extractall(temp)
        old=temp/(MOD+"_"+BASE_VERSION)
        mod=temp/(MOD+"_"+NEW_VERSION)
        old.rename(mod)
        info_file=mod/"info.json";info=json.loads(info_file.read_text())
        if info.get("name")!=MOD or info.get("version")!=BASE_VERSION or info.get("factorio_version")!="2.1":
            raise RuntimeError("Previous release identity/version differs")
        info["version"]=NEW_VERSION
        info_file.write_text(json.dumps(info,indent=2)+"\n")
        hashes={}
        for name in sorted(assets):
            relative=("graphics/icons/" if "icon" in name else "graphics/entity/")+name
            target=mod/relative
            if target.exists():raise RuntimeError("Refusing sprite overwrite: "+name)
            target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(ART/name,target)
            hashes[relative]=sha(target.read_bytes())
        entity=mod/"prototypes/entity/entities.lua"
        entity.write_text(kiln_section(entity.read_text(),lua))
        for path in ("prototypes/item/item.lua","prototypes/technology/technology.lua"):
            file=mod/path;file.write_text(icon_patch(file.read_text()))
        with zipfile.ZipFile(zip_path,"w",zipfile.ZIP_DEFLATED,compresslevel=6) as z:
            for f in sorted(mod.rglob("*")):
                if f.is_file():z.write(f,f.relative_to(temp).as_posix())
    with zipfile.ZipFile(zip_path) as z:
        if z.testzip() is not None:raise RuntimeError("New ZIP CRC failed")
        root=MOD+"_"+NEW_VERSION+"/"
        info=json.loads(z.read(root+"info.json"))
        if info.get("version")!=NEW_VERSION or info.get("factorio_version")!="2.1":
            raise RuntimeError("Wrong release metadata")
        for rel,h in hashes.items():
            if sha(z.read(root+rel))!=h:raise RuntimeError("Art corruption "+rel)
        lua=z.read(root+"prototypes/entity/entities.lua").decode()
        sec=lua[lua.index("--pit-kiln"):lua.index("--workbench",lua.index("--pit-kiln"))]
        if (sec.count(PREFIX+"-burning-128.png")!=4 or sec.count(PREFIX+"-idle-128.png")!=4 or
            "pit-kiln-w.png" in sec or
            "match_animation_speed_to_activity = false" not in sec or
            "collision_box = {{-1.2, -1.1}, {1.2, 1.1}}" not in sec or
            "},\n    crafting_categories" not in sec):
            raise RuntimeError("Full kiln prototype integration failed")
        for path in ("prototypes/item/item.lua","prototypes/technology/technology.lua"):
            s=z.read(root+path).decode();at=s.index('name = "pit-kiln"')
            if PREFIX+"-icon-64.png" not in s[at:at+350]:raise RuntimeError("Icon not integrated: "+path)
        if "clay-pit-v4c-working.png" not in lua or "campfire-v12-burning.png" not in lua:
            raise RuntimeError("Previously accepted assets missing")
        count=len(z.namelist())
    digest=sha(zip_path.read_bytes())
    (out/(zip_path.name+".sha256")).write_text(digest+"  "+zip_path.name+"\n")
    receipt={"version":NEW_VERSION,"factorio_version":"2.1","package":zip_path.name,
      "sha256":digest,"file_count":count,"approved_asset":"Pit Kiln V6",
      "source_revision":"v6-final-inward-lateral-slide-with-forward-pitch",
      "source_master_sha256":qa["source_master_sha256"],
      "source_frames":68,"frames_per_direction":16,
      "directions":["north","east","south","west"],
      "new_art_hashes":hashes,"campfire_and_clay_pit_preserved":True,
      "factorio_engine_tested":False}
    (out/"pit-kiln-19898-receipt.json").write_text(json.dumps(receipt,indent=2)+"\n")
    print("PIT_KILN_V6_FACTORIO_21_BUILD_OK",json.dumps(receipt,sort_keys=True),flush=True)
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--base",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    build(a.base.resolve(),a.output.resolve())
if __name__=="__main__":main()
