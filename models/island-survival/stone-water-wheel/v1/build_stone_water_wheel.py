"""Author an original scoop wheel; stage editable source and FMPL export only.

Run in Blender 5.x. Requires the exact reusable fluid fixture and verified FMPL
camera authority. All output is a fresh candidate directory; game art is untouched.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import sys

import bpy
import numpy as np
from mathutils import Vector

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
TAU = math.tau
FRAMES = list(range(1, 92, 6))
WATERLINE = .25

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def git_blob(path):
    b = Path(path).read_bytes()
    return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()

def write_json(path, data):
    Path(path).write_text(json.dumps(data, indent=2)+'\n', encoding='utf-8')

def collection(name):
    c = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(c)
    return c

def empty(name, parent=None, location=(0,0,0)):
    o = bpy.data.objects.new(name, None)
    MODEL.objects.link(o)
    o.parent, o.location = parent, location
    return o

def finish(o, name, mat, parent= None, bevel=.008):
    o.name = name
    for c in tuple(o.users_collection):
        c.objects.unlink(o)
    MODEL.objects.link(o)
    o.parent = parent or ROOT_OBJ
    o.data.materials.append(mat)
    if bevel:
        mod = o.modifiers.new('Supported softened edges', 'BEVEL')
        mod.width, mod.segments = bevel, 2
        o.modifiers.new('Weighted surface normals', 'WEIGHTED_NORMAL')
    return o

def uv_box(o):
    # Each real face has local grain along its longest dimension. This is
    # physical per-piece placement, rather than one world-space stripe mask.
    mesh = o.data
    uv = mesh.uv_layers.active or mesh.uv_layers.new(name='Authored physical grain')
    for face in mesh.polygons:
        coords = [mesh.vertices[mesh.loops[i].vertex_index].co for i in face.loop_indices]
        axes = sorted(range(3), key=lambda k:max(v[k] for v in coords)-min(v[k] for v in coords), reverse=True)
        u,v = axes[:2]
        low_u,low_v = min(p[u] for p in coords),min(p[v] for p in coords)
        len_u = max(p[u] for p in coords)-low_u
        len_v = max(p[v] for p in coords)-low_v
        for idx,p in zip(face.loop_indices, coords):
            uv.data[idx].uv = (.025+.95*(p[u]-low_u)/max(len_u,1e-6),
                               .025+.95*(p[v]-low_v)/max(len_v,1e-6))

def box(name, pos, dims, mat, parent=None, bevel=.008, rotation=(0,0,0)):
    bpy.ops.mesh.primitive_cube_add(size=1)
    o = bpy.context.object
    o.scale = dims
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    uv_box(o)
    finish(o, name, mat, parent, bevel)
    o.location, o.rotation_euler = pos, rotation
    return o

def cylinder(name, pos, radius, depth, mat, parent=None):
    bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=radius, depth=depth)
    o = finish(bpy.context.object, name, mat, parent, .003)
    o.location, o.rotation_euler = pos, (0,math.pi/2,0)
    for face in o.data.polygons:
        if len(face.vertices)==4:
            face.use_smooth=True
    return o

def rim(name, x, outer, inner, mat, parent):
    verts, faces = [], []
    n=96
    for xx,r in ((x-.022,outer),(x+.022,outer),(x-.022,inner),(x+.022,inner)):
        verts += [(xx,r*math.cos(i*TAU/n),r*math.sin(i*TAU/n)) for i in range(n)]
    for i in range(n):
        j=(i+1)%n
        faces += [(i,j,n+j,n+i),(2*n+i,3*n+i,3*n+j,2*n+j),
                  (i,2*n+i,2*n+j,j),(n+i,n+j,3*n+j,3*n+i)]
    mesh=bpy.data.meshes.new(name)
    mesh.from_pydata(verts,[],faces)
    mesh.update()
    o=bpy.data.objects.new(name,mesh)
    MODEL.objects.link(o)
    finish(o,name,mat,parent,.004)
    uv_box(o)
    return o

def image(name, array, out, noncolor=False):
    h,w = array.shape[:2]
    im=bpy.data.images.new(name,width=w,height=h,alpha=True)
    if noncolor:
        im.colorspace_settings.name='Non-Color'
    pixels=np.ones((h,w,4),dtype=np.float32)
    if array.ndim==2:
        pixels[:,:,:3]=array[:,:,None]
    else:
        pixels[:,:,:3]=array
    im.pixels.foreach_set(pixels.ravel())
    im.filepath_raw=str(out/(name+'.png'))
    im.file_format='PNG'
    im.save()
    im.pack()
    return im

def pbr(name, color, roughness, metallic=0, maps=None):
    m=bpy.data.materials.new(name)
    m.use_nodes=True
    m.diffuse_color=(*color,1)
    bs=m.node_tree.nodes.get('Principled BSDF')
    bs.inputs['Base Color'].default_value=(*color,1)
    bs.inputs['Roughness'].default_value=roughness
    bs.inputs['Metallic'].default_value=metallic
    if maps:
        for role,im in maps.items():
            tex=m.node_tree.nodes.new('ShaderNodeTexImage')
            tex.image=im
            if role=='albedo':
                m.node_tree.links.new(tex.outputs['Color'],bs.inputs['Base Color'])
            elif role=='roughness':
                m.node_tree.links.new(tex.outputs['Color'],bs.inputs['Roughness'])
            elif role=='orm':
                sep=m.node_tree.nodes.new('ShaderNodeSeparateColor')
                m.node_tree.links.new(tex.outputs['Color'],sep.inputs['Color'])
                m.node_tree.links.new(sep.outputs['Green'],bs.inputs['Roughness'])
                m.node_tree.links.new(sep.outputs['Blue'],bs.inputs['Metallic'])
            elif role=='normal':
                norm=m.node_tree.nodes.new('ShaderNodeNormalMap')
                norm.inputs['Strength'].default_value=.45
                m.node_tree.links.new(tex.outputs['Color'],norm.inputs['Color'])
                m.node_tree.links.new(norm.outputs['Normal'],bs.inputs['Normal'])
    return m

def materials(args,out):
    # A unique image set designed for this wheel's long planks and cup walls.
    u,v=np.meshgrid(np.linspace(0,1,512),np.linspace(0,1,256))
    grain=np.sin(v*230+np.sin(u*8)*1.8)+.35*np.sin(v*641+np.sin(u*19))
    height=.5+.16*grain+.04*np.sin(u*50+v*35)
    wood=np.stack([.30+.070*grain,.20+.048*grain,.105+.027*grain],axis=-1)
    wood_maps={'albedo':image('wheel-driftwood-grain-albedo',np.clip(wood,.025,.8),out),
               'roughness':image('wheel-driftwood-grain-roughness',np.clip(.78+.055*grain,.55,.96),out,True)}
    dy,dx=np.gradient(height)
    normal=np.stack([-dx*5,-dy*5,np.ones_like(dx)],axis=-1)
    normal/=np.linalg.norm(normal,axis=-1)[:,:,None]
    wood_maps['normal']=image('wheel-driftwood-grain-normal',normal*.5+.5,out,True)
    fmpl={}
    records={}
    want={'albedo':'e1a06e81086b1228188e1e47bca236aaada1394c',
          'orm':'379af05909cd028194b5f38a74f19c7911ff9eb1',
          'normal':'8cbbf97beb1866109df97124901fefad66e137b5'}
    for role in want:
        path=args.materials_root/('ferrocrete_'+role+'.png')
        assert git_blob(path)==want[role], 'FMPL source map changed: '+str(path)
        im=bpy.data.images.load(str(path),check_existing=False)
        im.name='WHEEL | FMPL footing '+role
        if role!='albedo':
            im.colorspace_settings.name='Non-Color'
        im.pack()
        fmpl[role]=im
        records[path.name]={'git_blob':want[role],'sha256':sha(path)}
    mats={
        'wood':pbr('WHEEL | lengthwise salt-worn timber',(.30,.20,.105),.8,maps=wood_maps),
        'stone':pbr('WHEEL | bedded stone faces',(.36,.38,.32),.90),
        'stone2':pbr('WHEEL | wet lower stone courses',(.21,.25,.23),.72),
        'pad':pbr('WHEEL | FMPL isolated ferrocrete feet',(.35,.35,.33),.85,maps=fmpl),
        'iron':pbr('WHEEL | forged straps and pins',(.095,.115,.12),.55,.82),
        'bearing':pbr('WHEEL | bronze axle bearing',(.33,.22,.085),.42,.72),
        'water':pbr('WHEEL | carried water',(.055,.23,.29),.23,.12)}
    return mats,records

def construct(args,out):
    global MODEL,ROOT_OBJ
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene=bpy.context.scene
    MODEL=collection('STONE WATER WHEEL | authored editable geometry')
    ROOT_OBJ=empty('WHEEL | placement root')
    ROOT_OBJ['prototype']='offshore-pump/stone-water-wheel'
    ROOT_OBJ['units_per_tile']=1.
    mats,records=materials(args,out)
    # Load paths: four small independent feet support two masonry bearing piers.
    for side in (-1,1):
        for yy in (.19,.66):
            box('Footing | isolated structural pad',(side*.46,yy,.06),(.28,.35,.12),mats['pad'])
        for level in range(3):
            for row in range(2):
                yy=.17+row*.28+(.025 if level%2 else 0)
                box('Masonry | fitted bearing pier',(side*.46,yy,.18+level*.15),
                    (.24,.265,.14),mats['stone2' if level==0 else 'stone'],bevel=.022)
        box('Masonry | continuous bearing cap',(side*.46,.43,.62),(.30,.64,.13),mats['stone'],bevel=.018)
        cylinder('Bearing | stationary bronze bush',(side*.46,.43,.73),.105,.19,mats['bearing'])
        box('Bearing | strap foot',(side*.46,.43,.66),(.2,.26,.04),mats['iron'])
        for yy in (.33,.53):
            box('Bearing | supported anchor bolt',(side*.46,yy,.695),(.045,.045,.045),mats['iron'],bevel=.004)
    wheel=empty('WHEEL | rotating scoop assembly',ROOT_OBJ,(0,.43,.73))
    for x in (-.205,.205):
        rim('Rim | segmented timber annulus',x,.52,.44,mats['wood'],wheel)
        rim('Rim | forged external retaining band',x,.531,.513,mats['iron'],wheel)
        for i in range(8):
            angle=i*TAU/8
            box('Spoke | jointed radial timber',(x,.25*math.cos(angle),.25*math.sin(angle)),
                (.048,.46,.055),mats['wood'],wheel,.006,(angle,0,0))
    cylinder('Axle | through timber shaft',(0,0,0),.064,1.15,mats['wood'],wheel)
    for x in (-.245,.245):
        cylinder('Hub | forged retaining boss',(x,0,0),.12,.075,mats['iron'],wheel)
    for i in range(12):
        cup=empty('Scoop %02d | open top timber cup'%i,wheel)
        cup.rotation_euler.x=i*TAU/12
        box('Scoop %02d | radial back'%i,(0,.48,0),(.40,.045,.16),mats['wood'],cup)
        box('Scoop %02d | supported lip'%i,(0,.405,-.075),(.40,.15,.025),mats['wood'],cup,.004)
        for xx in (-.20,.20):
            box('Scoop %02d | closed end cheek'%i,(xx,.435,0),(.025,.13,.16),mats['wood'],cup,.004)
            cylinder('Scoop %02d | cheek fastener'%i,(xx*1.08,.48,.035),.015,.018,mats['iron'],cup)
        carried=box('Scoop %02d | carried water'%i,(0,.428,-.045),(.34,.10,.018),mats['water'],cup,.002)
        for frame in range(1,98):
            angle=(i*TAU/12-TAU*(frame-1)/96)%TAU
            # Fill while submerged, carry up the rising front, empty near top.
            carried.scale.z=1 if math.pi*.58<angle<math.pi*1.54 else .001
            carried.keyframe_insert(data_path='scale',frame=frame)
        if i==0:
            box('Repair | unique bolted scoop strap',(0,.51,.025),(.27,.02,.035),mats['iron'],cup,.003)
            for xx in (-.10,.10):
                box('Repair | strap bolt',(xx,.525,.025),(.026,.018,.026),mats['iron'],cup,.003)
    # Fixed discharge race sits beside the rising quadrant; its feed mouth is
    # clear of the rotating wheel by 0.06 tile along X.
    box('Discharge | open timber race floor',(-.375,.13,.94),(.19,.78,.045),mats['wood'])
    for xx in (-.48,-.27):
        box('Discharge | race side rail',(xx,.13,1.005),(.025,.78,.15),mats['wood'])
    box('Discharge | visible water in race',(-.375,.13,.975),(.17,.72,.015),mats['water'],bevel=.003)
    for yy in (-.18,.42):
        box('Discharge | supported race bracket',(-.375,yy,.85),(.20,.075,.16),mats['iron'])
    # Collection vessel is built around the full-size canonical collar and throat.
    box('Outlet | timber collection box',(0,-.29,.44),(.64,.28,.48),mats['wood'],bevel=.018)
    box('Outlet | collection water surface',(0,-.29,.69),(.54,.22,.014),mats['water'],bevel=.005)
    box('Discharge | landward upright support',(-.46,-.18,.48),(.11,.11,.84),mats['wood'])
    box('Discharge | upright footing',(-.46,-.18,.06),(.22,.22,.12),mats['pad'])
    for z in (.28,.60):
        box('Outlet | front forged band',(0,-.445,z),(.66,.028,.045),mats['iron'])
    reference=args.fixture
    assert sha(reference)=='af6d1d74f0439b327b0b4e496386aa35fdac0859c177b55707dbfb5243e691ca'
    with bpy.data.libraries.load(str(reference),link=False) as (src,dst):
        dst.objects=['IFACE | machine collar template','IFACE | machine throat template']
    for obj in dst.objects:
        MODEL.objects.link(obj)
        obj.parent=ROOT_OBJ
        obj.location=(0,-.49,0)
        obj.rotation_euler=(0,0,math.pi)
        obj.data.materials.clear()
        obj.data.materials.append(mats['iron'])
        obj['role']='stationary_outlet'
        obj.name='Outlet | canonical '+('collar' if 'collar' in obj.name else 'full bore throat')
    # Discard parent dependencies pulled with library objects, retain editable meshes.
    for obj in list(bpy.data.objects):
        if obj.name.startswith('IFACE |') and obj not in dst.objects:
            bpy.data.objects.remove(obj,do_unlink=True)
    marker=empty('SOCKET | nominal south visual mouth',ROOT_OBJ,(0,-.49,.36))
    marker['native_position']=[0,.25]
    marker['registration']='visual nominal from Beach Pump V2; native calibration pending'
    wheel.rotation_mode='XYZ'
    for frame,angle in ((1,0),(97,-TAU)):
        wheel.rotation_euler.x=angle
        wheel.keyframe_insert(data_path='rotation_euler',frame=frame)
    # Set linear interpolation through action slots using the actual Blender API.
    action=wheel.animation_data.action
    for layer in action.layers:
        for strip in layer.strips:
            for bag in strip.channelbags:
                for curve in bag.fcurves:
                    for key in curve.keyframe_points:
                        key.interpolation='LINEAR'
    scene.frame_start,scene.frame_end=1,97
    scene.render.fps=48
    scene['candidate_state']='working'
    scene['shoreline_waterline']=WATERLINE
    scene['surface_plan']='Timber grain per piece; wet stone only in lowest courses; forged rims/pins; bronze bearings; FMPL pad PBR only on discrete load-bearing feet.'
    scene['gameplay_unchanged']=True
    profile={'camera_policy':'fmpl.factorio45.v1','capture_kind':'entity',
        'orientation_policy':'rotatable','directions':[0,90,180,270],
        'states':{'idle':[1],'working':FRAMES},'source_size':256,
        'camera_override':{'type':'ORTHO','elevation_deg':45,'azimuth_deg':0,
            'distance':8,'ortho_scale':2.5,'target':[0,.20,.66]}}
    from blender_camera_guard import install_canonical_camera,assert_clean,camera_record
    install_canonical_camera(scene,profile,bpy)
    scene.render.engine='CYCLES'
    scene.cycles.samples=24
    scene.cycles.use_denoising=False
    scene.cycles.seed=1511
    scene.render.threads_mode='FIXED'
    scene.render.threads=6
    scene.render.film_transparent=True
    scene.render.image_settings.file_format='PNG'
    scene.render.image_settings.color_mode='RGBA'
    scene.view_settings.view_transform='AgX'
    scene.world=bpy.data.worlds.new('WHEEL | daylight world')
    scene.world.use_nodes=True
    scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.35
    for name,pos,power,size in [('key',(-3,-4,6),450,4),('fill',(3,2,4),180,3)]:
        light=bpy.data.lights.new('WHEEL | '+name,'AREA')
        light.energy,light.shape,light.size=power,'DISK',size
        o=bpy.data.objects.new(light.name,light)
        scene.collection.objects.link(o)
        o.location=pos
        o.rotation_euler=(Vector((0,.3,.5))-o.location).to_track_quat('-Z','Y').to_euler()
    scene.frame_set(1)
    bpy.context.view_layer.update()
    assert_clean(scene,profile,bpy)
    write_json(out/'capture-profile.json',profile)
    write_json(out/'provenance.json',{'source_baseline':'7290824bf43711d0bb31bd8e2969c51459864f91',
        'builder_sha256':sha(__file__),'fixture_sha256':sha(reference),'fmpl_maps':records,
        'fmpl_material_revision':'b16f98c6e62d0a82697fd01eaa3fc6953c35ccde',
        'fmpl_camera_revision':'939ff2d0fea5d236d7092b907c5f08961d5a7560',
        'materials':'Original model-specific timber images and stone/metal finishes; FMPL original ferrocrete maps on feet only.',
        'camera':camera_record(scene),'native_registration':'pending actual Factorio offshore-pump test'})
    bpy.ops.wm.save_as_mainfile(filepath=str(out/'stone-water-wheel-v1.blend'),compress=True)
    # Selection-only export contains physical geometry and mechanism, no camera/light.
    bpy.ops.object.select_all(action='DESELECT')
    for obj in MODEL.objects:
        obj.select_set(True)
    bpy.ops.export_scene.gltf(filepath=str(out/'stone-water-wheel-v1.glb'),export_format='GLB',
        use_selection=True,export_cameras=False,export_lights=False,export_animations=True,
        export_animation_mode='SCENE',export_frame_range=True,export_force_sampling=True,
        export_frame_step=6,export_apply=True,export_extras=True)
    return scene,profile

def install_layer_clips():
    """Derived render shader only: exact world-height split, never double-body masks."""
    controls=[]
    for mat in bpy.data.materials:
        if not mat.use_nodes:
            continue
        nodes,links=mat.node_tree.nodes,mat.node_tree.links
        output=next((n for n in nodes if n.type=='OUTPUT_MATERIAL'),None)
        if output is None or not output.inputs['Surface'].links:
            continue
        old=output.inputs['Surface'].links[0].from_socket
        geo=nodes.new('ShaderNodeNewGeometry')
        sep=nodes.new('ShaderNodeSeparateXYZ')
        compare=nodes.new('ShaderNodeMath')
        compare.inputs[1].default_value=WATERLINE
        gate=nodes.new('ShaderNodeMath')
        gate.operation='MULTIPLY'
        gate.inputs[1].default_value=0
        mix=nodes.new('ShaderNodeMixShader')
        # Holdout preserves the first visible surface as an occluder. Plain
        # transparency would reveal hidden back surfaces in the other layer.
        transparent=nodes.new('ShaderNodeHoldout')
        links.new(geo.outputs['Position'],sep.inputs['Vector'])
        links.new(sep.outputs['Z'],compare.inputs[0])
        links.new(compare.outputs[0],gate.inputs[0])
        links.new(gate.outputs[0],mix.inputs[0])
        links.new(old,mix.inputs[1])
        links.new(transparent.outputs[0],mix.inputs[2])
        links.new(mix.outputs[0],output.inputs['Surface'])
        controls.append((compare,gate))
    return controls

def render(scene,profile,out,full):
    from blender_camera_guard import assert_clean
    root=bpy.data.objects['WHEEL | placement root']
    wheel=bpy.data.objects['WHEEL | rotating scoop assembly']
    frames=FRAMES if full else [1,25]
    manifest=[]
    controls=install_layer_clips()
    for facing,yaw in [('north',0),('east',270),('south',180),('west',90)]:
        root.rotation_euler.z=math.radians(yaw)
        for state in ('idle','working'):
            for frame in ([1] if state=='idle' else frames):
                scene.frame_set(frame)
                if state=='idle':
                    wheel.rotation_euler.x=0
                bpy.context.view_layer.update()
                assert_clean(scene,profile,bpy)
                for layer in ('full','above-water','underwater'):
                    for compare,gate in controls:
                        gate.inputs[1].default_value=0 if layer=='full' else 1
                        compare.operation='LESS_THAN' if layer=='above-water' else 'GREATER_THAN'
                    path=out/(f'{facing}-{state}-{frame:03d}-{layer}.png')
                    scene.render.filepath=str(path)
                    bpy.ops.render.render(write_still=True)
                    manifest.append({'file':path.name,'sha256':sha(path),'facing':facing,'yaw':yaw,'state':state,'frame':frame,'layer':layer})
    root.rotation_euler.z=0
    scene.frame_set(1)
    write_json(out/'render-manifest.json',{'kind':'full' if full else 'pilot',
        'genuine_blender_frames':len(manifest),'source_sha256':sha(out/(scene.get('asset_stem','stone-water-wheel-v1')+'.blend')),
        'runtime_export_sha256':sha(out/(scene.get('asset_stem','stone-water-wheel-v1')+'.glb')),'blender':bpy.app.version_string,'images':manifest})

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--fmpl-tools',type=Path,required=True)
    parser.add_argument('--materials-root',type=Path,required=True)
    parser.add_argument('--fixture',type=Path,required=True)
    parser.add_argument('--full',action='store_true')
    args=parser.parse_args(sys.argv[sys.argv.index('--')+1:])
    args.fixture=args.fixture.resolve()
    args.materials_root=args.materials_root.resolve()
    out=args.out.resolve()
    if out.exists():
        raise FileExistsError('Preserve prior candidate; choose a fresh output directory: '+str(out))
    out.mkdir(parents=True)
    sys.path.insert(0,str(args.fmpl_tools.resolve()))
    scene,profile=construct(args,out)
    render(scene,profile,out,args.full)
    print('STONE_WATER_WHEEL_CANDIDATE',str(out),flush=True)

if __name__=='__main__':
    main()
