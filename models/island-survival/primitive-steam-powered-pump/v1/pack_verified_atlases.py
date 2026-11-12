#!/usr/bin/env python3
"""Non-destructive 4-direction 8FPS sprite packing of a VERIFIED native 1x2 pump.

This is a candidate-only production tool. It refuses unverified Blender output
and NEVER modifies Factorio entity prototypes, saves, install directories or
release artifacts. Pump prototype schema is distinct from assembling machines.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image

HERE=Path(__file__).resolve().parent
DIRS=("north","east","south","west")
SOURCE_MAP=(0,3,2,1)
SIZES=(64,128,256)
FRAMES=tuple(range(1,92,6))
EXPECTED=68
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def validate(source):
    contract=json.loads((HERE/"contract.json").read_text(encoding="utf-8"))
    manifest=json.loads((source/"build-report.json").read_text(encoding="utf-8"))
    qa=json.loads((source/"native-reopen-qa.json").read_text(encoding="utf-8"))
    assert manifest["schema"]=="tanks.primitive-steam-pump.v1.native-source"
    assert manifest["render_mode"]=="all" and manifest["render_count"]==EXPECTED
    assert len(manifest["renders"])==EXPECTED
    assert manifest["type"]==contract["entity_type"]=="pump"
    assert manifest["name"]==contract["entity_name"]=="primitive-steam-powered-pump"
    assert manifest["dimensions"]==contract["footprint_tiles"]==[1,2]
    assert tuple(manifest["frames"])==FRAMES
    assert tuple(manifest["directions"])==(0,90,180,270)
    assert qa["schema"]=="tanks.primitive-steam-pump.v1.native-reopen-qa"
    assert qa["passed"] is True and qa["actual_blender_frame_count"]==EXPECTED
    assert qa["native_sha256"]==manifest["native_sha256"]
    assert qa["full_bore_rigid_mesh_count"]==4 and qa["mating_vertices_each"]==256
    assert qa["native_positions"]==[[0,-.75],[0,.75]]
    assert qa["loop_97_matches_1"] and qa["single_45_degree_ortho"]
    assert not qa["game_integrated"] and not qa["owner_visual_approved"]
    assert sha(source/"pump-v1.blend")==manifest["native_sha256"]
    assert manifest["fixture_sha256"]==contract["fixture"]["sha256"]
    assert manifest["pbr_donor_sha256"]==contract["fmpl_pbr_donor"]["sha256"]
    frames={}
    for row in manifest["renders"]:
        d=int(row["direction"])
        k=int(row["index"])
        state=row["state"]
        assert 0<=d<4 and state in ("idle","working")
        assert (state=="idle" and k==-1) or (state=="working" and 0<=k<16)
        assert row["frame"]==(0 if state=="idle" else FRAMES[k])
        ident=(state,d,k)
        assert ident not in frames, ("duplicate render",ident)
        p=source/row["file"]
        assert p.is_file() and sha(p)==row["sha256"],("missing/altered frame",p)
        with Image.open(p) as img:
            assert img.mode=="RGBA" and img.size==(256,256)
            bounds=img.getchannel("A").getbbox()
            assert bounds and bounds[0]>0 and bounds[1]>0 and bounds[2]<256 and bounds[3]<256,(p,bounds)
        frames[ident]=p
    assert len(frames)==EXPECTED
    for d in range(4):
        assert ("idle",d,-1) in frames
        for k in range(16):assert ("working",d,k) in frames
    return manifest,contract,qa,frames

def build(source,out):
    if out.exists():raise FileExistsError("Refuse to overwrite atlas work: "+str(out))
    manifest,contract,qa,frames=validate(source)
    out.mkdir(parents=True,exist_ok=False)
    files={}
    for size in SIZES:
        for state in ("idle","working"):
            cols,rows=(4,1) if state=="idle" else (8,8)
            atlas=Image.new("RGBA",(cols*size,rows*size),(0,0,0,0))
            for d in range(4):
                for k in ((-1,) if state=="idle" else range(16)):
                    with Image.open(frames[state,d,k]) as original:
                        cell=original.copy() if size==256 else original.resize(
                            (size,size),Image.Resampling.LANCZOS)
                    x=(d if state=="idle" else k%8)*size
                    y=(0 if state=="idle" else d*2+k//8)*size
                    atlas.paste(cell,(x,y))
                    assert atlas.crop((x,y,x+size,y+size)).tobytes()==cell.tobytes()
            p=out/(f"{state}-{size}.png")
            atlas.save(p,optimize=True)
            with Image.open(p) as check:
                check.verify()
            with Image.open(p) as check:
                assert check.mode=="RGBA" and check.size==(cols*size,rows*size)
            files[p.name]={"sha256":sha(p),"px":[cols*size,rows*size],"cell_px":size}
    # Candidate orientation/scale values are diagnostics until an actual 2.1
    # pump graphics schema test; the Factorio runtime will NOT load this file.
    cam=contract["capture"]
    scale=32*cam["ortho_scale"]/cam["resolution"][0]
    shift=-(cam["camera"][1]+cam["camera"][2])/(2**.5)
    candidate={
        "schema":"tanks.primitive-steam-pump.v1.candidate-only-atlas",
        "passed":True,
        "factorio_prototype":{"type":"pump","name":"primitive-steam-powered-pump"},
        "footprint":[1,2],"source_native_sha256":manifest["native_sha256"],
        "native_connections":contract["native_connections"],
        "factorio_facing_order":list(DIRS),
        "blender_orientation_index_per_facing":list(SOURCE_MAP),
        "animated_frames_per_direction":16,"fps":8,
        "proposed_not_verified_scale256":scale,
        "proposed_not_verified_shift":[0,shift],
        "atlas_files":files,
        "source_frame_count_verified":len(frames),
        "factorio_pump_schema_verified":False,
        "game_integrated":False,
        "owner_visual_approved":False
    }
    (out/"candidate-atlas-qa.json").write_text(
        json.dumps(candidate,indent=2)+"\n",encoding="utf-8")
    print("TANKS_PUMP_VERIFIED_68_FRAME_ATLAS_CANDIDATE_PASS",
          len(files),"output atlases; native pump prototype untouched",flush=True)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--source",type=Path,required=True)
    p.add_argument("--out",type=Path,required=True)
    args=p.parse_args()
    build(args.source.resolve(),args.out.resolve())
if __name__=="__main__":main()
