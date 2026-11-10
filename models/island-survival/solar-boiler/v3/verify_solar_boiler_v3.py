#!/usr/bin/env python3
"""Independent native Blender reopen: V3 gauge, red emissive heat, four steam joints.

V2 file and V3 source are distinct; checks actual saved animation/effect values,
tracked port faces, camera identity and the immutable optical trough geometry.
"""
from __future__ import annotations
import argparse, hashlib, json, math, sys
from pathlib import Path

import bpy
from mathutils import Vector

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from animate_solar_boiler_v3 import (gauge_degrees, heat_strength, puff_state,
                                    camera_record, mesh_fingerprint, FRAMES, LOOP_END)


def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def check_scene(output):
    source = HERE.parent/'generated-v2'/'solar-boiler-v2.blend'
    source_record = json.loads((HERE.parent/'generated-v2'/'build-report.json').read_text())
    v3_path = output/'solar-boiler-v3.blend'
    report = json.loads((output/'build-report.json').read_text())
    assert Path(bpy.data.filepath).resolve() == v3_path.resolve(), 'Different native source opened'
    assert sha(v3_path) == report['native_sha256'], 'Native source readback hash mismatch'
    assert sha(source) == source_record['native_sha256'] == report['source_v2_sha256']
    assert report['footprint'] == [3,2]
    assert report['frames'] == list(FRAMES) and report['working_fps'] == 8
    assert not report['visual_approved'] and not report['game_integrated']
    s=bpy.context.scene
    root=bpy.data.objects['EXPORT | rotate Solar Boiler model, never camera']
    assert list(root['footprint_tiles']) == [3,2]
    s.frame_set(0); root.rotation_euler.z = 0
    bpy.context.view_layer.update()
    assert camera_record(s) == report['camera']
    assert len([o for o in bpy.data.objects if o.type=='CAMERA']) == 1
    assert s.camera.data.type == 'ORTHO' and not s.camera.parent
    assert s.render.film_transparent and s.render.image_settings.color_mode == 'RGBA'
    refs=bpy.data.collections['REFERENCE ONLY | adjacent matched 1-tile pipe fixtures']
    assert refs.hide_render
    packed={}
    for mid in ('ferrocrete','ferrocrete_light','ferrocrete_dark'):
        mat=bpy.data.materials['TP Library | '+mid]
        images=[n.image for n in mat.node_tree.nodes if n.type=='TEX_IMAGE']
        assert len(images)==3 and all(im and im.packed_file for im in images),mid
        packed[mid]=[im.name for im in images]
    ports=json.loads((HERE.parent/'v1'/'port-contract.json').read_text())['ports']
    port_checks=[]
    for port in ports:
        name=port['id'];P=Vector(port['blender_flange_xyz']);N=Vector(port['normal_xyz'])
        machine=bpy.data.objects[f'PORT | {name} | full machine collar']
        ref=bpy.data.objects[f'REF | {name} | near matching collar']
        assert machine.get('fmpl_socket_id')==name
        assert list(machine['native_cell'])==port['native_cell']
        def plane(ob):
            return [ob.matrix_world@v.co for v in ob.data.vertices
                    if abs((ob.matrix_world@v.co-P).dot(N))<1e-6]
        a=plane(machine); b=plane(ref)
        assert len(a)==len(b)==128,(name,len(a),len(b))
        delta=max(min((v-w).length for w in b) for v in a)
        assert delta<1e-5,(name,delta)
        port_checks.append({'id':name,'native_cell':port['native_cell'],'face_vertices':128,'max_error_bu':delta})
    # Original optical geometry and both rigid thermal loops cannot move.
    optics=[]
    for label in ('west','east'):
        rig=bpy.data.objects[f'SOLAR | {label} | adjustable trough pivot']
        mirror=bpy.data.objects[f'CONCENTRATOR | {label} | true parabolic continuous mirror']
        absorber=bpy.data.objects[f'CONCENTRATOR | {label} | focal black absorber tube']
        assert rig.animation_data is None
        assert mirror.parent is rig and absorber.parent is rig
        foc=float(mirror['focal_height_bu'])
        assert abs(foc-.28)<1e-6 and len(mirror.data.vertices)==990
        err=max(abs(v.co.z-v.co.y*v.co.y/(4*foc)) for v in mirror.data.vertices[:495])
        assert err<1e-5
        optics.append({'label':label,'parabola_residual_bu':err,'focus':foc})
        for role in ('hot collector outlet to drum','cool thermal return from drum'):
            conduit=bpy.data.objects[f'CONCENTRATOR | {label} | continuous {role}']
            assert conduit.parent is root and conduit.get('thermal_loop_role')
    # Historical needle remains recoverable, but only the new anchored pointer renders.
    legacy=bpy.data.objects['GAUGE | live pressure needle']
    assert legacy.hide_render and legacy.type=='MESH'
    pivot=bpy.data.objects[report['gauge_pivot']]
    needle=bpy.data.objects['GAUGE V3 | crimson actual oscillating needle']
    assert needle.parent is pivot and pivot.parent is root
    angles=[]
    for k,frame in enumerate((*FRAMES,LOOP_END)):
        s.frame_set(frame);bpy.context.view_layer.update()
        angle=math.degrees(pivot.rotation_euler.y)
        assert abs(angle-gauge_degrees(k))<.001,(frame,angle,gauge_degrees(k))
        angles.append(angle)
    assert max(angles)-min(angles)>55
    assert abs(angles[0]-angles[-1])<.0001
    # Accumulator is the existing pressure drum, now with real emissive 3D shroud.
    jacket=bpy.data.objects[report['accumulator_jacket']]
    core=bpy.data.objects['PROCESS | horizontal copper steam drum']
    assert jacket.parent is root and core.parent is root
    assert jacket['pressure_source']==core.name
    mat=bpy.data.materials[report['accumulator_material']]
    socket=mat.node_tree.nodes['Principled BSDF'].inputs['Emission Strength']
    lamp=bpy.data.objects[report['accumulator_light']]
    assert lamp.type=='LIGHT' and lamp.parent is root
    s.frame_set(0)
    assert abs(socket.default_value)<1e-5 and lamp.data.energy<1e-5
    intensities=[]
    for k,frame in enumerate((*FRAMES,LOOP_END)):
        s.frame_set(frame);bpy.context.view_layer.update()
        got=float(socket.default_value)
        assert abs(got-heat_strength(k))<.02,(frame,got,heat_strength(k))
        assert abs(lamp.data.energy-heat_strength(k)*1.8)<.5
        intensities.append(got)
    assert max(intensities)-min(intensities)>1.45
    assert abs(intensities[0]-intensities[-1])<.001
    # Joint steam: four actual anchor objects and 4 independently phased wisps each.
    source_endpoints=source_record['solar_thermal_endpoints']
    expected={
        'west-hot-union':source_endpoints['west']['hot_drum'],
        'east-hot-union':source_endpoints['east']['hot_drum'],
        'steam-extraction-neck':[0,.22,1.05],
        'steam-output-flange':[0,1,.36]}
    vapors=[ob for ob in s.objects if ob.name.startswith('STEAM JOINT V3 | ')]
    assert len(vapors)==16 and all(ob.type=='MESH' and ob.parent is root for ob in vapors)
    for name,anchor in expected.items():
        group=[o for o in vapors if o['joint_id']==name]
        assert len(group)==4
        assert {o['phase'] for o in group}=={0,4,8,12}
        for ob in group:
            assert (Vector(ob['joint_xyz'])-Vector(anchor)).length<1e-5
            assert bpy.data.objects.get(ob['physical_anchor']) is not None
            s.frame_set(0); assert ob.hide_render
            s.frame_set(1); assert not ob.hide_render
            first=(ob.location.copy(),ob.scale.copy())
            s.frame_set(97)
            assert not ob.hide_render
            assert (first[0]-ob.location).length<1e-5
            assert (first[1]-ob.scale).length<1e-5
            s.frame_set(49); assert (ob.location-first[0]).length>.008
    # No saved production camera rotation or extra image capture cameras.
    s.frame_set(0);root.rotation_euler.z=0;bpy.context.view_layer.update()
    original_camera=camera_record(s)
    for deg in (0,90,180,270):
        root.rotation_euler.z=math.radians(deg)
        s.frame_set(25);bpy.context.view_layer.update()
        assert camera_record(s)==original_camera
    root.rotation_euler.z=0;s.frame_set(0);bpy.context.view_layer.update()
    for record in report['renders']:
        file=output/record['file']
        assert file.is_file() and sha(file)==record['sha256'], file
    assert len(report['renders'])==report['render_count']==68
    isolation=report.get('isolation',{})
    for effect in ('gauge','heat','joint-steam'):
        assert effect in isolation and len(isolation[effect])==2
        for item in isolation[effect]:
            file=output/item['file']
            assert file.is_file() and sha(file)==item['sha256']
    receipt={'schema':'tanks.solar-boiler.v3.native-reopen', 'passed':True,
        'source_v2_sha256':sha(source),'native_sha256':sha(v3_path),
        'preserved_source_mesh_count':report['original_meshes_preserved'],
        'gauge_range_degrees':[min(angles),max(angles)],
        'heat_emission_range':[min(intensities),max(intensities)],
        'steam_joint_ids':list(expected), 'steam_joint_puffs':len(vapors),
        'ports':port_checks, 'parabolic_optics':optics, 'fmpl_pbr_maps_packed':packed,
        'camera_locked':True,'loop_frame97_equals_frame1':True,
        'actual_blender_frames':68,'effect_isolation_images':6,
        'visual_approved':False,'game_integrated':False}
    (output/'native-reopen-qa.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print('SOLAR_V3_NATIVE_REOPEN_ANIMATIONS_PASS',len(vapors),len(port_checks),len(report['renders']),flush=True)


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else sys.argv[1:])
    check_scene(a.output.resolve())

if __name__=='__main__': main()
