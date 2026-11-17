"""Refine the saved wheel into an upright-bucket shoreline intake; candidate only."""
import bpy,bmesh,json,math,hashlib,sys,tempfile,argparse,importlib.util
from pathlib import Path
from mathutils import Vector
import numpy as np
H=Path(__file__).resolve().parent;R=H.parents[3]
p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);O=a.out.resolve()
if O.exists():raise FileExistsError(O)
O.mkdir(parents=True);tempfile.tempdir=str(R/'build/quarry-export-temp')
sys.path.insert(0,str(R/'models/island-survival/primitive-steam-powered-pump/v3'));sys.path.insert(0,str(R.parent/'model-production/tools/fmpl'))
from mesh_util import box,cylinder,tube,mesh
import surfaces
from blender_camera_guard import install_canonical_camera,assert_clean,temporary_inspection_camera
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
P=H.parent/'candidates/v2-pilot02/stone-water-wheel-v2.blend';assert sha(P)=='7b58b52cc244e901035adf8fc7ffac2c8c0cc6f3f465ae01a3a6388bebe2fe6b'
bpy.ops.wm.open_mainfile(filepath=str(P));s=bpy.context.scene;s.frame_set(1);root=bpy.data.objects['WHEEL | placement root'];wheel=bpy.data.objects['WHEEL | rotating scoop assembly'];col=bpy.data.collections.new('V3 | upright bucket refinement');s.collection.children.link(col)
for o in tuple(root.children_recursive):
 if o.name.startswith(('V2 scoop','V2 receiver','V2 race')):bpy.data.objects.remove(o,do_unlink=True)
wood=bpy.data.materials['V2 | weathered structural oak grain by part'];endgrain=None
rng=np.random.default_rng(171803);u,v=np.meshgrid(np.linspace(0,1,512),np.linspace(0,1,512));broad=surfaces.field(rng,(512,512),.018);fine=surfaces.field(rng,(512,512),.22)
materials={}
for name,color,rough,metal in [('forged-wet-iron',(.105,.12,.115),.62,.80),('worn-bearing-bronze',(.36,.265,.11),.43,.72),('carried-river-water',(.055,.20,.235),.20,.05)]:
 detail=.012*broad+.003*fine;materials[name]=surfaces.material('stone-water-wheel-'+name,np.stack([c+detail for c in color],axis=-1),rough+.02*fine,.5+.008*broad+.004*fine,metal,O)
iron=materials['forged-wet-iron'];bronze=materials['worn-bearing-bronze'];water=materials['carried-river-water']
for o in root.children_recursive:
 if o.type=='MESH':
  for i,m in enumerate(o.data.materials):
   if m and ('forged' in m.name or 'iron' in m.name):o.data.materials[i]=iron
   elif m and 'bronze' in m.name:o.data.materials[i]=bronze
for m in (wood,iron,bronze,water):m['surface_authorship']='Stone Water Wheel V3: retained saved curved-rim/pier image surfacing, physically aligned oak on fitted upright buckets and receiver; new model-specific wet forged iron, bearing bronze and carried-water albedo/roughness/normal maps.'
def E(n,parent=root,p=(0,0,0)):
 o=bpy.data.objects.new('V3 | '+n,None);col.objects.link(o);o.parent=parent;o.location=p;return o
def B(n,p,d,m=wood,parent=root,bevel=.003):
 o=box('V3 | '+n,p,d,m,col,parent,bevel);surfaces.physical_box_uv(o);return o
def C(n,p,r,d,m=iron,axis='X',parent=root):
 o=cylinder('V3 | '+n,p,r,d,m,col,parent,axis,40);surfaces.physical_box_uv(o);return o
def ring(n,p,outer,inner,depth,m=bronze,parent=root,axis='X'):
 o=tube('V3 | '+n,[(Vector((0,0,-depth/2)),Vector((0,0,1)),outer,inner),(Vector((0,0,depth/2)),Vector((0,0,1)),outer,inner)],m,col,parent,40);o.location=p
 if axis=='X':o.rotation_euler.y=math.pi/2
 if axis=='Y':o.rotation_euler.x=math.pi/2
 surfaces.physical_box_uv(o);return o
def beam(n,start,end,w,m=wood,parent=root):
 x,y=Vector(start),Vector(end);o=B(n,(x+y)/2,(w,w,(y-x).length),m,parent);o.rotation_euler=(y-x).to_track_quat('Z','Y').to_euler();return o
def bore(o,p,r,d,axis='X'):
 cut=C('temporary real bore',p,r,d,iron,axis,o.parent);bpy.context.view_layer.update();bpy.context.view_layer.objects.active=o;mod=o.modifiers.new('Real fitted opening','BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=cut;bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cut,do_unlink=True)
def lin(o):
 if o.animation_data and o.animation_data.action:
  for layer in o.animation_data.action.layers:
   for strip in layer.strips:
    for bag in strip.channelbags:
     for curve in bag.fcurves:
      for key in curve.keyframe_points:key.interpolation='LINEAR'
def lift(angle):
 dist=abs(math.atan2(math.sin(angle-math.pi/2),math.cos(angle-math.pi/2)));return .055*max(0,1-dist/.20)
# Preserve the measured fixed full-size collar/throat and all useful V2 rim,
# spokes, axle, hollow bearings and stone support geometry.
wheel.animation_data_clear();wheel.rotation_euler=(0,0,0);wheel.location=(0,.47,.65)
buckets=[]
for i in range(8):
 phase=i*math.tau/8;py=.47*math.cos(phase);pz=.47*math.sin(phase)
 C('bucket %02d fixed through pivot'%i,(0,py,pz),.009,.44,iron,parent=wheel)
 bucket=E('bucket %02d independently upright'%i,wheel,(0,py,pz));bucket['mechanism']='Gravity-hung independent pivot; fixed world upright at every key. Lower body COM below pivot.';buckets.append(bucket)
 for sign in (-1,1):
  ring('bucket %02d bored hanging eye'%i,(sign*.130,0,0),.019,.0105,.018,bronze,bucket)
  B('bucket %02d seated hanger'%i,(sign*.130,0,-.082),(.013,.024,.13),iron,bucket)
  wall=B('bucket %02d closed end wall'%i,(sign*.130,0,-.110),(.014,.16,.13),wood,bucket)
  if sign==-1:bore(wall,(-.130,.05,-.140),.012,.07)
 for yy in (-.075,.075):
  for j in range(3):B('bucket %02d horizontal stave'%i,(0,yy,-.066-j*.043),(.246,.014,.041),wood,bucket)
 B('bucket %02d retained floor'%i,(0,0,-.180),(.276,.164,.018),wood,bucket)
 for yy in (-.085,.085):B('bucket %02d fitted hoop'%i,(0,yy,-.135),(.276,.008,.018),iron,bucket)
 ring('bucket %02d side drain sleeve'%i,(-.143,.05,-.140),.016,.012,.024,bronze,bucket)
 gate=E('bucket %02d gravity return drain gate'%i,bucket)
 B('bucket %02d sliding gate plate'%i,(-.1585,.05,-.140),(.007,.038,.034),iron,gate)
 B('bucket %02d gate lift rod'%i,(-.165,.05,-.016),(.006,.009,.24),iron,gate)
 C('bucket %02d cam follower roller'%i,(-.158,.05,.108),.012,.018,bronze,parent=gate)
 B('bucket %02d rod retained cleat'%i,(-.163,.05,-.126),(.012,.016,.015),iron,gate)
 for z in (-.060,.035):
  # Real open guide, rather than a solid block crossing the translating rod.
  for yy in (.038,.062):B('bucket %02d rod guide cheek'%i,(-.165,yy,z),(.018,.008,.014),bronze,bucket)
 surface=B('bucket %02d carried water'%i,(0,0,-.066),(.240,.132,.006),water,bucket,.001)
 jet=C('bucket %02d short draining water'%i,(-.245,.05,-.143),.006,.190,water,parent=bucket)
 drop=C('bucket %02d falling drain water'%i,(-.337,.05,-.163),.006,.040,water,'Z',bucket)
 for f in range(1,194):
  theta=-math.tau*(f-1)/192;angle=phase+theta
  bucket.rotation_euler.x=-theta;bucket.keyframe_insert(data_path='rotation_euler',frame=f)
  gate.location.z=lift(angle);gate.keyframe_insert(data_path='location',frame=f)
  dist=abs(math.atan2(math.sin(angle-math.pi/2),math.cos(angle-math.pi/2)))
  # Fill at the submerged bottom; retain through the rising/front half; drain
  # through the controlled side gate at the top while remaining upright.
  aa=angle%math.tau;filled=math.pi/2+.10<aa<5.50
  surface.scale=(1,1,1) if filled else (.001,.001,.001);surface.keyframe_insert(data_path='scale',frame=f)
  jet.scale=(1,1,1) if dist<.08 else (.001,.001,.001);jet.keyframe_insert(data_path='scale',frame=f)
  drop.scale=jet.scale;drop.keyframe_insert(data_path='scale',frame=f)
 for o in (bucket,gate,surface,jet,drop):lin(o)
for f in range(1,194):
 wheel.rotation_euler.x=-math.tau*(f-1)/192;wheel.keyframe_insert(data_path='rotation_euler',frame=f)
lin(wheel)
# Water current acts on these low, rigid paddles; there is no invented engine.
for i in range(8):
 angle=i*math.tau/8+math.pi/8
 for sign in (-1,1):
  o=B('outboard current paddle',(sign*.27,.51*math.cos(angle),.51*math.sin(angle)),(.056,.060,.025),wood,wheel);o.rotation_euler.x=angle
  beam('current paddle seated stub',(sign*.21,.51*math.cos(angle),.51*math.sin(angle)),(sign*.27,.51*math.cos(angle),.51*math.sin(angle)),.027,iron,wheel)
# Fixed cam track follows the follower path and lifts the drain only at the top.
for k in range(20):
 aa=math.pi/2-.22+k*.44/20;bb=math.pi/2-.22+(k+1)*.44/20
 def follower(t):return (-.158,.47+.47*math.cos(t)+.05,.65+.47*math.sin(t)+.108+lift(t)+.012)
 beam('fixed drain cam contact rail',follower(aa),follower(bb),.009,iron)
beam('cam over-wheel mounting bridge',(-.46,.52,1.38),(-.158,.52,1.38),.032,iron)
beam('cam fixed suspended bracket',(-.158,.52,1.38),(-.158,.52,1.298),.025,iron)
beam('cam founded upright',(-.46,.68,.57),(-.46,.68,1.38),.035,iron)
beam('cam bridge diagonal',(-.46,.68,1.38),(-.46,.52,1.38),.032,iron)
# Closed, watertight plank receiver with one correctly bored front mounting wall.
B('receiver grounded sole',(0,-.27,.035),(.68,.30,.07))
front=B('receiver monolithic fitted front',(0,-.399,.385),(.68,.03,.66));bore(front,(0,-.399,.36),.287,.09,'Y')
B('receiver closed rear',(0,-.135,.385),(.68,.03,.66))
for x in (-.323,.323):B('receiver fitted side',(x,-.267,.385),(.034,.264,.66))
B('receiver sealed floor',(0,-.267,.070),(.62,.234,.020))
for x in (-.345,.345):
 B('receiver corner iron angle',(x,-.399,.385),(.018,.033,.68),iron)
 for z in (.10,.68):C('receiver retained corner fastener',(x,-.424,z),.011,.026,bronze,'Y')
B('receiver contained water',(0,-.267,.54),(.607,.226,.009),water,bevel=.001)
# Flared capture race outside the left rim receives the top side-drain jet.
path=[(-.36,.52,.94),(-.42,.10,.82),(-.42,-.21,.75),(-.21,-.27,.73)]
for i,(start,end) in enumerate(zip(path,path[1:])):
 av,bv=Vector(start),Vector(end);across=Vector((-(bv-av).y,(bv-av).x,0)).normalized()
 def strip(name,offset,width,thickness,mat,zshift=0):
  corners=[av+across*(offset-width/2),av+across*(offset+width/2),bv+across*(offset+width/2),bv+across*(offset-width/2)]
  verts=[tuple(q+Vector((0,0,zshift+z))) for z in (-thickness/2,thickness/2) for q in corners]
  o=mesh('V3 | '+name,verts,[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],mat,col,root);surfaces.physical_box_uv(o);return o
 strip('joined sloping race bed',0,.14,.020,wood)
 for sign in (-1,1):strip('joined race side',sign*.077,.014,.060,wood,.024)
 strip('shallow water along race',0,.125,.006,water,.014)
B('flared side jet capture bed',(-.36,.52,.94),(.10,.24,.02))
for yy in (.648,):B('jet capture raised end',(-.36,yy,.97),(.10,.016,.07))
B('jet capture outer back',(-.417,.57,.97),(.014,.17,.07))
for xx,yy,zz in ((-.42,.10,.79),(-.42,-.21,.72),(-.21,-.27,.70)):
 beam('race vertical founded support',(xx,yy,.055),(xx,yy,zz),.045)
 beam('race diagonal support',(xx,yy,.30),(xx+.05,yy+.07,zz-.02),.027)
# Freeze real geometry and remove the known boolean zero-area remnants.
for o in root.children_recursive:
 if o.type!='MESH':continue
 if o.modifiers:
  o.data=bpy.data.meshes.new_from_object(o.evaluated_get(bpy.context.evaluated_depsgraph_get()));o.modifiers.clear()
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.triangulate(bm,faces=list(bm.faces));bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-7);bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=1e-7);bmesh.ops.delete(bm,geom=[x for x in bm.verts if not x.link_faces],context='VERTS');bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free();o.data.calc_loop_triangles();bad={t.polygon_index for t in o.data.loop_triangles if t.area<1e-12}
 if bad:
  bm=bmesh.new();bm.from_mesh(o.data);bm.faces.ensure_lookup_table();bmesh.ops.delete(bm,geom=[bm.faces[i] for i in bad],context='FACES');bm.to_mesh(o.data);bm.free()
 if not o.data.uv_layers:surfaces.physical_box_uv(o)
s.frame_start=1;s.frame_end=193;s.render.fps=48;s.frame_set(1);s['asset_stem']='stone-water-wheel-v3';s['shoreline_waterline']=.25;s['visual_status']='V3 candidate: upright buckets, controlled side discharge and supported collector, not yet promoted';s['surface_plan']='Retained physically authored curved oak and bedded masonry images; fitted bucket staves/receiver/race grain, new wet iron and worn bronze maps. Water distinct from structure.'
profile=json.loads((P.parent/'capture-profile.json').read_text());profile['source_size']=256;profile['states']={'idle':[1],'working':list(range(1,194,12))[:16]};profile['camera_override'].update(target=[0,0,.62],ortho_scale=3.3)
install_canonical_camera(s,profile,bpy);s.render.resolution_x=s.render.resolution_y=256;s.cycles.samples=32;s.render.film_transparent=True;s.render.image_settings.color_mode='RGBA';assert_clean(s,profile,bpy)
bpy.ops.file.pack_all();native=O/'stone-water-wheel-v3.blend';bpy.ops.wm.save_as_mainfile(filepath=str(native),compress=True);bpy.ops.wm.open_mainfile(filepath=str(native));s=bpy.context.scene;root=bpy.data.objects['WHEEL | placement root'];bpy.ops.object.select_all(action='DESELECT')
for o in [root,*root.children_recursive]:o.select_set(True)
bpy.ops.export_scene.gltf(filepath=str(O/'stone-water-wheel-v3.glb'),export_format='GLB',use_selection=True,export_cameras=False,export_lights=False,export_animations=True,export_animation_mode='SCENE',export_anim_scene_split_object=False,export_frame_range=True,export_force_sampling=True,export_frame_step=1,export_apply=True,export_extras=True)
(O/'capture-profile.json').write_text(json.dumps(profile,indent=2)+'\n');(O/'construction-receipt.json').write_text(json.dumps(dict(parent_source_sha256=sha(P),source_sha256=sha(native),runtime_sha256=sha(O/'stone-water-wheel-v3.glb'),preserved='Curved fitted rim, spokes, axle, hollow bearings, masonry piers and exact stationary collar/throat',upright_buckets=8,mechanism='Gravity-hung independent pivots with fixed cam lifted drain gates; river-current paddles; short top side jet into supported collection race',native_integrated=False,owner_visual_approved=False),indent=2)+'\n')
projection=bpy.data.objects.new('SPRITE ONLY | square ground correction',None);s.collection.objects.link(projection);projection.scale.y=math.sqrt(2);root.parent=projection;s.render.resolution_x=s.render.resolution_y=512
for name,yaw in [('front',0),('rear',180),('side',90)]:
 root.rotation_euler.z=math.radians(yaw);s.render.filepath=str(O/(name+'-review512.png'));bpy.ops.render.render(write_still=True)
root.rotation_euler.z=0
with temporary_inspection_camera(s,bpy,'Upright bucket eyes and fixed cam') as camera:
 target=Vector((0,.47*math.sqrt(2),.88));camera.data.type='ORTHO';camera.data.ortho_scale=1.60;camera.location=target+Vector((-2,-2,1.3));camera.rotation_euler=(target-camera.location).to_track_quat('-Z','Y').to_euler();s.camera=camera;s.render.filepath=str(O/'bucket-cam-close512.png');bpy.ops.render.render(write_still=True)
print('WHEEL_V3_SAVED_REOPENED_EXPORTED',sha(native),flush=True)
