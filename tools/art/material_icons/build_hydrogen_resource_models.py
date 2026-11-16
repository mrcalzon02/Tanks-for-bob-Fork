"""Editable resource props, baked PBR GLBs, and canonical FMPL item profiles."""
import argparse
import os
import hashlib
import json
import math
from pathlib import Path
import random
import sys
import tempfile
import struct

import bpy
import bmesh
from mathutils import Vector

ROOT = Path(os.environ['ICON_PIPELINE_ROOT']).resolve()
TEMP = ROOT / 'build/resource-icon-temp'
TEMP.mkdir(parents=True, exist_ok=True)
tempfile.tempdir = str(TEMP)
sys.path.insert(0, str(ROOT / 'tools/fmpl'))
from blender_camera_guard import install_canonical_camera, assert_clean

OUT = ROOT / 'art/source-to-3d/metallic-hydrogen-chain/resource-icons/v02-modeled'
ASSETS = ['purified-water', 'hydrogen-gas', 'oxygen-gas', 'compressed-hydrogen',
          'liquid-hydrogen', 'liquid-oxygen', 'pellet-fresh', 'pellet-waning',
          'pellet-degraded', 'pellet-critical', 'pellet-inert',
          'empty-pressure-shell', 'charged-fuel-canister']


def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def preserve_glb_images(folder):
    """Materialize exact embedded GLB PNG bytes before packing the reimport."""
    blob=(folder/'model.glb').read_bytes();length=struct.unpack_from('<I',blob,12)[0]
    document=json.loads(blob[20:20+length]);binary=blob[28+length:]
    destination=folder/'runtime-textures';destination.mkdir(exist_ok=True)
    for index,row in enumerate(document['images']):
        view=document['bufferViews'][row['bufferView']];start=view.get('byteOffset',0)
        path=destination/(str(index)+'.png');path.write_bytes(binary[start:start+view['byteLength']])
        image=bpy.data.images.get(row['name'])
        if image is None:raise RuntimeError('Missing imported GLB image '+row['name'])
        image.filepath=str(path);image.reload();image.pack()
        assert image.packed_file and image.size[0]>0


def finish(ob, name, mat, bevel=0):
    ob.name = name
    ob.data.materials.append(mat)
    if bevel:
        mod = ob.modifiers.new('Machined edge highlight', 'BEVEL')
        mod.width = bevel; mod.segments = 3
        bpy.context.view_layer.objects.active = ob
        bpy.ops.object.modifier_apply(modifier=mod.name)
    for face in ob.data.polygons: face.use_smooth = True
    return ob


def cylinder(name, radius, depth, z, mat, xy=(0, 0), vertices=64):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=(*xy, z))
    ob = finish(bpy.context.object, name, mat, min(.022, depth*.14))
    for p in ob.data.polygons:
        if abs(p.normal.z) > .99: p.use_smooth = False
    return ob


def box(name, pos, scale, mat, bevel=.025):
    bpy.ops.mesh.primitive_cube_add(size=1, location=pos)
    ob = bpy.context.object; ob.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return finish(ob, name, mat, bevel)


def sphere(name, pos, scale, mat, subdivisions=3):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=subdivisions, radius=1, location=pos)
    ob = bpy.context.object; ob.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return finish(ob, name, mat)


def ring(name, radius, minor, z, mat, center=(0, 0)):
    bpy.ops.mesh.primitive_torus_add(major_segments=64, minor_segments=12, major_radius=radius,
        minor_radius=minor, location=(*center, z))
    return finish(bpy.context.object, name, mat)


def tube(name, points, radius, mat):
    curve = bpy.data.curves.new(name, 'CURVE'); curve.dimensions='3D'
    curve.bevel_depth=radius; curve.bevel_resolution=3; curve.resolution_u=12
    curve.use_fill_caps=True
    spline=curve.splines.new('POLY'); spline.points.add(len(points)-1)
    for p, co in zip(spline.points, points): p.co=(*co, 1)
    ob=bpy.data.objects.new(name,curve); bpy.context.collection.objects.link(ob)
    bpy.ops.object.select_all(action='DESELECT'); ob.select_set(True); bpy.context.view_layer.objects.active=ob
    bpy.ops.object.convert(target='MESH')
    return finish(bpy.context.object,name,mat)


def material(name, color, metal=.0, rough=.4, emission=0, grit=.1):
    mat=bpy.data.materials.new(name); mat.use_nodes=True
    n=mat.node_tree.nodes; l=mat.node_tree.links; bs=n.get('Principled BSDF')
    bs.inputs['Metallic'].default_value=metal; bs.inputs['Roughness'].default_value=rough
    noise=n.new('ShaderNodeTexNoise'); noise.inputs['Scale'].default_value=32
    noise.inputs['Detail'].default_value=3
    mix=n.new('ShaderNodeMixRGB'); mix.inputs[1].default_value=(*[c*(1-grit) for c in color],1)
    mix.inputs[2].default_value=(*[min(1,c*(1+grit)) for c in color],1)
    l.new(noise.outputs['Fac'],mix.inputs[0])
    if metal > .2:
        geom=n.new('ShaderNodeNewGeometry'); edge=n.new('ShaderNodeValToRGB')
        edge.color_ramp.elements[0].position=.42; edge.color_ramp.elements[0].color=(.24,.24,.24,1)
        edge.color_ramp.elements[1].position=.55; edge.color_ramp.elements[1].color=(1,1,1,1)
        l.new(geom.outputs['Pointiness'],edge.inputs[0])
        highlight=n.new('ShaderNodeMixRGB'); highlight.blend_type='MULTIPLY'; highlight.inputs[0].default_value=.42
        l.new(mix.outputs[0],highlight.inputs[1]); l.new(edge.outputs[0],highlight.inputs[2]); colorout=highlight.outputs[0]
        ao=n.new('ShaderNodeAmbientOcclusion'); ao.inputs['Distance'].default_value=.15
        cavity=n.new('ShaderNodeMixRGB'); cavity.blend_type='MULTIPLY'; cavity.inputs[0].default_value=.65
        l.new(colorout,cavity.inputs[1]); l.new(ao.outputs['Color'],cavity.inputs[2]); colorout=cavity.outputs[0]
    else: colorout=mix.outputs[0]
    l.new(colorout,bs.inputs['Base Color'])
    bump=n.new('ShaderNodeBump'); bump.inputs['Strength'].default_value=.15
    bump.inputs['Distance'].default_value=.003 if metal else .001
    l.new(noise.outputs['Fac'],bump.inputs['Height']); l.new(bump.outputs[0],bs.inputs['Normal'])
    if emission:
        bs.inputs['Emission Color'].default_value=(*color,1); bs.inputs['Emission Strength'].default_value=emission
    bs.inputs['Coat Weight'].default_value=.12 if metal else .3
    return mat


def canister(charged, mats):
    steel,brass,dark,energy=mats['steel'],mats['brass'],mats['dark'],mats['energy']
    barrel=cylinder('Closed pressure vessel barrel',.47,1.2,.81,steel)
    sphere('Domed pressure head',(0,0,1.38),(.47,.47,.2),steel)
    cylinder('Heavy base ring',.51,.16,.2,dark)
    for z in (.31,1.23):
        cylinder('Retaining belt',.505,.115,z,steel)
        ring('Belt edge',.504,.018,z+.058,brass)
        for a in range(0,360,45):
            t=math.radians(a)
            bolt=sphere('Belt mounted fastener',(.51*math.sin(t),.51*math.cos(t),z),(.033,.033,.034),brass,2)
    for x in (-.34,.34):
        for y in (-.29,.29): box('Grounded foot',(x,y,.1),(.2,.18,.2),dark,.02)
    cylinder('Valve neck',.13,.17,1.59,brass)
    cylinder('Valve stem',.055,.18,1.73,steel)
    ring('Handwheel rim',.19,.035,1.83,brass)
    for a in (0,90):
        ob=box('Handwheel spoke',(0,0,1.83),(.35,.035,.035),brass,.01);ob.rotation_euler.z=math.radians(a)
    # A real aperture exposes a recessed fuel chamber instead of a cyan slab.
    cutter=box('Witness aperture cutter',(-.075,-.43,.79),(.27,.42,.77),dark,.065)
    bpy.context.view_layer.objects.active=barrel
    cut=barrel.modifiers.new('Machined fuel inspection opening','BOOLEAN');cut.operation='DIFFERENCE';cut.object=cutter
    bpy.ops.object.modifier_apply(modifier=cut.name);bpy.data.objects.remove(cutter,do_unlink=True)
    box('Recessed fuel chamber back',(-.075,-.262,.79),(.245,.027,.73),dark,.045)
    # Rounded, open perimeter rings leave the fuel visible at physical depth.
    def surround(label,x,y,z,width,height,rad,thickness,mat):
        points=[]
        for cx,cz,start in ((x+width/2-rad,z+height/2-rad,0),
                (x-width/2+rad,z+height/2-rad,90),
                (x-width/2+rad,z-height/2+rad,180),
                (x+width/2-rad,z-height/2+rad,270)):
            for a in range(start,start+91,15):
                angle=math.radians(a);points.append((cx+rad*math.cos(angle),y,cz+rad*math.sin(angle)))
        points.append(points[0]);return tube(label,points,thickness,mat)
    surround('Brass inspection flange',-.075,-.466,.79,.31,.82,.07,.027,brass)
    surround('Black glass pressure gasket',-.075,-.484,.79,.248,.748,.06,.014,dark)
    if charged:
        # Distinct metal fuel capsules and bright cores remain visible through glass.
        for z in (.55,.79,1.03):
            cylinder('Contained metallicized fuel core',.079,.17,z,energy,xy=(-.075,-.365))
            for end in (-.078,.078):cylinder('Fuel core retaining end',.084,.025,z+end,steel,xy=(-.075,-.365))
        tube('Fuel capsule retaining rail',[(-.17,-.305,.43),(-.17,-.305,1.15)],.015,brass)
    else:
        for z in (.55,.79,1.03):
            box('Visible empty cartridge cradle',(-.075,-.303,z),(.15,.024,.025),steel,.006)
    glazing=box('Pressure-rated inspection glass',(-.075,-.479,.79),(.203,.012,.69),mats['window-glazing'],.034)
    for z in (.4,1.18):
        for x in (-.2,.05):sphere('Inspection flange screw',(x,-.477,z),(.023,.018,.023),steel,2)
    # Flush front-face gauge. The pressure takeoff is internal to the vessel.
    # Keep the entire bezel on the straight barrel, above the window flange.
    bore=cylinder('Gauge recessed seat cutter',.079,.15,0,dark)
    bore.rotation_euler.x=math.pi/2;bore.location=(0,-.446,1.32)
    bpy.context.view_layer.objects.active=barrel
    cut=barrel.modifiers.new('Recessed front gauge bore','BOOLEAN');cut.operation='DIFFERENCE';cut.object=bore
    bpy.ops.object.modifier_apply(modifier=cut.name);bpy.data.objects.remove(bore,do_unlink=True)
    gauge=cylinder('Flush front gauge bezel',.09,.022,0,brass)
    gauge.rotation_euler.x=math.pi/2;gauge.location=(0,-.475,1.32)
    face=cylinder('Recessed gauge dial',.073,.008,0,mats['ceramic'])
    face.rotation_euler.x=math.pi/2;face.location=(0,-.483,1.32)
    for angle in (-125,-85,-45,-5,35,75,115):
        t=math.radians(angle)
        tick=box('Dial calibration tick',(.058*math.sin(t),-.489,1.32+.058*math.cos(t)),(.006,.003,.013),dark,.001)
        tick.rotation_euler.y=t
    needle=box('Gauge pressure needle',(0,-.492,1.334),(.006,.004,.062),dark,.001)
    needle.rotation_euler.y=math.radians(48 if charged else -110)
    hub=sphere('Gauge needle spindle',(0,-.494,1.32),(.011,.006,.011),brass,2)
    # Flush instrument panel follows barrel tangent; each lamp has a dark bezel.
    box('Charge instrument housing',(.267,-.392,.79),(.19,.07,.52),steel,.035)
    box('Recessed instrument face',(.267,-.432,.79),(.145,.018,.46),dark,.025)
    for z in (.63,.79,.95):
        box('Recessed charge lamp bezel',(.267,-.448,z),(.115,.018,.081),brass,.014)
        box('Charge status lens',(.267,-.46,z),(.077,.012,.042),energy if charged else mats['glass'],.012)
    if charged:
        ring('Locked cap seal',.15,.025,1.6,mats['red'])


def pellet(stage, mats):
    body=mats['steel'] if stage < 2 else mats['decayed']
    # Shape the actual end and circumference: decay changes geometry, not just hue.
    n=96; rows=32; vertices=[]; faces=[];grooves=[]
    for j in range(rows+1):
        z=.13+j/rows*1.24
        for i in range(n):
            a=2*math.pi*i/n
            chip=0
            if stage==1:
                chip=.023*max(0,math.sin(a*5+j*.35))**10
                if j>26:chip+=.025*max(0,math.sin(a*3+.3))
            if stage>=2:
                chip=(.03+.025*stage)*max(0,math.sin(a*5+j*.35))**10
                if j>24: chip+=.035*stage*max(0,math.sin(a*3+.3))
            groove=0
            if j>4:
                for crack in range(3+stage):
                    center=2*math.pi*crack/(3+stage)+.2+math.sin(j*.33+crack)*.09
                    delta=abs((a-center+math.pi)%(2*math.pi)-math.pi)
                    depth=(.012,.026,.049,.056,.063)[stage]
                    groove=max(groove,depth*max(0,1-delta/.12))
            r=max(.085,.31-chip-groove)
            if stage==4:
                r*=1-.42*(j/rows)**4
                worn_z=z-.23*(j/rows)**2+.045*(j/rows)**5*math.sin(a*5)
            else:worn_z=z
            vertices.append((r*math.cos(a),r*math.sin(a),worn_z))
            grooves.append(groove)
    for j in range(rows):
        for i in range(n):
            k=j*n+i;q=j*n+(i+1)%n
            faces.append((k,q,q+n,k+n))
    faces += [tuple(reversed(range(n))),tuple(range(rows*n,(rows+1)*n))]
    mesh=bpy.data.meshes.new('Pellet machined/chipped topology');mesh.from_pydata(vertices,[],faces);mesh.update()
    ob=bpy.data.objects.new('Metallicized pellet body',mesh);bpy.context.collection.objects.link(ob)
    ob.data.materials.append(body)
    ob.data.materials.append(mats['dark'])
    if stage<4:ob.data.materials.append(mats['residual-energy'] if stage==3 else mats['energy'])
    # Grooves are part of a single closed radial surface; there are no added crack objects.
    # Physical recesses receive the dark exposed interior material.
    for face in ob.data.polygons:
        if any(grooves[v]>(.004,.009,.025,.025,.025)[stage] for v in face.vertices):
            face.material_index=1
            center=sum((mesh.vertices[v].co for v in face.vertices),Vector())/len(face.vertices)
            if stage==3 and center.x>.14 and .55<center.z<1.13:
                face.material_index=2
            elif stage<3 and center.x>(-.1,.02,-.18)[stage] and (.25,.35,.26)[stage]<center.z<(1.28,1.22,1.30)[stage]:
                face.material_index=2
    # Energy belongs to recessed fracture faces, never raised tubes or rings.
    for face in ob.data.polygons:face.use_smooth=True
    cylinder('Machined end cap',.292,.03,.145,body)
    # Author geometry attitude; the FMPL camera remains at zero azimuth.
    for ob in list(bpy.context.scene.objects):
        if ob.type=='MESH':
            for v in ob.data.vertices: v.co=ob.matrix_world @ v.co
            ob.matrix_world.identity()
            ob.rotation_euler=(math.radians(28),math.radians(-42),math.radians(-20))
    bpy.context.view_layer.update()


def droplet(name, mat, mats):
    profile=[(0,.12),(.24,.15),(.43,.3),(.49,.52),(.46,.73),(.37,.94),(.27,1.12),(.16,1.35),(.07,1.58),(0,1.82)]
    verts=[];faces=[];n=64
    for r,z in profile:
        r=max(r,.001)
        for i in range(n):
            a=2*math.pi*i/n;verts.append((r*math.cos(a),r*math.sin(a),z))
    for j in range(len(profile)-1):
        for i in range(n):
            a=j*n+i;b=j*n+(i+1)%n;faces.append((a,b,b+n,a+n))
    faces += [tuple(reversed(range(n))),tuple(range((len(profile)-1)*n,len(profile)*n))]
    mesh=bpy.data.meshes.new('Lathed droplet');mesh.from_pydata(verts,[],faces);mesh.update()
    ob=bpy.data.objects.new('Liquid meniscus',mesh);bpy.context.collection.objects.link(ob);finish(ob,ob.name,mat)
    bpy.context.view_layer.objects.active=ob
    mod=ob.modifiers.new('Continuous liquid surface','SUBSURF');mod.levels=2
    bpy.ops.object.modifier_apply(modifier=mod.name)
    # Raised caustic streaks and surface microbubbles survive the small icon.
    tube('Curved reflected streak',[(-.24,-.29,.4),(-.28,-.31,.64),(-.23,-.29,.86),(-.14,-.23,1.08)],.018,mats['glint'])
    if name.startswith('liquid-'):
        for i in range(6):
            a=i*2*math.pi/6
            sphere('Cryogenic frost inclusion',(.38*math.cos(a),.38*math.sin(a),.29),(.09,.06,.07),mats['frost'],1)
    else:
        for x,z,r in ((.19,.58,.035),(.1,.83,.025),(.29,.43,.02)):
            sphere('Water surface bubble',(x,-.38,z),(r,r,r),mats['glint'],2)


def gas(name, mat, mats):
    oxygen=name=='oxygen-gas'
    centers=[(-.31,0,.56),(.27,.05,.62),(0,-.17,.83),(-.2,.1,1.08),(.2,0,1.18)]
    if oxygen: centers += [(-.21,.03,1.48),(.27,.04,1.66)]
    else: centers += [(-.45,0,.86),(.4,.01,.93)]
    lobes=[]
    for i,p in enumerate(centers):lobes.append(sphere('Vapor lobe',p,(.34,.29,.3),mat,3))
    bpy.ops.object.select_all(action='DESELECT')
    for ob in lobes: ob.select_set(True)
    bpy.context.view_layer.objects.active=lobes[0];bpy.ops.object.join();ob=bpy.context.object
    # Actual union/remesh, rather than overlapping unjoined organic surfaces.
    remesh=ob.modifiers.new('Connected vapor envelope','REMESH');remesh.mode='VOXEL';remesh.voxel_size=.025
    bpy.ops.object.modifier_apply(modifier=remesh.name)
    smooth=ob.modifiers.new('Soft gas transitions','SMOOTH');smooth.factor=1.4;smooth.iterations=4
    bpy.ops.object.modifier_apply(modifier=smooth.name)
    for f in ob.data.polygons:f.use_smooth=True
    ob.name='Connected oxygen plume' if oxygen else 'Connected hydrogen vapor'
    tube('Raised curling vapor highlight',[(-.39,-.23,.65),(-.2,-.35,.72),(.03,-.41,.86),(.15,-.29,1.02)],.027,mats['glint'])


def compressed(mats):
    sphere('Dense compressed hydrogen',(0,0,.9),(.56,.56,.56),mats['fluid'])
    for rot in (0,math.pi/2):
        ob=ring('Pressure cage meridian',.58,.048,0,mats['steel']);ob.rotation_euler=(math.pi/2,rot,0);ob.location.z=.9
    ring('Pressure cage equator',.58,.048,.9,mats['steel'])
    for x,y in ((0,-.59),(0,.59),(-.59,0),(.59,0)):
        box('Cage bolted junction',(x,y,.9),(.15,.15,.15),mats['brass'],.025)
    cylinder('Top pressure boss',.14,.14,1.51,mats['brass'])


def unwrap_and_bake(folder, preserve_uv=False, bake_resolution=None):
    meshes=[ob for ob in bpy.context.scene.objects if ob.type=='MESH']
    bpy.ops.object.select_all(action='DESELECT')
    for ob in meshes:ob.select_set(True)
    bpy.context.view_layer.objects.active=meshes[0];bpy.ops.object.join();ob=bpy.context.object
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    if not preserve_uv:
        bm=bmesh.new();bm.from_mesh(ob.data)
        bmesh.ops.triangulate(bm,faces=list(bm.faces))
        bmesh.ops.dissolve_degenerate(bm,dist=1e-6,edges=list(bm.edges))
        invalid=[face for face in bm.faces if face.calc_area()<1e-12]
        if invalid:bmesh.ops.delete(bm,geom=invalid,context='FACES')
        bm.to_mesh(ob.data);bm.free();ob.data.update()
    native_uv=None
    if preserve_uv:
        native_uv=ob.data.uv_layers.active.name
        def bind_native_uv(tree):
            for node in list(tree.nodes):
                if node.type=='TEX_IMAGE' and not node.inputs['Vector'].is_linked:
                    uv=tree.nodes.new('ShaderNodeUVMap');uv.uv_map=native_uv
                    tree.links.new(uv.outputs['UV'],node.inputs['Vector'])
                if node.type=='NORMAL_MAP':node.uv_map=native_uv
                if node.type=='GROUP' and node.node_tree:bind_native_uv(node.node_tree)
        for mat in ob.data.materials:bind_native_uv(mat.node_tree)
        atlas=ob.data.uv_layers.new(name='ProductionAtlas')
        ob.data.uv_layers.active=atlas;atlas.active_render=True
    if not preserve_uv:
        bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.uv.smart_project(angle_limit=math.radians(65),island_margin=.02,area_weight=1)
        bpy.ops.object.mode_set(mode='OBJECT')
    scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=8
    scene.render.bake.margin=4;scene.render.bake.use_clear=True
    originals=list(ob.data.materials);images={}
    # Imported meshes use split corner vertices. Repacking each disconnected
    # triangle destroys texel density; keep their proven native layout instead.
    bake_size=256
    if preserve_uv:
        source_sizes=[max(n.image.size) for mat in originals for n in mat.node_tree.nodes if n.type=='TEX_IMAGE' and n.image]
        bake_size=min(2048,max([1024,*source_sizes]))
    if bake_resolution is not None:
        if not isinstance(bake_resolution,int) or bake_resolution<256:raise ValueError('Invalid bake resolution')
        bake_size=bake_resolution
    glazing_faces=[face.index for face in ob.data.polygons if 'window glazing' in originals[face.material_index].name]
    glazing_material=next((mat for mat in originals if 'window glazing' in mat.name),None)
    for channel,socket in [('base-color','Base Color'),('roughness','Roughness'),('metallic','Metallic'),('emission','Emission Color'),('normal',None)]:
        image=bpy.data.images.new(folder.name+' '+channel,bake_size,bake_size,alpha=False)
        if channel not in ('base-color','emission'):image.colorspace_settings.name='Non-Color'
        saved=[]
        for mat in originals:
            nodes=mat.node_tree.nodes;links=mat.node_tree.links
            tex=nodes.new('ShaderNodeTexImage');tex.image=image;nodes.active=tex
            output=nodes.get('Material Output');old=output.inputs['Surface'].links[0].from_socket
            saved.append((mat,old,tex))
            if channel!='normal':
                bs=nodes.get('Principled BSDF');inp=bs.inputs[socket]
                emit=nodes.new('ShaderNodeEmission');emit.name='BAKE_TEMP'
                if inp.is_linked:links.new(inp.links[0].from_socket,emit.inputs['Color'])
                else:
                    value=inp.default_value
                    emit.inputs['Color'].default_value=(*([value]*3 if isinstance(value,float) else list(value)[:3]),1)
                if channel=='emission':emit.inputs['Strength'].default_value=bs.inputs['Emission Strength'].default_value
                links.new(emit.outputs[0],output.inputs['Surface'])
        bpy.ops.object.bake(type='NORMAL' if channel=='normal' else 'EMIT',uv_layer='ProductionAtlas' if preserve_uv else '')
        image.filepath_raw=str(folder/(channel+'.png'));image.file_format='PNG';image.save();image.pack();images[channel]=image
        for mat,old,tex in saved:
            nodes=mat.node_tree.nodes;links=mat.node_tree.links
            links.new(old,nodes.get('Material Output').inputs['Surface']);nodes.remove(tex)
            temp=nodes.get('BAKE_TEMP')
            if temp:nodes.remove(temp)
    # Preserve editable region materials in authoring source, use baked maps in runtime derivative.
    bpy.ops.wm.save_as_mainfile(filepath=str(folder/'authored.blend'))
    baked=bpy.data.materials.new(folder.name+' baked model-specific PBR');baked.use_nodes=True
    n=baked.node_tree.nodes;l=baked.node_tree.links;bs=n.get('Principled BSDF')
    uv=None
    if preserve_uv:
        uv=n.new('ShaderNodeUVMap');uv.uv_map='ProductionAtlas'
    for channel,socket in [('base-color','Base Color'),('roughness','Roughness'),('metallic','Metallic'),('emission','Emission Color')]:
        tex=n.new('ShaderNodeTexImage');tex.image=images[channel];l.new(tex.outputs['Color'],bs.inputs[socket])
        if uv:l.new(uv.outputs['UV'],tex.inputs['Vector'])
    normal=n.new('ShaderNodeNormalMap');tex=n.new('ShaderNodeTexImage');tex.image=images['normal']
    l.new(tex.outputs['Color'],normal.inputs['Color']);l.new(normal.outputs[0],bs.inputs['Normal'])
    if uv:
        l.new(uv.outputs['UV'],tex.inputs['Vector']);normal.uv_map='ProductionAtlas'
    bs.inputs['Emission Strength'].default_value=1
    ob.data.materials.clear();ob.data.materials.append(baked)
    for p in ob.data.polygons:p.material_index=0
    if glazing_material:
        ob.data.materials.append(glazing_material)
        for index in glazing_faces:ob.data.polygons[index].material_index=1
    return ob


def measure(objects):
    points=[ob.matrix_world@v.co for ob in objects for v in ob.data.vertices]
    return [[min(p[i] for p in points) for i in range(3)],[max(p[i] for p in points) for i in range(3)]]


def lighting(scene):
    scene.world=bpy.data.worlds.new('Nauvis-like muted daylight');scene.world.use_nodes=True
    n=scene.world.node_tree.nodes;l=scene.world.node_tree.links;bg=n.get('Background')
    sky=n.new('ShaderNodeTexSky');sky.sky_type='MULTIPLE_SCATTERING';sky.sun_disc=False
    sky.sun_elevation=math.radians(35);sky.sun_rotation=math.radians(130)
    bg.inputs['Strength'].default_value=.18;l.new(sky.outputs[0],bg.inputs['Color'])
    for name,pos,power,size,color in [('Warm upper-left key',(-3,-4,6),450,4,(1,.86,.7)),
            ('Cool environment fill',(4,-1,3),160,4,(.64,.79,1)),('Back edge separation',(-1,3,4),230,3,(1,.93,.78))]:
        data=bpy.data.lights.new(name,'AREA');data.energy=power;data.shape='DISK';data.size=size;data.color=color
        ob=bpy.data.objects.new(name,data);scene.collection.objects.link(ob);ob.location=pos
        ob.rotation_euler=(Vector((0,0,.8))-ob.location).to_track_quat('-Z','Y').to_euler()
    scene.render.engine='CYCLES';scene.cycles.samples=32;scene.cycles.use_denoising=True
    scene.view_settings.view_transform='AgX'


def build(name):
    folder=OUT/name
    if folder.exists():raise FileExistsError('Preserve modeled revisions: '+str(folder))
    folder.mkdir(parents=True)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    palette={'purified-water':(.015,.26,.43),'liquid-hydrogen':(.16,.55,.66),
             'liquid-oxygen':(.055,.09,.5),'hydrogen-gas':(.24,.49,.54),
             'oxygen-gas':(.35,.29,.52),'compressed-hydrogen':(.015,.42,.52)}
    stage=ASSETS.index(name)-6 if name.startswith('pellet-') else 0
    m={
        'steel':material(name+' machined steel',(.23,.25,.26),.82,.32,grit=.24),
        'brass':material(name+' tarnished valve brass',(.4,.25,.075),.78,.32,grit=.27),
        'dark':material(name+' recess and gasket',(.017,.023,.027),.15,.75),
        'energy':material(name+' contained fuel',((.005,.5,.66),(.025,.41,.4),(.9,.42,.045),(.005,.5,.66),(.005,.5,.66))[stage],.2,.22,emission=(2.4,1.9,1.8,.36,.2)[stage]),
        'decayed':material(name+' fractured oxidation',(.095,.09,.083) if stage<4 else (.029,.031,.028),.38 if stage<4 else .08,.7 if stage<4 else .91,grit=.5),
        'residual-energy':material(name+' residual fracture energy',(.9,.19,.018),.05,.45,emission=2.4,grit=.06),
        'glass':material(name+' empty smoked window',(.025,.055,.06),.35,.2),
        'ceramic':material(name+' gauge ceramic',(.65,.62,.49),.0,.65),
        'red':material(name+' pressure seal',(.25,.035,.018),.05,.6),
        'glint':material(name+' reflected caustic',(.5,.8,.86),.15,.15),
        'frost':material(name+' frost',(.52,.69,.72),.05,.55),
        'fluid':material(name+' fluid',palette.get(name,(.015,.42,.52)),.0 if name.endswith('gas') else .22,.7 if name.endswith('gas') else .18,grit=.06),
        'window-glazing':material(name+' window glazing',(.8,.94,1),.0,.08,grit=0),
    }
    glass_bs=m['window-glazing'].node_tree.nodes.get('Principled BSDF')
    glass_bs.inputs['Transmission Weight'].default_value=.98;glass_bs.inputs['IOR'].default_value=1.45
    if name.endswith('canister') or name=='empty-pressure-shell':canister(name=='charged-fuel-canister',m)
    elif name.startswith('pellet-'):pellet(stage,m)
    elif name.endswith('gas'):gas(name,m['fluid'],m)
    elif name=='compressed-hydrogen':compressed(m)
    else:droplet(name,m['fluid'],m)
    # Ground each physical prop without changing its authored attitude.
    bpy.context.view_layer.update()
    meshes=[ob for ob in bpy.context.scene.objects if ob.type=='MESH'];bounds=measure(meshes)
    for ob in meshes:ob.location.z-=bounds[0][2]
    bpy.context.view_layer.update()
    lighting(bpy.context.scene)
    ob=unwrap_and_bake(folder)
    region_names=[mat.name for mat in m.values()]
    before=measure([ob])
    bpy.ops.export_scene.gltf(filepath=str(folder/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_animations=False)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=str(folder/'model.glb'))
    preserve_glb_images(folder)
    objects=[o for o in bpy.context.scene.objects if o.type=='MESH'];bpy.context.view_layer.update();after=measure(objects)
    triangles=0;degenerate=0;uv_missing=[]
    for ob in objects:
        ob.data.calc_loop_triangles();triangles+=len(ob.data.loop_triangles)
        degenerate+=sum(t.area<1e-12 for t in ob.data.loop_triangles)
        if not ob.data.uv_layers:uv_missing.append(ob.name)
        assert all(math.isfinite(v) for p in ob.data.vertices for v in p.co)
    error=max(abs(before[j][i]-after[j][i]) for j in range(2) for i in range(3))
    image_count=sum(image.source=='FILE' and image.size[0]>0 for image in bpy.data.images)
    inspection=dict(asset=name,passed=error<1e-5 and not degenerate and not uv_missing and image_count>=4,
        bounds_before=before,bounds_after=after,bounds_max_error=error,triangles=triangles,
        degenerate_triangles=degenerate,missing_uv=uv_missing,reimported_images=image_count,glb_sha256=sha(folder/'model.glb'))
    (folder/'runtime-inspection.json').write_text(json.dumps(inspection,indent=2)+'\n')
    if not inspection['passed']:raise RuntimeError(inspection)
    bpy.data.orphans_purge(do_recursive=True)
    for image in bpy.data.images:
        if image.source in ('FILE','GENERATED'):image.pack()
    scene=bpy.context.scene;lighting(scene)
    center=[(after[0][i]+after[1][i])/2 for i in range(3)]
    # Account for world X span and 45-degree projection of Y/Z; never rotate camera.
    extent=max(after[1][0]-after[0][0],((after[1][1]-after[0][1])+(after[1][2]-after[0][2]))/math.sqrt(2))
    cfg=json.loads((ROOT/'tools/fmpl/profiles/item-icon.example.json').read_text())
    cfg.update(asset=name,source='runtime-reimport.blend',source_size=256,sizes=[64,128,256],samples=32,threads=4)
    cfg['camera_override']['target']=center;cfg['camera_override']['ortho_scale']=extent*1.22
    install_canonical_camera(scene,cfg,bpy);assert_clean(scene,cfg,bpy)
    bpy.ops.wm.save_as_mainfile(filepath=str(folder/'runtime-reimport.blend'))
    (folder/'capture-profile.json').write_text(json.dumps(cfg,indent=2)+'\n')
    (folder/'surface-plan.json').write_text(json.dumps(dict(asset=name,
        construction='Authored geometry; baked model-specific UV atlas; actual GLB reimport before FMPL capture',
        regions=region_names,maps=['base-color','roughness','metallic','normal','emission'],
        reference='https://github.com/malcolmriley/unused-renders/wiki',
        lessons=['Nauvis-like environmental light','geometry bevel highlights','baked cavity AO and edge wear',
            'local roughness and oxidation','128/64 px readability','single persistent FMPL 45 degree camera']),indent=2)+'\n')
    print('RESOURCE_MODEL_BUILT '+name,flush=True)


def main():
    global OUT
    parser=argparse.ArgumentParser();parser.add_argument('--assets',nargs='+',default=ASSETS)
    parser.add_argument('--out',type=Path)
    args=parser.parse_args(sys.argv[sys.argv.index('--')+1:])
    if args.out:OUT=args.out.resolve()
    for name in args.assets:
        if name not in ASSETS:raise ValueError(name)
        build(name)


if __name__=='__main__':main()
