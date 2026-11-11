#!/usr/bin/env python3
"""Solar Boiler V6: glass boilers at BOTH parabolic optical foci, gentle rumble.

Source is the immutable V5 wood-and-pipe-repair Blender file. The erroneous
above-barrel V5 glass/steam is hidden but retained as source. Both focal tubes
become editable hollow handblown glass with real 3D bubbling liquid, a moving
meniscus and staggered feathered steam from exposed relief holes near their
ends. The wooden body and mirrors shake by a fraction of a tile. Three native
pipe mouths and their outer timber sleeves remain rigid; each wooden sleeve
flexes gradually away from its fixed Factorio fitting.

No live prototypes, release, or production sprites are changed here.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
SOLAR = HERE.parent
SOURCE = SOLAR/'generated-v5'/'solar-boiler-v5.blend'
SOURCE_REPORT = SOLAR/'generated-v5'/'build-report.json'
FOCI_REPORT = SOLAR/'generated-v2'/'build-report.json'
FRAMES = tuple(range(1,92,6))
CLOSE = 97
YAW = (0,90,180,270)
TUBE_RADIUS = .095
WATER_RADIUS = .079
TUBE_LENGTH = .85
PORTS = ('water-west','water-east','steam-north')


def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def rumble(k):
    """Deterministic small 3D timber shudder. Index 16 closes at index 0."""
    q=math.tau*(k % 16)/16
    return (.014*math.sin(3*q)+.0035*math.sin(7*q+.25),
            .010*math.sin(5*q+.55),
            .008*math.sin(4*q+1.2))


def boil(k,phase=0):
    q=math.tau*(k%16)/16
    return (.50+.48*math.sin(q+phase),
            .45+.45*math.cos(2*q+phase+.7),
            .55+.44*math.sin(3*q+phase+.2))


def steam_on(tube,cap,k):
    """Phase-shifted relief spits; no steam from sealed native grid sockets."""
    k=(k+3*tube+5*cap)%16
    return k in (1,2,3,6,7,10,11)


def vent_lobe_enabled(tube,cap,phase,k):
    """Per-lobe phase modulo must close at frame 97 (k=16)."""
    index=k%16
    return steam_on(tube,cap,index) and ((index+phase*2)%3!=2)


def self_check():
    assert len(FRAMES)==16 and FRAMES[0]==1 and FRAMES[-1]==91
    assert all(abs(a-b)<1e-11 for a,b in zip(rumble(0),rumble(16)))
    assert all(abs(a-b)<1e-11 for a,b in zip(boil(0,.35),boil(16,.35)))
    for tube in (0,1):
        for cap in (0,1):
            assert steam_on(tube,cap,0)==steam_on(tube,cap,16)
        assert any(steam_on(tube,0,k)!=steam_on(tube,1,k) for k in range(16))
        for cap in (0,1):
            for phase in range(3):
                assert vent_lobe_enabled(tube,cap,phase,0)==vent_lobe_enabled(tube,cap,phase,16)
    assert max(abs(v) for k in range(16) for v in rumble(k))<.022
    assert WATER_RADIUS<TUBE_RADIUS-.012 and .75<TUBE_LENGTH<.95
    report=json.loads(SOURCE_REPORT.read_text())
    assert report['barrel_staves']==18 and report['bentwood_pipe_planks']==65
    assert len(report['patched_join_roofs'])==2 and report['wood_mirrors']==2
    foci=json.loads(FOCI_REPORT.read_text())['solar_thermal_endpoints']
    assert set(foci)=={'west','east'}
    for side in ('west','east'):
        hot,cool=foci[side]['hot_start'],foci[side]['cool_start']
        assert abs(hot[2]-cool[2])<1e-5 and abs(hot[1]-cool[1])<1e-5
        assert .89<abs(hot[0]-cool[0])<.91
    print('SOLAR_V6_FOCUS_AND_ANCHOR_MATH_PASS',flush=True)


def new_mesh(bpy,name,vertices,faces,material,col,parent,smooth=False):
    mesh=bpy.data.meshes.new(name+' | editable 3D')
    mesh.from_pydata(vertices,[],faces);mesh.update()
    ob=bpy.data.objects.new(name,mesh);col.objects.link(ob)
    ob.parent=parent
    if material:mesh.materials.append(material)
    for polygon in mesh.polygons:polygon.use_smooth=smooth
    return ob


def copy_material(bpy,name,target,kind):
    mat=bpy.data.materials[target].copy()
    mat.name=name
    mat['v6_machine_material_source']=target
    mat['v6_role']=kind
    p=next(n for n in mat.node_tree.nodes if n.type=='BSDF_PRINCIPLED')
    if kind=='glass':
        p.inputs['Base Color'].default_value=(.92,.96,.92,1)
        p.inputs['Roughness'].default_value=.075
        p.inputs['Transmission Weight'].default_value=.94
    elif kind=='fluid':
        p.inputs['Base Color'].default_value=(.12,.45,.58,1)
        p.inputs['Roughness'].default_value=.16
        p.inputs['Transmission Weight'].default_value=.50
        if p.inputs.get('Alpha'):p.inputs['Alpha'].default_value=.86
        # Keep a visible fluid core while still exposing internal bubbles.
    elif kind=='foam':
        p.inputs['Base Color'].default_value=(.93,.95,.82,1)
        if p.inputs.get('Emission Strength'):p.inputs['Emission Strength'].default_value=.12
    return mat


def tube_shell(bpy,name,x0,x1,y,z,mat,col,parent):
    n=48;steps=22;thick=.011
    vs=[];faces=[]
    for layer in (0,1):
        for i in range(steps+1):
            x=x0+(x1-x0)*i/steps
            for j in range(n):
                a=math.tau*j/n
                varying=.0015*math.sin(5*a+1.7*i)+.0008*math.cos(9*a-i*.9)
                r=TUBE_RADIUS-layer*thick+varying
                vs.append((x,y+r*math.cos(a),z+r*math.sin(a)))
    per=(steps+1)*n
    for layer in (0,1):
        for i in range(steps):
            for j in range(n):
                k=(j+1)%n;u=layer*per+i*n+j;v=layer*per+(i+1)*n+j
                faces.append((u,v,layer*per+(i+1)*n+k,layer*per+i*n+k) if layer==0 else
                             (layer*per+i*n+k,layer*per+(i+1)*n+k,v,u))
    for i in (0,steps):
        for j in range(n):
            k=(j+1)%n
            faces.append((i*n+j,i*n+k,per+i*n+k,per+i*n+j))
    ob=new_mesh(bpy,name,vs,faces,mat,col,parent,True)
    ob['focal_outer_radius']=TUBE_RADIUS;ob['glass_wall_thickness']=thick
    ob['focal_length']=x1-x0;ob['glass_has_inner_and_outer_walls']=True
    return ob


def fluid_body(bpy,name,x0,x1,y,z,mat,col,parent):
    # Lower circular liquid segment with a true 3D curved underside and upper
    # meniscus; fluid is not a billboard or entire opaque green cylinder.
    n=25;steps=24;r=WATER_RADIUS;h=.014
    offset=math.asin(h/r)
    verts=[];faces=[]
    for i in range(steps+1):
        x=(x0+.035)+(x1-x0-.070)*i/steps
        for j in range(n):
            a=math.pi-offset+(math.pi+2*offset)*j/(n-1)
            verts.append((x,y+r*math.cos(a),z+r*math.sin(a)))
    for i in range(steps):
        for j in range(n-1):
            a=i*n+j;b=(i+1)*n+j;faces.append((a,b,b+1,a+1))
        faces.append((i*n,(i+1)*n,(i+1)*n+n-1,i*n+n-1))
    faces.extend((tuple(range(n-1,-1,-1)),tuple(steps*n+j for j in range(n))))
    obj=new_mesh(bpy,name,verts,faces,mat,col,parent,True)
    obj['fluid_contained_in_focal_glass']=True
    return obj


def fluid_surface(bpy,name,x0,x1,y,z,water,foam,col,parent,phase):
    # Two independently editable shape-key meshes: a real water meniscus and
    # a brighter thin crest, each with its own keyed oscillation.
    objects=[]
    for isfoam in (False,True):
        rows=6 if isfoam else 13;cols=30
        ww=.055 if isfoam else .057
        verts=[];faces=[]
        for i in range(cols):
            x=x0+.048+(x1-x0-.096)*i/(cols-1)
            for j in range(rows):
                ty=2*j/(rows-1)-1
                yy=y+(ty*ww if not isfoam else -.058+.009*(j/(rows-1)))
                verts.append((x,yy,z+.015+(.002 if isfoam else 0)))
        for i in range(cols-1):
            for j in range(rows-1):
                a=i*rows+j;faces.append((a,a+rows,a+rows+1,a+1))
        ob=new_mesh(bpy,name+(' | churning foam crest' if isfoam else ' | moving real meniscus'),
                    verts,faces,foam if isfoam else water,col,parent,False)
        ob.shape_key_add(name='Basis')
        for label,ph,amp in (('Roil',0,.026),('Backwash',2.0,.021),('Pulse',3.8,.028)):
            shape=ob.shape_key_add(name=label)
            for i,vert in enumerate(shape.data):
                x,yy,_=verts[i]
                s=(x-x0)/(x1-x0)
                taper=max(.12,1-((yy-y)/max(ww,.001))**2) if not isfoam else 1.
                vert.co.z+=amp*taper*math.sin(math.tau*(2.2*s)+ph)
        kb=ob.data.shape_keys.key_blocks
        for frame,k in [(0,None)]+list(zip(FRAMES,range(16)))+[(CLOSE,16)]:
            values=(0.,0.,0.) if k is None else boil(k,phase+(0.6 if isfoam else 0))
            for nm,val in zip(('Roil','Backwash','Pulse'),values):
                kb[nm].value=float(val);kb[nm].keyframe_insert(data_path='value',frame=frame)
            if isfoam:
                ob.hide_render=(k is None)
                ob.keyframe_insert(data_path='hide_render',frame=frame)
        ob['v6_focal_waterline']=True
        ob['v6_rig_phase']=phase
        objects.append(ob)
    return objects


def bubbles(bpy,label,x0,x1,y,z,foam,col,parent,tube_index):
    result=[]
    for j in range(12):
        x=x0+.065+(x1-x0-.130)*(j%6)/5
        yy=y+((j%5)-2)*.018
        size=.014+.004*(j%4)
        bpy.ops.mesh.primitive_uv_sphere_add(segments=10,ring_count=7,radius=1,location=(x,yy,z))
        obj=bpy.context.object
        for prev in tuple(obj.users_collection):prev.objects.unlink(obj)
        col.objects.link(obj)
        obj.name=f'GLASS V6 | {label} | internal boiling bubble {j:02d}'
        obj.parent=parent;obj.data.materials.append(foam)
        obj['v6_boiling_bubble']=True;obj['focus_tube']=label
        for frame,k in [(0,None)]+list(zip(FRAMES,range(16)))+[(CLOSE,16)]:
            age=0 if k is None else ((k+2*j+3*tube_index)%16)/16
            obj.location=(x+.005*math.sin(math.tau*age+j),yy+.005*math.cos(math.tau*age+j),z-.045+.067*age)
            obj.scale=(size*(.85+.4*age),size*(.8+.25*age),size*(1.4+.4*age))
            obj.hide_render=(k is None)
            for prop in ('location','scale','hide_render'):obj.keyframe_insert(data_path=prop,frame=frame)
        result.append(obj)
    return result


def torus(bpy,name,center,bronze,col,parent,major=.070,minor=.010):
    bpy.ops.mesh.primitive_torus_add(major_segments=32,minor_segments=8,
                                     location=center,rotation=(0,math.pi/2,0),
                                     major_radius=major,minor_radius=minor)
    obj=bpy.context.object
    for prev in tuple(obj.users_collection):prev.objects.unlink(obj)
    col.objects.link(obj);obj.name=name;obj.parent=parent
    obj.data.materials.append(bronze)
    return obj


def feathered_steam(bpy,name,center,sign,material,col,parent,phase,tube,cap):
    # Feathered 3D gas lobes. Small irregular volumes rise from open pinhole
    # relief nozzles on focal tube collars, not from connected Factorio pipes.
    rings=9;around=16;verts=[];faces=[]
    for i in range(rings):
        t=i/(rings-1)
        radius=(.018+.032*math.sin(math.pi*t)**.9)*(1+.08*math.sin(phase*1.7))
        for j in range(around):
            angle=math.tau*j/around
            jag=1+.12*math.sin(j*3.1+i*2+phase)
            verts.append((.07*t*sign+.007*math.sin(phase+t*7)+radius*math.cos(angle)*jag,
                          .013*math.sin(t*6+phase)+radius*math.sin(angle)*jag,
                          .13*t))
    for i in range(rings-1):
        for j in range(around):
            k=(j+1)%around
            faces.append((i*around+j,(i+1)*around+j,(i+1)*around+k,i*around+k))
    faces.extend((tuple(range(around-1,-1,-1)),tuple((rings-1)*around+j for j in range(around))))
    obj=new_mesh(bpy,name,verts,faces,material,col,parent,False)
    obj.location=center
    obj['v6_steam_origin']='open focal receiver relief hole'
    obj['v6_receiver_tube']=tube;obj['v6_glass_end']=cap
    obj['v6_no_closed_pipe_leaks']=True
    for frame,k in [(0,None)]+list(zip(FRAMES,range(16)))+[(CLOSE,16)]:
        on=k is not None and vent_lobe_enabled(tube,cap,phase,k)
        age=0 if k is None else ((k+phase*3)%16)/16
        obj.hide_render=not on
        obj.location=(center[0]+sign*.025*age,center[1]+.012*math.sin(4*age+phase),center[2]+.04*age)
        obj.scale=(.9+.18*age,.9+.20*age,.8+.22*age)
        for key in ('hide_render','location','scale'):obj.keyframe_insert(data_path=key,frame=frame)
    return obj


def hide_wrong_v5_glass(bpy):
    # V5 joint roof repairs belong to the wood machine and MUST stay visible.
    removed=[]
    for group in ('10 | V5 glass accumulator, liquid and wooden joint repair',
                  '11 | V5 intentional intermittent glass-end steam vents'):
        col=bpy.data.collections[group]
        for obj in col.objects:
            if obj.name.startswith('WOOD REPAIR V5 |'):
                continue
            # Keyed hide_render cannot silently restore the misplaced vessel.
            if obj.animation_data:
                for fc in getattr(obj.animation_data.action,'fcurves',[]):
                    if fc.data_path=='hide_render':fc.mute=True
            obj.hide_render=True
            removed.append(obj.name)
    assert any('main visibly imperfect hollow accumulator' in n for n in removed)
    assert len([o for o in bpy.data.objects if o.name.startswith('WOOD REPAIR V5 |') and not o.hide_render])==2
    return removed


def anchor_flex(bpy,root,work_group):
    """Fixed pipe socket exterior, local bend in wooden conduits toward vessel."""
    fixed=[];flexed=[]
    for obj in list(bpy.data.objects):
        if obj.parent is not root or obj.type!='MESH':continue
        name=obj.name
        if not any(name.startswith('WOOD PIPE V4 | '+key+' |') for key in
                ('west water inlet','east water inlet','north steam outlet')):continue
        if obj.get('wood_role')!='curved planking on hollow conduit':
            # Wound cinch at the native mouth must stay attached and rigid.
            fixed.append(name)
            continue
        name=obj.name
        north='north steam outlet' in name
        obj.shape_key_add(name='V6 original fixed socket')
        ky=obj.shape_key_add(name='V6 local flex lateral')
        kz=obj.shape_key_add(name='V6 local flex vertical')
        ky.slider_min=kz.slider_min=-1.0
        ky.slider_max=kz.slider_max=1.0
        # V4 path_samples creates two longitudinal vertices per section and
        # two radial layers. The exterior socket is the entire FIRST section,
        # NOT one absolute-coordinate extremum (which varies across a bend).
        # Each timber stave therefore has FOUR immutable socket-end vertices.
        vertex_count=len(obj.data.vertices)
        if vertex_count%4 or vertex_count<16:
            raise RuntimeError(('Unexpected V4 bentwood stave topology',name,vertex_count))
        sections=vertex_count//4
        edge=max(v.co.y for v in obj.data.vertices) if north else max(abs(v.co.x) for v in obj.data.vertices)
        obj['v6_socket_anchor_edge']=float(edge)  # measured reference only
        obj['v6_socket_anchor_axis']='Y north' if north else 'X west-east'
        obj['v6_socket_anchor_indices']=[0,1,2*sections,2*sections+1]
        obj['v6_socket_lock_fraction']=0.125
        for i,vert in enumerate(obj.data.vertices):
            # Source layout is [outer 2*sections, inner 2*sections].
            # Hold the first 12.5% rigid, then smoothly ramp flex toward the
            # pressure barrel. No world-space flange or exposed pipe mouth moves.
            section=(i%(2*sections))//2
            u=section/(sections-1)
            ramp=min(1.,max(0.,(u-.125)/.625))
            weight=ramp*ramp*(3.-2.*ramp)
            dy=.014*weight
            dz=.010*weight
            ky.data[i].co.x+=dy if north else 0.
            ky.data[i].co.y+=0. if north else dy
            kz.data[i].co.z+=dz
        for frame,k in [(0,None)]+list(zip(FRAMES,range(16)))+[(CLOSE,16)]:
            dx,dy,dz=(0.,0.,0.) if k is None else rumble(k)
            ky.value=float((dx if north else dy)/.014)
            kz.value=float(dz/.010)
            ky.keyframe_insert(data_path='value',frame=frame)
            kz.keyframe_insert(data_path='value',frame=frame)
        obj['v6_anchor_deforms_not_mouth']=True
        flexed.append(name)
    if len(flexed)!=33:raise RuntimeError(f'Expected 33 independent fixed-socket timber sleeve planks; got {len(flexed)}')
    return flexed


def build_rumble_group(bpy,scene,root):
    group=bpy.data.objects.new('SHAKE V6 | wooden boiler and two concentrators; sockets stationary',None)
    scene.collection.objects.link(group);group.parent=root
    # Pivot stays at local model origin; all shifts remain below .022 tile.
    group.location=(0.,0.,0.)
    for obj in list(bpy.data.objects):
        if obj is group or obj is root or obj.parent is not root:continue
        if obj.type=='CAMERA' or obj.name.startswith(('PORT |','REF |')):continue
        if any(obj.name.startswith('WOOD PIPE V4 | '+key+' |') for key in
               ('west water inlet','east water inlet','north steam outlet')):continue
        if any(c.name.startswith('REFERENCE ONLY') for c in obj.users_collection):continue
        # Existing meshes have source-local vertices and identity parent inverse;
        # a zero-positioned rig preserves the entire V5 mesh layout.
        # Preserve the source's world transform when switching parents.
        original_matrix=obj.matrix_world.copy()
        obj.parent=group
        obj.matrix_world=original_matrix
    for frame,k in [(0,None)]+list(zip(FRAMES,range(16)))+[(CLOSE,16)]:
        group.location=(0.,0.,0.) if k is None else rumble(k)
        group.keyframe_insert(data_path='location',frame=frame)
    group['shake_amplitude_max_tiles']=.022
    group['ports_are_children']=False
    return group


def camera_record(scene):
    ob=scene.camera
    return {'name':ob.name,'matrix_world':[list(row) for row in ob.matrix_world],
            'type':ob.data.type,'ortho_scale':ob.data.ortho_scale,
            'shift_x':ob.data.shift_x,'shift_y':ob.data.shift_y,
            'resolution':[scene.render.resolution_x,scene.render.resolution_y]}


def render(bpy,scene,path):
    scene.render.filepath=str(path)
    print('SOLAR_V6_CYCLES_RENDER',path.name,scene.frame_current,flush=True)
    bpy.ops.render.render(write_still=True)
    return {'file':path.name,'frame':scene.frame_current,'sha256':sha(path)}


def build(args):
    import bpy
    self_check()
    if args.output.exists() and any(args.output.iterdir()):
        raise FileExistsError('V6 cannot overwrite previously captured production evidence')
    original=json.loads(SOURCE_REPORT.read_text())
    actual_sha=sha(SOURCE)
    assert actual_sha==original['native_sha256'], 'V5 source hash mismatch'
    bpy.ops.wm.open_mainfile(filepath=str(SOURCE))
    scene=bpy.context.scene
    root=bpy.data.objects['EXPORT | rotate Solar Boiler model, never camera']
    scene.frame_set(0);root.rotation_euler.z=0;bpy.context.view_layer.update()
    cam=camera_record(scene)
    assert cam==original['camera']
    assert len([x for x in bpy.data.objects if x.type=='CAMERA'])==1
    assert list(root['footprint_tiles'])==[3,2]
    old_glass=hide_wrong_v5_glass(bpy)
    # These are the real optical foci from the approved V2 geometry and
    # already saved piping, NOT an invented coordinate over the barrel.
    foci=json.loads(FOCI_REPORT.read_text())['solar_thermal_endpoints']
    old_absorbers=[]
    for name in ('west','east'):
        ob=bpy.data.objects[f'CONCENTRATOR | {name} | focal black absorber tube']
        ob.hide_render=True
        old_absorbers.append(ob.name)
    group=build_rumble_group(bpy,scene,root)
    flexed=anchor_flex(bpy,root,group)
    collection=bpy.data.collections.new('12 | V6 visible glass focal receiver boiling and relief')
    scene.collection.children.link(collection)
    glass=copy_material(bpy,'V6 | imperfect transparent focal glass',
                        'V5 | cloudy irregular handblown accumulator glass','glass')
    water=copy_material(bpy,'V6 | roiling water in paired solar foci',
                        'V5 | boiling mineral water liquid, blue-green cloudy','fluid')
    foam=copy_material(bpy,'V6 | imperfect mineral foam inside focal glass',
                       'V5 | churned water bubbles / off-white foam','foam')
    gas=bpy.data.materials['V5 | intermittent end vent feathered real steam volume'].copy()
    gas.name='V6 | plume feathering at focal receiver relief ports'
    gas['v6_role']='intermittent non-billboard volume from pinhole on focal-glass end'
    bronze=bpy.data.materials['Solar Boiler | bronze']
    tube_names=[];bubbles_count=0;vent_names=[];menisci=[]
    for tid,label in enumerate(('west','east')):
        hot,cool=foci[label]['hot_start'],foci[label]['cool_start']
        x0=min(hot[0],cool[0])+.025;x1=max(hot[0],cool[0])-.025
        y=(hot[1]+cool[1])/2;z=(hot[2]+cool[2])/2
        tube=tube_shell(bpy,f'GLASS V6 | {label} | optical focal hot-water receiver',
                        x0,x1,y,z,glass,collection,group)
        tube['v6_focal_center']=[(hot[0]+cool[0])/2,y,z]
        tube['v6_concentrator']=label
        tube['v6_not_barrel_accumulator']=True
        tube_names.append(tube.name)
        body=fluid_body(bpy,f'FLUID V6 | {label} | boiling confined fluid',x0,x1,y,z,
                        water,collection,group)
        body['v6_concentrator']=label
        menisci.extend(o.name for o in fluid_surface(bpy,f'FLUID V6 | {label}',x0,x1,y,z,
                                                      water,foam,collection,group,tid*.67))
        bubbles_count+=len(bubbles(bpy,label,x0,x1,y,z,foam,collection,group,tid))
        for cap,x in enumerate((x0,x1)):
            side=-1 if cap==0 else 1
            torus(bpy,f'FITTING V6 | {label} focal glass {cap} | tiny bronze collar',
                  (x,y,z),bronze,collection,group)
            # Small intentional upward relief hole on the glass end collar.
            torus(bpy,f'RELIEF V6 | {label} glass {cap} | leaky vent seat',
                  (x,y,z+.100),bronze,collection,group,major=.013,minor=.005)
            for j in range(3):
                vent=feathered_steam(bpy,
                    f'VENT V6 | {label} | end {cap} | soft gas lobe {j:02d}',
                    (x,y,z+.114),side,gas,collection,group,j,tid,cap)
                vent_names.append(vent.name)
    scene.frame_start=0;scene.frame_end=CLOSE
    scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=args.samples
    scene.cycles.seed=5855;scene.cycles.use_animated_seed=False
    if hasattr(scene.cycles,'use_denoising'):scene.cycles.use_denoising=False
    for layer in scene.view_layers:
        if hasattr(layer.cycles,'use_denoising'):layer.cycles.use_denoising=False
    scene.render.film_transparent=True
    scene.render.resolution_x=scene.render.resolution_y=256
    scene.render.resolution_percentage=100
    scene.render.image_settings.file_format='PNG'
    scene.render.image_settings.color_mode='RGBA';scene.render.image_settings.color_depth='8'
    scene.render.fps=8;scene.render.threads_mode='FIXED';scene.render.threads=4
    scene['solar_boiler_revision']='V6 two glass focal boil tubes and socket-anchored timber rumble'
    scene['v6_v5_sha256']=actual_sha
    scene['game_integration']=False
    scene.frame_set(0);root.rotation_euler.z=0;bpy.context.view_layer.update()
    assert camera_record(scene)==cam
    # Rigid ports must never become children of the vibrating rig.
    for port in PORTS:
        for obj in bpy.data.objects:
            if obj.name.startswith(f'PORT | {port} |'):
                assert obj.parent is root
    args.output.mkdir(parents=True,exist_ok=True)
    native=args.output/'solar-boiler-v6.blend'
    bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(native),compress=True,check_existing=False)
    report={'schema':'tanks.solar-boiler.v6.dual-focal-glass-rumble',
            'native_sha256':sha(native),'v5_source_sha256':actual_sha,
            'camera':cam,'footprint':[3,2],'fps':8,'directions':list(YAW),
            'frames':list(FRAMES),'seam':CLOSE,'glass_receiver_names':tube_names,
            'glass_focus_records':foci,'bubbles':bubbles_count,'menisci':menisci,
            'steam_vents':len(vent_names),'steam_objects':vent_names,
            'old_v5_above_barrel_hidden':len(old_glass),
            'old_absorbers_hidden':old_absorbers,
            'rumble_rig':group.name,'flexed_wood_pipe_planks':flexed,
            'wood_staves_preserved':18,'wood_conduit_planks_preserved':65,
            'polished_wood_parabolas_preserved':2,'roof_patches_preserved':2,
            'native_port_interfaces_fixed':list(PORTS),
            'visual_approved':False,'game_integrated':False,
            'renders':[],'isolation':{}}
    manifest=args.output/'build-report.json'
    manifest.write_text(json.dumps(report,indent=2)+'\n')
    if args.render=='none':return
    # One fixed camera, pivoting only the *whole* assembly for cardinal views.
    for state in ('idle','working'):
        seq=[0] if state=='idle' else (range(16) if args.render=='all' else (4,))
        for d,yaw in enumerate(YAW):
            root.rotation_euler.z=math.radians(yaw)
            for k in seq:
                scene.frame_set(0 if state=='idle' else FRAMES[k])
                bpy.context.view_layer.update()
                assert camera_record(scene)==cam
                filename=f'{state}-d{d:02d}.png' if state=='idle' else f'working-d{d:02d}-f{k:03d}.png'
                record=render(bpy,scene,args.output/filename)
                record.update({'direction':d,'state':state,'index':k})
                report['renders'].append(record)
                manifest.write_text(json.dumps(report,indent=2)+'\n')
    # True same-frame effect isolation; keys are muted for the chosen effect
    # only so the difference cannot be created by moving the camera or frame.
    root.rotation_euler.z=0;scene.frame_set(FRAMES[4]);bpy.context.view_layer.update()
    def curves(datablock,path=None):
        action=getattr(getattr(datablock,'animation_data',None),'action',None)
        return [fc for fc in (getattr(action,'fcurves',None) or [])
                if path is None or fc.data_path==path]
    def isolate(effect,objects,path,k=4):
        scene.frame_set(FRAMES[k]);bpy.context.view_layer.update()
        tracks=[]
        for ob in objects:tracks+=curves(ob,path)
        assert tracks,('Missing isolation animation curves',effect)
        states=[(fc,fc.mute) for fc in tracks]
        try:
            for fc in tracks:fc.mute=True
            for setting in ('off','on'):
                for ob in objects:
                    if path=='hide_render':ob.hide_render=(setting=='off')
                    elif path=='location':ob.location=(0,0,0) if setting=='off' else rumble(k)
                bpy.context.view_layer.update()
                f=args.output/f'iso-{effect}-{setting}.png'
                report['isolation'].setdefault(effect,[]).append(render(bpy,scene,f))
        finally:
            for fc,value in states:fc.mute=value
            scene.frame_set(FRAMES[k]-1);scene.frame_set(FRAMES[k]);bpy.context.view_layer.update()
    # Focal bubbles and steam in both receivers: measure pixels from actual 3D.
    isolate('focal-boil',[o for o in bpy.data.objects if o.get('v6_boiling_bubble')], 'hide_render')
    isolate('focal-steam',[bpy.data.objects[n] for n in vent_names],'hide_render',k=2)
    isolate('body-rumble',[group],'location')
    report['render_count']=len(report['renders'])
    manifest.write_text(json.dumps(report,indent=2)+'\n')
    root.rotation_euler.z=0;scene.frame_set(0);bpy.context.view_layer.update()
    assert sha(SOURCE)==actual_sha
    print('SOLAR_V6_GLASS_AT_FOCI_RUMBLE_CYCLES_COMPLETE',len(report['renders']),flush=True)


def main():
    if '--self-check' in sys.argv:
        self_check();return
    p=argparse.ArgumentParser()
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--samples',type=int,default=24)
    p.add_argument('--render',choices=('none','proof','all'),default='all')
    args=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else sys.argv[1:])
    if not 4<=args.samples<=64:raise ValueError('Bounded Cycles samples 4-64 only')
    build(args)

if __name__=='__main__':main()
