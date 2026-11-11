#!/usr/bin/env python3
"""Resume *only missing* Blender V6 4-way frames from the saved native source.

This is a true Cycles continuation, not re-packing existing wrong geometry or
silently accepting absent frames. One Blender process handles one orientation
(or one effect-isolation pair), avoiding the Ubuntu/Cycles renderer exit-139
observed after 52 continuous frames in one process.
"""
from __future__ import annotations
import argparse, hashlib, json, math
from pathlib import Path
import sys
import bpy

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from build_solar_boiler_v6 import SOURCE,SOURCE_REPORT,FRAMES,YAW,rumble,sha,camera_record


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,required=True)
    mode=parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--direction',type=int,choices=(0,1,2,3))
    mode.add_argument('--effect',choices=('focal-boil','focal-steam','body-rumble'))
    mode.add_argument('--audit',action='store_true')
    args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else sys.argv[1:])
    out=args.output.resolve();source=out/'solar-boiler-v6.blend'
    receipt=out/'build-report.json'
    assert source.is_file() and receipt.is_file(),'Recovered actual Cycles V6 scene/manifest missing'
    info=json.loads(receipt.read_text())
    assert Path(bpy.data.filepath).resolve()==source.resolve(),'Wrong Blender source open'
    assert sha(source)==info['native_sha256'],'Recovered Blender source SHA mismatch'
    v5=json.loads(SOURCE_REPORT.read_text())
    assert sha(SOURCE)==v5['native_sha256']==info['v5_source_sha256']
    scene=bpy.context.scene
    root=bpy.data.objects['EXPORT | rotate Solar Boiler model, never camera']
    assert camera_record(scene)==info['camera']
    assert len([ob for ob in bpy.data.objects if ob.type=='CAMERA'])==1
    assert scene.render.engine=='CYCLES' and scene.render.film_transparent
    assert scene.render.image_settings.color_mode=='RGBA'
    assert scene.render.resolution_x==scene.render.resolution_y==256
    assert scene.render.fps==8

    def check_png(path):
        with path.open('rb') as f:
            header=f.read(24)
        assert len(header)==24 and header[:8]==b'\x89PNG\r\n\x1a\n',path
        assert int.from_bytes(header[16:20],'big')==256 and int.from_bytes(header[20:24],'big')==256,path

    def guard_record(filename):
        matches=[r for r in info['renders'] if r['file']==filename]
        assert len(matches)<=1,(filename,len(matches))
        path=out/filename
        if path.exists():
            check_png(path)
            if matches:
                assert sha(path)==matches[0]['sha256'],('Existing Cycles frame drift',filename)
                print('SOLAR_V6_NATIVE_FRAME_REUSED',filename,flush=True)
                return True
            # If the renderer saved PNG before crashing but did not flush the
            # manifest record, do not trust it silently: re-render that frame.
        elif matches:
            raise RuntimeError('Saved report names a missing genuine Blender frame: '+filename)
        return False

    def render(filename,frame):
        path=out/filename
        scene.frame_set(frame);bpy.context.view_layer.update()
        assert camera_record(scene)==info['camera']
        scene.render.filepath=str(path)
        print('SOLAR_V6_RESUMED_REAL_CYCLES',filename,frame,flush=True)
        bpy.ops.render.render(write_still=True)
        check_png(path)
        return sha(path)

    if args.direction is not None:
        d=args.direction
        root.rotation_euler.z=math.radians(YAW[d])
        for k,frame in enumerate(FRAMES):
            filename=f'working-d{d:02d}-f{k:03d}.png'
            if guard_record(filename):continue
            digest=render(filename,frame)
            info['renders'].append({'file':filename,'frame':frame,'direction':d,
                                    'state':'working','index':k,'sha256':digest})
            receipt.write_text(json.dumps(info,indent=2)+'\n')
        print('SOLAR_V6_RESUME_CARDINAL_PASS',d,flush=True)

    def curves(obj,path=None):
        action=getattr(getattr(obj,'animation_data',None),'action',None)
        return [fc for fc in (getattr(action,'fcurves',None) or [])
                if path is None or fc.data_path==path]

    if args.effect is not None:
        effect=args.effect
        root.rotation_euler.z=0
        objs=( [o for o in bpy.data.objects if o.get('v6_boiling_bubble')]
               if effect=='focal-boil' else
               [bpy.data.objects[n] for n in info['steam_objects']]
               if effect=='focal-steam' else
               [bpy.data.objects[info['rumble_rig']]] )
        path='location' if effect=='body-rumble' else 'hide_render'
        k=2 if effect=='focal-steam' else 4
        states=[(fc,fc.mute) for ob in objs for fc in curves(ob,path)]
        assert states,('No Blender animation channels for',effect)
        seen=info['isolation'].get(effect,[])
        for state in ('off','on'):
            filename=f'iso-{effect}-{state}.png'
            old=[r for r in seen if r['file']==filename]
            assert len(old)<=1
            if (out/filename).is_file() and old:
                assert sha(out/filename)==old[0]['sha256']
                continue
            scene.frame_set(FRAMES[k]);bpy.context.view_layer.update()
            for fc,mute in states:fc.mute=True
            for ob in objs:
                if path=='hide_render':ob.hide_render=(state=='off')
                else:ob.location=(0,0,0) if state=='off' else rumble(k)
            bpy.context.view_layer.update()
            digest=render(filename,FRAMES[k])
            record={'file':filename,'frame':FRAMES[k],'sha256':digest}
            seen=[r for r in seen if r['file']!=filename]+[record]
            info['isolation'][effect]=seen
            receipt.write_text(json.dumps(info,indent=2)+'\n')
        print('SOLAR_V6_ISOLATION_RECOVERED',effect,flush=True)

    if args.audit:
        records=info['renders']
        assert len(records)==68,('Invalid frame total',len(records))
        expected=[f'idle-d{d:02d}.png' for d in range(4)]
        expected +=[f'working-d{d:02d}-f{k:03d}.png' for d in range(4) for k in range(16)]
        names=[r['file'] for r in records]
        assert sorted(names)==sorted(expected),('Missing/duplicate frame registrations',len(names))
        for r in records:
            check_png(out/r['file'])
            assert sha(out/r['file'])==r['sha256']
        assert set(info['isolation'])=={'focal-boil','focal-steam','body-rumble'}
        for name,records in info['isolation'].items():
            assert len(records)==2,name
            for r in records:
                check_png(out/r['file']);assert sha(out/r['file'])==r['sha256']
        info['render_count']=68
        receipt.write_text(json.dumps(info,indent=2)+'\n')
        print('SOLAR_V6_68_REAL_RENDER_AND_6_ISOLATION_DIGESTS_PASS',flush=True)

if __name__=='__main__':main()
