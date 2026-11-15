"""Finish the owner-accepted V3: repair one degenerate vertex and capture motion."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import sys

import bpy
import bmesh

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,data):p.write_text(json.dumps(data,indent=2)+'\n')

def main():
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--fmpl-tools',type=Path,required=True)
    args=p.parse_args(sys.argv[sys.argv.index('--')+1:]);source=args.source.resolve();out=args.out.resolve()
    if out.exists():raise FileExistsError(out)
    out.mkdir(parents=True);sys.path.insert(0,str(args.fmpl_tools.resolve()))
    from blender_camera_guard import install_canonical_camera,assert_clean,camera_record
    bpy.ops.wm.open_mainfile(filepath=str(source))
    scene=bpy.context.scene;scene.frame_set(1)
    body=bpy.data.objects['V3 PRESSURE | hollow cast pump barrel']
    body.data.calc_loop_triangles()
    bad=[t for t in body.data.loop_triangles if t.area<1e-12]
    assert len(bad)==1,'Expected the measured single collinear floor vertex'
    indices=list(bad[0].vertices)
    # Remove only the middle point on an exactly straight floor edge.
    candidate=None
    for i in indices:
        others=[j for j in indices if j!=i]
        a,b=[body.data.vertices[j].co for j in others];v=body.data.vertices[i].co
        edge=b-a;t=(v-a).dot(edge)/edge.length_squared
        if 0<t<1 and (v-(a+t*edge)).length<1e-8:candidate=i
    assert candidate is not None
    bm=bmesh.new();bm.from_mesh(body.data);bm.verts.ensure_lookup_table()
    bmesh.ops.dissolve_verts(bm,verts=[bm.verts[candidate]],use_face_split=False,use_boundary_tear=False)
    bm.to_mesh(body.data);bm.free();body.data.update();body.data.calc_loop_triangles()
    assert not any(t.area<1e-12 for t in body.data.loop_triangles)
    lever=bpy.data.objects['V3 RELIEF | mounted weighted lever']
    stem=bpy.data.objects['V3 RELIEF | pressure stem']
    stem_z=stem.location.z
    for frame in range(1,98):
        phase=(frame-1)*math.tau/96
        lever.rotation_euler.y=.035*math.sin(phase)
        stem.location.z=stem_z+.003*math.sin(phase)
        lever.keyframe_insert(data_path='rotation_euler',frame=frame)
        stem.keyframe_insert(data_path='location',frame=frame)
    for obj in (lever,stem):
        for layer in obj.animation_data.action.layers:
            for strip in layer.strips:
                for bag in strip.channelbags:
                    for curve in bag.fcurves:
                        for point in curve.keyframe_points:point.interpolation='LINEAR'
    profile=json.loads((source.parent/'capture-profile.json').read_text())
    profile['source_size']=256
    profile['states']={'idle':[0],'working':list(range(1,92,6))}
    install_canonical_camera(scene,profile,bpy)
    scene.cycles.samples=48
    scene.cycles.use_denoising=False
    scene.frame_set(1)
    root=bpy.data.objects['EXPORT | rotate primitive steam-powered pump, never camera']
    root.rotation_euler=(0,0,0)
    assert_clean(scene,profile,bpy)
    write(out/'capture-profile.json',profile)
    write(out/'owner-disposition.json',{'date':'2026-11-15','accepted_design_source_sha256':sha(source),
        'instruction':'Cool great done let\'s move on, Small animation a couple of bits twiddle and move integrate and away we go we have so much to do',
        'scope':'Keep the displayed V3 design; add restrained movement, repair the export defect and integrate. Stop further cosmetic redesign.',
        'changes':['Dissolved the single exactly collinear floor vertex','Small relief-lever and stem movement; existing piston/flywheel/gauge loop retained'],
        'camera':camera_record(scene),'gameplay_fields_changed':False})
    native=out/'pipe-pump-v3.blend'
    bpy.ops.wm.save_as_mainfile(filepath=str(native),compress=True)
    bpy.ops.wm.open_mainfile(filepath=str(native))
    scene=bpy.context.scene
    root=bpy.data.objects['EXPORT | rotate primitive steam-powered pump, never camera']
    assert_clean(scene,profile,bpy)
    bpy.ops.object.select_all(action='DESELECT')
    for obj in [root,*list(root.children_recursive)]:obj.select_set(True)
    runtime=out/'pipe-pump-v3.glb'
    bpy.ops.export_scene.gltf(filepath=str(runtime),export_format='GLB',use_selection=True,export_cameras=False,export_lights=False,
        export_animations=True,export_animation_mode='SCENE',export_frame_range=True,export_force_sampling=True,
        export_frame_step=1,export_apply=True,export_extras=True)
    # Factorio's ground tile grid is square on screen. Unforeshorten only the
    # stationary camera's ground-depth axis in this derived sprite capture.
    # The editable source and GLB were saved/exported at exact unit scale above.
    projection=bpy.data.objects.new('SPRITE ONLY | square ground-grid projection',None)
    scene.collection.objects.link(projection)
    projection.scale.y=math.sqrt(2)
    root.parent=projection
    images=[]
    for facing,yaw in [('north',0),('east',270),('south',180),('west',90)]:
        root.rotation_euler.z=math.radians(yaw)
        for state,frames in profile['states'].items():
            for index,frame in enumerate(frames):
                scene.frame_set(frame);assert_clean(scene,profile,bpy)
                path=out/(f'{facing}-{state}-{index:02d}.png')
                scene.render.filepath=str(path);bpy.ops.render.render(write_still=True)
                images.append({'file':path.name,'facing':facing,'yaw':yaw,'state':state,'index':index,'source_frame':frame,'sha256':sha(path)})
    write(out/'capture-manifest.json',{'schema':'tanks.pipe-pump.v3.production-capture','source_sha256':sha(native),'runtime_sha256':sha(runtime),
        'blender':bpy.app.version_string,'genuine_blender_frames':len(images),'frame_size':[256,256],'fps':8,'images':images,
        'owner_design_approved':True,'native_game_verified':False,
        'native_projection':{'global_ground_y_scale':math.sqrt(2),'runtime_geometry_changed':False,
                             'purpose':'Match Factorio square ground tiles under the fixed 45-degree camera'}})
    print('PIPE_PUMP_V3_FULL_CAPTURE',len(images),flush=True)

if __name__=='__main__':main()
