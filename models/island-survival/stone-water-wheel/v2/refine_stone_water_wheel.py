"""Rebuild the rejected V1 wheel's construction, joinery and surface treatment."""
import argparse
import importlib.util
import json
import math
from pathlib import Path
import sys

import bpy
import numpy as np

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('wheel_base',HERE.parent/'v1/build_stone_water_wheel.py')
base=importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)
TAU=math.tau

def mesh_object(name,vertices,faces,mat,parent,bevel=.005):
    mesh=bpy.data.meshes.new(name)
    mesh.from_pydata(vertices,[],faces)
    mesh.update()
    obj=bpy.data.objects.new(name,mesh)
    base.MODEL.objects.link(obj)
    base.finish(obj,name,mat,parent,bevel)
    base.uv_box(obj)
    return obj

def beam(name,start,end,width,depth,mat,parent):
    from mathutils import Vector
    a,b=Vector(start),Vector(end)
    obj=base.box(name,(a+b)/2,(width,depth,(b-a).length),mat,parent,.008)
    obj.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler()
    return obj

def stone(name,pos,dims,mat,seed):
    rng=np.random.default_rng(seed)
    obj=base.box(name,pos,dims,mat,bevel=0)
    # Deliberately fitted bedding faces, worn variable corners and sloped ends.
    for v in obj.data.vertices:
        v.co.x+=float(rng.uniform(-.012,.012))
        v.co.y+=float(rng.uniform(-.012,.012))
        if v.co.z>0:
            v.co.z+=float(rng.uniform(-.007,.007))
    mod=obj.modifiers.new('Worn stone arrises','BEVEL')
    mod.width,mod.segments=.018,3
    obj.modifiers.new('Weighted stone normals','WEIGHTED_NORMAL')
    return obj

def sector(name,x,start,end,r0,r1,mat,parent):
    verts=[]
    n=9
    for xx,r in ((x-.025,r0),(x-.025,r1),(x+.025,r0),(x+.025,r1)):
        verts.extend((xx,r*math.cos(a),r*math.sin(a)) for a in np.linspace(start,end,n))
    faces=[]
    for i in range(n-1):
        j=i+1
        faces += [(i,j,n+j,n+i),(2*n+i,3*n+i,3*n+j,2*n+j),
                  (i,2*n+i,2*n+j,j),(n+i,n+j,3*n+j,3*n+i)]
    faces += [(0,n,3*n,2*n),(n-1,3*n-1,4*n-1,2*n-1)]
    obj=mesh_object(name,verts,faces,mat,parent,.004)
    # Circumferential grain follows this actual curved timber segment.
    for poly in obj.data.polygons:
        for idx in poly.loop_indices:
            co=obj.data.vertices[obj.data.loops[idx].vertex_index].co
            a=math.atan2(co.z,co.y)
            while a<start-.1:a+=TAU
            radius=math.hypot(co.y,co.z)
            obj.data.uv_layers.active.data[idx].uv=(.025+.95*(a-start)/(end-start),.05+.9*(radius-r0)/(r1-r0))
    return obj

def sleeve(name,x,depth,outer,inner,mat,parent):
    obj=base.rim(name,x,outer,inner,mat,parent)
    # The original helper has 0.044 axial thickness. Keep the bore, extend only X.
    for v in obj.data.vertices:
        v.co.x=x+(v.co.x-x)*depth/.044
    return obj

def surface_maps(out):
    u,v=np.meshgrid(np.linspace(0,1,768),np.linspace(0,1,384))
    fibers=np.sin(v*430+1.9*np.sin(u*9+v*4))+.24*np.sin(v*1170+np.sin(u*31))
    broad=np.sin(v*49+np.sin(u*8))*.5
    knot=np.exp(-((u-.63)**2/.002+(v-.41)**2/.009))
    height=.5+.10*fibers+.07*broad-.13*knot
    wood=np.stack([.38+.055*fibers+.035*broad,.285+.045*fibers+.027*broad,.17+.028*fibers+.02*broad],axis=-1)
    wood*=1-.30*knot[:,:,None]
    dy,dx=np.gradient(height)
    n=np.stack([-dx*4,-dy*4,np.ones_like(dx)],axis=-1)
    n/=np.linalg.norm(n,axis=-1)[:,:,None]
    maps={'albedo':base.image('v2-wheel-timber-albedo',np.clip(wood,.025,.8),out),
          'roughness':base.image('v2-wheel-timber-roughness',np.clip(.73+.04*fibers,.55,.94),out,True),
          'normal':base.image('v2-wheel-timber-normal',n*.5+.5,out,True)}
    woodmat=base.pbr('V2 | weathered structural oak grain by part',(.38,.285,.17),.75,maps=maps)
    rng=np.random.default_rng(15112026)
    p,q=np.meshgrid(np.linspace(0,1,384),np.linspace(0,1,384))
    def stone_noise(band):
        raw=rng.normal(0,1,p.shape)
        f=np.fft.fftfreq(p.shape[0])
        fx,fy=np.meshgrid(f,f)
        filtered=np.fft.ifft2(np.fft.fft2(raw)*np.exp(-(fx*fx+fy*fy)/(2*band*band))).real
        return filtered/max(filtered.std(),1e-6)
    mineral=.023*stone_noise(.025)+.012*stone_noise(.09)+.004*stone_noise(.35)
    h=.5+.25*mineral
    dy,dx=np.gradient(h)
    n=np.stack([-dx*3,-dy*3,np.ones_like(dx)],axis=-1)
    n/=np.linalg.norm(n,axis=-1)[:,:,None]
    rgb=np.stack([.29+mineral,.305+mineral,.26+mineral*.85],axis=-1)
    sm={'albedo':base.image('v2-wheel-bedded-stone-albedo',np.clip(rgb,.03,.7),out),
        'roughness':base.image('v2-wheel-bedded-stone-roughness',np.clip(.84+mineral,.7,.96),out,True),
        'normal':base.image('v2-wheel-bedded-stone-normal',n*.5+.5,out,True)}
    stonemat=base.pbr('V2 | weathered individually bedded stone',(.29,.305,.26),.85,maps=sm)
    wet=stonemat.copy()
    wet.name='V2 | water-stained stone foot courses'
    wet.node_tree.nodes.get('Principled BSDF').inputs['Roughness'].default_value=.58
    return woodmat,stonemat,wet

def rebuild(args,out):
    bpy.ops.wm.open_mainfile(filepath=str(args.source.resolve()))
    scene=bpy.context.scene
    scene.frame_set(1)
    base.MODEL=bpy.data.collections['STONE WATER WHEEL | authored editable geometry']
    base.ROOT_OBJ=bpy.data.objects['WHEEL | placement root']
    root=base.ROOT_OBJ
    wheel=bpy.data.objects['WHEEL | rotating scoop assembly']
    keep={root,wheel,*[o for o in base.MODEL.objects if o.get('role')=='stationary_outlet']}
    for obj in list(base.MODEL.objects):
        if obj not in keep:
            bpy.data.objects.remove(obj,do_unlink=True)
    wood,rock,wet=surface_maps(out)
    iron=base.pbr('V2 | dark forged retaining iron',(.10,.12,.115),.47,.75)
    bronze=base.pbr('V2 | polished worn bearing bronze',(.36,.265,.11),.35,.72)
    water=base.pbr('V2 | shallow carried water',(.055,.20,.235),.18,.12)
    pad=next(m for m in bpy.data.materials if m.name=='WHEEL | FMPL isolated ferrocrete feet')
    wheel.location=(0,.47,.65)
    for side in (-1,1):
        for yy in (.32,.62):
            base.box('V2 footing | inset separate structural foot',(side*.46,yy,.04),(.27,.29,.08),pad,bevel=.014)
        for layer in range(3):
            for row in range(2):
                yy=.36+row*.22+(.012 if layer%2 else 0)
                stone('V2 masonry | fitted coursed bearing pier',(side*.46,yy,.15+layer*.13),(.24,.205,.12),wet if layer==0 else rock,layer*4+row+(10 if side==1 else 0))
        cap=stone('V2 masonry | carved bearing saddle',(side*.46,.47,.53),(.29,.46,.11),rock,31+(1 if side==1 else 0))
        # Cut the real concave bearing seat before adding its hollow sleeve.
        bpy.ops.mesh.primitive_cylinder_add(vertices=64,radius=.105,depth=.5,location=(side*.46,.47,.65),rotation=(0,math.pi/2,0))
        cutter=bpy.context.object
        boolean=cap.modifiers.new('Carved half-round axle seat','BOOLEAN')
        boolean.object=cutter
        boolean.operation='DIFFERENCE'
        bpy.context.view_layer.objects.active=cap
        bpy.ops.object.modifier_apply(modifier=boolean.name)
        bpy.data.objects.remove(cutter,do_unlink=True)
        bearing_root=base.empty('V2 bearing | fixed seat',root,(0,.47,.65))
        sleeve('V2 bearing | hollow bronze sleeve',side*.46,.19,.108,.069,bronze,bearing_root)
        sleeve('V2 bearing | raised iron lip',side*.565,.025,.125,.071,iron,bearing_root)
        for yy in (.36,.58):
            base.box('V2 bearing | anchored forged shoe',(side*.46,yy,.586),(.19,.055,.025),iron)
            base.box('V2 bearing | load-bearing bolt head',(side*.46,yy,.61),(.042,.042,.025),iron,bevel=.005)
    for side in (-1,1):
        x=side*.205
        for i in range(12):
            a=i*TAU/12
            sector('V2 rim | joined curved oak segment',x,a+.009,a+TAU/12-.009,.47,.55,wood,wheel)
            # Joint plates span two real segments and stay mounted on their rim.
            for sign in (-1,1):
                b=a+sign*.036
                base.cylinder('V2 rim | supported joint rivet',(x+side*.035,.513*math.cos(b),.513*math.sin(b)),.013,.018,iron,wheel)
        sleeve('V2 rim | thin forged tyre',x,.028,.557,.545,iron,wheel)
        for i in range(8):
            a=i*TAU/8
            beam('V2 spoke | tapered tenoned oak',(x,.10*math.cos(a),.10*math.sin(a)),(x,.49*math.cos(a),.49*math.sin(a)),.043,.045,wood,wheel)
    base.cylinder('V2 axle | turned through-shaft',(0,0,0),.062,1.19,wood,wheel)
    for side in (-1,1):
        base.cylinder('V2 hub | turned timber boss',(side*.235,0,0),.115,.10,wood,wheel)
        sleeve('V2 hub | forged binding ring',side*.29,.023,.12,.093,iron,wheel)
        base.cylinder('V2 axle | supported end washer',(side*.602,0,0),.079,.018,iron,wheel)
    for i in range(12):
        scoop=base.empty('V2 scoop %02d | curved lifting bucket'%i,wheel)
        scoop.rotation_euler.x=i*TAU/12
        # Seven fitted curved staves create a concave trough, with clear lip and
        # end-cheeks shaped to its section, rather than a solid rectangular box.
        radius=.075
        for j in range(7):
            a=-math.pi*.55+j*math.pi*1.1/6
            pos=(0,.485+radius*math.cos(a),radius*math.sin(a))
            base.box('V2 scoop %02d | fitted curved stave'%i,pos,(.35,.021,.039),wood,scoop,.004,(a,0,0))
        # Curved end-cheeks close the trough without concealing its open mouth.
        for side in (-1,1):
            verts=[(side*.18,.485,0)]
            verts += [(side*.18,.485+radius*math.cos(a),radius*math.sin(a)) for a in np.linspace(-math.pi*.55,math.pi*.55,13)]
            faces=[(0,j,j+1) for j in range(1,13)]
            cheek=mesh_object('V2 scoop %02d | curved end cheek'%i,verts,faces,wood,scoop,0)
            solid=cheek.modifiers.new('Real cheek thickness','SOLIDIFY')
            solid.thickness=.014
        carried=base.box('V2 scoop %02d | water retained in cup'%i,(0,.515,0),(.32,.025,.085),water,scoop,.003)
        for frame in range(1,98):
            a=(i*TAU/12-TAU*(frame-1)/96)%TAU
            carried.scale.z=1 if math.pi*.60<a<math.pi*1.58 else .001
            carried.keyframe_insert(data_path='scale',frame=frame)
        if i==0:
            base.box('V2 scoop | one authentic bolted repair',(0,.565,0),(.24,.012,.028),iron,scoop,.003)
    # Hollow receiving tank. Its inside remains visibly open and its narrow
    # rear wall clears the spinning wheel throughout the full sweep.
    for x in (-.275,.275):
        base.box('V2 receiver | separate side stave',(x,-.29,.40),(.035,.24,.58),wood,bevel=.006)
    for y in (-.42,-.16):
        for x in np.linspace(-.25,.25,7):
            base.box('V2 receiver | fitted front/rear plank',(x,y,.40),(.069,.032,.58),wood,bevel=.005)
    base.box('V2 receiver | supported floor',(0,-.29,.09),(.57,.28,.04),wood)
    bpy.ops.mesh.primitive_cylinder_add(vertices=96,radius=.245,depth=.9,location=(0,-.40,.36),rotation=(math.pi/2,0,0))
    bore=bpy.context.object
    for obj in list(base.MODEL.objects):
        if obj.name.startswith('V2 receiver | fitted front/rear plank'):
            mod=obj.modifiers.new('Unobstructed full-size outlet bore','BOOLEAN')
            mod.object,mod.operation=bore,'DIFFERENCE'
            bpy.context.view_layer.objects.active=obj
            bpy.ops.object.modifier_apply(modifier=mod.name)
    bpy.data.objects.remove(bore,do_unlink=True)
    base.box('V2 receiver | visible internal water',(0,-.29,.52),(.51,.20,.012),water,bevel=.002)
    for z in (.28,.56):
        base.box('V2 receiver | front binding strap',(0,-.442,z),(.59,.018,.032),iron)
        for x in (-.25,.25):
            base.box('V2 receiver | strap nail',(x,-.454,z),(.025,.012,.025),iron,bevel=.003)
    # Continuous joined race: no floating segments and its outlet actually lands
    # inside the receiver. A narrow catch lip clears the rotating scoop ends.
    path=[(-.29,.22,1.02),(-.32,.04,.87),(-.20,-.27,.69)]
    for i,(a,b) in enumerate(zip(path,path[1:])):
        from mathutils import Vector
        av,bv=Vector(a),Vector(b)
        tangent=bv-av
        across=Vector((-tangent.y,tangent.x,0)).normalized()
        def channel_strip(name,offset,width,thickness,mat,zshift=0):
            corners=[av+across*(offset-width/2),av+across*(offset+width/2),
                     bv+across*(offset+width/2),bv+across*(offset-width/2)]
            verts=[tuple(v+Vector((0,0,zshift+z))) for z in (-thickness/2,thickness/2) for v in corners]
            return mesh_object(name,verts,[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],mat,root,.003)
        channel_strip('V2 race | continuous sloping bed',0,.17,.025,wood)
        for sign in (-1,1):
            channel_strip('V2 race | joined side rail',sign*.092,.018,.105,wood,.042)
        channel_strip('V2 race | visible shallow flow',0,.145,.008,water,.018)
    for x,yy,top in ((-.38,.13,.96),(-.25,-.23,.68)):
        base.box('V2 race | timber upright',(x,yy,top/2),(.075,.075,top),wood)
        base.box('V2 race | upright foot',(x,yy,.035),(.16,.16,.07),pad,bevel=.01)
        beam('V2 race | diagonal braced support',(x,yy,.30),(x+.06,yy+.12,top-.07),.045,.045,wood,root)
    scene['asset_stem']='stone-water-wheel-v2'
    scene['visual_status']='V1 explicitly rejected as rough by owner; V2 construction pilot awaiting inspection'
    scene['surface_plan']='Curved timber grain follows individual rim arcs; long grain follows spokes, bucket staves and vessel planks. Fitted mineral-stained masonry, bronze open bearings, locally forged iron, no shared metal stripe treatment.'
    profile=json.loads((args.source.parent/'capture-profile.json').read_text())
    profile['source_size']=768
    profile['camera_override']['target']=[0,.18,.65]
    profile['camera_override']['ortho_scale']=2.30
    from blender_camera_guard import install_canonical_camera,assert_clean,camera_record
    install_canonical_camera(scene,profile,bpy)
    scene.cycles.samples=48
    scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.48
    for obj in scene.objects:
        if obj.type=='LIGHT':obj.data.energy*=1.25
    bpy.data.orphans_purge(do_recursive=True)
    scene.frame_set(1)
    assert_clean(scene,profile,bpy)
    base.write_json(out/'capture-profile.json',profile)
    base.write_json(out/'provenance.json',{'refined_from_sha256':base.sha(args.source),
        'builder_sha256':base.sha(__file__),'reason':'Owner rejected V1 rough construction',
        'camera':camera_record(scene),'materials':'Original model-specific baked timber/stone images; retained packed FMPL ferrocrete maps on structural feet',
        'gameplay_modified':False,'visual_approved':False})
    bpy.ops.wm.save_as_mainfile(filepath=str(out/'stone-water-wheel-v2.blend'),compress=True)
    bpy.ops.object.select_all(action='DESELECT')
    for obj in base.MODEL.objects:
        obj.select_set(True)
    bpy.ops.export_scene.gltf(filepath=str(out/'stone-water-wheel-v2.glb'),export_format='GLB',use_selection=True,
        export_cameras=False,export_lights=False,export_animations=True,export_animation_mode='SCENE',
        export_frame_range=True,export_force_sampling=True,export_frame_step=6,export_apply=True,export_extras=True)
    return scene,profile

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--source',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True)
    p.add_argument('--fmpl-tools',type=Path,required=True)
    args=p.parse_args(sys.argv[sys.argv.index('--')+1:])
    args.source=args.source.resolve()
    out=args.out.resolve()
    if out.exists():raise FileExistsError(out)
    out.mkdir(parents=True)
    sys.path.insert(0,str(args.fmpl_tools.resolve()))
    scene,profile=rebuild(args,out)
    base.render(scene,profile,out,False)

if __name__=='__main__':
    main()
