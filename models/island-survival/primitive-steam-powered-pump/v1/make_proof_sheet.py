#!/usr/bin/env python3
"""One contact-sheet from REAL Blender pump frames; not simulated images."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image,ImageDraw,ImageChops,ImageFont

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",type=Path,required=True)
    args=parser.parse_args()
    out=args.output.resolve()
    report=json.loads((out/"build-report.json").read_text(encoding="utf-8"))
    native=json.loads((out/"native-reopen-qa.json").read_text(encoding="utf-8"))
    assert native["passed"] and report["render_count"]>=8
    assert native["actual_blender_frame_count"]==report["render_count"]
    sheet=Image.new("RGB",(1108,777),(26,31,35))
    d=ImageDraw.Draw(sheet)
    font=ImageFont.load_default()
    d.text((16,9),"PRIMITIVE STEAM PUMP V1 | ACTUAL BLENDER 45-DEGREE 1x2 MODEL",fill="white",font=font)
    d.text((16,28),"North output (-0.75); south input (+0.75); 2 rigid FMPL full-bore sockets; source candidate, not in game",fill="#c8d0d5",font=font)
    records=[]
    for index,orientation in enumerate(("north","east","south","west")):
        x=16+273*index
        d.text((x+4,50),orientation.upper(),fill="white",font=font)
        images={}
        for row,(state,path) in enumerate((
            ("idle",out/("idle-d%02d.png"%index)),
            ("working",out/("working-d%02d-f004.png"%index))
        )):
            with Image.open(path) as im:
                assert im.size==(256,256) and im.mode=="RGBA"
                alpha=im.getchannel("A").getbbox()
                assert alpha and 0<alpha[0] and 0<alpha[1] and alpha[2]<256 and alpha[3]<256,(path,alpha)
                src=im.copy()
            y=71+282*row
            sheet.paste(src,(x,y),src)
            d.text((x+7,y+261),state.upper(),fill="#ced7da",font=font)
            records.append({"orientation":orientation,"state":state,
                            "file":path.name,"sha256":sha(path),"alpha_bounds":alpha})
            images[state]=src
        assert ImageChops.difference(images["idle"].convert("RGB"),
                                     images["working"].convert("RGB")).getbbox() is not None
        small=images["working"].resize((64,64),Image.Resampling.LANCZOS)
        sheet.paste(small,(x+8,635),small)
        d.text((x+82,661),"64px inspection",fill="#cdd9d9",font=font)
    d.text((16,753),"Native Blender proof only. No game client screenshot, production prototype replacement or art approval implied.",fill="#d0c0ac",font=font)
    output=out/"review-four-directions.png"
    sheet.save(output,optimize=True)
    result={"schema":"tanks.primitive-steam-pump.v1.four-way-proof",
            "passed":True,"actual_cycles_renders":len(report["renders"]),
            "verified_native_blend_sha256":native["native_sha256"],
            "images":records,"contact_sha256":sha(output),
            "owner_visual_approved":False,"game_integrated":False}
    (out/"proof-qa.json").write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print("TANKS_PUMP_GENUINE_FOUR_WAY_PROOF_PASS",len(records),flush=True)

if __name__=="__main__":
    main()
