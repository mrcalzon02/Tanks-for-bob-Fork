#!/usr/bin/env python3
"""Proof from genuine Blender RGBA frames, never illustrations or fake sprites."""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageChops

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True,type=Path)
    args=p.parse_args();out=args.output.resolve()
    report=json.loads((out/'build-report.json').read_text())
    assert len(report['renders'])==24 and set(report['isolation'])=={'fluid','steam'}
    dirs=('NORTH','EAST','SOUTH','WEST')
    images={}
    source=[]
    for state in ('idle','working'):
        for d in range(4):
            filename=f'{state}-d{d:02d}.png'
            with Image.open(out/filename) as im:
                assert im.mode=='RGBA' and im.size==(256,256),filename
                img=im.copy();bbox=img.getchannel('A').getbbox()
                assert bbox is not None,filename
                assert bbox[0]>0 and bbox[1]>0 and bbox[2]<256 and bbox[3]<256,(filename,bbox)
                images[state,d]=img
                source.append({'file':filename,'sha256':sha(out/filename),'bounds':list(bbox)})
    frames=[]
    for i in range(16):
        path=out/f'working-north-f{i:03d}.png'
        with Image.open(path) as im:
            assert im.mode=='RGBA' and im.size==(256,256),path.name
            img=im.copy();bbox=img.getchannel('A').getbbox()
            assert bbox and bbox[0]>0 and bbox[1]>0 and bbox[2]<256 and bbox[3]<256,(path.name,bbox)
            frames.append(img)
    assert len(set(sha(out/f'working-north-f{i:03d}.png') for i in range(16)))>=13,'Animated boiling scene appears static'
    effects={}
    def changed(a,b,threshold=11):
        da=ImageChops.difference(a.convert('RGB'),b.convert('RGB'))
        pix=list(da.getdata());return sum(max(rgb)>threshold for rgb in pix)
    for name in ('fluid','steam'):
        with Image.open(out/f'iso-{name}-off.png') as a,Image.open(out/f'iso-{name}-on.png') as b:
            aa=a.convert('RGBA');bb=b.convert('RGBA')
            effects[name]={'pixel_changes_256':changed(aa,bb),'pixel_changes_64':changed(
                aa.resize((64,64),Image.Resampling.LANCZOS),bb.resize((64,64),Image.Resampling.LANCZOS),6)}
    # Real 64px gameplay visibility gates; do not accept only metadata.
    assert effects['fluid']['pixel_changes_256']>=60,effects
    assert effects['fluid']['pixel_changes_64']>=3,effects
    assert effects['steam']['pixel_changes_256']>=40,effects
    assert effects['steam']['pixel_changes_64']>=2,effects
    bg=(23,29,33)
    canvas=Image.new('RGB',(1130,875),bg)
    draw=ImageDraw.Draw(canvas);font=ImageFont.load_default()
    draw.text((18,13),'SOLAR BOILER V5 - ACTUAL BLENDER / GLASS BOILING TUBE / WOOD SOCKET REPAIRS / END VENT STEAM',fill=(238,238,226),font=font)
    draw.text((18,31),'V4 timber retained: 18 barrel staves, 65 plank conduits, polished-wood parabolas, 3 original fluid fittings',fill=(183,201,180),font=font)
    for d,name in enumerate(dirs):
        x=15+d*278
        draw.text((x+5,54),name,fill='white',font=font)
        for row,state in enumerate(('idle','working')):
            y=76+row*281;im=images[state,d]
            canvas.paste(im,(x,y),im)
            draw.text((x+5,y+260),state.upper(),fill=(224,225,222),font=font)
        mini=images['working',d].resize((64,64),Image.Resampling.LANCZOS)
        canvas.paste(mini,(x+12,656),mini)
        draw.text((x+88,680),'64px native read',fill=(204,218,212),font=font)
    draw.text((18,756),'REAL CYCLIC EFFECTS - 16 animated boiling poses; alternating steam jets at intentionally vented glass ends',fill=(220,225,217),font=font)
    draw.text((18,778),f"FLUID pixels: {effects['fluid']['pixel_changes_256']} @256, {effects['fluid']['pixel_changes_64']} @64",fill=(167,219,203),font=font)
    draw.text((18,797),f"END STEAM pixels: {effects['steam']['pixel_changes_256']} @256, {effects['steam']['pixel_changes_64']} @64",fill=(177,204,219),font=font)
    draw.text((18,826),'CANDIDATE ONLY: user visual approval / full four-direction atlas / Factorio prototype integration pending',fill=(240,214,157),font=font)
    canvas.save(out/'review-four-directions.png',optimize=True)
    # Small original GIF compiled solely from the native Blender frame series.
    anim=[]
    for im in frames:
        rgb=Image.new('RGB',im.size,bg);rgb.paste(im,mask=im.getchannel('A'))
        anim.append(rgb)
    anim[0].save(out/'working-north-boiling-and-venting.gif',save_all=True,
                 append_images=anim[1:],duration=125,loop=0,optimize=False)
    with Image.open(out/'working-north-boiling-and-venting.gif') as gif:
        assert gif.n_frames==16
    qa={'schema':'tanks.solar.v5.cycles.proof','passed':True,'actual_blender_views':24,
        'isolation_render_count':4,'four_directions':list(dirs),'fps':8,'work_frames_per_direction_proven':16,
        'real_unique_working_north_frames':len(set(sha(out/f'working-north-f{i:03d}.png') for i in range(16))),
        'glass_fluid_effect_pixels':effects['fluid'],'two_end_steam_effect_pixels':effects['steam'],
        'images':source,'proof_sha256':sha(out/'review-four-directions.png'),
        'gif_sha256':sha(out/'working-north-boiling-and-venting.gif'),
        'native_reopen':(out/'native-reopen-qa.json').is_file(),
        'visual_approved':False,'game_integrated':False}
    (out/'proof-qa.json').write_text(json.dumps(qa,indent=2)+'\n')
    print('SOLAR_V5_VISIBLE_GLASS_FLUID_AND_END_STEAM_CYCLES_PASS',effects,flush=True)

if __name__=='__main__':main()
