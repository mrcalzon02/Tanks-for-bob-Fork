"""Pack the 68 verified owner-accepted pump captures without a new dependency."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

import bpy
import numpy as np

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def pixels(path,size):
    im=bpy.data.images.load(str(path),check_existing=False)
    assert tuple(im.size)==(256,256)
    if size!=256:im.scale(size,size)
    data=np.array(im.pixels[:],dtype=np.float32).reshape(size,size,4)
    bpy.data.images.remove(im)
    return data

def main():
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);source=a.source.resolve();out=a.out.resolve()
    if out.exists():raise FileExistsError(out)
    manifest=json.loads((source/'capture-manifest.json').read_text())
    inspect=json.loads((source/'runtime-inspection.json').read_text())
    assert manifest['genuine_blender_frames']==len(manifest['images'])==68
    assert inspect['geometry_and_motion_checks_passed'] and inspect['max_socket_motion_tiles']==0
    assert sha(source/'pipe-pump-v3.blend')==manifest['source_sha256']==inspect['source_sha256']
    assert sha(source/'pipe-pump-v3.glb')==manifest['runtime_sha256']==inspect['glb_sha256']
    frames={}
    for row in manifest['images']:
        file=source/row['file'];assert sha(file)==row['sha256']
        key=(row['facing'],row['state'],row['index']);assert key not in frames;frames[key]=file
        data=pixels(file,256)
        ys,xs=np.nonzero(data[:,:,3]>.01)
        assert len(xs)>50 and xs.min()>0 and ys.min()>0 and xs.max()<255 and ys.max()<255
    out.mkdir(parents=True)
    files={}
    for size in (64,128,256):
        for state in ('idle','working'):
            cols,rows=(4,1) if state=='idle' else (8,8)
            atlas=np.zeros((rows*size,cols*size,4),dtype=np.float32)
            for d,facing in enumerate(('north','east','south','west')):
                for k in range(1 if state=='idle' else 16):
                    x=(d if state=='idle' else k%8)*size
                    y=(0 if state=='idle' else d*2+k//8)*size
                    cell=pixels(frames[facing,state,k],size)
                    atlas[(rows*size-y-size):(rows*size-y),x:x+size]=cell
            im=bpy.data.images.new(state+str(size),width=cols*size,height=rows*size,alpha=True)
            im.pixels.foreach_set(atlas.ravel());im.file_format='PNG'
            file=out/(state+'-'+str(size)+'.png');im.filepath_raw=str(file);im.save();bpy.data.images.remove(im)
            check=bpy.data.images.load(str(file),check_existing=False)
            actual=np.array(check.pixels[:],dtype=np.float32).reshape(rows*size,cols*size,4)
            assert np.max(np.abs(actual-atlas))<=1/255+.00001
            bpy.data.images.remove(check)
            files[file.name]={'sha256':sha(file),'dimensions':[cols*size,rows*size],'cell_size':size}
    receipt={'schema':'tanks.pipe-pump.v3.atlas','source_sha256':manifest['source_sha256'],'glb_sha256':manifest['runtime_sha256'],
        'genuine_frames':68,'working_frames_per_facing':16,'fps':8,'facing_order':['north','east','south','west'],
        'files':files,'verified':True,'native_game_verified':False}
    receipt['native_projection']=manifest.get('native_projection')
    (out/'atlas-manifest.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print('PIPE_PUMP_V3_SIX_ATLASES_VERIFIED',json.dumps(receipt),flush=True)

if __name__=='__main__':main()
