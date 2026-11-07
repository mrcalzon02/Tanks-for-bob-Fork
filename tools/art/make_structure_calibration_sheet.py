"""Generate immutable calibration comparisons from real rendered frames and original sprite."""
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageChops
import argparse

parser=argparse.ArgumentParser()
parser.add_argument('--captures',type=Path,required=True)
parser.add_argument('--original',type=Path,required=True)
opts=parser.parse_args()
out=opts.captures
manifest=json.loads((out/'capture.json').read_text())
if not manifest['passed'] or len(manifest['captures']) != 13:
    raise SystemExit("Capture manifest incomplete")
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',17)
small=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',13)
bg=(26,29,34)
tile=(45,48,54)
def paste_obj(canvas,img,x,y,size=210):
    image=Image.open(img).convert('RGBA')
    image.thumbnail((size,size),Image.Resampling.LANCZOS)
    rect=Image.new('RGBA',(size,size),(47,49,52,255))
    rect.alpha_composite(image,((size-image.width)//2,(size-image.height)//2))
    canvas.paste(rect.convert('RGB'),(x,y))
def label(draw,xy,txt):
    draw.text(xy,txt,font=font,fill=(235,236,239))
def make(rows,filename,subtitle):
    n=max(len(row) for row in rows)
    margin,gap,cell,top=22,14,210,75
    width=margin*2+n*cell+(n-1)*gap
    height=top+len(rows)*266+25
    im=Image.new('RGB',(width,height),bg)
    dr=ImageDraw.Draw(im)
    dr.text((margin,12),subtitle,font=font,fill=(248,249,250))
    for i,row in enumerate(rows):
        y=top+i*266
        for j,(caption,path) in enumerate(row):
            x=margin+j*(cell+gap)
            paste_obj(im,path,x,y)
            dr.text((x,y+216),caption,font=small,fill=(225,225,228))
    im.save(out/filename)
    return im
original=opts.original
if not original.is_file():
    raise SystemExit("Missing original unlit sprite")
make([
    [('ORIGINAL: game 64px',original),
     ('CURRENT: ~32.4°, yaw 35°',out/'previous_32_d000.png'),
     ('38°, yaw 0°',out/'candidate_38_d000.png')],
    [('45°, yaw 0°',out/'factorio_45_d000.png'),
     ('45°, yaw 35°',out/'diagonal_45_d000.png'),
     ('50°, yaw 0°',out/'candidate_50_d000.png')],
], 'calibration-pitches.png', 'CAMPFIRE CAMERA CALIBRATION | original vs actual Blender renders')
make([
    [(f'STRUCTURE 45° | model {a}°',out/f'factorio_45_d{a:03d}.png')
      for a in (0,90,180,270)]
], 'calibration-four-directions.png', 'FOUR STRUCTURE ORIENTATIONS | fixed 45° orthographic camera')
make([
    [('ORIGINAL 64x64',original),
     ('OLD V11 ~32.4°',out/'previous_32_d000.png'),
     ('PROPOSED 45°',out/'factorio_45_d000.png')]
], 'campfire-before-after.png', 'CAMPFIRE | in-game reference and candidate structure angle')
for rec in manifest['captures']:
    p=out/rec['image']
    with Image.open(p) as image:
        if image.mode != 'RGBA' or image.size != (256,256):
            raise SystemExit(f'Invalid Blender capture: {p}')
for p in ['calibration-pitches.png','calibration-four-directions.png','campfire-before-after.png']:
    if not (out/p).is_file():
        raise SystemExit(f'Missing comparison: {p}')
print('CALIBRATION_COMPARISON_PASSED; 13 captured views; 3 contact sheets')
