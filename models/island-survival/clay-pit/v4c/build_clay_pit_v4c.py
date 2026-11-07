#!/usr/bin/env python3
"""Clay Pit V4: preserve V3 meshes, darken wet clay, animate water bucket and lantern."""
import bpy, math, sys, hashlib, json, shutil
from pathlib import Path

def digest(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def main():
    import argparse
    ap=argparse.ArgumentParser()
    ap.add_argument('--out',required=True)
    ap.add_argument('--samples',type=int,default=20)
    opt=ap.parse_args(sys.argv[sys.argv.index('--')+1:])
    out=Path(opt.out).resolve()
    if out.exists() and any(out.iterdir()):
        raise ValueError('Output must be new/empty: preserve earlier revisions')
    out.mkdir(parents=True,exist_ok=True)
    scene=bpy.context.scene
    if not scene.camera or scene.camera.data.type!='ORTHO' or abs(scene.camera.data.ortho_scale-3.30)>.01:
        raise ValueError('Calibrated V3 45-degree structure camera required')
    root=bpy.data.objects.get('EXPORT | rotate all clay and tools, never camera')
    basin=next((o for o in scene.objects if 'one broad excavated clay bowl' in o.name),None)
    if not root or not basin or len(basin.data.materials)!=1:
        raise ValueError('V3 model and one continuous basin material required')
    m=basin.data.materials[0]
    if not m.name.startswith('V3 | single feathered clay field'):
        raise ValueError('Unrecognized saved V3 material; refusing unrelated changes')
    # The saved production V3 scene uses UNPOSITIONED color-ramp nodes.
    # Identify ramps by their exact authored control points, never editor XY.
    ramps=[n.color_ramp for n in m.node_tree.nodes if n.type=='VALTORGB']
    wetness=next((r for r in ramps if
                  len(r.elements)==5 and
                  any(abs(e.position-.23)<.01 for e in r.elements) and
                  any(abs(e.position-.43)<.01 for e in r.elements) and
                  any(abs(e.position-.59)<.01 for e in r.elements)),None)
    damp=next((r for r in ramps if len(r.elements)==3 and
               any(abs(e.position-.5)<.01 and abs(e.color[0]-.13)<.02
                   for e in r.elements)),None)
    if not damp or not wetness:
        raise ValueError('Saved V3 saturated-clay control ramps could not be verified')
    for pos,color in ((0,(.048,.021,.012,1)),(.5,(.092,.041,.023,1)),
                      (1,(.185,.095,.050,1))):
        el=min(damp.elements,key=lambda e:abs(e.position-pos))
        if abs(el.position-pos)>.02: raise ValueError('Unexpected V3 dark-mud palette')
        el.color=color
    for pos,value in ((.23,.96),(.43,.76),(.59,.27)):
        el=min(wetness.elements,key=lambda e:abs(e.position-pos))
        if abs(el.position-pos)>.02: raise ValueError('Unexpected V3 moisture gradient')
        el.color=(value,value,value,1)
    m.name='V4 | feathered banks and deeper wet clay'
    rope=bpy.data.objects.get('WORK | rope hanging down from hoist arm')
    bucket=[o for o in scene.objects if
        o.name.startswith('WORK | OPEN WOODEN WATER BUCKET') or
        o.name.startswith('WORK | bucket fiber hoop segment') or
        o.name.startswith('WORK | bucket handle tie') or
        o.name=='WORK | water visible below bucket rim']
    if not rope or len(bucket)<25:
        raise ValueError('Rope or wooden bucket components missing')
    rig=bpy.data.objects.new('ANIMATION | bucket and rope pendulum pivot',None)
    scene.collection.objects.link(rig)
    rig.location=(.04,-.17,.57)
    bpy.context.view_layer.update()
    world=rig.matrix_world.copy();rig.parent=root;rig.matrix_world=world
    bpy.context.view_layer.update()
    for ob in [rope]+bucket:
        world=ob.matrix_world.copy()
        ob.parent=rig
        ob.matrix_world=world
    frames=list(range(1,92,6))
    flicker=[.94,1.00,.965,1.07,.955,.99,1.055,.985,.915,1.015,1.06,.97,.93,1.01,1.045,.975]
    for i,frame in enumerate(frames+[97]):
        rig.rotation_euler.y=math.radians(-15.0*math.cos(2*math.pi*(i%16)/16))
        rig.keyframe_insert(data_path='rotation_euler',frame=frame)
    for curve in rig.animation_data.action.fcurves:
        for key in curve.keyframe_points:
            key.interpolation='BEZIER'
            key.handle_left_type='AUTO_CLAMPED'
            key.handle_right_type='AUTO_CLAMPED'
    paper=bpy.data.materials['LANTERN | pale wax-paper panels']
    core=bpy.data.materials['LANTERN | warm inner illumination']
    paper_node=paper.node_tree.nodes.get('Principled BSDF')
    core_node=core.node_tree.nodes.get('Principled BSDF')
    ps=paper_node.inputs.get('Emission Strength')
    pc=paper_node.inputs.get('Emission Color')
    cs=core_node.inputs.get('Emission Strength')
    if ps is None or pc is None or cs is None:
        raise RuntimeError('Blender candle emission channels missing')
    pc.default_value=(1.0,.58,.25,1)
    lamp_data=bpy.data.lights.new('V4 | wax paper candle','POINT')
    lamp_data.color=(1.0,.61,.28)
    lamp_data.shadow_soft_size=.13
    lamp=bpy.data.objects.new('WORK | softly flickering lantern light',lamp_data)
    scene.collection.objects.link(lamp)
    lamp.location=(.19,.24,.886)
    bpy.context.view_layer.update()
    world=lamp.matrix_world.copy();lamp.parent=root;lamp.matrix_world=world
    for i,frame in enumerate(frames+[97]):
        level=flicker[i%16]
        lamp_data.energy=2.4*level
        lamp_data.keyframe_insert(data_path='energy',frame=frame)
        ps.default_value=.16*level
        ps.keyframe_insert(data_path='default_value',frame=frame)
        cs.default_value=.78*level
        cs.keyframe_insert(data_path='default_value',frame=frame)
    lamp.hide_render=True;lamp.keyframe_insert(data_path='hide_render',frame=0)
    lamp.hide_render=False;lamp.keyframe_insert(data_path='hide_render',frame=1)
    lamp.keyframe_insert(data_path='hide_render',frame=97)
    scene.render.engine='CYCLES'
    scene.cycles.samples=opt.samples
    scene.cycles.device='CPU'
    scene.render.resolution_x=scene.render.resolution_y=256
    scene.render.resolution_percentage=100
    scene.render.image_settings.file_format='PNG'
    scene.render.image_settings.color_mode='RGBA'
    scene.render.film_transparent=True
    scene.render.fps=8
    root.rotation_euler.z=0
    scene.frame_set(0)
    bpy.context.view_layer.update()
    bpy.ops.wm.save_as_mainfile(filepath=str(out/'clay-pit-v4c.blend'),check_existing=False)
    records=[]
    for state,samples in (('idle',[0]),('working',frames)):
        for d,angle in enumerate((0,90,180,270)):
            root.rotation_euler.z=math.radians(angle)
            for i,frame in enumerate(samples):
                scene.frame_set(frame)
                bpy.context.view_layer.update()
                name=(f'idle-d{d:02d}.png' if state=='idle'
                      else f'working-d{d:02d}-f{i:03d}.png')
                path=out/name
                scene.render.filepath=str(path)
                print('V4_CAPTURE',state,angle,frame,flush=True)
                bpy.ops.render.render(write_still=True)
                if state=='working' and i==2:
                    shutil.copyfile(path,out/f'working-d{d:02d}.png')
                records.append({'state':state,'angle':angle,'index':i,
                                'frame':frame,'path':name,'sha256':digest(path)})
    root.rotation_euler.z=0;scene.frame_set(0)
    report={'schema':4,'revision':'v4c-readable-bucket-swing',
            'camera_pitch_deg':45,'ortho_scale':3.30,'frames':frames,
            'directions':[0,90,180,270],'fps':8,'swing_degrees':[-15,15],
            'flicker':flicker,'actual_frame_count':len(records),
            'blender':bpy.app.version_string,'visual_accepted':False,
            'factorio_client_tested':False,'captures':records}
    (out/'build-report.json').write_text(json.dumps(report,indent=2)+'\n')
    print('V4C_NATIVE_CAPTURE_COMPLETE',len(records),flush=True)

if __name__=='__main__':main()
