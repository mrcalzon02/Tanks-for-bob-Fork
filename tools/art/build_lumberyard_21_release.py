#!/usr/bin/env python3
"""Promote actual accepted Steam Lumberyard V2b Blender captures into Tanks for Bob 1.8.99 / Factorio 2.1.

Reuses the already-proven 1.8.98 production package, leaves all older sources/art
unchanged, and substitutes only the growing-plot prototype, icons, and newly named art.
The 68 committed V2b frames are the source of truth; no rerender required.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import tempfile
import zipfile
from PIL import Image, ImageChops

ROOT = Path(__file__).resolve().parents[2]
BASE_VERSION = '1.8.98'
NEW_VERSION = '1.8.99'
MOD_NAME = 'tanks_for_bob_fork'
SOURCE = ROOT / 'models/island-survival/lumberyard/generated-v2b'
PREFIX = 'lumberyard-v2b'
DIRECTIONS = ('north', 'east', 'south', 'west')
FRAMES = 16
FPS = 8


def sha_bytes(data):
    return hashlib.sha256(data).hexdigest()


def sha(path):
    return sha_bytes(Path(path).read_bytes())


def assert_source(captures):
    report=json.loads((captures/'build-report.json').read_text())
    qa=json.loads((captures/'review-qa.json').read_text())
    if (report.get('revision')!='steam-lumberyard-v2b-visible-power-transmission' or
        report.get('source_frames')!=68 or report.get('camera_elevation')!=45 or
        report.get('directions')!=[0,90,180,270] or report.get('states')!={'idle':1,'working':16} or
        report.get('fps')!=8 or report.get('piston_animation_keys')!=17 or
        report.get('connecting_rod_animation_keys')!=17 or
        not report.get('wooden_drive_pulley_fixed_to_boiler_shafts') or
        not qa.get('passed') or qa.get('source_frames')!=68 or
        not qa.get('mechanical_belt_drive') or not qa.get('spinning_saw') or
        not qa.get('real_lengthwise_half_log_ejection')):
        raise RuntimeError('The user-accepted, shaft-fixed V2b animation or QA is missing')
    if sha(captures/'steam-lumberyard-v2b.blend')!=report['master_sha256']:
        raise RuntimeError('Saved native V2b source file changed')
    for pulley in ('wooden_drive_pulley','steel_flywheel','saw_pulley'):
        if max(report['shaft_mount_after_fix'][pulley])>.002:
            raise RuntimeError('Detached wandering drive pulley detected: '+pulley)
    expected={('idle',d,0) for d in range(4)}|{('working',d,f) for d in range(4) for f in range(16)}
    records={}
    for rec in report['captures']:
        key=(rec['state'],rec['direction'],rec['index'])
        if key in records:raise RuntimeError('Duplicate source frame')
        path=captures/rec['path']
        if not path.is_file() or sha(path)!=rec['sha256']:
            raise RuntimeError('Frame hash failed: '+str(path))
        records[key]=path
    if set(records)!=expected:
        raise RuntimeError('68 exact V2b frames required')
    return report,qa,{'shaft_mount_after_fix':report['shaft_mount_after_fix']},records

def crop_and_resize(source, size):
    with Image.open(source) as im:
        if im.mode != 'RGBA' or im.size != (256,256):
            raise RuntimeError('V4c frame must be 256x256 transparent RGBA')
        image = im.resize((size,size), Image.Resampling.LANCZOS)
    if image.getchannel('A').getbbox() is None or image.getchannel('A').getextrema()[0] == 255:
        raise RuntimeError('Empty or opaque Blender source')
    # Clear invisible color in final sprite cells to avoid unwanted RGB fringes.
    if image.mode != 'RGBA': raise RuntimeError('RGBA preservation failed')
    px = list(image.getdata())
    image.putdata([(r,g,b,a) if a else (0,0,0,0) for r,g,b,a in px])
    return image


def make_atlas(records, state, size):
    atlas = Image.new('RGBA',(8*size,8*size),(0,0,0,0))
    for d in range(4):
        hashes=[]
        for i in range(16):
            path = records[(state,d,0 if state=='idle' else i)]
            cell=crop_and_resize(path,size)
            hashes.append(sha_bytes(cell.tobytes()))
            x=(i%8)*size
            y=(d*2 + i//8)*size
            atlas.paste(cell,(x,y))
        if state=='idle' and len(set(hashes)) != 1:
            raise RuntimeError(f'Idle frames changed in direction {d}')
        if state=='working' and len(set(hashes)) != 16:
            raise RuntimeError(f'Animated frames duplicate in direction {d}')
    return atlas


def fourway(filename, cell, state):
    result=[]
    for d,dirn in enumerate(DIRECTIONS):
        result.append('        '+dirn+' = { filename = "__tanks_for_bob_fork__/graphics/entity/'+filename+'", priority = "high", width = '+str(cell)+', height = '+str(cell)+', x = 0, y = '+str(d*2*cell)+', frame_count = 16, line_length = 8, animation_speed = 8/60, scale = '+('0.5' if cell==256 else '1')+', shift = {0, 0} }')
    return '{\n'+',\n'.join(result)+'\n      }'


def patch_lumberyard_prototype(mod, idle, working, icon):
    file=mod/'prototypes/entity/entities.lua'
    source=file.read_text(encoding='utf-8')
    start=source.index('  --Growing plot')
    end=source.index('--quarry',start)
    section=source[start:end]
    if (section.count('name = "growing-plot"')!=1 or
        section.count('graphics_set =')!=1 or
        section.count('growing-plot-w.png')!=1):
        raise RuntimeError('Wrong target or pre-existing replacement; refusing')
    gfx_start=section.index('    graphics_set =')
    gfx_end=section.index('    crafting_categories =',gfx_start)
    gfx=('    -- User accepted Steam Lumberyard V2b: one full four-way working state.\n'
         '    graphics_set = {\n'
         '      animation = '+fourway(working,256,'working')+',\n'
         '      idle_animation = '+fourway(idle,256,'idle')+',\n'
         '      always_draw_idle_animation = false,\n'
         '      working_visualisations = {{ light = {intensity = 0.4, size = 6} }}\n'
         '    },\n\n')
    section=section[:gfx_start]+gfx+section[gfx_end:]
    old_box='collision_box = {{-2, -2}, {2, 2}}'
    if section.count(old_box)!=1:raise RuntimeError('Expected one square growing-plot collision box')
    section=section.replace(old_box,'collision_box = {{-2.0, -1.9}, {2.0, 1.9}}')
    if section.count('graphics/icons/growing-plot.png')!=1:
        raise RuntimeError('Wrong growing-plot entity icon')
    section=section.replace('graphics/icons/growing-plot.png','graphics/icons/'+icon)
    if section.count('    crafting_speed = 0.30,')!=1:
        raise RuntimeError('Unknown animation speed field')
    section=section.replace('    crafting_speed = 0.30,',
       '    crafting_speed = 0.30,\n    match_animation_speed_to_activity = false,')
    file.write_text(source[:start]+section+source[end:],encoding='utf-8')
    for name in ('prototypes/item/item.lua','prototypes/technology/technology.lua'):
        file=mod/name
        source=file.read_text(encoding='utf-8')
        position=source.index('name = "growing-plot"')
        start=source.rfind('{',0,position)
        end=source.index('}',position)+1
        fragment=source[start:end]
        if fragment.count('graphics/icons/growing-plot.png')!=1:
            raise RuntimeError('Unrecognized growing-plot icon in '+name)
        fragment=fragment.replace('graphics/icons/growing-plot.png','graphics/icons/'+icon)
        file.write_text(source[:start]+fragment+source[end:],encoding='utf-8')
    return []

def archive_mod(src,dest):
    if dest.exists():raise FileExistsError('Release already exists, refusing overwrite')
    with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for path in sorted(src.rglob('*')):
            if path.is_file():z.write(path,path.relative_to(src.parent).as_posix())
    with zipfile.ZipFile(dest) as z:
        if z.testzip() is not None:raise RuntimeError('Corrupt release archive')
        root=f'{MOD_NAME}_{NEW_VERSION}/'
        metadata=json.loads(z.read(root+'info.json'))
        if metadata.get('version')!=NEW_VERSION or metadata.get('factorio_version')!='2.1':
            raise RuntimeError('Wrong metadata')
        for state in ('working','idle'):
            path=root+'graphics/entity/'+PREFIX+'-'+state+'.png'
            if path not in z.namelist():raise RuntimeError('Missing live '+state+' atlas')
        entity=z.read(root+'prototypes/entity/entities.lua').decode()
        lumber=entity[entity.index('  --Growing plot'):entity.index('--quarry')]
        if (lumber.count(PREFIX+'-working.png')!=4 or
            lumber.count(PREFIX+'-idle.png')!=4 or
            'growing-plot-w.png' in lumber or
            'always_draw_idle_animation = false' not in lumber or
            'match_animation_speed_to_activity = false' not in lumber):
            raise RuntimeError('Wrong four-direction growing-plot attachment')
        for path in ('prototypes/item/item.lua','prototypes/technology/technology.lua'):
            s=z.read(root+path).decode()
            idx=s.index('name = "growing-plot"')
            if PREFIX+'.png' not in s[idx:idx+300]:raise RuntimeError('Missing corresponding icon')
        if not all(x in entity for x in
                   ('campfire-v12-burning.png','clay-pit-v4c-working.png',
                    'pit-kiln-v6-burning-128.png')):
            raise RuntimeError('Prior accepted artwork lost')
        return len(z.namelist())

def run(base_zip, captures, out):
    if base_zip.name != f'{MOD_NAME}_{BASE_VERSION}.zip':
        raise RuntimeError('Expected verified previous 1.8.96 full release archive')
    report,qa,motion,records=assert_source(captures)
    if not out.exists(): out.mkdir(parents=True)
    package=out/f'{MOD_NAME}_{NEW_VERSION}.zip'
    if package.exists(): raise FileExistsError('Refusing to overwrite 1.8.97 output')
    with tempfile.TemporaryDirectory(prefix='lumberyard-v2b-package-') as directory:
        working_dir=Path(directory)
        with zipfile.ZipFile(base_zip) as z:
            if z.testzip() is not None: raise RuntimeError('Base Factorio release ZIP failed CRC')
            # Keep expected directory structure and ensure paths cannot escape extraction.
            base_root=f'{MOD_NAME}_{BASE_VERSION}/'
            for member in z.infolist():
                if not member.filename.startswith(base_root): raise RuntimeError('Unexpected base archive path')
                target=(working_dir/member.filename).resolve()
                if not target.is_relative_to(working_dir.resolve()): raise RuntimeError('Unsafe archive path')
            z.extractall(working_dir)
        old=working_dir/f'{MOD_NAME}_{BASE_VERSION}'
        mod=working_dir/f'{MOD_NAME}_{NEW_VERSION}'
        old.rename(mod)
        meta=mod/'info.json'
        info=json.loads(meta.read_text(encoding='utf-8'))
        if info.get('version')!=BASE_VERSION or info.get('factorio_version')!='2.1':
            raise RuntimeError('Previous mod base is not 1.8.96 Factorio 2.1')
        info['version']=NEW_VERSION
        meta.write_text(json.dumps(info,indent=2)+'\n',encoding='utf-8')
        graphics=mod/'graphics/entity'
        icons=mod/'graphics/icons'
        graphics.mkdir(parents=True,exist_ok=True)
        icons.mkdir(parents=True,exist_ok=True)
        outputs={}
        for state in ('idle','working'):
            for size in (64,128,256):
                name=f'{PREFIX}-{state}'+('' if size==256 else '-'+str(size))+'.png'
                path=graphics/name
                if path.exists(): raise RuntimeError('Versioned lumberyard artwork already exists: '+name)
                atlas=make_atlas(records,state,size)
                atlas.save(path)
                with Image.open(path) as image:
                    if image.size!=(8*size,8*size) or image.mode!='RGBA' or ImageChops.difference(image,atlas).getbbox():
                        raise RuntimeError('Atlas save mismatch')
                outputs['graphics/entity/'+name]=sha(path)
        icon=f'{PREFIX}.png'
        with Image.open(records[('idle',0,0)]) as src:
            src.resize((64,64),Image.Resampling.LANCZOS).save(icons/icon)
        outputs['graphics/icons/'+icon]=sha(icons/icon)
        patch_lumberyard_prototype(mod,f'{PREFIX}-idle.png',f'{PREFIX}-working.png',icon)
        count=archive_mod(mod,package)
    digest=sha(package)
    (out/(package.name+'.sha256')).write_text(f'{digest}  {package.name}\n')
    receipt={'schema':1,'version':NEW_VERSION,'factorio_version':'2.1','package':package.name,
             'sha256':digest,'file_count':count,'source_revision':report['revision'],
             'capture_frame_count':qa['source_frames'],'frame_count_per_direction':FRAMES,
             'directions':list(DIRECTIONS),'camera_elevation':45,
             'shaft_mount_after_fix':motion['shaft_mount_after_fix'],'pulley_alignment_verified':True,
             'new_art_hashes':outputs,'base_version':BASE_VERSION,'original_2_0_source_untouched':True,'previous_art_preserved':True,
             'runtime_proven':False}
    (out/'lumberyard-v2b-release-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print('STEAM_LUMBERYARD_V2B_21_BUILD_OK '+json.dumps(receipt,sort_keys=True),flush=True)
    return receipt


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--base',required=True,type=Path,help='Full verified 1.8.96 Factorio mod archive')
    p.add_argument('--capture',type=Path,default=SOURCE)
    p.add_argument('--output',required=True,type=Path)
    a=p.parse_args()
    run(a.base.resolve(),a.capture.resolve(),a.output.resolve())

if __name__=='__main__': main()
