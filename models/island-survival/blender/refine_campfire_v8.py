#!/usr/bin/env python3
"""Refine native V7 .blend materials and flame keys IN BLENDER; keep editable meshes.
All artwork generated here is native procedural Blender shader work.
No image generation and no unverified third-party bitmaps.
"""
from __future__ import annotations
import argparse, math, random, sys
from pathlib import Path
import bpy
from mathutils import Vector

argv=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
parser=argparse.ArgumentParser()
parser.add_argument('--out',type=Path,required=True)
parser.add_argument('--samples',type=int,default=20)
parser.add_argument('--resolution',type=int,default=512)
opts=parser.parse_args(argv)
opts.out.mkdir(parents=True,exist_ok=True)
scene=bpy.context.scene
assert scene.render.engine=='CYCLES' and scene.camera
stones=sorted((o for o in scene.objects if o.type=='MESH' and o.name.startswith('stone_')),key=lambda o:o.name)
wood=sorted((o for o in scene.objects if o.type=='MESH' and any(c.name=='02 | Firewood' for c in o.users_collection)),key=lambda o:o.name)
flames=sorted((o for o in scene.objects if o.type=='MESH' and o.name.startswith('flame_tongue')),key=lambda o:o.name)
assert len(stones)==15 and len(flames)==6 and len(wood)>=25, (len(stones),len(flames),len(wood))
assert len([im for im in bpy.data.images if im.packed_file])>=15
LIGHT=bpy.data.objects['04 | animated fire light']
assert LIGHT.type=='LIGHT' and LIGHT.data.animation_data

def newmat(name):
    m=bpy.data.materials.new('CF8 | '+name)
    m.use_nodes=True
    nodes=m.node_tree.nodes;nodes.clear()
    links=m.node_tree.links
    output=nodes.new('ShaderNodeOutputMaterial');output.location=(950,100)
    return m,nodes,links,output

def node(ns,typ,name,x,y):
    n=ns.new(typ);n.label=name;n.location=(x,y)
    return n

def ramp(ns,positions,colors,name,x,y):
    n=node(ns,'ShaderNodeValToRGB',name,x,y)
    elems=n.color_ramp.elements
    elems.remove(elems[1])
    elems[0].position=positions[0];elems[0].color=(*colors[0],1) if len(colors[0])==3 else colors[0]
    for p,c in zip(positions[1:],colors[1:]):
        e=elems.new(p);e.color=(*c,1) if len(c)==3 else c
    n.color_ramp.interpolation='EASE'
    return n

def normal_from_original(ns,links,family,x=-600,y=-420):
    im=bpy.data.images.get('CF7 | '+family+' | normal')
    assert im and im.packed_file, 'Missing packed tangent normal '+family
    tex=node(ns,'ShaderNodeTexImage','Existing packed normal map / Non-Color',x,y)
    tex.image=im;im.colorspace_settings.name='Non-Color'
    coords=node(ns,'ShaderNodeTexCoord','Existing UVs',x-230,y)
    links.new(coords.outputs['UV'],tex.inputs['Vector'])
    nm=node(ns,'ShaderNodeNormalMap','Tangent normal map',x+230,y)
    nm.inputs['Strength'].default_value={'stone':.24,'bark':.29,'endgrain':.22}[family]
    links.new(tex.outputs['Color'],nm.inputs['Color'])
    return nm.outputs['Normal']

def noise(ns,links,vec,name,scale,detail,x,y):
    n=node(ns,'ShaderNodeTexNoise',name,x,y)
    n.inputs['Scale'].default_value=scale
    n.inputs['Detail'].default_value=detail
    n.inputs['Roughness'].default_value=.66
    links.new(vec,n.inputs['Vector'])
    return n

def surf(ns,links,out):
    p=node(ns,'ShaderNodeBsdfPrincipled','Physical nonmetallic surface',690,80)
    p.inputs['Metallic'].default_value=0
    links.new(p.outputs['BSDF'],out.inputs['Surface'])
    return p

def map_range(ns,links,socket,low,high,x,y):
    n=node(ns,'ShaderNodeMapRange','Physical roughness range',x,y)
    n.inputs['From Min'].default_value=0.0
    n.inputs['From Max'].default_value=1.0
    n.inputs['To Min'].default_value=low
    n.inputs['To Max'].default_value=high
    links.new(socket,n.inputs['Value'])
    return n.outputs['Result']

def close_normals(ns,links,p,normal,displacement,amount,x,y):
    b=node(ns,'ShaderNodeBump','Surface-scale micro relief',x,y)
    b.inputs['Strength'].default_value=amount
    b.inputs['Distance'].default_value=displacement
    links.new(normal,b.inputs['Normal'])
    links.new(b.outputs['Normal'],p.inputs['Normal'])
    return b

# Unique stone materials: object-specific seeded palette + two independent scales
# of noise and original packed tangent normal maps; no repeated identical boulders.
for i,o in enumerate(stones):
    rand=random.Random(6100+i*31)
    v=rand.uniform(.78,1.24)
    warm=rand.uniform(-.06,.07)
    colors=[
        (v*.12,v*.115+warm*.3,v*.105+warm*.14),
        (v*.27,v*.255+warm*.36,v*.225+warm*.20),
        (v*.46,v*.425+warm*.35,v*.38+warm*.20)
    ]
    colors=[tuple(max(0,min(.9,n)) for n in c) for c in colors]
    m,ns,links,out=newmat('stone %02d | %s'%(i+1,o.name))
    coords=node(ns,'ShaderNodeTexCoord','Object-local generated coordinates',-1250,150)
    mapper=node(ns,'ShaderNodeMapping','Unique stone orientation / scale',-1050,190)
    mapper.inputs['Location'].default_value=tuple(rand.uniform(-5,5) for _ in range(3))
    mapper.inputs['Scale'].default_value=(rand.uniform(.9,1.4),rand.uniform(.9,1.5),rand.uniform(1.0,1.6))
    links.new(coords.outputs['Generated'],mapper.inputs['Vector'])
    coarse=noise(ns,links,mapper.outputs['Vector'],'Stone mineral patches',4.0,4,-800,210)
    fine=noise(ns,links,mapper.outputs['Vector'],'Stone micro chips',27,3,-800,-120)
    cr=ramp(ns,[.33,.52,.72],colors,'Non-uniform mineral color',-420,220)
    links.new(coarse.outputs['Fac'],cr.inputs['Fac'])
    p=surf(ns,links,out)
    links.new(cr.outputs['Color'],p.inputs['Base Color'])
    links.new(map_range(ns,links,coarse.outputs['Fac'],.77,.97,-400,-60),p.inputs['Roughness'])
    bump=close_normals(ns,links,p,normal_from_original(ns,links,'stone'),.044,.22,310,-190)
    links.new(fine.outputs['Fac'],bump.inputs['Height'])
    for n in range(len(o.data.materials)):o.data.materials[n]=m
    o['CF8 stone hue']=round(v,3)
    for poly in o.data.polygons:poly.use_smooth=True

# Non-repeating bark color, growth-grain, weathering and char depth. Every log
# receives its own material seed, but cut ends stay distinct/editable.
for i,o in enumerate(wood):
    rand=random.Random(7400+i*43)
    dim=o.dimensions
    along_x=dim.x>=dim.y
    for slot in range(len(o.data.materials)):
        old=o.data.materials[slot]
        old_name=(old.name.lower() if old else '')
        is_end=any(tag in old_name for tag in ('cut','ring','sapwood','heart'))
        is_char=('char' in old_name or 'coal' in old_name)
        family='endgrain' if is_end else 'bark'
        m,ns,links,out=newmat('%s | wood %02d | %s'%(('cut' if is_end else 'bark'),i+1,slot))
        coords=node(ns,'ShaderNodeTexCoord','Per-piece generated UV',-1250,150)
        mapper=node(ns,'ShaderNodeMapping','Grain direction and unique offset',-1040,180)
        mapper.inputs['Location'].default_value=tuple(rand.uniform(-3,3) for _ in range(3))
        mapper.inputs['Scale'].default_value=(.75,9,10) if along_x else (9,.75,10)
        links.new(coords.outputs['Generated'],mapper.inputs['Vector'])
        grain=noise(ns,links,mapper.outputs['Vector'],'Lengthwise wood fibers',4.3,3,-800,200)
        bark_variation=noise(ns,links,coords.outputs['Generated'],'Non-repeating scorch / weathering',5,3,-800,-120)
        tone=rand.uniform(.69,1.28)
        if is_end:
            colors=[(.14*tone,.068*tone,.035*tone),(.41*tone,.24*tone,.105*tone),(.65*tone,.42*tone,.22*tone)]
        elif is_char:
            colors=[(.055,.045,.035),(.16,.10,.062),(.31,.18,.085)]
        else:
            colors=[(.045*tone,.028*tone,.017*tone),(.16*tone,.084*tone,.035*tone),(.37*tone,.22*tone,.09*tone)]
        cr=ramp(ns,[.31,.52,.70],colors,'Per-log fiber and stain palette',-410,230)
        links.new(grain.outputs['Fac'],cr.inputs['Fac'])
        colorMix=node(ns,'ShaderNodeMixRGB','Subtle weathered patches',-80,215)
        colorMix.blend_type='MULTIPLY'
        colorMix.inputs[0].default_value=.36
        links.new(cr.outputs['Color'],colorMix.inputs[1])
        weather=ramp(ns,[.26,.70],[(.55,.55,.55),(1,1,1)],'Weathering',-380,-15)
        links.new(bark_variation.outputs['Fac'],weather.inputs['Fac'])
        links.new(weather.outputs['Color'],colorMix.inputs[2])
        p=surf(ns,links,out)
        links.new(colorMix.outputs['Color'],p.inputs['Base Color'])
        links.new(map_range(ns,links,grain.outputs['Fac'],.72,.94,-105,-130),p.inputs['Roughness'])
        bump=close_normals(ns,links,p,normal_from_original(ns,links,family),.030,.19,340,-200)
        links.new(grain.outputs['Fac'],bump.inputs['Height'])
        o.data.materials[slot]=m
    for poly in o.data.polygons:
        if len(o.data.polygons)>8:poly.use_smooth=True

# Flames: physically separated translucent emissive meshes. Height-based
# yellow/white base -> gold -> orange -> deep-red transparent tips; animated
# 4D noise opacity and *actual shape keys* create a coherent flicker loop.
for i,o in enumerate(flames):
    m,ns,links,out=newmat('flame %02d | vertical color and fading alpha'%i)
    coord=node(ns,'ShaderNodeTexCoord','Flame local position',-1000,250)
    xyz=node(ns,'ShaderNodeSeparateXYZ','Vertical profile',-750,270)
    links.new(coord.outputs['Generated'],xyz.inputs['Vector'])
    palette=ramp(ns,[0,.14,.38,.69,1],[
        (1.0,.86,.32),(1.0,.71,.09),(.99,.36,.020),(.80,.105,.012),(.25,.012,.004)
    ],'Pale-hot base to fading red tip',-450,350)
    links.new(xyz.outputs['Z'],palette.inputs['Fac'])
    fade=ramp(ns,[0,.26,.59,.80,1],[
        (.84,.84,.84),(.80,.80,.80),(.52,.52,.52),(.20,.20,.20),(.015,.015,.015)
    ],'Smooth opacity lead-off',-440,-95)
    links.new(xyz.outputs['Z'],fade.inputs['Fac'])
    animated=node(ns,'ShaderNodeTexNoise','Animated 4D flame breakup',-720,-360)
    animated.noise_dimensions='4D'
    animated.inputs['Scale'].default_value=7
    animated.inputs['Detail'].default_value=2.2
    animated.inputs['Roughness'].default_value=.63
    links.new(coord.outputs['Generated'],animated.inputs['Vector'])
    mask=node(ns,'ShaderNodeMath','Fade multiplied by irregular edge',-120,-130)
    mask.operation='MULTIPLY'
    links.new(fade.outputs['Color'],mask.inputs[0])
    links.new(animated.outputs['Fac'],mask.inputs[1])
    transparent=node(ns,'ShaderNodeBsdfTransparent','Soft invisible edges',120,120)
    emission=node(ns,'ShaderNodeEmission','True gradient emission',130,-100)
    emission.inputs['Strength'].default_value=1.35
    links.new(palette.outputs['Color'],emission.inputs['Color'])
    mix=node(ns,'ShaderNodeMixShader','Transparent / emitting flames',480,85)
    links.new(mask.outputs['Value'],mix.inputs[0])
    links.new(transparent.outputs['BSDF'],mix.inputs[1])
    links.new(emission.outputs['Emission'],mix.inputs[2])
    links.new(mix.outputs['Shader'],out.inputs['Surface'])
    for slot in range(len(o.data.materials)):o.data.materials[slot]=m
    animated.inputs['W'].default_value=0
    for frame in (1,13,25,37,49,61,73,85,97):
        phase=2*math.pi*(frame-1)/96
        animated.inputs['W'].default_value=.68*math.sin(phase+i*.43)
        animated.inputs['W'].keyframe_insert(data_path='default_value',frame=frame)
    # Shape keys deform only the upper lengths; contact points remain stable.
    basis=o.shape_key_add(name='Basis',from_mix=False)
    sway=o.shape_key_add(name='Wind sway',from_mix=False)
    curl=o.shape_key_add(name='Tip curl',from_mix=False)
    height=[v.co.z for v in o.data.vertices]
    low=min(height);span=max(height)-low or 1.0
    for vid,v in enumerate(o.data.vertices):
        original=basis.data[vid].co
        h=max(0,min(1,(original.z-low)/span))**1.65
        sway.data[vid].co=original+Vector((.14*h,.045*h,0))
        curl.data[vid].co=original+Vector((-.055*h,.115*h,.014*h))
    for frame in (1,13,25,37,49,61,73,85,97):
        phase=2*math.pi*(frame-1)/96
        sway.value=.5+.48*math.sin(phase+i*.8)
        curl.value=.5+.45*math.sin(phase+1.4+i*.55)
        sway.keyframe_insert(data_path='value',frame=frame)
        curl.keyframe_insert(data_path='value',frame=frame)
    o['CF8 gradient']='Pale hot core to translucent orange / red tips'
    o['CF8 motion']='Keyframed shape keys + 4D noise + original transform animation'

# The physical light remains independently animated. Broader orange range,
# restrained relative to stable key/fill/rim; no whole-scene strobing.
LIGHT.data.color=(1.0,.33,.072)
LIGHT.data.shadow_soft_size=.73
ctrl=bpy.data.objects.get('CAMPFIRE CONTROLS | collection 03 toggle fire')
if ctrl:
    ctrl['CF8 revision']='15 unique stone shader graphs, log-wise bark and cuts, animated vertical flame gradient'
    ctrl['CF8 editable animation']='Flame shape keys and material 4D Noise W + existing firelight keyframes'
    ctrl['CF8 provenance']='Original procedural node materials only; external repositories are reference sources'

scene.cycles.samples=opts.samples
scene.render.image_settings.file_format='PNG'
scene.render.image_settings.color_mode='RGBA'
scene.render.film_transparent=True
scene.render.resolution_percentage=100
scene.render.resolution_x=opts.resolution;scene.render.resolution_y=opts.resolution
scene.frame_set(13)
def render(name,active,res):
    for f in flames:f.hide_render=not active
    LIGHT.hide_render=not active
    scene.render.resolution_x=res;scene.render.resolution_y=res
    scene.render.filepath=str(opts.out/name)
    bpy.ops.render.render(write_still=True)
render('campfire-v8-idle.png',False,opts.resolution)
render('campfire-v8-burning.png',True,opts.resolution)
render('campfire-v8-native64.png',True,64)
for f in flames:f.hide_render=False
LIGHT.hide_render=False
scene.render.resolution_x=opts.resolution;scene.render.resolution_y=opts.resolution
scene.frame_set(13)
scene.render.filepath='//campfire-v8-burning.png'
blend=opts.out/'campfire-v8-animated.blend'
bpy.ops.wm.save_as_mainfile(filepath=str(blend),compress=True)
triangles=sum(len(o.data.polygons) for o in scene.objects if o.type=='MESH' and o.name!='Ground | shadow catcher')
assert triangles==12152
report='\n'.join([
    'V8 actual native Blender material and animation revision',
    'Blender version: '+bpy.app.version_string,
    'Triangles: '+str(triangles),
    'Distinct stone material instances: '+str(len(stones)),
    'Wood material slots revised: '+str(sum(len(o.data.materials) for o in wood)),
    'Animated gradient flame objects: '+str(len(flames)),
    'Packed texture maps: '+str(sum(bool(i.packed_file) for i in bpy.data.images)),
    'Engine: '+scene.render.engine,
    'Animation frames: 1-96',
    'Source: actual V7 Blender native scene',
    'Assets: no unverified third party art',
])+'\n'
(opts.out/'campfire-v8-build-report.txt').write_text(report)
print('CF8_SCENE_OK',report,flush=True)
