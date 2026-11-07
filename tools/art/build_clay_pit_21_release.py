#!/usr/bin/env python3
"""Promote actual Clay Pit V4c Blender captures into Tanks for Bob 1.8.97 / Factorio 2.1.

Reuses the already-proven 1.8.96 production package, leaves all older sources/art
unchanged, and substitutes only the clay-pit prototype, icons, and newly named art.
The 68 committed V4c frames are the source of truth; no rerender required.
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
BASE_VERSION = '1.8.96'
NEW_VERSION = '1.8.97'
MOD_NAME = 'tanks_for_bob_fork'
SOURCE = ROOT / 'models/island-survival/clay-pit/generated-v4c'
PREFIX = 'clay-pit-v4c'
DIRECTIONS = ('north', 'east', 'south', 'west')
FRAMES = 16
FPS = 8


def sha_bytes(data):
    return hashlib.sha256(data).hexdigest()


def sha(path):
    return sha_bytes(Path(path).read_bytes())


def assert_source(captures):
    report = json.loads((captures/'build-report.json').read_text())
    qa = json.loads((captures/'review-qa.json').read_text())
    motion = json.loads((captures/'bucket-motion-qa.json').read_text())
    if (report.get('revision') != 'v4c-readable-bucket-swing' or
        report.get('actual_frame_count') != 68 or report.get('camera_pitch_deg') != 45 or
        report.get('directions') != [0,90,180,270] or
        report.get('frames') != list(range(1, 92, 6)) or
        report.get('fps') != 8 or report.get('swing_degrees') != [-15,15] or
        not qa.get('passed') or qa.get('capture_count') != 68 or
        not motion.get('passed') or len(motion.get('directions',{})) != 4 or
        min(r['travel_px_256'] for r in motion['directions'].values()) < 14.0):
        raise RuntimeError('Clay Pit V4c source/animation gate failed: do not publish a different model')
    expected = {('idle',d,0) for d in range(4)} | {('working',d,f) for d in range(4) for f in range(16)}
    records = {}
    for rec in report['captures']:
        key = (rec['state'],rec['angle']//90,rec['index'])
        if key in records: raise RuntimeError(f'Duplicate source frame {key}')
        file = captures / rec['path']
        if not file.is_file() or sha(file) != rec['sha256']:
            raise RuntimeError(f'Clay source checksum mismatch: {file}')
        records[key] = file
    if set(records) != expected:
        raise RuntimeError('All 68 V4c Blender frames are required')
    return report, qa, motion, records


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
        result.append('        '+dirn+' = { filename = "__tanks_for_bob_fork__/graphics/entity/'+filename+'", priority = "high", width = '+str(cell)+', height = '+str(cell)+', x = 0, y = '+str(d*2*cell)+', frame_count = 16, line_length = 8, animation_speed = 8/60, scale = '+('0.5' if cell==128 else '1')+', shift = {0, 0} }')
    return '{\n'+',\n'.join(result)+'\n      }'


def patch_clay_prototype(mod, idle, working, icon):
    file=mod/'prototypes/entity/entities.lua'
    source=file.read_text(encoding='utf-8')
    start=source.index('  --claypit')
    end=source.index('--pit-kiln',start)
    section=source[start:end]
    if section.count('name = "clay-pit"') != 1 or section.count('graphics_set =') != 1 or 'clay-pit-w.png' not in section:
        raise RuntimeError('Ambiguous clay pit definition; refusing to replace unrelated graphics')
    gfx_start=section.index('    graphics_set =')
    gfx_end=section.index('    crafting_categories =',gfx_start)
    gfx='''    -- V4c source: four complete directional states; no doubled base/overlay.\n    graphics_set = {\n      animation = '''+fourway(working,128,'working')+''',\n      idle_animation = '''+fourway(idle,128,'idle')+''',\n      always_draw_idle_animation = false,\n      working_visualisations = {{ light = {intensity = 0.3, size = 3} }}\n    },\n\n'''
    section=section[:gfx_start]+gfx+section[gfx_end:]
    old_box='collision_box = {{-1.2, -1.2}, {1.2, 1.2}}'
    new_box='collision_box = {{-1.2, -1.1}, {1.2, 1.1}}'
    if section.count(old_box)!=1: raise RuntimeError('Clay pit collision box must match old source')
    section=section.replace(old_box,new_box,1)
    if section.count('icon = "__tanks_for_bob_fork__/graphics/icons/clay-pit.png"') != 1:
        raise RuntimeError('Cannot locate clay pit entity icon')
    section=section.replace('graphics/icons/clay-pit.png','graphics/icons/'+icon,1)
    if 'match_animation_speed_to_activity' not in section:
        section=section.replace('    crafting_speed = 0.30,','    crafting_speed = 0.30,\n    match_animation_speed_to_activity = false,',1)
    file.write_text(source[:start]+section+source[end:],encoding='utf-8')
    item=mod/'prototypes/item/item.lua'
    items=item.read_text(encoding='utf-8')
    a=items.index('name = "clay-pit"')
    lo=items.rfind('{',0,a)
    hi=items.index('}',a)+1
    fragment=items[lo:hi]
    if fragment.count('graphics/icons/clay-pit.png')!=1:
        raise RuntimeError('Missing exact clay pit item icon')
    items=items[:lo]+fragment.replace('graphics/icons/clay-pit.png','graphics/icons/'+icon)+items[hi:]
    item.write_text(items,encoding='utf-8')
    tech=mod/'prototypes/technology/technology.lua'
    technologies=tech.read_text(encoding='utf-8')
    at=technologies.index('name = "clay-pit"')
    before=technologies.rfind('{',0,at)
    after=technologies.index('}',at)+1
    one=technologies[before:after]
    if one.count('graphics/icons/clay-pit.png')!=1:
        raise RuntimeError('Missing exact clay pit technology icon')
    technologies=technologies[:before]+one.replace('graphics/icons/clay-pit.png','graphics/icons/'+icon)+technologies[after:]
    tech.write_text(technologies,encoding='utf-8')
    # Preserve ingredient/pipe connections and burner mechanics literally.
    return [file,item,tech]


def archive_mod(src, dest):
    if dest.exists(): raise FileExistsError(f'Refusing package overwrite: {dest}')
    with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as out:
        for path in sorted(src.rglob('*')):
            if path.is_file(): out.write(path,path.relative_to(src.parent).as_posix())
    with zipfile.ZipFile(dest) as z:
        if z.testzip() is not None: raise RuntimeError('Produced corrupt Factorio ZIP')
        root=f'{MOD_NAME}_{NEW_VERSION}/'
        metadata=json.loads(z.read(root+'info.json'))
        if (metadata.get('version')!=NEW_VERSION or metadata.get('factorio_version')!='2.1' or
            'base >= 2.1' not in metadata.get('dependencies',[])):
            raise RuntimeError('Wrong version metadata in release package')
        for name in (f'graphics/entity/{PREFIX}-working.png',f'graphics/entity/{PREFIX}-idle.png',
                     f'graphics/icons/{PREFIX}.png'):
            if root+name not in z.namelist(): raise RuntimeError(f'Missing actual installed {name}')
        entity=z.read(root+'prototypes/entity/entities.lua').decode('utf-8')
        clay=entity[entity.index('  --claypit'):entity.index('--pit-kiln')]
        if (clay.count(PREFIX+'-working.png')!=4 or clay.count(PREFIX+'-idle.png')!=4 or
            'always_draw_idle_animation = false' not in clay):
            raise RuntimeError('Released prototype does not reference every direction')
        return len(z.namelist())


def run(base_zip, captures, out):
    if base_zip.name != f'{MOD_NAME}_{BASE_VERSION}.zip':
        raise RuntimeError('Expected verified previous 1.8.96 full release archive')
    report,qa,motion,records=assert_source(captures)
    if not out.exists(): out.mkdir(parents=True)
    package=out/f'{MOD_NAME}_{NEW_VERSION}.zip'
    if package.exists(): raise FileExistsError('Refusing to overwrite 1.8.97 output')
    with tempfile.TemporaryDirectory(prefix='clay-v4c-package-') as directory:
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
            for size in (64,128):
                name=f'{PREFIX}-{state}'+('' if size==128 else '-64')+'.png'
                path=graphics/name
                if path.exists(): raise RuntimeError('Versioned clay artwork already exists: '+name)
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
        patch_clay_prototype(mod,f'{PREFIX}-idle.png',f'{PREFIX}-working.png',icon)
        count=archive_mod(mod,package)
    digest=sha(package)
    (out/(package.name+'.sha256')).write_text(f'{digest}  {package.name}\n')
    receipt={'schema':1,'version':NEW_VERSION,'factorio_version':'2.1','package':package.name,
             'sha256':digest,'file_count':count,'source_revision':report['revision'],
             'capture_frame_count':qa['capture_count'],'frame_count_per_direction':FRAMES,
             'directions':list(DIRECTIONS),'camera_elevation':45,
             'bucket_motion_64px':{k:v['travel_px_64'] for k,v in motion['directions'].items()},
             'new_art_hashes':outputs,'base_version':BASE_VERSION,'original_2_0_source_untouched':True,
             'runtime_proven':False}
    (out/'clay-v4c-promotion-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print('CLAY_PIT_V4C_2_1_BUILD_OK '+json.dumps(receipt,sort_keys=True),flush=True)
    return receipt


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--base',required=True,type=Path,help='Full verified 1.8.96 Factorio mod archive')
    p.add_argument('--capture',type=Path,default=SOURCE)
    p.add_argument('--output',required=True,type=Path)
    a=p.parse_args()
    run(a.base.resolve(),a.capture.resolve(),a.output.resolve())

if __name__=='__main__': main()
