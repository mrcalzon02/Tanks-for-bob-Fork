#!/usr/bin/env python3
"""Independent reopened .blend QA: focal receivers move, grid ports stay rigid."""
from __future__ import annotations
import argparse, hashlib, json, math
from pathlib import Path
import sys
import bpy
from mathutils import Vector

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from build_solar_boiler_v6 import SOURCE,SOURCE_REPORT,FRAMES,CLOSE,PORTS,rumble,boil,camera_record,sha


def check(output):
    output=output.resolve()
    native=output/'solar-boiler-v6.blend'
    report=json.loads((output/'build-report.json').read_text())
    source_report=json.loads(SOURCE_REPORT.read_text())
    assert Path(bpy.data.filepath).resolve()==native.resolve(), 'Did not reopen new native source'
    assert sha(native)==report['native_sha256']
    assert sha(SOURCE)==source_report['native_sha256']==report['v5_source_sha256']
    assert report['footprint']==[3,2]
    assert report['frames']==list(FRAMES) and report['seam']==CLOSE and report['fps']==8
    assert not report['visual_approved'] and not report['game_integrated']
    s=bpy.context.scene
    root=bpy.data.objects['EXPORT | rotate Solar Boiler model, never camera']
    group=bpy.data.objects[report['rumble_rig']]
    assert group.parent is root and root.animation_data is None
    assert len([o for o in bpy.data.objects if o.type=='CAMERA'])==1
    assert s.camera.data.type=='ORTHO' and s.camera.parent is None
    assert s.render.film_transparent and s.render.image_settings.color_mode=='RGBA'
    s.frame_set(0);root.rotation_euler.z=0;bpy.context.view_layer.update()
    assert camera_record(s)==report['camera']
    assert s.render.resolution_x==s.render.resolution_y==256

    # The erroneous V5 hero vessel, above the central barrel, is render-hidden
    # even when its original hide_render action would otherwise change frames.
    old=bpy.data.objects['GLASS V5 | main visibly imperfect hollow accumulator']
    for frame in (0,1,25,49,91,97):
        s.frame_set(frame)
        assert old.hide_render,('Wrong above-barrel glass became visible',frame)
    patches=[o for o in s.objects if o.name.startswith('WOOD REPAIR V5 | ')]
    assert len(patches)==2 and all(not p.hide_render for p in patches)
    assert all(abs(float(p['bore_radius'])-.132)<1e-6 for p in patches)
    wood_staves=[o for o in s.objects if o.get('wood_role')=='rough bowed barrel planking']
    wood_planks=[o for o in s.objects if o.get('wood_role')=='curved planking on hollow conduit']
    mirrors=[o for o in s.objects if o.get('wood_role')=='polished actual wood reflective parabola']
    assert len(wood_staves)==18 and len(wood_planks)==65 and len(mirrors)==2
    for pivot in ('SOLAR | west | adjustable trough pivot','SOLAR | east | adjustable trough pivot'):
        assert bpy.data.objects[pivot].parent is group, 'Optical concentrator not attached to rumble rig'
    for stave in wood_staves:assert stave.parent is group
    for parabolic in mirrors:
        assert parabolic.parent.parent is group

    # Exact persistent native Factorio port geometry and adjacent pipe fixtures.
    from mathutils import Vector
    contract=json.loads((HERE.parent/'v1'/'port-contract.json').read_text())
    checked=[]
    s.frame_set(0);bpy.context.view_layer.update()
    snapshots={}
    for p in contract['ports']:
        name=p['id'];P=Vector(p['blender_flange_xyz']);N=Vector(p['normal_xyz'])
        machine=bpy.data.objects['PORT | '+name+' | full machine collar']
        ref=bpy.data.objects['REF | '+name+' | near matching collar']
        assert machine.parent is root and ref.parent is root
        assert machine.get('fmpl_socket_id')==name
        assert list(machine['native_cell'])==p['native_cell']
        def face(ob):
            return [ob.matrix_world@v.co for v in ob.data.vertices
                    if abs((ob.matrix_world@v.co-P).dot(N))<1e-6]
        a=face(machine);b=face(ref)
        assert len(a)==len(b)==128,(name,len(a),len(b))
        deviation=max(min((aa-bb).length for bb in b) for aa in a)
        assert deviation<1e-5,(name,deviation)
        snapshots[name]=[vec.copy() for vec in a]
        checked.append({'id':name,'native_cell':p['native_cell'],'mating_error_bu':deviation})
    for frame in (1,7,25,49,73,91,97):
        s.frame_set(frame);bpy.context.view_layer.update()
        for name,points in snapshots.items():
            ob=bpy.data.objects['PORT | '+name+' | full machine collar']
            P=Vector(next(q['blender_flange_xyz'] for q in contract['ports'] if q['id']==name))
            N=Vector(next(q['normal_xyz'] for q in contract['ports'] if q['id']==name))
            new=[ob.matrix_world@v.co for v in ob.data.vertices
                 if abs((ob.matrix_world@v.co-P).dot(N))<1e-6]
            assert len(new)==len(points)==128
            error=max((a-b).length for a,b in zip(new,points))
            assert error<1e-6,(name,frame,error)

    # Socket flexing moves interior wood only; at native mouth every original
    # skin vertex matches the deformed shape exactly at both extreme poses.
    flexed=[bpy.data.objects[x] for x in report['flexed_wood_pipe_planks']]
    assert len(flexed)==33
    for obj in flexed:
        keys=obj.data.shape_keys
        assert keys is not None
        basis=keys.key_blocks['V6 original fixed socket']
        lat=keys.key_blocks['V6 local flex lateral']
        vert=keys.key_blocks['V6 local flex vertical']
        north='north steam outlet' in obj.name
        edge=float(obj['v6_socket_anchor_edge'])
        measured=max(v.co.y for v in basis.data) if north else max(abs(v.co.x) for v in basis.data)
        assert abs(measured-edge)<1e-5,(obj.name,measured,edge)
        fixed=0
        deform=0
        for i,v in enumerate(basis.data):
            at_port=abs((v.co.y if north else abs(v.co.x))-edge)<1e-5
            diff=max((v.co-lat.data[i].co).length,(v.co-vert.data[i].co).length)
            if at_port:
                assert diff<1e-6,(obj.name,i,diff)
                fixed+=1
            elif diff>.0001:
                deform+=1
        assert fixed>=4 and deform>0,(obj.name,fixed,deform)
    s.frame_set(1)
    start=group.location.copy()
    s.frame_set(CLOSE)
    assert (group.location-start).length<1e-6
    assert (group.location-Vector(rumble(0))).length<1e-6
    motion=[]
    for i,frame in enumerate(FRAMES):
        s.frame_set(frame);bpy.context.view_layer.update()
        assert (group.location-Vector(rumble(i))).length<1e-5
        motion.append(tuple(group.location))
    assert max((Vector(p)-Vector(motion[0])).length for p in motion)>.018
    assert max(v.length for v in map(Vector,motion))<.022

    # Glass receivers now sit along the two actual V2 optical focal lines.
    foci=report['glass_focus_records']
    tubes=[]
    surface_count=0
    for label in ('west','east'):
        name=f'GLASS V6 | {label} | optical focal hot-water receiver'
        tube=bpy.data.objects[name]
        assert tube.parent is group and tube['v6_not_barrel_accumulator']
        assert tube['glass_has_inner_and_outer_walls']
        assert .092<float(tube['focal_outer_radius'])<.098
        hot=foci[label]['hot_start'];cool=foci[label]['cool_start']
        datum=Vector(((hot[0]+cool[0])/2,(hot[1]+cool[1])/2,(hot[2]+cool[2])/2))
        error=(Vector(tube['v6_focal_center'])-datum).length
        assert error<1e-5,(label,error)
        assert abs(float(tube['v6_focal_center'][2])-1.4448555707931519)<.015
        body=bpy.data.objects[f'FLUID V6 | {label} | boiling confined fluid']
        assert body.parent is group and body['fluid_contained_in_focal_glass']
        surface=[o for o in s.objects if o.name.startswith(f'FLUID V6 | {label} |') and o.get('v6_focal_waterline')]
        assert len(surface)==2
        for surf in surface:
            keys=surf.data.shape_keys.key_blocks
            assert set(('Roil','Backwash','Pulse')).issubset({k.name for k in keys})
            s.frame_set(1);vals=tuple(keys[k].value for k in ('Roil','Backwash','Pulse'))
            s.frame_set(97)
            assert max(abs(keys[k].value-v) for k,v in zip(('Roil','Backwash','Pulse'),vals))<1e-5
        surface_count+=len(surface)
        tubes.append({'name':label,'center':list(datum),'focus_error_bu':error})
    actual_bubbles=[o for o in s.objects if o.get('v6_boiling_bubble')]
    assert len(actual_bubbles)==24
    for item in actual_bubbles:
        assert item.parent is group
        s.frame_set(0);assert item.hide_render
        s.frame_set(25);assert not item.hide_render
        s.frame_set(1);p1=item.location.copy()
        s.frame_set(97);assert (item.location-p1).length<1e-5
    vents=[o for o in s.objects if o.get('v6_steam_origin')=='open focal receiver relief hole']
    assert len(vents)==12
    groups={}
    for o in vents:
        assert o.parent is group and o['v6_no_closed_pipe_leaks']
        key=(o['v6_receiver_tube'],int(o['v6_glass_end']))
        groups.setdefault(key,[]).append(o)
    assert len(groups)==4 and all(len(v)==3 for v in groups.values())
    for key,objs in groups.items():
        ons=[]
        for frame in FRAMES:
            s.frame_set(frame)
            ons.append(any(not o.hide_render for o in objs))
        assert 1<sum(ons)<16,('Relief vent stuck on/off',key,ons)
    for o in vents:
        s.frame_set(0);assert o.hide_render
        s.frame_set(1);a=(o.location.copy(),o.scale.copy(),o.hide_render)
        s.frame_set(97);assert (o.location-a[0]).length<1e-5 and (o.scale-a[1]).length<1e-5 and o.hide_render==a[2]

    s.frame_set(0);root.rotation_euler.z=0;bpy.context.view_layer.update()
    assert camera_record(s)==report['camera']
    for yaw in (0,90,180,270):
        root.rotation_euler.z=math.radians(yaw)
        s.frame_set(25);bpy.context.view_layer.update()
        assert camera_record(s)==report['camera']
    root.rotation_euler.z=0;s.frame_set(0)
    assert len(report['renders'])==report.get('render_count')==68
    for item in report['renders']:
        file=output/item['file'];assert file.is_file() and sha(file)==item['sha256']
    assert set(report['isolation'])=={'focal-boil','focal-steam','body-rumble'}
    for records in report['isolation'].values():
        assert len(records)==2
        for item in records:
            file=output/item['file'];assert file.is_file() and sha(file)==item['sha256']
    receipt={'schema':'tanks.solar.v6.native-reopen','passed':True,
             'v5_source_sha256':sha(SOURCE),'v6_native_sha256':sha(native),
             'source_barrel_staves':18,'source_bentwood_planks':65,
             'wood_socket_repairs':len(patches),'wood_mirrors':len(mirrors),
             'focal_glass_receivers':tubes,'water_surfaces':surface_count,
             'internal_bubbles':len(actual_bubbles),'vent_lobes':len(vents),
             'independent_vent_sites':len(groups),'flexed_pipe_staves':len(flexed),
             'native_pipe_mouths_rigid':checked,'rumble_loop_verified':True,
             'fixed_camera_verified':True,'source_wrong_above_barrel_glass_hidden':True,
             'render_count':68,'visual_approved':False,'game_integrated':False}
    (output/'native-reopen-qa.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print('SOLAR_V6_NATIVE_REOPEN_FOCI_AND_FIXED_PORTS_PASS',len(tubes),len(checked),len(flexed),len(vents),flush=True)


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--output',type=Path,required=True)
    args=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else sys.argv[1:])
    check(args.output)

if __name__=='__main__':main()
