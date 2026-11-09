"""Cooking Fire V2: full-size fluid mount and two reference-derived bellows.

Run with Blender and the committed Cooking Fire V1 source. This adds visible
mechanical components and a separate pipe-fit reference collection only.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import struct
import sys

import bpy
import bmesh
from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bellows_components as bellows

SOURCE_SHA256='edf8e055e4f1e8ee1a94e7a7bc0028ef51aab9b7c83fae22a382a59a579957b8'
SOURCE_COMMIT='d9e12ce02fa55c5239be12b5f38e6ac14b87dddc'
SOURCE_PATH='models/island-survival/cooking-fire/v1/cooking-fire-v1.blend'
PIPE_REFERENCE_COMMIT='0ea7ed22d508fb2f5c7d71102679b0be80a379ab'
DIRECTIONS=(('north',0),('east',-90),('south',180),('west',90))
REPLACED=('Cooking Fire | rear steam feed','Cooking Fire | open north steam socket',
          'Cooking Fire | steam collar','SOCKET | steam input | north boundary')


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def fingerprint(obj):
    record={'type':obj.type,'matrix_basis':[list(row) for row in obj.matrix_basis],
            'parent':obj.parent.name if obj.parent else None}
    if obj.type=='MESH':
        h=hashlib.sha256()
        for v in obj.data.vertices:
            h.update(struct.pack('<3f',*v.co))
        for p in obj.data.polygons:
            h.update(struct.pack('<I',len(p.vertices)))
            h.update(struct.pack('<'+'I'*len(p.vertices),*p.vertices))
            h.update(struct.pack('<I',p.material_index))
        record['geometry']=h.hexdigest()
    elif obj.type=='CURVE':
        record['geometry']=[{'type':s.type,'bezier':[[*p.co,*p.handle_left,*p.handle_right] for p in s.bezier_points],'points':[list(p.co) for p in s.points]} for s in obj.data.splines]
    if hasattr(obj.data,'materials'):
        record['materials']=[m.name if m else None for m in obj.data.materials]
    return hashlib.sha256(json.dumps(record,sort_keys=True).encode()).hexdigest()


def mesh(name,verts,faces,collection,pivot,material):
    data=bpy.data.meshes.new(name)
    data.from_pydata(verts,[],faces)
    data.update()
    bm=bmesh.new();bm.from_mesh(data)
    bmesh.ops.recalc_face_normals(bm,faces=bm.faces)
    bm.to_mesh(data);bm.free()
    obj=bpy.data.objects.new(name,data)
    collection.objects.link(obj)
    obj.parent=pivot
    data.materials.append(material)
    return obj


def box(name,center,size,collection,pivot,material,bevel=.025):
    x,y,z=center; sx,sy,sz=[v/2 for v in size]
    verts=[(x+dx*sx,y+dy*sy,z+dz*sz) for dz in (-1,1) for dy in (-1,1) for dx in (-1,1)]
    faces=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]
    obj=mesh(name,verts,faces,collection,pivot,material)
    if bevel:
        mod=obj.modifiers.new('Soft cast or worn edges','BEVEL');mod.width=bevel;mod.segments=3
        norm=obj.modifiers.new('Weighted face normals','WEIGHTED_NORMAL');norm.keep_sharp=True
    return obj


def ring(name,center,normal,outer,inner,depth,collection,pivot,material):
    # Exact barrel/collar geometry from the boiler V05 reference constructor.
    p=Vector(center); n=Vector(normal).normalized(); q=n.to_track_quat('Z','Y')
    count=64;verts=[];faces=[]
    for z,r in [(-depth/2,outer),(depth/2,outer),(-depth/2,inner),(depth/2,inner)]:
        verts += [p+q@Vector((r*math.cos(i*math.tau/count),r*math.sin(i*math.tau/count),z)) for i in range(count)]
    for i in range(count):
        j=(i+1)%count
        faces += [(i,j,count+j,count+i),(count+i,count+j,3*count+j,3*count+i),
                  (2*count+j,2*count+i,3*count+i,3*count+j),(j,i,2*count+i,2*count+j)]
    obj=mesh(name,verts,faces,collection,pivot,material)
    for poly in obj.data.polygons:
        poly.use_smooth=abs(poly.normal.dot(n))<.5
    bevel=obj.modifiers.new('Rolled pipe edge','BEVEL');bevel.width=.003;bevel.segments=3
    return obj


def pipe_curve(name,points,radius,collection,pivot,material):
    return bellows._tube(name,points,radius,collection,pivot,material)


def stone_height(scene,x,y):
    heights=[]
    for obj in scene.objects:
        if obj.type!='MESH' or not obj.name.startswith('stone_'):
            continue
        inv=obj.matrix_world.inverted()
        ok,loc,_,_=obj.ray_cast(inv@Vector((x,y,3)),(inv.to_3x3()@Vector((0,0,-1))).normalized())
        if ok:
            heights.append((obj.matrix_world@loc).z)
    return max(heights) if heights else .02


def set_camera(scene,target,scale,resolution=512):
    target=Vector(target)
    scene.camera.location=target+Vector((0,-1,1)).normalized()*6
    scene.camera.rotation_euler=(target-scene.camera.location).to_track_quat('-Z','Y').to_euler()
    scene.camera.data.ortho_scale=scale
    scene.render.resolution_x=scene.render.resolution_y=resolution


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--source-blend',type=Path,required=True)
    parser.add_argument('--output-dir',type=Path,required=True)
    parser.add_argument('--render',choices=('none','pilot','proof'),default='proof')
    args=parser.parse_args(sys.argv[sys.argv.index('--')+1:])
    if digest(args.source_blend)!=SOURCE_SHA256:
        raise ValueError('Expected the committed Cooking Fire V1 native source')
    out=args.output_dir.resolve();out.mkdir(parents=True,exist_ok=True)
    bpy.ops.wm.open_mainfile(filepath=str(args.source_blend.resolve()))
    scene=bpy.data.scenes['RENDER'];bpy.context.window.scene=scene
    pivot=bpy.data.objects['EXPORT | direction pivot'];pivot.rotation_euler.z=0
    scene.frame_set(0);bpy.context.view_layer.update()
    protected={o.name:fingerprint(o) for o in scene.objects if o.type in {'MESH','CURVE'} and o.name not in REPLACED}
    old_actions={a.name for a in bpy.data.actions}
    for name in REPLACED:
        obj=bpy.data.objects.get(name)
        if obj:bpy.data.objects.remove(obj,do_unlink=True)
    collection=bpy.data.collections.new('06 | Pump box and bellows')
    scene.collection.children.link(collection)
    bpy.data.scenes['MODEL'].collection.children.link(collection)
    reference=bpy.data.collections.new('REFERENCE ONLY | adjacent standard pipe')
    scene.collection.children.link(reference)
    reference['Purpose']='Separate assembly jig; exclude from production sprites'
    m=bellows.materials()
    iron=bpy.data.materials['Cooking Fire | hammered cast iron']
    soot=bpy.data.materials['Cooking Fire | soot-dark iron']
    # A full-size rear mounting box with a real, visible open mouth.
    body=box('Pump box | cast housing',(0,1.14,.40),(.92,.48,.76),collection,pivot,iron,.045)
    bpy.ops.mesh.primitive_cylinder_add(vertices=96,radius=.245,depth=.40,location=(0,1.40,.36),rotation=(math.pi/2,0,0))
    cutter=bpy.context.object
    cutter.name='Temporary bore cutter'
    modifier=body.modifiers.new('Open rear bore','BOOLEAN');modifier.operation='DIFFERENCE';modifier.solver='EXACT';modifier.object=cutter
    bpy.context.view_layer.objects.active=body
    # Apply only the new housing's boolean; source geometry is never selected.
    bpy.ops.object.modifier_apply(modifier=modifier.name)
    bpy.data.objects.remove(cutter,do_unlink=True)
    box('Pump box | upper seating lip',(0,1.14,.775),(.96,.51,.05),collection,pivot,soot,.02)
    ring('Pump box | full-size throat',(0,1.355,.36),(0,1,0),.285,.245,.29,collection,pivot,iron)
    mouth=ring('Pump box | standard mounting collar',(0,1.4625,.36),(0,1,0),.34,.245,.075,collection,pivot,iron)
    pipe_curve('Pump box | reduced feed to cooking pot',[(0,.895,.60),(0,.79,.65),(0,.72,1.15),(0,.60,1.245),(0,.52,1.25)],.067,collection,pivot,soot)
    ring('Pump box | pot feed seating collar',(0,.575,1.245),(0,1,0),.090,.058,.040,collection,pivot,iron)
    marker=bpy.data.objects.new('SOCKET | steam input | north plane',None)
    collection.objects.link(marker);marker.parent=pivot;marker.location=(0,1.5,.36)
    marker.empty_display_type='ARROWS';marker.empty_display_size=.18
    marker['Factorio pipe cell']=[0,-1];marker['Adjacent pipe center']=[0,-2]
    marker['Blender outward normal']=[0,1,0];marker['Barrel diameter']=.57
    marker['Collar diameter']=.68;marker['Bore diameter']=.49
    marker['Interface authority']='Boiler V05/V07 and condenser standard; 1 Blender unit per tile'
    squeeze=bellows.build_squeeze_bellows(collection,pivot,location=(0,1.12,.80),radius=.25,height=.38,animate=True)
    hand=bellows.build_hand_bellows(collection,pivot,location=(1.02,-.16,.34),yaw=-math.pi/2,scale=.67,animate=True)
    # Support the fixed lower board without obstructing its moving upper paddle.
    support_records=[]
    for label,x in [('front',1.02-.27*.67),('rear',1.02+.23*.67)]:
        y=-.16;bottom=stone_height(scene,x,y)-.002;top=.34
        box('Hand bellows | '+label+' timber support',(x,y,(bottom+top)/2),(.075,.21,top-bottom),collection,pivot,m['wood'],.008)
        support_records.append({'name':label,'position':[x,y],'bottom':bottom,'top':top})
    # The reference pipe duplicates the boiler's one-tile barrel and two collars.
    ring('REFERENCE | one-tile pipe barrel',(0,2,.36),(0,1,0),.285,.245,1.0,reference,pivot,iron)
    mate=ring('REFERENCE | near pipe collar',(0,1.5375,.36),(0,1,0),.34,.245,.075,reference,pivot,iron)
    ring('REFERENCE | far pipe collar',(0,2.4625,.36),(0,1,0),.34,.245,.075,reference,pivot,iron)
    reference.hide_render=True
    scene.frame_start=0;scene.frame_end=96;scene.render.fps=8
    scene.render.film_transparent=True
    scene.render.resolution_percentage=100
    scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.image_settings.color_depth='8'
    scene.cycles.device='CPU';scene.cycles.samples=40;scene.cycles.use_denoising=True
    scene.cycles.seed=5855;scene.cycles.use_animated_seed=False
    scene.render.threads_mode='FIXED';scene.render.threads=4
    set_camera(scene,(0,0,.70),3.35)
    scene['Cooking Fire status']='V2 pump-box and bellows model candidate; not installed as game sprites'
    scene['Cooking Fire pipe standard']='0.57 barrel / 0.68 collar / 0.49 bore / 0.36 centerline, one unit per tile'
    scene['Cooking Fire directions']='Blender +Y is north; N0,E-90,S180,W90'
    scene.frame_set(0);pivot.rotation_euler.z=0;bpy.context.view_layer.update()
    assert all(fingerprint(bpy.data.objects[n])==h for n,h in protected.items()),'Retained V1 geometry changed'
    assert old_actions <= {a.name for a in bpy.data.actions},'Inherited animation action missing'
    # Compare the actual two open annular faces, not just object origins.
    source_face=[v.co.copy() for v in mouth.data.vertices if abs(v.co.y-1.5)<1e-6]
    mate_face=[v.co.copy() for v in mate.data.vertices if abs(v.co.y-1.5)<1e-6]
    assert len(source_face)==len(mate_face)==128
    residual=max(min((a-b).length for b in mate_face) for a in source_face)
    assert residual<1e-6
    interface_views=[]
    expected={'north':(0,1.5,.36),'east':(1.5,0,.36),'south':(0,-1.5,.36),'west':(-1.5,0,.36)}
    for name,angle in DIRECTIONS:
        pivot.rotation_euler.z=math.radians(angle);bpy.context.view_layer.update()
        point=marker.matrix_world.translation.copy()
        assert (point-Vector(expected[name])).length<1e-6
        interface_views.append({'direction':name,'yaw':angle,'model_plane':list(point),'native_adjacent_pipe_center':{'north':[0,-2],'east':[2,0],'south':[0,2],'west':[-2,0]}[name]})
    pivot.rotation_euler.z=0;scene.frame_set(0);bpy.context.view_layer.update()
    poses=[]
    for frame in (0,1,25,49,73,97):
        scene.frame_set(frame);bpy.context.view_layer.update()
        poses.append({'frame':frame,'hand_compression':float(hand['root']['compression']),'accordion_compression':float(squeeze['root']['compression']),'upper_board_angle_degrees':math.degrees(hand['top_rig'].rotation_euler.x),'accordion_cap_z':squeeze['top_cap'].matrix_world.translation.z})
    scene.frame_set(0);pivot.rotation_euler.z=0;bpy.context.view_layer.update()
    for image in bpy.data.images:
        if image.source=='FILE' and not image.packed_file:raise ValueError('Unpacked texture: '+image.name)
    native=out/'cooking-fire-v2.blend'
    bpy.ops.wm.save_as_mainfile(filepath=str(native),check_existing=False,compress=True)
    bpy.ops.wm.open_mainfile(filepath=str(native))
    scene=bpy.data.scenes['RENDER'];bpy.context.window.scene=scene
    scene.frame_set(0);bpy.context.view_layer.update()
    assert all(fingerprint(bpy.data.objects[n])==h for n,h in protected.items()),'Retained geometry changed after reopen'
    pivot=bpy.data.objects['EXPORT | direction pivot']
    reference=bpy.data.collections['REFERENCE ONLY | adjacent standard pipe']
    report={'asset':'Cooking Fire V2','status':'model candidate','source_commit':SOURCE_COMMIT,'source_path':SOURCE_PATH,'source_sha256':SOURCE_SHA256,'native_sha256':digest(native),'blender':bpy.app.version_string,'preserved_v1_objects':len(protected),'preserved_v1_geometry':protected,'replaced_v1_objects':list(REPLACED),'inherited_animation_actions':sorted(old_actions),'native_reopen':'passed','supports':support_records,'bellows_poses':poses,'pipe_interface':{'reference_repo_commit':PIPE_REFERENCE_COMMIT,'reference_source':'art/source-to-3d/boiler-v05/build_boiler_v05.py','units_per_tile':1,'barrel_od':.57,'collar_od':.68,'bore_id':.49,'collar_depth':.075,'center_height':.36,'machine_plane':[0,1.5,.36],'adjacent_barrel_span_y':[1.5,2.5],'matched_vertices':len(source_face),'max_mating_error':residual,'directions':interface_views,'native_cooking_fire_registration':'not yet performed; model fit only'},'camera':{'elevation_deg':45,'asset_scale':3.35,'asset_target':[0,0,.70]},'game_integration':False,'captures':[]}
    record=out/'build-report.json';record.write_text(json.dumps(report,indent=2)+'\n')
    if args.render=='none':return
    tasks=[('hero',25,225,False,'asset')]
    if args.render=='proof':
        tasks += [('working-'+name,25,angle,False,'asset') for name,angle in DIRECTIONS]
        tasks += [('idle-'+name,0,angle,False,'asset') for name,angle in DIRECTIONS]
        tasks += [('pipe-fit-'+name,25,angle,True,'pipe') for name,angle in DIRECTIONS]
        tasks += [('bellows-open',1,225,False,'asset'),('bellows-compressed',49,225,False,'asset')]
        tasks += [(f'loop-{i:02d}',frame,225,False,'asset') for i,frame in enumerate(range(1,97,6))]
    for name,frame,angle,show_pipe,camera_mode in tasks:
        pivot.rotation_euler.z=math.radians(angle);scene.frame_set(frame)
        reference.hide_render=not show_pipe
        set_camera(scene,(0,0,.70),5.35 if show_pipe else 3.35)
        bpy.context.view_layer.update()
        path=out/'renders'/(name+'.png');path.parent.mkdir(exist_ok=True)
        scene.render.filepath=str(path)
        print('COOKING_FIRE_V2_CAPTURE',name,frame,angle,flush=True)
        bpy.ops.render.render(write_still=True)
        report['captures'].append({'name':name,'frame':frame,'yaw':angle,'reference_pipe_visible':show_pipe,'path':str(path.relative_to(out)),'sha256':digest(path)})
        record.write_text(json.dumps(report,indent=2)+'\n')


if __name__=='__main__':main()
