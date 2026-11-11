#!/usr/bin/env python3
"""Correct only the unrendered frame-97 visibility seam of V6 glass relief.

The 68 gameplay candidate frames and six effect-isolation images are all
captured from poses 1..91. The stored native model mis-keyed the closing pose
97 for some 3-phase steam wisps. This tool reopens the actual saved .blend,
repairs only that final visibility key, and updates its source SHA receipt.
No game assets, pipes, wood geometry or source V5 Blender file are touched.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys
import bpy

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from build_solar_boiler_v6 import vent_lobe_enabled, sha


def repair(out):
    out=out.resolve()
    native=out/'solar-boiler-v6.blend'
    manifest=out/'build-report.json'
    rec=json.loads(manifest.read_text())
    original_sha=sha(native)
    assert Path(bpy.data.filepath).resolve()==native.resolve()
    assert rec['native_sha256']==original_sha
    assert len(rec['renders'])==68
    assert set(rec['isolation'])=={'focal-boil','focal-steam','body-rumble'}
    for image in rec['renders']:
        assert sha(out/image['file'])==image['sha256']
    for images in rec['isolation'].values():
        assert len(images)==2
        for image in images:
            assert sha(out/image['file'])==image['sha256']

    vents=[ob for ob in bpy.data.objects
           if ob.get('v6_steam_origin')=='open focal receiver relief hole']
    assert len(vents)==12
    scene=bpy.context.scene
    scene.frame_set(1)
    first={}
    for ob in vents:
        tube=int(ob['v6_receiver_tube'])
        cap=int(ob['v6_glass_end'])
        phase=int(ob.name.rsplit(' ',1)[-1])
        expected_hidden=not vent_lobe_enabled(tube,cap,phase,0)
        assert ob.hide_render==expected_hidden,('Unexpected first-frame steam',ob.name)
        first[ob.name]=(ob.hide_render,ob.location.copy(),ob.scale.copy())
    scene.frame_set(97)
    repaired=0
    for ob in vents:
        hidden,location,scale=first[ob.name]
        assert (ob.location-location).length<1e-5,(ob.name,'location seam')
        assert (ob.scale-scale).length<1e-5,(ob.name,'scale seam')
        if ob.hide_render!=hidden:
            repaired+=1
        ob.hide_render=hidden
        ob.keyframe_insert(data_path='hide_render',frame=97)
    assert repaired>0
    scene.frame_set(97)
    for ob in vents:
        hidden,location,scale=first[ob.name]
        assert ob.hide_render==hidden,(ob.name,'visibility seam')
        assert (ob.location-location).length<1e-5
        assert (ob.scale-scale).length<1e-5
    scene.frame_set(0)
    bpy.context.view_layer.update()
    bpy.ops.wm.save_as_mainfile(filepath=str(native),compress=True,check_existing=False)
    new_sha=sha(native)
    assert new_sha!=original_sha
    rec['native_sha256']=new_sha
    rec['frame97_steam_seam_repair']={
        'original_native_sha256':original_sha,
        'corrected_native_sha256':new_sha,
        'corrected_steam_visibility_keys':repaired,
        'unchanged_blender_sprite_frames':len(rec['renders']),
        'unchanged_isolation_images':sum(map(len,rec['isolation'].values())),
        'scope':'Frame 97 closure only; no rendered frames altered'
    }
    manifest.write_text(json.dumps(rec,indent=2)+'\n')
    print('SOLAR_V6_STEAM_SEAM_FIXED',repaired,new_sha,flush=True)


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--output',type=Path,required=True)
    args=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else sys.argv[1:])
    repair(args.output)


if __name__=='__main__':
    main()
