#!/usr/bin/env python3
"""Factorio 2.1 hotfix: label existing growing-plot prototypes as Lumberyard.

Stable internal ID, saved entities, recipes and research remain intact.
No approved source images, sprite atlases or game behavior are modified.
"""
import argparse,hashlib,io,json,re,zipfile
from pathlib import Path
from PIL import Image

MOD="tanks_for_bob_fork"
BASE="1.8.99"
VERSION="1.8.100"
ICON="__tanks_for_bob_fork__/graphics/icons/lumberyard-v2b.png"
NAME="growing-plot"
DESC={
 "prototypes/entity/entities.lua":"A primitive boiler-driven lumberyard that turns whole logs into split timber.",
 "prototypes/item/item.lua":"A primitive steam-driven lumberyard with a belt-powered timber saw.",
 "prototypes/recipe/recipe.lua":"Build a primitive steam-powered lumberyard.",
 "prototypes/technology/technology.lua":"Unlocks the Lumberyard, a primitive steam-driven timber saw.",
 "recipe.lua":"Build a primitive steam-powered lumberyard."
}
LOCAL=("locale/en/base.cfg","locale/en/40k.cfg")
NAME_RE=re.compile(r'(?m)^([ \t]*)name\s*=\s*"growing-plot",')
def hash_bytes(data):return hashlib.sha256(data).hexdigest()

def proto(text,path):
    if path=="prototypes/entity/entities.lua":
        a=text.index("  --Growing plot")
        b=text.index("--quarry",a)
    else:
        matches=list(NAME_RE.finditer(text))
        if len(matches)!=1:raise RuntimeError("Unexpected prototype occurrences in "+path)
        a,b=matches[0].start(),matches[0].end()
    section=text[a:b]
    if len(NAME_RE.findall(section))!=1 or "localised_name" in section:
        raise RuntimeError("Wrong or previously renamed prototype: "+path)
    def inject(match):
        indent=match.group(1)
        return (match.group(0)+"\n"+indent+'localised_name = {"", "Lumberyard"},'
              +"\n"+indent+'localised_description = {"", '+json.dumps(DESC[path])+'},')
    section=NAME_RE.sub(inject,section,count=1)
    if path.endswith("/recipe/recipe.lua"):
        # Active Factorio recipe inherited its old output icon implicitly;
        # explicitly select the user's approved new 64px Lumberyard preview.
        section+='\n        icon = "'+ICON+'",\n        icon_size = 64,'
    elif path=="recipe.lua":
        # Dormant historical duplicate kept consistent, not loaded by data.lua.
        after=text[b:]
        before='icon = "__tanks_for_bob_fork__/graphics/icons/growing-plot.png"'
        if before not in after[:400]:raise RuntimeError("Old duplicate recipe icon missing")
        after=after.replace(before,'icon = "'+ICON+'"',1)
        return text[:a]+section+after
    elif path=="prototypes/entity/entities.lua":
        if ICON not in section:raise RuntimeError("Approved entity icon missing")
    else:
        if ICON not in text:raise RuntimeError("Approved item/technology icon missing")
    return text[:a]+section+text[b:]

def locale(raw,path):
    lines=raw.decode("utf-8").splitlines(keepends=True)
    found=0
    out=[]
    for line in lines:
        if not line.startswith("growing-plot="):
            out.append(line);continue
        found+=1
        current=line[len("growing-plot="):].rstrip("\n")
        if ("Growing Plot" in current or
            current.startswith("Rite of ") or
            current.startswith("Recovered Doctrine")):
            new="Lumberyard"
        elif current.startswith(("Builds ","Begins ","Forge-world annotation: builds ",
                                 "Forge-world annotation: begins ")):
            new="Unlocks the Lumberyard's primitive boiler-driven timber saw."
        else:
            new="A primitive lumberyard that saws whole logs into split timber."
        out.append("growing-plot="+new+("\n" if line.endswith("\n") else ""))
    if found!=8:raise RuntimeError("Expected 8 original names/descriptions in "+path)
    return "".join(out).encode("utf-8")

def build(base,out):
    if base.name!=f"{MOD}_{BASE}.zip":
        raise RuntimeError("Expected verified 1.8.99 Factorio mod ZIP")
    out.mkdir(parents=True,exist_ok=True)
    package=out/f"{MOD}_{VERSION}.zip"
    if package.exists():raise FileExistsError("Never overwrite an existing release")
    before_root=f"{MOD}_{BASE}/"
    after_root=f"{MOD}_{VERSION}/"
    changed={}
    art_hashes={}
    with zipfile.ZipFile(base) as original, zipfile.ZipFile(package,"w",zipfile.ZIP_DEFLATED,compresslevel=6) as result:
        if original.testzip() is not None:raise RuntimeError("Corrupt prior release")
        prior=set(original.namelist())
        icon_path=before_root+"graphics/icons/lumberyard-v2b.png"
        if icon_path not in prior:raise RuntimeError("Real Lumberyard preview missing")
        png=original.read(icon_path)
        with Image.open(io.BytesIO(png)) as image:
            if image.size!=(64,64) or image.mode!="RGBA":
                raise RuntimeError("Lumberyard inventory preview not RGBA 64px")
        for name in original.namelist():
            if not name.startswith(before_root):raise RuntimeError("Unexpected ZIP root")
            rel=name[len(before_root):]
            raw=original.read(name)
            if rel=="info.json":
                meta=json.loads(raw)
                if meta.get("name")!=MOD or meta.get("version")!=BASE or meta.get("factorio_version")!="2.1":
                    raise RuntimeError("Wrong base version or Factorio engine")
                meta["version"]=VERSION
                data=(json.dumps(meta,indent=2)+"\n").encode()
            elif rel in DESC:
                data=proto(raw.decode("utf-8"),rel).encode("utf-8")
            elif rel in LOCAL:
                data=locale(raw,rel)
            else:
                data=raw
            if data!=raw:changed[rel]={"old":hash_bytes(raw),"new":hash_bytes(data)}
            if rel.startswith(("graphics/icons/lumberyard-v2b","graphics/entity/lumberyard-v2b")):
                art_hashes[rel]=hash_bytes(raw)
            result.writestr(after_root+rel,data)
    expected=set(DESC)|set(LOCAL)|{"info.json"}
    if set(changed)!=expected:raise RuntimeError("Unexpected modification scope: "+repr(set(changed)^expected))
    with zipfile.ZipFile(package) as archive:
        if archive.testzip() is not None:raise RuntimeError("Bad full ZIP CRC")
        root=after_root
        if json.loads(archive.read(root+"info.json"))["version"]!=VERSION:
            raise RuntimeError("Wrong release metadata")
        if archive.read(root+"graphics/icons/lumberyard-v2b.png")!=png:
            raise RuntimeError("Accepted Lumberyard preview changed")
        for rel,hashvalue in art_hashes.items():
            if hash_bytes(archive.read(root+rel))!=hashvalue:
                raise RuntimeError("Approved artwork changed")
        for rel in DESC:
            content=archive.read(root+rel).decode()
            if path_has_name(content,rel) is False:
                raise RuntimeError("Lumberyard display label not present: "+rel)
        for rel in ("prototypes/entity/entities.lua","prototypes/item/item.lua",
                    "prototypes/recipe/recipe.lua","prototypes/technology/technology.lua"):
            source=archive.read(root+rel).decode()
            if 'name = "growing-plot"' not in source:raise RuntimeError("Stable ID unexpectedly renamed")
        entity=archive.read(root+"prototypes/entity/entities.lua").decode()
        part=entity[entity.index("  --Growing plot"):entity.index("--quarry")]
        if part.count("lumberyard-v2b-idle.png")!=4 or part.count("lumberyard-v2b-working.png")!=4:
            raise RuntimeError("Approved 4-direction animation missing")
        for item in ("pit-kiln-v6-burning-128.png","clay-pit-v4c-working.png","campfire-v12-burning.png"):
            if item not in entity:raise RuntimeError("Prior structures missing")
        if ICON not in archive.read(root+"prototypes/recipe/recipe.lua").decode():
            raise RuntimeError("Updated recipe preview missing")
    digest=hash_bytes(package.read_bytes())
    (out/(package.name+".sha256")).write_text(digest+"  "+package.name+"\n")
    receipt={"version":VERSION,"factorio_version":"2.1",
      "base_version":BASE,"package":package.name,"sha256":digest,
      "display_name":"Lumberyard","internal_id":"growing-plot",
      "approved_icon":"graphics/icons/lumberyard-v2b.png",
      "approved_icon_sha256":hash_bytes(png),
      "art_hashes":art_hashes,"changed_files":changed,
      "all_existing_machine_ids_preserved":True,
      "no_render_or_gameplay_changes":True,
      "runtime_tested":False}
    (out/"lumberyard-label-receipt.json").write_text(json.dumps(receipt,indent=2)+"\n")
    print("LUMBERYARD_DISPLAY_1_8_100_PACKAGE_PASS",digest,flush=True)
    return receipt

def path_has_name(source,rel):
    if rel=="prototypes/entity/entities.lua":
        source=source[source.index("  --Growing plot"):source.index("--quarry")]
    return 'localised_name = {"", "Lumberyard"}' in source

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--base",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    build(a.base.resolve(),a.output.resolve())
if __name__=="__main__":main()
