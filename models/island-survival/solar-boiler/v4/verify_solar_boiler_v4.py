#!/usr/bin/env python3
"""Independent saved Blender V4 validation; only source-preserving wood rebuilds pass."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import sys

import bpy
from mathutils import Vector

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[3]
assert HERE.name=='v4'
sys.path.insert(0,str(HERE))
from build_solar_boiler_v4 import FRAMES, LOOP_END, camera_record, metal_heating, mesh_hash, sha


def run(out):
    saved=out/'solar-boiler-v4.blend'
    record=json.loads((out/'build-report.json').read_text())
    assert Path(bpy.data.filepath).resolve()==saved.resolve()
    assert sha(saved)==record['native_sha256']
    source=REPO/'models/island-survival/solar-boiler/generated-v3/solar-boiler-v3.blend'
    assert sha(source)==record['source_v3_sha256']
    donor=REPO/'models/island-survival/blender/generated-v8/campfire-v8-animated.blend'
    assert sha(donor)==record['source_wood_sha256']
    s=bpy.context.scene
    root=bpy.data.objects['EXPORT | rotate Solar Boiler model, never camera']
    assert list(root['footprint_tiles'])==[3,2]
    s.frame_set(0);root.rotation_euler.z=0;bpy.context.view_layer.update()
    assert camera_record(s)==record['camera']
    assert len([o for o in bpy.data.objects if o.type=='CAMERA'])==1
    assert s.camera.data.type=='ORTHO' and not s.camera.parent
    assert s.render.fps==8 and s.render.film_transparent
    assert s.render.resolution_x==256 and s.render.resolution_y==256
    refs=bpy.data.collections['REFERENCE ONLY | adjacent matched 1-tile pipe fixtures']
    assert refs.hide_render
    # All original cold/current-native ports are untouched full-bore metal.
    contract=json.loads((REPO/'models/island-survival/solar-boiler/v1/port-contract.json').read_text())
    ports=[]
    for spec in contract['ports']:
        name=spec['id'];P=Vector(spec['blender_flange_xyz']);N=Vector(spec['normal_xyz'])
        collar=bpy.data.objects[f'PORT | {name} | full machine collar']
        ref=bpy.data.objects[f'REF | {name} | near matching collar']
        assert not collar.hide_render and collar['fmpl_socket_id']==name
        assert list(collar['native_cell'])==spec['native_cell']
        def points(o):
            return [o.matrix_world@v.co for v in o.data.vertices if abs((o.matrix_world@v.co-P).dot(N))<1e-6]
        a,b=points(collar),points(ref)
        assert len(a)==len(b)==128,(name,len(a),len(b))
        err=max(min((x-y).length for y in b) for x in a)
        assert err<1e-5,(name,err)
        ports.append({'name':name,'game_cell':spec['native_cell'],'mating_error_bu':err})
    # No industrial red-hot barrel can leak through the wood; preserved source
    # nodes remain in the Blender datablock, but its old pressure drum hidden.
    assert bpy.data.objects['PROCESS | horizontal copper steam drum'].hide_render
    assert bpy.data.objects['ACCUMULATOR V3 | red-hot cylindrical pressure drum jacket'].hide_render
    assert bpy.data.objects['ACCUMULATOR V3 | localized thermal radiation'].hide_render
    assert all(o.hide_render for o in bpy.data.objects if o.name.startswith('PROCESS | cast retainer band'))
    staves=[o for o in s.objects if o.name.startswith('WOOD V4 | barrel stave')]
    assert len(staves)==18 and all(o.type=='MESH' and o.parent is root and not o.hide_render for o in staves)
    conduits=[o for o in s.objects if o.get('wood_role')=='curved planking on hollow conduit']
    assert len(conduits)>=60,(len(conduits))
    woods=[o for o in s.objects if o.get('wood_role')]
    assert len(woods)>=80 and all(o.type=='MESH' for o in woods)
    mirrors=[]
    for side in ('west','east'):
        original=bpy.data.objects[f'CONCENTRATOR | {side} | true parabolic continuous mirror']
        fresh=bpy.data.objects[f'WOOD MIRROR V4 | {side} | polished parabolic timber surface']
        assert original.hide_render and not fresh.hide_render
        assert original.parent is fresh.parent
        assert len(original.data.vertices)==len(fresh.data.vertices)==990
        assert max((a.co-b.co).length for a,b in zip(original.data.vertices,fresh.data.vertices))<1e-8
        assert fresh.data.materials[0].name.startswith('SOLAR V4 | polished wood')
        assert len(fresh.data.uv_layers)>0
        assert abs(float(fresh['focus_height_bu'])-.28)<1e-5
        mirrors.append({'side':side,'vertices':len(fresh.data.vertices),'wood_material':fresh.data.materials[0].name})
    # Wood must actually reuse packed accepted Campfire bark/endgrain shaders.
    wood_mats=[m for m in bpy.data.materials if m.name.startswith('SOLAR V4 |') and m.get('source_material_name')]
    assert len(wood_mats)>=6
    packed=[]
    for m in wood_mats:
        textures=[n.image for n in m.node_tree.nodes if n.type=='TEX_IMAGE']
        assert len(textures)>=1 and all(im and im.packed_file for im in textures),m.name
        assert any(n.type=='TEX_NOISE' for n in m.node_tree.nodes),m.name
        assert any(n.type=='NORMAL_MAP' for n in m.node_tree.nodes),m.name
        packed.append({'name':m.name,'donor':m['source_material_name'],'maps':[im.name for im in textures]})
    # Existing canonical ferrocrete PBR untouched.
    for name in ('ferrocrete','ferrocrete_light','ferrocrete_dark'):
        mat=bpy.data.materials['TP Library | '+name]
        assert len([n for n in mat.node_tree.nodes if n.type=='TEX_IMAGE' and n.image and n.image.packed_file])==3
    # Gauge moves, but only the actual two metallic focal receiver pipes heat.
    pivot=bpy.data.objects['GAUGE V3 | real face-center needle pivot']
    angles=[]
    for frame in FRAMES:
        s.frame_set(frame);bpy.context.view_layer.update()
        angles.append(math.degrees(pivot.rotation_euler.y))
    assert max(angles)-min(angles)>50
    assert not bpy.data.objects['GAUGE | enamel face'].hide_render
    heating=[]
    for side in ('west','east'):
        tube=bpy.data.objects[f'CONCENTRATOR | {side} | focal black absorber tube']
        assert tube['solar_v4_receiving_heat_only']
        m=tube.data.materials[0]
        assert m.name.startswith('SOLAR V4 |') and 'receiver warmth' in m.name
        socket=next(n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED').inputs['Emission Strength']
        s.frame_set(0); assert socket.default_value<1e-5
        values=[]
        for i,frame in enumerate(FRAMES):
            s.frame_set(frame);bpy.context.view_layer.update();values.append(float(socket.default_value))
            assert abs(values[-1]-metal_heating(i))<.012
        s.frame_set(LOOP_END); assert abs(float(socket.default_value)-values[0])<1e-5
        assert max(values)-min(values)>.20 and max(values)<.28
        heating.append({'side':side,'emission_range':[min(values),max(values)]})
    # FMPL-style genuine 3D gas density; not opaque spheres or capped cones.
    lobes=[o for o in s.objects if o.name.startswith('STEAM V4 | open relief | lobe')]
    assert len(lobes)==12
    assert not [o for o in s.objects if o.name.startswith('STEAM JOINT V3') and not o.hide_render]
    assert all(o['emitter']=='open pressure relief valve only' for o in lobes)
    assert all(o.parent is root and o.type=='MESH' for o in lobes)
    assert len([o for o in s.objects if o.name.startswith('RELIEF V4 |')])==1
    for ob in lobes:
        mat=ob.data.materials[0]
        assert mat.node_tree.nodes.get('V4 calibrated steam optical density')
        assert any(n.type=='OUTPUT_MATERIAL' and n.inputs['Volume'].is_linked for n in mat.node_tree.nodes)
        s.frame_set(0);assert ob.hide_render
        s.frame_set(1);first=(ob.location.copy(),ob.scale.copy(),ob.hide_render)
        s.frame_set(97);last=(ob.location.copy(),ob.scale.copy(),ob.hide_render)
        assert (first[0]-last[0]).length<1e-6 and (first[1]-last[1]).length<1e-6 and first[2]==last[2]
    assert record['steam_sources']==['open-pressure-relief-nozzle']
    # Model rotations must not move the single FMPL Wube-standard camera.
    s.frame_set(0);root.rotation_euler.z=0;bpy.context.view_layer.update()
    camera=camera_record(s)
    for deg in (0,90,180,270):
        root.rotation_euler.z=math.radians(deg)
        s.frame_set(25);bpy.context.view_layer.update()
        assert camera_record(s)==camera
    root.rotation_euler.z=0;s.frame_set(0)
    for frame in record['renders']:
        path=out/frame['file']
        assert path.exists() and sha(path)==frame['sha256']
    assert len(record['renders'])==24
    receipt={'schema':'tanks.solar-boiler.v4.native-readback','passed':True,
             'source_v3_sha256':record['source_v3_sha256'],'native_sha256':record['native_sha256'],
             'barrel_staves':len(staves),'wood_plank_conduits':len(conduits),'wood_models':len(woods),
             'polished_parabolic_wood':mirrors,'wood_source_maps_packed':packed,
             'heated_metal_receivers':heating,'gauge_range_degrees':[min(angles),max(angles)],
             'steam_wisps':len(lobes),'steam_origin':'open-pressure-relief-nozzle only',
             'original_steam_source_hidden':True,'copper_drum_hidden':True,'red_jacket_hidden':True,
             'ports':ports,'camera':camera,'render_count':len(record['renders']),
             'visual_approved':False,'game_integrated':False}
    (out/'native-reopen-qa.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print('SOLAR_V4_NATIVE_REOPEN_PASS',len(staves),len(conduits),len(lobes),len(record['renders']),flush=True)


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True)
    args=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else sys.argv[1:])
    run(args.output.resolve())

if __name__=='__main__':main()
