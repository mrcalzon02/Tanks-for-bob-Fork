#!/usr/bin/env python3
"""Native-render four-way Fish Pond V1 QA and 64px contact proof."""
from PIL import Image,ImageChops,ImageDraw,ImageFont
from pathlib import Path
import hashlib,json,sys
out=Path(sys.argv[1]).resolve()
names=('north','east','south','west')
images={}
checks=[]
for i, direction in enumerate(names):
    for state,filename in (('idle',f'idle-d{i:02d}.png'),
                           ('working',f'working-d{i:02d}-f004.png')):
        path=out/filename
        with Image.open(path) as original:
            assert original.mode=='RGBA' and original.size==(256,256),filename
            im=original.copy()
            bounds=im.getchannel('A').getbbox()
            assert bounds and bounds[0]>0 and bounds[1]>0 and bounds[2]<256 and bounds[3]<256,(filename,bounds)
            images[state,i]=im
            checks.append({'file':filename,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'alpha_bounds':bounds})
    assert ImageChops.difference(images['idle',i].convert('RGB'),images['working',i].convert('RGB')).getbbox() is not None, direction
canvas=Image.new('RGB',(1108,780),(27,32,37))
draw=ImageDraw.Draw(canvas)
font=ImageFont.load_default()
draw.text((20,10),'FISH POND V1 - BLENDER PROOF - CANDIDATE, NOT APPROVED',fill='white',font=font)
for i,direction in enumerate(names):
    x=20+i*270
    draw.text((x+6,37),direction.upper(),fill=(240,240,240),font=font)
    for row,state in enumerate(('idle','working')):
        y=60+row*279
        im=images[state,i]
        canvas.paste(im,(x,y),im)
        draw.text((x+6,y+260),state.upper(),fill=(210,210,210),font=font)
    small=images['working',i].resize((64,64),Image.Resampling.LANCZOS)
    canvas.paste(small,(x+16,633),small)
    draw.text((x+90,654),'64px proof',fill=(210,210,210),font=font)
canvas.save(out/'review-four-directions.png',optimize=True)
report=json.loads((out/'build-report.json').read_text())
assert report['fish_count']==4 and report['tail_stroke_keys_per_fish']==17
assert report['game_integration'] is False and report['visual_approved'] is False
assert len(report['renders'])==8
receipt={'schema':1,'passed':True,'actual_blender_renders':len(checks),
         'native_model':report['master_sha256'],'donor_sha256':report['source_sha256'],
         'visual_approved':False,'game_integrated':False,
         'four_directions':list(names),'images':checks,
         'contact_sha256':hashlib.sha256((out/'review-four-directions.png').read_bytes()).hexdigest()}
(out/'proof-qa.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('FISH_POND_V1_CARDINAL_PROOF_QA_PASS',receipt['actual_blender_renders'])
