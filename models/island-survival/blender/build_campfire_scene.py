#!/usr/bin/env python3
"""Tanks for Bob campfire: editable, animated native Blender scene.

Run with:
 blender -b -t 4 --python build_campfire_scene.py -- --obj path/to/campfire-smoothed-v6.obj --out outdir

No Wube artwork or unverified third-party texture is embedded. All procedural
maps are generated inside Blender and packed as editable images in .blend.
"""
from __future__ import annotations
import argparse, math, random, sys
from pathlib import Path

import bpy
from mathutils import Vector

BLENDER_VERSION = bpy.app.version
if BLENDER_VERSION < (3, 6, 0):
    raise RuntimeError('Blender 3.6 or newer required')

args = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
p = argparse.ArgumentParser()
p.add_argument('--obj', type=Path, required=True)
p.add_argument('--out', type=Path, required=True)
p.add_argument('--samples', type=int, default=24)
p.add_argument('--resolution', type=int, default=512)
opts = p.parse_args(args)
opts.out.mkdir(parents=True, exist_ok=True)

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
for d in list(bpy.data.collections):
    if d.name != bpy.context.scene.collection.name:
        if d.users == 0: bpy.data.collections.remove(d)

scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.cycles.samples = opts.samples
scene.cycles.use_denoising = False
# Ubuntu/Debian Blender builds may not include OpenImageDenoise.
# Keep the rendering usable on stock Blender without optional denoiser.
scene.render.film_transparent = True
try: bpy.context.view_layer.cycles.use_denoising = False
except AttributeError: pass
scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_mode = 'RGBA'
scene.render.resolution_percentage = 100
scene.render.resolution_x = opts.resolution
scene.render.resolution_y = opts.resolution
try: scene.view_settings.view_transform = 'AgX'
except Exception: scene.view_settings.view_transform = 'Standard'
try: scene.view_settings.look = 'Medium High Contrast'
except Exception: pass
scene.frame_start=1
scene.frame_end=96
scene.render.film_transparent=True
scene.world.use_nodes = True
bg=scene.world.node_tree.nodes.get('Background')
if bg:
    bg.inputs['Color'].default_value=(0.52,0.59,0.67,1)
    bg.inputs['Strength'].default_value=0.38

# Distinct, editable collections: no merged fire/solid/lighting objects.
def col(name):
    c=bpy.data.collections.new(name)
    scene.collection.children.link(c)
    return c
stones_col=col('01 | Stones + ash + coals')
wood_col=col('02 | Firewood')
flame_col=col('03 | Animated fire tongues')
lights_col=col('04 | Factorio lighting rig')
controls_col=col('05 | Camera + controls')
ground_col=col('06 | Ground shadow catcher')

def place_obj_in_collection(obj, dest):
    for collection in list(obj.users_collection): collection.objects.unlink(obj)
    dest.objects.link(obj)

# Procedural per-material image maps. The image nodes remain editable in Blender;
# the files are packed so the native .blend is truly self-contained.
MAP_SIZE=192
family_color={
    'stone': (0.47,0.46,0.43),
    'bark': (0.31,0.19,0.095),
    'endgrain': (0.66,0.45,0.25),
    'ash': (0.25,0.25,0.23),
    'char': (0.11,0.095,0.085)
}
family_roughness={'stone':0.91,'bark':0.86,'endgrain':0.77,'ash':0.98,'char':0.92}
normal_strength={'stone':0.18,'bark':0.32,'endgrain':0.30,'ash':0.25,'char':0.24}

# Fast periodic waveform noise that yields separate proper tangent-space normal maps.
# No third party art or external dependencies.
def field(u,v,f):
    twopi=2*math.pi
    if f=='bark':
        return .5 + .22*math.sin(twopi*(8*u +.2*math.sin(twopi*1.3*v))) + .08*math.sin(twopi*21*u+0.8*math.cos(twopi*v)) + .035*math.cos(twopi*(37*u+3*v))
    if f=='endgrain':
        dx=u-.5;dy=v-.5;r=math.hypot(dx,dy)
        return .5+.17*math.sin(2*math.pi*(17*r +.12*math.sin(12*math.atan2(dy,dx))))+.06*math.sin(twopi*(15*u+12*v))
    if f=='stone':
        return .5+.085*math.sin(twopi*(3*u+4*v)) * math.cos(twopi*(4*u-2*v))+.038*math.sin(twopi*(13*u+11*v))+.012*math.sin(twopi*(37*u-29*v))
    if f=='ash':
        return .5+.18*math.sin(twopi*(7*u+8*v))*math.sin(twopi*(6*v-2*u))+.075*math.cos(twopi*(21*u-19*v))
    return .5+.23*math.sin(twopi*6*u)*math.cos(twopi*8*v)+.08*math.sin(twopi*(25*u+19*v))

maps={}
for family in family_color:
    W=MAP_SIZE
    heights=[]
    for y in range(W):
        for x in range(W):
            heights.append(field(x/W,y/W,family))
    def get_height(x,y): return heights[(y%W)*W+(x%W)]
    albedo=[]; rough=[]; normal=[]
    for y in range(W):
        for x in range(W):
            h=get_height(x,y)
            sh=h-.5
            c=family_color[family]
            lit=max(.48,min(1.48,1+.48*sh))
            if family=='stone': lit*=.92+.055*math.sin((x+y)*.17)
            albedo.extend((min(1,c[0]*lit),min(1,c[1]*lit),min(1,c[2]*lit),1))
            r=max(.2,min(1,family_roughness[family] + .11*sh))
            rough.extend((r,r,r,1))
            scale = 1.75 if family=='stone' else (1.2 if family=='bark' else .7)
            dx=(get_height(x-1,y)-get_height(x+1,y))*scale
            dy=(get_height(x,y-1)-get_height(x,y+1))*scale
            n=Vector((dx,dy,1)).normalized()
            normal.extend((.5+.5*n.x,.5+.5*n.y,.5+.5*n.z,1))
    maps[family]={}
    for name,pixels in [('albedo',albedo),('roughness',rough),('normal',normal)]:
        img=bpy.data.images.new(f'CF7 | {family} | {name}',width=W,height=W,alpha=True)
        img.pixels.foreach_set(pixels)
        img.file_format='PNG'
        img.pack()
        maps[family][name]=img

FIRE_COLORS={
    'flame_gold':(1.0,.39,.019,1),
    'flame_orange':(1.0,.15,.012,1),
    'flame_yellow':(1.0,.82,.08,1),
    'embers':(1.0,.25,.025,1)
}
TINTS={
    'stone_dark':.77,'stone_light':1.17,'stone_pale':1.32,'stone_warm':1.03,'stone_base':1,
    'wood_bark':1,'wood_bark_dark':.72,'wood_bark_light':1.21,'wood_weathered':1.18,
    'wood_cut':1,'wood_cut_ring':.75,'wood_sapwood':1.16,'wood_heart':.68,
    'ash':1,'ash_light':1.14,'char':1
}

def family_for(name):
    if name.startswith('stone'):return 'stone'
    if name.startswith('wood_bark') or name=='wood_weathered':return 'bark'
    if name.startswith('wood_'):return 'endgrain'
    if name.startswith('ash'):return 'ash'
    return 'char'

def material(name):
    existing=bpy.data.materials.get('CF7 | '+name)
    if existing:return existing
    m=bpy.data.materials.new('CF7 | '+name)
    m.use_nodes=True
    ns=m.node_tree.nodes
    ns.clear();links=m.node_tree.links
    output=ns.new('ShaderNodeOutputMaterial');output.location=(660,40)
    if name in FIRE_COLORS:
        emission=ns.new('ShaderNodeEmission');emission.inputs['Color'].default_value=FIRE_COLORS[name]
        emission.inputs['Strength'].default_value=1.35 if name!='embers' else 1.1
        emission.location=(270,-100)
        if name.startswith('flame_'):
            # A translucent emission surface keeps animated flame meshes from looking like solid plastic.
            transparent=ns.new('ShaderNodeBsdfTransparent');transparent.location=(0,130)
            mix=ns.new('ShaderNodeMixShader');mix.location=(450,40)
            mix.inputs[0].default_value=.72
            links.new(transparent.outputs['BSDF'],mix.inputs[1])
            links.new(emission.outputs[0],mix.inputs[2])
            links.new(mix.outputs[0],output.inputs['Surface'])
        else:
            links.new(emission.outputs[0],output.inputs['Surface'])
        m.diffuse_color=FIRE_COLORS[name]
        return m
    family=family_for(name)
    bsdf=ns.new('ShaderNodeBsdfPrincipled');bsdf.location=(350,40)
    links.new(bsdf.outputs['BSDF'],output.inputs['Surface'])
    bsdf.inputs['Metallic'].default_value=0
    try: bsdf.inputs['Specular IOR Level'].default_value=.28
    except KeyError: pass
    uv=ns.new('ShaderNodeTexCoord');uv.location=(-1000,20)
    alb=ns.new('ShaderNodeTexImage');alb.image=maps[family]['albedo'];alb.location=(-740,260)
    rough=ns.new('ShaderNodeTexImage');rough.image=maps[family]['roughness'];rough.image.colorspace_settings.name='Non-Color';rough.location=(-740,-15)
    ntex=ns.new('ShaderNodeTexImage');ntex.image=maps[family]['normal'];ntex.image.colorspace_settings.name='Non-Color';ntex.location=(-740,-300)
    for node in (alb,rough,ntex):links.new(uv.outputs['UV'],node.inputs['Vector'])
    tint=ns.new('ShaderNodeMixRGB');tint.blend_type='MULTIPLY';tint.inputs[0].default_value=1
    value=TINTS.get(name,1)
    tint.inputs[2].default_value=(value,value,value,1)
    tint.location=(-275,240)
    links.new(alb.outputs['Color'],tint.inputs[1]);links.new(tint.outputs['Color'],bsdf.inputs['Base Color'])
    links.new(rough.outputs['Color'],bsdf.inputs['Roughness'])
    normal_map=ns.new('ShaderNodeNormalMap');normal_map.location=(-220,-275)
    normal_map.space='TANGENT';normal_map.inputs['Strength'].default_value=normal_strength[family]
    links.new(ntex.outputs['Color'],normal_map.inputs['Color'])
    links.new(normal_map.outputs['Normal'],bsdf.inputs['Normal'])
    m.diffuse_color=(*family_color[family],1)
    return m

# Read the deterministic V6 OBJ directly. Separate mesh objects by g/group;
# UVs and materials are editable in Blender, unlike a flattened preview.
def import_grouped_obj(path):
    positions=[];groups={};current_group='unassigned';current_mat='stone_base'
    for line in path.read_text().splitlines():
        if line.startswith('v '):
            positions.append(tuple(float(a) for a in line.split()[1:4]))
        elif line.startswith('g '):
            current_group=line[2:].strip();groups.setdefault(current_group,[])
        elif line.startswith('usemtl '):current_mat=line[7:].strip()
        elif line.startswith('f '):
            vals=[]
            for tok in line[2:].split():vals.append(int(tok.split('/')[0])-1)
            if len(vals)==3:groups.setdefault(current_group,[]).append((vals,current_mat))
    verts_total=0;faces_total=0;fireobjs=[]
    for group,faces in groups.items():
        if not faces:continue
        indices=sorted(set(i for face,_ in faces for i in face))
        mapping={g:i for i,g in enumerate(indices)}
        xyz=[positions[i] for i in indices]
        triangles=[tuple(mapping[i] for i in f) for f,_ in faces]
        mesh=bpy.data.meshes.new('Mesh | '+group)
        mesh.from_pydata(xyz,[],triangles);mesh.update(calc_edges=True)
        ob=bpy.data.objects.new(group,mesh)
        if group.startswith('flame_tongue'):
            target=flame_col;fireobjs.append(ob)
        elif group.startswith('stone') or group.startswith('ash') or group.startswith('coal'):
            target=stones_col
        else:target=wood_col
        target.objects.link(ob)
        mats=list(dict.fromkeys(mat for _,mat in faces))
        for mat in mats:mesh.materials.append(material(mat))
        lut={mat:i for i,mat in enumerate(mats)}
        xlo=min(x for x,y,z in xyz);xhi=max(x for x,y,z in xyz)
        ylo=min(y for x,y,z in xyz);yhi=max(y for x,y,z in xyz)
        zlo=min(z for x,y,z in xyz);zhi=max(z for x,y,z in xyz)
        cx=(xlo+xhi)/2;cy=(ylo+yhi)/2;cz=(zlo+zhi)/2
        dx=max(.001,xhi-xlo);dy=max(.001,yhi-ylo);dz=max(.001,zhi-zlo)
        group_wood=group.startswith('cross_log')
        mesh.uv_layers.new(name='CF7 | per-component UV')
        uv=mesh.uv_layers.active
        for poly,(_,mat_name) in zip(mesh.polygons,faces):
            poly.material_index=lut[mat_name]
            poly.use_smooth=not ('_end_' in group)
            for loopi in poly.loop_indices:
                vertex=mesh.vertices[mesh.loops[loopi].vertex_index].co
                x,y,z=vertex
                if group_wood:
                    if '_end_' in group:
                        if dx>=dy:u=(y-ylo)/dy;v=(z-zlo)/dz
                        else:u=(x-xlo)/dx;v=(z-zlo)/dz
                    elif dx>=dy:
                        u=(x-xlo)/dx*1.8;v=math.atan2(z-cz,y-cy)/(2*math.pi)+.5
                    else:
                        u=(y-ylo)/dy*1.8;v=math.atan2(z-cz,x-cx)/(2*math.pi)+.5
                elif group.startswith('stone'):
                    u=(math.atan2(y-cy,x-cx)/(2*math.pi)+.5)*1.4
                    v=(z-zlo)/dz
                else:
                    u=(x-xlo)/dx;v=(y-ylo)/dy
                uv.data[loopi].uv=(u,v)
        verts_total+=len(xyz);faces_total+=len(faces)
    return fireobjs,verts_total,faces_total,len(groups)

fireobjs,vertices,triangles,groups=import_grouped_obj(opts.obj)
if triangles!=12152:
    raise AssertionError(f'Expected V6 mesh with 12152 triangles, got {triangles}')

# Fire objects and warm emissive lighting: visible/hidden in collection UI.
for i,ob in enumerate(fireobjs):
    ob['role']='Animated flame; visibility controlled by 03 collection'
    randomizer=random.Random(500+i)
    base_scale=ob.scale.copy()
    for t in (1,13,25,37,49,61,73,85,97):
        u=(t-1)/96*2*math.pi
        ob.scale=(base_scale.x*(1+.05*math.sin(u+i)),base_scale.y*(1+.08*math.cos(u*2+i)),base_scale.z*(1+.11*math.sin(u*2+i*.7)))
        ob.keyframe_insert(data_path='scale',frame=t,group='Flame flicker')
        ob.rotation_euler[2]=.045*math.sin(u+i*.33)
        ob.keyframe_insert(data_path='rotation_euler',frame=t,group='Flame flicker')
    ob.animation_data.action.name='CF7 | flame movement'

# Functional lighting policy: stable, directional daylight + restrained fill/rim,
# physical AO from path tracing; separate colored fire light is keyed.
def aim(obj,target): obj.rotation_euler=(Vector(target)-obj.location).to_track_quat('-Z','Y').to_euler()
def area(name,loc,power,color,size):
    lamp=bpy.data.lights.new(name,'AREA');lamp.energy=power;lamp.color=color;lamp.shape='DISK';lamp.size=size
    ob=bpy.data.objects.new(name,lamp);lights_col.objects.link(ob);ob.location=loc;aim(ob,(0,0,.30));return ob

key=area('01 | NW warm key | broad source',(-3.1,-4.2,6.0),550,(1.00,.91,.77),4.2)
fill=area('02 | SE cool fill | restrained',(3.8,-1.0,4.1),180,(.70,.83,1.00),4.5)
rim=area('03 | rear edge light',(1.1,3.5,3.5),270,(1,.91,.79),3.2)
fl=bpy.data.lights.new('04 | animated ember point','POINT');fl.color=(1,.28,.035);fl.energy=35;fl.shadow_soft_size=.60
fire_light=bpy.data.objects.new('04 | animated fire light',fl);lights_col.objects.link(fire_light);fire_light.location=(.0,.0,.48)
for frame,energy in [(1,29),(13,42),(25,32),(37,38),(49,29),(61,42),(73,32),(85,38),(97,29)]:
    fl.energy=energy;fl.keyframe_insert(data_path='energy',frame=frame)

controller=bpy.data.objects.new('CAMPFIRE CONTROLS | collection 03 toggle fire',None)
controls_col.objects.link(controller);controller.empty_display_type='SPHERE';controller.empty_display_size=.13
controller.location=(0,0,1.35)
controller['Scene notes']='Toggle collection 03 for idle/burning. Animate flame objects and orange light. Static stone and wood never move.'
controller['Normal maps']='Packed native Blender images, Non-Color -> Normal Map -> Principled Normal'
controller['Lighting']='Nauvis-inspired neutral key, cool fill, rear rim, warm flickering fire; path traced ambient occlusion'
controller['Source license']='Own procedural images; references credited in docs; no Snouz/Wube/Unused Renders artwork copied.'

camera_data=bpy.data.cameras.new('Factorio orthographic camera');camera_data.type='ORTHO';camera_data.ortho_scale=2.65
camera=bpy.data.objects.new('Factorio render camera',camera_data);controls_col.objects.link(camera)
camera.location=(3.0,-4.3,3.7);aim(camera,(0,0,.37));scene.camera=camera
camera_data.lens=55

# Ground-only catcher gives soft contact shadow on transparency (Cycles).
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.026))
ground=bpy.context.object;ground.name='Ground | shadow catcher'
place_obj_in_collection(ground,ground_col)
try: ground.is_shadow_catcher=True
except Exception: pass

scene.frame_set(13)
scene.render.resolution_x=opts.resolution;scene.render.resolution_y=opts.resolution

def render(name,burning,resolution):
    for ob in fireobjs:ob.hide_render=not burning
    fire_light.hide_render=not burning
    scene.render.resolution_x=resolution;scene.render.resolution_y=resolution
    scene.render.filepath=str(opts.out/name)
    bpy.ops.render.render(write_still=True)

render('campfire-blender-idle.png',False,opts.resolution)
render('campfire-blender-burning.png',True,opts.resolution)
render('campfire-blender-native64.png',True,64)
for ob in fireobjs:ob.hide_render=False
fire_light.hide_render=False
scene.render.resolution_x=opts.resolution;scene.render.resolution_y=opts.resolution
scene.frame_set(13)
scene.render.filepath='//campfire-blender-burning.png'
bpy.ops.wm.save_as_mainfile(filepath=str(opts.out/'campfire-v7-animated.blend'),compress=True)

# Readback report for CI and manual Blender inspection.
report=(
 f'Blender version: {bpy.app.version_string}\n'
 f'Vertices in separated groups: {vertices}\n'
 f'Triangles: {triangles}\nGroups: {groups}\n'
 f'Material instances: {len([m for m in bpy.data.materials if m.name.startswith("CF7")])}\n'
 f'Packed texture images: {sum(bool(im.packed_file) for im in bpy.data.images)}\n'
 f'Animated fire objects: {len(fireobjs)}\n'
 f'Camera: {camera_data.type}, scale={camera_data.ortho_scale}\n'
 f'Engine: {scene.render.engine}, samples={opts.samples}\n'
)
(opts.out/'campfire-blender-build-report.txt').write_text(report)
print(report)
