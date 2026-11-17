"""Finish the existing Tanks condenser for operational delivery; no redesign."""
import argparse, hashlib, importlib.util, json, math, shutil, sys
from pathlib import Path
import bpy
import numpy as np

ROOT=Path(__file__).resolve().parents[4]
STEM='steam-condenser-v1'
ROOT_NAME='EXPORT | rotate Tanks Steam Condenser, never camera'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d): p.write_text(json.dumps(d,indent=2)+'\n')
def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    result=importlib.util.module_from_spec(spec);spec.loader.exec_module(result);return result
def main():
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);out=a.out.resolve()
    if out.exists(): raise FileExistsError(out)
    out.mkdir(parents=True)
    helper=module('pond_surface_tools',ROOT/'models/island-survival/fish-pond/v2/build_candidate.py')
    inspect=module('pond_geometry_tools',ROOT/'models/island-survival/fish-pond/v2/inspect_export.py')
    sys.path.insert(0,str(ROOT/'build/fmpl-pin'))
    from blender_camera_guard import install_canonical_camera,assert_clean
    bpy.ops.wm.open_mainfile(filepath=str(a.source.resolve()))
    scene=bpy.context.scene;scene.frame_set(1);root=bpy.data.objects[ROOT_NAME]
    for obj in list(root.children_recursive):
        if obj.type=='CURVE':
            bpy.ops.object.select_all(action='DESELECT');obj.select_set(True);bpy.context.view_layer.objects.active=obj
            bpy.ops.object.convert(target='MESH')
    for obj in root.children_recursive:
        for curve in helper.curves(obj):
            for key in curve.keyframe_points: key.interpolation='LINEAR'
        if obj.name.startswith(('STEAM |','MOISTURE |')):
            obj['fmpl_visibility_group']='working-effects'
            for frame,hidden in [(0,True),(1,False),(97,False)]:
                obj.hide_render=hidden;obj.keyframe_insert(data_path='hide_render',frame=frame)
    scene.frame_set(1);scene.render.fps=48;scene.frame_start=1;scene.frame_end=97
    opaque=[]
    for obj in root.children_recursive:
        if obj.type!='MESH': continue
        shaders=[m.node_tree.nodes.get('Principled BSDF') for m in obj.data.materials if m and m.use_nodes]
        translucent=any(s and (s.inputs['Transmission Weight'].default_value>0) for s in shaders)
        if obj.name.startswith('STEAM |'):
            for mat in obj.data.materials:
                s=mat.node_tree.nodes.get('Principled BSDF');s.inputs['Alpha'].default_value=.22
                mat.surface_render_method='DITHERED'
            translucent=True
        if not translucent: opaque.append(obj)
        elif not obj.data.uv_layers: obj.data.uv_layers.new(name='Uniform optical surface')
    helper.bake(scene,opaque,out,1024)
    bpy.data.orphans_purge(do_recursive=True)
    profile={'camera_policy':'fmpl.factorio45.v1','capture_kind':'entity','orientation_policy':'rotatable',
      'directions':[0,90,180,270],'states':{'idle':[0],'working':list(range(1,92,6))},'source_size':256,
      'camera_override':{'type':'ORTHO','elevation_deg':45,'azimuth_deg':0,'distance':math.sqrt(72),'ortho_scale':5.2,'target':[0,0,.93]}}
    install_canonical_camera(scene,profile,bpy);scene.cycles.samples=16;scene.cycles.use_denoising=False
    scene.frame_set(1);assert_clean(scene,profile,bpy)
    native=out/(STEM+'.blend');runtime=out/(STEM+'.glb')
    bpy.ops.wm.save_as_mainfile(filepath=str(native),compress=True)
    expected={}
    for frame in (1,25,49,73,97):
        scene.frame_set(frame);bpy.context.view_layer.update()
        expected[frame]={'geometry':inspect.summary(inspect.geometry()),'rotor':[list(r) for r in bpy.data.objects['COOLING | rotating vane drive'].matrix_world]}
    assert not expected[1]['geometry']['degenerate_objects'],expected[1]
    scene.frame_set(1);bpy.ops.object.select_all(action='DESELECT')
    for obj in [root,*list(root.children_recursive)]: obj.select_set(True)
    bpy.ops.export_scene.gltf(filepath=str(runtime),export_format='GLB',use_selection=True,
        export_cameras=False,export_lights=False,export_animations=True,export_animation_mode='SCENE',
        export_anim_scene_split_object=False,export_frame_range=True,export_force_sampling=True,export_apply=False)
    bpy.ops.wm.read_factory_settings(use_empty=True);bpy.context.scene.render.fps=48
    bpy.ops.import_scene.gltf(filepath=str(runtime));scene=bpy.context.scene
    errors=[]
    for frame,reference in expected.items():
        scene.frame_set(frame);bpy.context.view_layer.update();actual=inspect.summary(inspect.geometry())
        assert actual['finite'] and not actual['degenerate_objects'] and not actual['missing_uv'],actual
        errors.append(max(abs(x-y) for key in ('min','max') for x,y in zip(actual[key],reference['geometry'][key])))
        matrix=bpy.data.objects['COOLING | rotating vane drive'].matrix_world
        errors.append(max(abs(matrix[i][j]-reference['rotor'][i][j]) for i in range(4) for j in range(4)))
    assert max(errors)<1e-5,errors
    verification={'technical_checks_passed':True,'source_sha256':sha(native),'glb_sha256':sha(runtime),
      'sampled_source_frames':list(expected),'source_geometry':expected[1]['geometry'],
      'max_roundtrip_error_tiles':max(errors),'gameplay_changed':False,'owner_visual_approved':False,
      'review_policy':'Owner authorized operational close-enough completion; cosmetic polish deferred.'}
    write(out/'runtime-inspection.json',verification);write(out/'capture-profile.json',profile)
    bpy.ops.wm.open_mainfile(filepath=str(native));scene=bpy.context.scene;root=bpy.data.objects[ROOT_NAME]
    projection=bpy.data.objects.new('SPRITE ONLY | square ground-grid projection',None);scene.collection.objects.link(projection)
    projection.scale.y=math.sqrt(2);root.parent=projection
    images=[]
    for facing,yaw in [('north',0),('east',270),('south',180),('west',90)]:
        root.rotation_euler.z=math.radians(yaw)
        for state,frames in profile['states'].items():
            for index,frame in enumerate(frames):
                scene.frame_set(frame);assert_clean(scene,profile,bpy);path=out/f'{facing}-{state}-{index:02d}.png'
                scene.render.filepath=str(path);bpy.ops.render.render(write_still=True)
                images.append({'file':path.name,'facing':facing,'state':state,'index':index,'source_frame':frame,'sha256':sha(path)})
    write(out/'capture-manifest.json',{'source_sha256':sha(native),'runtime_sha256':sha(runtime),
      'genuine_blender_frames':len(images),'fps':8,'images':images,'native_projection':{'global_ground_y_scale':math.sqrt(2),'runtime_geometry_changed':False}})
    print('TANKS_CONDENSER_OPERATIONAL_SOURCE_AND_CAPTURE',len(images),flush=True)
if __name__=='__main__':main()
