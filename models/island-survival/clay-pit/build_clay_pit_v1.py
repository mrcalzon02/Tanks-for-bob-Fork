#!/usr/bin/env python3
"""Source-guided Clay Pit V1 native Blender blockout.

Reference is graphics/entity/clay-pit.png: 120x64 stored, first 64x64
used by prototype. Working overlay adds separate primitive implements.
All geometry is physically authored, editable and reusable; no image planes.
Does not edit gameplay prototypes or existing sprites.
"""
import argparse
import hashlib
import json
import math
import pathlib
import random
import sys

import bpy
from mathutils import Vector


def args_from_blender():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True)
    ap.add_argument('--samples', type=int, default=30)
    argv = sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
    return ap.parse_args(argv)


def coll(name, parent=None):
    result = bpy.data.collections.new(name)
    (parent.children if parent else bpy.context.scene.collection.children).link(result)
    return result


def move(obj, target):
    for old in list(obj.users_collection):
        old.objects.unlink(obj)
    target.objects.link(obj)
    return obj


def mat(name, color, roughness=0.98):
    m=bpy.data.materials.new(name)
    m.use_nodes=True
    p=m.node_tree.nodes.get('Principled BSDF')
    p.inputs['Base Color'].default_value=(*color,1)
    p.inputs['Roughness'].default_value=roughness
    p.inputs['Metallic'].default_value=0
    if p.inputs.get('Specular IOR Level'):
        p.inputs['Specular IOR Level'].default_value=0.12
    return m


def mesh_obj(name, verts, faces, collection, materials, material_ids=None):
    mesh=bpy.data.meshes.new(name+' mesh')
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj=bpy.data.objects.new(name, mesh)
    collection.objects.link(obj)
    for m in materials: obj.data.materials.append(m)
    for p,n in zip(mesh.polygons, material_ids or [0]*len(faces)):
        p.material_index=n
        p.use_smooth=True
    return obj


def make_basin(name, x, y, rx, ry, collection, colors, depth=0.20, seed=14):
    """Editable concentric geometry: broad dry skirt, raised lip, damp inside.

    Shared reusable shape generator for this and future clay/pond/kiln assets.
    Does not create hidden pipework or an underground chamber.
    """
    n=48
    # radius, height, index of band material from this ring toward next ring
    bands=[(1.18,-.018,0),(1.09,.035,0),(.995,.13,1),(.875,.155,1),(.76,.045,2),(.62,-.075,2),(.30,-depth+.015,3),(0,-depth,3)]
    rng=random.Random(seed)
    distort=[1 + 0.028*math.sin((2*math.pi*i/n)*5+.31) + 0.024*math.cos((2*math.pi*i/n)*9-0.15) + rng.uniform(-.013,.013) for i in range(n)]
    vertices=[];faces=[];indices=[]
    for r,z,_ in bands[:-1]:
        for i in range(n):
            t=2*math.pi*i/n
            # source rim has a naturally uneven perimeter, not round machinery
            variation=distort[i] * (1+0.012*math.sin(3*t+z))
            vertices.append((x+rx*r*variation*math.cos(t),y+ry*r*variation*math.sin(t),z+.012*math.sin(t*7+.4)*r))
    for j in range(len(bands)-2):
        for i in range(n):
            nexti=(i+1)%n
            faces.append((j*n+i,j*n+nexti,(j+1)*n+nexti,(j+1)*n+i))
            indices.append(bands[j][2])
    center=len(vertices)
    vertices.append((x,y,-depth))
    j=len(bands)-2
    for i in range(n):
        faces.append((j*n+i,j*n+(i+1)%n,center))
        indices.append(3)
    obj=mesh_obj(name,vertices,faces,collection,colors,indices)
    return obj


def geo_rock(name, place, scales, m, collection, seed):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=1, location=place)
    ob=move(bpy.context.object, collection)
    ob.name=name
    ob.scale=scales
    ob.data.materials.append(m)
    return ob


def rod(name,a,b,radius,material,collection,vertices=9):
    a,b=Vector(a),Vector(b)
    direction=b-a
    midpoint=(a+b)*.5
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=direction.length, location=midpoint)
    ob=move(bpy.context.object, collection)
    ob.name=name
    ob.rotation_euler=direction.to_track_quat('Z','Y').to_euler()
    ob.data.materials.append(material)
    return ob


def spade_head(collection, material):
    # Compact flattened, slightly pointed primitive paddle, not a steel shovel.
    v=[(-.91,-.50,.11),(-.74,-.56,.13),(-.55,-.50,.09),(-.56,-.42,.08),(-.79,-.37,.09),(-.98,-.42,.12)]
    # two-sided for all directional renders
    return mesh_obj('WORK | shallow stone/wood spade blade', v, [(0,1,2,3,4,5),(5,4,3,2,1,0)], collection,[material])


def set_visibility(objects, active):
    for ob in objects:
        ob.hide_render=not active
        ob.keyframe_insert(data_path='hide_render', frame=1 if active else 0)
        if ob.animation_data:
            for curve in ob.animation_data.action.fcurves:
                for key in curve.keyframe_points: key.interpolation='CONSTANT'


def lamp(name,loc,power,color,size,collection,target=(0,0,0)):
    light=bpy.data.lights.new(name,'AREA')
    light.energy=power
    light.shape='DISK'
    light.size=size
    light.color=color
    ob=bpy.data.objects.new(name,light)
    collection.objects.link(ob)
    ob.location=loc
    ob.rotation_euler=(Vector(target)-ob.location).to_track_quat('-Z','Y').to_euler()
    return ob


def main():
    arg=args_from_blender()
    out=pathlib.Path(arg.out).resolve()
    out.mkdir(parents=True,exist_ok=True)
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    scene=bpy.context.scene
    scene.render.engine='CYCLES'
    scene.cycles.samples=arg.samples
    scene.cycles.device='CPU'
    scene.render.film_transparent=True
    scene.render.resolution_x=256
    scene.render.resolution_y=256
    scene.render.resolution_percentage=100
    scene.render.image_settings.file_format='PNG'
    scene.render.image_settings.color_mode='RGBA'
    scene.render.fps=8
    scene.render.image_settings.color_depth='8'
    scene.view_settings.view_transform='Standard'
    scene.view_settings.look='Medium High Contrast'
    scene.world.use_nodes=True
    scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.22,.20,.17,1)
    scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.65
    scene.render.image_settings.compression=12
    main_col=coll('CLAY PIT | reusable earthwork module')
    tools_col=coll('WORKING | primitive implements')
    lighting=coll('FIXED | Factorio lighting and camera')
    soil=mat('DRY | disturbed ochre earth',(.45,.245,.09),1)
    rim=mat('RIM | compacted ochre clay',(.59,.32,.12),.98)
    wall=mat('WALL | exposed damp clay',(.37,.24,.13),.95)
    floor=mat('FLOOR | dark wet clay',(.14,.075,.035),.83)
    clod=mat('CLODS | medium brown',(.34,.19,.08),.97)
    wood=mat('WOOD | crude straight branches',(.29,.18,.09),.96)
    pale=mat('TOOL | muted pale stone',(.46,.40,.28),.95)
    rope=mat('CORD | vegetable fiber',(.39,.29,.11),.98)
    basin=make_basin('01 | one primary excavated basin',0,0,1.12,1.30,main_col,[soil,rim,wall,floor],depth=.215)
    # Sparse clearly visible mud lumps, not random new structures.
    for i,(x,y,s) in enumerate([(-.50,-.33,.11),(-.28,-.46,.11),(.32,-.32,.13),(.57,.20,.08),(-.15,.51,.09)]):
        geo_rock(f'02 | exposed clay clod {i+1}',(x,y,-.11),(s,s*.82,s*.49),clod,main_col,i+11)
    # Small irregularities around the inner ring. Reusable helper meshes remain separate.
    for i,(theta,s) in enumerate([(.12,.07),(.67,.09),(1.62,.05),(2.52,.11),(3.45,.07),(4.26,.08),(5.12,.07)]):
        geo_rock(f'03 | rim fragment {i+1}',(1.12*.91*math.cos(theta),1.30*.91*math.sin(theta),.13),(s,s*.76,s*.28),rim,main_col,i+70)
    # Primitive working overlay: spade to left, stakes and hanging scoop near center.
    objects=[]
    objects.append(rod('WORK | left spade handle',(-1.12,-.52,.32),(-.58,-.45,.14),.025,wood,tools_col))
    objects.append(spade_head(tools_col,pale))
    joint=(.22,.26,.68)
    for name,start,end,r in [
       ('WORK | upright stake',(.14,.22,.07),joint,.032),
       ('WORK | angled stake to south',(.88,-.72,.07),joint,.028),
       ('WORK | angled stake to north',(.93,.71,.06),joint,.023),
       ('WORK | crossbar',(-.13,.17,.59),(1.00,.23,.64),.022)]:
        objects.append(rod(name,start,end,r,wood,tools_col))
    objects.append(rod('WORK | hanging fiber loop',(.18,.22,.62),(.12,.20,.26),.011,rope,tools_col))
    objects.append(geo_rock('WORK | small hanging clay scoop',(.12,.20,.21),(.115,.10,.095),floor,tools_col,72))
    # Source overlay is a still; author deliberate subtle tool movement only.
    # Make movement real via two handful-sized stirring tool pieces, not physics simulation.
    objects.append(rod('WORK | active paddle',(.05,-.28,.02),(.30,-.24,.46),.023,wood,tools_col))
    for ob in objects:
        ob.hide_render=True
        ob.keyframe_insert(data_path='hide_render',frame=0)
        ob.hide_render=False
        ob.keyframe_insert(data_path='hide_render',frame=1)
        ob.keyframe_insert(data_path='hide_render',frame=96)
        if ob.animation_data:
            for curve in ob.animation_data.action.fcurves:
                for key in curve.keyframe_points:key.interpolation='CONSTANT'
    paddle=next(x for x in objects if x.name=='WORK | active paddle')
    for frame, angle in [(1,-.10),(25,.12),(49,-.09),(73,.10),(97,-.10)]:
        paddle.rotation_euler.z=angle
        paddle.keyframe_insert(data_path='rotation_euler',frame=frame)
    # Parent the actual modeling collections through a single pivot so directions
    # rotate the model, NOT the stationary Factorio camera or world illumination.
    pivot=bpy.data.objects.new('EXPORT | model rotation pivot',None)
    main_col.objects.link(pivot)
    for ob in list(main_col.objects)+list(tools_col.objects):
        if ob is pivot: continue
        mw=ob.matrix_world.copy()
        ob.parent=pivot
        ob.matrix_world=mw
    cam_data=bpy.data.cameras.new('Calibrated structure ortho 45 degrees')
    cam_data.type='ORTHO'
    cam_data.ortho_scale=3.30
    cam=bpy.data.objects.new('Factorio structure camera fixed',cam_data)
    lighting.objects.link(cam)
    cam.location=(0,-6,6+.14)
    cam.rotation_euler=(Vector((0,0,.14))-cam.location).to_track_quat('-Z','Y').to_euler()
    scene.camera=cam
    lamp('NW | broad warm key',(-3.5,-4,6.2),420,(1.0,.9,.74),5,lighting)
    lamp('SE | quiet fill',(3.3,2,4.2),210,(.70,.82,1.0),6,lighting)
    scene.frame_set(0)
    scene.render.filepath='//previews/'
    scene.camera=cam
    bpy.ops.wm.save_as_mainfile(filepath=str(out/'clay-pit-greybox-v1.blend'),check_existing=False)
    records=[]
    for state,frame in [('idle',0),('working',13)]:
        for direction,angle in enumerate((0,90,180,270)):
            pivot.rotation_euler.z=math.radians(angle)
            scene.frame_set(frame)
            bpy.context.view_layer.update()
            target=out/f'{state}-d{direction:02d}.png'
            scene.render.filepath=str(target)
            print('SOURCE_ALIGNED_RENDER',state,angle,flush=True)
            bpy.ops.render.render(write_still=True)
            records.append({'state':state,'angle':angle,'path':target.name,'sha256':hashlib.sha256(target.read_bytes()).hexdigest()})
    # Restore the canonical editable authoring state; no source graphics altered.
    pivot.rotation_euler.z=0
    scene.frame_set(0)
    report={'schema':1,'asset':'clay-pit','revision':'greybox-v1','actual_source_dimensions':[120,64],
       'active_crop_dimensions':[64,64],'reference_primary_pit_count':1,
       'source_unused_basin_variants':2,'blender_version':bpy.app.version_string,
       'camera_elevation_deg':45,'camera_azimuth_deg':0,'ortho_scale':3.30,
       'states':['idle','working'],'directions':[0,90,180,270],
       'model_meshes':len([o for o in scene.objects if o.type=='MESH']),
       'client_tested':False,'user_art_accepted':False,
       'source_primary':'tanks_for_bob_fork_1.8.95/graphics/entity/clay-pit.png',
       'source_working':'tanks_for_bob_fork_1.8.95/graphics/entity/clay-pit-w.png',
       'captures':records}
    (out/'build-report.json').write_text(json.dumps(report,indent=2)+'\n')
    print('CLAY_PIT_GREYBOX_CAPTURE_PASS',len(records),flush=True)


if __name__=='__main__':main()
