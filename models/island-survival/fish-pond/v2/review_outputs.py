"""Compose genuine capture comparisons and a lossless animated PNG preview."""
import argparse
import hashlib
import json
from pathlib import Path
import struct
import sys
import zlib

import bpy
import numpy as np


def chunk(kind, data):
    return struct.pack('>I',len(data))+kind+data+struct.pack('>I',zlib.crc32(kind+data))


def read_chunks(path):
    data = path.read_bytes()
    assert data[:8] == b'\x89PNG\r\n\x1a\n'
    pos = 8
    result = []
    while pos < len(data):
        length = struct.unpack_from('>I', data, pos)[0]
        kind, body = data[pos+4:pos+8],data[pos+8:pos+8+length]
        assert zlib.crc32(kind+body) == struct.unpack_from('>I',data,pos+8+length)[0]
        result.append((kind,body))
        pos += length+12
    assert result[-1][0] == b'IEND'
    return result


def apng(paths, output):
    images = [read_chunks(path) for path in paths]
    header = images[0][0][1]
    assert all(image[0] == (b'IHDR',header) for image in images)
    width, height = struct.unpack_from('>II',header)
    data = b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',header)
    for kind, body in images[0]:
        if kind in (b'sRGB',b'gAMA',b'cHRM'):
            data += chunk(kind,body)
    data += chunk(b'acTL',struct.pack('>II',len(paths),0))
    seq = 0
    for index, image in enumerate(images):
        data += chunk(b'fcTL',struct.pack('>IIIIIHHBB',seq,width,height,0,0,1,8,0,0))
        seq += 1
        for kind, body in image:
            if kind == b'IDAT':
                if index == 0:
                    data += chunk(b'IDAT',body)
                else:
                    data += chunk(b'fdAT',struct.pack('>I',seq)+body)
                    seq += 1
    output.write_bytes(data+chunk(b'IEND',b''))
    assert len([1 for kind,_ in read_chunks(output) if kind == b'fcTL']) == 16


def pixels(path):
    im = bpy.data.images.load(str(path),check_existing=False)
    width,height = im.size
    data = np.array(im.pixels[:],dtype=np.float32).reshape(height,width,4)
    bpy.data.images.remove(im)
    return data


def save(path, data):
    height,width = data.shape[:2]
    im = bpy.data.images.new(path.stem,width=width,height=height,alpha=True)
    im.pixels.foreach_set(data.ravel())
    im.file_format='PNG'
    im.filepath_raw=str(path)
    im.save()
    bpy.data.images.remove(im)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--source',type=Path,required=True)
    p.add_argument('--gui',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True)
    a = p.parse_args(sys.argv[sys.argv.index('--')+1:])
    source,gui,out = a.source.resolve(),a.gui.resolve(),a.out.resolve()
    out.mkdir(parents=True,exist_ok=True)
    paths = [source/f'north-working-{i:02d}.png' for i in range(16)]
    apng(paths,out/'fish-pond-v2-loop.png')
    # Exact same crop and native zoom on both sides: legacy left, candidate right.
    board = np.zeros((400,880,4),dtype=np.float32)
    for col,name in enumerate(('north-legacy-close.png','north-close.png')):
        data = pixels(gui/name)
        board[:,col*440:(col+1)*440] = data[56:456,164:604]
    save(out/'native-before-after.png',board)
    board = np.zeros((800,880,4),dtype=np.float32)
    for d,name in enumerate(('north','east','south','west')):
        board[(1-d//2)*400:(2-d//2)*400,d%2*440:(d%2+1)*440] = pixels(gui/(name+'-fluid-close.png'))[56:456,164:604]
    save(out/'native-four-connections.png',board)
    result = {'previews':{},'animation':{'fps':8,'frames':16,'source':'genuine Blender working frames'},
              'comparison':{'left':'legacy active art','right':'candidate V2','native_zoom':2.5,'identical_crop':True}}
    for name in ('fish-pond-v2-loop.png','native-before-after.png','native-four-connections.png'):
        result['previews'][name] = hashlib.sha256((out/name).read_bytes()).hexdigest()
    (out/'preview-manifest.json').write_text(json.dumps(result,indent=2)+'\n')
    print('FISH_POND_REVIEW_PREVIEWS_READY')


if __name__ == '__main__':
    main()
