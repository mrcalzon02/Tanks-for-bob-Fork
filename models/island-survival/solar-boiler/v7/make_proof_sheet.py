#!/usr/bin/env python3
"""Build visible proof using ONLY genuine V6 and V7 Blender PNG renders."""
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent
V6=HERE.parent/"generated-v6"
NAMES=("NORTH","EAST","SOUTH","WEST")
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def png(path):
    with Image.open(path) as im:
        assert im.size==(256,256) and im.mode=="RGBA",path
        return im.copy()
def main():
    p=argparse.ArgumentParser();p.add_argument("--output",type=Path,required=True)
    a=p.parse_args();out=a.output.resolve()
    qa=json.loads((out/"native-reopen-qa.json").read_text())
    assert qa["passed"] and qa["max_ground_vertex_drift_bu"]<1e-6
    data={}
    for d in range(4):
        data[d,"idle",-1]=png(out/f"idle-d{d:02d}.png")
        for k in range(16):data[d,"working",k]=png(out/f"working-d{d:02d}-f{k:03d}.png")
    bg=(29,33,37);font=ImageFont.load_default()
    canvas=Image.new("RGB",(1140,695),bg);draw=ImageDraw.Draw(canvas)
    draw.text((18,12),"SOLAR BOILER V7 | NATIVE BLENDER | BASE PLATE LOCKED TO THE GROUND",font=font,fill="white")
    draw.text((18,30),"Fixed concrete and supports; half-strength upper rumble; unchanged glass boiling and steam; 3 fixed Factorio pipe mouths",font=font,fill=(203,225,215))
    for d,name in enumerate(NAMES):
        x=18+d*280
        draw.text((x+5,55),name,font=font,fill="white")
        for row,(state,k) in enumerate((("idle",-1),("working",4))):
            y=80+row*284
            im=data[d,state,k];canvas.paste(im,(x,y),im)
            draw.text((x+5,y+259),"IDLE" if row==0 else "BOILING & VENTING",font=font,fill=(222,226,213))
    draw.text((20,668),f"VERIFIED: {qa['grounded_mesh_count']} grounded meshes, zero movement at every sampled frame; 68 real Cycles views; owner review pending",font=font,fill=(228,213,175))
    canvas.save(out/"review-four-directions.png",optimize=True)
    # Four-panel animation uses exact rendered frame files, not constructed sprites.
    frames=[]
    for k in range(16):
        view=Image.new("RGB",(512,512),bg)
        for d in range(4):
            im=data[d,"working",k];view.paste(im,((d%2)*256,(d//2)*256),im.getchannel("A"))
        frames.append(view)
    gif=out/"working-four-directions-ground-locked.gif"
    frames[0].save(gif,save_all=True,append_images=frames[1:],duration=125,loop=0,optimize=False)
    with Image.open(gif) as check:assert check.n_frames==16
    # Comparison is real old/new Blender renders, not a synthetic redraw.
    side=Image.new("RGB",(544,302),bg)
    draw2=ImageDraw.Draw(side)
    old=png(V6/"working-d00-f004.png")
    new=data[0,"working",4]
    side.paste(old,(8,28),old.getchannel("A"))
    side.paste(new,(280,28),new.getchannel("A"))
    draw2.text((8,8),"V6 | entire footing shakes",font=font,fill="white")
    draw2.text((280,8),"V7 | fixed footing, calmer upper body",font=font,fill="white")
    side.save(out/"comparison-v6-v7-real-blender.png",optimize=True)
    previews={}
    for size in (64,128,256):
        idle=Image.new("RGBA",(4*size,size))
        motion=Image.new("RGBA",(8*size,8*size))
        for d in range(4):
            idle.paste(data[d,"idle",-1].resize((size,size),Image.Resampling.LANCZOS),(d*size,0))
            for k in range(16):
                slot=d*16+k
                motion.paste(data[d,"working",k].resize((size,size),Image.Resampling.LANCZOS),((slot%8)*size,(slot//8)*size))
        idle_name=f"preview-only-solar-v7-idle-{size}.png"
        work_name=f"preview-only-solar-v7-working-{size}.png"
        idle.save(out/idle_name,optimize=True)
        motion.save(out/work_name,optimize=True)
        previews[str(size)]={"idle":idle_name,"working":work_name}
    result={"schema":"tanks.solar.v7.actual-cycles-proof","passed":True,
            "frames":68,"directions":4,"fps":8,"preview_only":True,
            "review_four_directions_sha256":sha(out/"review-four-directions.png"),
            "real_before_after_sha256":sha(out/"comparison-v6-v7-real-blender.png"),
            "four_direction_gif_sha256":sha(gif),"atlases":previews,
            "visual_approved":False,"game_integrated":False}
    (out/"proof-qa.json").write_text(json.dumps(result,indent=2)+"\n")
    print("SOLAR_V7_REAL_BLENDER_PROOF_AND_GIF_PASS",flush=True)
if __name__=="__main__":main()
