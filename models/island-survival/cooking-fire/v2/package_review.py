"""Package actual V2 Blender renders into compact review sheets and animation."""
import json
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'output'
RENDERS=OUT/'renders'
BG=(28,33,38);FG=(234,237,239);SUB=(178,187,196)
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
def font(size):return ImageFont.truetype(FONT,size)
def place(canvas,name,xy):
    im=Image.open(RENDERS/(name+'.png')).convert('RGBA')
    canvas.paste(im,xy,im)

hero=Image.new('RGB',(560,612),BG)
d=ImageDraw.Draw(hero)
d.text((24,18),'Cooking Fire V2',font=font(24),fill=FG)
d.text((24,51),'Pump box + hand and accordion bellows',font=font(18),fill=SUB)
place(hero,'hero',(24,83))
hero.save(OUT/'review-hero.png',optimize=True)

for prefix,title,subtitle,destination in [
    ('working-','Cooking Fire V2 | four directions','Wood and leather bellows, full-size rear fluid mount','review-four-directions.png'),
    ('pipe-fit-','Cooking Fire V2 | adjacent pipe fit','Same barrel, bore, collar and centerline as the boiler reference','review-pipe-fit.png')]:
    sheet=Image.new('RGB',(1080,1216),BG);d=ImageDraw.Draw(sheet)
    d.text((24,17),title,font=font(27),fill=FG)
    d.text((24,56),subtitle,font=font(18),fill=SUB)
    for i,name in enumerate(('north','east','south','west')):
        x=14+(i%2)*540;y=93+(i//2)*550
        place(sheet,prefix+name,(x,y))
        d.text((x+15,y+506),name.capitalize(),font=font(19),fill=FG)
    if prefix=='pipe-fit-':
        d.text((24,1184),'3D reference-pipe fit; native game sprite registration is a separate step.',font=font(17),fill=SUB)
    sheet.save(OUT/destination,optimize=True)

sheet=Image.new('RGB',(1080,636),BG);d=ImageDraw.Draw(sheet)
d.text((24,17),'Bellows motion | open and squeezed',font=font(27),fill=FG)
d.text((24,56),'Boards, caps and leather deform together',font=font(18),fill=SUB)
for i,(name,label) in enumerate([('bellows-open','Open'),('bellows-compressed','Squeezed')]):
    x=14+i*540
    place(sheet,name,(x,92))
    d.text((x+15,598),label,font=font(19),fill=FG)
sheet.save(OUT/'review-bellows-poses.png',optimize=True)

frames=[]
for i in range(16):
    im=Image.open(RENDERS/f'loop-{i:02d}.png').convert('RGBA')
    background=Image.new('RGBA',im.size,(*BG,255));background.alpha_composite(im)
    frames.append(background.convert('RGB'))
palette=Image.new('RGB',(2048,2048))
for i,frame in enumerate(frames):palette.paste(frame,((i%4)*512,(i//4)*512))
palette=palette.quantize(colors=256)
quantized=[f.quantize(palette=palette,dither=Image.Dither.NONE) for f in frames]
quantized[0].save(OUT/'working-preview.gif',save_all=True,append_images=quantized[1:],duration=125,loop=0,disposal=2,optimize=False)

checks=[]
for p in sorted(RENDERS.glob('*.png')):
    with Image.open(p) as im:
        im.load()
        assert im.size==(512,512) and im.mode=='RGBA'
        bb=im.getchannel('A').getbbox()
        assert bb and bb[0]>1 and bb[1]>1 and bb[2]<511 and bb[3]<511,(p.name,bb)
        checks.append({'file':p.name,'alpha_bounds':bb})
with Image.open(OUT/'working-preview.gif') as gif:assert gif.n_frames==16
report=json.loads((OUT/'build-report.json').read_text())
report['capture_checks']={'decoded_pngs':len(checks),'rgba_size':[512,512],'all_frames_have_margin':True,'gif_frames':16,'gif_fps':8,'frames':checks}
(OUT/'build-report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'pngs':len(checks),'gif_frames':16,'preserved_v1_objects':report['preserved_v1_objects'],'mating_error':report['pipe_interface']['max_mating_error']}))
