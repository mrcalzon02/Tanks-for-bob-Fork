#!/usr/bin/env python3
"""Contact sheet, GIF and actual small-size QA for Solar Boiler V4 pilot."""
from pathlib import Path
from PIL import Image,ImageChops,ImageDraw,ImageFont
import argparse,hashlib,json,math


def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();out=a.output.resolve()
    rec=json.loads((out/'build-report.json').read_text())
    native=json.loads((out/'native-reopen-qa.json').read_text())
    assert native['passed'] and native['wood_plank_conduits']>=60
    assert len(rec['renders'])==24
    assert len(rec.get('steam_isolation',[]))==2
    collected={}
    margins=[]
    for sample in rec['renders']:
        path=out/sample['file']
        with Image.open(path) as original:
            assert original.mode=='RGBA' and original.size==(256,256),path
            im=original.copy()
        box=im.getchannel('A').getbbox()
        assert box and 0<box[0]<box[2]<256 and 0<box[1]<box[3]<256,(path.name,box)
        collected[path.name]=im
        margins.append({'file':path.name,'bounds':list(box),'sha256':sha(path)})
    steam0=out/'steam-isolation-off.png';steam1=out/'steam-isolation-on.png'
    with Image.open(steam0) as a,Image.open(steam1) as b:
        before=a.convert('RGB');after=b.convert('RGB')
    # Compare same-frame steam enable/disable; no other actor/camera moves.
    delta=ImageChops.difference(before,after)
    changed=sum(1 for r,g,b in delta.getdata() if max(r,g,b)>=9)
    assert changed>=18,('Soft steam invisible in actual Cycles sprite',changed)
    # Actual 8 different rendered views; real 16-frame motion in north.
    for i,orientation in enumerate(('north','east','south','west')):
        idle=collected[f'idle-d{i:02d}.png'].convert('RGB')
        active=collected[f'working-d{i:02d}.png'].convert('RGB')
        assert ImageChops.difference(idle,active).getbbox() is not None,orientation
    frames=[collected[f'loop-d00-f{k:03d}.png'] for k in range(16)]
    unique=len({hashlib.sha256(im.tobytes()).hexdigest() for im in frames})
    assert unique>=12,('V4 animation not visually moving',unique)
    # Stone-quiet scene needs a recognizable wooden barrel at 64px.
    small=collected['working-d00.png'].resize((64,64),Image.Resampling.LANCZOS)
    small.save(out/'north-working-native-64.png')
    B=(23,27,31)
    sheet=Image.new('RGB',(1116,946),B);draw=ImageDraw.Draw(sheet)
    font=ImageFont.load_default()
    draw.text((22,12),'SOLAR BOILER V4 | 3x2 SURVIVAL TIMBER | REAL BLENDER CYCLES PROOF',fill='white',font=font)
    draw.text((22,30),'18 bowed barrel staves / wooden plank pipes / polished wood parabola / open relief vapor',fill=(200,205,208),font=font)
    for i,orientation in enumerate(('north','east','south','west')):
        x=16+i*275
        draw.text((x+8,55),orientation.upper(),fill=(244,240,222),font=font)
        for j,state in enumerate(('idle','working')):
            y=75+j*301
            im=collected[f'{state}-d{i:02d}.png']
            sheet.paste(im,(x,y),im)
            draw.text((x+8,y+260),state.upper(),fill=(205,205,205),font=font)
        tiny=collected[f'working-d{i:02d}.png'].resize((64,64),Image.Resampling.LANCZOS)
        sheet.paste(tiny,(x+8,715),tiny)
        draw.text((x+79,744),'64px native scale',fill=(210,210,210),font=font)
    draw.text((22,816),'Only metal: 3 native pipe collars, small gauge, relief valve and focal receiver tubes.',fill=(240,230,202),font=font)
    draw.text((22,838),'No red-hot wooden barrel. All original V3 thermal-shell/steam-sphere parts preserved but render-hidden.',fill=(210,210,210),font=font)
    proof=out/'review-four-directions.png';sheet.save(proof,optimize=True)
    # A GIF is a diagnostic of native Cycles frames, no synthetic interpolation.
    outframes=[]
    for im in frames:
        layer=Image.new('RGBA',(256,256),(*B,255));layer.alpha_composite(im)
        outframes.append(layer.convert('RGB'))
    gif=out/'working-north-v4-preview.gif'
    outframes[0].save(gif,save_all=True,append_images=outframes[1:],duration=125,loop=0,disposal=2)
    with Image.open(gif) as g:assert g.n_frames==16
    qa={'schema':'tanks.solar-boiler.v4.pixel-qa','passed':True,
        'native_reopen':True,'actual_blender_views':24,'cardinal_idle_and_working':8,
        'north_working_frames':16,'working_unique_pixel_frames':unique,
        'native64_size':[64,64],'all_alpha_margins_valid':True,
        'pixel_checks':margins,'proof_sha256':sha(proof),'gif_sha256':sha(gif),
        'steam_source':'atmospheric-relief-only','steam_changed_rgb_pixels':changed,'wood_material_source':'approved campfire packed PBR',
        'visual_approved':False,'game_integrated':False}
    (out/'proof-qa.json').write_text(json.dumps(qa,indent=2)+'\n')
    print('SOLAR_V4_TRUE_CYCLES_24_RENDER_AND_64PX_PROOF_PASS',unique,flush=True)

if __name__=='__main__':main()
