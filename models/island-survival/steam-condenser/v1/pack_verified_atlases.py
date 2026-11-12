#!/usr/bin/env python3
"""Package only VERIFIED genuine Blender Steam Condenser V1 frames as candidate atlases.

Does NOT render anything, change active game prototypes or publish a release.
The native source has to be independently reopened and all 68 source images
must agree with their individually recorded SHA-256 before packing begins.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
from pathlib import Path
from PIL import Image

HERE = Path(__file__).resolve().parent
DIRS = ("north", "east", "south", "west")
BLENDER_SOURCE_FOR_FACTORIO = (0, 3, 2, 1)
SIZES = (64, 128, 256)
FPS = 8

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def checked_sources(source):
    report=json.loads((source/"build-report.json").read_text(encoding="utf-8"))
    qa=json.loads((source/"native-reopen-qa.json").read_text(encoding="utf-8"))
    contract=json.loads((HERE/"contract.json").read_text(encoding="utf-8"))
    assert report["schema"]=="tanks.steam-condenser.v1.native-proof"
    assert qa["passed"] is True and qa["native_sha256"]==report["native_sha256"]
    assert report["render_mode"]=="all" and report["render_count"]==68
    assert len(report["renders"])==68 and qa["actual_render_count"]==68
    assert qa["full_bore_port_count"]==2 and qa["fixed_fluid_cells"]==[[0,-1],[0,1]]
    assert report["footprint"]==contract["footprint_tiles"]==[3,3]
    assert report["game_integrated"] is False and report["owner_visual_approved"] is False
    assert sha(source/"steam-condenser-v1.blend")==report["native_sha256"]
    assert sha(HERE/"contract.json") and contract["capture"]["fps"]==FPS
    cam=contract["capture"]
    assert cam["camera_ortho_scale"]==5.2 and cam["fixed_camera"]==[0,-6,6.93]
    assert cam["camera_rotation_deg"]==[45,0,0] and cam["resolution"]==[256,256]
    indexed={}
    for row in report["renders"]:
        direction=int(row["direction"])
        state=row["state"]
        index=int(row["index"])
        assert 0<=direction<4 and state in ("idle","working")
        assert (state=="idle" and index==-1) or (state=="working" and 0<=index<16)
        key=(state,direction,index)
        assert key not in indexed, ("duplicate source",key)
        f=source/row["file"]
        assert f.is_file() and sha(f)==row["sha256"], ("changed Blender frame",f)
        with Image.open(f) as im:
            assert im.size==(256,256) and im.mode=="RGBA", ("not native RGBA",f)
            alpha=im.getchannel("A").getbbox()
            assert alpha is not None, ("empty sprite",f)
        indexed[key]=f
    assert len(indexed)==68
    for d in range(4):
        assert ("idle",d,-1) in indexed
        for i in range(16):
            assert ("working",d,i) in indexed
    return report,qa,contract,indexed

def pack(source, target):
    if target.exists():
        raise FileExistsError("Refuse to overwrite existing native atlas output: "+str(target))
    report,qa,contract,files=checked_sources(source)
    target.mkdir(parents=True,exist_ok=False)
    outputs={}
    for size in SIZES:
        for state in ("idle","working"):
            ncols=4 if state=="idle" else 8
            nrows=1 if state=="idle" else 8
            atlas=Image.new("RGBA",(ncols*size,nrows*size))
            for d in range(4):
                ks=(-1,) if state=="idle" else range(16)
                for k in ks:
                    with Image.open(files[state,d,k]) as im:
                        cell=im.copy() if size==256 else im.resize(
                            (size,size),Image.Resampling.LANCZOS)
                    x=(d if state=="idle" else k%8)*size
                    y=(0 if state=="idle" else 2*d+k//8)*size
                    atlas.paste(cell,(x,y))
                    assert atlas.crop((x,y,x+size,y+size)).tobytes()==cell.tobytes()
            name=f"{state}-{size}.png"
            path=target/name
            atlas.save(path,optimize=True)
            with Image.open(path) as verify:
                assert verify.mode=="RGBA"
                assert verify.size==(ncols*size,nrows*size)
                assert verify.getchannel("A").getbbox() is not None
            outputs[name]={"sha256":sha(path),"width":ncols*size,"height":nrows*size}
    # Candidate graphics adapter only. This Lua MUST NOT be auto-installed or
    # called from data-final-fixes before independent in-game graphics review.
    camera=contract["capture"]
    scale=32*camera["camera_ortho_scale"]/camera["resolution"][0]
    cy,cz=camera["fixed_camera"][1:]
    yshift=-(cy+cz)/math.sqrt(2)
    lines=[
        "-- PREVIEW ONLY: this adapter is NOT installed by the atlas packer.",
        "-- Requires manual client 4-direction review; native 3x3 fluid boxes untouched.",
        'local entity=assert(data.raw["assembling-machine"] and data.raw["assembling-machine"]["steam-condenser"])',
        'assert(entity.selection_box[1][1]==-1.5 and entity.selection_box[2][1]==1.5)',
        'local boxes=assert(entity.fluid_boxes)',
        'assert(#boxes==2 and #boxes[1].pipe_connections==1 and #boxes[2].pipe_connections==1)',
        'assert(boxes[1].pipe_connections[1].position[1]==0 and boxes[1].pipe_connections[1].position[2]==-1)',
        'assert(boxes[2].pipe_connections[1].position[1]==0 and boxes[2].pipe_connections[1].position[2]==1)',
        'assert(boxes[1].pipe_connections[1].direction==defines.direction.north)',
        'assert(boxes[2].pipe_connections[1].direction==defines.direction.south)',
        'local prefix="__tanks_for_bob_fork__/graphics/entity/steam-condenser-v1/"',
        'local idle={}',
        'local active={}',
    ]
    for facing,idx in zip(DIRS,BLENDER_SOURCE_FOR_FACTORIO):
        lines.append(
            f'idle.{facing}={{filename=prefix.."idle-256.png",priority="high",'
            f'width=256,height=256,x={idx*256},y=0,frame_count=1,line_length=1,'
            f'scale={scale:.9f},shift={{0,{yshift:.9f}}}}}')
        lines.append(
            f'active.{facing}={{filename=prefix.."working-256.png",priority="high",'
            f'width=256,height=256,x=0,y={2*idx*256},frame_count=16,line_length=8,'
            f'animation_speed={FPS/60:.9f},scale={scale:.9f},'
            f'shift={{0,{yshift:.9f}}}}}')
    lines += [
        '-- Deliberately do not draw the legacy duplicate full-image working_visualisation.',
        'entity.graphics_set={animation=active,idle_animation=idle,',
        '  always_draw_idle_animation=false,',
        '  working_visualisations={{light={intensity=0.4,size=6}}}}',
        '-- No entity energy/recipes/fluids/collision/mining/icon fields changed.'
    ]
    lua=target/"candidate-graphics-only.lua"
    lua.write_text("\n".join(lines)+"\n",encoding="utf-8")
    receipt={
        "schema":"tanks.steam-condenser.v1.candidate-atlas",
        "passed":True,"native_sha256":report["native_sha256"],
        "source_render_count":68,"directions":list(DIRS),
        "blender_direction_map":list(BLENDER_SOURCE_FOR_FACTORIO),
        "frames_per_working_direction":16,"fps":FPS,
        "scale256":scale,"vertical_shift_tiles":yshift,
        "files":outputs,"lua_candidate_sha256":sha(lua),
        "game_integrated":False,"owner_visual_approved":False,
        "actual_client_screenshots":0}
    (target/"candidate-atlas-qa.json").write_text(
        json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    print("TANKS_CONDENSER_VERIFIED_68_FRAME_ATLAS_CANDIDATE_PASS",len(outputs),
          "files; NOT installed",flush=True)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--source",required=True,type=Path)
    p.add_argument("--output",required=True,type=Path)
    a=p.parse_args()
    pack(a.source.resolve(),a.output.resolve())

if __name__=="__main__":
    main()
