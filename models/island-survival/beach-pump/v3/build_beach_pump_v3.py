#!/usr/bin/env python3
"""Beach Pump V3 — real native Blender refinement of immutable V2, not generated imagery."""
from __future__ import annotations
import argparse,hashlib,importlib.util,json,math,sys
from pathlib import Path

HERE=Path(__file__).resolve().parent
V2=HERE.parent/"v2"/"build_beach_pump_v2.py"
spec=importlib.util.spec_from_file_location("beach_pump_v2_locked",V2)
v2=importlib.util.module_from_spec(spec)
sys.modules[spec.name]=v2
spec.loader.exec_module(v2)
OLD_CONSTRUCT=v2.construct

def cupped_bucket(bpy,name,angle,material,collection,parent):
    """Twenty-vertex hollow wooden scoop: 8 individually rotated real 3D meshes."""
    cs,sn=math.cos(angle),math.sin(angle)
    section=((-0.076,.314),(-.038,.285),(0.,.272),(.038,.285),(.076,.314))
    verts=[]
    for inset in (0.,.019):
        for x in (-.111,.111):
            for t,r in section:
                radius=r-inset
                verts.append((x,radius*cs-t*sn,radius*sn+t*cs))
    faces=[]
    for i in range(4):
        faces.extend(((i,i+1,i+6,i+5),
                      (i+10,i+15,i+16,i+11),
                      (i,i+10,i+11,i+1),
                      (i+5,i+6,i+16,i+15)))
    faces.extend(((0,5,15,10),(4,14,19,9)))
    mesh=bpy.data.meshes.new(name+" - concave wooden profile")
    mesh.from_pydata(verts,[],faces)
    mesh.update()
    ob=bpy.data.objects.new(name,mesh)
    collection.objects.link(ob)
    ob.parent=parent
    ob.data.materials.append(material)
    mod=ob.modifiers.new("Soft hand-worn curved lip","BEVEL")
    mod.width=.007
    mod.segments=3
    ob.modifiers.new("Soft handmade normals","WEIGHTED_NORMAL")
    ob["editable_curved_bucket"]=True
    return ob

def real_water_surface(bpy,a,b,material,collection,root):
    from mathutils import Vector
    a,b=Vector(a),Vector(b)
    sideways=Vector((-(b-a).y,(b-a).x,0)).normalized()
    verts=[]
    for j in range(25):
        t=j/24
        center=a.lerp(b,t)+Vector((0,0,.052+.0038*math.sin(6*math.pi*t)))
        for sign in (-1,1):
            width=.073*(.90+.09*math.sin(math.pi*t))
            verts.append(tuple(center+sideways*width*sign))
    mesh=bpy.data.meshes.new("Thin continuous ripple surface")
    mesh.from_pydata(verts,[],[(2*j,2*j+1,2*j+3,2*j+2) for j in range(24)])
    mesh.update()
    ob=bpy.data.objects.new("TROUGH | clearly visible blue-green water ribbon",mesh)
    collection.objects.link(ob)
    ob.parent=root
    ob.data.materials.append(material)
    ob["real_surface_not_cylinder"]=True
    return ob

def smooth_action(bpy,obj):
    data=obj.animation_data
    if not data or not data.action:return 0
    action=data.action
    curves=list(getattr(action,"fcurves",()) or ())
    for layer in getattr(action,"layers",()):
        for strip in getattr(layer,"strips",()):
            for bag in getattr(strip,"channelbags",()):
                curves.extend(getattr(bag,"fcurves",()))
    seen=set();changed=0
    for curve in curves:
        identity=curve.as_pointer()
        if identity in seen:continue
        seen.add(identity)
        for p in curve.keyframe_points:
            p.interpolation="LINEAR"
            changed+=1
    return changed

def refine_construct(bpy,v1,contract,original,root,ports):
    from mathutils import Vector
    result=OLD_CONSTRUCT(bpy,v1,contract,original,root,ports)
    water=bpy.data.materials["BEACH | bright visibly blue-green moving water"]
    # A dense eight-board dock and rectangular wheel buckets dominated V2.
    boards=sorted((o for o in bpy.data.objects if o.name.startswith("DOCK | narrow separated driftwood plank")),key=lambda o:o.name)
    if len(boards)!=8:raise RuntimeError("Unexpected V2 dock reference, no silent reconstruction")
    for index in (1,3,5):bpy.data.objects.remove(boards[index],do_unlink=True)
    wheel=bpy.data.objects["MOTION | full bucket waterwheel shaft"]
    rotor=bpy.data.objects["MOTION | keyed Archimedes screw rotation"]
    old_buckets=sorted((o for o in bpy.data.objects if o.name.startswith("WHEEL | chunky bucket paddle")),key=lambda o:o.name)
    if len(old_buckets)!=8:raise RuntimeError("Original V2 wheel paddle count changed")
    collection=old_buckets[0].users_collection[0]
    wood=old_buckets[0].data.materials[0]
    for ob in old_buckets:bpy.data.objects.remove(ob,do_unlink=True)
    for k in range(8):
        cupped_bucket(bpy,f"WHEEL | cupped tapered paddle {k:02d}",
                      k*2*math.pi/8,wood,collection,wheel)
    for ob in bpy.data.objects:
        if ob.name.startswith("WHEEL | 3D timber rim"):
            ob.scale=(1.1,1.1,1.1)
            ob.name=ob.name.replace("3D timber rim","thinner rounded timber rim")
        elif ob.name.startswith("WHEEL | broad brass hub"):
            ob.scale=(.79,.79,.79)
            ob.name="WHEEL | compact forged bronze bearing"
        elif ob.name.startswith("DRIVE | massive bronze right angle bevel housing"):
            ob.scale=(.70,.70,.70)
            ob.name="DRIVE | reduced exposed bevel bearing"
    # The blue tube in the discharge gutter read as rigid piping rather than flow.
    old=bpy.data.objects["TROUGH | clearly visible blue-green water ribbon"]
    col=old.users_collection[0]
    bpy.data.objects.remove(old,do_unlink=True)
    a=Vector((-.19,.085,1.385))
    b=Vector((.225,-.105,1.345))
    real_water_surface(bpy,a,b,water,col,root)
    seafoam=v1.material(bpy,"pale mobile foam highlights",(.28,.74,.70,1),.24,.05,.03)
    glints=[]
    for i in range(4):
        bpy.ops.mesh.primitive_uv_sphere_add(segments=16,ring_count=8,radius=.013)
        glint=v1.move(bpy,bpy.context.object,col,root)
        glint.name=f"WATER | running stream glint {i:02d}"
        glint.data.materials.append(seafoam)
        glints.append(glint)
    # Replace obvious stacked cylinders with softer true fluid lenses while
    # retaining the original animation paths on the exact same objects.
    fluid_mesh_replacements=0
    for ob in tuple(bpy.data.objects):
        if not (ob.name.startswith("WATER | cascading trough-wheel spill") or
                ob.name.startswith("WATER | visibly rising screw pocket")):continue
        bpy.ops.mesh.primitive_uv_sphere_add(segments=20,ring_count=12,radius=.045)
        sphere=bpy.context.object
        mesh=sphere.data.copy()
        for mat in ob.data.materials:mesh.materials.append(mat)
        ob.data=mesh
        bpy.data.objects.remove(sphere,do_unlink=True)
        fluid_mesh_replacements+=1
    helix=bpy.data.objects["SCREW | exposed 3-turn bronze helical flight"]
    trim_points=[]
    length=result["length_bu"]
    for j in range(145):
        f=j/144
        th=6*math.pi*f
        trim_points.append((.173*math.cos(th),.173*math.sin(th),
                            (f-.5)*(length-.11)+.018))
    flight_edge=v1.pipe(bpy,"SCREW | smooth rolled outer flight rim",
                        trim_points,.006,helix.data.materials[0],
                        helix.users_collection[0],rotor)
    flight_edge["rotates_with_screw"]=True
    droplets=[o for o in bpy.data.objects if o.name.startswith("WATER | cascading trough-wheel spill")]
    pockets=[o for o in bpy.data.objects if o.name.startswith("WATER | visibly rising screw pocket")]
    for k,frame in enumerate((*v2.FRAMES,v2.SEAM)):
        for i,pocket in enumerate(sorted(pockets,key=lambda x:x.name)):
            t=((k/16)+(i/6))%1
            pocket.scale=(.70,.70,max(.018,min(1.,t*10,(1-t)*10)))
            pocket.keyframe_insert(data_path="scale",frame=frame)
        for i,glint in enumerate(glints):
            t=((k/16)+(i/4))%1
            glint.location=a.lerp(b,t)+Vector((0,0,.068))
            glint.scale=(.91,.61,max(.02,math.sin(math.pi*t)))
            glint.keyframe_insert(data_path="location",frame=frame)
            glint.keyframe_insert(data_path="scale",frame=frame)
    linear=sum(smooth_action(bpy,o) for o in [rotor,wheel]+pockets+droplets+glints)
    if linear<30:raise RuntimeError("Continuous water and drive movement not linearly keyed")
    result.update(v3_refinement=True,cupped_mesh_buckets=8,remaining_dock_planks=5,
                  fluid_sphere_replacements=fluid_mesh_replacements,moving_water_glints=4,
                  linear_keyframes=linear)
    return result

def main():
    if "--self-check" in sys.argv:
        c,original,donor=v2.source()
        assert c["lock"]["water_per_tick"]==.01
        print("BEACH_PUMP_V3_DONOR_AND_NATIVE_CONTRACT_PASS",flush=True)
        return
    args=argparse.ArgumentParser()
    args.add_argument("--out",required=True,type=Path)
    args.add_argument("--render",choices=("none","proof","all"),default="all")
    args.add_argument("--samples",type=int,default=16)
    v= args.parse_args(sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else sys.argv[1:])
    if not 4<=v.samples<=64:raise ValueError("Cycles samples must be 4..64")
    v2.construct=refine_construct
    v2.build(v)
    import bpy
    root=bpy.data.objects["EXPORT | rotate beachpump not camera"]
    root.rotation_euler.z=0
    bpy.context.scene.frame_set(0)
    bpy.context.scene["source_model"]="Tanks beachpump V3: curved cups, open dock, moving water"
    bpy.context.scene["human_visual_approved"]=False
    bpy.context.scene["game_integrated"]=False
    native=v.out.resolve()/"beach-pump-v3.blend"
    bpy.ops.wm.save_as_mainfile(filepath=str(native),compress=True,check_existing=False)
    prev=v.out.resolve()/"beach-pump-v2.blend"
    if not prev.is_file():raise RuntimeError("Original in-process Blender master missing")
    prev.unlink()
    reportpath=v.out.resolve()/"build-report.json"
    report=json.loads(reportpath.read_text(encoding="utf-8"))
    report["schema"]="tanks.beach-pump.v3.archimedes-native-blender"
    report["native_sha256"]=hashlib.sha256(native.read_bytes()).hexdigest()
    report["visual_refinement"]="curved cupped buckets; reduced blocky deck; thin water and keyed glints"
    report["human_visual_approved"]=False
    report["game_integrated"]=False
    reportpath.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print("BEACH_PUMP_V3_REAL_EDITABLE_NATIVE_RENDER_PASS",
          report["render_count"],report["native_sha256"],flush=True)

if __name__=="__main__":
    main()
