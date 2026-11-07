#!/usr/bin/env python3
"""Fail-closed sprite comparison for the actual native clay-pit V2 renders."""
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageChops


def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def visible_rgb_difference(left, right):
    """Compare visible composite RGB, not RGBA alpha-only getbbox.

    PIL Image.getbbox on an RGBA difference may ignore changed RGB when alpha
    is identical, incorrectly calling material-only revisions visually equal.
    """
    if left.size != right.size:
        raise ValueError('Cannot compare images of different sizes')
    background=Image.new('RGBA',left.size,(48,51,56,255))
    a=Image.alpha_composite(background,left.convert('RGBA')).convert('RGB')
    b=Image.alpha_composite(background,right.convert('RGBA')).convert('RGB')
    return ImageChops.difference(a,b).getbbox()


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--out',type=Path,required=True)
    p.add_argument('--mod',type=Path,required=True)
    p.add_argument('--v1',type=Path)
    args=p.parse_args()
    out=args.out.resolve()
    mod=args.mod.resolve()
    report=json.loads((out/'build-report.json').read_text())
    if report.get('schema')!=2 or len(report['captures'])!=8:
        raise ValueError('Missing V2 native build/capture report')
    source=Image.open(mod/'graphics/entity/clay-pit.png').convert('RGBA')
    overlay=Image.open(mod/'graphics/entity/clay-pit-w.png').convert('RGBA')
    if source.size not in ((64,64),(120,64)) or overlay.size!=(64,64):
        raise ValueError('Unexpected source sprite dimensions')
    original=source.crop((0,0,64,64))
    original.save(out/'source-idle-64.png')
    overlay.save(out/'source-overlay-64.png')
    composite=Image.alpha_composite(original,overlay)
    composite.save(out/'source-composite-64.png')
    shots={}
    for state in ('idle','working'):
        for d in range(4):
            file=out/f'{state}-d{d:02d}.png'
            with Image.open(file) as loaded:
                if loaded.mode!='RGBA' or loaded.size!=(256,256):
                    raise ValueError(f'Wrong rendered image type/dimensions: {file}')
                img=loaded.copy()
            bounds=img.getchannel('A').point(lambda v:255 if v>5 else 0).getbbox()
            if bounds is None or bounds[0]<2 or bounds[1]<2 or bounds[2]>254 or bounds[3]>254:
                raise ValueError(f'Clipped/empty Blender render: {file}, bounds={bounds}')
            record=next((r for r in report['captures'] if r['state']==state and
                          r['angle']==d*90),None)
            if not record or record['sha256']!=sha(file):
                raise ValueError('Actual captured frame hash missing/mismatch')
            shots[state,d]=img
        if len({sha(out/f'{state}-d{d:02d}.png') for d in range(4)})!=4:
            raise ValueError(f'Direction rotation failed: {state}')
    for d in range(4):
        if not visible_rgb_difference(shots['idle',d],shots['working',d]):
            raise ValueError(f'Working props invisible in direction {d}')
    try:
        font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',15)
        bold=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',18)
    except OSError:
        font=bold=ImageFont.load_default()
    states=('idle','working')
    board=Image.new('RGB',(4*270+20,2*297+65),(27,30,34))
    draw=ImageDraw.Draw(board)
    draw.text((12,13),'CLAY PIT V2 | 45-degree structure camera | NOT ACCEPTED ART',font=bold,fill='white')
    for r,state in enumerate(states):
        y=48+r*297
        for d in range(4):
            x=10+d*270
            tile=Image.new('RGBA',(256,256),(48,51,56,255))
            tile.alpha_composite(shots[state,d])
            board.paste(tile.convert('RGB'),(x,y))
            draw.text((x+8,y+260),f'{state.upper()} / {d*90} deg',font=font,fill='white')
    board.save(out/'v2-four-direction-proof.png')
    compare=Image.new('RGB',(4*272+18,344),(27,30,34))
    d=ImageDraw.Draw(compare)
    d.text((12,10),'SOURCE SPRITE vs V2 MODEL | 64px effective pixel scale',font=bold,fill='white')
    targets=[('Original idle',original),('V2 idle',shots['idle',0]),
            ('Original working',composite),('V2 working',shots['working',0])]
    for k,(name,img) in enumerate(targets):
        x=10+k*272
        native=img.resize((64,64),Image.Resampling.LANCZOS) if img.size!=(64,64) else img
        plate=Image.new('RGBA',(64,64),(48,51,56,255))
        plate.alpha_composite(native)
        compare.paste(plate.resize((256,256),Image.Resampling.NEAREST).convert('RGB'),(x,43))
        d.text((x+8,305),name,font=font,fill='white')
    compare.save(out/'v2-original-vs-model-64.png')
    artifacts=['v2-four-direction-proof.png','v2-original-vs-model-64.png']
    if args.v1 and args.v1.is_file():
        with Image.open(args.v1) as v1:
            if v1.size!=(256,256) or v1.mode!='RGBA':
                raise ValueError('V1 benchmark must be actual 256px Blender frame')
            old=v1.copy()
        if not visible_rgb_difference(old,shots['working',0]):
            raise ValueError('V2 model is visually identical to V1')
    qa={'passed':True,'render_count':8,'visible_pits':1,
        'four_cardinal_directions':True,'working_state_visually_distinct':True,
        'visual_art_accepted':False,'engine_tested':False,
        'source_png_hashes':{'idle':sha(mod/'graphics/entity/clay-pit.png'),
                             'working':sha(mod/'graphics/entity/clay-pit-w.png')},
        'sheet_hashes':{x:sha(out/x) for x in artifacts}}
    (out/'review-qa.json').write_text(json.dumps(qa,indent=2)+'\n')
    print('CLAY_PIT_V2_REFERENCE_AND_EIGHT_RENDER_QA_PASS',flush=True)


if __name__=='__main__':main()
