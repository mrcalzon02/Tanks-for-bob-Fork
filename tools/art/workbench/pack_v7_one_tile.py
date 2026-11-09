#!/usr/bin/env python3
"""Losslessly pack approved V7 Blender frames for a one-tile graphical workbench.

Input: ZIP of the already completed OLD-CORE30 V7 rendered-frame artifact.
Outputs: four 96-cell 128px RGBA sheets, four idle 128px RGBA cells, an
independently measured footprint manifest, and exact cell readback receipts.

This does not regenerate geometry, adjust workbench animation, or alter Lua.
The game sprite scale and shift are metadata, so no source pixel resampling occurs.
"""
import argparse, hashlib, io, json, zipfile
from pathlib import Path
from PIL import Image, ImageChops

ORDER = ('north','east','south','west')
FRAMES = tuple(range(2,193,2))
SCALE = 0.33
SHIFT = (0.0,-0.07)
TILE_PX = 32
CELL_PX = 128
COLUMNS = 12
ROWS = 8


def sha(b):
    if not isinstance(b,bytes):b=Path(b).read_bytes()
    return hashlib.sha256(b).hexdigest()


def box(im):
    return im.getchannel('A').point(lambda p:255 if p>20 else 0).getbbox()


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--input-zip',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args()
    args.out.mkdir(parents=True,exist_ok=True)
    manifest={
        'schema':'workbench-one-tile-v8', 'source':'original corrected workbench V7 real OLD-CORE30 Blender animation frames',
        'source_archive_sha256':sha(args.input_zip),'tile_size_pixels':TILE_PX,
        'scale':SCALE,'shift':list(SHIFT),'frame_cell_px':[128,128],
        'frame_count':len(FRAMES),'line_length':COLUMNS,'fps':12,'animation_speed':0.2,
        'directions':ORDER,'graphics_only':True,'working_animation_source_unchanged':True,
        'footprint_tiles':[1,1],'per_direction':{}
    }
    with zipfile.ZipFile(args.input_zip) as z:
        src=json.loads(z.read('render-manifest.json'))
        validation=json.loads(z.read('reopen-validation.json'))
        assert src['width']==src['height']==CELL_PX and src['frames']==96 and src['columns']==12
        assert src['directions']==list(ORDER)
        assert validation['rest_loop_exact'] and validation['fully_cold_at_end']
        assert validation['all_192_frames_clear_sheet']
        assert src['timeline_frames']==list(FRAMES)
        manifest['blender_source_sha256']=src['source_sha256']
        manifest['blender_version']=src['blender']
        manifest['impact_frames']=validation['impact_frames']
        for direction in ORDER:
            atlas=Image.new('RGBA',(COLUMNS*CELL_PX,ROWS*CELL_PX),(0,0,0,0))
            cells=[]
            all_boxes=[]
            for index,frame in enumerate(FRAMES):
                image=Image.open(io.BytesIO(z.read(f'frames/{direction}/{frame:04d}.png'))).convert('RGBA')
                assert image.size==(CELL_PX,CELL_PX)
                assert image.getchannel('A').getextrema()[1]>0
                atlas.paste(image,((index%COLUMNS)*CELL_PX,(index//COLUMNS)*CELL_PX))
                bb=box(image)
                all_boxes.append(bb)
                cells.append(sha(image.tobytes()))
            fname=f'working-{direction}.png'
            atlas.save(args.out/fname,optimize=True,compress_level=9)
            replay=Image.open(args.out/fname).convert('RGBA')
            for index,recorded in enumerate(cells):
                cropped=replay.crop(((index%COLUMNS)*CELL_PX,(index//COLUMNS)*CELL_PX,
                                     ((index%COLUMNS)+1)*CELL_PX,((index//COLUMNS)+1)*CELL_PX))
                assert sha(cropped.tobytes())==recorded, (direction,index,'unpacked cell differs')
            idle=Image.open(io.BytesIO(z.read(f'frames/{direction}/0002.png'))).convert('RGBA')
            idle.save(args.out/f'idle-{direction}.png', optimize=True)
            w,h=(all_boxes[0][2]-all_boxes[0][0],all_boxes[0][3]-all_boxes[0][1])
            pw,ph=(w*SCALE,h*SCALE)
            assert pw<=TILE_PX and ph<=TILE_PX,(direction,'resting sprite exceeds one tile',pw,ph)
            extrema=[(min(b[0] for b in all_boxes),min(b[1] for b in all_boxes),
                      max(b[2] for b in all_boxes),max(b[3] for b in all_boxes))]
            manifest['per_direction'][direction]={
                'rest_alpha_bbox':list(all_boxes[0]), 'rest_width_game_px':round(pw,3),
                'rest_height_game_px':round(ph,3),'rest_width_tiles':round(pw/TILE_PX,4),
                'rest_height_tiles':round(ph/TILE_PX,4),'animated_alpha_union':list(extrema[0]),
                'rest_frame_sha256':sha(z.read(f'frames/{direction}/0002.png')),
                'working_atlas_sha256':sha(args.out/fname),
                'idle_png_sha256':sha(args.out/f'idle-{direction}.png'),
                'cell_readback_count':96
            }
    (args.out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print('ONE_TILE_TEST_PASS: 4 dirs x 96 frames, 8 PNGs, all exact cell readbacks; idle <=1 tile')
    print('WORKBENCH_DISPLAY:',SCALE,SHIFT)


if __name__=='__main__':main()
