"""Refine the actual two-port pipe pump; preserve native ports and V1 master."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import sys

import bpy
from mathutils import Vector

EXPECTED_SOURCE='1c6e1b23d0ec1472d1c25303416b97b827735298f9a34724beecc7e085d9cd6c'
RADIUS=.103
ROD_LENGTH=.60

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def record(path,data):Path(path).write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')

def children(root):
    return [root,*list(root.children_recursive)]

def cylinder(name,pos,radius,depth,mat,collection,parent,axis_x=True):
    bpy.ops.mesh.primitive_cylinder_add(vertices=48,radius=radius,depth=depth)
    obj=bpy.context.object
    obj.name=name
    for c in tuple(obj.users_collection):c.objects.unlink(obj)
    collection.objects.link(obj)
    obj.parent=parent
    obj.location=pos
    if axis_x:obj.rotation_euler.y=math.pi/2
    obj.data.materials.append(mat)
    for face in obj.data.polygons:face.use_smooth=len(face.vertices)==4
    return obj

def pipe_mesh(name,points,mat,collection,parent):
    # Cubic Hermite sections produce smooth physical elbows, with the original
    # fixed interface planes and full bore. The actual exported artifact includes
    # both inner and outer walls and end annuli, not an unexported Curve.
    control=[Vector(p) for p in points]
    centers=[]
    for i in range(len(control)-1):
        a,b=control[i],control[i+1]
        before=control[i-1] if i else a-(b-a)
        after=control[i+2] if i+2<len(control) else b+(b-a)
        ma=(b-before)*.5
        mb=(after-a)*.5
        for j in range(12):
            t=j/12
            centers.append((2*t**3-3*t*t+1)*a+(t**3-2*t*t+t)*ma+(-2*t**3+3*t*t)*b+(t**3-t*t)*mb)
    centers.append(control[-1])
    verts=[]
    n=48
    lengths=[0.]
    for i in range(1,len(centers)):lengths.append(lengths[-1]+(centers[i]-centers[i-1]).length)
    for radius in (.285,.245):
        for i,center in enumerate(centers):
            tangent=(centers[min(i+1,len(centers)-1)]-centers[max(0,i-1)]).normalized()
            axis_x=Vector((1,0,0))
            side=tangent.cross(axis_x).normalized()
            for k in range(n):
                a=k*math.tau/n
                verts.append(tuple(center+radius*(math.cos(a)*axis_x+math.sin(a)*side)))
    rings=len(centers)
    off=n*rings
    faces=[]
    for layer,offset in enumerate((0,off)):
        for i in range(rings-1):
            for k in range(n):
                j=(k+1)%n
                face=(offset+i*n+k,offset+i*n+j,offset+(i+1)*n+j,offset+(i+1)*n+k)
                faces.append(face if layer==0 else tuple(reversed(face)))
    for end in (0,rings-1):
        for k in range(n):
            j=(k+1)%n
            faces.append((end*n+k,end*n+j,off+end*n+j,off+end*n+k))
    mesh=bpy.data.meshes.new(name)
    mesh.from_pydata(verts,[],faces)
    mesh.update()
    uv=mesh.uv_layers.new(name='Physical pipe length and circumference')
    for face in mesh.polygons:
        for idx in face.loop_indices:
            vi=mesh.loops[idx].vertex_index%off
            ring,k=divmod(vi,n)
            uv.data[idx].uv=(k/n,lengths[ring]/max(lengths[-1],1e-6))
        face.use_smooth=True
    obj=bpy.data.objects.new(name,mesh)
    collection.objects.link(obj)
    obj.parent=parent
    mesh.materials.append(mat)
    return obj

def linear_keys(obj):
    action=obj.animation_data.action if obj.animation_data else None
    if not action:return
    for layer in action.layers:
        for strip in layer.strips:
            for bag in strip.channelbags:
                for curve in bag.fcurves:
                    for point in curve.keyframe_points:point.interpolation='LINEAR'

def inspect(scene,model,out):
    wheel=bpy.data.objects['MOTION | keyed lateral 3D drive flywheel']
    piston=bpy.data.objects['MOTION | vertically reciprocating piston']
    link=bpy.data.objects['MOTION | hinged connecting rod']
    pin=bpy.data.objects['MOTION | crank eccentric pin']
    ports=[o for o in children(model) if o.name.startswith('PORT | ')]
    scene.frame_set(1)
    bpy.context.view_layer.update()
    originals={o.name:o.matrix_world.copy() for o in ports}
    max_joint_error=0.
    max_length_error=0.
    max_port_error=0.
    piston_heights=[]
    for frame in range(1,98):
        scene.frame_set(frame)
        bpy.context.view_layer.update()
        crank=pin.matrix_world.translation
        head=model.matrix_world@Vector((.335,-.16,1.54+piston.location.z))
        end_a=link.matrix_world@Vector((0,0,-ROD_LENGTH/2))
        end_b=link.matrix_world@Vector((0,0,ROD_LENGTH/2))
        max_joint_error=max(max_joint_error,(end_a-crank).length,(end_b-head).length)
        max_length_error=max(max_length_error,abs((end_b-end_a).length-ROD_LENGTH))
        piston_heights.append(float(piston.location.z))
        for obj in ports:
            max_port_error=max(max_port_error,max(abs(obj.matrix_world[i][j]-originals[obj.name][i][j]) for i in range(4) for j in range(4)))
    assert max_joint_error<1e-5 and max_length_error<1e-6 and max_port_error<1e-7
    assert len(ports)==4 and all(len(o.data.vertices)==256 for o in ports)
    result={'schema':'tanks.pipe-pump.v2.mechanism-check','passed':True,
        'sampled_frames':97,'rigid_rod_length_tiles':ROD_LENGTH,
        'maximum_joint_error_tiles':max_joint_error,'maximum_rod_length_error_tiles':max_length_error,
        'maximum_port_motion_tiles':max_port_error,'piston_stroke_tiles':max(piston_heights)-min(piston_heights),
        'native_positions':[[0,-.75],[0,.75]],'bucket_mechanism':False,
        'game_integrated':False,'visual_approved':False}
    record(out/'mechanism-inspection.json',result)
    scene.frame_set(1)
    return result

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--source',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True)
    p.add_argument('--fmpl-tools',type=Path,required=True)
    args=p.parse_args(sys.argv[sys.argv.index('--')+1:])
    source=args.source.resolve()
    assert sha(source)==EXPECTED_SOURCE,'Expected the recovered successful V1 master'
    out=args.out.resolve()
    if out.exists():raise FileExistsError(out)
    out.mkdir(parents=True)
    sys.path.insert(0,str(args.fmpl_tools.resolve()))
    from blender_camera_guard import install_canonical_camera,assert_clean,camera_record
    bpy.ops.wm.open_mainfile(filepath=str(source))
    scene=bpy.context.scene
    scene.frame_set(1)
    model=bpy.data.objects['EXPORT | rotate primitive steam-powered pump, never camera']
    model.rotation_euler=(0,0,0)
    wheel=bpy.data.objects['MOTION | keyed lateral 3D drive flywheel']
    piston=bpy.data.objects['MOTION | vertically reciprocating piston']
    link=bpy.data.objects['MOTION | hinged connecting rod']
    pin=bpy.data.objects['MOTION | crank eccentric pin']
    motion=link.users_collection[0]
    iron=bpy.data.materials['PUMP | forged iron']
    bronze=bpy.data.materials['PUMP | brass collar']
    for obj in (wheel,piston,link):obj.animation_data_clear()
    pin.location.z=RADIUS
    link.scale=(1,1,1)
    for v in link.data.vertices:v.co.z*=ROD_LENGTH
    # Crosshead reaches the crank plane; the rod runs in one plane rather than
    # skewing sideways from a centerline head to an offset wheel.
    crosshead=bpy.data.objects['MOTION | crosshead on straight guides']
    for v in crosshead.data.vertices:v.co.x*=.74/.49
    cylinder('V2 JOINT | real crosshead pivot',(.335,-.16,1.54),.045,.095,bronze,motion,piston)
    for z in (-ROD_LENGTH/2,ROD_LENGTH/2):
        bpy.ops.mesh.primitive_torus_add(major_segments=40,minor_segments=10,major_radius=.045,minor_radius=.012)
        eye=bpy.context.object
        eye.name='V2 JOINT | connecting rod eye'
        for c in tuple(eye.users_collection):c.objects.unlink(eye)
        motion.objects.link(eye)
        eye.parent=link
        eye.location=(0,0,z)
        eye.rotation_euler.y=math.pi/2
        eye.data.materials.append(iron)
    for frame in range(1,98):
        phase=(frame-1)*math.tau/96
        crank=Vector((.335,-.15-RADIUS*math.sin(phase),.94+RADIUS*math.cos(phase)))
        dy=-.16-crank.y
        head_z=crank.z+math.sqrt(ROD_LENGTH**2-dy**2)
        head=Vector((.335,-.16,head_z))
        wheel.rotation_euler.x=phase
        piston.location.z=head_z-1.54
        link.location=(crank+head)/2
        link.rotation_mode='QUATERNION'
        link.rotation_quaternion=(head-crank).to_track_quat('Z','Y')
        for obj,field in ((wheel,'rotation_euler'),(piston,'location'),(link,'location'),(link,'rotation_quaternion')):
            obj.keyframe_insert(data_path=field,frame=frame)
    for obj in (wheel,piston,link):linear_keys(obj)
    pipes=[o for o in children(model) if o.name.startswith('PIPE | ')]
    assert len(pipes)==2
    for old in pipes:
        points=[tuple(p.co[:3]) for p in old.data.splines[0].points]
        name,mat,coll=old.name,old.data.materials[0],old.users_collection[0]
        bpy.data.objects.remove(old,do_unlink=True)
        pipe_mesh(name+' | hollow smooth mesh',points,mat,coll,model)
    scene.render.fps=48
    scene.frame_start,scene.frame_end=1,97
    profile={'camera_policy':'fmpl.factorio45.v1','capture_kind':'entity','orientation_policy':'rotatable',
        'directions':[0,90,180,270],'states':{'idle':[1],'working':[1,49]},'source_size':768,
        'camera_override':{'type':'ORTHO','elevation_deg':45,'azimuth_deg':0,
                          'distance':math.sqrt(72),'ortho_scale':3.85,'target':[0,0,.93]}}
    install_canonical_camera(scene,profile,bpy)
    scene.cycles.samples=48
    scene.cycles.use_denoising=False
    result=inspect(scene,model,out)
    scene['production_status']='mechanism candidate; surfaces and game integration remain open'
    scene['functional_contract']='Two-port burner pipe pump; no lifting buckets, no third external steam port'
    record(out/'capture-profile.json',profile)
    record(out/'provenance.json',{'recovered_source_sha256':EXPECTED_SOURCE,'artifact_id':13927757032,
        'builder_sha256':sha(__file__),'camera':camera_record(scene),
        'changes':['Constant-length slider-crank; no stretching rod','Crank-plane crosshead and real pivots',
                   'True hollow smooth pipe meshes survive GLB export','Canonical FMPL camera installed and validated'],
        'surface_limit':'Inherited procedural timber/metal bump still needs model-specific baking and visual refinement',
        'game_integrated':False,'owner_visual_approved':False})
    native=out/'pipe-pump-v2.blend'
    bpy.ops.wm.save_as_mainfile(filepath=str(native),compress=True)
    # Independent source reopen is performed before export and repeated checks.
    bpy.ops.wm.open_mainfile(filepath=str(native))
    scene=bpy.context.scene
    model=bpy.data.objects['EXPORT | rotate primitive steam-powered pump, never camera']
    assert_clean(scene,profile,bpy)
    result=inspect(scene,model,out)
    bpy.ops.object.select_all(action='DESELECT')
    for obj in children(model):obj.select_set(True)
    bpy.ops.export_scene.gltf(filepath=str(out/'pipe-pump-v2.glb'),export_format='GLB',use_selection=True,
        export_cameras=False,export_lights=False,export_animations=True,export_animation_mode='SCENE',
        export_frame_range=True,export_force_sampling=True,export_frame_step=1,export_apply=True,export_extras=True)
    renders=[]
    for direction,yaw in [('north',0),('east',270),('south',180),('west',90)]:
        model.rotation_euler.z=math.radians(yaw)
        for frame in (1,49):
            scene.frame_set(frame)
            assert_clean(scene,profile,bpy)
            image=out/(direction+'-working-'+str(frame)+'.png')
            scene.render.filepath=str(image)
            bpy.ops.render.render(write_still=True)
            renders.append({'file':image.name,'sha256':sha(image),'frame':frame,'direction':direction})
    record(out/'candidate-receipt.json',{'source_sha256':sha(native),'glb_sha256':sha(out/'pipe-pump-v2.glb'),
        'mechanism':result,'renders':renders,'blender':bpy.app.version_string,'overall_finished':False})
    print('PIPE_PUMP_MECHANISM_REFINED',json.dumps(result),flush=True)

if __name__=='__main__':main()
