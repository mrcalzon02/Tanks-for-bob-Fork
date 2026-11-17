"""Refine the tracked timber/thatch hut into the actual burner-powered research lab."""
import bpy,bmesh,json,math,sys,tempfile,hashlib
import numpy as np
from pathlib import Path
from mathutils import Vector
H=Path(__file__).resolve().parent;R=H.parents[3];O=H.parent/'candidates/v1-study03'
if O.exists():raise FileExistsError(O)
O.mkdir(parents=True);tempfile.tempdir=str(R/'build/quarry-export-temp')
sys.path.insert(0,str(R/'models/island-survival/primitive-steam-powered-pump/v3'))
from mesh_util import mesh,box,cylinder,tube,lathe
import surfaces
sys.path.insert(0,str(R.parent/'model-production/tools/fmpl'))
from blender_camera_guard import install_canonical_camera,assert_clean,temporary_inspection_camera
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
contract=json.loads((H/'contract.json').read_text(encoding='utf-8'));starter=H/'starter-thinking-hut.obj';assert sha(starter)==contract['source']['sha256']
bpy.ops.wm.read_factory_settings(use_empty=True);s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=48;s.cycles.use_denoising=False;s.render.film_transparent=True;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGBA'
s.world=bpy.data.worlds.new('Neutral hut workshop');s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs[0].default_value=(.30,.30,.30,1)
for p,power,size in [((4,-4,7),800,5),((-4,2,5),480,4),((0,2,7),280,3)]:
 light=bpy.data.lights.new('Workshop area','AREA');light.energy=power;light.size=size;o=bpy.data.objects.new('Workshop area',light);s.collection.objects.link(o);o.location=p;o.rotation_euler=(Vector((0,0,1.2))-o.location).to_track_quat('-Z','Y').to_euler()
root=bpy.data.objects.new('EXPORT | Thinking Hut authored shelter',None);s.collection.objects.link(root);col=bpy.data.collections.new('THINKING HUT | supported research shelter');s.collection.children.link(col)
m=surfaces.create(O);rng=np.random.default_rng(171700);u,v=np.meshgrid(np.linspace(0,1,512),np.linspace(0,1,512));broad=surfaces.field(rng,(512,512),.018);fine=surfaces.field(rng,(512,512),.22)
straw=np.sin(u*310+.7*np.sin(v*7)+.10*broad)+.3*np.sin(u*793+.6*np.sin(v*12));weave=.5*np.sin(u*145)*np.sin(v*167)
for name,color,rough,detail in [('bound-reed-thatch',(.36,.285,.15),.95,.026*straw+.012*broad),('clay-daub-wattle',(.36,.315,.235),.92,.018*weave+.012*broad),('clay-flue',(.285,.20,.12),.85,.014*broad+.004*fine),('rounded-hearth-stone',(.27,.27,.24),.94,.015*broad),('soot-and-coal',(.035,.030,.024),.96,.007*fine),('hemp-binding',(.27,.21,.125),.95,.012*np.sin(u*290+v*30)),('seared-food',(.31,.16,.065),.75,.018*broad)]:
 m[name]=surfaces.material('thinking-hut-'+name,np.stack([x+detail for x in color],axis=-1),rough+.015*fine,.5+.018*broad+.013*fine,0,O)
paper=np.stack([.61+.018*broad,.55+.015*broad,.40+.014*broad],axis=-1)
ink=np.zeros((512,512),dtype=bool)
for j in range(9):
 y=65+j*42
 for i in range(7):
  x=45+i*55+int(rng.integers(0,9));ink[y:y+3,x:x+int(rng.integers(19,42))]=True;ink[y-8:y+2,x+4:x+7]=True
ink[28:31,28:484]=True;ink[480:483,28:484]=True;paper[ink]=(.12,.085,.045)
m['paper']=surfaces.material('thinking-hut-handwritten-records',paper,.90+.02*fine,.5+.014*broad,0,O)
m['ember']=surfaces.material('thinking-hut-hot-lamp-wick',np.stack([.70+.04*broad,.20+.015*broad,.035+.006*broad],axis=-1),.66+.01*fine,.5+.01*fine,0,O)
shader=m['ember'].node_tree.nodes['Principled BSDF'];shader.inputs['Emission Color'].default_value=(.7,.13,.015,1);shader.inputs['Emission Strength'].default_value=.8
for mat in m.values():mat.name=mat.name.replace('PUMP V3','THINKING HUT');mat['surface_authorship']='Thinking Hut: bound weathered reed roof, woven daub, timber grain/end cuts, handwritten actual research-document records, fired clay hearth/flue, lamp and food support for the current 14-input burner lab'
def B(n,p,d,mat,parent=root,bevel=.006):
 o=box('HUT | '+n,p,d,mat,col,parent,bevel);surfaces.apply(o,mat,m['endgrain'] if mat==m['wood'] else None);return o
def C(n,p,r,d,mat,axis='Z',parent=root,segments=32):
 o=cylinder('HUT | '+n,p,r,d,mat,col,parent,axis,segments);surfaces.apply(o,mat);return o
def E(n,p=(0,0,0)):
 o=bpy.data.objects.new('HUT | '+n,None);col.objects.link(o);o.parent=root;o.location=p;return o
def beam(n,a,b,w,mat=m['wood'],parent=root):
 a,b=Vector(a),Vector(b);o=B(n,(a+b)/2,(w,w,(b-a).length),mat,parent);o.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler();return o
def ring(n,p,outer,inner,depth,mat,axis='Z',parent=root):
 t=Vector({'X':(1,0,0),'Y':(0,1,0),'Z':(0,0,1)}[axis]);o=tube('HUT | '+n,[(-t*depth/2,t,outer,inner),(t*depth/2,t,outer,inner)],mat,col,parent,40);o.location=p;return o
def bore(o,cut):
 bpy.context.view_layer.update();bpy.context.view_layer.objects.active=o;mod=o.modifiers.new('Real usable opening','BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=cut;bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cut,do_unlink=True)
def rope(n,points,r=.008,parent=root):
 p=[Vector(x) for x in points];return tube('HUT | '+n,[(x,(p[min(i+1,len(p)-1)]-p[max(0,i-1)]).normalized(),r,0) for i,x in enumerate(p)],m['hemp-binding'],col,parent,8)
# Preserve the actual starter floor, wall shell, sloped roof, doorway, lantern
# backing and open vent. Strip closed blockout caps where construction is open.
verts=[];groups={};group=None
for line in starter.read_text().splitlines():
 t=line.split()
 if not t:continue
 if t[0]=='v':verts.append(Vector(map(float,t[1:])))
 elif t[0]=='g':group=t[1];groups[group]=[]
 elif t[0]=='f':groups[group].append(tuple(int(x)-1 for x in t[1:]))
reused=[]
for name,faces in groups.items():
 ids=sorted({i for face in faces for i in face});lookup={i:j for j,i in enumerate(ids)};pts=[verts[i].copy() for i in ids];fs=[tuple(lookup[i] for i in face) for face in faces];mat=m['wood'];solid=None
 if name.endswith('_floor'):pts=[(p.x,p.y,p.z*.40) for p in pts]
 elif name.endswith('_hut_walls'):
  fs=fs[6:];pts=[(p.x,-.45+(p.y+1.11)*(1.56/2.22),.18+(p.z-.305)*(1.56/1.55)) for p in pts];mat=m['clay-daub-wattle'];solid=.055
 elif name.endswith('_thatch_roof'):
  fs=fs[:4];pts=[(p.x,p.y,2.10+(p.z-1.53)*.83) for p in pts];mat=m['bound-reed-thatch'];solid=.075
 elif name.endswith('_doorway'):
  pts=[(-.70+p.x*.90,-.48+(p.y+1.13)*.6,.18+(p.z-.425)*1.25) for p in pts]
 elif name.endswith('_wall_lantern'):
  fs=fs[8:10];pts=[(-1.09+(p.x-.84)*.70,-1.15+(p.y+1.15)*.6,1.35+(p.z-1.45)*.75) for p in pts];mat=m['iron'];solid=.01
 elif name.endswith('_smoke_vent'):
  fs=[f for f in fs if max(pts[i].z for i in f)-min(pts[i].z for i in f)>.1];pts=[(.82+p.x-.65,.50+p.y-.60,2.74+(p.z-2.585)*(.51/.39)) for p in pts];mat=m['clay-flue'];solid=.03
 o=mesh('HUT | REUSED '+name,pts,fs,mat,col,root);surfaces.apply(o,mat,m['endgrain'] if mat==m['wood'] else None);reused.append(o.name)
 if solid:
  mod=o.modifiers.new('Real construction thickness','SOLIDIFY');mod.thickness=solid;mod.offset=-1
  bpy.context.view_layer.objects.active=o;bpy.ops.object.modifier_apply(modifier=mod.name)
 if name.endswith('_hut_walls'):
  for x in (-1.13,1.13):bore(o,B('temporary wall window',(x,.10,1.10),(.30,.65,.58),m['iron']))
 if name.endswith('_thatch_roof'):bore(o,C('temporary clay flue roof clearance',(.82,.50,2.80),.225,1.4,m['iron']))
# Timber foundations, joined frame and an open study porch; no floating roof.
for i in range(14):B('separate floor board',(-1.30+i*.20,0,.153),(.192,2.76,.050),m['wood'])
for x in (-1.18,1.18):
 for y in (-1.20,1.07):
  B('load carrying post',(x,y,1.11),(.12,.12,1.86),m['wood']);B('post stone pad',(x,y,.10),(.21,.21,.16),m['rounded-hearth-stone'])
  beam('post knee brace',(x,y,1.70),(x-math.copysign(.28,x),y,2.03),.065)
 B('eaves beam',(x,0,2.035),(.13,2.73,.105),m['wood'])
for y in (-1.20,1.07):B('roof bearing crossbeam',(0,y,2.035),(2.70,.11,.105),m['wood'])
for x in (-1.25,-.63,0,.63,1.25):
 for sign in (-1,1):beam('roof rafter',(x,sign*1.36,2.9632-1.36*(.8632/1.41)-.112),(x,0,2.8512),.07)
 B('rear rafter bearing seat',(x,1.07,2.118),(.08,.12,.061),m['wood'])
beam('supported ridge purlin',(-1.32,0,2.88),(1.32,0,2.88),.08)
for x in (-1.18,1.18):
 for y,z in [(-1.20,2.05),(1.07,2.05)]:
  for j in range(3):rope('lashed beam joint',[(x-.085,y-.085,z-.015+j*.017),(x+.085,y-.085,z-.015+j*.017),(x+.085,y+.085,z-.015+j*.017),(x-.085,y+.085,z-.015+j*.017),(x-.085,y-.085,z-.015+j*.017)],.009)
# Roof reed bundles follow the actual slope; omit the hot flue penetration.
for sign in (-1,1):
 for course in range(3):
  ya=.02+course*.43;yb=min(1.45,ya+.61)
  for i in range(38):
   x=-1.37+i*.074+float(rng.uniform(-.008,.008));yy=sign*(ya+yb)/2
   if sign>0 and abs(x-.82)<.26 and .20<yy<.79:continue
   for dx in (-.023,-.008,.008,.023):
    aa=max(.005,ya+float(rng.uniform(-.035,.025)));bb=yb+float(rng.uniform(-.035,.035));a=Vector((x+dx,sign*aa,2.9632-aa*(.8632/1.41)+.035));b=Vector((x+dx+float(rng.uniform(-.009,.009)),sign*bb,2.9632-bb*(.8632/1.41)+.035))
    o=C('individual staggered roof reed',(a+b)/2,float(rng.uniform(.0045,.0075)),(b-a).length,m['bound-reed-thatch'],segments=10);o.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler()
for i in range(22):
 x=-1.32+i*.125;rope('ridge saddle binding',[(x,-.19,2.90),(x,0,3.01),(x,.19,2.90)],.014)
# Wattle ribs, real window frames/shutters, door supports and clear entrance.
for x in (-1.13,1.13):
 for y in (-.42,.48,1.07):B('wall exposed stave',(x,y,.96),(.075,.07,1.56),m['wood'])
 for z in (.78,1.42):B('window lintel sill',(x,.10,z),(.13,.80,.075),m['wood'])
 for y in (-.26,.46):B('window side jamb',(x,y,1.10),(.13,.07,.66),m['wood'])
 for z in (.94,1.18):B('window open slat',(x,.10,z),(.040,.66,.028),m['wood'])
for x in (-1.025,-.375):B('door jamb',(x,-.48,.88),(.09,.11,1.40),m['wood'])
B('door lintel',(-.70,-.48,1.60),(.80,.13,.10),m['wood'])
for z in (.55,1.25):B('door strap',(-.70,-.515,z),(.54,.025,.035),m['iron'])
for i in range(5):B('door plank seam',(-.94+i*.12,-.516,.88),(.008,.012,1.26),m['iron'],bevel=0)
C('door latch pivot',(-.46,-.55,.93),.024,.04,m['bronze'],'Y');B('door wooden latch',(-.51,-.575,.93),(.17,.025,.025),m['wood'])
B('entry step',(-.70,-1.44,.06),(.70,.10,.12),m['rounded-hearth-stone'])
# Desk and paper/document handling visibly match the actual research supplies.
for x in (-.12,.96):
 for y in (-1.18,-.80):
  B('study bench leg',(x,y,.4875),(.075,.075,.615),m['wood']);beam('bench bracing',(x,y,.30),(x,y+.12,.74),.035)
B('study bench top',(.42,-.99,.83),(1.25,.52,.07),m['wood'])
for x in (-.13,.97):B('desk apron',(x,-.99,.73),(.055,.49,.08),m['wood'])
for i in range(5):B('stacked research records',(.12,-1.04,.875+i*.009),(.27,.30,.008),m['paper'],bevel=.001)
for j in range(3):B('sorted dossier bundle',(.06+j*.16,-.79,.89),(.125,.12,.045),m['paper'],bevel=.002)
rope('document cord',[(-.015,-.79,.92),(.06,-.85,.92),(.135,-.79,.92),(.06,-.73,.92),(-.015,-.79,.92)],.004)
ring('quill ink pot',(.37,-.78,.91),.043,.027,.09,m['clay-flue']);beam('reed writing stylus',(.37,-.78,.93),(.43,-.76,1.12),.009,m['wood'])
tray=lathe('HUT | food support bowl',[(0,.865),(.105,.865),(.12,.89),(.13,.94),(.115,.94),(.10,.89),(0,.89)],(-.08,-.84),m['clay-flue'],col,root,32);surfaces.physical_box_uv(tray)
B('meal ration in bowl',(-.08,-.84,.91),(.12,.09,.04),m['seared-food'])
# A sensitive bench balance supplies restrained research activity. Its pans
# translate from the exact beam eye positions and remain upright in world space.
origin=Vector((.70,-1.08,1.28));balance=E('research balance beam',origin)
beam('balance crossbar',(-.32,0,0),(.32,0,0),.025,m['bronze'],balance)
for x in (-.28,.28):ring('balance retained suspension eye',(x,0,0),.016,.007,.025,m['bronze'],'Y',balance)
C('balance pivot pin',origin,.018,.10,m['iron'],'Y');B('balance upright',(.70,-1.035,1.08),(.045,.045,.39),m['wood']);B('balance base',(.70,-1.035,.89),(.22,.16,.05),m['wood'])
pans=[]
for sign in (-1,1):
 pan=E('upright suspended weighing pan '+str(sign));pans.append((sign,pan))
 dish=lathe('HUT | suspended balance dish '+str(sign),[(0,-.018),(.070,-.018),(.086,.010),(.086,.022),(.078,.022),(.066,-.006),(0,-.006)],(0,0),m['bronze'],col,pan,32);surfaces.physical_box_uv(dish)
 for i in range(3):
  a=i*math.tau/3;rope('three point suspension cord',[(.078*math.cos(a),.078*math.sin(a),.015),(0,0,.22)],.003,parent=pan)
 B('research sample on pan',(0,0,.008),(.055,.048,.025),m['seared-food'] if sign<0 else m['paper'],pan,bevel=.003)
# Continuous hearth -> clay hood -> supported flue, with a real roof hole.
for layer in range(3):
 for x in (.68,.96):
  for y in (.34,.61):B('bonded hearth footing',(x,y,.23+layer*.10),(.14,.27,.095),m['rounded-hearth-stone'])
ring('clay firepot',(.82,.50,.63),.190,.148,.32,m['clay-flue']);C('coal bed',(.82,.50,.61),.145,.035,m['soot-and-coal']);C('working hearth ember',(.82,.50,.645),.12,.018,m['ember'])
hood=tube('HUT | shouldered clay smoke hood',[(Vector((.82,.50,.79)),Vector((0,0,1)),.195,.169),(Vector((.82,.50,1.08)),Vector((0,0,1)),.145,.116)],m['clay-flue'],col,root,48)
ring('continuous clay flue',(.82,.50,1.91),.15,.12,1.66,m['clay-flue']);curb=ring('roof heat clearance curb',(.82,.50,2.692),.245,.157,.055,m['clay-flue'])
for vtx in curb.data.vertices:vtx.co.z-=(.8632/1.41)*vtx.co.y
# Retained lantern backing receives a supported cage and an attached live wick.
for x in (-1.18,-1.00):
 for y in (-1.27,-1.15):C('lantern cage corner',(x,y,1.35),.008,.25,m['iron'])
for z in (1.22,1.48):B('lantern cage plate',(-1.09,-1.21,z),(.22,.16,.025),m['iron'])
beam('lantern post bracket',(-1.18,-1.20,1.48),(-1.09,-1.21,1.48),.022,m['iron'])
C('lamp oil cup',(-1.09,-1.21,1.26),.040,.055,m['clay-flue']);flame=E('working lamp flame',(-1.09,-1.21,1.30))
bpy.ops.mesh.primitive_uv_sphere_add(segments=16,ring_count=8,radius=1);o=bpy.context.object
for collection in tuple(o.users_collection):collection.objects.unlink(o)
col.objects.link(o);o.name='HUT | actual wick flame';o.parent=flame;o.scale=(.018,.018,.050);o.location.z=.025;surfaces.apply(o,m['ember'])
for frame in range(0,194):
 phase=math.tau*(frame-1)/192;angle=0 if frame==0 else .10*math.sin(phase);balance.rotation_euler.y=angle;balance.keyframe_insert(data_path='rotation_euler',frame=frame)
 for sign,pan in pans:
  eye=origin+Vector((sign*.28*math.cos(angle),0,-sign*.28*math.sin(angle)));pan.location=eye-Vector((0,0,.22));pan.rotation_euler=(0,0,0);pan.keyframe_insert(data_path='location',frame=frame)
 flame.scale=(1,1,.001 if frame==0 else .92+.14*math.sin(phase*3)+.055*math.sin(phase*7));flame.keyframe_insert(data_path='scale',frame=frame)
for o in root.children_recursive:
 if o.animation_data:
  for layer in o.animation_data.action.layers:
   for strip in layer.strips:
    for bag in strip.channelbags:
     for curve in bag.fcurves:
      for key in curve.keyframe_points:key.interpolation='LINEAR'
 if o.type!='MESH':continue
 if o.modifiers:o.data=bpy.data.meshes.new_from_object(o.evaluated_get(bpy.context.evaluated_depsgraph_get()));o.modifiers.clear()
 if not o.data.uv_layers:surfaces.physical_box_uv(o)
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.triangulate(bm,faces=list(bm.faces));bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-7);bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=1e-7);bmesh.ops.delete(bm,geom=[v for v in bm.verts if not v.link_faces],context='VERTS');bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free()
 o.data.calc_loop_triangles();bad={t.polygon_index for t in o.data.loop_triangles if t.area<1e-12}
 if bad:
  bm=bmesh.new();bm.from_mesh(o.data);bm.faces.ensure_lookup_table();bmesh.ops.delete(bm,geom=[bm.faces[i] for i in bad],context='FACES');bm.to_mesh(o.data);bm.free()
profile={'camera_policy':'fmpl.factorio45.v1','capture_kind':'entity','orientation_policy':'fixed','directions':[0],'states':{'idle':[0],'working':list(range(1,193,12))},'source_size':256,'fps':4,'camera_override':{'type':'ORTHO','elevation_deg':45,'azimuth_deg':0,'distance':math.sqrt(72),'ortho_scale':5.8,'target':[0,0,1.20]}}
s.frame_start=1;s.frame_end=193;s.render.fps=48;s.render.resolution_x=s.render.resolution_y=256;s.render.resolution_percentage=100
install_canonical_camera(s,profile,bpy);s.frame_set(1);assert_clean(s,profile,bpy);bpy.ops.file.pack_all();native=O/'thinking-hut-v1.blend';bpy.ops.wm.save_as_mainfile(filepath=str(native),compress=True)
bpy.ops.wm.open_mainfile(filepath=str(native));s=bpy.context.scene;root=bpy.data.objects['EXPORT | Thinking Hut authored shelter'];bpy.ops.object.select_all(action='DESELECT')
for o in [root,*root.children_recursive]:o.select_set(True)
bpy.ops.export_scene.gltf(filepath=str(O/'thinking-hut-v1.glb'),export_format='GLB',use_selection=True,export_cameras=False,export_lights=False,export_animations=True,export_animation_mode='SCENE',export_anim_scene_split_object=False,export_frame_range=True,export_force_sampling=True,export_frame_step=1,export_apply=True,export_extras=True)
(O/'capture-profile.json').write_text(json.dumps(profile,indent=2)+'\n');(O/'construction-receipt.json').write_text(json.dumps(dict(source_sha256=sha(native),glb_sha256=sha(O/'thinking-hut-v1.glb'),starter_sha256=sha(starter),reused_groups=reused,native_orientation='fixed north verified: all requested directions normalize to north; rotate false',gameplay_changed=False,owner_visual_approved=False,native_integrated=False),indent=2)+'\n')
projection=bpy.data.objects.new('SPRITE ONLY | square ground projection',None);s.collection.objects.link(projection);projection.scale.y=math.sqrt(2);root.parent=projection;s.render.resolution_x=s.render.resolution_y=512;s.render.filepath=str(O/'front-review512.png');bpy.ops.render.render(write_still=True)
with temporary_inspection_camera(s,bpy,'Hut study bench construction') as camera:
 camera.data.type='ORTHO';camera.data.ortho_scale=2.6;camera.location=(2,-4,2.6);camera.rotation_euler=(Vector((.25,-.70,.90))-camera.location).to_track_quat('-Z','Y').to_euler();s.camera=camera;s.render.filepath=str(O/'bench-close512.png');bpy.ops.render.render(write_still=True)
print('THINKING_HUT_SOURCE_SAVED',native,flush=True)
