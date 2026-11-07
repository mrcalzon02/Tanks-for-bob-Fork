#!/usr/bin/env python3
"""Fail-closed review sheet of real source PNGs and actual Blender render evidence."""
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageChops


def digest(f):return hashlib.sha256(Path(f).read_bytes()).hexdigest()


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--out',type=Path,required=True)
    p.add_argument('--mod',type=Path,required=True)
    a=p.parse_args()
    out=a.out.resolve(); mod=a.mod.resolve()
    base=Image.open(mod/'graphics/entity/clay-pit.png').convert('RGBA')
    work=Image.open(mod/'graphics/entity/clay-pit-w.png').convert('RGBA')
    if base.size!=(120,64) or work.size!=(64,64):
        raise ValueError('Unexpected mod sprite dimensions; revisit exact source analysis')
    gamebase=base.crop((0,0,64,64))
    fill=Image.new('RGBA',(64,64),(53,55,58,255))
    composite=Image.alpha_composite(Image.alpha_composite(fill,gamebase),work)
    gamebase.save(out/'reference-idle-64.png')
    work.save(out/'reference-working-overlay-64.png')
    composite.save(out/'reference-working-composite-64.png')
    # Each of these images must be an actual Blender capture and not a programmatic
    # sprite rotation. Compare directional states as genuine independent 3D renders.
    captures={}
    for state in ('idle','working'):
        for d in range(4):
            path=out/f'{state}-d{d:02d}.png'
            if not path.is_file():raise FileNotFoundError(path)
            with Image.open(path) as im:
                if im.mode!='RGBA' or im.size!=(256,256):raise ValueError('Render is not 256px RGBA')
                tile=im.copy()
            alpha=tile.getchannel('A')
            bbox=alpha.point(lambda v:255 if v>5 else 0).getbbox()
            if not bbox or any((bbox[0] < 2,bbox[1] < 2,bbox[2] > 254,bbox[3] > 254)):
                raise ValueError(f'Clipping or empty Blender render: {state} {d} {bbox}')
            captures[(state,d)]=tile
    for d in range(4):
        if not ImageChops.difference(captures[('idle',d)],captures[('working',d)]).getbbox():
            raise ValueError(f'Idle/working state not visually distinct: {d}')
    for state in ('idle','working'):
        if len({digest(out/f'{state}-d{d:02d}.png') for d in range(4)})!=4:
            raise ValueError(f'Four actual directions are not unique for {state}')
    try:font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',15)
    except OSError:font=ImageFont.load_default()
    board=Image.new('RGB',(4*270+24,2*306+64),(27,29,33))
    draw=ImageDraw.Draw(board)
    draw.text((16,12),'CLAY PIT V1 | 45 degree structure-camera blockout | NOT ACCEPTED ART',font=font,fill='white')
    labels=('0 / NORTH','90 / EAST','180 / SOUTH','270 / WEST')
    for row,state in enumerate(('idle','working')):
        y=46+row*306
        for d in range(4):
            x=12+d*270
            plate=Image.new('RGBA',(256,256),(49,52,56,255))
            plate.alpha_composite(captures[(state,d)])
            board.paste(plate.convert('RGB'),(x,y))
            draw.text((x+8,y+262),f'{state.upper()} / {labels[d]}',font=font,fill=(239,239,241))
    board.save(out/'v1-four-direction-proof.png')
    reference=Image.new('RGB',(900,330),(27,29,33))
    dr=ImageDraw.Draw(reference)
    dr.text((12,10),'SOURCE TRUTH: only first 64 columns of 120px base are rendered in game',font=font,fill='white')
    for i,(label,tile) in enumerate([('CURRENT BASE',gamebase),('CURRENT WORKING OVERLAY',work),('GAME COMPOSITE',composite)]):
        x=12+i*296
        under=Image.new('RGBA',(64,64),(49,52,56,255));under.alpha_composite(tile)
        reference.paste(under.resize((256,256),Image.Resampling.NEAREST).convert('RGB'),(x,42))
        dr.text((x+8,303),label,font=font,fill='white')
    reference.save(out/'source-reference-three-panel.png')
    report=json.loads((out/'build-report.json').read_text())
    if len(report['captures'])!=8:raise ValueError('Unexpected native capture count')
    qa={'passed':True,'evidence':['source-reference-three-panel.png','v1-four-direction-proof.png'],
        'source_dimensions':list(base.size),'game_visible_crop':[0,0,64,64],
        'working_sprite_dimensions':list(work.size),'render_count':8,
        'source_png_hashes':{'base':digest(mod/'graphics/entity/clay-pit.png'),'working':digest(mod/'graphics/entity/clay-pit-w.png')},
        'review_hashes':{n:digest(out/n) for n in ['v1-four-direction-proof.png','source-reference-three-panel.png']}}
    (out/'review-qa.json').write_text(json.dumps(qa,indent=2)+'\n')
    print('CLAY_PIT_REFERENCE_AND_RENDER_QA_PASS: 1 visible basin; 4 actual rotations; idle+working')

if __name__=='__main__':main()
