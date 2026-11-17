import bpy,numpy as np,json,math,hashlib,sys,argparse
from pathlib import Path
parser=argparse.ArgumentParser();parser.add_argument('--source',type=Path,required=True);parser.add_argument('--client',type=Path,required=True);a=parser.parse_args(sys.argv[sys.argv.index('--')+1:]);c=a.source.resolve();p=a.client.resolve()
def pixels(path):
 im=bpy.data.images.load(str(path),check_existing=False);w,h=im.size;arr=np.array(im.pixels[:],dtype=np.float32).reshape(h,w,4)[::-1].copy();bpy.data.images.remove(im);return arr
alpha=np.min([pixels(c/f'north-working-{i:02d}.png')[:,:,3] for i in range(32)],axis=0);rows,cols=np.nonzero((alpha>.999)&(np.indices(alpha.shape)[0]<170));shift=-1.25/math.sqrt(2);xx=np.rint(320+(cols+.5-128)*2.4).astype(int);yy=np.rint(320+.6*96+shift*96+(rows+.5-128)*2.4).astype(int)
def delta(a,b):
 aa,bb=pixels(p/a),pixels(p/b);d=np.abs(aa[yy,xx,:3]-bb[yy,xx,:3]).max(axis=1);return dict(sampled_opaque_upper_pixels=len(d),changed_over_005=int((d>.05).sum()),maximum=float(d.max()),mean=float(d.mean()))
result=dict(working=delta('north-motion-00.png','north-motion-07.png'),disabled=delta('stopped-a.png','stopped-b.png'),full_output=delta('blocked-item-a.png','blocked-item-b.png'),scope='Matched opaque source-alpha intersection across all 32 phases, upper machinery only; excludes ground, fixtures and background.',source_pixel_count=len(rows))
result['passed']=result['working']['changed_over_005']>100 and result['disabled']['changed_over_005']==result['full_output']['changed_over_005']==0
assert result['passed'],result
(p/'native-animation-observation.json').write_text(json.dumps(result,indent=2)+'\n');print('TANK_NATIVE_ANIMATION_OBSERVATION',json.dumps(result),flush=True)
