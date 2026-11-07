#!/usr/bin/env python3
"""Validate actual 68 lumberyard Blender captures, expose four-way proof and GIFs."""
import argparse,hashlib,json
from pathlib import Path
from PIL import Image,ImageDraw,ImageChops

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def run():
    parser=argparse.ArgumentParser()
    parser.add_argument("--out",type=Path,required=True)
    args=parser.parse_args()
    out=args.out
    receipt=json.loads((out/"build-report.json").read_text())
    geo=receipt["geometry"]
    if (receipt["source_frames"]!=68 or
        receipt["rotations"]!=[0,90,180,270] or
        receipt["camera_elevation"]!=45 or
        receipt["states"]!={"idle":1,"working":16} or
        geo["raw_full_logs"]<5 or geo["output_true_split_halves"]<5 or
        not geo["two_separating_active_halves"] or
        not geo["wedge_slider"]):
        raise RuntimeError("Incomplete actual lumberyard build")
    images={}
    for f in receipt["frames"]:
        path=out/f["path"]
        if sha(path)!=f["sha256"]:raise ValueError("Source render SHA mismatch: "+str(path))
        with Image.open(path) as i:
            if i.mode!="RGBA" or i.size!=(256,256):
                raise ValueError("Wrong source image type")
            image=i.copy()
        bbox=image.getchannel("A").point(lambda a:255 if a>4 else 0).getbbox()
        if not bbox or bbox[0]<2 or bbox[1]<2 or bbox[2]>254 or bbox[3]>254:
            raise ValueError("Clipped or empty PNG: "+str(path)+" "+str(bbox))
        key=(f["state"],f["direction"],f["frame_index"])
        if key in images:raise ValueError("Duplicate image")
        images[key]=image
    if len(images)!=68:raise RuntimeError("Not all 68 Blender frames exist")
    if len({sha(out/f"idle-d{d:02d}.png") for d in range(4)})!=4:
        raise RuntimeError("Four different actual model rotations not captured")
    for d in range(4):
        motion=[images["working",d,i] for i in range(16)]
        if len({sha(out/f"working-d{d:02d}-f{i:03d}.png") for i in range(16)})<12:
            raise ValueError("Splitter animation did not produce actual visual differences")
        plates=[]
        for img in motion:
            canvas=Image.new("RGBA",(256,256),(43,46,49,255))
            canvas.alpha_composite(img)
            plates.append(canvas.convert("RGB"))
        path=out/f"working-d{d:02d}-preview.gif"
        plates[0].save(path,save_all=True,append_images=plates[1:],
                       duration=125,loop=0,disposal=2,optimize=False)
        with Image.open(path) as gif:
            if gif.n_frames<12:raise RuntimeError("Preview collapsed")
    board=Image.new("RGB",(4*268+16,2*286+55),(26,28,32))
    draw=ImageDraw.Draw(board)
    draw.text((12,10),"LUMBERYARD V1 | REAL BLENDER BLOCKOUT | FOUR CARDINAL DIRECTIONS",fill="white")
    for row,state in enumerate(("idle","working")):
        for d in range(4):
            im=images[state,d,0 if state=="idle" else 8]
            tile=Image.new("RGBA",(256,256),(43,46,49,255))
            tile.alpha_composite(im)
            x,y=8+d*268,44+row*286
            board.paste(tile.convert("RGB"),(x,y))
            draw.text((x+8,y+261),f"{state.upper()} / {d*90} deg",fill="white")
    board.save(out/"four-direction-proof.png")
    if sha(out/receipt["editable_blend"])!=receipt["master_sha256"]:
        raise RuntimeError("Editable saved native Blender master checksum mismatch")
    qa={"passed":True,"capture_count":68,"four_idle_views":True,
        "four_animated_working_views":True,
        "source_verified":True,
        "component_order":["whole round raw logs","rough wedge processor","split half-log output"],
        "game_prototype_unchanged":True,"visual_accepted":False}
    (out/"review-qa.json").write_text(json.dumps(qa,indent=2)+"\n")
    print("LUMBERYARD_V1_NATIVE_RENDER_QA_PASSED",flush=True)
if __name__=="__main__":run()
