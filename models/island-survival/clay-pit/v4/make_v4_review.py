#!/usr/bin/env python3
"""Verify the actual 68 Blender frames and display game-vs-new four-way evidence."""
from PIL import Image, ImageDraw, ImageFont, ImageChops
from pathlib import Path
import argparse, json, hashlib

def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--mod',type=Path,required=True)
    ap.add_argument('--previous',type=Path,required=True)
    opts=ap.parse_args()
    out=opts.out
    data=json.loads((out/'build-report.json').read_text())
    if (data.get('actual_frame_count')!=68 or len(data['captures'])!=68 or
        data['directions']!=[0,90,180,270] or len(data['frames'])!=16 or
        data['camera_pitch_deg']!=45):
        raise ValueError('Incomplete actual Blender four-way capture')
    captures={}
    for record in data['captures']:
        path=out/record['path']
        if digest(path)!=record['sha256']:
            raise ValueError(f'Capture hash mismatch: {path}')
        with Image.open(path) as image:
            if image.mode!='RGBA' or image.size!=(256,256):
                raise ValueError('Non-RGBA or wrong-sized render')
            copy=image.copy()
        bound=copy.getchannel('A').point(lambda a:255 if a>4 else 0).getbbox()
        if not bound or bound[0]<2 or bound[1]<2 or bound[2]>254 or bound[3]>254:
            raise ValueError(f'Clipping/empty sprite: {path}')
        key=(record['state'],record['angle'],record['index'])
        if key in captures: raise ValueError('Duplicate capture')
        captures[key]=copy
    if len(captures)!=68:raise ValueError('Missing actual rendered frames')
    gifs=[]
    for d in range(4):
        stills=[captures['working',d*90,i] for i in range(16)]
        if len({hashlib.sha256(s.tobytes()).hexdigest() for s in stills})<13:
            raise ValueError(f'Animation not distinct in direction {d}')
        if not ImageChops.difference(stills[0].convert('RGB'),stills[8].convert('RGB')).getbbox():
            raise ValueError('Pendulum motion not visible')
        framed=[]
        for still in stills:
            bg=Image.new('RGBA',(256,256),(45,48,52,255))
            bg.alpha_composite(still)
            framed.append(bg.convert('RGB'))
        gif=out/f'working-d{d:02d}-preview.gif'
        framed[0].save(gif,save_all=True,append_images=framed[1:],
                       duration=125,loop=0,disposal=2,optimize=False)
        with Image.open(gif) as check:
            if check.n_frames!=16:raise ValueError('GIF collapsed')
        gifs.append(gif)
    if len({digest(out/f'idle-d{i:02d}.png') for i in range(4)})!=4:
        raise ValueError('Cardinal model rotations did not differ')
    old=Image.open(opts.previous).convert('RGBA')
    if old.size!=(256,256) or not ImageChops.difference(old.convert('RGB'),captures['idle',0,0].convert('RGB')).getbbox():
        raise ValueError('Wet-clay material unchanged since V3')
    source=Image.open(opts.mod/'graphics/entity/clay-pit.png').convert('RGBA').crop((0,0,64,64))
    source.save(out/'source-idle-64.png')
    overlay=Image.open(opts.mod/'graphics/entity/clay-pit-w.png').convert('RGBA')
    Image.alpha_composite(source,overlay).save(out/'source-working-64.png')
    try:
        font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',16)
    except OSError:
        font=ImageFont.load_default()
    board=Image.new('RGB',(4*264+16,2*287+50),(26,29,33))
    draw=ImageDraw.Draw(board)
    draw.text((10,12),'CLAY PIT V4 | real Blender captures | not accepted art',font=font,fill='white')
    for row,state in enumerate(('idle','working')):
        for d in range(4):
            image=captures[state,d*90,0 if state=='idle' else 2]
            plate=Image.new('RGBA',(256,256),(47,49,53,255))
            plate.alpha_composite(image)
            x,y=8+264*d,45+287*row
            board.paste(plate.convert('RGB'),(x,y))
            draw.text((x+5,y+260),f'{state} / {d*90} deg',font=font,fill='white')
    board.save(out/'v4-four-direction-proof.png')
    compare=Image.new('RGB',(4*263+12,338),(26,29,33))
    dr=ImageDraw.Draw(compare)
    dr.text((8,10),'GAME  |  V3  |  V4  |  V4 WORKING',font=font,fill='white')
    for i,img in enumerate((source,old,captures['idle',0,0],captures['working',0,2])):
        frame=img if img.size==(64,64) else img.resize((64,64),Image.Resampling.LANCZOS)
        plate=Image.new('RGBA',(64,64),(47,49,53,255))
        plate.alpha_composite(frame)
        compare.paste(plate.resize((256,256),Image.Resampling.NEAREST).convert('RGB'),(4+263*i,42))
    compare.save(out/'v4-game-v3-comparison.png')
    if not (out/'clay-pit-v4.blend').is_file():raise ValueError('Editable .blend missing')
    qa={'passed':True,'capture_count':68,'animated_per_direction':16,
        'gifs':{p.name:digest(p) for p in gifs},
        'visual_approved':False,'game_tested':False}
    (out/'review-qa.json').write_text(json.dumps(qa,indent=2)+'\n')
    print('CLAY_PIT_V4_68_REAL_FRAMES_QA_PASS',flush=True)
if __name__=='__main__':main()
