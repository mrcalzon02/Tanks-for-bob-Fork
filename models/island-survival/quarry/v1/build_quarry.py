"""Refine the tracked quarry into a supported fuel-driven windlass and mineral working."""
import bpy,bmesh,json,math,sys,tempfile,hashlib
import numpy as np
from pathlib import Path
from mathutils import Vector
H=Path(__file__).resolve().parent;R=H.parents[3];O=R/'models/island-survival/quarry/candidates/v1-pilot01'
if O.exists():raise FileExistsError(O)
O.mkdir(parents=True);temp=R/'build/quarry-export-temp';temp.mkdir(exist_ok=True);tempfile.tempdir=str(temp)
sys.path.insert(0,str(R/'models/island-survival/primitive-steam-powered-pump/v3'))
from mesh_util import mesh,box,cylinder,tube
import surfaces
sys.path.insert(0,str(R.parent/'model-production/tools/fmpl'))
from blender_camera_guard import install_canonical_camera,assert_clean
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
starter=H/'starter-quarry.obj';contract=json.loads((H/'contract.json').read_text());assert sha(starter)==contract['source']['sha256']
bpy.ops.wm.read_factory_settings(use_empty=True);scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=32;scene.cycles.use_denoising=False;scene.render.film_transparent=True
scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA'
scene.world=bpy.data.worlds.new('Quarry neutral environment');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.22,.22,.22,1)
for pos,power,size in [((4,-4,7),700,5),((-4,2,5),450,4),((0,2,7),250,3)]:
 data=bpy.data.lights.new('Quarry area','AREA');data.energy=power;data.size=size;o=bpy.data.objects.new('Quarry area',data);scene.collection.objects.link(o);o.location=pos;o.rotation_euler=(Vector((0,0,.9))-o.location).to_track_quat('-Z','Y').to_euler()
root=bpy.data.objects.new('EXPORT | Quarry all authored parts',None);scene.collection.objects.link(root)
col=bpy.data.collections.new('QUARRY | excavated rock thermal drive and windlass');scene.collection.children.link(col)
m=surfaces.create(O)
rng=np.random.default_rng(171129);shape=(512,512);u,v=np.meshgrid(np.linspace(0,1,512),np.linspace(0,1,512))
broad=surfaces.field(rng,shape,.014);fine=surfaces.field(rng,shape,.16)
strata=np.sin(v*62+.55*np.sin(u*13)+.08*broad)
for name,tint,base in [('stone-face',(.97,1,.96),.32),('stone-bed',(.91,.94,.92),.22),('soil',(.85,.64,.40),.21),('iron-seam',(1,.48,.25),.25),('copper-seam',(.50,.82,.63),.26)]:
 tone=np.clip(base+.02*broad+.012*strata+.006*fine,.04,.55)
 color=np.stack([tone*t for t in tint],axis=-1)
 m[name]=surfaces.material('quarry-'+name,color,.86+.025*fine,.5+.04*strata+.025*broad,0,O)
weave=np.sin(u*math.tau*14+v*math.tau*4)*np.sin(u*math.tau*10-v*math.tau*5)
tone=.21+.022*weave+.008*fine
m['rope']=surfaces.material('quarry-twisted-hemp',np.stack([tone*1.3,tone,tone*.62],axis=-1),.91+.02*fine,.5+.045*weave,0,O)
for mat in m.values():mat.name=mat.name.replace('PUMP V3','QUARRY');mat['surface_authorship']='Quarry-specific rock strata/mineral traces, local timber fibers, cut ends, hemp braid and thermal drive roles'
def B(n,p,d,mat,parent=root,bevel=.006):
 o=box('QUARRY | '+n,p,d,mat,col,parent,bevel);surfaces.apply(o,mat,m['endgrain'] if mat==m['wood'] else None);return o
def C(n,p,r,d,mat,axis='Z',parent=root,segments=48):
 o=cylinder('QUARRY | '+n,p,r,d,mat,col,parent,axis,segments);surfaces.apply(o,mat);return o
def E(n,p=(0,0,0),parent=root):
 o=bpy.data.objects.new('QUARRY | '+n,None);col.objects.link(o);o.parent=parent;o.location=p;return o
def beam(n,a,b,width,mat=m['wood'],parent=root):
 a,b=Vector(a),Vector(b);o=B(n,(a+b)/2,(width,width,(b-a).length),mat,parent);o.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler();return o
def boolean(a,b,op):
 bpy.context.view_layer.objects.active=a;mod=a.modifiers.new('Authored connected excavation','BOOLEAN');mod.object=b;mod.operation=op;mod.solver='EXACT';bpy.ops.object.modifier_apply(modifier=mod.name)
def pipe(n,pts,outer=.027,inner=.016):
 samples=[]
 for i,p in enumerate(pts):samples.append((p,(Vector(pts[min(i+1,len(pts)-1)])-Vector(pts[max(0,i-1)])).normalized(),outer,inner))
 return tube('QUARRY | '+n,samples,m['copper'],col,root)
def torus(n,p,major,minor,mat,parent=root,axis='X'):
 bpy.ops.mesh.primitive_torus_add(major_segments=48,minor_segments=8,location=(0,0,0),major_radius=major,minor_radius=minor)
 o=bpy.context.object
 for c in tuple(o.users_collection):c.objects.unlink(o)
 col.objects.link(o);o.name='QUARRY | '+n;o.parent=parent;o.location=p
 if axis=='X':o.rotation_euler.y=math.pi/2
 elif axis=='Y':o.rotation_euler.x=math.pi/2
 surfaces.apply(o,mat);return o
# Import the useful named groups without requiring legacy OBJ materials.
verts=[];groups={};group=None
for line in starter.read_text().splitlines():
 p=line.split()
 if not p:continue
 if p[0]=='v':verts.append(Vector(map(float,p[1:])))
 elif p[0]=='g':group=p[1];groups[group]=[]
 elif p[0]=='f':groups[group].append([int(x)-1 for x in p[1:]])
reused={};payload_faces=None;payload_pts=None
for name,faces in groups.items():
 ids=sorted({i for f in faces for i in f});lookup={i:j for j,i in enumerate(ids)}
 points=[verts[i].copy() for i in ids];localfaces=[tuple(lookup[i] for i in f) for f in faces]
 if 'quarried_block_a' in name:
  center=sum(points,Vector())/len(points);payload_pts=[tuple((p-center)*.65) for p in points];payload_faces=localfaces;continue
 if 'hoist_roller' in name:continue
 wood='a_frame' in name
 mat=m['wood'] if wood else m['soil'] if 'excavation_floor' in name else m['stone-bed'] if 'base_stone' in name else m['stone-face']
 if wood:
  sign=-1 if 'left' in name else 1
  for p in points:
   if p.z>1:p.x+=sign*.43;p.z+=.29
 if 'quarried_block_b' in name:
  for p in points:p.z+=.09
 o=mesh('QUARRY | REUSED '+name,[tuple(p) for p in points],localfaces,mat,col,root,0 if 'base_stone' in name or 'cut_face' in name else .015)
 if wood:
  sign=-1 if 'left' in name else 1
  a,b=Vector((sign*.9,.5,.3)),Vector((sign*.43,.6,2.4));center=(a+b)/2;q=(b-a).to_track_quat('Z','Y')
  for vertex in o.data.vertices:vertex.co=q.inverted()@(vertex.co-center)
  o.location=center;o.rotation_euler=q.to_euler()
 surfaces.apply(o,mat,m['endgrain'] if wood else None);reused[name]=o
base=reused['quarry_base_stone']
for name in ('quarry_cut_face_north','quarry_cut_face_east'):
 o=reused[name];boolean(base,o,'UNION');bpy.data.objects.remove(o,do_unlink=True)
cutter=B('temporary north terrace',(0,.745,1.0),(2.65,.28,.36),m['stone-face'],bevel=0)
boolean(base,cutter,'DIFFERENCE');bpy.data.objects.remove(cutter,do_unlink=True)
bevel=base.modifiers.new('Cut rock edge arris','BEVEL');bevel.width=.018;bevel.segments=2
# Real mineral traces lie on the remaining cut faces, not arbitrary glowing machinery.
for name,y,z,mat in [('iron',.738,.62,m['iron-seam']),('copper',.878,.99,m['copper-seam'])]:
 xs=[-1.15,-.72,-.32,.11,.56,1.15];zs=[z,z+.025,z-.012,z+.018,z-.01,z+.012]
 p=[(x,y,zz+delta) for delta in (-.014,.014) for x,zz in zip(xs,zs)]
 f=[(i,i+1,6+i+1,6+i) for i in range(5)]
 o=mesh('QUARRY | exposed '+name+' mineral trace',p,f,mat,col,root);surfaces.physical_box_uv(o)
# The retained A-frame is braced to actual rock/wood bearing supports.
B('windlass head tie',(0,.60,2.4),(1.12,.18,.13),m['wood'])
for sign in (-1,1):
 beam('rear thrust brace',(sign*.95,1.14,1.135),(sign*.43,.60,2.4),.12)
 B('front heel shoe',(sign*.9,.5,.34),(.25,.24,.065),m['iron'])
 B('shaft bearing seat',(sign*.47,.59,2.00),(.20,.22,.14),m['wood'])
 C('shaft bearing housing',(sign*.47,.59,2.1),.08,.12,m['bronze'],'X')
B('outboard bearing pier',(1.16,.59,1.53),(.15,.18,1.30),m['wood'])
C('outboard bearing housing',(1.16,.59,2.1),.08,.14,m['bronze'],'X')
C('fixed carrier axle',(.25,.59,2.1),.03,1.92,m['iron'],'X')
WINCH_RADIUS=.188;LIFT=.70;BASE=.43;HOOK=.715;TOP=2.1
drum=E('winding drum',(0,.59,TOP))
C('refined original hoist roller',(0,0,0),.18,.58,m['wood'],'X',drum)
for x in (-.307,.307):C('windlass retaining flange',(x,0,0),.214,.035,m['iron'],'X',drum)
for i in range(-4,5):torus('wound hemp turn',(i*.04,0,0),WINCH_RADIUS,.012,m['rope'],drum)
# Upright bucket, four supported sides, handles and a reused stone payload.
bucket=E('upright lifting bucket',(0,.59-WINCH_RADIUS,BASE))
for i in range(5):B('bucket floor plank',(i*.12-.24,0,.03),(.118,.60,.06),m['wood'],bucket)
for sign in (-1,1):
 for i in range(5):
  B('bucket side stave',(sign*.29,i*.11-.22,.20),(.035,.105,.28),m['wood'],bucket)
  B('bucket end stave',(i*.11-.22,sign*.285,.20),(.105,.035,.28),m['wood'],bucket)
 for z in (.12,.31):
  B('bucket side restraint',(sign*.313,0,z),(.025,.63,.035),m['iron'],bucket)
  B('bucket end restraint',(0,sign*.31,z),(.63,.025,.035),m['iron'],bucket)
 C('bucket handle upright',(sign*.265,0,.47),.018,.37,m['iron'],parent=bucket)
B('bucket lifting yoke',(0,0,.65),(.55,.045,.04),m['iron'],bucket)
torus('bucket rope eye',(0,0,.69),.025,.010,m['iron'],bucket,'Y')
load=mesh('QUARRY | reused lifted stone',payload_pts,payload_faces,m['stone-face'],col,bucket,.016);load.location.z=.23;surfaces.apply(load,m['stone-face'])
cable=C('taut lifting cable',(0,.59-WINCH_RADIUS,1.5),.012,1,m['rope'])
# Brick/tools supplies make the real ore recipes legible beside the cutting face.
for i in range(5):
 B('retaining brick stock',(-1.01+(i%2)*.23,.99,1.195+(i//2)*.12),(.22,.30,.115),m['brick'])
for x in (-.94,-.63):
 beam('stone-tool handle',(x,-.82,.47),(x,-.43,.67),.028)
 C('stone-tool head',(x,-.42,.68),.055,.17,m['stone-face'],'X',segments=16)
# Contained burner/thermal drive; quarry has NO external fluid connections.
PULLEY_R=.195;DZ=.82;DIST=2*math.pi*PULLEY_R;EY=.59-math.sqrt(DIST*DIST-DZ*DZ)
EC=Vector((.82,EY,1.28));UP=Vector((.82,.59,TOP));ROD=.26;CRANK=.07
for z in (.94,1.06):
 for y in (EY-.20,EY+.20):B('fuel firebox brick',(1.10,y,z),(.46,.10,.115),m['brick'])
 for x in (.91,1.29):B('firebox side brick',(x,EY,z),(.10,.30,.115),m['brick'])
B('iron stoke door',(1.10,EY-.263,1.0),(.30,.035,.21),m['iron'])
B('stoke door latch',(1.10,EY-.29,1.01),(.13,.035,.025),m['bronze'])
C('contained copper heat jacket',(1.10,EY,1.34),.19,.32,m['copper'])
C('heat jacket crown',(1.10,EY,1.51),.205,.025,m['bronze'])
pipe('contained steam feed',[(.94,EY,1.43),(.85,EY-.25,1.43),(.75,EY-.54,1.35)])
pipe('brick firebox flue',[(1.29,EY+.1,1.12),(1.33,EY+.1,1.37),(1.33,EY+.1,1.68)],.04,.027)
B('engine cylinder bed',(.94,EY-.5,.92),(.50,.45,.08),m['iron'])
B('crank bearing sole',(.88,EY,.92),(.28,.25,.08),m['iron'])
B('crank bearing pedestal',(.88,EY,1.10),(.12,.15,.29),m['wood'])
C('crank bearing housing',(.88,EY,1.28),.065,.10,m['bronze'],'X')
C('engine crank shaft',(.82,EY,1.28),.025,.18,m['iron'],'X')
C('pressure cylinder',(.75,EY-.54,1.28),.075,.28,m['iron'],'Y')
C('cylinder front gland',(.75,EY-.395,1.28),.08,.025,m['bronze'],'Y')
for y in (EY-.63,EY-.45):B('cylinder saddle',(.75,y,1.11),(.14,.08,.30),m['wood'])
for x in (.70,.80):C('crosshead guide',(x,EY-.27,1.26),.012,.30,m['iron'],'Y')
wheel=E('thermal engine flywheel',EC);drive=E('driven upper pulley',UP)
for parent in (wheel,drive):
 C('timber transmission pulley',(0,0,0),.18,.045,m['wood'],'X',parent)
 for x in (-.032,.032):C('pulley rope flange',(x,0,0),.21,.012,m['iron'],'X',parent)
 for k in range(3):
  a=k*math.tau/3
  beam('pulley face spoke',(-.043,.04*math.cos(a),.04*math.sin(a)),(-.043,.15*math.cos(a),.15*math.sin(a)),.02,m['bronze'],parent)
pin=C('retained engine crank pin',(-.07,CRANK,0),.023,.14,m['bronze'],'X',wheel)
piston=C('guided working piston',(.75,EY-.43,1.28),.020,.32,m['iron'],'Y');piston.rotation_euler.x=-math.pi/2
slider=B('crosshead slider',(.75,EY-.27,1.28),(.14,.07,.10),m['bronze'],bevel=0)
for x in (.70,.80):
 cutter=C('temporary slider guide bore',(x,EY-.27,1.26),.016,.20,m['iron'],'Y');boolean(slider,cutter,'DIFFERENCE');bpy.data.objects.remove(cutter,do_unlink=True)
rod=C('rigid engine connecting rod',(.75,EY-.12,1.28),.016,ROD,m['iron'])
C('windlass clutch counterplate',(.62,0,0),.13,.04,m['bronze'],'X',drum)
C('driving friction plate',(-.16,0,0),.13,.04,m['iron'],'X',drive)
B('brake lever support',(1.16,.80,1.93),(.10,.42,.10),m['iron'])
beam('mounted hand brake lever',(1.16,.96,1.93),(.67,.74,2.10),.027,m['wood'])
# The cord drive has exactly three pulley circumferences per closed belt loop.
D=(UP-EC).normalized();normal=Vector((0,-D.z,D.y));A=math.atan2(normal.z,normal.y)
HALF=math.pi*PULLEY_R;PERIM=2*HALF+2*DIST
def belt_pose(distance):
 q=distance%PERIM
 if q<HALF:
  a=A+q/PULLEY_R;p=EC+Vector((0,math.cos(a),math.sin(a)))*PULLEY_R;t=Vector((0,-math.sin(a),math.cos(a)))
 elif q<HALF+DIST:
  f=(q-HALF)/DIST;p=(EC-normal*PULLEY_R).lerp(UP-normal*PULLEY_R,f);t=D
 elif q<2*HALF+DIST:
  a=A+math.pi+(q-HALF-DIST)/PULLEY_R;p=UP+Vector((0,math.cos(a),math.sin(a)))*PULLEY_R;t=Vector((0,-math.sin(a),math.cos(a)))
 else:
  f=(q-2*HALF-DIST)/DIST;p=(UP+normal*PULLEY_R).lerp(EC+normal*PULLEY_R,f);t=-D
 return p,t
points=[belt_pose(PERIM*i/160) for i in range(160)]
vtx=[]
for p,t in points:
 across=Vector((1,0,0));side=t.cross(across).normalized()
 for j in range(8):vtx.append(tuple(p+.014*(math.cos(j*math.tau/8)*across+math.sin(j*math.tau/8)*side)))
faces=[]
for i in range(160):
 for j in range(8):faces.append((i*8+j,i*8+(j+1)%8,((i+1)%160)*8+(j+1)%8,((i+1)%160)*8+j))
belt=mesh('QUARRY | taut closed hemp transmission',vtx,faces,m['rope'],col,root);surfaces.physical_box_uv(belt)
markers=[C('travelling cord splice '+str(i),(0,0,0),.021,.045,m['rope'],segments=16) for i in range(3)]
# Key real rigid motions and paid-out cable length; the bucket never tilts.
for f in range(1,194):
 phase=(f-1)*math.tau/192;lift=LIFT*(.5-.5*math.cos(phase));theta=phase*3
 wheel.rotation_euler.x=theta;drive.rotation_euler.x=theta;drum.rotation_euler.x=-lift/WINCH_RADIUS
 bucket.location.z=BASE+lift
 hook=bucket.location.z+HOOK;length=TOP-hook;cable.location=(0,.59-WINCH_RADIUS,(TOP+hook)/2);cable.scale.z=length
 crank=Vector((.75,EY+CRANK*math.cos(theta),1.28+CRANK*math.sin(theta)))
 slide=Vector((.75,crank.y-math.sqrt(ROD**2-(crank.z-1.28)**2),1.28))
 slider.location=slide;piston.location=(.75,slide.y-.16,1.28)
 rod.location=(crank+slide)/2;rod.rotation_euler=(crank-slide).to_track_quat('Z','Y').to_euler()
 for o in (wheel,drive,drum):o.keyframe_insert(data_path='rotation_euler',frame=f)
 for o in (bucket,cable,slider,piston,rod):o.keyframe_insert(data_path='location',frame=f)
 cable.keyframe_insert(data_path='scale',frame=f);rod.keyframe_insert(data_path='rotation_euler',frame=f)
 for i,marker in enumerate(markers):
  p,t=belt_pose(PERIM*((f-1)/192+i/3));marker.location=p;marker.rotation_euler=t.to_track_quat('Z','Y').to_euler();marker.keyframe_insert(data_path='location',frame=f);marker.keyframe_insert(data_path='rotation_euler',frame=f)
# Freeze evaluated arrises, then repair only actual zero-area triangles.
repairs={}
for o in root.children_recursive:
 if o.type!='MESH':continue
 if o.modifiers:
  ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());data=bpy.data.meshes.new_from_object(ev);o.modifiers.clear();o.data=data
 if not o.data.uv_layers:surfaces.physical_box_uv(o)
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.triangulate(bm,faces=list(bm.faces));bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-7);bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=1e-7);bm.to_mesh(o.data);bm.free()
 o.data.calc_loop_triangles();bad={t.polygon_index for t in o.data.loop_triangles if t.area<1e-12}
 if bad:
  bm=bmesh.new();bm.from_mesh(o.data);bm.faces.ensure_lookup_table();bmesh.ops.delete(bm,geom=[bm.faces[i] for i in bad],context='FACES');bm.to_mesh(o.data);bm.free();repairs[o.name]=len(bad)
 if o.animation_data:
  for layer in o.animation_data.action.layers:
   for strip in layer.strips:
    for bag in strip.channelbags:
     for curve in bag.fcurves:
      for key in curve.keyframe_points:key.interpolation='LINEAR'
profile={'camera_policy':'fmpl.factorio45.v1','capture_kind':'entity','orientation_policy':'fixed','directions':[0],'states':{'idle':[0],'working':list(range(1,182,12))},'source_size':256,'fps':4,'camera_override':{'type':'ORTHO','elevation_deg':45,'azimuth_deg':0,'distance':math.sqrt(72),'ortho_scale':5.6,'target':[0,0,1.05]}}
scene.render.fps=48;scene.frame_start=1;scene.frame_end=193;install_canonical_camera(scene,profile,bpy);scene.frame_set(1);bpy.ops.file.pack_all();assert_clean(scene,profile,bpy)
source=O/'quarry-v1.blend';bpy.ops.wm.save_as_mainfile(filepath=str(source),compress=True)
bpy.ops.wm.open_mainfile(filepath=str(source));scene=bpy.context.scene;root=bpy.data.objects['EXPORT | Quarry all authored parts']
bpy.ops.object.select_all(action='DESELECT')
for o in [root,*root.children_recursive]:o.select_set(True)
bpy.ops.export_scene.gltf(filepath=str(O/'quarry-v1.glb'),export_format='GLB',use_selection=True,export_cameras=False,export_lights=False,export_animations=True,export_animation_mode='SCENE',export_anim_scene_split_object=False,export_frame_range=True,export_force_sampling=True,export_frame_step=1,export_apply=True,export_extras=True)
(O/'capture-profile.json').write_text(json.dumps(profile,indent=2)+'\n')
(O/'construction-receipt.json').write_text(json.dumps(dict(source_sha256=sha(source),runtime_sha256=sha(O/'quarry-v1.glb'),starter_sha256=sha(starter),reused_groups=list(reused),winch_radius=WINCH_RADIUS,lift=LIFT,bucket_base_z=BASE,hook_offset=HOOK,cable_top=[0,.59-WINCH_RADIUS,TOP],engine_center=list(EC),crank_radius=CRANK,rod_length=ROD,belt_perimeter=PERIM,belt_pulley_radius=PULLEY_R,engine_turns_per_cycle=3,zero_area_repairs=repairs,native_fixed_orientation=True),indent=2)+'\n')
projection=bpy.data.objects.new('SPRITE ONLY square ground grid',None);scene.collection.objects.link(projection);projection.scale.y=math.sqrt(2);root.parent=projection
for name,yaw in [('native',0),('inspection-east',270),('inspection-rear',180),('inspection-west',90)]:
 root.rotation_euler.z=math.radians(yaw);scene.frame_set(49);assert_clean(scene,profile,bpy);scene.render.filepath=str(O/(name+'-pilot.png'));bpy.ops.render.render(write_still=True)
print('QUARRY_AUTHORED_SOURCE_SAVED',source,flush=True)
