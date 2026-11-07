#!/usr/bin/env python3
"""Pack already VERIFIED Pit Kiln V4b Blender captures into Factorio sprite atlases.

Fast pack-only production. This does not rerender, touch live graphics or change
a prototype; uses the source SHA256 frame manifest and 4-direction QA receipt.
"""
import argparse,hashlib,json,shutil
from pathlib import Path
from PIL import Image

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def make():
    ap=argparse.ArgumentParser()
    ap.add_argument("--source",required=True,type=Path)
    ap.add_argument("--out",required=True,type=Path)
    args=ap.parse_args()
    src=args.source.resolve();out=args.out.resolve()
    if out.exists() and any(out.iterdir()):
        raise ValueError("Production path exists; refuse overwriting approved art")
    out.mkdir(parents=True,exist_ok=True)
    report=json.loads((src/"build-report.json").read_text())
    qa=json.loads((src/"review-qa.json").read_text())
    if not(qa.get("passed") and qa.get("real_source_frames")==68 and
           report.get("original_campfire_flames")==6 and
           report.get("staged_bricks_wobbling")==4 and
           report.get("new_crackle_controls")==6 and
           report.get("tray_parts")==5 and
           report.get("staging_board_stationary") is False and
           qa.get("whole_board_and_bricks_rock_together") is True):
        raise ValueError("Unverified V4b input, missing source original campfire or brick wobble")
    records={(r["state"],r["direction"],r["index"]):r for r in report["captures"]}
    if len(records)!=68:raise ValueError("Source frame manifest incomplete")
    if sha(src/"pit-kiln-v4b-whole-tray.blend")!=report["master_sha256"]:
        raise ValueError("Saved Blender master has changed")
    outputs={}
    for state in ("idle","burning"):
        for size in (64,128,256):
            atlas=Image.new("RGBA",(size*8,size*8),(0,0,0,0))
            for direction in range(4):
                for frame in range(16):
                    record=records[(state,direction,frame if state=="burning" else 0)]
                    path=src/record["path"]
                    if not path.is_file() or sha(path)!=record["sha256"]:
                        raise ValueError("Source frame checksum failure: "+record["path"])
                    with Image.open(path) as original:
                        if original.mode!="RGBA" or original.size!=(256,256):
                            raise ValueError("Source is not 256x256 RGBA")
                        image=(original.copy() if size==256 else original.resize(
                            (size,size),Image.Resampling.LANCZOS))
                    if image.getchannel("A").getbbox() is None:
                        raise ValueError("Empty source frame")
                    px=(frame%8)*size;py=(direction*2+frame//8)*size
                    atlas.paste(image,(px,py))
            name=f"pit-kiln-v4b-{state}-{size}.png"
            target=out/name
            atlas.save(target,optimize=True)
            with Image.open(target) as verify:
                if verify.mode!="RGBA" or verify.size!=(size*8,size*8):
                    raise ValueError("Atlas re-open failed")
                for d in range(4):
                    for f in range(16):
                        crop=verify.crop(((f%8)*size,(d*2+f//8)*size,
                                          (f%8+1)*size,(d*2+f//8+1)*size))
                        if not crop.getchannel("A").getbbox():
                            raise ValueError("Empty atlas cell")
            outputs[name]={"sha256":sha(target),"cell_px":size,"dimensions":[8*size,8*size]}
    # Factorio 2.1 Lua attachment reference: complete alternate idle and burning
    # states, no layered duplicate fire; choose 128px cells -> scale 0.5.
    def dirs(state):
        lines=[]
        for i,d in enumerate(("north","east","south","west")):
            lines.append(f'    {d} = {{ filename = "__tanks_for_bob_fork__/graphics/entity/pit-kiln-v4b-{state}-128.png", '
                         f'width = 128, height = 128, x = 0, y = {i*256}, '
                         f'line_length = 8, frame_count = 16, animation_speed = 8/60, scale = 0.5 }}')
        return "{\n"+",\n".join(lines)+"\n  }"
    lua=("-- Prototype-ready Factorio 2.1 graphics_set for existing assembling-machine/pit-kiln.\n"
         "-- Attach ONLY after explicit art approval. Original prototype is unchanged.\n"
         "graphics_set = {\n  animation = "+dirs("burning")+
         ",\n  idle_animation = "+dirs("idle")+
         ",\n  always_draw_idle_animation = false\n}\n")
    (out/"prototype-ready.lua").write_text(lua)
    shutil.copy2(src/"four-view-review.png",out/"four-view-review.png")
    icon_source=src/"idle-d00.png"
    with Image.open(icon_source) as still:
        icon=still.convert("RGBA").resize((64,64),Image.Resampling.LANCZOS)
        icon.save(out/"pit-kiln-v4b-icon-64.png")
    outputs["pit-kiln-v4b-icon-64.png"]={"sha256":sha(out/"pit-kiln-v4b-icon-64.png"),"dimensions":[64,64]}
    receipt={"passed":True,"asset":"pit-kiln","revision":"v4b",
        "original_source":"Campfire V9 keyframed native fire, retained via V3b",
        "source_master_sha256":report["master_sha256"],"source_rgba_frames":68,
        "idle_frames_per_direction":16,"burning_frames_per_direction":16,
        "model_rotations":[0,90,180,270],"fps":8,"three_resolutions":[64,128,256],
        "whole_tray_motion_verified":True,"art_accepted":False,"prototype_attached":False,"factorio_client_tested":False,
        "files":outputs}
    (out/"production-qa.json").write_text(json.dumps(receipt,indent=2)+"\n")
    print("PIT_KILN_V4B_FACTORIO_ATLAS_QA_PASS",json.dumps({k:v["sha256"] for k,v in outputs.items()}),flush=True)
if __name__=="__main__":make()
