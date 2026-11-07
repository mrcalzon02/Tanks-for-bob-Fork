#!/usr/bin/env python3
"""Make actual V2 four-way visual evidence from rendered RGBA frames and source."""
import argparse,hashlib,json,math
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageChops

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def run():
    p=argparse.ArgumentParser()
    p.add_argument("--out",type=Path,required=True)
    p.add_argument("--mod",type=Path,required=True)
    args=p.parse_args()
    out=args.out
    manifest=json.loads((out/"build-report.json").read_text())
    if (manifest["frame_count"]!=68 or manifest["staged_bricks"]!=4 or
        manifest["inner_bank_bricks"]!=10 or manifest["staging_wooden_slab_count"]!=1):
        raise RuntimeError("V2 construction/readback mismatch")
    imgs={}
    for record in manifest["captures"]:
        path=out/record["path"]
        if sha(path)!=record["sha256"]:
            raise RuntimeError(f"Frame SHA mismatch {path}")
        with Image.open(path) as source:
            if source.mode!="RGBA" or source.size!=(256,256):
                raise RuntimeError("NonRGBA or wrong-size render")
            img=source.copy()
        bbox=img.getchannel("A").point(lambda x:255 if x>4 else 0).getbbox()
        if not bbox or min(bbox[:2])<2 or max(bbox[2:])>254:
            raise RuntimeError(f"Clipped visible geometry {path}: {bbox}")
        key=(record["state"],record["direction"],record["index"])
        if key in imgs:raise RuntimeError("Duplicate frame")
        imgs[key]=img
    if len(imgs)!=68:raise RuntimeError("Missing genuine rendered frames")
    for d in range(4):
        sequence=[imgs["burning",d,i] for i in range(16)]
        if len({hashlib.sha256(im.tobytes()).hexdigest() for im in sequence})<14:
            raise RuntimeError("Flame animation lacks distinct motion")
        opaque=[]
        for im in sequence:
            b=Image.new("RGBA",(256,256),(43,46,50,255))
            b.alpha_composite(im)
            opaque.append(b.convert("RGB"))
        gif=out/f"burning-d{d:02d}-preview.gif"
        opaque[0].save(gif,save_all=True,append_images=opaque[1:],
                       duration=125,loop=0,disposal=2,optimize=False)
        with Image.open(gif) as check:
            if check.n_frames!=16:raise RuntimeError("GIF frame collapse")
    if len({sha(out/f"idle-d{d:02d}.png") for d in range(4)}) !=4:
        raise RuntimeError("Four rotated idle views missing")
    def canvas(image):
        bg=Image.new("RGBA",(256,256),(43,46,50,255))
        bg.alpha_composite(image)
        return bg.convert("RGB")
    board=Image.new("RGB",(4*264+16,2*285+48),(25,27,31))
    pen=ImageDraw.Draw(board)
    pen.text((10,8),"PIT KILN V2 | STAGED WET BRICKS + FIRING BANK / REVIEW ONLY",fill="white")
    for row,state in enumerate(("idle","burning")):
        for d in range(4):
            x,y=8+d*264,40+row*285
            board.paste(canvas(imgs[state,d,0 if state=="idle" else 2]),(x,y))
            pen.text((x+8,y+259),f"{state} {d*90}deg",fill="white")
    board.save(out/"four-view-review.png")
    original=Image.open(args.mod/"graphics/entity/pit-kiln.png").convert("RGBA").crop((0,0,64,64))
    base=Image.open(args.mod/"graphics/entity/pit-kiln-w.png").convert("RGBA")
    active=Image.alpha_composite(original,base.crop((0,0,64,64)))
    match=Image.new("RGB",(4*264+16,322),(25,27,31))
    d=ImageDraw.Draw(match)
    d.text((8,8),"ORIGINAL IDLE | V2 IDLE | ORIGINAL ACTIVE | V2 ACTIVE",fill="white")
    for i,im in enumerate((original,imgs["idle",0,0],active,imgs["burning",0,2])):
        im=im.resize((64,64),Image.Resampling.LANCZOS if im.width!=64 else Image.Resampling.NEAREST)
        bg=Image.new("RGBA",(64,64),(43,46,50,255))
        bg.alpha_composite(im)
        match.paste(bg.resize((256,256),Image.Resampling.NEAREST).convert("RGB"),(8+i*264,40))
    match.save(out/"original-vs-v2.png")
    if not (out/"pit-kiln-v2.blend").is_file():raise RuntimeError("No editable master")
    receipt={"passed":True,"frame_count":68,"four_idles":True,
             "bricks_on_slab":4,"bricks_on_firing_bank":10,
             "all_four_animations_verified":True,"production_accepted":False}
    (out/"review-qa.json").write_text(json.dumps(receipt,indent=2)+"\n")
    print("PIT_KILN_V2_QA_COMPLETE",flush=True)
if __name__=="__main__":run()
