#!/usr/bin/env python3
"""Construct an original editable Tanks Solar Boiler 3x2 using source-indexed FMPL.

Geometry is new and purpose-built, but its physical ports are the measured
Boiler V05/F MPL full-bore connector standard and it imports exact pinned
ferrocrete PBR textures from the owner's Tech-Priests catalog. No blanket
re-import of the 2x2 emergency boiler; no gameplay or sprite substitutions.

Capture: one canonical FMPL 45-degree/zero-azimuth camera, model pivot rotated
0/90/180/270 for four Factorio entity directions; icon view is NOT repeated.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
FRAMES=tuple(range(1,92,6))
DIRECTIONS=(0,90,180,270)
COLORS={
 'aged_iron':((.18,.195,.20,1),.78,.74),
 'iron_dark':((.075,.095,.105,1),.81,.81),
 'aged_copper':((.46,.215,.08,1),.47,.79),
 'bronze':((.40,.29,.12,1),.57,.78),
 'brass':((.62,.44,.175,1),.43,.8),
 'reflector':((.17,.47,.58,1),.15,.65),
 'reflector_light':((.58,.73,.75,1),.16,.60),
 'absorber':((.08,.11,.125,1),.73,.48),
 'water':((.14,.52,.69,1),.22,.12),
 'steam':((.71,.81,.87,.31),.88,0),
 'glass':((.49,.72,.76,.4),.14,.08),
 'dial':((.87,.81,.63,1),.65,.08),
 'needle':((.71,.21,.09,1),.44,.24),
}

def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def self_check():
    contract=json.loads((HERE/'port-contract.json').read_text())
    assert contract['footprint_tiles']==[3,2] and len(contract['ports'])==3
    expected={'water-west':(-1.5,-.5,.36),'water-east':(1.5,-.5,.36),
              'steam-north':(0.,1.,.36)}
    for p in contract['ports']:
        assert tuple(p['blender_flange_xyz'])==expected[p['id']]
        x,y,z=p['blender_flange_xyz']
        assert abs(z-.36)<1e-10 and (abs(x)==1.5 or abs(y)==1.)
    assert len(FRAMES)==16 and FRAMES[0]==1 and FRAMES[-1]==91
    print('SOLAR_BOILER_SOURCE_CONTRACT_PASS',flush=True)


def rgba_mat(bpy,name,source):
    color,rough,metal=source
    mat=bpy.data.materials.new('Solar Boiler | '+name)
    mat.use_nodes=True
    bsdf=mat.node_tree.nodes.get('Principled BSDF')
    bsdf.inputs['Base Color'].default_value=color
    bsdf.inputs['Roughness'].default_value=rough
    bsdf.inputs['Metallic'].default_value=metal
    if name in ('steam','glass'):
        mat.diffuse_color=color
        mat.blend_method='BLEND'
        bsdf.inputs['Alpha'].default_value=color[-1]
    elif name in ('aged_iron','iron_dark','aged_copper','bronze','brass'):
        tex=mat.node_tree.nodes.new('ShaderNodeTexNoise')
        tex.inputs['Scale'].default_value=33
        tex.inputs['Detail'].default_value=3
        bump=mat.node_tree.nodes.new('ShaderNodeBump')
        bump.inputs['Strength'].default_value=.16
        bump.inputs['Distance'].default_value=.003
        mat.node_tree.links.new(tex.outputs['Fac'],bump.inputs['Height'])
        mat.node_tree.links.new(bump.outputs['Normal'],bsdf.inputs['Normal'])
    return mat


def new_mesh(bpy,name,verts,faces,mat,collection,parent,subsurf=False):
    from mathutils import Vector
    mesh=bpy.data.meshes.new(name)
    mesh.from_pydata(verts,[],faces)
    mesh.update()
    ob=bpy.data.objects.new(name,mesh)
    collection.objects.link(ob)
    ob.parent=parent
    if mat:mesh.materials.append(mat)
    if subsurf:
        for p in mesh.polygons:p.use_smooth=True
    return ob


def move_to(bpy,obj,col,root):
    for old in tuple(obj.users_collection):old.objects.unlink(obj)
    col.objects.link(obj)
    obj.parent=root
    return obj


def brick_uv(ob,repeats=1.25):
    # Use actual tile-proportional UVs so a 3x2 slab does not stretch a 1x1 map.
    uv=ob.data.uv_layers.active
    if uv is None:uv=ob.data.uv_layers.new(name='Tile relative PBR')
    verts=ob.data.vertices
    for face in ob.data.polygons:
        no=face.normal
        for li in face.loop_indices:
            co=verts[ob.data.loops[li].vertex_index].co
            if abs(no.z)>.5:p=(co.x,co.y)
            elif abs(no.x)>.5:p=(co.y,co.z)
            else:p=(co.x,co.z)
            uv.data[li].uv=(p[0]*repeats,p[1]*repeats)


def block(bpy,name,xyz,dim,material,col,root,bevel=.018,uv=False):
    bpy.ops.mesh.primitive_cube_add(size=1,location=xyz)
    o=move_to(bpy,bpy.context.object,col,root);o.name=name
    o.scale=dim
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    if material:o.data.materials.append(material)
    if uv:brick_uv(o)
    if bevel:
        m=o.modifiers.new('Soft machined or chipped corners','BEVEL')
        m.width=min(bevel,min(dim)*.19);m.segments=2
        o.modifiers.new('Weighted broad surface normals','WEIGHTED_NORMAL')
    return o


def cyl(bpy,name,xyz,radius,depth,material,col,root,rotation=(0,0,0),segments=48):
    bpy.ops.mesh.primitive_cylinder_add(vertices=segments,radius=radius,depth=depth,location=xyz,rotation=rotation)
    o=move_to(bpy,bpy.context.object,col,root)
    o.name=name;o.data.materials.append(material)
    for p in o.data.polygons:p.use_smooth=(len(p.vertices)==4)
    m=o.modifiers.new('Rounded machined rims','BEVEL');m.width=min(depth*.08,.008);m.segments=2
    return o


def sphere(bpy,name,xyz,dim,material,col,root):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=12,ring_count=8,radius=1,location=xyz)
    o=move_to(bpy,bpy.context.object,col,root);o.name=name;o.scale=dim;o.data.materials.append(material)
    for p in o.data.polygons:p.use_smooth=True
    return o


def rod(bpy,name,a,b,radius,material,col,root):
    from mathutils import Vector
    aa=Vector(a);bb=Vector(b);d=bb-aa
    o=cyl(bpy,name,(aa+bb)/2,radius,d.length,material,col,root,segments=16)
    o.rotation_euler=d.to_track_quat('Z','Y').to_euler()
    return o


def hollow_sweep(bpy,name,points,radii,material,col,root,segments=48):
    """Actual hollow reducing pipe mesh with inner wall, outer wall and open mouths."""
    from mathutils import Vector
    ps=[Vector(p) for p in points]
    assert len(ps)==len(radii) and len(ps)>=2
    sampled=[]
    for i in range(len(ps)-1):
        a=ps[max(0,i-1)];b=ps[i];c=ps[i+1];d=ps[min(i+2,len(ps)-1)]
        for j in range(8):
            t=j/8
            p=.5*((2*b)+(-a+c)*t+(2*a-5*b+4*c-d)*t*t+(-a+3*b-3*c+d)*t*t*t)
            r=radii[i]*(1-t)+radii[i+1]*t
            sampled.append((p,r))
    sampled.append((ps[-1],radii[-1]))
    verts=[];faces=[]
    for i,(center,r) in enumerate(sampled):
        tangent=(sampled[min(i+1,len(sampled)-1)][0]-sampled[max(0,i-1)][0]).normalized()
        axis=tangent.cross(Vector((0,0,1)))
        if axis.length<.01:axis=tangent.cross(Vector((0,1,0)))
        axis.normalize();v=tangent.cross(axis).normalized()
        for radius in (r,r*(.245/.285)):
            verts.extend(center+radius*(math.cos(2*math.pi*j/segments)*axis+
                                         math.sin(2*math.pi*j/segments)*v) for j in range(segments))
    span=segments*2
    for i in range(len(sampled)-1):
        for j in range(segments):
            nj=(j+1)%segments
            a=i*span+j;b=i*span+nj;c=(i+1)*span+nj;d=(i+1)*span+j
            faces.extend(((a,b,c,d),(a+segments,d+segments,c+segments,b+segments)))
    for i in (0,len(sampled)-1):
        for j in range(segments):
            nj=(j+1)%segments;a=i*span+j;b=i*span+nj
            faces.append((a,a+segments,b+segments,b))
    return new_mesh(bpy,name,verts,faces,material,col,root,True)


def annulus(bpy,name,center,normal,outer,inner,thickness,material,col,root,segments=64):
    from mathutils import Vector
    P=Vector(center);N=Vector(normal).normalized();q=N.to_track_quat('Z','Y')
    verts=[];faces=[]
    for z,r in ((-thickness/2,outer),(thickness/2,outer),(-thickness/2,inner),(thickness/2,inner)):
        verts.extend(P+q@Vector((r*math.cos(2*math.pi*i/segments),r*math.sin(2*math.pi*i/segments),z)) for i in range(segments))
    for i in range(segments):
        j=(i+1)%segments
        faces.extend(((i,j,segments+j,segments+i),
                      (segments+i,segments+j,3*segments+j,3*segments+i),
                      (2*segments+j,2*segments+i,3*segments+i,3*segments+j),
                      (j,i,2*segments+i,2*segments+j)))
    return new_mesh(bpy,name,verts,faces,material,col,root,True)


def make_materials(bpy, fmpl_root):
    base=fmpl_root/'art/source-to-3d/shared-parts/industrial-asset-library'
    sys.path.insert(0,str(base))
    try:from import_materials import import_materials
    finally:sys.path.pop(0)
    lib=import_materials(fmpl_root,material_ids=('ferrocrete','ferrocrete_light','ferrocrete_dark'),pack=True)
    m=dict(lib)
    m.update({key:rgba_mat(bpy,key,rec) for key,rec in COLORS.items()})
    return m


def port_assembly(bpy,record,materials,col,ref,root):
    from mathutils import Vector
    P=Vector(record['blender_flange_xyz']);N=Vector(record['normal_xyz'])
    name=record['id'];inward=P-N*.20
    throat=annulus(bpy,'PORT | '+name+' | full hollow throat',P-N*.155,N,.285,.245,.31,
                   materials['aged_iron'],col,root)
    flange=annulus(bpy,'PORT | '+name+' | full machine collar',P-N*.0375,N,.34,.245,.075,
                   materials['aged_iron'],col,root)
    flange['fmpl_socket_id']=name
    flange['native_cell']=record['native_cell']
    flange['native_direction']=record['native_direction']
    flange['port_center']=list(P)
    flange['port_normal']=list(N)
    flange['standard_id']='factorio-fluid-interface-v1'
    tangent=N.cross(Vector((0,0,1)))
    if tangent.length<.01:tangent=N.cross(Vector((0,1,0)))
    tangent.normalize();up=N.cross(tangent).normalized()
    for k in range(8):
        a=k*2*math.pi/8
        pos=P + .304*(math.cos(a)*tangent+math.sin(a)*up)-N*.007
        cyl(bpy,f'PORT | {name} | flange stud {k:02d}',pos,.014,.019,materials['brass'],col,root,
            segments=8).rotation_euler=N.to_track_quat('Z','Y').to_euler()
    # Invisible adjacent reference pipe lives fully outside the 3x2 model.
    refcenter=P+N*.5
    annulus(bpy,'REF | '+name+' | one-tile barrel',refcenter,N,.285,.245,1.0,
            materials['aged_iron'],ref,root)
    annulus(bpy,'REF | '+name+' | near matching collar',P+N*.0375,N,.34,.245,.075,
            materials['aged_iron'],ref,root)
    # Reference annuli have exactly matching end-face vertices on the tile plane.
    return flange


def solar_panel(bpy,label,center,materials,col,root):
    # Thermal, not photovoltaic: reflector trough and visibly heated copper tube.
    rig=bpy.data.objects.new('SOLAR | '+label+' | adjustable trough pivot',None)
    col.objects.link(rig);rig.parent=root;rig.location=center
    frame=materials['aged_iron'];mirror=materials['reflector'];bright=materials['reflector_light']
    block(bpy,'SOLAR | '+label+' | cast reflector backing',(0,0,0),(.96,.68,.045),frame,col,rig,.02)
    for ix in range(6):
        xx=-.40+ix*.16
        block(bpy,f'SOLAR | {label} | segmented mirror strip {ix+1}',(xx,0,.041),(.142,.57,.012),
              mirror if ix%2==0 else bright,col,rig,.005)
    for yy in (-.32,.32):
        block(bpy,'SOLAR | '+label+' | folded end rail',(0,yy,.06),(1.01,.045,.10),frame,col,rig)
    for xx in (-.48,.48):
        block(bpy,'SOLAR | '+label+' | side retaining rail',(xx,0,.06),(.038,.70,.10),frame,col,rig)
    # Actual receiver tube with capped thermal manifold at its ends.
    rod(bpy,'SOLAR | '+label+' | black thermal absorber',(-.38,0,.16),(.38,0,.16),.055,
        materials['absorber'],col,rig)
    rod(bpy,'SOLAR | '+label+' | copper transfer strip',(-.36,-.08,.085),(.36,-.08,.085),.023,
        materials['aged_copper'],col,rig)
    for x in (-.32,.32):
        cyl(bpy,'SOLAR | '+label+' | absorber termination',(x,0,.16),.065,.095,
            materials['aged_copper'],col,rig,rotation=(0,math.pi/2,0))
    rig.rotation_euler.x=math.radians(21)
    for j,frame in enumerate((*FRAMES,97)):
        rig.rotation_euler.x=math.radians(21+4*math.sin(j*2*math.pi/16))
        rig.keyframe_insert(data_path='rotation_euler',frame=frame)
    rig.rotation_euler.x=math.radians(21)
    return rig


def build(args):
    import bpy
    from mathutils import Vector
    self_check()
    out=args.output.resolve();fmpl=args.fmpl_root.resolve()
    if out.exists() and any(out.iterdir()):raise FileExistsError('Never overwrite a native proof directory')
    if not (fmpl/'fmpl-stage-receipt.json').is_file():raise FileNotFoundError('Pinned FMPL PBR staging missing')
    stage=json.loads((fmpl/'fmpl-stage-receipt.json').read_text())
    if stage.get('source_commit')!='939ff2d0fea5d236d7092b907c5f08961d5a7560':
        raise ValueError('FMPL material source not pinned to verified consumer')
    contract=json.loads((HERE/'port-contract.json').read_text())
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene=bpy.context.scene;scene.name='SOLAR BOILER | 3x2 source'
    mat=make_materials(bpy,fmpl)
    def collection(name):
        c=bpy.data.collections.new(name);scene.collection.children.link(c);return c
    foundation=collection('01 | FMPL original ferrocrete PBR footing')
    mechanics=collection('02 | Thermal vessel, physically supported')
    solar=collection('03 | Two thermal collector arrays')
    pipe=collection('04 | Three actual grid-aligned boiler ports')
    operating=collection('05 | Pressure and animation')
    refs=collection('REFERENCE ONLY | adjacent matched 1-tile pipe fixtures')
    refs.hide_render=True
    root=bpy.data.objects.new('EXPORT | rotate Solar Boiler model, never camera',None)
    scene.collection.objects.link(root);root['footprint_tiles']=[3,2];root['model']='solar-boiler'
    slab=block(bpy,'FMPL | 3x2 ferrocrete continuous equipment pad',(0,0,.038),(2.94,1.94,.076),
         mat['ferrocrete'],foundation,root,.024,True)
    # Staggered physical perimeter pavers, not a fake unverified brick texture.
    for side in (-1,1):
        for i in range(5):
            x=-1.20+i*.60+.10*(i%2)
            block(bpy,'FMPL | laid exterior concrete paver',(x,side*.84,.090),(.50,.23,.047),
                  mat['ferrocrete_light'] if i%2 else mat['ferrocrete_dark'],foundation,root,.009,True)
    for x in (-.70,.70):
        for y in (-.22,.40):
            block(bpy,'SUPPORT | boiler cast seating plinth',(x,y,.19),(.22,.27,.23),
                  mat['ferrocrete_dark'],foundation,root,.016,True)
            block(bpy,'SUPPORT | rusted steel saddle shoe',(x,y,.32),(.26,.28,.055),
                  mat['aged_iron'],mechanics,root)
    # Cylindrical heat-transfer pressure drum with actual receiver lips and bands.
    cyl(bpy,'PROCESS | horizontal copper steam drum',(0,-.10,.77),.37,1.55,
        mat['aged_copper'],mechanics,root,rotation=(0,math.pi/2,0),segments=72)
    for x in (-.65,-.29,.29,.65):
        annulus(bpy,'PROCESS | cast retainer band',(x,-.10,.77),(1,0,0),.392,.34,.052,
                mat['aged_iron'],mechanics,root)
    for x in (-.73,.73):
        cyl(bpy,'PROCESS | pressure vessel round end plate',(x,-.10,.77),.315,.08,
            mat['aged_iron'],mechanics,root,rotation=(0,math.pi/2,0))
        for i in range(8):
            a=2*math.pi*i/8
            cyl(bpy,'PROCESS | service plate stud',(x+(-.048 if x<0 else .048),-.10+.278*math.cos(a),.77+.278*math.sin(a)),
                .012,.028,mat['brass'],mechanics,root,rotation=(0,math.pi/2,0),segments=8)
    # North and lateral native connections all use hollow full-bore fittings.
    for item in contract['ports']:
        port_assembly(bpy,item,mat,pipe,refs,root)
    for side in (-1,1):
        pts=[(side*1.5,-.5,.36),(side*1.22,-.5,.36),
             (side*1.03,-.48,.40),(side*.89,-.38,.53),(side*.70,-.29,.72)]
        hollow_sweep(bpy,'PROCESS | '+('west' if side<0 else 'east')+' water reducing elbow',
            pts,[.285,.285,.245,.19,.125],mat['aged_iron'],pipe,root)
        annulus(bpy,'PROCESS | water vessel receiver',(side*.73,-.30,.72),(side,0,0),
                .17,.10,.04,mat['brass'],pipe,root)
    hollow_sweep(bpy,'PROCESS | north output steam reducing downpipe',
       [(0,1,.36),(0,.79,.36),(0,.60,.43),(0,.42,.72),(0,.22,1.05)],
       [.285,.285,.24,.17,.105],mat['aged_iron'],pipe,root)
    annulus(bpy,'PROCESS | steam drum steam extraction neck',(0,.22,1.05),(0,1,0),
            .15,.10,.052,mat['brass'],pipe,root)
    # The operator can visually follow steam and heating from collectors to drum.
    for sign in (-1,1):
        cx=sign*.66
        for sy in (-.05,.57):
            rod(bpy,'SOLAR | load-bearing angled steel array support',(cx,sy,.16),(cx,sy,.99),
                .045,mat['aged_iron'],solar,root)
            block(bpy,'SOLAR | array mounting clamp',(cx,sy,.98),(.15,.14,.065),
                  mat['bronze'],solar,root)
        solar_panel(bpy,'west' if sign<0 else 'east',(cx,.25,1.17),mat,solar,root)
        hollow_sweep(bpy,'SOLAR | hot copper transfer pipe from collector',
            [(cx,.22,1.17),(cx,.10,1.08),(sign*.51,-.08,1.08),(sign*.45,-.18,1.12)],
            [.048,.048,.055,.052],mat['aged_copper'],solar,root,segments=20)
        block(bpy,'SOLAR | diagonal collector cage brace',(cx,.47,.78),(.075,.08,.70),
            mat['aged_iron'],solar,root,.01)
    # Service pressure gauge with a real moving needle and brass bezel.
    gauge=cyl(bpy,'GAUGE | enamel face',(0,-.515,.94),.155,.047,
              mat['dial'],operating,root,rotation=(math.pi/2,0,0))
    annulus(bpy,'GAUGE | brass outer rim',(0,-.542,.94),(0,-1,0),.18,.15,.032,
            mat['brass'],operating,root)
    needle=rod(bpy,'GAUGE | live pressure needle',(0,-.549,.94),(.10,-.549,.97),
        .012,mat['needle'],operating,root)
    # Simple small keyed needle rotation does not rotate the camera.
    for i,frame in enumerate((*FRAMES,97)):
        needle.rotation_euler.y=math.radians(8*math.sin(i*2*math.pi/16))
        needle.keyframe_insert(data_path='rotation_euler',frame=frame)
    # A real relief valve on the drum. Vapor originates there, never inside a wall.
    rod(bpy,'PRESSURE | relief nozzle and welded seat',(0,-.1,1.12),(0,-.1,1.36),
        .053,mat['brass'],operating,root)
    cyl(bpy,'PRESSURE | relief valve safety crown',(0,-.1,1.34),.095,.055,
        mat['aged_iron'],operating,root)
    for j,z in enumerate((1.40,1.52,1.65)):
        vapor=sphere(bpy,f'PRESSURE | short active plume {j+1}',(.025*math.sin(j),-.1+.027*j,z),
             (.10+j*.04,.09+j*.035,.055+j*.035),mat['steam'],operating,root)
        vapor.hide_render=True;vapor.keyframe_insert(data_path='hide_render',frame=0)
        vapor.hide_render=False;vapor.keyframe_insert(data_path='hide_render',frame=1)
        for k,frame in enumerate((*FRAMES,97)):
            wave=1+.16*math.sin((k+j*3)*2*math.pi/16)
            vapor.scale=((.10+j*.04)*wave,(.09+j*.035)*wave,(.055+j*.035)*wave)
            vapor.keyframe_insert(data_path='scale',frame=frame)
    # In-memory source uses one and only one authoritative FMPL camera.
    sys.path.insert(0,str(fmpl/'tools/fmpl'))
    try:
        from capture_policy import POLICY_ID
        from blender_camera_guard import install_canonical_camera, assert_clean, camera_record
    finally:sys.path.pop(0)
    cfg={'camera_policy':POLICY_ID,'capture_kind':'entity','directions':list(DIRECTIONS),
         'states':{'idle':[0],'working':list(FRAMES)},'source_size':256,
         'camera_override':{'type':'ORTHO','elevation_deg':45,'azimuth_deg':0,
              'distance':8.48528137423857,'target':[0,0,.93],
              'ortho_scale':4.45,'shift_x':0,'shift_y':0}}
    scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=args.samples
    # The runner's Cycles may omit OpenImageDenoiser entirely.
    if hasattr(scene.cycles,'use_denoising'):
        scene.cycles.use_denoising=False
    for layer in scene.view_layers:
        if hasattr(layer.cycles,'use_denoising'):
            layer.cycles.use_denoising=False

    scene.render.film_transparent=True
    scene.render.image_settings.file_format='PNG'
    scene.render.image_settings.color_mode='RGBA'
    scene.render.image_settings.color_depth='8'
    scene.render.resolution_percentage=100
    scene.render.fps=8
    scene.cycles.seed=5855;scene.cycles.use_animated_seed=False
    scene.render.threads_mode='FIXED';scene.render.threads=4
    scene.world=bpy.data.worlds.new('SOLAR | daylight sky')
    scene.world.use_nodes=True
    back=scene.world.node_tree.nodes.get('Background')
    if back:back.inputs['Color'].default_value=(.27,.32,.35,1);back.inputs['Strength'].default_value=.68
    for name,loc,power,size in (('warm sky',(-4,-5,8),700,5),('cool fill',(4,3,7),360,5)):
        data=bpy.data.lights.new('SOLAR | '+name,'AREA');data.energy=power;data.size=size
        obj=bpy.data.objects.new('SOLAR | '+name,data);scene.collection.objects.link(obj)
        obj.location=loc;obj.rotation_euler=(Vector((0,0,.8))-obj.location).to_track_quat('-Z','Y').to_euler()
    camera_receipt=install_canonical_camera(scene,cfg,bpy)
    assert_clean(scene,cfg,bpy)
    root.rotation_euler.z=0;scene.frame_set(0);bpy.context.view_layer.update()
    source_files=stage['files']
    scene['fmpl_source_commit']=stage['source_commit']
    scene['tile_footprint']=[3,2]
    scene['game_integration']=False
    scene['solar_boiler_revision']='v1-native-candidate'
    # Hidden reference fixtures stay embedded as precision test setup.
    out.mkdir(parents=True,exist_ok=True)
    native=out/'solar-boiler-v1.blend'
    bpy.ops.file.pack_all()
    bpy.ops.wm.save_as_mainfile(filepath=str(native),check_existing=False,compress=True)
    report={'schema':1,'asset':'solar-boiler','revision':'v1','active_target':'tanks_for_bob_fork_1.8.102',
            'source_commit':stage['source_commit'],'material_ids':stage['material_ids'],
            'texture_sha256s':{entry['path']:entry['sha256'] for entry in source_files if entry.get('material_id')},
            'native_sha256':digest(native),'native_reopen_passed':False,
            'footprint':[3,2],'port_standard':contract['fitting_standard'],'ports':contract['ports'],
            'camera_profile':cfg,'camera_receipt':camera_receipt,'camera':camera_record(scene),
            'idle_frames':[0],'working_frames':list(FRAMES),'directions':list(DIRECTIONS),
            'visual_approved':False,'game_integrated':False,'model_meshes':sum(o.type=='MESH' for o in scene.objects),
            'renders':[]}
    rec=out/'build-report.json'
    rec.write_text(json.dumps(report,indent=2)+'\n')
    if args.render=='none':return
    for state,timeline in (('idle',0),('working',25)):
        for i,degrees in enumerate(DIRECTIONS):
            root.rotation_euler.z=math.radians(degrees)
            scene.frame_set(timeline)
            refs.hide_render=True
            bpy.context.view_layer.update()
            assert_clean(scene,cfg,bpy)
            dest=out/(f'{state}-d{i:02d}.png')
            scene.render.filepath=str(dest)
            print('SOLAR_NATIVE_RENDER',state,i,timeline,flush=True)
            bpy.ops.render.render(write_still=True)
            report['renders'].append({'state':state,'index':i,'yaw':degrees,'frame':timeline,
                                     'file':dest.name,'sha256':digest(dest)})
            rec.write_text(json.dumps(report,indent=2)+'\n')
    root.rotation_euler.z=0;scene.frame_set(0);refs.hide_render=True
    bpy.context.view_layer.update()
    print('SOLAR_BOILER_V1_BLENDER_PROOF_COMPLETE',len(report['renders']),flush=True)


def main():
    if '--self-check' in sys.argv:
        self_check();return
    p=argparse.ArgumentParser()
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--fmpl-root',type=Path,required=True)
    p.add_argument('--render',choices=('none','proof'),default='proof')
    p.add_argument('--samples',type=int,default=24)
    args=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else sys.argv[1:])
    if not 4<=args.samples<=64:raise ValueError('Bounded samples 4..64 only')
    build(args)

if __name__=='__main__':main()
