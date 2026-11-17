"""Pack real Pondering Hovel renders and verify all cells, alpha bounds and loop poses."""
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
 parser=argparse.ArgumentParser();parser.add_argument('--source',type=Path,required=True);parser.add_argument('--out',type=Path,required=True);args=parser.parse_args(sys.argv[sys.argv.index('--')+1:]);source=args.source.resolve();out=args.out.resolve()
 if out.exists():raise FileExistsError(out)
 receipt=json.loads((source/'capture-manifest.json').read_text());inspect=json.loads((source/'runtime-inspection.json').read_text());assert receipt['genuine_rendered_passes']==len(receipt['images'])==396;assert inspect['technical_checks_passed'];assert sha(source/'stone-water-wheel-v3.blend')==receipt['source_sha256']==inspect['source_sha256'];assert sha(source/'stone-water-wheel-v3.glb')==receipt['runtime_sha256']==inspect['glb_sha256'];arrays={};bounds=[]
 for row in receipt['images']:
  p=source/row['file'];assert sha(p)==row['sha256'];key=(row['facing'],row['state'],row['index'],row['layer']);assert key not in arrays;data=pixels(p);arrays[key]=data;ys,xs=np.nonzero(data[:,:,3]>.01);assert len(xs)>2;assert min(xs.min(),ys.min())>1 and max(xs.max(),ys.max())<254,(p.name,'clipped');bounds.append(dict(file=p.name,alpha_bounds=[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)]))
 layer_qa=[];unique={}
 for facing in ('north','east','south','west'):
  unique[facing]=len({sha(source/f'{facing}-working-{i:02d}-full.png') for i in range(32)});assert unique[facing]>=8,(facing,unique[facing])
  for state,count in [('idle',1),('working',32)]:
   for i in range(count):
    full=arrays[facing,state,i,'full'];above=arrays[facing,state,i,'above-water'];under=arrays[facing,state,i,'underwater'];overlap=int(np.count_nonzero((above[:,:,3]>.95)&(under[:,:,3]>.95)));missing=int(np.count_nonzero((full[:,:,3]>.95)&(np.maximum(above[:,:,3],under[:,:,3])<.05)));assert overlap==missing==0,(facing,state,i,overlap,missing);layer_qa.append(dict(facing=facing,state=state,index=i,opaque_overlap=overlap,missing_body=missing))
 out.mkdir(parents=True);files={}
 for size in (64,128,256):
  for facing in ('north','east','south','west'):
   for state in ('idle','working'):
    for layer in ('full','above-water','underwater'):
     atlas=np.zeros((size*4,size*8,4),dtype=np.float32)
     for i in range(32):
      data=pixels(source/f'{facing}-{state}-{(0 if state=="idle" else i):02d}-{layer}.png',size);row=i//8;col=i%8;atlas[(3-row)*size:(4-row)*size,col*size:(col+1)*size]=data
     path=out/f'{facing}-{state}-{layer}-{size}.png';save(path,atlas);files[path.name]=dict(sha256=sha(path),dimensions=[size*8,size*4])
 manifest=dict(schema='tanks.stone-water-wheel.v3.atlas',verified=True,source_sha256=receipt['source_sha256'],runtime_sha256=receipt['runtime_sha256'],genuine_combined_camera_captures=132,genuine_rendered_layer_passes=396,working_frames_per_facing=32,fps=8,unique_working_images=unique,idle_policy='One genuine frozen pose repeated explicitly in the idle atlas. The native offshore pump freezes its current mechanical pose; no separate idle-animation field.',layer_policy='Complementary exact world-height holdouts, verified at all 132 camera/state/time samples. Native animated submerged layer uses tint/alpha over the actual water; no static frozen underwater wheel substitute.',files=files,layer_qa=layer_qa,alpha_bounds=bounds);(out/'atlas-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print('WHEEL_ATLAS_PASS',len(files),unique,flush=True)
if __name__=='__main__':main()
