"""Native V6 -> V7 bucket / wheel clearance and authored splash refinement.

blender -b V6.blend --python refine_buckets.py -- --out DIR
No game data, atlas production or fluid simulation is performed.
"""
import argparse, hashlib, json, math, sys
from pathlib import Path
import bpy, bmesh
from mathutils import Vector

ap=argparse.ArgumentParser()
ap.add_argument('--out',type=Path,required=True)
args=ap.parse_args(sys.argv[sys.argv.index('--')+1:])
out=args.out.resolve();out.mkdir(parents=True,exist_ok=True)
s=bpy.context.scene
root=bpy.data.objects['EXPORT | rotate beachpump not camera']
root.rotation_euler.z=0;s.frame_set(1)
ports=[o for o in bpy.data.objects if o.name.startswith('PORT |')]
def port_points():
    bpy.context.view_layer.update()
    return [tuple(o.matrix_world@v.co) for o in ports for v in o.data.vertices]
original_ports=port_points()
wheel=bpy.data.objects['MOTION | full bucket waterwheel shaft']
old=sorted([o for o in bpy.data.objects if o.name.startswith('WHEEL | cupped tapered paddle')],key=lambda o:o.name)
assert len(old)==8
col=old[0].users_collection[0];wood=old[0].data.materials[0]
for o in old:bpy.data.objects.remove(o,do_unlink=True)

def mesh_object(name,vertices,faces,mat,parent=wheel,bevel=.002):
    mesh=bpy.data.meshes.new(name+' mesh');mesh.from_pydata(vertices,[],faces);mesh.update()
    bm=bmesh.new();bm.from_mesh(mesh);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(mesh);bm.free()
    ob=bpy.data.objects.new(name,mesh);col.objects.link(ob);ob.parent=parent;mesh.materials.append(mat)
    if bevel:
        m=ob.modifiers.new('Small worn edge bevel','BEVEL');m.width=bevel;m.segments=3
        ob.modifiers.new('Solid timber normals','WEIGHTED_NORMAL')
    return ob

def extrude_profile(name,profile,x0,x1,angle,mat):
    # Profile is in tangential / radial coordinates, extruded along the axle.
    n=len(profile);cs=math.cos(angle);sn=math.sin(angle)
    verts=[(x,r*cs-t*sn,r*sn+t*cs) for x in (x0,x1) for t,r in profile]
    faces=[tuple(reversed(range(n))),tuple(n+j for j in range(n))]
    faces += [(j,(j+1)%n,(j+1)%n+n,j+n) for j in range(n)]
    return mesh_object(name,verts,faces,mat)

# Cup interiors face radially outward. A real 18 mm wall separates the water
# cavity from the rim/spokes. Side cheeks close the trough ends, not the mouth.
count=12
outer=[(-.084+.168*j/count,.274+.039*((-.084+.168*j/count)/.084)**2) for j in range(count+1)]
inner=[(t,r+.018) for t,r in outer]
shell=outer+list(reversed(inner))
cup_checks=[]
for k in range(8):
    a=2*math.pi*k/8
    body=extrude_profile(f'WHEEL | V7 solid bucket shell {k:02d}',shell,-.120,.120,a,wood)
    body['wall_thickness_bu']=.018
    # Fill the U-shaped end profile up to its lip with full wooden cheek walls.
    end_profile=inner+[(inner[-1][0],.342),(inner[0][0],.342)]
    for side,x0,x1 in [('left',-.120,-.102),('right',.102,.120)]:
        extrude_profile(f'WHEEL | V7 closed bucket end {k:02d} {side}',end_profile,x0,x1,a,wood)
    cup_checks.append(body.name)

# Keep structural rings entirely outside the bucket end walls. Old rings had
# x=+/-0.068 inside the 0.240-wide buckets, exposing timber through the cavities.
rings=[o for o in bpy.data.objects if o.name.startswith('WHEEL | thinner rounded timber rim')]
assert len(rings)==2
for o in rings:
    o.location.x=math.copysign(.153,o.location.x)
    o.scale=(.82,.82,.82)
    o['outside_bucket_end_wall']=True
# Preserve the axle location in XY, reduce only excess radius to clear the gutter.
wheel.scale=(.96,1.15,1.15);wheel.location.z=.92
for o in bpy.data.objects:
    if o.name.startswith(('CRANK |','WHEEL | asymmetrical bright')) and o.parent==wheel:
        o.location.x+=.100
fixed=bpy.data.objects['WHEEL | fixed axle support'];fixed.location.z-=.05
for o in bpy.data.objects:
    if o.name.startswith('WHEEL | fixed timber bearing frame'):
        # Rod's lower end stays anchored; shift its upper end down to the axle.
        axis=o.rotation_euler.to_matrix()@Vector((0,0,1))
        half=(max(v.co.z for v in o.data.vertices)-min(v.co.z for v in o.data.vertices))*o.scale.z/2
        ends=[o.location-axis*half,o.location+axis*half]
        high=max(range(2),key=lambda i:ends[i].z);ends[high].z-=.05
        d=ends[1]-ends[0];o.location=(ends[0]+ends[1])/2
        o.rotation_euler=d.to_track_quat('Z','Y').to_euler()
        o.scale.z*=d.length/(2*half)
drive=bpy.data.objects['DRIVE | exposed rigid wheel-to-screw gearbox input']
def replace_rod(ob,a,b,radius):
    a,b=Vector(a),Vector(b);d=b-a
    bpy.ops.mesh.primitive_cylinder_add(vertices=32,radius=radius,depth=d.length)
    temp=bpy.context.object;mat=ob.data.materials[0]
    ob.data=temp.data.copy();ob.data.materials.append(mat)
    bpy.data.objects.remove(temp,do_unlink=True)
    ob.location=(a+b)/2;ob.rotation_euler=d.to_track_quat('Z','Y').to_euler();ob.scale=(1,1,1)
replace_rod(drive,(.23,-.13,.93),(-.08,.085,1.36),.058)
# The outward crank needs a continuous visible axle from hub to lever.
bpy.ops.mesh.primitive_cylinder_add(vertices=32,radius=.043,depth=.19)
axle=bpy.context.object
for c in tuple(axle.users_collection):c.objects.unlink(axle)
col.objects.link(axle);axle.parent=wheel
axle.name='WHEEL | V7 continuous outer crank axle'
axle.location=(.145,0,0);axle.rotation_euler=(0,math.pi/2,0)
axle.data.materials.append(bpy.data.materials['BEACH | black wet forged iron'])
# Lower catch-pan bottom to leave the bucket lips clear at the lowest rotation.
bpy.data.objects['SUMP | wood catch basin underneath wheel'].location.z-=.045
bpy.data.objects['SUMP | blue-green collected flow'].location.z-=.025

water=bpy.data.materials['BEACH V6 | clear shallow seawater']
foam=bpy.data.materials.new('BEACH V7 | aerated splash highlights');foam.use_nodes=True
bs=foam.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(.52,.79,.75,1)
bs.inputs['Roughness'].default_value=.24;bs.inputs['Transmission Weight'].default_value=.25

def curve_object(name,pts,radius,mat,parent=root):
    curve=bpy.data.curves.new(name,'CURVE');curve.dimensions='3D';curve.resolution_u=12
    curve.bevel_depth=radius;curve.bevel_resolution=3
    poly=curve.splines.new('POLY');poly.points.add(len(pts)-1)
    for p,co in zip(poly.points,pts):p.co=(*co,1)
    ob=bpy.data.objects.new(name,curve);col.objects.link(ob);ob.parent=parent;curve.materials.append(mat)
    return ob

oldspill=bpy.data.objects['WATER | uninterrupted trough-to-wheel falling sheet']
bpy.data.objects.remove(oldspill,do_unlink=True)
start=Vector((.225,-.105,1.398));impact=Vector((.255,-.100,1.290))
verts=[]
for j in range(17):
    t=j/16;c=start.lerp(impact,t);c.y-=.012*math.sin(math.pi*t)
    width=.053*(1-.20*t)
    verts.extend([tuple(c+Vector((-width,0,0))),tuple(c+Vector((width,0,0)))])
spill=mesh_object('WATER | V7 trough to upper bucket connected falling sheet',verts,
                  [(2*j,2*j+1,2*j+3,2*j+2) for j in range(16)],water,root,0)
solid=spill.modifiers.new('Water film thickness','SOLIDIFY');solid.thickness=.002

splash_objects=[spill]
# Tiny ballistic droplets start at the actual impact, taper out before return,
# and are hidden in idle. No large decorative blue balls.
for i in range(24):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2,radius=1)
    ob=bpy.context.object;ob.name=f'WATER | V7 impact spray droplet {i:02d}';ob.parent=root
    for c in tuple(ob.users_collection):c.objects.unlink(ob)
    col.objects.link(ob);ob.data.materials.append(foam if i%3==0 else water)
    for poly in ob.data.polygons:poly.use_smooth=True
    ang=i*2.399963;speed=.11+.025*(i%4)
    velocity=Vector((speed*math.cos(ang),speed*math.sin(ang),.20+.035*(i%5)))
    for fr in range(1,98,3):
        t=(((fr-1)/96*4+i/24)%1)
        ob.location=impact+velocity*t+Vector((0,0,-.38*t*t))
        size=(.006+.002*(i%3))*math.sin(math.pi*t)**.45
        ob.scale=(size,size,size*1.65)
        ob.keyframe_insert('location',frame=fr);ob.keyframe_insert('scale',frame=fr)
    splash_objects.append(ob)

# Short broken curtains drain from the lower passing buckets into the catch pan.
for i in range(7):
    x=.18+i*.026
    pts=[(x,-.15+.016*math.sin(j*.8+i),.64-j*.012) for j in range(9)]
    ob=curve_object(f'WATER | V7 bucket runoff thread {i:02d}',pts,.0035,water)
    for fr in range(1,98,3):
        ob.location.z=.009*math.sin(2*math.pi*((fr-1)/24+i/7))
        ob.keyframe_insert('location',frame=fr)
    splash_objects.append(ob)
for i in range(4):
    pts=[(.26+(.035+i*.012)*math.cos(j*math.pi/14),
          -.15+(.035+i*.012)*math.sin(j*math.pi/14),.550) for j in range(29)]
    ob=curve_object(f'WATER | V7 small catch-pan foam ripple {i:02d}',pts,.0025,foam)
    splash_objects.append(ob)

# Four restrained impact fingers give the spray a connected splash silhouette.
for i in range(4):
    ang=i*math.pi/2+.4
    pts=[tuple(impact+Vector((.062*math.cos(ang)*j/10,.062*math.sin(ang)*j/10,
                              .034*math.sin(math.pi*j/10)))) for j in range(11)]
    ob=curve_object(f'WATER | V7 impact crown finger {i:02d}',pts,.003,foam)
    splash_objects.append(ob)

for o in splash_objects:
    for fr,hidden in ((0,True),(1,False),(97,False)):
        o.hide_render=hidden;o.keyframe_insert('hide_render',frame=fr)

s['source_model']='Beach Pump V7 solid bucket troughs and impact splash review'
s['water_simulation']='authored ballistic droplets, runoff curves and water sheet'
s['game_integrated']=False;s['human_visual_approved']=False
s.frame_set(25);bpy.context.view_layer.update()
assert port_points()==original_ports
report={'blender':bpy.app.version_string,'bucket_shells':8,'closed_end_walls':16,
        'bucket_axial_half_width':.120,'rim_axial_center':.153,
        'rim_axial_outer_radius':.026*.82,'rim_bucket_axial_gap':.153-.026*.82-.120,
        'solid_bucket_bottoms':True,'impact_droplets':24,'runoff_threads':7,
        'idle_splash_hidden':True,'port_vertices_unchanged':True,
        'game_integrated':False,'human_visual_approved':False}
assert report['rim_bucket_axial_gap']>.01
for ob in [o for o in bpy.data.objects if o.name.startswith(('WHEEL | V7 solid bucket','WHEEL | V7 closed bucket'))]:
    bm=bmesh.new();bm.from_mesh(ob.data)
    assert all(e.is_manifold for e in bm.edges),ob.name
    bm.free()
report['all_24_bucket_wall_meshes_manifold']=True

s.render.engine='CYCLES';s.cycles.samples=32;s.cycles.use_denoising=True
s.render.resolution_x=s.render.resolution_y=768;s.render.resolution_percentage=100
s.render.threads_mode='FIXED';s.render.threads=8;s.camera.data.ortho_scale=2.75
root.rotation_euler.z=math.radians(-45)
bpy.ops.wm.save_as_mainfile(filepath=str(out/'beach-pump-v7-review.blend'),compress=True)
def render(name):
    s.render.filepath=str(out/name);bpy.ops.render.render(write_still=True)
render('v7-review.png')
# Close view of the corrected buckets, using the same 45-degree camera elevation.
oldcam=s.camera.location.copy();oldscale=s.camera.data.ortho_scale
target=root.matrix_world@Vector((.26,-.13,1.02))
s.camera.location=target+Vector((0,-6,6));s.camera.data.ortho_scale=1.42
render('v7-buckets-closeup.png')
s.render.resolution_x=s.render.resolution_y=448;s.cycles.samples=16
for i,fr in enumerate(range(1,97,6)):
    s.frame_set(fr);render(f'close-frame-{i:02d}.png')
s.camera.location=oldcam;s.camera.data.ortho_scale=oldscale
for i,fr in enumerate(range(1,97,6)):
    s.frame_set(fr);render(f'frame-{i:02d}.png')
report['native_sha256']=hashlib.sha256((out/'beach-pump-v7-review.blend').read_bytes()).hexdigest()
(out/'build-review.json').write_text(json.dumps(report,indent=2)+'\n')
print('V7_BUCKETS_RENDERED',json.dumps(report),flush=True)
