"""Pack real pond renders and verify all cells, alpha bounds and loop poses."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

import bpy
import numpy as np


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def pixels(path, size=256):
    im = bpy.data.images.load(str(path), check_existing=False)
    assert tuple(im.size) == (256, 256)
    if size != 256:
        im.scale(size, size)
    data = np.array(im.pixels[:], dtype=np.float32).reshape(size, size, 4)
    bpy.data.images.remove(im)
    return data


def save(path, data):
    height, width = data.shape[:2]
    im = bpy.data.images.new(path.stem, width=width, height=height, alpha=True)
    im.pixels.foreach_set(data.ravel())
    im.file_format = 'PNG'
    im.filepath_raw = str(path)
    im.save()
    bpy.data.images.remove(im)
    check = bpy.data.images.load(str(path), check_existing=False)
    actual = np.array(check.pixels[:], dtype=np.float32).reshape(height, width, 4)
    assert np.max(np.abs(actual-data)) <= 1/255+.00001
    bpy.data.images.remove(check)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args(sys.argv[sys.argv.index('--')+1:])
    source, out = args.source.resolve(), args.out.resolve()
    if out.exists():
        raise FileExistsError(out)
    receipt = json.loads((source/'capture-manifest.json').read_text())
    inspect = json.loads((source/'runtime-inspection.json').read_text())
    assert receipt['genuine_blender_frames'] == len(receipt['images']) == 68
    assert inspect['technical_checks_passed']
    assert sha(source/'fish-pond-v2.blend') == receipt['source_sha256'] == inspect['source_sha256']
    assert sha(source/'fish-pond-v2.glb') == receipt['runtime_sha256'] == inspect['glb_sha256']
    frames, arrays, bounds = {}, {}, []
    for row in receipt['images']:
        path = source/row['file']
        assert sha(path) == row['sha256']
        key = row['facing'], row['state'], row['index']
        assert key not in frames
        frames[key] = path
        data = pixels(path)
        arrays[key] = data
        ys, xs = np.nonzero(data[:,:,3] > .01)
        assert len(xs) > 50 and min(xs.min(),ys.min()) > 1 and max(xs.max(),ys.max()) < 254, (path.name, xs.min(),ys.min(),xs.max(),ys.max())
        bounds.append({'file':path.name, 'alpha_bounds':[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)]})
    for facing in ('north','east','south','west'):
        poses = [sha(frames[facing,'working',k]) for k in range(16)]
        assert len(set(poses)) == 16
        assert any(np.abs(arrays[facing,'idle',0]-arrays[facing,'working',k]).max() > .01 for k in range(16))
    out.mkdir(parents=True)
    files = {}
    for size in (64,128,256):
        for state in ('idle','working'):
            # Native idle_animation must have the same frame count as working.
            # Explicitly repeat the one genuine idle capture, with no fabricated
            # claim that these 16 identical idle cells are separate renders.
            cols, rows = 8,8
            atlas = np.zeros((rows*size, cols*size, 4), dtype=np.float32)
            for d, facing in enumerate(('north','east','south','west')):
                for k in range(16):
                    x = k%8*size
                    y = (d*2+k//8)*size
                    atlas[rows*size-y-size:rows*size-y,x:x+size] = pixels(frames[facing,state,0 if state == 'idle' else k],size)
            path = out/(state+'-'+str(size)+'.png')
            save(path, atlas)
            files[path.name] = {'sha256':sha(path), 'dimensions':[cols*size,rows*size], 'cell_size':size}
    # Transparent visual board, row one idle, row two working. No source-image
    # painting or generated substitutes: these are the original captured cells.
    board = np.zeros((512,1024,4), dtype=np.float32)
    for d, facing in enumerate(('north','east','south','west')):
        for state, y in [('working',0),('idle',256)]:
            board[y:y+256,d*256:d*256+256] = arrays[facing,state,4 if state == 'working' else 0]
    save(out/'review-four-directions.png', board)
    result = {'schema':'tanks.fish-pond.v2.atlas', 'verified':True,
        'source_sha256':receipt['source_sha256'], 'glb_sha256':receipt['runtime_sha256'],
        'genuine_frames':68, 'working_frames_per_facing':16, 'fps':8,
        'unique_idle_frames_per_facing':1, 'native_idle_cells_per_facing':16,
        'facing_order':['north','east','south','west'], 'files':files,
        'alpha_bounds':bounds, 'native_projection':receipt['native_projection'],
        'visual_approved':False, 'native_game_verified':False}
    (out/'atlas-manifest.json').write_text(json.dumps(result, indent=2)+'\n')
    print('FISH_POND_SIX_ATLASES_VERIFIED', json.dumps(files), flush=True)


if __name__ == '__main__':
    main()
