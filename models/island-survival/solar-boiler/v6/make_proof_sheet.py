#!/usr/bin/env python3
"""QA and GIF assembled from real Blender RGBA images; no synthetic sprites."""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageChops

DIRECTIONS=('NORTH','EAST','SOUTH','WEST')


def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def pixel_difference(a,b,threshold=12):
    dif=ImageChops.difference(a.convert('RGB'),b.convert('RGB'))
    return sum(max(rgb)>threshold for rgb in dif.getdata())


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True)
    args=p.parse_args();out=args.output.resolve()
    report=json.loads((out/'build-report.json').read_text())
    native=json.loads((out/'native-reopen-qa.json').read_text())
    assert native['passed'] and native['native_pipe_mouths_rigid']
    assert len(report['renders'])==68 and len(report['isolation'])==3
    data={};checks=[]
    for d,direction in enumerate(DIRECTIONS):
        for state in ('idle','working'):
            seq=(-1,) if state=='idle' else range(16)
            for k in seq:
                filename=f'idle-d{d:02d}.png' if state=='idle' else f'working-d{d:02d}-f{k:03d}.png'
                path=out/filename
                with Image.open(path) as img:
                    assert img.mode=='RGBA' and img.size==(256,256),(filename,img.size,img.mode)
                    im=img.copy()
                bounds=im.getchannel('A').getbbox()
                assert bounds and 0<bounds[0]<bounds[2]<256 and 0<bounds[1]<bounds[3]<256,(filename,bounds)
                data[d,state,k]=im
                checks.append({'file':filename,'sha256':sha(path),'bounds':list(bounds)})
    effects={}
    for name in ('focal-boil','focal-steam','body-rumble'):
        files=[out/f'iso-{name}-{state}.png' for state in ('off','on')]
        with Image.open(files[0]) as l,Image.open(files[1]) as r:
            a=l.convert('RGBA');b=r.convert('RGBA')
            effects[name]={
                'changed_rgb_256':pixel_difference(a,b,12),
                'changed_rgb_64':pixel_difference(
                    a.resize((64,64),Image.Resampling.LANCZOS),
                    b.resize((64,64),Image.Resampling.LANCZOS),6)
            }
    # Actual captured 64px sprite visibility, not a rig keyframe existence test.
    assert effects['focal-boil']['changed_rgb_256']>=30,effects
    assert effects['focal-boil']['changed_rgb_64']>=3,effects
    assert effects['focal-steam']['changed_rgb_256']>=18,effects
    assert effects['focal-steam']['changed_rgb_64']>=2,effects
    assert effects['body-rumble']['changed_rgb_256']>=10,effects
    # Rumble can be deliberately subpixel at 64px; capture at 256 and 64.
    assert effects['body-rumble']['changed_rgb_64']>=1,effects
    for d in range(4):
        hashes=[sha(out/f'working-d{d:02d}-f{k:03d}.png') for k in range(16)]
        assert len(set(hashes))==16,(d,len(set(hashes)))
        assert pixel_difference(data[d,'idle',-1],data[d,'working',4])>30

    # Fixed Factorio camera, 4 directions x 16 ordered frames. Explicitly
    # mark atlases preview-only until human approval/native engine attachment.
    atlases={}
    for size in (64,128,256):
        def scaled(src):return src.resize((size,size),Image.Resampling.LANCZOS)
        idle=Image.new('RGBA',(size*4,size))
        for d in range(4):idle.paste(scaled(data[d,'idle',-1]),(d*size,0))
        idlename=f'preview-only-solar-v6-idle-{size}.png'
        idle.save(out/idlename,optimize=True)
        working=Image.new('RGBA',(size*8,size*8))
        for d in range(4):
            for k in range(16):
                slot=d*16+k
                working.paste(scaled(data[d,'working',k]),
                              ((slot%8)*size,(slot//8)*size))
        name=f'preview-only-solar-v6-working-{size}.png'
        working.save(out/name,optimize=True)
        atlases[str(size)]={'idle':{'file':idlename,'sha256':sha(out/idlename)},
                            'working':{'file':name,'sha256':sha(out/name)},
                            'ordered_frames':64,'direction_order':list(DIRECTIONS)}

    bg=(27,32,36);font=ImageFont.load_default()
    canvas=Image.new('RGB',(1130,905),bg)
    draw=ImageDraw.Draw(canvas)
    draw.text((20,12),'SOLAR BOILER V6 | TRUE BLENDER | GLASS HOT-WATER RECEIVERS AT BOTH OPTICAL FOCI',font=font,fill=(241,241,230))
    draw.text((20,31),'Wooden barrel and polished timber optics; BOTH glass foci boil and vent; rigid Factorio sockets',font=font,fill=(195,215,195))
    for d,name in enumerate(DIRECTIONS):
        x=16+d*278
        draw.text((x+4,54),name,font=font,fill='white')
        for row,(state,k,label) in enumerate((('idle',-1,'IDLE / cold focal glass'),('working',4,'WORKING / boiling glass'))):
            y=76+row*284
            im=data[d,state,k]
            canvas.paste(im,(x,y),im)
            draw.text((x+4,y+260),label,font=font,fill=(212,219,215))
        mini=data[d,'working',4].resize((64,64),Image.Resampling.LANCZOS)
        canvas.paste(mini,(x+10,659),mini)
        draw.text((x+84,685),'native 64px',font=font,fill=(200,212,208))
    draw.text((20,769),'FOCAL TUBES: clear water, keyed roiling surfaces, 24 moving bubbles; steam from four tiny open relief holes.',font=font,fill=(207,221,208))
    draw.text((20,790),'MOTION: restrained wooden body/2 concentrator rumble; 33 flexible plank skins; 3 metal grid pipe mouths immobile.',font=font,fill=(207,221,208))
    draw.text((20,819),f"ISOLATION: bubble {effects['focal-boil']['changed_rgb_64']}px, steam {effects['focal-steam']['changed_rgb_64']}px, rumble {effects['body-rumble']['changed_rgb_64']}px (at 64px).",font=font,fill=(158,217,226))
    draw.text((20,856),'CANDIDATE ONLY | Visual approval and Factorio prototype game integration have not occurred.',font=font,fill=(237,201,140))
    contact=out/'review-four-directions.png'
    canvas.save(contact,optimize=True)

    # This is a genuine animated GIF of the actual 64 Cycles sprite renders.
    frames=[]
    for k in range(16):
        comp=Image.new('RGB',(512,512),bg)
        for d in range(4):
            im=data[d,'working',k]
            dx=256*(d%2);dy=256*(d//2)
            comp.paste(im,(dx,dy),im.getchannel('A'))
        frames.append(comp)
    gif=out/'working-four-directions-focal-glass-rumble.gif'
    frames[0].save(gif,save_all=True,append_images=frames[1:],duration=125,loop=0,optimize=False)
    with Image.open(gif) as image:
        assert image.n_frames==16

    receipt={'schema':'tanks.solar.v6.focal-glass-rumble.cycles',
             'passed':True,'native_reopen':native['passed'],
             'actual_blender_views':68,'effect_isolation_render_count':6,
             'directions':list(DIRECTIONS),'fps':8,'frames_per_direction':16,
             'measured_rgba_pixel_changes':effects,
             'real_blender_render_sources':checks,
             'atlases':atlases,'preview_only':True,
             'contact_sha256':sha(contact),'gif_sha256':sha(gif),
             'visual_approved':False,'game_integrated':False}
    (out/'proof-qa.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print('SOLAR_V6_FOUR_CARDINAL_GLASS_BOIL_STEAM_AND_RUMBLE_PROOF_PASS',effects,flush=True)

if __name__=='__main__':main()
