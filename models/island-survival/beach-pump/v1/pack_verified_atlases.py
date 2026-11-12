#!/usr/bin/env python3
"""Pack only authentic SHA-verified Blender Beach Pump V1 frames as art candidates.

The Factorio offshore-pump uses different graphics fields than PumpPrototype.
Never auto-attach this full-object animation; the existing vanilla fallback stays
active until an official client visual and prototype-registration test succeeds.
"""
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
from PIL import Image,ImageChops

HERE=Path(__file__).resolve().parent
STATES=("idle","working")
SIZES=(64,128,256)
DIRECTIONS=("north","east","south","west")
BLENDER_FOR_FACTORIO=(0,3,2,1)
WORK_FRAMES=tuple(range(1,92,6))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def validate(source):
    c=json.loads((HERE/"contract.json").read_text(encoding="utf-8"))
    report=json.loads((source/"build-report.json").read_text(encoding="utf-8"))
    qa=json.loads((source/"native-reopen-qa.json").read_text(encoding="utf-8"))
    assert report["schema"]=="tanks.beach-pump.v1.native-blender"
    assert report["asset"]=="beachpump" and report["factorio_prototype"]=="offshore-pump/beachpump"
    assert report["render_mode"]=="all" and report["render_count"]==68
    assert len(report["renders"])==68
    assert report["working_frames"]==list(WORK_FRAMES)
    assert report["orientation_degrees"]==[0,90,180,270] and report["fps"]==8
    assert qa["passed"] and qa["real_blender_frame_count"]==68
    assert qa["source_sha256"]==report["master_sha256"]==sha(source/"beach-pump-v1.blend")
    assert qa["fixed_one_full_bore_output"] and qa["port_vertices_each"]==256
    assert qa["native_output_position"]==[0,.25] and qa["water_intake_native"]==[0,-1]
    assert qa["blender_visible_output_joint"]==[0,-.49,.36]
    assert qa["animation_loop_closed"] and qa["single_45_degree_camera"]
    assert report["fluid_fixture_sha256"]==c["fixture"]["sha256"]
    assert report["pbr_material_donor_sha256"]==c["pbr_donor"]["sha256"]
    assert report["prototype"]["tile_width"]==report["prototype"]["tile_height"]==1
    assert report["prototype"]["selection_box_native"]==[[-.6,-1.49],[.6,.49]]
    assert not report["game_integrated"] and not report["human_approved"]
    frames={}
    for rec in report["renders"]:
        d=int(rec["direction"]);k=int(rec["index"]);state=rec["state"]
        assert 0<=d<4 and state in STATES
        assert (state=="idle" and k==-1 and rec["frame"]==0) or (
            state=="working" and 0<=k<16 and rec["frame"]==WORK_FRAMES[k])
        key=(state,d,k)
        assert key not in frames,("duplicate native source",key)
        src=source/rec["file"]
        assert src.is_file() and sha(src)==rec["sha256"]
        with Image.open(src) as opened:
            assert opened.mode=="RGBA" and opened.size==(256,256)
            bounds=opened.getchannel("A").getbbox()
            assert bounds and bounds[0]>0 and bounds[1]>0 and bounds[2]<256 and bounds[3]<256
        frames[key]=src
    assert len(frames)==68
    for d in range(4):
        assert ("idle",d,-1) in frames
        for k in range(16):assert ("working",d,k) in frames
        with Image.open(frames["working",d,0]) as x,Image.open(frames["working",d,4]) as y:
            assert ImageChops.difference(x.convert("RGB"),y.convert("RGB")).getbbox() is not None
    return c,report,qa,frames

def pack(source,target):
    if target.exists():raise FileExistsError("Never overwrite prior candidate atlas directory: "+str(target))
    c,report,qa,frames=validate(source)
    target.mkdir(parents=True,exist_ok=False)
    output={}
    for size in SIZES:
        for state in STATES:
            cols,rows=((4,1) if state=="idle" else (8,8))
            atlas=Image.new("RGBA",(cols*size,rows*size),(0,0,0,0))
            for direction in range(4):
                for index in ((-1,) if state=="idle" else range(16)):
                    with Image.open(frames[state,direction,index]) as f:
                        cell=f.copy() if size==256 else f.resize(
                            (size,size),Image.Resampling.LANCZOS)
                    x=(direction if state=="idle" else index%8)*size
                    y=(0 if state=="idle" else (2*direction+index//8))*size
                    atlas.paste(cell,(x,y))
                    assert atlas.crop((x,y,x+size,y+size)).tobytes()==cell.tobytes()
            name=f"{state}-{size}.png"
            dest=target/name
            atlas.save(dest,optimize=True)
            with Image.open(dest) as check:
                check.verify()
            with Image.open(dest) as check:
                assert check.mode=="RGBA" and check.size==(cols*size,rows*size)
            output[name]={"sha256":sha(dest),"width":cols*size,"height":rows*size}
    candidate={
        "schema":"tanks.beach-pump.v1.68-frame-candidate-atlas",
        "passed":True,"source_blender_sha256":report["master_sha256"],
        "blender_native_reopen_passed":True,"actual_cycles_frame_count":68,
        "factorio_entity":"offshore-pump/beachpump",
        "native_single_south_output":c["entity"]["output_connection"],
        "fluid_source_offset_native":c["entity"]["fluid_source_offset"],
        "native_placement_selection_box":c["entity"]["selection_box_native"],
        "factorio_direction_order":list(DIRECTIONS),
        "blender_source_index_for_factorio":list(BLENDER_FOR_FACTORIO),
        "fps":8,"working_frames_each_direction":16,
        "files":output,
        "original_game_graphics_replaced":False,
        "official_offshore_pump_schema_tested":False,
        "native_client_visual_approved":False
    }
    (target/"candidate-atlas-qa.json").write_text(
        json.dumps(candidate,indent=2)+"\n",encoding="utf-8")
    print("BEACH_PUMP_GENUINE_68_FRAME_SIX_ATLASES_PASS",
          len(output),"versioned candidates; no Factorio modification",flush=True)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--source",required=True,type=Path)
    parser.add_argument("--out",required=True,type=Path)
    args=parser.parse_args()
    pack(args.source.resolve(),args.out.resolve())
if __name__=="__main__":
    main()
