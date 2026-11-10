#!/usr/bin/env python3
"""Independent Blender reopen test: parabolic optics, native 3-port fixture and packed PBR.

Checks the ACTUAL saved .blend, not source text or an optimistic build report.
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


def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--output',type=Path,required=True)
    args=p.parse_args(sys.argv[sys.argv.index('--')+1:])
    output=args.output.resolve()
    report=json.loads((output/'build-report.json').read_text())
    source=HERE.parent/'generated-v1'/'solar-boiler-v1.blend'
    native=output/'solar-boiler-v2.blend'
    assert Path(bpy.data.filepath).resolve()==native.resolve()
    assert sha(native)==report['native_sha256']
    assert sha(source)==report['source_v1_sha256']
    assert report['native_footprint_tiles']==[3,2]
    assert report['parabolic_concentrators']==2
    assert not report['game_integrated'] and not report['visual_approved']
    s=bpy.context.scene
    root=bpy.data.objects['EXPORT | rotate Solar Boiler model, never camera']
    assert list(root['footprint_tiles'])==[3,2]
    assert s.render.engine=='CYCLES' and s.render.film_transparent
    cams=[o for o in bpy.data.objects if o.type=='CAMERA']
    assert len(cams)==1 and cams[0] is s.camera
    cam=s.camera
    original=report['camera']
    def camera_record():
        return {'name':cam.name,'matrix_world':[list(r) for r in cam.matrix_world],
            'type':cam.data.type,'ortho_scale':cam.data.ortho_scale,
            'shift_x':cam.data.shift_x,'shift_y':cam.data.shift_y,
            'resolution':[s.render.resolution_x,s.render.resolution_y]}
    assert camera_record()==original
    assert cam.data.type=='ORTHO' and not cam.parent and cam.data.shift_x==cam.data.shift_y==0
    refs=bpy.data.collections['REFERENCE ONLY | adjacent matched 1-tile pipe fixtures']
    assert refs.hide_render
    packed={}
    for key in ('ferrocrete','ferrocrete_light','ferrocrete_dark'):
        mat=bpy.data.materials['TP Library | '+key]
        images=[n.image for n in mat.node_tree.nodes if n.type=='TEX_IMAGE']
        assert len(images)==3 and all(im and im.packed_file for im in images)
        packed[key]=[im.name for im in images]
    contract=json.loads((HERE.parent/'v1'/'port-contract.json').read_text())
    # Preserve the native 3x2 standard ports and all 128 mating face vertices.
    checks=[]
    for port in contract['ports']:
        name=port['id'];P=Vector(port['blender_flange_xyz']);N=Vector(port['normal_xyz'])
        m=bpy.data.objects[f'PORT | {name} | full machine collar']
        r=bpy.data.objects[f'REF | {name} | near matching collar']
        assert m.get('fmpl_socket_id')==name
        assert list(m['native_cell'])==port['native_cell']
        def face(obj):
            return [obj.matrix_world@v.co for v in obj.data.vertices
                    if abs((obj.matrix_world@v.co-P).dot(N))<1e-6]
        a=face(m);b=face(r)
        assert len(a)==len(b)==128,(name,len(a),len(b))
        error=max(min((v-w).length for w in b) for v in a)
        assert error<1e-5,(name,error)
        checks.append({'id':name,'game_cell':port['native_cell'],
                       'face_vertices':128,'mating_error_bu':error})
    # Check the actual new mesh: 32 segments of continuously rising parabolic
    # reflector, not flat strips. Trace rays from several shell vertices.
    optics=[];loops=[]
    focus=float(report['focus_height_bu']);half=float(report['aperture_half_width_bu'])
    root.rotation_euler.z=0;s.frame_set(0);bpy.context.view_layer.update()
    for label,sign in (('west',-1),('east',1)):
        rig=bpy.data.objects[f'SOLAR | {label} | adjustable trough pivot']
        mirror=bpy.data.objects[f'CONCENTRATOR | {label} | true parabolic continuous mirror']
        tube=bpy.data.objects[f'CONCENTRATOR | {label} | focal black absorber tube']
        assert mirror.parent is rig and tube.parent is rig
        assert mirror.type==tube.type=='MESH'
        assert len(mirror.data.vertices)==990
        assert rig.animation_data is None, 'Rigid pipes cannot follow a moving collector'
        assert abs(math.degrees(rig.rotation_euler.x)-report['tilt_deg'])<1e-5
        samples=mirror.data.vertices[:495]
        errors=[abs(v.co.z-v.co.y**2/(4*focus)) for v in samples]
        assert max(errors)<1e-5,(label,max(errors))
        assert abs(max(v.co.z for v in samples)-half*half/(4*focus))<1e-5
        axis=tube['optical_focal_axis']
        assert len(axis)==2 and all(abs(p[1])<1e-6 and abs(p[2]-focus)<1e-6 for p in axis)
        for y in (-half,-.20,-.10,.10,.20,half):
            slope=y/(2*focus);d_y=-2*slope/(1+slope*slope);d_z=(1-slope*slope)/(1+slope*slope)
            hit=y*y/(4*focus)-y*d_z/d_y
            assert abs(hit-focus)<1e-9
        # Rigid copper conduits: each begin at the real FOCUS receiver bore,
        # and end on the source pressure drum, across idle/working states.
        for role,x in (('hot collector outlet to drum',-.45*sign),
                       ('cool thermal return from drum',.45*sign)):
            line=bpy.data.objects[f'CONCENTRATOR | {label} | continuous {role}']
            assert line.parent is root
            expected=rig.matrix_world@Vector((x,0,focus))
            actual=Vector(line['source_focal_endpoint_world'])
            assert (actual-expected).length<1e-5,(label,role,actual,expected)
            end=Vector(line['pressure_drum_endpoint_world'])
            assert abs(end.y+.1)<1e-6 and .80<=end.z<=1.06
            for frame in (0,25,97):
                s.frame_set(frame);bpy.context.view_layer.update()
                assert (rig.matrix_world@Vector((x,0,focus))-actual).length<1e-5
            loops.append({'collector':label,'role':role,
                          'receiver_distance_bu':(actual-expected).length,
                          'outlet_end':list(end)})
        s.frame_set(0)
        optics.append({'id':label,'mesh_parabola_max_error_bu':max(errors),
                       'focal_axis_z_bu':focus,'rim_z_bu':half*half/(4*focus),
                       'focus_ray_samples':6,'mirror_quad_count':len(mirror.data.polygons)})
    assert not any(o.name.startswith('SOLAR | west | segmented mirror strip') or
                   o.name.startswith('SOLAR | east | segmented mirror strip') for o in s.objects)
    assert len([o for o in s.objects if o.name.startswith('PRESSURE | short active plume')])==3
    assert bpy.data.objects.get('PROCESS | horizontal copper steam drum')
    for yaw in (0,90,180,270):
        root.rotation_euler.z=math.radians(yaw)
        s.frame_set(25);bpy.context.view_layer.update()
        assert camera_record()==original
    root.rotation_euler.z=0;s.frame_set(0)
    assert len(report['renders'])==8
    for e in report['renders']:
        img=output/e['file'];assert img.is_file() and sha(img)==e['sha256']
    result={'schema':'tanks.solar-boiler.v2.native-reopen','passed':True,
            'master_sha256':report['native_sha256'],'source_v1_preserved':True,
            'focal_geometry':optics,'four_physically_continuous_thermal_lines':loops,
            'standard_native_port_faces':checks,'packed_fmpl_pbr':packed,
            'one_45_degree_camera_preserved':True,'render_count':8,
            'visual_approved':False,'game_integrated':False}
    (output/'native-reopen-qa.json').write_text(json.dumps(result,indent=2)+'\n')
    print('SOLAR_V2_NATIVE_REOPEN_PARABOLA_FOCUS_AND_PORTS_PASS',len(optics),len(checks),flush=True)

if __name__=='__main__':main()
