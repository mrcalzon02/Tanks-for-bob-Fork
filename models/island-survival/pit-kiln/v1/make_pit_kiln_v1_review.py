#!/usr/bin/env python3
"""Validate actual rendered source frames and create direct visual review for pit kiln."""
import argparse
import hashlib
import json
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageChops

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--out",type=Path,required=True)
    ap.add_argument("--mod",type=Path,required=True)
    args=ap.parse_args()
    out=args.out
    report=json.loads((out/"build-report.json").read_text())
    if (report["frames_count"]!=68 or report["basin_count"]!=1 or
        report["directions"] != [0,90,180,270] or
        report["states"]!={"idle":1,"burning":16}):
        raise ValueError("Wrong source geometry or four-way capture count")
    if sha(out/"pit-kiln-v1.blend")!=report["master_sha256"]:
        raise ValueError("Native Blender master checksum changed")
    images={}
    for record in report["captures"]:
        file=out/record["path"]
        if sha(file)!=record["sha256"]:
            raise ValueError("Frame checksum incorrect")
        with Image.open(file) as image:
            if image.mode!="RGBA" or image.size!=(256,256):
                raise ValueError("Wrong frame dimensions/mode")
            copy=image.copy()
        a=copy.getchannel("A")
        bbox=a.point(lambda px:255 if px>4 else 0).getbbox()
        if not bbox or min(bbox[:2])<2 or max(bbox[2:])>254:
            raise ValueError(f"Empty or clipped capture: {file}")
        key=(record["state"],record["direction"],record["index"])
        if key in images:raise ValueError("Duplicate frame record")
        images[key]=copy
    if len(images)!=68:raise ValueError("Incomplete genuine Blender captures")
    if len({sha(out/f"idle-d{d:02d}.png") for d in range(4)})!=4:
        raise ValueError("Four independent orientations missing")
    gif_paths=[]
    for d in range(4):
        animation=[images["burning",d,i] for i in range(16)]
        if len({hashlib.sha256(im.tobytes()).hexdigest() for im in animation}) < 16:
            raise ValueError(f"Collapsed fire animation in orientation {d}")
        gif_frames=[]
        for image in animation:
            background=Image.new("RGBA",(256,256),(41,44,48,255))
            background.alpha_composite(image)
            gif_frames.append(background.convert("RGB"))
        filename=out/f"burning-d{d:02d}-preview.gif"
        gif_frames[0].save(filename,save_all=True,append_images=gif_frames[1:],
                           duration=125,loop=0,disposal=2,optimize=False)
        with Image.open(filename) as saved:
            if saved.n_frames!=16:raise ValueError("Animation export collapsed frames")
        gif_paths.append(filename.name)
    original=Image.open(args.mod/"graphics/entity/pit-kiln.png").convert("RGBA")
    overlay=Image.open(args.mod/"graphics/entity/pit-kiln-w.png").convert("RGBA")
    if original.size!=(64,64) or overlay.size!=(128,64):
        raise ValueError("Source graphics changed unexpectedly")
    base=original.copy()
    for k,src in [("source-idle-64.png",base),("source-working-64.png",
                  Image.alpha_composite(base,overlay.crop((0,0,64,64))))]:
        src.save(out/k)
    try:font=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",17)
    except OSError:font=ImageFont.load_default()
    board=Image.new("RGB",(4*264+14,2*286+55),(26,29,33))
    draw=ImageDraw.Draw(board)
    draw.text((10,12),"PIT KILN V1 | actual four-view Blender render | ART REVIEW ONLY",
              font=font,fill="white")
    for row,state in enumerate(("idle","burning")):
        for d in range(4):
            src=images[state,d,0 if state=="idle" else 6]
            plate=Image.new("RGBA",(256,256),(44,47,51,255))
            plate.alpha_composite(src)
            x,y=7+264*d,46+286*row
            board.paste(plate.convert("RGB"),(x,y))
            draw.text((x+5,y+257),f"{state.upper()} / {d*90} DEG",fill="white",font=font)
    board.save(out/"four-view-review.png")
    side=Image.new("RGB",(4*263+10,334),(26,29,33))
    sd=ImageDraw.Draw(side)
    sd.text((8,9),"ORIGINAL IDLE / V1 IDLE / ORIGINAL WORKING / V1 BURNING",font=font,fill="white")
    views=[base,images["idle",0,0],Image.alpha_composite(base,overlay.crop((0,0,64,64))),
           images["burning",0,6]]
    for i,im in enumerate(views):
        display=im if im.size==(64,64) else im.resize((64,64),Image.Resampling.LANCZOS)
        bg=Image.new("RGBA",(64,64),(44,47,51,255));bg.alpha_composite(display)
        side.paste(bg.resize((256,256),Image.Resampling.NEAREST).convert("RGB"),(5+263*i,40))
    side.save(out/"original-versus-v1.png")
    qa=dict(passed=True,frame_count=len(images),directions=4,animation_frames_per_direction=16,
            source_graphics_unchanged=True,gifs=gif_paths,visual_approved=False,
            factorio_client_tested=False)
    (out/"review-qa.json").write_text(json.dumps(qa,indent=2)+"\n")
    print("PIT_KILN_V1_REAL_FRAMES_QA_PASS",flush=True)


if __name__=="__main__":
    main()
