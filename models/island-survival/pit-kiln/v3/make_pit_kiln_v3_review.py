#!/usr/bin/env python3
"""Review actual imported campfire-rendered kiln, not synthetic animation placeholders."""
import argparse,hashlib,json
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageChops

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--out",type=Path,required=True)
    p.add_argument("--mod",type=Path,required=True)
    a=p.parse_args()
    out=a.out
    report=json.loads((out/"build-report.json").read_text())
    if report["source_frames"]!=68 or report["imported_flame_count"]!=6 or report["removed_old_fake_flames"]!=8:
        raise ValueError("Real-source fire reuse was not confirmed")
    if len(report["source_actions"])!=6:
        raise ValueError("Six imported keyed original campfire actions not recorded")
    images={}
    for item in report["captures"]:
        path=out/item["path"]
        if sha(path)!=item["sha256"]:raise ValueError(f"Frame hash differs: {path}")
        with Image.open(path) as image:
            if image.mode!="RGBA" or image.size!=(256,256):raise ValueError("Wrong dimensions/format")
            copy=image.copy()
        a2=copy.getchannel("A").point(lambda q:255 if q>4 else 0).getbbox()
        if not a2 or min(a2[0:2])<1 or max(a2[2:4])>255:raise ValueError(f"Frame clipped: {path}")
        key=(item["state"],item["direction"],item["index"])
        if key in images:raise ValueError("Duplicate capture")
        images[key]=copy
    if len(images)!=68:raise ValueError("Source frames incomplete")
    for d in range(4):
        sequence=[images["burning",d,i] for i in range(16)]
        if len({hashlib.sha256(img.tobytes()).hexdigest() for img in sequence})<14:
            raise ValueError(f"Campfire source frames not animating in direction {d}")
        bg=[]
        for img in sequence:
            canvas=Image.new("RGBA",(256,256),(44,46,50,255))
            canvas.alpha_composite(img);bg.append(canvas.convert("RGB"))
        gif=out/f"burning-d{d:02d}-preview.gif"
        bg[0].save(gif,save_all=True,append_images=bg[1:],duration=125,loop=0,disposal=2,optimize=False)
        with Image.open(gif) as playback:
            if playback.n_frames!=16:raise ValueError("GIF collapsed")
    if len({sha(out/f"idle-d{d:02d}.png") for d in range(4)})!=4:
        raise ValueError("Direction rotations indistinguishable")
    def on_dark(image):
        canvas=Image.new("RGBA",(256,256),(44,46,50,255))
        canvas.alpha_composite(image)
        return canvas.convert("RGB")
    board=Image.new("RGB",(4*264+16,2*285+52),(26,28,32))
    draw=ImageDraw.Draw(board)
    draw.text((12,10),"KILN V3 | REAL CAMPFIRE V9 FLAME ANIMATION | FOUR ROTATIONS",fill="white")
    for row,state in enumerate(("idle","burning")):
        for d in range(4):
            x,y=8+264*d,45+285*row
            frame=images[state,d,0 if state=="idle" else 3]
            board.paste(on_dark(frame),(x,y))
            draw.text((x+4,y+259),f"{state.upper()} / {d*90} deg",fill="white")
    board.save(out/"four-view-review.png")
    a_img=Image.open(a.mod/"graphics/entity/pit-kiln.png").convert("RGBA").crop((0,0,64,64))
    original_active=Image.alpha_composite(a_img,
        Image.open(a.mod/"graphics/entity/pit-kiln-w.png").convert("RGBA").crop((0,0,64,64)))
    comp=Image.new("RGB",(4*264+16,331),(26,28,32))
    cdraw=ImageDraw.Draw(comp)
    cdraw.text((12,11),"GAME IDLE | V3 IDLE | GAME BURNING | V3 BURNING",fill="white")
    for i,im in enumerate((a_img,images["idle",0,0],original_active,images["burning",0,3])):
        frame=im.resize((64,64),Image.Resampling.LANCZOS if im.width!=64 else Image.Resampling.NEAREST)
        bg=Image.new("RGBA",(64,64),(44,46,50,255));bg.alpha_composite(frame)
        comp.paste(bg.resize((256,256),Image.Resampling.NEAREST).convert("RGB"),(8+264*i,43))
    comp.save(out/"game-versus-v3.png")
    verified=dict(passed=True,actual_frames=68,campfire_flames_imported=6,
                  old_kiln_flames_removed=8,active_frames_per_direction=16,
                  real_source_actions=report["source_actions"],
                  art_approved=False,game_installed=False)
    (out/"review-qa.json").write_text(json.dumps(verified,indent=2)+"\n")
    print("PIT_KILN_V3_IMPORTED_CAMPFIRE_PROOF_PASS",flush=True)

if __name__=="__main__":main()
