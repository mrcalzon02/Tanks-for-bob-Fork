#!/usr/bin/env python3
"""Four-way honest proof from genuine 256px Blender renders; no image generation."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageChops, ImageDraw, ImageFont

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",required=True,type=Path)
    args=parser.parse_args()
    out=args.output.resolve()
    manifest=json.loads((out/"build-report.json").read_text())
    native=json.loads((out/"native-reopen-qa.json").read_text())
    assert native["passed"] is True and native["actual_render_count"]>=8
    assert manifest["render_mode"] in ("proof","all")
    font=ImageFont.load_default()
    poster=Image.new("RGB",(1115,785),(25,30,34))
    draw=ImageDraw.Draw(poster)
    draw.text((16,12),"TANKS 3x3 STEAM CONDENSER V1 | GENUINE BLENDER SOURCE PROOF (not Factorio)",font=font,fill="white")
    draw.text((16,30),"Four rotations | idle and keyed working | original 3x3 geometry | two rigid FMPL pipe sockets",font=font,fill="#d7d9d2")
    src={}
    proofs=[]
    for d,facing in enumerate(("north","east","south","west")):
        x=16+d*274
        draw.text((x,53),facing.upper(),font=font,fill="white")
        for j,(state,name) in enumerate((("idle","idle-d%02d.png"%d),
                  ("working","working-d%02d-f004.png"%d))):
            path=out/name
            with Image.open(path) as im:
                assert im.size==(256,256) and im.mode=="RGBA"
                assert im.getchannel("A").getbbox()
                rgba=im.copy()
            y=76+j*282
            poster.paste(rgba,(x,y),rgba)
            draw.text((x+4,y+260),state.upper(),font=font,fill="white")
            src[state,d]=rgba
            proofs.append({"file":name,"sha256":sha(path)})
        rgbA=src["idle",d].convert("RGB")
        rgbB=src["working",d].convert("RGB")
        assert ImageChops.difference(rgbA,rgbB).getbbox() is not None, facing
        img=src["working",d].resize((64,64),Image.Resampling.LANCZOS)
        poster.paste(img,(x+6,650),img)
        draw.text((x+80,675),"64px visibility sample",font=font,fill="#ccd5d9")
    draw.text((16,759),"Render proof only; no gameplay/client screenshot approval or in-game attachment claimed.",font=font,fill="#cbbdb2")
    poster.save(out/"review-four-directions.png",optimize=True)
    receipt={"schema":"tanks.steam-condenser.v1.four-way-render-proof",
             "passed":True,"authentic_native_blender_renders":len(manifest["renders"]),
             "four_directions":True,"preview_64px":True,
             "native_reopened":True,"png_hashes":proofs,
             "contact_sha256":sha(out/"review-four-directions.png"),
             "game_integrated":False,"visual_owner_approved":False}
    (out/"proof-qa.json").write_text(json.dumps(receipt,indent=2)+"\n")
    print("TANKS_CONDENSER_4_DIRECTION_REAL_BLENDER_PROOF_PASS",flush=True)

if __name__=="__main__":
    main()
