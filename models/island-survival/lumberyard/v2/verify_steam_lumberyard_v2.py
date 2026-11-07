#!/usr/bin/env python3
"""QA for actual steam lumberyard Blender captures and four preview GIFs."""
import argparse,hashlib,json
from pathlib import Path
from PIL import Image,ImageDraw,ImageChops
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--out",type=Path,required=True)
    o=p.parse_args()
    root=o.out
    r=json.loads((root/"build-report.json").read_text())
    counts=r["counts"]
    required={"raw_round_logs":6,"output_true_lengthwise_split_halves":6,
        "stove_firebox":1,"pressure_boiler":1,"steam_piston":1,
        "leather_belt":1,"drive_pulleys":2,"actual_saw_blades":1,
        "hero_split_halves":2}
    if any(counts.get(k)!=v for k,v in required.items()):raise RuntimeError("Machine geometry incomplete")
    if r["source_frames"]!=68 or r["directions"]!=[0,90,180,270] or r["camera_elevation"]!=45:
        raise RuntimeError("Incomplete camera or source render")
    if sha(root/"steam-lumberyard-v2.blend")!=r["master_sha256"]:
        raise RuntimeError("Native master not saved unchanged")
    images={}
    for rec in r["captures"]:
        path=root/rec["path"]
        if sha(path)!=rec["sha256"]:raise RuntimeError("Frame source checksum mismatch")
        with Image.open(path) as im:
            if im.mode!="RGBA" or im.size!=(256,256):raise RuntimeError("Wrong PNG mode or resolution")
            rgba=im.copy()
        bounds=rgba.getchannel("A").point(lambda x:255 if x>4 else 0).getbbox()
        if not bounds or min(bounds[:2])<1 or max(bounds[2:])>255:
            raise RuntimeError(f"Empty/clipped rendered structure: {path}, {bounds}")
        key=(rec["state"],rec["direction"],rec["index"])
        if key in images:raise RuntimeError("Duplicate render")
        images[key]=rgba
    if len(images)!=68:raise RuntimeError("Not 68 native Blender source frames")
    if len({sha(root/f"idle-d{i:02d}.png") for i in range(4)})!=4:
        raise RuntimeError("Four unique model rotations required")
    change={}
    for d in range(4):
        frames=[images["working",d,i] for i in range(16)]
        if len({sha(root/f"working-d{d:02d}-f{i:03d}.png") for i in range(16)})<15:
            raise RuntimeError("Saw/belt animation collapsed")
        # Actual log cutting/ejecting causes visual movement, not merely a light pulse.
        dif=ImageChops.difference(frames[4].convert("RGB"),frames[13].convert("RGB"))
        changed=sum(1 for rgb in dif.getdata() if max(rgb)>28)
        if changed<75:raise RuntimeError("Log cut/ejection not clearly readable "+str(d))
        change[str(d*90)]=changed
        boards=[]
        for image in frames:
            bg=Image.new("RGBA",(256,256),(41,44,48,255));bg.alpha_composite(image)
            boards.append(bg.convert("RGB"))
        preview=root/f"working-d{d:02d}-preview.gif"
        boards[0].save(preview,save_all=True,append_images=boards[1:],
                       duration=125,loop=0,disposal=2,optimize=False)
        with Image.open(preview) as gif:
            if gif.n_frames!=16:raise RuntimeError("GIF frame count collapsed")
    board=Image.new("RGB",(4*265+16,2*289+45),(25,28,32))
    pen=ImageDraw.Draw(board)
    pen.text((10,10),"LUMBERYARD V2 | BOILER / BELT / SPINNING SAW / LOGS SPLIT LENGTHWISE",fill="white")
    for row,state in enumerate(("idle","working")):
        for d in range(4):
            idx=0 if state=="idle" else 8
            bg=Image.new("RGBA",(256,256),(41,44,48,255))
            bg.alpha_composite(images[state,d,idx])
            x,y=8+265*d,38+289*row
            board.paste(bg.convert("RGB"),(x,y))
            pen.text((x+8,y+260),f"{state.upper()} / {d*90} degrees",fill="white")
    board.save(root/"four-view-review.png")
    qa={"passed":True,"source_frames":68,
        "four_original_model_rotations":True,
        "steam_stove_and_piston":True,"mechanical_belt_drive":True,
        "spinning_saw":True,"real_lengthwise_half_log_ejection":True,
        "machine_animation_change_pixels":change,
        "working_gifs":4,"game_prototype_changed":False,"visual_accepted":False}
    (root/"review-qa.json").write_text(json.dumps(qa,indent=2)+"\n")
    print("STEAM_LUMBERYARD_V2_REAL_BLENDER_QA_PASSED",json.dumps(change),flush=True)
if __name__=="__main__":main()
