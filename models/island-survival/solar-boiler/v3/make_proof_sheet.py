#!/usr/bin/env python3
"""Generate actual 16-frame x four-orientation atlas and visual GIF proof; no proxy art."""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
from PIL import Image, ImageChops, ImageDraw, ImageFont

STATES=('idle','working')
NAMES=('north','east','south','west')


def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def actual_rgb_delta(first,second,threshold=12):
    a=first.convert('RGB');b=second.convert('RGB')
    diff=ImageChops.difference(a,b)
    r,g,blue=diff.split()
    return sum(1 for x,y,z in zip(r.getdata(),g.getdata(),blue.getdata()) if max(x,y,z)>threshold)


def make_atlas(frames,size):
    """8 columns, 2 rows per orientation, four orientations stacked, 16 frames."""
    count=16
    sheet=Image.new('RGBA',(size*8,size*8))
    for direction in range(4):
        for index in range(count):
            source=frames[direction][index].resize((size,size),Image.Resampling.LANCZOS)
            x=(index%8)*size
            y=(direction*2+index//8)*size
            sheet.paste(source,(x,y))
    return sheet


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--pilot-isolation',action='store_true')
    args=parser.parse_args()
    out=args.output.resolve()
    report=json.loads((out/'build-report.json').read_text())
    if args.pilot_isolation:
        contrasts={}
        assert set(report['isolation'])=={'gauge','heat','joint-steam'}
        for group,pair in report['isolation'].items():
            for rec in pair:
                assert sha(out/rec['file'])==rec['sha256']
            with Image.open(out/pair[0]['file']) as f, Image.open(out/pair[1]['file']) as t:
                contrasts[group]=actual_rgb_delta(f.convert('RGBA'),t.convert('RGBA'))
        print('SOLAR_V3_PILOT_EFFECT_CHANGED_PIXELS',contrasts,flush=True)
        assert contrasts['gauge']>=18,contrasts
        assert contrasts['heat']>=30,contrasts
        assert contrasts['joint-steam']>=30,contrasts
        (out/'pilot-isolation-qa.json').write_text(json.dumps({'passed':True,'changed_pixels':contrasts},indent=2)+'\n')
        return
    reopen=json.loads((out/'native-reopen-qa.json').read_text())
    assert reopen['passed'] and report['render_count']==68
    by_name={rec['file']:rec for rec in report['renders']}
    images={'idle':[], 'working':[]}
    checks=[]
    for direction in range(4):
        idlefile=f'idle-d{direction:02d}.png'
        with Image.open(out/idlefile) as source:
            assert source.mode=='RGBA' and source.size==(256,256)
            idle=source.copy()
        images['idle'].append([idle]*16)
        assert sha(out/idlefile)==by_name[idlefile]['sha256']
        box=idle.getchannel('A').getbbox()
        assert box and 0<box[0]<box[2]<256 and 0<box[1]<box[3]<256
        checks.append({'file':idlefile,'sha256':sha(out/idlefile),'alpha_bounds':box})
        row=[]
        for index in range(16):
            path=out/f'working-d{direction:02d}-f{index:03d}.png'
            with Image.open(path) as source:
                assert source.mode=='RGBA' and source.size==(256,256)
                frame=source.copy()
            assert sha(path)==by_name[path.name]['sha256']
            box=frame.getchannel('A').getbbox()
            assert box and 0<box[0]<box[2]<256 and 0<box[1]<box[3]<256,(path.name,box)
            row.append(frame)
            checks.append({'file':path.name,'sha256':sha(path),'alpha_bounds':box})
        images['working'].append(row)
        assert len({hashlib.sha256(x.tobytes()).hexdigest() for x in row})==16
    assets={}
    for state in STATES:
        for size in (64,128,256):
            atlas=make_atlas(images[state],size)
            dest=out/f'preview-only-solar-boiler-v3-{state}-{size}.png'
            atlas.save(dest,optimize=True)
            with Image.open(dest) as check:
                assert check.size==(size*8,size*8) and check.mode=='RGBA'
            assets[dest.name]=sha(dest)
    # One 2-second true Blender capture GIF; keep consistent palette.
    frames=[]
    bg=(29,32,37,255)
    for n in range(16):
        composite=Image.new('RGBA',(4*256,256),bg)
        for d in range(4): composite.alpha_composite(images['working'][d][n],(d*256,0))
        frames.append(composite.convert('RGB'))
    mosaic=Image.new('RGB',(4*1024,4*256))
    for n,frame in enumerate(frames):
        mosaic.paste(frame,((n%4)*1024,(n//4)*256))
    palette=mosaic.quantize(colors=192)
    quantized=[frame.quantize(palette=palette,dither=Image.Dither.NONE) for frame in frames]
    gifpath=out/'working-four-directions.gif'
    quantized[0].save(gifpath,save_all=True,append_images=quantized[1:],duration=125,loop=0,disposal=2,optimize=False)
    with Image.open(gifpath) as f: assert f.n_frames==16
    assets[gifpath.name]=sha(gifpath)
    # All original 256px Cycles images; no hand drawn/icon/collage substituted.
    sheet=Image.new('RGB',(1140,1140),(27,32,37))
    draw=ImageDraw.Draw(sheet)
    font=ImageFont.load_default()
    draw.text((18,12),'SOLAR BOILER V3 | ACTUAL CYCLES ANIMATION: GAUGE + HOT ACCUMULATOR + FOUR JOINT VENTS',fill=(248,238,219),font=font)
    draw.text((18,27),'V2 parabolic optics preserved | 3x2 tile geometry | 4 directions | true 16-frame motion',fill=(184,204,217),font=font)
    for d,name in enumerate(NAMES):
        x=16+d*280
        draw.text((x+7,47),name.upper(),fill=(235,236,236),font=font)
        for row,(state,index,label) in enumerate((('idle',0,'IDLE / cold'),('working',4,'WORKING / hot'),('working',12,'WORKING / cooled'))):
            y=66+row*291
            source=images[state][d][index]
            sheet.paste(source,(x,y),source)
            draw.text((x+7,y+260),label,fill=(220,220,220),font=font)
        small=images['working'][d][4].resize((64,64),Image.Resampling.LANCZOS)
        sheet.paste(small,(x+11,947),small)
        draw.text((x+86,976),'64px readability',fill=(200,211,220),font=font)
    contact=out/'review-four-directions.png'
    sheet.save(contact,optimize=True)
    assets[contact.name]=sha(contact)
    # Controlled same-frame Cycles effect isolation. This checks real image
    # contributions rather than accepting only key names/metadata.
    contrasts={}
    for group,pair in report['isolation'].items():
        first=out/pair[0]['file'];second=out/pair[1]['file']
        for rec in pair: assert sha(out/rec['file'])==rec['sha256']
        with Image.open(first) as f, Image.open(second) as s:
            a=f.convert('RGBA');b=s.convert('RGBA')
            assert a.size==b.size==(256,256)
            contrasts[group]=actual_rgb_delta(a,b)
        assert contrasts[group]>=18,(group,contrasts[group])
    assert contrasts['heat'] >= 30 and contrasts['joint-steam'] >= 30,contrasts
    receipt={'schema':'tanks.solar-boiler.v3.animated-proof','passed':True,
       'blender_source_sha256':report['native_sha256'],'frames_per_direction':16,
       'actual_blender_views':68,'isolations_rendered':6,
       'fps':8,'loop_duration_ms':2000,'directions':list(NAMES),
       'effect_isolation_changed_rgb_pixels':contrasts,
       'preview_only_atlas_sha256':assets,'render_file_checks':checks,
       'native_reopen':True,'materials_packed':True,
       'visual_approved':False,'game_integrated':False}
    (out/'proof-qa.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print('SOLAR_V3_REAL_ANIMATED_FOUR_WAY_SPRITES_QA_PASS',len(checks),contrasts,flush=True)


if __name__=='__main__':main()
