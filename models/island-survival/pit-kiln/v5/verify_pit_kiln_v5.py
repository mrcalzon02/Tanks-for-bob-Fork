#!/usr/bin/env python3
"""Verify V5 rigid TRAY animation, original Campfire V9 effects and four Blender views."""
import argparse,hashlib,json
from pathlib import Path
from PIL import Image,ImageChops,ImageDraw
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--out",type=Path,required=True)
    p.add_argument("--previous",type=Path,required=True)
    args=p.parse_args()
    out=args.out
    source=json.loads((out/"build-report.json").read_text())
    assert source["source_frames"]==68
    assert source["rocking_plank_count"]==1 and source["rocking_brick_count"]==4
    assert source["per_brick_actions_remaining"]==0
    assert source["static_firing_bank_bricks"]==10
    assert source["original_campfire_flames"]==6 and len(source["original_campfire_source_actions"])==6
    assert source["preserved_v4_crackle_controls"]==6
    assert len(source["tray_children"])==5 and len(set(source["tray_children"]))==5
    assert len(source["tray_pixel_motion"])==4
    for d,measure in source["tray_pixel_motion"].items():
        if measure["tray_corner_motion_px_256"]<3.5 or measure["seam_px_256"]>.15:
            raise RuntimeError(f"Invalid whole-tray movement in {d} degrees")
    images={}
    for item in source["captures"]:
        path=out/item["path"]
        if sha(path)!=item["sha256"]:raise RuntimeError("SHA error "+str(path))
        with Image.open(path) as raw:
            if raw.mode!="RGBA" or raw.size!=(256,256):raise RuntimeError("Invalid native render")
            image=raw.copy()
        bound=image.getchannel("A").point(lambda x:255 if x>4 else 0).getbbox()
        if not bound or min(bound[:2])<2 or max(bound[2:])>254:
            raise RuntimeError("Clipped transparent source "+str(path))
        key=(item["state"],item["direction"],item["index"])
        if key in images:raise RuntimeError("Duplicate frame")
        images[key]=image
    if len(images)!=68:raise RuntimeError("Not 68 source frames")
    changes={}
    for d in range(4):
        old=args.previous/f"burning-d{d:02d}-f004.png"
        with Image.open(old) as v4:
            delta=ImageChops.difference(v4.convert("RGB"),images["burning",d,4].convert("RGB"))
            changed=sum(1 for pix in delta.getdata() if max(pix)>20)
        if changed<20:raise RuntimeError(f"V5 render identical to V4 in direction {d}")
        changes[str(d*90)]=changed
        sequence=[]
        for i in range(16):
            plate=Image.new("RGBA",(256,256),(43,46,51,255))
            plate.alpha_composite(images["burning",d,i])
            sequence.append(plate.convert("RGB"))
        target=out/f"burning-d{d:02d}-preview.gif"
        sequence[0].save(target,save_all=True,append_images=sequence[1:],
                         duration=125,loop=0,disposal=2,optimize=False)
        with Image.open(target) as gif:
            if gif.n_frames!=16:raise RuntimeError("Collapsed GIF")
    if len({sha(out/f"idle-d{d:02d}.png") for d in range(4)})!=4:
        raise RuntimeError("Four actual idle rotations not distinct")
    board=Image.new("RGB",(1072,627),(27,29,33))
    draw=ImageDraw.Draw(board)
    draw.text((12,11),"PIT KILN V5 | WHOLE WOODEN TRAY + FOUR BRICKS ROCK TOGETHER",fill="white")
    for row,state in enumerate(("idle","burning")):
        for d in range(4):
            src=images[state,d,0 if state=="idle" else 4]
            plate=Image.new("RGBA",(256,256),(43,46,51,255))
            plate.alpha_composite(src)
            x,y=8+d*264,43+row*287
            board.paste(plate.convert("RGB"),(x,y))
            draw.text((x+7,y+260),f"{state.upper()} / {d*90} deg",fill="white")
    board.save(out/"four-view-review.png")
    result={"passed":True,"frames":68,"entire_tray_children":5,
            "rig_rocking_bricks":4,"rig_rocking_plank":1,
            "independent_brick_keys":0,
            "preserved_campfire_flame_actions":6,
            "preserved_crackle_controls":6,
            "pixel_travel_by_direction":source["tray_pixel_motion"],
            "visual_changes_v4_to_v5":changes,
            "gifs":4,"prototype_changed":False,"art_approved":False}
    (out/"review-qa.json").write_text(json.dumps(result,indent=2)+"\n")
    print("PIT_KILN_V5_WHOLE_TRAY_QA_PASS",json.dumps(result["pixel_travel_by_direction"]),flush=True)
if __name__=="__main__":main()
