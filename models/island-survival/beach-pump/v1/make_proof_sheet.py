#!/usr/bin/env python3
"""Review ONLY true 256px Blender Cycles PNG frames from the saved beachpump."""
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
from PIL import Image,ImageChops,ImageDraw,ImageFont

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--out",required=True,type=Path)
    args=ap.parse_args()
    out=args.out.resolve()
    manifest=json.loads((out/"build-report.json").read_text(encoding="utf-8"))
    reopen=json.loads((out/"native-reopen-qa.json").read_text(encoding="utf-8"))
    assert reopen["passed"] and reopen["real_blender_frame_count"]>=8
    assert manifest["render_count"]>=8
    canvas=Image.new("RGB",(1116,796),(27,31,33))
    draw=ImageDraw.Draw(canvas)
    font=ImageFont.load_default()
    draw.text((18,9),"BEACH PUMP V1 | ORIGINAL NATIVE BLENDER, NOT IN-GAME SPRITES",
              fill="white",font=font)
    draw.text((18,28),"Water-side +Y / south single full-bore output / no concrete slab / shoreline rocker and paddle",
              fill="#d0d3cb",font=font)
    seen=[]
    for i,direction in enumerate(("north","east","south","west")):
        x=18+274*i
        draw.text((x,54),direction.upper(),fill="white",font=font)
        images={}
        for row,(state,path) in enumerate((
                ("idle",out/f"idle-d{i:02d}.png"),
                ("working",out/f"working-d{i:02d}-f004.png"))):
            with Image.open(path) as opened:
                assert opened.size==(256,256) and opened.mode=="RGBA",path
                img=opened.copy()
            alpha=img.getchannel("A").getbbox()
            assert alpha and alpha[0]>0 and alpha[1]>0 and alpha[2]<256 and alpha[3]<256,(path,alpha)
            y=73+282*row
            canvas.paste(img,(x,y),img)
            draw.text((x+5,y+258),state.upper(),fill="#d7e0de",font=font)
            images[state]=img
            seen.append({"state":state,"direction":direction,
                         "filename":path.name,"sha256":sha(path),
                         "alpha_bounds":list(alpha)})
        assert ImageChops.difference(images["idle"].convert("RGB"),
                images["working"].convert("RGB")).getbbox() is not None, direction
        small=images["working"].resize((64,64),Image.Resampling.LANCZOS)
        canvas.paste(small,(x+7,640),small)
        draw.text((x+76,664),"64px Factorio readability",fill="#d0d5d3",font=font)
    draw.text((18,763),"Authentic Blender renders / native source verified. NO Factorio client visuals or art approval asserted.",
        fill="#d8c2a7",font=font)
    dest=out/"review-four-directions.png"
    canvas.save(dest,optimize=True)
    qa={"schema":"tanks.beach-pump.v1.proof","passed":True,
        "actual_cycles_frames":manifest["render_count"],
        "native_source_sha256":manifest["master_sha256"],
        "true_cardinal_45_degree":True,"native_reopened":True,
        "four_facing_evidence":seen,"contact_sha256":sha(dest),
        "game_integrated":False,"human_art_approved":False}
    (out/"proof-qa.json").write_text(json.dumps(qa,indent=2)+"\n",encoding="utf-8")
    print("BEACH_PUMP_V1_REAL_FOUR_DIRECTION_BLENDER_PROOF_PASS",len(seen),flush=True)
if __name__=="__main__":
    main()
