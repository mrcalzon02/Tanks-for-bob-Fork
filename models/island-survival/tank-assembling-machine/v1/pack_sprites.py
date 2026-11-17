"""Pack real ammunition-assembler renders and verify all cells, alpha bounds and loop poses."""
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
 parser=argparse.ArgumentParser();parser.add_argument('--source',type=Path,required=True);parser.add_argument('--out',type=Path,required=True);a=parser.parse_args(sys.argv[sys.argv.index('--')+1:]);source=a.source.resolve();out=a.out.resolve()
 if out.exists():raise FileExistsError(out)
 receipt=json.loads((source/'capture-manifest.json').read_text());inspect=json.loads((source/'runtime-inspection.json').read_text());assert receipt['genuine_blender_frames']==len(receipt['images'])==33 and inspect['technical_checks_passed'];assert sha(source/'tank-assembler-v1.blend')==receipt['source_sha256']==inspect['source_sha256'];assert sha(source/'tank-assembler-v1.glb')==receipt['runtime_sha256']==inspect['glb_sha256'];images={};bounds=[]
 for row in receipt['images']:
  path=source/row['file'];assert sha(path)==row['sha256'];key=(row['facing'],row['state'],row['index']);assert key not in images;images[key]=path;data=pixels(path);ys,xs=np.nonzero(data[:,:,3]>.01);assert len(xs)>50;assert min(xs.min(),ys.min())>1 and max(xs.max(),ys.max())<254,(path.name,'clipping');bounds.append(dict(file=path.name,alpha_bounds=[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)]))
 unique={f:len({sha(images[f,'working',i]) for i in range(32)}) for f in ('north',)};assert min(unique.values())>=16,unique;out.mkdir(parents=True);files={}
 for size in (64,128,256):
  for state in ('idle','working'):
   columns,rows=8,4;atlas=np.zeros((size*rows,size*columns,4),dtype=np.float32)
   for facing_index,facing in enumerate(('north',)):
    for i in range(32):
     row=facing_index*4+i//8;col=i%8;data=pixels(images[facing,state,0 if state=='idle' else i],size);atlas[(rows-1-row)*size:(rows-row)*size,col*size:(col+1)*size]=data
   path=out/f'{state}-{size}.png';save(path,atlas);files[path.name]=dict(sha256=sha(path),dimensions=[size*columns,size*rows])
 (out/'atlas-manifest.json').write_text(json.dumps(dict(schema='tanks.vehicle-assembler.v1.atlas',verified=True,source_sha256=receipt['source_sha256'],runtime_sha256=receipt['runtime_sha256'],genuine_blender_frames=33,working_frames_per_facing=32,idle_frames_per_facing=1,fps=8,facings=['north'],unique_working_images=unique,working_layout='8 columns, four rows per direction; directions vertically stacked',idle_layout='One genuine idle pose per direction repeated explicitly into 32 cells to satisfy Factorio matching frame-count requirement; not 32 captured idle timestamps',files=files,alpha_bounds=bounds),indent=2)+'\n');print('TANK_ATLAS_PASS',unique,flush=True)
if __name__=='__main__':main()
