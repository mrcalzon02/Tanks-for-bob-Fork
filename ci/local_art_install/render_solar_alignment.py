"""Reproject the approved V8 source to native square ground tiles; no remodel."""
import argparse,hashlib,json,math,sys
from pathlib import Path
import bpy
import numpy as np
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);source=a.source.resolve();out=a.out.resolve()
    if out.exists():raise FileExistsError(out)
    original=sha(source);out.mkdir(parents=True)
    bpy.ops.wm.open_mainfile(filepath=str(source));scene=bpy.context.scene
    root=bpy.data.objects['EXPORT | rotate Solar Boiler model, never camera']
    projection=bpy.data.objects.new('SPRITE ONLY | native square ground tiles',None)
    scene.collection.objects.link(projection);projection.scale.y=math.sqrt(2);root.parent=projection
    scene.render.resolution_x=scene.render.resolution_y=256;scene.render.resolution_percentage=100
    scene.render.film_transparent=True;scene.render.image_settings.color_mode='RGBA'
    scene.cycles.samples=16;scene.cycles.use_denoising=False
    atlas=np.zeros((2048,2048,4),dtype=np.float32);frames=[]
    for d,(facing,yaw) in enumerate((('north',0),('east',270),('south',180),('west',90))):
        root.rotation_euler.z=math.radians(yaw)
        for k,frame in enumerate(range(1,92,6)):
            scene.frame_set(frame);file=out/f'{facing}-{k:02d}.png';scene.render.filepath=str(file)
            bpy.ops.render.render(write_still=True)
            im=bpy.data.images.load(str(file),check_existing=False)
            pixels=np.array(im.pixels[:],dtype=np.float32).reshape(256,256,4);bpy.data.images.remove(im)
            ys,xs=np.nonzero(pixels[:,:,3]>.01)
            assert len(xs)>10 and xs.min()>0 and ys.min()>0 and xs.max()<255 and ys.max()<255,file
            x=k%8*256;y=(d*2+k//8)*256
            atlas[2048-y-256:2048-y,x:x+256]=pixels
            frames.append({'facing':facing,'source_frame':frame,'file':file.name,'sha256':sha(file)})
    im=bpy.data.images.new('Solar V8 native ground projection',width=2048,height=2048,alpha=True)
    im.pixels.foreach_set(atlas.ravel());im.file_format='PNG';im.filepath_raw=str(out/'working-256.png');im.save()
    receipt={'asset':'solar-boiler-v8','source_sha256':original,'geometry_changed':False,
      'sprite_only_global_y_scale':math.sqrt(2),'fixed_camera_ortho':scene.camera.data.ortho_scale,
      'frame_count':16,'facings':['north','east','south','west'],'true_blender_frames':64,
      'native_scale':32*scene.camera.data.ortho_scale/256,'native_shift':[0,-.93/math.sqrt(2)+.25],
      'atlas_sha256':sha(out/'working-256.png'),'frames':frames,'native_alignment_verified':False}
    (out/'capture-manifest.json').write_text(json.dumps(receipt,indent=2)+'\n')
    assert sha(source)==original;print('SOLAR_V8_NATIVE_PROJECTION_CAPTURED',receipt['atlas_sha256'],flush=True)
if __name__=='__main__':main()
