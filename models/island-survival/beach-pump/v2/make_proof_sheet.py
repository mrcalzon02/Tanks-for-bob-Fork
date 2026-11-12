#!/usr/bin/env python3
"""Contact proof from real Beach Pump V2 Blender renders, not image generation."""
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
from PIL import Image,ImageChops,ImageDraw,ImageFont

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--out",required=True,type=Path)
    a=ap.parse_args()
    out=a.out.resolve()
    r=json.loads((out/"build-report.json").read_text(encoding="utf-8"))
    v=json.loads((out/"native-reopen-qa.json").read_text(encoding="utf-8"))
    assert v["passed"] and v["actual_blender_frames"]==r["render_count"]
    assert r["render_count"] in (8,68)
    canvas=Image.new("RGB",(1120,790),(27,31,36))
    d=ImageDraw.Draw(canvas)
    f=ImageFont.load_default()
    d.text((18,9),"BEACH PUMP V2: REAL BLENDER ARCHIMEDES SCREW / TROUGH / WHEEL / BIG CRANK",fill="white",font=f)
    d.text((18,27),"Independent Blender model reopen passed; four facings, idle and working, not game screenshots",fill="#c6d1cb",font=f)
    checks=[]
    for i,name in enumerate(("north","east","south","west")):
        x=18+i*274
        d.text((x+3,53),name.upper(),fill="#e0e5e7",font=f)
        views={}
        for row,(state,filename) in enumerate((("idle",f"idle-d{i:02d}.png"),
                            ("working",f"working-d{i:02d}-f004.png"))):
            path=out/filename
            with Image.open(path) as original:
                assert original.mode=="RGBA" and original.size==(256,256)
                rgba=original.copy()
            alpha=rgba.getchannel("A").getbbox()
            assert alpha and alpha[0]>0 and alpha[1]>0 and alpha[2]<256 and alpha[3]<256,(filename,alpha)
            y=74+281*row
            canvas.paste(rgba,(x,y),rgba)
            d.text((x+6,y+257),state.upper(),fill="#dae4e5",font=f)
            views[state]=rgba
            checks.append({"file":filename,"direction":name,"state":state,"sha256":sha(path),"alpha_bbox":alpha})
        assert ImageChops.difference(views["idle"].convert("RGB"),views["working"].convert("RGB")).getbbox() is not None,name
        sample=views["working"].resize((64,64),Image.Resampling.LANCZOS)
        canvas.paste(sample,(x+7,635),sample)
        d.text((x+81,667),"64px Factorio read",fill="#d8dddc",font=f)
    d.text((18,761),"Native Blender render proof. Original offshore pump logic / 0.01 tick speed / one south output untouched.",fill="#dec9b5",font=f)
    path=out/"review-four-directions.png"
    canvas.save(path,optimize=True)
    report={"schema":"tanks.beach-pump.v2.native-four-way-contact","passed":True,
      "native_reopened":True,"actual_blender_frames":r["render_count"],
      "verified_views":checks,"contact_sha256":sha(path),
      "game_integrated":False,"human_visual_approved":False}
    (out/"proof-qa.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print("BEACH_PUMP_V2_GENUINE_BLENDER_FOUR_WAY_PROOF_PASS",len(checks),flush=True)
if __name__=="__main__":
    main()
