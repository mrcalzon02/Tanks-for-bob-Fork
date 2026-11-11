#!/usr/bin/env python3
"""Solar Boiler V5: wood socket repair and a real glass boiling accumulator.

Derives, never overwrites, the independently verified V4 timber production model.
The wooden pressure barrel, bentwood conduits, polished parabolic reflectors,
three actual native Factorio pipe fittings and camera are source-authoritative.
A separately supported crude glass accumulator sits over the wooden barrel;
liquid is contained in a true 3D body below animated 3D water-surface shape keys.
Two imperfect end-vent nozzles emit *intermittent* feathered volume clouds.
No gas is emitted by the three sealed grid pipe fittings.
"""
from __future__ import annotations
import argparse, hashlib, json, math, sys
from pathlib import Path

HERE=Path(__file__).resolve().parent
SOLAR=HERE.parent
V4=SOLAR/'generated-v4'/'solar-boiler-v4.blend'
V4_REPORT=SOLAR/'generated-v4'/'build-report.json'
FRAMES=tuple(range(1,92,6))
ANGLES=(0,90,180,270)
END=97
CENTER=(0.0,-.29,1.32)
R_GLASS=.169
R_FLUID=.132
LENGTH=.94
PORTS=('water-west','water-east','steam-north')


def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def wave_values(k):
    p=math.tau*(k%16)/16
    return (.58+.42*math.sin(p+.2),.54+.46*math.sin(p+2.3),.5+.5*math.sin(2*p+.6))

def jet_on(side,k):
    # No constant/symmetric vents. One end spits while the other rests.
    k=k%16
    return k in ((2,3,4,5,8,9,10) if side=='west' else (0,1,6,7,12,13,14))

def self_check():
    assert len(FRAMES)==16 and FRAMES[0]==1 and FRAMES[-1]==91
    assert all(abs(a-b)<1e-12 for a,b in zip(wave_values(0),wave_values(16)))
    assert jet_on('west',0)==jet_on('west',16)
    assert jet_on('east',0)==jet_on('east',16)
    assert any(jet_on('west',i)!=jet_on('east',i) for i in range(16))
    assert R_GLASS>R_FLUID>.1 and LENGTH<1.05
    # An off-centre 0.13-bore is wholly inside the 0.345 barrel end circle.
    assert math.hypot(-.29+.10,.72-.77)+.132<.345
    report=json.loads(V4_REPORT.read_text())
    assert report['barrel_staves']==18 and report['stave_conduit_planks']==65
    assert len(report['polished_wood_mirrors'])==2
    print('SOLAR_V5_PYTHON_MATH_AND_WOOD_CONTRACT_PASS')


def new_mesh(bpy,name,vs,fs,mat,col,root,smooth=False):
    mesh=bpy.data.meshes.new(name+' | editable geometry')
    mesh.from_pydata(vs,[],fs);mesh.update()
    ob=bpy.data.objects.new(name,mesh);col.objects.link(ob);ob.parent=root
    if mat:mesh.materials.append(mat)
    for polygon in mesh.polygons:polygon.use_smooth=smooth
    if mat and (mat.get('v5_grain_uv',False) or mat.name.startswith('CF8 |')):
        uv=mesh.uv_layers.new(name='Source-approved wood grain UV')
        for poly in mesh.polygons:
            for li in poly.loop_indices:
                p=mesh.vertices[mesh.loops[li].vertex_index].co
                uv.data[li].uv=(p.x*2.25+.5,p.y*2.3+p.z*.85)
    return ob


def glass_material(bpy):
    # Derivative of historical Solar Boiler glass settings; *not* an imported
    # approved FMPL FX library or invented external texture source.
    historic=bpy.data.materials.get('Solar Boiler | glass')
    # V4 purges unused V1 material datablocks; build a source-traceable,
    # explicitly candidate FMPL-guided glass shader when that happens.
    # Never substitute a flat alpha image or claim to import a missing library.
    mat=historic.copy() if historic is not None else bpy.data.materials.new('V5 | handblown glass procedural PBR source')
    mat.name='V5 | cloudy irregular handblown accumulator glass'
    mat.use_nodes=True
    bsdf=next(x for x in mat.node_tree.nodes if x.type=='BSDF_PRINCIPLED')
    bsdf.inputs['Base Color'].default_value=(.91,.97,.94,1)
    bsdf.inputs['Roughness'].default_value=.067
    bsdf.inputs['Metallic'].default_value=0
    for name,value in [('Transmission Weight',.96),('IOR',1.47),('Alpha',.33)]:
        if bsdf.inputs.get(name):bsdf.inputs[name].default_value=value
    noise=mat.node_tree.nodes.new('ShaderNodeTexNoise')
    noise.name='V5 handblown irregular glass thickness'
    noise.inputs['Scale'].default_value=25
    noise.inputs['Detail'].default_value=3
    bump=mat.node_tree.nodes.new('ShaderNodeBump')
    bump.name='V5 fine glass warp (not uniformly polished)'
    bump.inputs['Distance'].default_value=.0018
    bump.inputs['Strength'].default_value=.10
    mat.node_tree.links.new(noise.outputs['Fac'],bump.inputs['Height'])
    mat.node_tree.links.new(bump.outputs['Normal'],bsdf.inputs['Normal'])
    # Thin, irregular glass must reveal the water and visible upper airspace.
    # A genuine BSDF transparency mix avoids the opaque grainy aqua shell from
    # the first Cycles attempt while retaining refraction and imperfections.
    output=next(n for n in mat.node_tree.nodes if n.type=='OUTPUT_MATERIAL')
    for link in list(output.inputs['Surface'].links):mat.node_tree.links.remove(link)
    transparent=mat.node_tree.nodes.new('ShaderNodeBsdfTransparent')
    mix=mat.node_tree.nodes.new('ShaderNodeMixShader')
    mix.name='V5 | rough glass versus clear visible interior'
    mix.inputs[0].default_value=.46
    mat.node_tree.links.new(transparent.outputs[0],mix.inputs[1])
    mat.node_tree.links.new(bsdf.outputs['BSDF'],mix.inputs[2])
    mat.node_tree.links.new(mix.outputs[0],output.inputs['Surface'])
    mat['v5_role']='transmissive glass showing actual animated fluid, not colored metal'
    return mat


def water_material(bpy):
    historic=bpy.data.materials.get('Solar Boiler | water')
    # The former water material is not necessarily saved when unused in V4.
    # This is a separately editable PBR material with documented FMPL
    # liquid/transmission conventions; wood PBR remains inherited unchanged.
    mat=historic.copy() if historic is not None else bpy.data.materials.new('V5 | mineral water procedural PBR source')
    mat.name='V5 | boiling mineral water liquid, blue-green cloudy'
    mat.use_nodes=True
    bsdf=next(x for x in mat.node_tree.nodes if x.type=='BSDF_PRINCIPLED')
    bsdf.inputs['Base Color'].default_value=(.09,.39,.49,1)
    bsdf.inputs['Roughness'].default_value=.16
    bsdf.inputs['Metallic'].default_value=0
    for name,value in [('Transmission Weight',.19),('IOR',1.33),('Alpha',.93)]:
        if bsdf.inputs.get(name):bsdf.inputs[name].default_value=value
    tex=mat.node_tree.nodes.new('ShaderNodeTexNoise')
    tex.name='V5 suspended mineral turbidity / procedural'
    tex.inputs['Scale'].default_value=19
    tex.inputs['Detail'].default_value=2.7
    bump=mat.node_tree.nodes.new('ShaderNodeBump')
    bump.inputs['Strength'].default_value=.18
    bump.inputs['Distance'].default_value=.004
    mat.node_tree.links.new(tex.outputs['Fac'],bump.inputs['Height'])
    mat.node_tree.links.new(bump.outputs['Normal'],bsdf.inputs['Normal'])
    mat['v5_role']='real 3D fluid interior'
    return mat


def foam_material(bpy):
    m=bpy.data.materials.new('V5 | churned water bubbles / off-white foam')
    m.use_nodes=True
    p=m.node_tree.nodes.get('Principled BSDF')
    p.inputs['Base Color'].default_value=(.85,.94,.92,1)
    p.inputs['Roughness'].default_value=.44
    if p.inputs.get('Alpha'):p.inputs['Alpha'].default_value=.93
    if p.inputs.get('Emission Color'):p.inputs['Emission Color'].default_value=(.65,.83,.83,1)
    if p.inputs.get('Emission Strength'):p.inputs['Emission Strength'].default_value=.22
    return m


def glass_shell(bpy,col,root,mat):
    # True annular open-wall glass, physically ripply instead of a flat image.
    n=56;steps=26;vs=[];fs=[]
    for inner in (False,True):
        radius=R_GLASS-(.014 if inner else 0)
        for i in range(steps+1):
            x=-LENGTH/2+LENGTH*i/steps
            offset=.0032*math.sin(i*1.5)
            for j in range(n):
                a=math.tau*j/n
                r=radius+.002*math.sin(4*a+1.7*i)+.0013*math.cos(9*a-i*.6)
                vs.append((x,CENTER[1]+(r+offset)*math.cos(a),CENTER[2]+r*math.sin(a)))
    span=(steps+1)*n
    for layer in (0,1):
        for i in range(steps):
            for j in range(n):
                k=(j+1)%n;u=layer*span+i*n+j;v=layer*span+(i+1)*n+j
                fs.append((u,v,layer*span+(i+1)*n+k,layer*span+i*n+k) if layer==0 else
                          (layer*span+i*n+k,layer*span+(i+1)*n+k,v,u))
    for at in (0,steps):
        for j in range(n):
            k=(j+1)%n;fs.append((at*n+j,at*n+k,span+at*n+k,span+at*n+j))
    ob=new_mesh(bpy,'GLASS V5 | main visibly imperfect hollow accumulator',vs,fs,mat,col,root,True)
    ob['v5_glass_outer_radius']=R_GLASS
    ob['v5_glass_inner_radius']=R_GLASS-.014
    ob['v5_glass_length']=LENGTH
    ob['v5_glass_transmission']=.96
    return ob


def ring(bpy,name,x,y,z,ro,ri,thick,mat,col,root,n=40):
    # Hollow annular connector; never block a real native Factorio fluid bore.
    vs=[];fs=[]
    for xp,r in ((x-thick/2,ro),(x+thick/2,ro),(x-thick/2,ri),(x+thick/2,ri)):
        vs.extend((xp,y+r*math.cos(math.tau*j/n),z+r*math.sin(math.tau*j/n)) for j in range(n))
    for j in range(n):
        k=(j+1)%n
        fs.extend(((j,k,n+k,n+j),(n+j,n+k,3*n+k,3*n+j),
                   (2*n+k,2*n+j,3*n+j,3*n+k),(j,2*n+j,2*n+k,k)))
    return new_mesh(bpy,name,vs,fs,mat,col,root,True)


def fluid_body(bpy,col,root,water):
    x0=-LENGTH/2+.042;x1=LENGTH/2-.042
    # Filled curved segment *inside* the glass, not a planar blue overlay.
    n=33;steps=24;r=R_FLUID;h=.021;offset=math.asin(h/r)
    vs=[];faces=[]
    for k in range(steps+1):
        x=x0+(x1-x0)*k/steps
        for j in range(n):
            a=math.pi-offset+(math.pi+2*offset)*j/(n-1)
            vs.append((x,CENTER[1]+r*math.cos(a),CENTER[2]+r*math.sin(a)))
    for i in range(steps):
        for j in range(n-1):
            a=i*n+j;b=(i+1)*n+j
            faces.append((a,b,b+1,a+1))
        # Water top, drawn by its own moving surface just above this top face.
        faces.append((i*n,(i+1)*n,(i+1)*n+n-1,i*n+n-1))
    faces.extend((tuple(range(n-1,-1,-1)),tuple(steps*n+j for j in range(n))))
    body=new_mesh(bpy,'FLUID V5 | non-flat 3D glass-contained liquid body',vs,faces,water,col,root,True)
    body['v5_liquid_fill_level']=h
    body['v5_liquid_radius']=r
    return body


def fluid_surface(bpy,col,root,water):
    rows=15;cols=32;chord=math.sqrt(R_FLUID**2-.021**2)-.007
    x0=-LENGTH/2+.055;x1=LENGTH/2-.055
    vs=[];faces=[]
    for i in range(cols):
        x=x0+(x1-x0)*i/(cols-1)
        for j in range(rows):
            y=CENTER[1]+(2*j/(rows-1)-1)*chord
            vs.append((x,y,CENTER[2]+.022))
    for i in range(cols-1):
        for j in range(rows-1):
            k=i*rows+j;faces.append((k,k+rows,k+rows+1,k+1))
    ob=new_mesh(bpy,'FLUID V5 | physically waving liquid meniscus',vs,faces,water,col,root,False)
    ob.shape_key_add(name='Basis')
    for label,seed in [('Roil crest',0.0),('Backwash',2.1),('Boil pulses',4.5)]:
        shape=ob.shape_key_add(name=label)
        for index,v in enumerate(shape.data):
            x,y,_=vs[index]
            u=(x-x0)/(x1-x0);vcoord=(y-CENTER[1])/chord
            envelope=max(0,1-vcoord*vcoord)
            shape.data[index].co.z += (.017 if label!='Boil pulses' else .024)*envelope*math.sin(2.8*math.tau*u + 2*vcoord+seed)
    keys=ob.data.shape_keys.key_blocks
    for f,index in [(0,None)]+[(fr,k) for k,fr in enumerate(FRAMES)]+[(END,16)]:
        values=(0,0,0) if index is None else wave_values(index)
        for label,value in zip(('Roil crest','Backwash','Boil pulses'),values):
            keys[label].value=float(value)
            keys[label].keyframe_insert(data_path='value',frame=f)
    return ob



def waterline_foam(bpy,col,root,foam):
    # An actual wavy, three-dimensional light foam rim at the liquid-air
    # boundary, inside the glass at the front edge visible to the one camera.
    # Not an image plane, sprite overlay or flat screen-facing billboard.
    nx=48;ny=4;vs=[];fs=[]
    x0=-LENGTH/2+.055;x1=LENGTH/2-.055
    for i in range(nx):
        x=x0+(x1-x0)*i/(nx-1)
        for j in range(ny):
            y=CENTER[1]-.119+.007*j
            z=CENTER[2]+.022+.005*math.sin(math.tau*4*i/(nx-1))
            vs.append((x,y,z))
    for i in range(nx-1):
        for j in range(ny-1):
            a=i*ny+j;fs.append((a,a+ny,a+ny+1,a+1))
    obj=new_mesh(bpy,'FOAM V5 | moving three-dimensional waterline crescent',vs,fs,foam,col,root,False)
    obj['v5_waterline_role']='foam at physical meniscus, inside crude glass'
    obj.shape_key_add(name='Basis')
    swell=obj.shape_key_add(name='Churned waterline')
    chop=obj.shape_key_add(name='Breaking turbulent crest')
    for i,(x,y,z) in enumerate(vs):
        phase=math.tau*(x-x0)/(x1-x0)
        swell.data[i].co.z=z+.010*math.sin(phase*3.6)
        chop.data[i].co.z=z+.014*math.sin(phase*7.5+.9)
    keys=obj.data.shape_keys.key_blocks
    for frame,index in [(0,None)]+[(f,k) for k,f in enumerate(FRAMES)]+[(END,16)]:
        v=(0,0) if index is None else (.50+.50*math.sin(math.tau*index/16),
                                    .50+.50*math.cos(math.tau*2*index/16))
        for name,amount in zip(('Churned waterline','Breaking turbulent crest'),v):
            keys[name].value=float(amount)
            keys[name].keyframe_insert(data_path='value',frame=frame)
        obj.hide_render=index is None
        obj.keyframe_insert(data_path='hide_render',frame=frame)
    return obj


def bubbles(bpy,col,root,foam,count=22):
    result=[]
    for j in range(count):
        x=(j%11-5)*.071+.007*math.sin(j*2.7)
        y=CENTER[1]+((j%5)-2)*.045
        size=.016+.008*((j*7)%5)/4
        bpy.ops.mesh.primitive_uv_sphere_add(segments=12,ring_count=8,radius=1.0,location=(x,y,CENTER[2]-.05))
        ob=bpy.context.object
        for old in tuple(ob.users_collection):old.objects.unlink(ob)
        col.objects.link(ob);ob.parent=root
        ob.name=f'BOILING V5 | genuine fluid bubble {j:02d}'
        ob.data.materials.append(foam)
        ob['v5_bubble_index']=j;ob['v5_bubble_role']='rising bubbles inside real glass'
        for frame,index in [(0,None)]+[(fr,k) for k,fr in enumerate(FRAMES)]+[(END,16)]:
            age=0 if index is None else ((index+3*j)%16)/16
            ob.location=(x+.008*math.sin(j+age*math.tau),y+.006*math.cos(j+age*math.tau),CENTER[2]-.105+age*.120)
            ob.scale=(size*(1+.15*age),size*(.77+.17*age),size*(1.25+.28*age))
            ob.hide_render=index is None
            for p in ('location','scale','hide_render'):ob.keyframe_insert(data_path=p,frame=frame)
        result.append(ob)
    return result


def wood_joint_patch(bpy,side,col,root,mat):
    """Fill the gap above the bentwood inlet while leaving its real bore open.

    A deliberately offset hole fits the north/south inner wooden sockets. The
    outer patch ring is clipped to the *wooden barrel end* circular envelope.
    """
    n=96;R=.343;yc,zc=-.10,.77;py,pz=-.29,.72;ri=.132
    offset=(py-yc,pz-zc)
    # Four surfaces: front/back ring at x=.791, inset x=.770, plus inner rim.
    verts=[];faces=[]
    x0=side*.789;x1=side*.765
    for x in (x0,x1):
        for layer in ('outer','inner'):
            for i in range(n):
                a=math.tau*i/n;uy,uz=math.cos(a),math.sin(a)
                dot=offset[0]*uy+offset[1]*uz
                edge=-dot+math.sqrt(dot*dot+R*R-offset[0]**2-offset[1]**2)
                rad=max(ri+.007,min(.238,edge-.012)) if layer=='outer' else ri
                verts.append((x,py+rad*uy,pz+rad*uz))
    # rings: front outer(0),front inner(n), back outer(2n), back inner(3n)
    for i in range(n):
        k=(i+1)%n
        faces.extend(((i,k,n+k,n+i),(2*n+k,2*n+i,3*n+i,3*n+k),
                      (i,2*n+i,2*n+k,k),(n+k,3*n+k,3*n+i,n+i)))
    ob=new_mesh(bpy,f'WOOD REPAIR V5 | {side} | closed gap above actual side conduit',verts,faces,mat,col,root,False)
    ob['wood_role']='repair upper endcap gap while preserving open circular major-pipe bore'
    ob['native_socket_unchanged']=True
    ob['bore_radius']=ri
    ob['barrel_end_clip_radius']=R
    return ob


def steam_material(bpy):
    canonical=bpy.data.materials.get('SOLAR V4 | real feathered steam volume')
    if not canonical:raise RuntimeError('V4 noise-feathered gas shader missing')
    m=canonical.copy();m.name='V5 | intermittent end vent feathered real steam volume'
    gain=m.node_tree.nodes.get('V4 calibrated steam optical density')
    if not gain:raise RuntimeError('Original verified self-feathering steam node missing')
    # A static density gain independent of the saved animation state.
    gain.inputs[1].default_value=3.0
    m['v5_role']='two discrete imperfect end-cap steam jets, no sealed pipe leaks'
    return m


def steam_lobe(bpy,side,j,col,root,material):
    # Irregular volume mesh, 10 sections of an upward/outward jet, not balls.
    sign=-1 if side=='west' else 1
    n=18;sec=10;verts=[];faces=[]
    for k in range(sec):
        t=k/(sec-1)
        spread=(.028+.047*math.sin(math.pi*t)**.8)*(1+.07*math.sin(j*1.4))
        x=sign*(LENGTH/2+.06+.20*t)+.012*math.sin(j+t*5)
        y=CENTER[1]+.013*math.cos(j+t*4)
        z=CENTER[2]+.015+.16*t+.009*math.sin(j+t*6)
        for a in range(n):
            theta=math.tau*a/n
            perturb=1+.16*math.sin(4*theta+3*t+j)
            verts.append((x,y+spread*math.cos(theta)*perturb,z+spread*math.sin(theta)*perturb))
    for k in range(sec-1):
        for a in range(n):
            b=(a+1)%n
            faces.append((k*n+a,(k+1)*n+a,(k+1)*n+b,k*n+b))
    faces.extend((tuple(range(n-1,-1,-1)),tuple((sec-1)*n+a for a in range(n))))
    ob=new_mesh(bpy,f'VENT V5 | {side} | intermittent feathered 3D steam {j:02d}',verts,faces,material,col,root,True)
    ob['v5_steam_side']=side;ob['v5_steam_lobe']=j
    ob['v5_emitter']='deliberately vented end of glass accumulator'
    ob['v5_no_native_pipe_vapor']=True
    for frame,index in [(0,None)]+[(fr,k) for k,fr in enumerate(FRAMES)]+[(END,16)]:
        state=False if index is None else jet_on(side,index)
        ob.hide_render=not state
        age=0 if index is None else ((index+j*2)%16)/16
        ob.location=(sign*.012*math.sin(age*math.tau+j),.014*math.sin(age*math.tau+j*1.7),.035*age)
        scale=(.85+.14*age)*(1+.05*math.sin(j+age*math.tau))
        ob.scale=(scale,scale,.86+.20*age)
        for p in ('hide_render','location','scale'):ob.keyframe_insert(data_path=p,frame=frame)
    return ob


def render_one(bpy,scene,path):
    scene.render.filepath=str(path)
    print('SOLAR_V5_CYCLES_FRAME',path.name,scene.frame_current,flush=True)
    bpy.ops.render.render(write_still=True)
    return {'file':path.name,'sha256':sha(path),'frame':scene.frame_current}


def camera_record(s):
    c=s.camera
    return {'name':c.name,'matrix_world':[list(v) for v in c.matrix_world],
      'type':c.data.type,'ortho_scale':c.data.ortho_scale,
      'shift_x':c.data.shift_x,'shift_y':c.data.shift_y,
      'resolution':[s.render.resolution_x,s.render.resolution_y]}


def build(opts):
    import bpy
    self_check()
    src=V4.resolve()
    if not src.is_file():raise FileNotFoundError(src)
    report4=json.loads(V4_REPORT.read_text());source_hash=sha(src)
    assert source_hash==report4['native_sha256'],'Verified V4 source SHA mismatch'
    if opts.output.exists() and any(opts.output.iterdir()):raise FileExistsError('Refusing to overwrite prior V5 evidence')
    bpy.ops.wm.open_mainfile(filepath=str(src))
    scene=bpy.context.scene
    root=bpy.data.objects['EXPORT | rotate Solar Boiler model, never camera']
    scene.frame_set(0);root.rotation_euler.z=0;bpy.context.view_layer.update()
    camera=camera_record(scene)
    assert camera==report4['camera'] and len([o for o in bpy.data.objects if o.type=='CAMERA'])==1
    assert list(root['footprint_tiles'])==[3,2]
    wood=bpy.data.materials.get(report4['wood_source_materials'][0]);light=bpy.data.materials.get(report4['wood_source_materials'][1])
    assert wood and light
    # Keep all actual native port geometry; both wooden end joins require patches.
    for name in PORTS:
        o=bpy.data.objects[f'PORT | {name} | full machine collar']
        assert o.type=='MESH' and not o.hide_render
    old_names=[o.name for o in bpy.data.objects if o.type=='MESH']
    old_mesh_counts={name:len(bpy.data.objects[name].data.vertices) for name in old_names}
    base_col=bpy.data.collections.new('10 | V5 glass accumulator, liquid and wooden joint repair')
    scene.collection.children.link(base_col)
    fx_col=bpy.data.collections.new('11 | V5 intentional intermittent glass-end steam vents')
    scene.collection.children.link(fx_col)
    # Keep the original V4 relief hardware, but deactivate its atmospheric gas.
    old_relief=[]
    for ob in bpy.data.objects:
        if ob.name.startswith('STEAM V4 |'):
            if ob.animation_data:ob.animation_data_clear()
            ob.hide_render=True
            ob['v5_obsolete_atmospheric_steam']='superseded by two glass endcap vents'
            old_relief.append(ob.name)
    assert len(old_relief)==12
    # Correct the hole left by deliberate V4 wooden end-cap trimming.
    patches=[wood_joint_patch(bpy,side,base_col,root,wood) for side in (-1,1)]
    glass=glass_material(bpy);water=water_material(bpy);foam=foam_material(bpy)
    shell=glass_shell(bpy,base_col,root,glass)
    liquid=fluid_body(bpy,base_col,root,water)
    waves=fluid_surface(bpy,base_col,root,water)
    foamline=waterline_foam(bpy,base_col,root,foam)
    bubbles_list=bubbles(bpy,base_col,root,foam)
    metal=bpy.data.materials.get('Solar Boiler | bronze')
    if not metal:raise RuntimeError('Existing small bronze fittings material is absent')
    for side in (-1,1):
        # Wood trestles actually touch barrel and lower glass under the end.
        name='west' if side<0 else 'east';x=side*.368
        for y in (CENTER[1]-.090,CENTER[1]+.090):
            bpy.ops.mesh.primitive_cube_add(size=1,location=(x,y,1.106))
            ob=bpy.context.object
            for old in tuple(ob.users_collection):old.objects.unlink(ob)
            base_col.objects.link(ob);ob.parent=root
            ob.name=f'WOOD V5 | {name} | crude upright accumulator saddle'
            ob.scale=(.078,.072,.073);ob.data.materials.append(light)
            ob['wood_role']='glass vessel held in notched rough timber cradle'
        # Both end membranes are actual punctured glass disks rather than flat caps.
        x=side*(LENGTH/2+.003)
        cap=ring(bpy,f'GLASS V5 | {name} | vented cloudy glass endcap',x,CENTER[1],CENTER[2],.153,.032,.020,glass,base_col,root)
        cap['v5_end_vent_side']=name
        ring(bpy,f'FITTING V5 | {name} | narrow seated metal edge ring',x,CENTER[1],CENTER[2],.176,.151,.032,metal,base_col,root)
        ring(bpy,f'FITTING V5 | {name} | deliberately leaky end vent',side*(LENGTH/2+.019),CENTER[1],CENTER[2],.061,.031,.028,metal,base_col,root)
    gas=steam_material(bpy)
    clouds=[steam_lobe(bpy,s,j,fx_col,root,gas) for s in ('west','east') for j in range(6)]
    # Retain all source vertices; only hide_render changes on previous relief steam.
    for name,count in old_mesh_counts.items():
        assert len(bpy.data.objects[name].data.vertices)==count,('V4 source mesh modified',name)
    scene['solar_boiler_revision']='V5 glass accumulator, active fluid and wooden socket repairs'
    scene['solar_boiler_v4_sha256']=source_hash
    scene['game_integration']=False
    scene.frame_start=0;scene.frame_end=END
    scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=opts.samples
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
    scene.frame_set(0);root.rotation_euler.z=0;bpy.context.view_layer.update()
    assert camera_record(scene)==camera
    opts.output.mkdir(parents=True,exist_ok=True)
    native=opts.output/'solar-boiler-v5.blend'
    bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(native),compress=True,check_existing=False)
    report={
      'schema':'tanks.solar-boiler.v5.glass-liquid.v1',
      'native_sha256':sha(native),'v4_source_sha256':source_hash,
      'v4_original_mesh_count':len(old_mesh_counts),
      'barrel_staves':18,'bentwood_pipe_planks':65,'wood_mirrors':2,
      'patched_join_roofs':[o.name for o in patches],
      'glass_accumulator':shell.name,'fluid_body':liquid.name,'fluid_surface':waves.name,'waterline_foam':foamline.name,
      'bubble_count':len(bubbles_list),'steam_vent_lobes':len(clouds),
      'obsoleted_v4_relief_steam':len(old_relief),
      'glass_properties':{'length':LENGTH,'outer_radius':R_GLASS,'interior_radius':R_GLASS-.014},
      'steam_vents':['west-glass-endcap','east-glass-endcap'],
      'frames':list(FRAMES),'loop_seam':END,'fps':8,'camera':camera,
      'port_geometry_preserved':list(PORTS),
      'renders':[],'isolation':{},'visual_approved':False,'game_integrated':False
    }
    manifest=opts.output/'build-report.json';manifest.write_text(json.dumps(report,indent=2)+'\n')
    if opts.render=='none':return
    refs=bpy.data.collections['REFERENCE ONLY | adjacent matched 1-tile pipe fixtures'];refs.hide_render=True
    # Four idle/working perspectives plus 16 north working poses.
    for state,frame in [('idle',0),('working',25)]:
        for i,angle in enumerate(ANGLES):
            scene.frame_set(frame);root.rotation_euler.z=math.radians(angle)
            bpy.context.view_layer.update()
            rec=render_one(bpy,scene,opts.output/f'{state}-d{i:02d}.png')
            rec.update({'state':state,'yaw':angle});report['renders'].append(rec)
            manifest.write_text(json.dumps(report,indent=2)+'\n')
    root.rotation_euler.z=0
    for k,frame in enumerate(FRAMES):
        scene.frame_set(frame);bpy.context.view_layer.update()
        rec=render_one(bpy,scene,opts.output/f'working-north-f{k:03d}.png')
        rec['sample']=k;report['renders'].append(rec)
        manifest.write_text(json.dumps(report,indent=2)+'\n')
    # Same-frame Cycles comparisons. Mute relevant fcurves or Blender will
    # reapply animation and make both control images accidentally identical.
    scene.frame_set(25);bpy.context.view_layer.update()
    def curves(data):
        action=getattr(getattr(data,'animation_data',None),'action',None)
        return list(getattr(action,'fcurves',[]) or [])
    all_wave_curves=curves(waves.data.shape_keys)+curves(foamline.data.shape_keys)
    foam_hide_curves=[fc for fc in curves(foamline) if fc.data_path=='hide_render']
    all_bubble_hide=[fc for ob in bubbles_list for fc in curves(ob) if fc.data_path=='hide_render']
    all_jet_hide=[fc for ob in clouds for fc in curves(ob) if fc.data_path=='hide_render']
    def capture_iso(name,trackset,changes):
        assert trackset,'No fcurves for '+name
        prior=[(fc,fc.mute) for fc in trackset]
        for fc in trackset:fc.mute=True
        outputs=[]
        try:
            for state,cb in changes:
                cb();bpy.context.view_layer.update()
                rec=render_one(bpy,scene,opts.output/f'iso-{name}-{state}.png')
                rec['effect']=name;rec['setting']=state;outputs.append(rec)
        finally:
            for fc,mute in prior:fc.mute=mute
            scene.frame_set(24);scene.frame_set(25);bpy.context.view_layer.update()
        report['isolation'][name]=outputs
    def set_fluid(active):
        for label,v in zip(('Roil crest','Backwash','Boil pulses'),(wave_values(4) if active else (0,0,0))):
            waves.data.shape_keys.key_blocks[label].value=v
        for name in ('Churned waterline','Breaking turbulent crest'):
            foamline.data.shape_keys.key_blocks[name].value=(.83 if active else 0.0)
        foamline.hide_render=not active
        for ob in bubbles_list:ob.hide_render=not active
    capture_iso('fluid',all_wave_curves+foam_hide_curves+all_bubble_hide,[('off',lambda:set_fluid(False)),('on',lambda:set_fluid(True))])
    capture_iso('steam',all_jet_hide,[('off',lambda:[setattr(o,'hide_render',True) for o in clouds]),
                                        ('on',lambda:[setattr(o,'hide_render',False) for o in clouds])])
    manifest.write_text(json.dumps(report,indent=2)+'\n')
    assert sha(src)==source_hash
    print('SOLAR_V5_GENUINE_CYCLES_COMPLETE',len(report['renders']),len(report['isolation']),flush=True)


def main():
    if '--self-check' in sys.argv:self_check();return
    p=argparse.ArgumentParser()
    p.add_argument('--output',required=True,type=Path)
    p.add_argument('--render',choices=('none','proof'),default='proof')
    p.add_argument('--samples',type=int,default=24)
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else sys.argv[1:])
    if not 4<=a.samples<=40:raise ValueError('Samples limited 4..40')
    build(a)

if __name__=='__main__':main()
