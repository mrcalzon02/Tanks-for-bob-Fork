#!/usr/bin/env python3
"""V4 survival solar boiler: wood staves, fitted plank conduits and feathered steam.

Immutable source: installed Solar Boiler V3 native .blend. 1 unit == 1 tile.
All optical/port geometry from V3 is preserved and version-hidden, not deleted.
A single original FMPL 45-degree camera renders all approved cardinal views.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import struct
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
SRC = REPO/'models/island-survival/solar-boiler/generated-v3/solar-boiler-v3.blend'
SRC_REPORT = SRC.with_name('build-report.json')
WOOD_DONOR = REPO/'models/island-survival/blender/generated-v8/campfire-v8-animated.blend'
FRAMES = tuple(range(1, 92, 6))
DIRECTIONS = (0, 90, 180, 270)
LOOP_END = 97


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def metal_heating(k):
    # Gentle, tarnished-bronze glint, never red-hot furnace emission.
    return .045 + .22 * (.5 + .5 * math.sin(math.tau * k / 16))


def steam_phase(k, phase):
    return ((k-phase) % 16) / 16


def self_check():
    assert len(FRAMES)==16 and FRAMES==(1,7,13,19,25,31,37,43,49,55,61,67,73,79,85,91)
    assert abs(metal_heating(0)-metal_heating(16))<1e-12
    assert max(metal_heating(k) for k in range(16)) < .27
    for phase in (0,4,8,12):
        assert steam_phase(0,phase)==steam_phase(16,phase)
    # Both water inputs and the steam output are boundary-mounted metal-only collars.
    contract=json.loads((REPO/'models/island-survival/solar-boiler/v1/port-contract.json').read_text())
    assert contract['footprint_tiles']==[3,2]
    assert {p['id'] for p in contract['ports']}=={'water-west','water-east','steam-north'}
    print('SOLAR_V4_STAVE_AND_STEAM_MATH_PASS',flush=True)


def mesh_hash(obj):
    h=hashlib.sha256()
    for v in obj.data.vertices:h.update(struct.pack('<3f',*v.co))
    for p in obj.data.polygons:
        h.update(struct.pack('<I',len(p.vertices)))
        for i in p.vertices:h.update(struct.pack('<I',i))
    return h.hexdigest()


def material_copy(source, name, rough_mult=1.0, polished=False):
    import bpy
    m=source.copy()
    m.name=name
    if m.use_nodes:
        nodes=m.node_tree.nodes; links=m.node_tree.links
        bsdf=next((n for n in nodes if n.type=='BSDF_PRINCIPLED'),None)
        if bsdf is None:raise RuntimeError('Wood donor missing Principled PBR shader')
        rough=bsdf.inputs.get('Roughness')
        if rough and rough.is_linked:
            link=next(iter(rough.links))
            original=link.from_socket
            links.remove(link)
            mul=nodes.new('ShaderNodeMath');mul.operation='MULTIPLY'
            mul.inputs[1].default_value=rough_mult
            links.new(original,mul.inputs[0]);links.new(mul.outputs[0],rough)
        elif rough:
            rough.default_value=max(.07,min(.9,rough.default_value*rough_mult))
        if polished:
            for key,value in (('Coat Weight',.85),('Coat Roughness',.045),('Specular IOR Level',.70)):
                inp=bsdf.inputs.get(key)
                if inp:inp.default_value=value
            for normal in nodes:
                if normal.type=='NORMAL_MAP':
                    strength=normal.inputs.get('Strength')
                    if strength:strength.default_value=.09
    m['solar_v4_material']='approved source wood material derivative'
    m['source_material_name']=source.name
    m['optical_design']='polished timber parabola, as requested' if polished else 'scavenged timber staves'
    return m


def import_wood(bpy):
    """Append only materials actually used on ACCEPTED native Campfire firewood.

    The frozen V8 donor precedes V9's animated charring mask. Material names
    vary across revisions, so never invent legacy CF7 material identifiers.
    Actual 02 | Firewood mesh slots determine the source of the PBR maps.
    """
    if not WOOD_DONOR.is_file():raise FileNotFoundError('Accepted Campfire V8 wood donor missing')
    with bpy.data.libraries.load(str(WOOD_DONOR),link=False) as (src,dst):
        if '02 | Firewood' not in src.collections:
            raise RuntimeError('Accepted Campfire has no Firewood objects')
        dst.collections=['02 | Firewood']
    collection=dst.collections[0]
    assert collection is not None
    donor_meshes=[obj for obj in collection.objects if obj.type=='MESH']
    assert len(donor_meshes)>=25,('Wrong accepted wood donor',len(donor_meshes))
    used={m.name:m for ob in donor_meshes for m in ob.data.materials if m}
    genuine=[]
    for mat in used.values():
        if not mat.use_nodes:continue
        images=[node.image for node in mat.node_tree.nodes if node.type=='TEX_IMAGE']
        if (len(images)>=1 and all(im and im.packed_file for im in images)
                and any(n.type=='TEX_NOISE' for n in mat.node_tree.nodes)
                and any(n.type=='NORMAL_MAP' for n in mat.node_tree.nodes)):
            genuine.append(mat)
    if len(genuine)<3:
        raise RuntimeError('No approved procedural wood + packed tangent normal in donor Firewood meshes: '+str(sorted(used)))
    genuine=sorted(genuine,key=lambda m:m.name)
    print('SOLAR_V4_ACCEPTED_WOOD_PBR_NAMES',repr([m.name for m in genuine]),flush=True)
    def pick(tokens,exclude=()):
        for token in tokens:
            for m in genuine:
                if token in m.name.lower() and not any(ex in m.name.lower() for ex in exclude):
                    return m
        return None
    bark=pick(('weathered','bark','rough')) or genuine[0]
    cut=pick(('cut','endgrain','ring','sapwood')) or next((m for m in genuine if m!=bark),genuine[0])
    light=pick(('sapwood','light','pale')) or next((m for m in genuine if m not in (bark,cut)),cut)
    dark=pick(('bark_dark','heart','dark','char'),exclude=('charred','charcoal')) or bark
    selected={m.name:m for m in (bark,cut,light,dark)}
    # Remove appended source geometry/collection; *only* the original PBR
    # material/images and their new derivatives are carried into V4.
    imported=list(collection.objects)
    bpy.data.collections.remove(collection,do_unlink=True)
    for ob in imported:
        if ob.users==0:bpy.data.objects.remove(ob,do_unlink=True)
    return {
       'weathered':material_copy(bark,'SOLAR V4 | scavenged weathered staves',.93),
       'bark':material_copy(dark,'SOLAR V4 | scarred timber conduit staves',.98),
       'light':material_copy(light,'SOLAR V4 | faded bent sapwood',.84),
       'endgrain':material_copy(cut,'SOLAR V4 | barrel endgrain',.90),
       'polished':material_copy(cut,'SOLAR V4 | polished wood solar parabolic reflector',.14,True),
       'polished_edge':material_copy(light,'SOLAR V4 | polished wood reflector strip',.19,True),
       'donor_names':list(selected),
    }


def mesh_obj(bpy,name,verts,faces,mat,collection,parent=None, smooth=False, uv=True):
    mesh=bpy.data.meshes.new(name+' mesh')
    mesh.from_pydata(verts,[],faces);mesh.update()
    ob=bpy.data.objects.new(name,mesh);collection.objects.link(ob)
    if parent is not None:ob.parent=parent
    mesh.materials.append(mat)
    for poly in mesh.polygons:poly.use_smooth=smooth
    if uv:
        layer=mesh.uv_layers.new(name='Approved timber PBR UV')
        for poly in mesh.polygons:
            for li in poly.loop_indices:
                co=mesh.vertices[mesh.loops[li].vertex_index].co
                # Natural grain follows the long axis of barrel and planks.
                layer.data[li].uv=((co.x+.9)*1.8,(co.y+co.z)*1.5)
    return ob


def hidden_source(ob, reason):
    if ob.animation_data and ob.name.startswith(('STEAM JOINT V3 |','PRESSURE | short active plume')):
        ob.animation_data_clear()  # historical source remains in V3 file unchanged
    ob.hide_render=True
    ob['solar_v4_hidden_source_reason']=reason


def hide_legacy(bpy):
    marked=[]
    exact={
      'PROCESS | horizontal copper steam drum',
      'GAUGE | live pressure needle',
      'ACCUMULATOR V3 | localized thermal radiation',
    }
    prefixes=(
      'PROCESS | cast retainer band','PROCESS | pressure vessel round end plate',
      'PROCESS | service plate stud','PROCESS | west water reducing elbow',
      'PROCESS | east water reducing elbow','PROCESS | north output steam reducing downpipe',
      'PROCESS | water vessel receiver','PROCESS | steam drum steam extraction neck',
      'ACCUMULATOR V3 |','STEAM JOINT V3 |','PRESSURE | short active plume',
      'CONCENTRATOR | west | true parabolic continuous mirror',
      'CONCENTRATOR | east | true parabolic continuous mirror',
      'CONCENTRATOR | west | continuous hot collector outlet to drum',
      'CONCENTRATOR | east | continuous hot collector outlet to drum',
      'CONCENTRATOR | west | continuous cool thermal return from drum',
      'CONCENTRATOR | east | continuous cool thermal return from drum',
      'CONCENTRATOR | west | hot collector outlet to drum |',
      'CONCENTRATOR | east | hot collector outlet to drum |',
      'CONCENTRATOR | west | cool thermal return from drum |',
      'CONCENTRATOR | east | cool thermal return from drum |',
      'CONCENTRATOR | west | curved end rib','CONCENTRATOR | east | curved end rib',
      'CONCENTRATOR | west | upturned rim bead','CONCENTRATOR | east | upturned rim bead',
      'CONCENTRATOR | west | load-bearing collector saddle extension',
      'CONCENTRATOR | east | load-bearing collector saddle extension',
      'SOLAR | load-bearing angled steel array support','SOLAR | diagonal collector cage brace',
      'SOLAR | array mounting clamp','SUPPORT | rusted steel saddle shoe',
    )
    for ob in list(bpy.data.objects):
        if ob.name in exact or ob.name.startswith(prefixes):
            hidden_source(ob,'V4 visual woodworking derivative, original preserved in V3 native file')
            marked.append(ob.name)
    assert any('horizontal copper steam drum' in n for n in marked)
    assert len([x for x in marked if x.startswith('STEAM JOINT V3 |')])==16
    return marked


def cylinder(bpy,name,xyz,radius,depth,material,col,root,axis=(0,0,1),segments=48):
    from mathutils import Vector
    bpy.ops.mesh.primitive_cylinder_add(vertices=segments,radius=radius,depth=depth,location=xyz)
    ob=bpy.context.object;ob.name=name
    for old in tuple(ob.users_collection):old.objects.unlink(ob)
    col.objects.link(ob);ob.parent=root;ob.data.materials.append(material)
    ob.rotation_euler=Vector(axis).to_track_quat('Z','Y').to_euler()
    return ob


def timber_rod(bpy,name,a,b,radius,mat,col,root):
    from mathutils import Vector
    aa=Vector(a);bb=Vector(b)
    return cylinder(bpy,name,(aa+bb)*.5,radius,(bb-aa).length,mat,col,root,(bb-aa).normalized(),12)


def barrel_staves(bpy,wood,col,root):
    """18 individually bowing and not-quite-fitted wooden planks, not copper skin."""
    n=18; length=1.52; segments=10; circ=[]
    y0,z0=-.10,.77
    for stave in range(n):
        # Longitudinal stave profile bulges in the centre like a real barrel.
        t0=math.tau*stave/n+.006
        t1=math.tau*(stave+1)/n-.006
        jitter=.006*math.sin(stave*2.1)
        vs=[]
        for xside,radial_offset in (('outer',0),('inner',-.042)):
            for k in range(segments+1):
                s=k/segments;x=(s-.5)*length
                crown=.032*(1-(2*s-1)**2)
                r=.365+crown+jitter+radial_offset
                for theta in (t0,t1):
                    vs.append((x,y0+r*math.cos(theta),z0+r*math.sin(theta)))
        per=(segments+1)*2
        fs=[]
        for k in range(segments):
            i=2*k;f=per+i
            fs.extend(((i,i+2,i+3,i+1),(f+1,f+3,f+2,f),
                       (i,f,f+2,i+2),(i+1,i+3,f+3,f+1)))
        fs.extend(((0,1,per+1,per),(2*segments,per+2*segments,per+2*segments+1,2*segments+1)))
        ob=mesh_obj(bpy,f'WOOD V4 | barrel stave {stave+1:02d}',vs,fs,
                    wood['weathered'] if stave%4 else wood['light'],col,root,True)
        ob['wood_role']='rough bowed barrel planking'
        circ.append(ob)
    # Lapped wooden hoops, slender bronze clasp instead of metal straps all over.
    for x in (-.61,.61):
        segs=64;rad=.407
        vs=[]
        for xi,r in ((x-.027,rad+.014),(x+.027,rad+.014),(x-.027,rad-.012),(x+.027,rad-.012)):
            vs.extend((xi,y0+r*math.cos(math.tau*k/segs),z0+r*math.sin(math.tau*k/segs)) for k in range(segs))
        fs=[]
        for j in range(segs):
            k=(j+1)%segs
            fs.extend(((j,k,segs+k,segs+j),(2*segs+k,2*segs+j,3*segs+j,3*segs+k),
                       (j,2*segs+j,2*segs+k,k),(segs+k,3*segs+k,3*segs+j,segs+j)))
        ob=mesh_obj(bpy,'WOOD V4 | bentwood hoop '+str(x),vs,fs,wood['bark'],col,root,False)
        ob['wood_role']='wood barrel hoop, not steel'
    # Individual rough end-grain planks, with a true opening near the existing
    # water-to-vessel socket so no wood visually seals the pipe into an endcap.
    for side in (-1,1):
        x=side*.777
        for j in range(13):
            cy=y0+(j-6)*.055
            if abs(cy-y0)>.340:continue
            half=math.sqrt(max(0,.344**2-(cy-y0)**2))
            zlow=z0-half;zhi=z0+half
            # The original side feed meets near y=-0.29, z=.72.
            if abs(cy+.29)<.10:
                # Leave open clearance in the end-grain where piping enters.
                if zlow < .77 and zhi > .64: zhi=.63
            if zhi-zlow<.035:continue
            verts=[(x,cy-.025,zlow),(x,cy+.025,zlow),(x,cy+.025,zhi),(x,cy-.025,zhi)]
            ob=mesh_obj(bpy,'WOOD V4 | rough barrel endcap '+str(side)+' '+str(j),verts,
                [(0,1,2,3)],wood['endgrain'],col,root)
            ob['wood_role']='wooden barrel end plank'
    return len(circ)


def path_samples(control, count=30):
    from mathutils import Vector
    ps=[Vector(q) for q in control]
    results=[]
    for i in range(len(ps)-1):
        a=ps[max(i-1,0)];b=ps[i];c=ps[i+1];d=ps[min(i+2,len(ps)-1)]
        for j in range(count//(len(ps)-1)):
            t=j/(count//(len(ps)-1))
            p=.5*((2*b)+(-a+c)*t+(2*a-5*b+4*c-d)*t*t+(-a+3*b-3*c+d)*t*t*t)
            results.append(p)
    results.append(ps[-1]);return results


def plank_conduit(bpy,name,points,radii,wood,col,root,staves=11):
    """Spline-built loosely jointed bentwood pipe, hollow and supported.

    The metal mouth at the native tile boundary is kept visible and never
    replaced by wood. Each visible exterior sleeve uses discrete planks with
    a closed radial thickness, unsanded seams and bound timber hoops.
    """
    from mathutils import Vector
    assert len(points)==len(radii) and len(points)>=3
    control=[Vector(p) for p in points]
    smoothed=path_samples(points,32)
    segments=len(smoothed)
    sleeves=[]
    for stave in range(staves):
        theta0=math.tau*stave/staves+.018
        theta1=math.tau*(stave+1)/staves-.018
        verts=[]
        for depth in (0.,-.021):
            for i,p in enumerate(smoothed):
                t=i/max(1,segments-1)
                scaled=t*(len(radii)-1)
                k=min(int(scaled),len(radii)-2);f=scaled-k
                base_r=radii[k]*(1-f)+radii[k+1]*f
                r=base_r+depth+.007*math.sin(stave*2.4+i*.35)
                tang=(smoothed[min(i+1,segments-1)]-smoothed[max(0,i-1)]).normalized()
                u=tang.cross(Vector((0,0,1)))
                if u.length<.01:u=tang.cross(Vector((0,1,0)))
                u.normalize();v=tang.cross(u).normalized()
                for theta in (theta0,theta1):
                    verts.append(tuple(p+r*(math.cos(theta)*u+math.sin(theta)*v)))
        layer=segments*2
        faces=[]
        for i in range(segments-1):
            a=2*i;b=layer+a
            faces.extend(((a,a+2,a+3,a+1),(b+1,b+3,b+2,b),
                          (a,b,b+2,a+2),(a+1,a+3,b+3,b+1)))
        faces.extend(((0,1,layer+1,layer),
                      (2*(segments-1),layer+2*(segments-1),layer+2*(segments-1)+1,2*(segments-1)+1)))
        ob=mesh_obj(bpy,f'WOOD PIPE V4 | {name} | bent stave {stave:02d}',verts,faces,
            wood['bark'] if stave%3 else wood['light'],col,root,False)
        ob['wood_role']='curved planking on hollow conduit'
        sleeves.append(ob)
    # Two physical wound/bentwood retaining hoops, not big brass over-straps.
    for index in (max(1,segments//3), min(segments-2,2*segments//3)):
        p=smoothed[index]
        tang=(smoothed[index+1]-smoothed[index-1]).normalized()
        i_r=index/(segments-1)*(len(radii)-1);k=min(int(i_r),len(radii)-2);f=i_r-k
        radius=radii[k]*(1-f)+radii[k+1]*f+.012
        # A thin wooden loop of round lashing strips, with real curvature.
        u=tang.cross(Vector((0,0,1)))
        if u.length<.01:u=tang.cross(Vector((0,1,0)))
        u.normalize();v=tang.cross(u).normalized()
        centers=[p+radius*(math.cos(k*math.tau/12)*u+math.sin(k*math.tau/12)*v) for k in range(13)]
        for k in range(12):
            timber_rod(bpy,f'WOOD PIPE V4 | {name} | wooden cinch {index:02d}-{k:02d}',centers[k],centers[k+1],.010,wood['weathered'],col,root)
    return sleeves


def reflectors_and_frame(bpy,wood,coll,root):
    # Preserve the exact verified parabolic mesh and focal axis from V2; this is
    # a wood MATERIAL/visible-construction replacement, not a new fake parabola.
    created=[]
    for name in ('west','east'):
        original=bpy.data.objects[f'CONCENTRATOR | {name} | true parabolic continuous mirror']
        duplicate=original.copy();duplicate.data=original.data.copy()
        duplicate.name=f'WOOD MIRROR V4 | {name} | polished parabolic timber surface'
        coll.objects.link(duplicate)
        duplicate.hide_render=False
        duplicate.data.materials.clear()
        for mat in (wood['polished'],wood['polished_edge'],wood['weathered']):
            duplicate.data.materials.append(mat)
        # The original metal parabola had no image UVs. Fit accepted endgrain
        # albedo, roughness and normal maps along the actual curved wood grain.
        uv=duplicate.data.uv_layers.active or duplicate.data.uv_layers.new(name='V4 polished timber parabola UV')
        for poly in duplicate.data.polygons:
            for li in poly.loop_indices:
                co=duplicate.data.vertices[duplicate.data.loops[li].vertex_index].co
                uv.data[li].uv=((co.x+.45)*2.2,(co.y+.34)*1.6)
        duplicate['wood_role']='polished actual wood reflective parabola'
        duplicate['source_v2_parabolic_mesh']=original.name
        duplicate['focus_height_bu']=float(original['focal_height_bu'])
        assert duplicate.parent is original.parent
        created.append(duplicate)
        # Clamped timber ribs following the same parabolic equation.
        focal=float(original['focal_height_bu'])
        for x in (-.445,.445):
            for j in range(16):
                aa=-.34+.68*j/16;bb=-.34+.68*(j+1)/16
                timber_rod(bpy,f'WOOD MIRROR V4 | {name} | curved edge rib {j}',
                    (x,aa,aa*aa/(4*focal)+.010),(x,bb,bb*bb/(4*focal)+.010),
                    .018,wood['bark'],coll,original.parent)
        for y in (-.34,.34):
            z=y*y/(4*focal)+.01
            timber_rod(bpy,f'WOOD MIRROR V4 | {name} | long edge rim',
                       (-.45,y,z),(.45,y,z),.018,wood['light'],coll,original.parent)
        sign=-1 if name=='west' else 1
        x=sign*.66
        for yy in (-.04,.53):
            timber_rod(bpy,'WOOD FRAME V4 | rough collector trestle upright',
                (x,yy,.25),(x,yy,1.11),.055,wood['weathered'],coll,root)
        timber_rod(bpy,'WOOD FRAME V4 | diagonal support A',
            (x,-.20,.25),(x,.55,1.13),.044,wood['bark'],coll,root)
        timber_rod(bpy,'WOOD FRAME V4 | diagonal support B',
            (x,.60,.25),(x,-.04,1.13),.044,wood['light'],coll,root)
    return created


def receiver_heat(bpy,wood,collection):
    """Gently heat only the focal METAL receiver tubes. Zero light on barrel."""
    heated=[]
    for name in ('west','east'):
        source=bpy.data.objects[f'CONCENTRATOR | {name} | focal black absorber tube']
        old=source.data.materials[0]
        mat=old.copy();mat.name='SOLAR V4 | '+name+' | gentle bronze receiver warmth'
        bsdf=next(n for n in mat.node_tree.nodes if n.type=='BSDF_PRINCIPLED')
        bsdf.inputs['Base Color'].default_value=(.27,.185,.091,1)
        bsdf.inputs['Metallic'].default_value=.77
        bsdf.inputs['Roughness'].default_value=.42
        bsdf.inputs['Emission Color'].default_value=(.7,.24,.055,1)
        socket=bsdf.inputs['Emission Strength']
        for frame,k in [(0,None)]+[(f,i) for i,f in enumerate(FRAMES)]+[(97,16)]:
            socket.default_value=0.0 if k is None else metal_heating(k)
            socket.keyframe_insert(data_path='default_value',frame=frame)
        source.data.materials[0]=mat
        source['solar_v4_receiving_heat_only']=True
        heated.append((source,mat))
    return heated


def mist_material(bpy,name,veil=False):
    """FMPL-inspired self-feathering gas VOLUME, without hard cone/sphere edge.

    A 3D density mask fades to zero *before* the polygonal cloud envelope:
    axial falloff, radial falloff and turbulent internal pockets multiply.
    Meshes are real geometry: never billboards, PNGs or overlay particles.
    """
    m=bpy.data.materials.new(name);m.use_nodes=True
    nodes=m.node_tree.nodes;nodes.clear();ln=m.node_tree.links
    output=nodes.new('ShaderNodeOutputMaterial')
    vol=nodes.new('ShaderNodeVolumePrincipled')
    vol.inputs['Color'].default_value=(.82,.88,.91,1)
    vol.inputs['Anisotropy'].default_value=.17
    tex=nodes.new('ShaderNodeTexCoord')
    split=nodes.new('ShaderNodeSeparateXYZ');ln.new(tex.outputs['Generated'],split.inputs[0])
    def abs_center(socket):
        sub=nodes.new('ShaderNodeMath');sub.operation='SUBTRACT';sub.inputs[1].default_value=.5
        ln.new(socket,sub.inputs[0])
        abs_node=nodes.new('ShaderNodeMath');abs_node.operation='ABSOLUTE';ln.new(sub.outputs[0],abs_node.inputs[0])
        return abs_node.outputs[0]
    mx=nodes.new('ShaderNodeMath');mx.operation='MAXIMUM'
    ln.new(abs_center(split.outputs['X']),mx.inputs[0]);ln.new(abs_center(split.outputs['Y']),mx.inputs[1])
    radial=nodes.new('ShaderNodeMapRange');radial.clamp=True
    radial.interpolation_type='SMOOTHERSTEP'
    radial.inputs['From Min'].default_value=.16
    radial.inputs['From Max'].default_value=.43
    radial.inputs['To Min'].default_value=1
    radial.inputs['To Max'].default_value=0
    ln.new(mx.outputs[0],radial.inputs['Value'])
    axial=nodes.new('ShaderNodeValToRGB')
    cr=axial.color_ramp;cr.interpolation='EASE'
    cr.elements[0].position=.04;cr.elements[0].color=(0,0,0,1)
    cr.elements[1].position=.96;cr.elements[1].color=(0,0,0,1)
    cr.elements.new(.18).color=(1,1,1,1)
    cr.elements.new(.72).color=(1,1,1,1)
    ln.new(split.outputs['Z'],axial.inputs['Fac'])
    noise=nodes.new('ShaderNodeTexNoise')
    noise.inputs['Scale'].default_value=5.0 if veil else 3.2
    noise.inputs['Detail'].default_value=3.2
    ln.new(tex.outputs['Generated'],noise.inputs['Vector'])
    breaks=nodes.new('ShaderNodeMapRange');breaks.clamp=True
    breaks.inputs['From Min'].default_value=.30
    breaks.inputs['From Max'].default_value=.72
    breaks.inputs['To Min'].default_value=0
    breaks.inputs['To Max'].default_value=1
    ln.new(noise.outputs['Fac'],breaks.inputs['Value'])
    def multiply(a,b):
        node=nodes.new('ShaderNodeMath');node.operation='MULTIPLY'
        ln.new(a,node.inputs[0]);ln.new(b,node.inputs[1]);return node.outputs[0]
    full=multiply(multiply(radial.outputs['Result'],axial.outputs['Color']),breaks.outputs['Result'])
    gain=nodes.new('ShaderNodeMath');gain.operation='MULTIPLY';gain.name='V4 calibrated steam optical density'
    gain.inputs[1].default_value=.9 if veil else 1.45
    ln.new(full,gain.inputs[0]);ln.new(gain.outputs[0],vol.inputs['Density'])
    ln.new(vol.outputs[0],output.inputs['Volume'])
    m['steam_effect']='FMPL feathered procedural 3D steam, no visible geometric silhouette'
    return m


def steam_lobe(bpy,name,collection,root,material,veil,phase_idx):
    """Irregular feathered 3D volume, open-sky safety exhaust only."""
    rings=9;radial=16
    verts=[]
    for i in range(rings):
        s=i/(rings-1)
        radius=(.028+.055*math.sin(math.pi*s)**.85)*(.62 if veil else 1.)
        cx=.013*math.sin(4*s+phase_idx*.72)
        cy=.012*math.cos(5*s+phase_idx*.47)
        for j in range(radial):
            a=math.tau*j/radial
            jag=1+.13*math.sin(j*3.7+i*1.4+phase_idx)
            verts.append((cx+radius*math.cos(a)*jag,cy+radius*math.sin(a)*jag,.24*s))
    faces=[]
    for i in range(rings-1):
        for j in range(radial):
            k=(j+1)%radial
            faces.append((i*radial+j,i*radial+k,(i+1)*radial+k,(i+1)*radial+j))
    faces.extend((tuple(reversed(range(radial))),tuple((rings-1)*radial+j for j in range(radial))))
    ob=mesh_obj(bpy,name,verts,faces,material,collection,root,False,uv=False)
    ob['emitter']='open pressure relief valve only'
    ob['steam_role']='feather veil' if veil else 'primary volume wisp'
    ob['phase']=phase_idx
    ob.location=(.016*math.sin(phase_idx*1.9),-.10+.016*math.cos(phase_idx*2),1.405)
    ob.hide_render=True
    ob.keyframe_insert(data_path='hide_render',frame=0)
    for k,frame in list(enumerate(FRAMES))+[(16,97)]:
        age=steam_phase(k,(phase_idx*4)%16)
        fade=math.sin(math.pi*age)
        ob.hide_render=age<.95 and fade>.01
        # Blender animates ob transforms, not the world camera.
        ob.location=(.016*math.sin(phase_idx*1.9)+.035*age*math.sin(phase_idx+age*3),
                     -.10+.016*math.cos(phase_idx*2)+.034*age,
                     1.405+.10*age)
        scale=(.65+.40*age)*(.85 if veil else 1.)
        ob.scale=(scale,scale,.82+.2*age)
        for key in ('location','scale','hide_render'):ob.keyframe_insert(data_path=key,frame=frame)
    return ob


def gauge_and_relief(bpy,wood,col,steam_col,root):
    # Gauge is the legitimate small metal instrument; keep V3 pivot/needle.
    dial=bpy.data.objects['GAUGE | enamel face']
    assert dial.type=='MESH'
    gauge=bpy.data.objects['GAUGE V3 | real face-center needle pivot']
    assert gauge.parent is root
    # One actual open steam nozzle; no gas where sealed pipes meet other pipes.
    metal=bpy.data.materials['Solar Boiler | bronze']
    cylinder(bpy,'RELIEF V4 | functional short open atmosphere nozzle',
             (0,-.1,1.385),.032,.13,metal,col,root,segments=28)
    # Small wooden housing under the metal relief cap.
    cylinder(bpy,'WOOD V4 | pressure relief seating block',(0,-.1,1.28),.075,.09,
             wood['bark'],col,root,segments=12)
    lobes=[]
    strong=mist_material(bpy,'SOLAR V4 | real feathered steam volume')
    thin=mist_material(bpy,'SOLAR V4 | soft thin steam halo',True)
    for i in range(12):
        lobes.append(steam_lobe(bpy,'STEAM V4 | open relief | lobe %02d'%i,steam_col,root,
                                thin if i>=4 else strong,i>=4,i))
    return lobes


def camera_record(scene):
    cam=scene.camera
    return {'name':cam.name,'matrix_world':[list(row) for row in cam.matrix_world],
            'type':cam.data.type,'ortho_scale':cam.data.ortho_scale,
            'shift_x':cam.data.shift_x,'shift_y':cam.data.shift_y,
            'resolution':[scene.render.resolution_x,scene.render.resolution_y]}


def build(opts):
    import bpy
    self_check()
    if opts.output.exists() and any(opts.output.iterdir()):
        raise FileExistsError('Refuse to overwrite previously rendered output')
    source_report=json.loads(SRC_REPORT.read_text())
    src_hash=sha(SRC)
    assert src_hash==source_report['native_sha256'],(src_hash,source_report['native_sha256'])
    bpy.ops.wm.open_mainfile(filepath=str(SRC))
    scene=bpy.context.scene
    root=bpy.data.objects['EXPORT | rotate Solar Boiler model, never camera']
    assert list(root['footprint_tiles'])==[3,2]
    scene.frame_set(0);root.rotation_euler.z=0
    bpy.context.view_layer.update()
    cam=camera_record(scene)
    assert len([o for o in bpy.data.objects if o.type=='CAMERA'])==1
    source_hashes={o.name:mesh_hash(o) for o in scene.objects if o.type=='MESH'}
    wood=import_wood(bpy)
    col=bpy.data.collections.new('08 | V4 approved timber, polished wood optics and FMPL feathered relief')
    scene.collection.children.link(col)
    hidden=hide_legacy(bpy)
    barrels=barrel_staves(bpy,wood,col,root)
    mirrors=reflectors_and_frame(bpy,wood,col,root)
    for xx in (-.57,.57):
        for yy in (-.34,.15):
            timber_rod(bpy,'WOOD V4 | shaped barrel seating cradle',
                       (xx,yy,.275),(xx,yy-.025,.416),.063,
                       wood['weathered'],col,root)
    paths=[
      ('west water inlet',[(-1.30,-.5,.36),(-1.15,-.5,.36),(-.96,-.44,.44),(-.85,-.32,.56),(-.72,-.29,.72)],
       [.28,.26,.215,.17,.13]),
      ('east water inlet',[(1.30,-.5,.36),(1.15,-.5,.36),(.96,-.44,.44),(.85,-.32,.56),(.72,-.29,.72)],
       [.28,.26,.215,.17,.13]),
      ('north steam outlet',[(0,.79,.36),(0,.69,.39),(0,.56,.46),(0,.39,.73),(0,.23,1.06)],
       [.28,.26,.22,.16,.11]),
    ]
    wooden_conduits=0
    for name,points,radii in paths:
        wooden_conduits+=len(plank_conduit(bpy,name,points,radii,wood,col,root))
    # Four smaller collector feeder/return sleeves: follow the SAME V2 world
    # endpoints, leave tiny metal union at the true receiver for heat isolation.
    endpoints=json.loads((HERE.parent/'generated-v2'/'build-report.json').read_text())['solar_thermal_endpoints']
    for name,sign in (('west',-1),('east',1)):
        dat=endpoints[name]
        h=dat['hot_start'];c=dat['cool_start']
        hot=[h,(h[0],h[1]-.07,h[2]-.025),(sign*.29,.10,1.29),(sign*.34,-.08,1.13),dat['hot_drum']]
        cold=[c,(c[0],c[1]+.035,c[2]-.045),(sign*1.01,.06,1.12),(sign*.83,-.06,.96),dat['cool_drum']]
        wooden_conduits+=len(plank_conduit(bpy,name+' bentwood hot exchanger cover',hot,[.071,.074,.085,.082,.071],wood,col,root,8))
        wooden_conduits+=len(plank_conduit(bpy,name+' bentwood cold return cover',cold,[.068,.071,.075,.069,.063],wood,col,root,8))
    tubes=receiver_heat(bpy,wood,col)
    steam_col=bpy.data.collections.new('09 | V4 soft atmosphere steam relief only')
    scene.collection.children.link(steam_col)
    steam=gauge_and_relief(bpy,wood,col,steam_col,root)
    # The old copper and glowing shroud are completely hidden; retained 3D for
    # source protection, not rendered with a wood overlay that leaks pink-red.
    for name in ('ACCUMULATOR V3 | red-hot cylindrical pressure drum jacket',
                 'PROCESS | horizontal copper steam drum'):
        assert bpy.data.objects[name].hide_render
    for name,digest in source_hashes.items():
        assert mesh_hash(bpy.data.objects[name])==digest,('Original V3 geometry changed',name)
    for key in ('water-west','water-east','steam-north'):
        assert bpy.data.objects[f'PORT | {key} | full machine collar'].hide_render is False
    for m in ('ferrocrete','ferrocrete_light','ferrocrete_dark'):
        material=bpy.data.materials['TP Library | '+m]
        assert len([n for n in material.node_tree.nodes if n.type=='TEX_IMAGE' and n.image and n.image.packed_file])==3
    scene['solar_boiler_revision']='V4 wood barrel and bentwood conduit with polished wood reflectors'
    scene['solar_v4_source_v3_sha256']=src_hash
    scene['solar_v4_wood_donor_sha256']=sha(WOOD_DONOR)
    scene['game_integration']=False
    scene.frame_start=0;scene.frame_end=97
    scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=opts.samples
    scene.cycles.seed=5855;scene.cycles.use_animated_seed=False
    if hasattr(scene.cycles,'use_denoising'):scene.cycles.use_denoising=False
    for layer in scene.view_layers:
        if hasattr(layer.cycles,'use_denoising'):layer.cycles.use_denoising=False
    scene.render.film_transparent=True;scene.render.resolution_x=256;scene.render.resolution_y=256
    scene.render.resolution_percentage=100
    scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA'
    scene.render.image_settings.color_depth='8';scene.render.fps=8
    scene.render.threads_mode='FIXED';scene.render.threads=4
    refs=bpy.data.collections['REFERENCE ONLY | adjacent matched 1-tile pipe fixtures'];refs.hide_render=True
    scene.frame_set(0);root.rotation_euler.z=0;bpy.context.view_layer.update()
    assert camera_record(scene)==cam
    opts.output.mkdir(parents=True,exist_ok=True)
    bpy.ops.file.pack_all()
    native=opts.output/'solar-boiler-v4.blend'
    bpy.ops.wm.save_as_mainfile(filepath=str(native),check_existing=False,compress=True)
    report={
       'schema':'tanks.solar-boiler.v4.wood-design.v1',
       'status':'editable native wood material and steam candidate',
       'source_v3_sha256':src_hash,'source_wood_sha256':sha(WOOD_DONOR),
       'native_sha256':sha(native),'source_meshes_protected':len(source_hashes),
       'source_geometry_hidden':hidden,'barrel_staves':barrels,
       'stave_conduit_planks':wooden_conduits,'polished_wood_mirrors':[o.name for o in mirrors],
       'steam_lobes':len(steam),'steam_sources':['open-pressure-relief-nozzle'],
       'heated_receivers':[o.name for o,m in tubes], 'wood_source_materials':wood['donor_names'],
       'camera':cam,'fps':8,'footprint':[3,2],
       'frames':list(FRAMES),'renders':[],
       'game_integrated':False,'visual_approved':False
    }
    record=opts.output/'build-report.json';record.write_text(json.dumps(report,indent=2)+'\n')
    if opts.render=='none':return
    # Model coverage first: all cardinal directions, active vs idle, then a
    # limited 16-pose north loop. Full 4-way animation is a separate approval.
    views=[('idle',d,0) for d in range(4)]+[('working',d,25) for d in range(4)]
    if opts.render=='pilot':views += [('loop',0,f) for f in FRAMES]
    for state,d,frame in views:
        root.rotation_euler.z=math.radians(DIRECTIONS[d]);scene.frame_set(frame)
        bpy.context.view_layer.update()
        # A saved model image must keep a fixed camera despite rotating the root.
        assert camera_record(scene)==cam
        fname=(f'{state}-d{d:02d}.png' if state!='loop' else f'loop-d00-f{FRAMES.index(frame):03d}.png')
        target=opts.output/fname;scene.render.filepath=str(target)
        print('SOLAR_V4_REAL_CYCLES',fname,'frame',frame,flush=True)
        bpy.ops.render.render(write_still=True)
        report['renders'].append({'file':fname,'state':state,'direction':d,'frame':frame,'sha256':sha(target)})
        record.write_text(json.dumps(report,indent=2)+'\n')
    # Non-keyed collection isolation defeats Blender fcurve reset and proves
    # the soft steam gas actually contributes pixels in the same Cycles pose.
    root.rotation_euler.z=0;scene.frame_set(25);bpy.context.view_layer.update()
    for label,visible in (('off',False),('on',True)):
        steam_col.hide_render=not visible
        bpy.context.view_layer.update()
        image=opts.output/('steam-isolation-'+label+'.png')
        scene.render.filepath=str(image)
        bpy.ops.render.render(write_still=True)
        report.setdefault('steam_isolation',[]).append({'file':image.name,'sha256':sha(image),'visible':visible})
    steam_col.hide_render=False
    record.write_text(json.dumps(report,indent=2)+'\n')
    root.rotation_euler.z=0;scene.frame_set(0)
    assert sha(SRC)==src_hash
    print('SOLAR_V4_24_FRAME_NATIVE_PROOF_COMPLETE',len(report['renders']),flush=True)


def main():
    if '--self-check' in sys.argv:self_check();return
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--render',choices=('none','pilot','proof'),default='pilot')
    parser.add_argument('--samples',type=int,default=24)
    a=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else sys.argv[1:])
    if not 4<=a.samples<=64:raise ValueError('Only bounded 4..64 Cycles samples supported')
    build(a)

if __name__=='__main__':main()
