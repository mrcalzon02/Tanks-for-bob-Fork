#!/usr/bin/env python3
"""Independent Blender V5 saved source test: wood, 3D boiling liquid and steam.

Actual native .blend must be reopened in a separate Blender process. Checks
original Factorio 3x2 pipe faces and visually significant 3D moving geometry,
not just a builder's optimistic output JSON.
"""
from __future__ import annotations
import argparse, hashlib, json, math, sys
from pathlib import Path
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from build_solar_boiler_v5 import (FRAMES,END,PORTS,CENTER,R_GLASS,R_FLUID,
    wave_values,jet_on,camera_record)

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def test(out):
    v4=HERE.parent/'generated-v4'/'solar-boiler-v4.blend'
    v4report=json.loads((HERE.parent/'generated-v4'/'build-report.json').read_text())
    native=out/'solar-boiler-v5.blend'
    report=json.loads((out/'build-report.json').read_text())
    assert Path(bpy.data.filepath).resolve()==native.resolve()
    assert sha(native)==report['native_sha256'] and sha(v4)==v4report['native_sha256']==report['v4_source_sha256']
    assert report['barrel_staves']==18 and report['bentwood_pipe_planks']==65 and report['wood_mirrors']==2
    assert report['bubble_count']>=20 and report['steam_vent_lobes']==12
    assert len(report['patched_join_roofs'])==2 and report['obsoleted_v4_relief_steam']==12
    assert report['frames']==list(FRAMES) and report['loop_seam']==END
    assert not report['game_integrated'] and not report['visual_approved']
    scene=bpy.context.scene
    root=bpy.data.objects['EXPORT | rotate Solar Boiler model, never camera']
    scene.frame_set(0);root.rotation_euler.z=0;bpy.context.view_layer.update()
    assert len([o for o in scene.objects if o.type=='CAMERA'])==1
    assert camera_record(scene)==report['camera']
    assert list(root['footprint_tiles'])==[3,2]
    wood_staves=[o for o in scene.objects if o.get('wood_role')=='rough bowed barrel planking']
    wood_conduits=[o for o in scene.objects if o.get('wood_role')=='curved planking on hollow conduit']
    mirrors=[o for o in scene.objects if o.get('wood_role')=='polished actual wood reflective parabola']
    assert len(wood_staves)==18 and len(wood_conduits)==65 and len(mirrors)==2
    for key in ('ferrocrete','ferrocrete_light','ferrocrete_dark'):
        m=bpy.data.materials['TP Library | '+key]
        assert len([n for n in m.node_tree.nodes if n.type=='TEX_IMAGE' and n.image and n.image.packed_file])==3
    # Legacy approved wood shader comes from real CF8 Firewood and packed
    # tangent normal; do not confuse it with guessed three-bitmap materials.
    assert any(m.name.startswith('CF8 | bark') for m in bpy.data.materials)
    original_steam=[o for o in scene.objects if o.name.startswith('STEAM V4 |')]
    assert len(original_steam)==12 and all(o.hide_render for o in original_steam)
    # End-cap gap repaired with annular timber, not a wooden plug in pipe bore.
    patches=[o for o in scene.objects if o.get('wood_role','').startswith('repair upper endcap gap')]
    assert len(patches)==2
    repairs=[]
    for patch in patches:
        assert patch.parent==root and patch.get('native_socket_unchanged')
        assert len(patch.data.vertices)==384
        assert len(patch.data.polygons)>100
        r0=float(patch['bore_radius']);assert abs(r0-.132)<1e-6
        yz=[(v.co.y,v.co.z) for v in patch.data.vertices]
        assert min(math.hypot(y+.29,z-.72) for y,z in yz)>=r0-1e-5
        assert any(abs(y+.29)<.013 and z>.88 for y,z in yz), 'Missing roof patch above pipe'
        repairs.append(patch.name)
    # Original 3 native port/adjacent reference fittings preserved exactly.
    contract=json.loads((HERE.parent/'v1'/'port-contract.json').read_text())
    nativeports=[]
    for port in contract['ports']:
        ident=port['id']; P=Vector(port['blender_flange_xyz']);N=Vector(port['normal_xyz'])
        machine=bpy.data.objects[f'PORT | {ident} | full machine collar']
        reference=bpy.data.objects[f'REF | {ident} | near matching collar']
        assert not machine.hide_render and machine.get('fmpl_socket_id')==ident
        assert list(machine['native_cell'])==port['native_cell']
        def points(obj):return [obj.matrix_world@v.co for v in obj.data.vertices if abs((obj.matrix_world@v.co-P).dot(N))<1e-6]
        a=points(machine);b=points(reference)
        assert len(a)==len(b)==128,(ident,len(a),len(b))
        residual=max(min((p-q).length for q in b) for p in a)
        assert residual<1e-5,(ident,residual)
        nativeports.append({'id':ident,'native_cell':port['native_cell'],'mating_error_bu':residual})
    glass=bpy.data.objects['GLASS V5 | main visibly imperfect hollow accumulator']
    liquid=bpy.data.objects['FLUID V5 | non-flat 3D glass-contained liquid body']
    surface=bpy.data.objects['FLUID V5 | physically waving liquid meniscus']
    assert glass.type==liquid.type==surface.type=='MESH'
    assert len(glass.data.vertices)>2600 and len(liquid.data.vertices)>750
    foamline=bpy.data.objects['FOAM V5 | moving three-dimensional waterline crescent']
    assert foamline.parent is root and foamline.get('v5_waterline_role','').startswith('foam at physical')
    assert len(foamline.data.vertices)==192 and len(foamline.data.shape_keys.key_blocks)==3
    assert glass.parent==liquid.parent==surface.parent==root
    assert abs(float(glass['v5_glass_outer_radius'])-R_GLASS)<1e-6
    assert float(glass['v5_glass_transmission'])>.7
    mat=glass.data.materials[0]
    assert mat.get('v5_role','').startswith('transmissive glass')
    principled=next(n for n in mat.node_tree.nodes if n.type=='BSDF_PRINCIPLED')
    assert principled.inputs['Transmission Weight'].default_value>.7
    water=liquid.data.materials[0]
    assert water.get('v5_role')=='real 3D fluid interior'
    keys=surface.data.shape_keys.key_blocks
    assert {k.name for k in keys}=={'Basis','Roil crest','Backwash','Boil pulses'}
    wavevals=[]
    for i,frame in enumerate((*FRAMES,END)):
        scene.frame_set(frame);bpy.context.view_layer.update()
        got=tuple(float(keys[name].value) for name in ('Roil crest','Backwash','Boil pulses'))
        assert all(abs(a-b)<1e-3 for a,b in zip(got,wave_values(i))), (frame,got,wave_values(i))
        wavevals.append(got)
    assert max(p[0] for p in wavevals)-min(p[0] for p in wavevals)>.7
    bubbles=[o for o in scene.objects if o.get('v5_bubble_role')=='rising bubbles inside real glass']
    assert len(bubbles)>=20
    for bubble in bubbles:
        scene.frame_set(0);assert bubble.hide_render
        scene.frame_set(1);assert not bubble.hide_render
        p=bubble.location.copy();size=bubble.scale.copy()
        scene.frame_set(97);assert (bubble.location-p).length<1e-5 and (bubble.scale-size).length<1e-5
    # Physically intermittent vent groups on each end, never a native pipe box.
    wisps=[o for o in scene.objects if o.get('v5_no_native_pipe_vapor',False)]
    assert len(wisps)==12 and all(o.type=='MESH' and o.parent==root for o in wisps)
    emitting={}
    for side in ('west','east'):
        group=[o for o in wisps if o.get('v5_steam_side')==side]
        assert len(group)==6
        series=[]
        for i,frame in enumerate(FRAMES):
            scene.frame_set(frame)
            on=not group[0].hide_render
            assert on==jet_on(side,i),(side,frame,on)
            series.append(on)
        assert any(series) and not all(series)
        scene.frame_set(97)
        assert (not group[0].hide_render)==jet_on(side,16)
        emitting[side]=sum(series)
    assert emitting['west']==7 and emitting['east']==7
    gas=wisps[0].data.materials[0]
    assert gas['v5_role'].startswith('two discrete imperfect end-cap')
    gain=gas.node_tree.nodes.get('V4 calibrated steam optical density')
    assert gain and float(gain.inputs[1].default_value)>2.5
    # Don't regress the existing glass/wood/steam pass to a single camera image.
    scene.frame_set(0);root.rotation_euler.z=0;bpy.context.view_layer.update()
    original_cam=camera_record(scene)
    for angle in (0,90,180,270):
        root.rotation_euler.z=math.radians(angle);scene.frame_set(25);bpy.context.view_layer.update()
        assert camera_record(scene)==original_cam
    root.rotation_euler.z=0;scene.frame_set(0);bpy.context.view_layer.update()
    assert len(report['renders'])==24 and len(report['isolation'])==2
    for record in report['renders']:
        image=out/record['file'];assert image.is_file() and sha(image)==record['sha256']
    for pair in report['isolation'].values():
        assert len(pair)==2
        for record in pair:
            p=out/record['file'];assert p.is_file() and sha(p)==record['sha256']
    receipt={
     'schema':'tanks.solar-boiler.v5.native-reopen','passed':True,
     'native_sha256':sha(native),'v4_source_sha256':sha(v4),
     'wood_staves':len(wood_staves),'wood_conduit_planks':len(wood_conduits),'wood_parabolic_reflectors':len(mirrors),
     'roof_socket_patches':repairs,'open_socket_hole_radius':.132,
     'glass_walls_are_thick_3d':True,'glass_transmission':principled.inputs['Transmission Weight'].default_value,
     'liquid_body_vertices':len(liquid.data.vertices),'wave_surface_vertices':len(surface.data.vertices),
     'foam_waterline_vertices':len(foamline.data.vertices),
     'shape_keys':[k.name for k in keys],'bubbles':len(bubbles),
     'steam_end_lobes':len(wisps),'steam_intervals':emitting,'existing_ports':nativeports,
     'camera_unchanged':True,'blender_loop_seam_closed':True,
     'render_count':24,'isolation_images':4,'visual_approved':False,'game_integrated':False
    }
    (out/'native-reopen-qa.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print('SOLAR_V5_NATIVE_GLASS_FLUID_GAP_AND_VENT_PASS',len(wood_staves),len(bubbles),len(wisps),len(nativeports),flush=True)


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True,type=Path)
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else sys.argv[1:])
    test(a.output.resolve())

if __name__=='__main__':main()
