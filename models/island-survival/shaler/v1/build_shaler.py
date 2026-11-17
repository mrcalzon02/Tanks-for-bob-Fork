"""Refine the tracked Shaler into a low-tech thermal waste digester and canister press."""
import bpy,bmesh,json,math,sys,tempfile,hashlib
import numpy as np
from pathlib import Path
from mathutils import Vector
H=Path(__file__).resolve().parent;R=H.parents[3];O=R/'models/island-survival/shaler/candidates/v1-production04'
if O.exists():raise FileExistsError(O)
O.mkdir(parents=True);tempfile.tempdir=str(R/'build/quarry-export-temp')
sys.path.insert(0,str(R/'models/island-survival/primitive-steam-powered-pump/v3'))
from mesh_util import mesh,box,cylinder,tube,lathe
import surfaces
sys.path.insert(0,str(R.parent/'model-production/tools/fmpl'))
from blender_camera_guard import install_canonical_camera,assert_clean,temporary_inspection_camera
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
contract=json.loads((H/'contract.json').read_text());starter=H/'starter-shaler.obj';assert sha(starter)==contract['source']['sha256']
bpy.ops.wm.read_factory_settings(use_empty=True);scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=48;scene.cycles.use_denoising=False;scene.render.film_transparent=True
scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA'
scene.world=bpy.data.worlds.new('Neutral workshop light');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.22,.22,.22,1)
for pos,power,size in [((4,-4,7),700,5),((-4,2,5),450,4),((0,2,7),250,3)]:
 light=bpy.data.lights.new('Workshop area','AREA');light.energy=power;light.size=size;o=bpy.data.objects.new('Workshop area',light);scene.collection.objects.link(o);o.location=pos;o.rotation_euler=(Vector((0,0,.9))-o.location).to_track_quat('-Z','Y').to_euler()
root=bpy.data.objects.new('EXPORT | Shaler all authored parts',None);scene.collection.objects.link(root)
col=bpy.data.collections.new('SHALER | retort firebox and guided press');scene.collection.children.link(col)
m=surfaces.create(O)
rng=np.random.default_rng(171141);shape=(512,512);u,v=np.meshgrid(np.linspace(0,1,512),np.linspace(0,1,512));broad=surfaces.field(rng,shape,.012);fine=surfaces.field(rng,shape,.22)
for name,tint,rough in [('worked-sandstone',(.29,.275,.23),.88),('ash-and-soot',(.045,.039,.029),.96),('salt-glazed-stoneware',(.255,.295,.225),.39),('fired-ore-residue',(.22,.105,.045),.86),('hemp-drive-belt',(.16,.125,.076),.91)]:
 mark=.012*broad+.005*fine
 if name=='hemp-drive-belt':mark+=.015*np.sin(u*170+v*40)*np.sin(u*90-v*60)
 color=np.stack([c+mark for c in tint],axis=-1);m[name]=surfaces.material('shaler-'+name,color,rough+.02*fine,.5+.03*broad+.01*fine,0,O)
for mat in m.values():mat.name=mat.name.replace('PUMP V3','SHALER');mat['surface_authorship']='Shaler-specific brick heat/soot, glazed digestion vessel, grain-aligned timber press, worked copper hopper, iron hoops, bronze bearings and hemp drive'
def B(n,p,d,mat,parent=root,bevel=.006):
 o=box('SHALER | '+n,p,d,mat,col,parent,bevel);surfaces.apply(o,mat,m['endgrain'] if mat==m['wood'] else None);return o
def C(n,p,r,d,mat,axis='Z',parent=root,segments=48):
 o=cylinder('SHALER | '+n,p,r,d,mat,col,parent,axis,segments);surfaces.apply(o,mat);return o
def E(n,p=(0,0,0),parent=root):
 o=bpy.data.objects.new('SHALER | '+n,None);col.objects.link(o);o.parent=parent;o.location=p;return o
def beam(n,a,b,w,mat=m['wood'],parent=root):
 a,b=Vector(a),Vector(b);o=B(n,(a+b)/2,(w,w,(b-a).length),mat,parent);o.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler();return o
def pipe(n,points,outer=.045,inner=.027,mat=m['copper'],parent=root):
 samples=[(p,tuple((Vector(points[min(i+1,len(points)-1)])-Vector(points[max(0,i-1)])).normalized()),outer,inner) for i,p in enumerate(points)]
 o=tube('SHALER | '+n,samples,mat,col,parent,segments=32);return o
def boolean(a,b):
 bpy.context.view_layer.objects.active=a;mod=a.modifiers.new('Bored supported joint','BOOLEAN');mod.operation='DIFFERENCE';mod.object=b;mod.solver='EXACT';bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(b,do_unlink=True)
def ring(n,p,outside,inside,depth,mat,axis='X',parent=root):
 # A true bored bearing/flange, rather than a disk blocking the shaft or pipe.
 o=tube('SHALER | '+n,[(tuple(Vector(p)-Vector((depth/2 if axis=='X' else 0,depth/2 if axis=='Y' else 0,depth/2 if axis=='Z' else 0))),{'X':(1,0,0),'Y':(0,1,0),'Z':(0,0,1)}[axis],outside,inside),(tuple(Vector(p)+Vector((depth/2 if axis=='X' else 0,depth/2 if axis=='Y' else 0,depth/2 if axis=='Z' else 0))),{'X':(1,0,0),'Y':(0,1,0),'Z':(0,0,1)}[axis],outside,inside)],mat,col,parent,segments=40);return o
def bolt(n,p,axis='Z',r=.022,depth=.028):return C(n,p,r,depth,m['bronze'],axis,segments=6)
# Retain and transform every useful starter group; invert/open the incorrectly closed hopper.
verts=[];groups={};group=None
for line in starter.read_text().splitlines():
 t=line.split()
 if not t:continue
 if t[0]=='v':verts.append(Vector(map(float,t[1:])))
 elif t[0]=='g':group=t[1];groups[group]=[]
 elif t[0]=='f':groups[group].append([int(x)-1 for x in t[1:]])
reused=[]
for name,faces in groups.items():
 ids=sorted({i for f in faces for i in f});lookup={i:j for j,i in enumerate(ids)};pts=[verts[i].copy() for i in ids];fs=[tuple(lookup[i] for i in f) for f in faces];mat=m['worked-sandstone']
 if 'stone_base' in name:
  pts=[(p.x,p.y,p.z*.20) for p in pts]
 elif 'crusher_body' in name:
  pts=[((p.x/1.9)*1.42-.18,(p.y/1.6)*1.34+.35,.08+(p.z-.425)*.20/1.15) for p in pts];mat=m['brick']
 elif 'jaw_' in name:
  oldx=-.4 if 'left' in name else .4;newx=.45 if oldx<0 else 1.07
  pts=[(newx+(p.x-oldx)*.5,-.65+(p.y+.85)*.6,.08+(p.z-.465)*1.86/1.35) for p in pts];mat=m['wood']
 elif 'raw_feed_hopper' in name:
  # Remove both triangulated caps and unused centers; retain the tapered wall.
  fs=[f for f in fs if len({round(pts[i].z,3) for i in f})>1]
  pts=[(-.18+p.x*.60,.35+(p.y-.14)*.60,1.70+(2.225-p.z)*.67) for p in pts];mat=m['copper']
 elif 'ore_chute' in name:
  pts=[(-.42+p.x*.72,-.96+(p.y+1)*.8,.31+(p.z-.47)*.18) for p in pts];mat=m['wood']
 o=mesh('SHALER | REUSED '+name,pts,fs,mat,col,root);surfaces.apply(o,mat,m['endgrain'] if mat==m['wood'] else None);reused.append(o.name)
 if 'raw_feed_hopper' in name:
  solid=o.modifiers.new('Real hopper wall thickness','SOLIDIFY');solid.thickness=.022;solid.offset=0
 bevel=o.modifiers.new('Worked edge easing','BEVEL');bevel.width=.012 if mat!=m['wood'] else .006;bevel.segments=3
# Paving joints and masonry are deliberate worked construction, not natural boulders.
for x in (-.93,-.46,0,.46,.93):B('paving recessed joint',(x,0,.076),(.009,2.72,.002),m['ash-and-soot'],bevel=0)
for y in (-.93,-.46,0,.46,.93):B('paving recessed joint',(0,y,.076),(2.72,.009,.002),m['ash-and-soot'],bevel=0)
# Firebox under the pressure retort. Side courses carry the vessel cap; front arch remains open.
for layer in range(4):
 z=.12+layer*.105
 for x in (-.81,.45):
  for j in range(5):B('bonded side firebrick',(x,-.24+j*.27,z),(.16,.255,.10),m['brick'])
 for j in range(5):B('rear firebrick',(-.72+j*.27,.94,z),(.255,.15,.10),m['brick'])
 for sign in (-1,1):B('stoke jamb',(-.18+sign*.48,-.30,z),(.34,.16,.10),m['brick'])
for i in range(7):
 a=math.pi*(i+.5)/7;radius=.285
 o=B('stoke arch voussoir',(-.18+radius*math.cos(a),-.30,.18+radius*math.sin(a)),(.12,.17,.15),m['brick']);o.rotation_euler.y=math.pi/2-a
B('heated load bearing hearth cap',(-.18,.35,.56),(1.38,1.38,.07),m['worked-sandstone'])
B('ash catch pan',(-.18,-.30,.105),(.58,.38,.035),m['iron'])
for j in range(5):B('coal grate bar',(-.43+j*.125,-.20,.14),(.025,.35,.025),m['iron'])
for i in range(9):C('visible fuel',(-.4+(i%3)*.20,-.14+(i//3)*.10,.18),.065,.07,m['ash-and-soot'],segments=9)
door=E('stoke door hinge',(-.49,-.40,.22));door.rotation_euler.z=-.9
B('open iron stoke door',(.26,0,0),(.53,.045,.27),m['iron'],door)
for z in (-.08,.08):C('hinge knuckle',(0,0,z),.026,.065,m['bronze'],parent=door)
# Glazed stoneware is bounded by load-bearing iron hoops, fitted lids and fixing studs.
vessel=lathe('SHALER | salt glazed digestion retort',[(.0,.60),(.46,.60),(.55,.70),(.56,1.42),(.51,1.63),(.37,1.70),(.10,1.70),(.10,1.63),(.33,1.60),(.46,1.39),(.46,.73),(.0,.73)],(-.18,.35),m['salt-glazed-stoneware'],col,root,64);surfaces.apply(vessel,m['salt-glazed-stoneware'])
for z,r in ((.73,.557),(1.04,.573),(1.41,.565)):
 ring('wrought retort hoop',(-.18,.35,z),r,r-.026,.065,m['iron'],'Z')
 for sign in (-1,1):B('hoop clasp',(-.18+sign*(r+.015),.35,z),(.05,.15,.10),m['iron']);bolt('hoop clasp fastener',(-.18+sign*(r+.047),.35,z),'X')
ring('sealed feed collar',(-.18,.35,1.69),.16,.035,.07,m['bronze'],'Z')
ring('rolled hopper rim',(-.18,.35,2.162),.482,.447,.045,m['bronze'],'Z')
for i in range(12):
 a=i*math.tau/12;C('hopper rim rivet',(-.18+.47*math.cos(a),.35+.47*math.sin(a),2.18),.012,.026,m['iron'],segments=8)
# Hopper is open; these pieces rest on its tapered inner wall and show its material feed.
for i in range(7):
 a=i*2.399;r=.20+(.04 if i%2 else 0);p=(-.18+r*math.cos(a),.35+r*math.sin(a),1.91)
 B('retort charge fragment',p,(.12,.09,.07),m['fired-ore-residue'],bevel=.018)
# Separate brick flue at the firebox rear, hollow at its working outlet.
for course in range(12):
 z=.64+course*.12
 for dx,dy,wx,wy in [(-.13,0,.10,.36),(.13,0,.10,.36),(0,-.13,.16,.10),(0,.13,.16,.10)]:B('bonded flue brick',(-1.02+dx,.76+dy,z),(wx,wy,.114),m['brick'])
ring('smoke outlet collar',(-1.02,.76,2.02),.19,.125,.07,m['iron'],'Z')
pipe('firebox to flue throat',[(-.72,.76,.39),(-1.02,.76,.39),(-1.02,.76,.66)],.09,.065,m['iron'])
# Fixed source sockets are north (+Y) inlet and south (-Y) acid outlet.
pipe('steam water inlet',[(0,1.5,.20),(0,1.30,.20),(.30,1.10,.20),(.42,.92,.40),(.42,.72,.92),(.32,.68,1.03)],.075,.051)
pipe('stoneware acid outlet',[(-.55,-.02,.77),(-.82,-.15,.60),(-.94,-.30,.22),(-.94,-1.04,.20),(-.80,-1.23,.20),(-.20,-1.28,.20),(0,-1.40,.20),(0,-1.5,.20)],.072,.049,m['salt-glazed-stoneware'])
for y in (-1.48,1.48):
 ring('fixed player pipe flange',(0,y,.20),.17,.09,.055,m['iron'],'Y')
 for a in (0,math.pi/2,math.pi,math.pi*1.5):bolt('pipe flange stud',(.132*math.cos(a),y,.20+.132*math.sin(a)),'Y',.015,.08)
for p in ((.42,.92,.22),(-.94,-.40,.12),(-.94,-.95,.12),(-.35,-1.27,.12)):
 B('pipe load cradle',p,(.20,.20,.08),m['worked-sandstone'])
ring('inlet stop valve gland',(.42,.72,.92),.09,.054,.06,m['bronze'],'Z')
C('inlet valve spindle',(.42,.72,1.04),.018,.18,m['bronze'])
B('inlet valve cross handle',(.42,.72,1.13),(.20,.025,.025),m['iron'])
# Supported press construction retains the two old jaw meshes as fitted uprights.
for x in (.45,1.07):
 B('press foot shoe',(x,-.65,.12),(.27,.29,.08),m['iron'])
 for yy in (-.74,-.56):bolt('foot anchor',(x,yy,.175))
 B('press bearing cheek',(x,-.65,1.85),(.21,.23,.22),m['wood'])
 hole=C('temporary bearing bore',(x,-.65,1.85),.038,.30,m['iron'],'X');boolean(bpy.data.objects['SHALER | press bearing cheek' if x==.45 else 'SHALER | press bearing cheek.001'],hole)
 ring('bored press shaft bush',(x,-.65,1.85),.063,.033,.25,m['bronze'])
 post=bpy.data.objects['SHALER | REUSED shaler_jaw_left' if x==.45 else 'SHALER | REUSED shaler_jaw_right'];boolean(post,C('temporary upright shaft bore',(x,-.65,1.85),.038,.30,m['iron'],'X'))
 beam('rear press stay',(x,-.65,1.53),(x,.02,.10),.09)
 B('press rear heel',(x,.02,.115),(.23,.24,.07),m['iron'])
B('press top tie',(.76,-.65,2.00),(.89,.23,.15),m['wood'])
guide=B('bored sliding ram guide',(.76,-.65,1.47),(.86,.23,.16),m['wood']);boolean(guide,C('temporary guide bore',(.76,-.65,1.47),.055,.30,m['iron']))
ring('guide bronze liner',(.76,-.65,1.47),.066,.043,.17,m['bronze'],'Z')
for x in (.45,1.07):
 B('tie iron cheek strap',(x,-.779,1.98),(.14,.025,.22),m['iron'])
 for z in (1.91,2.04):bolt('tie cheek bolt',(x,-.802,z),'Y')
C('fixed cam axle',(.86,-.65,1.85),.030,1.09,m['iron'],'X')
cam=E('eccentric press cam',(.76,-.65,1.85));C('cam rolling face',(0,.04,0),.18,.11,m['iron'],'X',cam)
ram=E('guided packing ram',(.76,-.65,.51));B('canister pressure platen',(0,0,0),(.37,.35,.04),m['iron'],ram)
C('sliding ram rod',(0,0,.57),.040,1.10,m['iron'],parent=ram)
B('flat cam follower',(0,0,1.135),(.18,.25,.05),m['bronze'],ram)
# The packing canister rests in a rigid cradle, never floating with the plunger.
C('packing canister',(.76,-.65,.27),.145,.36,m['iron'])
for z in (.12,.42):ring('packing canister rolled rim',(.76,-.65,z),.16,.135,.035,m['bronze'],'Z')
B('canister bottom seat',(.76,-.65,.095),(.36,.37,.035),m['wood'])
for x in (.56,.96):B('canister retaining block',(x,-.65,.21),(.075,.28,.19),m['wood'])
for sign in (-1,1):
 B('ore chute side rail',(-.42+sign*.31,-.96,.36),(.055,.58,.12),m['wood'])
 B('chute bracket',(-.42+sign*.27,-.96,.19),(.07,.18,.22),m['wood'])
for i in range(8):
 bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1,radius=1);ore=bpy.context.object
 for collection in tuple(ore.users_collection):collection.objects.unlink(ore)
 col.objects.link(ore);ore.name='SHALER | processed mineral fragment';ore.parent=root
 for point in ore.data.vertices:point.co*=float(rng.uniform(.82,1.15))
 ore.scale=(float(rng.uniform(.048,.065)),float(rng.uniform(.045,.060)),float(rng.uniform(.030,.050)))
 bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 ore.rotation_euler.z=float(rng.uniform(0,math.tau));ore.location=(-.62+(i%4)*.12,-1.10+(i//4)*.15,.33-min(v.co.z for v in ore.data.vertices));surfaces.apply(ore,m['fired-ore-residue'])
pipe('closed retort solids discharge',[(-.35,-.12,.78),(-.42,-.35,.56),(-.42,-.69,.41)],.12,.09,m['iron'])
for x in (.57,.95):B('canister loading skid',(x,-1.03,.12),(.05,.49,.07),m['wood'])
# Retort steam drives a bored horizontal engine; a closed hemp belt drives the press.
LOW=Vector((1.28,.45,.65));UP=Vector((1.28,-.65,1.85));DIST=(UP-LOW).length;PULLEY=DIST/(2*math.pi);PERIM=2*DIST+math.tau*PULLEY
wheel=E('engine crank flywheel',LOW);drive=E('upper driven pulley',UP)
for parent in (wheel,drive):
 ring('belt pulley rim',(0,0,0),PULLEY+.013,PULLEY-.035,.08,m['iron'],'X',parent)
 C('pulley bored hub',(0,0,0),.063,.10,m['bronze'],'X',parent)
 for i in range(6):
  a=i*math.tau/6;beam('pulley spoke',(0,.055*math.cos(a),.055*math.sin(a)),(0,(PULLEY-.02)*math.cos(a),(PULLEY-.02)*math.sin(a)),.028,m['iron'],parent)
pin=C('engine retained crank pin',(-.16,.05,0),.019,.07,m['bronze'],'X',wheel)
B('engine load pier',(1.08,.45,.32),(.20,.25,.48),m['wood'])
ring('lower crank bearing',(1.08,.45,.65),.068,.031,.12,m['bronze'])
C('lower axle',(1.18,.45,.65),.030,.39,m['iron'],'X')
ring('bored engine cylinder',(1.12,.99,.65),.087,.032,.30,m['iron'],'Y')
ring('engine gland',(1.12,.835,.65),.10,.025,.045,m['bronze'],'Y')
for z in (.59,.71):bolt('cylinder head bolt',(1.12,1.15,z),'Y')
B('cylinder cradle',(1.12,.99,.45),(.24,.38,.22),m['wood'])
for y in (.85,1.13):B('cylinder retaining saddle',(1.12,y,.53),(.25,.045,.06),m['iron'])
slider=E('engine crosshead',(1.12,.70,.65));shoe=B('engine crosshead shoe',(0,0,0),(.21,.06,.17),m['bronze'],slider)
bpy.context.view_layer.update()
for x in (1.04,1.20):boolean(shoe,C('temporary crosshead rail bore',(x,.70,.59),.017,.18,m['iron'],'Y'))
piston=C('engine guided piston',(1.12,.925,.65),.022,.45,m['iron'],'Y');piston.rotation_euler.x=-math.pi/2
for x in (1.04,1.20):
 C('crosshead fixed rail',(x,.76,.59),.013,.45,m['iron'],'Y')
 B('rail support',(x,.96,.54),(.06,.07,.13),m['iron'])
rod=C('rigid engine connecting rod',(1.12,.55,.65),.015,.25,m['iron'])
pipe('contained engine steam feed',[(.32,.68,1.03),(.65,.79,1.03),(.87,.98,.91),(1.12,1.08,.74)],.031,.018)
# Analytic equal-pulley belt. Three revolutions pay exactly one belt circuit per loop.
direction=(UP-LOW).normalized();normal=Vector((0,-direction.z,direction.y));ANGLE=math.atan2(direction.z,direction.y)
def belt_at(s):
 s%=PERIM
 if s<DIST:return LOW+normal*PULLEY+direction*s,direction
 s-=DIST
 if s<math.pi*PULLEY:
  a=s/PULLEY;return UP+PULLEY*(normal*math.cos(a)+direction*math.sin(a)),(-normal*math.sin(a)+direction*math.cos(a))
 s-=math.pi*PULLEY
 if s<DIST:return UP-normal*PULLEY-direction*s,-direction
 s-=DIST;a=s/PULLEY
 return LOW+PULLEY*(-normal*math.cos(a)-direction*math.sin(a)),normal*math.sin(a)-direction*math.cos(a)
sample=[tuple(belt_at(PERIM*i/160)[0]) for i in range(161)]
beltverts=[]
for p in sample:
 for x in (-.022,.022):beltverts.append(tuple(Vector(p)+Vector((x,0,0))))
belt=mesh('SHALER | continuous closed hemp belt',beltverts,[(2*i,2*i+1,2*i+3,2*i+2) for i in range(160)],m['hemp-drive-belt'],col,root);surfaces.physical_box_uv(belt)
solid=belt.modifiers.new('Real belt thickness','SOLIDIFY');solid.thickness=.012
splices=[B('travelling belt splice',(0,0,0),(.052,.035,.015),m['bronze']) for _ in range(3)]
# Every moving joint is driven by the same crank phase; pulley/belt/cam paths close.
for frame in range(1,194):
 phase=math.tau*(frame-1)/192;theta=phase*3
 wheel.rotation_euler.x=theta;drive.rotation_euler.x=theta;cam.rotation_euler.x=theta
 crank=Vector((1.12,.45+.05*math.cos(theta),.65+.05*math.sin(theta)))
 slide=Vector((1.12,crank.y+math.sqrt(.25**2-(crank.z-.65)**2),.65));slider.location=slide
 piston.location=(1.12,slide.y+.225,.65);rod.location=(crank+slide)/2;rod.rotation_euler=(crank-slide).to_track_quat('Z','Y').to_euler()
 ram.location.z=.51+.04*math.sin(theta)
 for actor in (wheel,drive,cam):actor.keyframe_insert(data_path='rotation_euler',frame=frame)
 for actor in (slider,piston,rod,ram):actor.keyframe_insert(data_path='location',frame=frame)
 rod.keyframe_insert(data_path='rotation_euler',frame=frame)
 for i,actor in enumerate(splices):
  p,t=belt_at(PERIM*((frame-1)/192+i/3));actor.location=p;actor.rotation_euler=t.to_track_quat('Y','X').to_euler();actor.keyframe_insert(data_path='location',frame=frame);actor.keyframe_insert(data_path='rotation_euler',frame=frame)
repairs={}
for obj in root.children_recursive:
 if obj.type!='MESH':continue
 if obj.modifiers:
  data=bpy.data.meshes.new_from_object(obj.evaluated_get(bpy.context.evaluated_depsgraph_get()));obj.modifiers.clear();obj.data=data
 if not obj.data.uv_layers:surfaces.physical_box_uv(obj)
 bm=bmesh.new();bm.from_mesh(obj.data);bmesh.ops.triangulate(bm,faces=list(bm.faces));bmesh.ops.delete(bm,geom=[v for v in bm.verts if not v.link_faces],context='VERTS');bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-7);bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=1e-7);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(obj.data);bm.free()
 obj.data.calc_loop_triangles();bad={t.polygon_index for t in obj.data.loop_triangles if t.area<1e-12}
 if bad:
  bm=bmesh.new();bm.from_mesh(obj.data);bm.faces.ensure_lookup_table();bmesh.ops.delete(bm,geom=[bm.faces[i] for i in bad],context='FACES');bm.to_mesh(obj.data);bm.free();repairs[obj.name]=len(bad)
 if obj.animation_data:
  for layer in obj.animation_data.action.layers:
   for strip in layer.strips:
    for bag in strip.channelbags:
     for curve in bag.fcurves:
      for key in curve.keyframe_points:key.interpolation='LINEAR'
profile={'camera_policy':'fmpl.factorio45.v1','capture_kind':'entity','orientation_policy':'rotatable','directions':[0,90,180,270],'states':{'idle':[0],'working':list(range(1,193,12))},'source_size':256,'fps':4,'camera_override':{'type':'ORTHO','elevation_deg':45,'azimuth_deg':0,'distance':math.sqrt(72),'ortho_scale':5.6,'target':[0,0,1.0]}}
scene.frame_start=1;scene.frame_end=193;scene.render.fps=48;scene.render.resolution_x=scene.render.resolution_y=256;scene.render.resolution_percentage=100
install_canonical_camera(scene,profile,bpy);scene.frame_set(1);assert_clean(scene,profile,bpy);bpy.ops.file.pack_all()
source=O/'shaler-v1.blend';bpy.ops.wm.save_as_mainfile(filepath=str(source),compress=True);bpy.ops.wm.open_mainfile(filepath=str(source));scene=bpy.context.scene;root=bpy.data.objects['EXPORT | Shaler all authored parts']
bpy.ops.object.select_all(action='DESELECT')
for obj in [root,*root.children_recursive]:obj.select_set(True)
bpy.ops.export_scene.gltf(filepath=str(O/'shaler-v1.glb'),export_format='GLB',use_selection=True,export_cameras=False,export_lights=False,export_animations=True,export_animation_mode='SCENE',export_anim_scene_split_object=False,export_frame_range=True,export_force_sampling=True,export_frame_step=1,export_apply=True,export_extras=True)
(O/'capture-profile.json').write_text(json.dumps(profile,indent=2)+'\n')
(O/'construction-receipt.json').write_text(json.dumps(dict(source_sha256=sha(source),glb_sha256=sha(O/'shaler-v1.glb'),starter_sha256=sha(starter),reused_groups=reused,repaired_degenerate_faces=repairs,belts=dict(radius=PULLEY,center_distance=DIST,perimeter=PERIM,turns_per_loop=3),native_sockets=contract['ports'],owner_visual_approved=False,native_integrated=False),indent=2)+'\n')
projection=bpy.data.objects.new('SPRITE ONLY | square ground grid',None);scene.collection.objects.link(projection);projection.scale.y=math.sqrt(2);root.parent=projection
scene.render.resolution_x=scene.render.resolution_y=512
for name,yaw in [('front',0),('east',270),('rear',180),('west',90)]:
 root.rotation_euler.z=math.radians(yaw);scene.frame_set(49);scene.render.filepath=str(O/(name+'-review512.png'));bpy.ops.render.render(write_still=True)
print('SHALER_SOURCE_SAVED',source,flush=True)
