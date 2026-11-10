#!/usr/bin/env python3
"""Independently reopen the actual Solar Boiler V1 scene and check PBR/ports.

It is deliberately not allowed to infer Factorio runtime connectivity from
model-space alignment; the active prototype cell mapping remains a separate
runtime integration gate once sprites are approved.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
from pathlib import Path
import sys
import bpy
from mathutils import Vector

HERE=Path(__file__).resolve().parent

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--fmpl-root',type=Path,required=True)
    args=parser.parse_args(sys.argv[sys.argv.index('--')+1:])
    out=args.output.resolve();fmpl=args.fmpl_root.resolve()
    native=out/'solar-boiler-v1.blend'
    record=json.loads((out/'build-report.json').read_text())
    contract=json.loads((HERE/'port-contract.json').read_text())
    assert Path(bpy.data.filepath).resolve()==native.resolve(), 'Did not reopen saved native file'
    assert sha(native)==record['native_sha256'], 'Native source checksum drift'
    assert record['footprint']==[3,2]
    assert record['source_commit']=='939ff2d0fea5d236d7092b907c5f08961d5a7560'
    # Same installed guard used by the original native model construction.
    sys.path.insert(0,str(fmpl/'tools/fmpl'))
    try:from blender_camera_guard import assert_clean, camera_record
    finally:sys.path.pop(0)
    s=bpy.context.scene
    assert_clean(s,record['camera_profile'],bpy)
    assert camera_record(s)==record['camera']
    assert not s.camera.parent
    assert s.render.film_transparent and s.render.image_settings.color_mode=='RGBA'
    # The approved reference maps are packed; paths may be discarded after build.
    image_slots={}
    for mid in record['material_ids']:
        material=bpy.data.materials['TP Library | '+mid]
        assert material.get('tp_library_material_id')==mid
        maps=[n.image for n in material.node_tree.nodes if n.type=='TEX_IMAGE']
        assert len(maps)==3
        assert all(im.packed_file for im in maps)
        image_slots[mid]=[im.name for im in maps]
    pivot=bpy.data.objects['EXPORT | rotate Solar Boiler model, never camera']
    assert list(pivot['footprint_tiles'])==[3,2]
    refs=bpy.data.collections['REFERENCE ONLY | adjacent matched 1-tile pipe fixtures']
    assert refs.hide_render, 'Reference/measurement pipes must not be captured'
    # Face-by-face proof that the machine collar mates exactly to an adjacent
    # boiler-standard pipe, not just their origins or centerlines matching.
    checks=[]
    for port in contract['ports']:
        name=port['id']
        actual=bpy.data.objects['PORT | '+name+' | full machine collar']
        adjacent=bpy.data.objects['REF | '+name+' | near matching collar']
        P=Vector(port['blender_flange_xyz']);N=Vector(port['normal_xyz'])
        assert actual.get('fmpl_socket_id')==name
        assert list(actual['native_cell'])==port['native_cell']
        assert max(abs(a-b) for a,b in zip(actual['port_center'],port['blender_flange_xyz'])) < 1e-5
        assert list(actual['port_normal'])==port['normal_xyz']
        def face_points(ob):
            return [ob.matrix_world@v.co for v in ob.data.vertices
                    if abs((ob.matrix_world@v.co-P).dot(N))<1e-6]
        machine=face_points(actual);reference=face_points(adjacent)
        assert len(machine)==len(reference)==128,(name,len(machine),len(reference))
        residual=max(min((a-b).length for b in reference) for a in machine)
        assert residual<1e-5,(name,residual)
        checks.append({'id':name,'native_cell':port['native_cell'],
                       'blender_mating_center':list(P),'face_vertices':len(machine),
                       'face_mating_error_bu':residual})
    tank=bpy.data.objects['PROCESS | horizontal copper steam drum']
    assert tank.type=='MESH' and tank.parent is pivot
    arrays=[o for o in s.objects if o.name.endswith('adjustable trough pivot')]
    assert len(arrays)==2
    pos=[]
    for frame in (1,25,49,73,97):
        s.frame_set(frame);bpy.context.view_layer.update()
        pos.append(math.degrees(arrays[0].rotation_euler.x))
    assert abs(pos[0]-pos[-1])<1e-3
    assert max(pos)-min(pos)>7.9 and abs(pos[1]-25)<.01 and abs(pos[3]-17)<.01,pos
    vapor=[o for o in s.objects if o.name.startswith('PRESSURE | short active plume')]
    assert len(vapor)==3
    s.frame_set(0);assert all(o.hide_render for o in vapor)
    s.frame_set(25);assert all(not o.hide_render for o in vapor)
    # One camera only. Cardinal model rotation must not move the camera.
    original=camera_record(s)
    for angle in (0,90,180,270):
        pivot.rotation_euler.z=math.radians(angle)
        s.frame_set(25);bpy.context.view_layer.update()
        assert camera_record(s)==original
    pivot.rotation_euler.z=0;s.frame_set(0)
    bpy.context.view_layer.update()
    assert_clean(s,record['camera_profile'],bpy)
    for entry in record['renders']:
        f=out/entry['file']
        assert f.is_file() and sha(f)==entry['sha256']
    assert len(record['renders'])==8
    receipt={'schema':'tanks.solar-boiler.v1.native-reopen','passed':True,
             'source_hash':record['native_sha256'],'camera':record['camera'],
             'fmpl_ferrocrete_pbr_packed':image_slots,'tile_ports':checks,
             'panel_angle_degrees':pos,'vapor_idle_hidden':True,'vapor_working_visible':True,
             'four_model_orientations_single_camera':True,
             'visual_approved':False,'native_factorio_tested':False}
    (out/'native-reopen-qa.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print('SOLAR_BOILER_V1_NATIVE_REOPEN_PASS',len(checks),len(record['renders']),flush=True)

if __name__=='__main__':main()
