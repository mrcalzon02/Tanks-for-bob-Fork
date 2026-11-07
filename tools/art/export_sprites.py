#!/usr/bin/env python3
"""One command: authored Blender model -> fixed RGBA frames -> verified sprite atlases.

Requires Blender 4.3+ and Pillow. No game installation or external add-on required.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import subprocess
import sys

from PIL import Image, ImageChops, ImageDraw


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_config(cfg):
    if cfg.get('schema') != 1:
        raise ValueError('Unknown config schema')
    for field in ('source_size', 'samples', 'columns', 'fps'):
        if type(cfg[field]) is not int or cfg[field] <= 0:
            raise ValueError(f'{field} must be a positive integer')
    if not cfg['sizes'] or any(type(s) is not int or s <= 0 or s > cfg['source_size'] for s in cfg['sizes']):
        raise ValueError('sizes must be positive integers no larger than source_size')
    if not cfg['directions'] or len(set(cfg['directions'])) != len(cfg['directions']):
        raise ValueError('Provide unique direction angles')
    if any(not isinstance(a, (int, float)) or not math.isfinite(a) for a in cfg['directions']):
        raise ValueError('Direction angles must be finite')
    if len(cfg['pivot']) != 3 or any(not math.isfinite(x) for x in cfg['pivot']):
        raise ValueError('pivot must contain three finite coordinates')
    if not cfg['states']:
        raise ValueError('At least one state required')
    for state, frames in cfg['states'].items():
        if not re.fullmatch(r'[a-zA-Z0-9_-]+', state):
            raise ValueError('Unsafe state name')
        if not frames or len(set(frames)) != len(frames) or any(type(f) is not int for f in frames):
            raise ValueError('State frames must be unique timeline integers')


def rgba(path, size):
    with Image.open(path) as image:
        if image.mode != 'RGBA' or image.size != (size, size):
            raise ValueError(f'Wrong mode/dimensions: {path}')
        result = image.copy()
    alpha = result.getchannel('A')
    if alpha.getextrema()[0] == 255 or alpha.getextrema()[1] == 0:
        raise ValueError(f'Opaque rectangle or empty frame: {path}')
    # Ignore sub-1% shadow tails, but fail on visible geometry touching the canvas.
    bounds = alpha.point(lambda value: 255 if value > 2 else 0).getbbox()
    if bounds is None or bounds[0] < 1 or bounds[1] < 1 or bounds[2] >= size or bounds[3] >= size:
        raise ValueError(f'Clipped frame: {path}: {bounds}')
    return result


def pack(out):
    manifest = json.loads((out / 'capture.json').read_text())
    cfg = manifest['config']
    validate_config(cfg)
    if digest(out / 'master.blend') != manifest['master_sha256']:
        raise ValueError('Saved master checksum mismatch')
    expected = [(state, d, i, f) for state, frames in cfg['states'].items()
                for d in range(len(cfg['directions'])) for i, f in enumerate(frames)]
    actual = [(r['state'], r['direction'], r['index'], r['timeline_frame']) for r in manifest['frames']]
    if expected != actual:
        raise ValueError('Frame count/order/timeline mismatch')
    images = {}
    for r in manifest['frames']:
        path = out / r['path']
        if digest(path) != r['sha256']:
            raise ValueError(f'Frame checksum mismatch: {path}')
        images[r['state'], r['direction'], r['index']] = rgba(path, cfg['source_size'])
    sheets = []
    for state, frames in cfg['states'].items():
        columns = min(cfg['columns'], len(frames))
        rows_per_direction = math.ceil(len(frames) / columns)
        for size in cfg['sizes']:
            atlas = Image.new('RGBA', (columns * size, rows_per_direction * len(cfg['directions']) * size))
            cells = []
            for d in range(len(cfg['directions'])):
                pixel_hashes = set()
                for i, frame in enumerate(frames):
                    cell = images[state, d, i].resize((size, size), Image.Resampling.LANCZOS)
                    # Zero hidden RGB, avoiding bright fringes in downstream tooling.
                    pixels = cell.get_flattened_data() if hasattr(cell, 'get_flattened_data') else cell.getdata()
                    cell.putdata([(r, g, b, a) if a else (0, 0, 0, 0) for r, g, b, a in pixels])
                    pixel_hashes.add(hashlib.sha256(cell.tobytes()).hexdigest())
                    x, y = (i % columns) * size, (d * rows_per_direction + i // columns) * size
                    atlas.paste(cell, (x, y))
                    cells.append({'direction': d, 'index': i, 'frame': frame, 'rect': [x, y, size, size]})
                if len(frames) > 1 and len(pixel_hashes) != len(frames):
                    raise ValueError(f'Duplicate animation cells: {state} direction {d} size {size}')
            target = out / f'{state}-{size}.png'
            atlas.save(target)
            # Independently reopen and extract each packed cell; no blend/paste alpha loss.
            with Image.open(target) as reopened:
                for cell in cells:
                    x, y, w, h = cell['rect']
                    reference = images[state, cell['direction'], cell['index']].resize((size, size), Image.Resampling.LANCZOS)
                    difference = ImageChops.difference(reopened.crop((x, y, x+w, y+h)), reference)
                    if difference.getchannel('A').getbbox():
                        raise ValueError('Atlas alpha roundtrip mismatch')
                    if any(channel.getbbox() for channel in difference.split()[0:3]) or difference.getchannel('A').getbbox():
                        # Hidden RGB was intentionally cleared; compare premultiplied visible result.
                        background = Image.new('RGBA', (size, size), (0, 0, 0, 255))
                        if ImageChops.difference(Image.alpha_composite(background, reference),
                                                 Image.alpha_composite(background, reopened.crop((x,y,x+w,y+h)))).convert('RGB').getbbox():
                            raise ValueError('Atlas roundtrip mismatch')
            sheets.append({'path': target.name, 'sha256': digest(target), 'state': state,
                           'cell_size': size, 'frame_count': len(frames), 'columns': columns,
                           'direction_count': len(cfg['directions']), 'rows_per_direction': rows_per_direction,
                           'dimensions': list(atlas.size), 'cells': cells})
    # Contact sheet: checkerboard compositing is preview-only, never used for sprites.
    preview_size = min(256, cfg['source_size'])
    tiles = list(images.values())
    cols = min(8, len(tiles)); rows = math.ceil(len(tiles)/cols)
    contact = Image.new('RGB', (cols*preview_size, rows*(preview_size+20)), (35,35,35))
    draw = ImageDraw.Draw(contact)
    for n, (key, tile) in enumerate(images.items()):
        x, y = n % cols * preview_size, n // cols * (preview_size+20)
        contact.paste(tile.resize((preview_size, preview_size)), (x,y), tile.resize((preview_size, preview_size)))
        draw.text((x+4,y+preview_size+3), f'{key[0]} d{key[1]} #{key[2]}', fill='white')
    contact.save(out / 'contact-sheet.png')
    for state, frames in cfg['states'].items():
        if len(frames) > 1:
            sequence = []
            for i in range(len(frames)):
                background = Image.new('RGBA', (cfg['source_size'],)*2, (38,38,38,255))
                sequence.append(Image.alpha_composite(background, images[state,0,i]).convert('RGB'))
            sequence[0].save(out / f'{state}-preview.gif', save_all=True, append_images=sequence[1:],
                             duration=round(1000/cfg['fps']/10)*10, loop=0, disposal=2)
            with Image.open(out / f'{state}-preview.gif') as gif:
                if gif.n_frames != len(frames):
                    raise ValueError('GIF frame collapse')
    report = {'passed': True, 'capture_count': len(images), 'atlas_count': len(sheets),
              'checks': ['source master hash', 'frame order and hashes', 'RGBA and dimensions',
                         'nonempty transparent canvas', 'visible clipping', 'unique animation cells',
                         'atlas cell roundtrip', 'GIF frame count'],
              'art_accepted': False, 'manual_review': ['stone appearance', 'lighting calibration',
              'native-size readability', 'animation loop seam'], 'sheets': sheets}
    (out / 'qa.json').write_text(json.dumps(report, indent=2) + '\n')
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--blender', default='blender')
    parser.add_argument('--pack-only', action='store_true')
    args = parser.parse_args()
    out = args.out.resolve()
    if not args.pack_only:
        if args.config is None:
            parser.error('--config required unless --pack-only')
        cfg = json.loads(args.config.read_text())
        validate_config(cfg)
        source = (args.config.resolve().parent / cfg['source']).resolve()
        if not source.is_file():
            parser.error(f'Missing Blender source: {source}')
        # Refuse to mix a new capture with an old run or overwrite prior evidence.
        if out.exists() and any(out.iterdir()):
            parser.error('Output directory must be new/empty; use --pack-only for QA retries')
        out.mkdir(parents=True, exist_ok=True)
        config = out / 'export-config.json'
        config.write_text(json.dumps(cfg, indent=2)+'\n')
        worker = Path(__file__).with_name('render_sprite_frames.py').resolve()
        command = [args.blender, '-b', '-t', '4', str(source), '--python-exit-code', '1',
                   '--python', str(worker), '--', '--config', str(config), '--out', str(out)]
        with (out / 'blender.log').open('w') as log:
            subprocess.run(command, stdout=log, stderr=subprocess.STDOUT, check=True)
        verifier = Path(__file__).with_name('verify_sprite_master.py').resolve()
        with (out / 'reopen.log').open('w') as log:
            subprocess.run([args.blender, '-b', '-t', '4', str(out / 'master.blend'),
                            '--python-exit-code', '1', '--python', str(verifier), '--', str(out)],
                           stdout=log, stderr=subprocess.STDOUT, check=True)
    report = pack(out)
    print(json.dumps({k: v for k,v in report.items() if k != 'sheets'}, indent=2))


if __name__ == '__main__':
    main()
