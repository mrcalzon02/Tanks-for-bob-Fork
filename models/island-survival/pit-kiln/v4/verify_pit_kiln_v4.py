#!/usr/bin/env python3
"""Validate V4's actual frames and produce four-direction visual review and GIFs."""
import argparse,hashlib,json
from pathlib import Path
from PIL import Image,ImageChops,ImageDraw
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def main():
    a=argparse.ArgumentParser()
    a.add_argument("--out",type=Path,required=True)
    a.add_argument("--previous",type=Path,required=True)
    opt=a.parse_args()
    out=opt.out;prev=opt.previous
    r=json.loads((out/"build-report.json").read_text())
    if (r["source_frames"]!=68 or r["original_campfire_flames"]!=6 or
        r["new_crackle_controls"]!=6 or r["staged_bricks_wobbling"]!=4 or
        r["bank_bricks_stationary"]!=10 or len(r["original_campfire_actions"])!=6):
        raise RuntimeError("Original flame provenance or brick motion setup invalid")
    images={}
    for rec in r["captures"]:
        path=out/rec["path"]
        if sha(path)!=rec["sha256"]:raise RuntimeError("Wrong frame checksum")
        with Image.open(path) as im:
            if im.mode!="RGBA" or im.size!=(256,256):raise RuntimeError("Wrong source image type")
            img=im.copy()
        bbox=img.getchannel("A").point(lambda q:255 if q>4 else 0).getbbox()
        if not bbox or min(bbox[:2])<2 or max(bbox[2:])>254:raise RuntimeError("Clipped frame")
        key=(rec["state"],rec["direction"],rec["index"])
        if key in images:raise RuntimeError("Duplicate frame")
        images[key]=img
    if len(images)!=68:raise RuntimeError("Incomplete render count")
    pixel_counts={}
    for d in range(4):
        files=[out/f"burning-d{d:02d}-f{i:03d}.png" for i in range(16)]
        if len(set(sha(p) for p in files))!=16:
            raise RuntimeError("Flame sequence has collapsed frames")
        with Image.open(prev/f"burning-d{d:02d}-f004.png") as old:
            delta=ImageChops.difference(images[("burning",d,4)].convert("RGB"),old.convert("RGB"))
            count=sum(1 for px in delta.getdata() if max(px)>25)
        if count<15:raise RuntimeError(f"Visual changes missing in {d*90}° direction: {count}")
        pixel_counts[str(d*90)]=count
        frames=[]
        for i in range(16):
            bg=Image.new("RGBA",(256,256),(43,46,50,255))
            bg.alpha_composite(images[("burning",d,i)])
            frames.append(bg.convert("RGB"))
        path=out/f"burning-d{d:02d}-preview.gif"
        frames[0].save(path,save_all=True,append_images=frames[1:],duration=125,loop=0,disposal=2,optimize=False)
        with Image.open(path) as gif:
            if gif.n_frames!=16:raise RuntimeError("GIF frame collapse")
    if len({sha(out/f"idle-d{d:02d}.png") for d in range(4)})!=4:
        raise RuntimeError("Four model rotations not distinct")
    board=Image.new("RGB",(1072,625),(26,29,33))
    dr=ImageDraw.Draw(board)
    dr.text((10,10),"PIT KILN V4 | WOBBLING WET BRICKS + CRACKLING REUSED CAMPFIRE",fill="white")
    for row,state in enumerate(("idle","burning")):
        for d in range(4):
            src=images[(state,d,0 if state=="idle" else 4)]
            bg=Image.new("RGBA",(256,256),(43,46,50,255));bg.alpha_composite(src)
            x,y=8+d*264,42+row*286
            board.paste(bg.convert("RGB"),(x,y))
            dr.text((x+6,y+260),f"{state.upper()} / {d*90} deg",fill="white")
    board.save(out/"four-view-review.png")
    report={"passed":True,"real_source_frames":68,"original_campfire_actions":6,
        "animated_staged_bricks":4,"nonmoving_bank_bricks":10,
        "original_flames_plus_crackle_controls":6,"emitted_embers":2,
        "crackle_pixel_changes":pixel_counts,"four_animated_gifs":4,
        "art_accepted":False,"prototype_modified":False}
    (out/"review-qa.json").write_text(json.dumps(report,indent=2)+"\n")
    print("PIT_KILN_V4_REUSABLE_ANIMATION_QA_PASS",pixel_counts)
if __name__=="__main__":main()
