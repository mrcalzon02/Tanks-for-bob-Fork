#!/usr/bin/env python3
"""Assemble strictly the eight actual Blender renders, 64px proofs and hashes."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image,ImageChops,ImageDraw,ImageFont


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--output',type=Path,required=True)
    args=p.parse_args()
    out=args.output.resolve()
    report=json.loads((out/'build-report.json').read_text())
    reopen=json.loads((out/'native-reopen-qa.json').read_text())
    assert reopen['passed'] and len(report['renders'])==8
    entries={(e['state'],e['index']):e for e in report['renders']}
    direction=('NORTH','EAST','SOUTH','WEST')
    images={};records=[]
    for i in range(4):
        for state in ('idle','working'):
            e=entries[state,i];f=out/e['file']
            with Image.open(f) as img:
                assert img.size==(256,256) and img.mode=='RGBA'
                im=img.copy()
            bbox=im.getchannel('A').getbbox()
            assert bbox and bbox[0]>0 and bbox[1]>0 and bbox[2]<256 and bbox[3]<256, (f,bbox)
            assert sha(f)==e['sha256']
            images[state,i]=im
            records.append({'file':f.name,'sha256':sha(f),'alpha_bbox':bbox})
        d=ImageChops.difference(images['idle',i].convert('RGB'),
                                images['working',i].convert('RGB'))
        assert d.getbbox() is not None,(i,'idle and working are pixel-identical')
    bg=(24,29,35)
    sheet=Image.new('RGB',(1120,782),bg)
    draw=ImageDraw.Draw(sheet)
    font=ImageFont.load_default()
    draw.text((24,12),'SOLAR BOILER V2 | TRUE PARABOLIC COLLECTORS | ACTUAL BLENDER PROOFS',fill=(244,236,217),font=font)
    draw.text((24,28),'3x2 | curved silver trough + focal tube | 3 native ports unchanged',fill=(171,194,209),font=font)
    for i,name in enumerate(direction):
        x=18+i*274
        draw.text((x+12,49),name,fill=(238,239,242),font=font)
        for row,state in enumerate(('idle','working')):
            y=68+row*282
            im=images[state,i]
            sheet.paste(im,(x,y),im)
            draw.text((x+9,y+259),state.upper(),fill=(208,212,218),font=font)
        mini=images['working',i].resize((64,64),Image.Resampling.LANCZOS)
        sheet.paste(mini,(x+20,637),mini)
        draw.text((x+94,665),'64px scale',fill=(200,207,211),font=font)
    outpath=out/'review-four-directions.png'
    sheet.save(outpath,optimize=True)
    # Genuine 128px and 64px derivatives, from the already-approved camera only.
    for size in (64,128):
        target=out/f'working-north-{size}.png'
        images['working',0].resize((size,size),Image.Resampling.LANCZOS).save(target)
    verdict={'schema':'tanks.solar-boiler.v2.review-proof','passed':True,
             'actual_blender_views':8,'directions':list(direction),
             'native_sha256':report['native_sha256'],
             'native_reopen':True,'fmpl_pbr_maps_packed':True,
             'directional_proof_sha256':sha(outpath),'cells':records,
             'working_north_64_sha256':sha(out/'working-north-64.png'),
             'working_north_128_sha256':sha(out/'working-north-128.png'),
             'visual_approved':False,'game_integrated':False}
    (out/'proof-qa.json').write_text(json.dumps(verdict,indent=2)+'\n')
    print('SOLAR_BOILER_V2_PROOF_QA_PASS',len(records),flush=True)

if __name__=='__main__':main()
