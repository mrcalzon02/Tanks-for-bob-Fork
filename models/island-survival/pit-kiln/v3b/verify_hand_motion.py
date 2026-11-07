#!/usr/bin/env python3
"""Test the pixel change from hand-keying all six imported flame meshes."""
import argparse,json
from pathlib import Path
from PIL import Image,ImageChops
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--out",required=True,type=Path)
    ap.add_argument("--previous",required=True,type=Path)
    a=ap.parse_args()
    new=json.loads((a.out/"build-report.json").read_text())
    if new.get("hand_keyed_original_flames")!=6 or new.get("hand_keyed_per_flame")!=17:
        raise ValueError("New keyed actions missing")
    for d in range(4):
        name=f"burning-d{d:02d}-f003.png"
        with Image.open(a.out/name) as x, Image.open(a.previous/name) as y:
            diff=ImageChops.difference(x.convert("RGB"),y.convert("RGB"))
            if not diff.getbbox():raise ValueError("No real rendered difference in direction "+str(d))
    (a.out/"hand-motion-qa.json").write_text(json.dumps({
        "passed":True,"original_animated_campfire_flames":6,
        "new_authored_keyframes_per_flame":17,"four_directions_changed":True,
        "source_frames":68,"art_accepted":False,"factorio_installed":False
    },indent=2)+"\n")
    print("HAND_AUTHORED_FIRE_PIXEL_QA_PASS")
if __name__=="__main__":main()
