"""Assemble unaltered Blender captures into review sheets and a loop preview."""
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'output'
RENDERS=OUT/'renders'
BG=(28,33,38)
FG=(233,236,239)
SUB=(177,187,197)
font_file='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
def font(size):
    return ImageFont.truetype(font_file,size)

def place(canvas,name,xy):
    image=Image.open(RENDERS/(name+'.png')).convert('RGBA')
    canvas.paste(image,xy,image)

comparison=Image.new('RGB',(832,492),BG)
d=ImageDraw.Draw(comparison)
d.text((28,19),'Accepted Campfire V12',font=font(21),fill=FG)
d.text((444,19),'Cooking Fire V1',font=font(21),fill=FG)
place(comparison,'source-campfire',(16,60))
place(comparison,'working-north',(432,60))
d.text((28,453),'Same stonework, logs, embers and fire animation',font=font(17),fill=SUB)
comparison.save(OUT/'review-comparison.png',optimize=True)

sheet=Image.new('RGB',(832,940),BG)
d=ImageDraw.Draw(sheet)
d.text((24,20),'Cooking Fire V1 | four directions',font=font(24),fill=FG)
d.text((24,54),'Real Blender captures at the inherited 45-degree angle',font=font(17),fill=SUB)
for i,name in enumerate(('north','east','south','west')):
    x=16+(i%2)*416
    y=92+(i//2)*416
    place(sheet,'working-'+name,(x,y))
    d.text((x+15,y+379),name.capitalize(),font=font(18),fill=FG)
sheet.save(OUT/'review-four-directions.png',optimize=True)

frames=[]
for i in range(16):
    image=Image.open(RENDERS/f'loop-{i:02d}.png').convert('RGBA')
    canvas=Image.new('RGBA',image.size,(*BG,255))
    canvas.alpha_composite(image)
    frames.append(canvas.convert('RGB'))
palette=Image.new('RGB',(384*4,384*4))
for i,frame in enumerate(frames):
    palette.paste(frame,((i%4)*384,(i//4)*384))
palette=palette.quantize(colors=256)
quantized=[f.quantize(palette=palette,dither=Image.Dither.NONE) for f in frames]
quantized[0].save(OUT/'working-preview.gif',save_all=True,append_images=quantized[1:],duration=125,loop=0,disposal=2,optimize=False)

checks=[]
for image_file in sorted(RENDERS.glob('*.png')):
    with Image.open(image_file) as im:
        im.load()
        assert im.size==(384,384)
        assert im.mode=='RGBA'
        box=im.getchannel('A').getbbox()
        assert box and box[0]>1 and box[1]>1 and box[2]<383 and box[3]<383, (image_file.name,box)
        checks.append({'file':image_file.name,'alpha_bounds':box})
with Image.open(OUT/'working-preview.gif') as gif:
    assert gif.n_frames==16
report=json.loads((OUT/'build-report.json').read_text())
report['review_capture_checks']={'decoded_frames':len(checks),'frame_size':[384,384],'transparent_rgba':True,'all_frames_have_margin':True,'gif_frames':16,'gif_fps':8,'frames':checks}
(OUT/'build-report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'captures':len(checks),'gif_frames':16,'source_meshes_unchanged':report['source_meshes_unchanged'],'native_reopen':report['native_reopen']}))
