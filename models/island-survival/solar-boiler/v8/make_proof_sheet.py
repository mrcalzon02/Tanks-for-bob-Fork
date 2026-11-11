#!/usr/bin/env python3
"""Actual Blender V8 render contact, GIF, before/after and preview atlases."""
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageChops
HERE=Path(__file__).resolve().parent
V7=HERE.parent/"generated-v7"
NAMES=("NORTH","EAST","SOUTH","WEST")
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def png(p):
    with Image.open(p) as im:
        assert im.size==(256,256) and im.mode=="RGBA",p
        return im.copy()
def main():
    p=argparse.ArgumentParser();p.add_argument("--output",type=Path,required=True)
    a=p.parse_args();out=a.output.resolve()
    qa=json.loads((out/"native-reopen-qa.json").read_text())
    assert qa["passed"] and qa["absent_floor_mesh_count"]==11
    assert qa["max_support_vertex_drift_bu"]<1e-6
    frames={}
    for d in range(4):
        frames[d,"idle",-1]=png(out/f"idle-d{d:02d}.png")
        for k in range(16):
            frames[d,"working",k]=png(out/f"working-d{d:02d}-f{k:03d}.png")
    bg=(29,33,37);font=ImageFont.load_default()
    sheet=Image.new("RGB",(1140,695),bg)
    draw=ImageDraw.Draw(sheet)
    draw.text((18,12),"SOLAR BOILER V8 | GROUND-FREE FACTORIO MACHINE | TRUE BLENDER RENDERS",font=font,fill="white")
    draw.text((18,30),"NO CONCRETE PAD / NO PAVERS | 20 original rigid supports | V7's restrained shake, bubbling and intermittent steam",font=font,fill=(203,225,215))
    for d,nm in enumerate(NAMES):
        x=18+d*280
        draw.text((x+5,55),nm,font=font,fill="white")
        for row,(state,k) in enumerate((("idle",-1),("working",4))):
            y=80+row*284
            im=frames[d,state,k];sheet.paste(im,(x,y),im)
            draw.text((x+5,y+259),"IDLE" if row==0 else "BOILING + VENTING",font=font,fill=(222,226,213))
    draw.text((20,668),"REAL Blender Cycles: 4 idle, 64 operating; 11 ground meshes removed; 3 Factorio fluid mouths fixed | REVIEW CANDIDATE",font=font,fill=(228,213,175))
    sheet.save(out/"review-four-directions.png",optimize=True)
    movie=[]
    for k in range(16):
        canvas=Image.new("RGB",(512,512),bg)
        for d in range(4):
            im=frames[d,"working",k]
            canvas.paste(im,((d%2)*256,(d//2)*256),im.getchannel("A"))
        movie.append(canvas)
    gif=out/"working-four-directions-floorless.gif"
    movie[0].save(gif,save_all=True,append_images=movie[1:],
                  duration=125,loop=0,optimize=False)
    with Image.open(gif) as im:assert im.n_frames==16
    side=Image.new("RGB",(544,302),bg)
    d2=ImageDraw.Draw(side)
    old=png(V7/"working-d00-f004.png")
    new=frames[0,"working",4]
    side.paste(old,(8,28),old.getchannel("A"))
    side.paste(new,(280,28),new.getchannel("A"))
    d2.text((8,8),"V7 | concrete pad and pavers",font=font,fill="white")
    d2.text((280,8),"V8 | same machine, no built-in floor",font=font,fill="white")
    side.save(out/"comparison-v7-v8-actual-blender.png",optimize=True)
    # The resulting floorless render must genuinely have transparent pixels
    # where V7's concrete plate covered the terrain.
    alpha_removed=[]
    for d in range(4):
        prev=png(V7/f"working-d{d:02d}-f004.png")
        curr=frames[d,"working",4]
        count=sum(x>y+40 for x,y in zip(prev.getchannel("A").getdata(),
                                          curr.getchannel("A").getdata()))
        assert count>=100,("No meaningful alpha cutout from pad removal",d,count)
        alpha_removed.append(count)
    atlases={}
    for size in (64,128,256):
        idle=Image.new("RGBA",(4*size,size))
        work=Image.new("RGBA",(8*size,8*size))
        for d in range(4):
            idle.paste(frames[d,"idle",-1].resize((size,size),Image.Resampling.LANCZOS),(d*size,0))
            for k in range(16):
                slot=d*16+k
                work.paste(frames[d,"working",k].resize((size,size),Image.Resampling.LANCZOS),
                           ((slot%8)*size,(slot//8)*size))
        a=f"preview-only-solar-v8-idle-{size}.png"
        b=f"preview-only-solar-v8-working-{size}.png"
        idle.save(out/a,optimize=True);work.save(out/b,optimize=True)
        atlases[str(size)]={"idle":a,"working":b}
    proof={
        "schema":"tanks.solar.v8.actual-cycles-floorless-proof","passed":True,
        "real_blender_frames":68,"directions":4,"fps":8,
        "measured_removed_opaque_pixels_by_direction":alpha_removed,
        "contact_sha256":sha(out/"review-four-directions.png"),
        "comparison_sha256":sha(out/"comparison-v7-v8-actual-blender.png"),
        "gif_sha256":sha(gif),"atlases":atlases,
        "preview_only":True,"visual_approved":False,"game_integrated":False}
    (out/"proof-qa.json").write_text(json.dumps(proof,indent=2)+"\n")
    print("SOLAR_V8_REAL_BLENDER_TRANSPARENT_FLOORLESS_PROOF_PASS",alpha_removed,flush=True)
if __name__=="__main__":main()
