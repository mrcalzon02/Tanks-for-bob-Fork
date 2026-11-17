"""Tracked Calcifier starter refined as a heated wet-mineral mixer, not an invented lime recipe."""
import bpy,bmesh,json,math,sys,tempfile,hashlib
import numpy as np
from pathlib import Path
from mathutils import Vector
H=Path(__file__).resolve().parent;R=H.parents[3];O=R/'models/island-survival/calcifier/candidates/v1-production01'
if O.exists():raise FileExistsError(O)
O.mkdir(parents=True);tempfile.tempdir=str(R/'build/quarry-export-temp')
sys.path.insert(0,str(R/'models/island-survival/primitive-steam-powered-pump/v3'))
from mesh_util import mesh,box,cylinder,tube,lathe
import surfaces
sys.path.insert(0,str(R.parent/'model-production/tools/fmpl'))
from blender_camera_guard import install_canonical_camera,assert_clean,temporary_inspection_camera
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
contract=json.loads((H/'contract.json').read_text());starter=H/'starter-calcifier.obj';assert sha(starter)==contract['source']['sha256']
bpy.ops.wm.read_factory_settings(use_empty=True);scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=48;scene.cycles.use_denoising=False;scene.render.film_transparent=True;scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA'
scene.world=bpy.data.worlds.new('Calcifier workshop environment');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.22,.22,.22,1)
for pos,power,size in [((4,-4,7),700,5),((-4,2,5),450,4),((0,2,7),250,3)]:
 light=bpy.data.lights.new('Workshop area','AREA');light.energy=power;light.size=size;obj=bpy.data.objects.new('Workshop area',light);scene.collection.objects.link(obj);obj.location=pos;obj.rotation_euler=(Vector((0,0,1.0))-obj.location).to_track_quat('-Z','Y').to_euler()
root=bpy.data.objects.new('EXPORT | Calcifier all authored parts',None);scene.collection.objects.link(root);col=bpy.data.collections.new('CALCIFIER | heated mineral bed and geared paddle machinery');scene.collection.children.link(col)
m=surfaces.create(O);rng=np.random.default_rng(171150);u,v=np.meshgrid(np.linspace(0,1,512),np.linspace(0,1,512));broad=surfaces.field(rng,(512,512),.012);fine=surfaces.field(rng,(512,512),.19)
for name,color,rough in [('worked-stone',(.30,.285,.245),.9),('refractory-liner',(.29,.205,.13),.85),('wet-mineral-bed',(.35,.365,.31),.43),('chalky-crystal-growth',(.49,.495,.42),.73),('ash-and-coal',(.043,.037,.028),.96),('reinforced-lagging',(.14,.105,.064),.9)]:
 detail=.012*broad+.005*fine
 if name=='wet-mineral-bed':detail+=.012*np.sin(u*135+v*23)*np.sin(v*147-u*25)
 if name=='reinforced-lagging':detail+=.012*np.sin(u*230+v*40)*np.sin(v*280-u*30)
 m[name]=surfaces.material('calcifier-'+name,np.stack([x+detail for x in color],axis=-1),rough+.025*fine,.5+.025*broad+.008*fine,0,O)
for material in m.values():material.name=material.name.replace('PUMP V3','CALCIFIER');material['surface_authorship']='Calcifier mineral/steam-water roles: wet growth bed, chalky product, refractory bowl, bonded firebrick, supported timber grain/endgrain, bronze journals and lagged copper circuits'
def B(n,p,d,material,parent=root,bevel=.006):
 o=box('CALCIFIER | '+n,p,d,material,col,parent,bevel);surfaces.apply(o,material,m['endgrain'] if material==m['wood'] else None);return o
def C(n,p,r,d,material,axis='Z',parent=root,segments=48):
 o=cylinder('CALCIFIER | '+n,p,r,d,material,col,parent,axis,segments);surfaces.apply(o,material);return o
def E(n,p=(0,0,0),parent=root):
 o=bpy.data.objects.new('CALCIFIER | '+n,None);col.objects.link(o);o.parent=parent;o.location=p;return o
def beam(n,a,b,w,material=m['wood'],parent=root):
 a,b=Vector(a),Vector(b);o=B(n,(a+b)/2,(w,w,(b-a).length),material,parent);o.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler();return o
def bore(obj,cutter):
 bpy.context.view_layer.update();bpy.context.view_layer.objects.active=obj;mod=obj.modifiers.new('Actual fitted bore','BOOLEAN');mod.object=cutter;mod.operation='DIFFERENCE';mod.solver='EXACT';bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cutter,do_unlink=True)
def ring(n,p,outer,inner,depth,material,axis='Z',parent=root):
 t=Vector({'X':(1,0,0),'Y':(0,1,0),'Z':(0,0,1)}[axis]);o=tube('CALCIFIER | '+n,[(-t*depth/2,t,outer,inner),(t*depth/2,t,outer,inner)],material,col,parent,40);o.location=p;return o
def bolt(n,p,axis='Z',parent=root):return C(n,p,.019,.03,m['bronze'],axis,parent,6)
def circuit(n,points,outer=.035,inner=.023,material=m['copper']):
 controls=[Vector(p) for p in points];pts=[]
 for i in range(len(controls)-1):
  p0,p1,p2,p3=controls[max(0,i-1)],controls[i],controls[i+1],controls[min(len(controls)-1,i+2)]
  for k in range(10):
   t=k/10;pts.append(.5*(2*p1+(-p0+p2)*t+(2*p0-5*p1+4*p2-p3)*t*t+(-p0+3*p1-3*p2+p3)*t*t*t))
 pts.append(controls[-1]);samples=[(p,(pts[min(i+1,len(pts)-1)]-pts[max(0,i-1)]).normalized(),outer,inner) for i,p in enumerate(pts)]
 o=tube('CALCIFIER | '+n,samples,material,col,root,32)
 for index in (0,-1):
  p,t,_,_=samples[index];f=ring(n+' end union',p,outer+.018,inner,.05,m['bronze']);f.rotation_euler=t.to_track_quat('Z','Y').to_euler()
 return o
# The six named starter components remain editable, with gravity-correct open vessels.
verts=[];groups={};group=None
for line in starter.read_text().splitlines():
 t=line.split()
 if not t:continue
 if t[0]=='v':verts.append(Vector(map(float,t[1:])))
 elif t[0]=='g':group=t[1];groups[group]=[]
 elif t[0]=='f':groups[group].append([int(x)-1 for x in t[1:]])
reused=[]
for name,faces in groups.items():
 ids=sorted({i for f in faces for i in f});lookup={i:j for j,i in enumerate(ids)};pts=[verts[i].copy() for i in ids];fs=[tuple(lookup[i] for i in f) for f in faces];material=m['worked-stone'];solid=None
 if name.endswith('_base'):pts=[(p.x,p.y,p.z*.2) for p in pts]
 elif name.endswith('_kiln_drum'):
  fs=[f for f in fs if not all(abs(pts[i].z-1.735)<.001 for i in f)];pts=[(-.30+p.x*.82,.05+p.y*.82,.55+(p.z-.385)*.70) for p in pts];material=m['refractory-liner'];solid=.07
 elif name.endswith('_mineral_hopper'):
  fs=[f for f in fs if len({round(pts[i].z,3) for i in f})>1];pts=[(-.87+p.x*.50,.92+p.y*.50,1.64+(2.27-p.z)*.90) for p in pts];material=m['copper'];solid=.022
 elif name.endswith('_furnace_door'):
  pts=[(-.30+p.x*.75,-.74+(p.y+.76)*.30,.35+(p.z-.64)*.50) for p in pts];material=m['iron']
 elif name.endswith('_exhaust'):
  fs=[f for f in fs if len({round(pts[i].z,3) for i in f})>1];pts=[(.99+(p.x-.65)*.70,1.05+(p.y-.45)*.70,1.55+(p.z-1.68)*.78) for p in pts];material=m['iron'];solid=.024
 elif name.endswith('_coal_rake'):
  pts=[(-1.15+(p.x-1.02)*.68,-1.15+(p.y+.65),.17+(p.z-.24)*.80) for p in pts];material=m['ash-and-coal']
 obj=mesh('CALCIFIER | REUSED '+name,pts,fs,material,col,root);surfaces.apply(obj,material);reused.append(obj.name)
 if solid:mod=obj.modifiers.new('Real open vessel wall','SOLIDIFY');mod.thickness=solid;mod.offset=0
 bevel=obj.modifiers.new('Worked edge easing','BEVEL');bevel.width=.009;bevel.segments=3
# Individual hearth masonry supports the refractory bowl rather than a generic enclosing box.
for layer in range(4):
 z=.13+layer*.115
 for x in (-.96,.36):
  for j in range(5):B('bonded hearth side brick',(x,-.49+j*.27,z),(.15,.255,.108),m['brick'])
 for j in range(5):B('rear hearth brick',(-.84+j*.27,.67,z),(.255,.15,.108),m['brick'])
 for sign in (-1,1):B('stoke arch jamb',(-.30+sign*.49,-.58,z),(.32,.16,.108),m['brick'])
for i in range(7):
 a=math.pi*(i+.5)/7;o=B('stoke arch voussoir',(-.30+.29*math.cos(a),-.58,.22+.29*math.sin(a)),(.12,.17,.14),m['brick']);o.rotation_euler.y=math.pi/2-a
B('hearth cap carrying bowl',(-.30,.05,.54),(1.43,1.40,.065),m['worked-stone'])
for z in (.74,1.02,1.30):ring('bowl external iron hoop',(-.30,.05,z),.66,.628,.05,m['iron'])
ring('bowl rolled upper rim',(-.30,.05,1.495),.67,.588,.045,m['bronze'])
C('wet mineral growth bed',(-.30,.05,.95),.555,.025,m['wet-mineral-bed'])
water=lathe('CALCIFIER | wetted mineral surface',[(0,1.015),(.55,1.015),(.55,1.023),(0,1.023)],(-.30,.05),m['wet-mineral-bed'],col,root,64);surfaces.apply(water,m['wet-mineral-bed'])
ring('sealed lower mixer journal',(-.30,.05,.68),.095,.040,.19,m['bronze'])
# Continuous supported flue: brick pedestal to paving, then the reused metal exhaust.
B('flue stone footing',(.99,1.05,.14),(.43,.43,.136),m['worked-stone'])
for course in range(12):
 z=.24+course*.115
 for dx,dy,wx,wy in [(-.11,0,.09,.31),(.11,0,.09,.31),(0,-.11,.13,.09),(0,.11,.13,.09)]:B('bonded flue pedestal',(.99+dx,1.05+dy,z),(wx,wy,.108),m['brick'])
ring('flue supported lower collar',(.99,1.05,1.55),.15,.108,.07,m['bronze'])
ring('flue open mouth',(.99,1.05,2.30),.15,.108,.045,m['iron'])
circuit('hearth combustion passage',[(.36,.55,.36),(.65,.69,.36),(.99,1.05,.36),(.99,1.05,.61)],.075,.055,m['iron'])
# Four braced posts carry both vertical journals and the hopper; no suspended masonry.
for x in (-1.25,1.14):
 for y in (-.85,.65):
  B('timber drive frame post',(x,y,1.06),(.13,.16,1.976),m['wood']);B('post anchored iron shoe',(x,y,.12),(.20,.23,.09),m['iron'])
  for yy in (y-.075,y+.075):bolt('frame foot anchor',(x,yy,.18))
 B('upper side frame beam',(x,-.10,2.04),(.14,1.64,.16),m['wood'])
 beam('rear frame diagonal',(x,-.85,.17),(x,.65,1.88),.075)
header=B('mixer journal crossbeam',(-.055,.05,2.00),(2.49,.16,.14),m['wood'])
for x,r in ((-.30,.044),(.63,.038)):
 bore(header,C('temporary vertical shaft bore',(x,.05,2.00),r,.30,m['iron']));ring('upper vertical shaft bronze bush',(x,.05,2.00),r+.027,r,.16,m['bronze'])
for x in (-1.25,1.14):
 B('frame iron cheek strap',(x,-.096,2.00),(.12,.025,.23),m['iron'])
 for z in (1.92,2.08):bolt('crossbeam retaining bolt',(x,-.12,z),'Y')
# Reused hopper is supported at its neck and rim and feeds below the turning gear plane.
ring('rolled open feed hopper rim',(-.87,.92,2.198),.415,.383,.045,m['bronze'])
ring('feed hopper neck union',(-.87,.92,1.64),.073,.032,.06,m['bronze'])
beam('hopper neck bracket',(-1.25,.65,1.55),(-.87,.92,1.59),.07,m['iron'])
beam('hopper rim bracket',(-1.25,.65,2.04),(-1.12,.78,2.08),.06,m['iron'])
circuit('mineral feed downspout',[(-.87,.92,1.64),(-.78,.85,1.56),(-.70,.70,1.48),(-.55,.43,1.34)],.065,.044,m['copper'])
# The genuine inlet distributes water or steam; the south output has no current recipe use.
circuit('north water steam inlet',[(0,1.5,.20),(0,1.29,.20),(.31,1.10,.24),(.45,.82,.48),(.34,.52,.88),(.28,.43,1.14)],.075,.051)
circuit('capped spare south outlet',[(0,-1.10,.20),(0,-1.34,.20),(0,-1.50,.20)],.075,.051,m['iron'])
for y in (-1.48,1.48):
 ring('fixed player pipe flange',(0,y,.20),.17,.09,.055,m['iron'],'Y')
 for a in (0,math.pi/2,math.pi,math.pi*1.5):bolt('pipe flange stud',(.132*math.cos(a),y,.20+.132*math.sin(a)),'Y')
C('blanked unused process outlet',(0,-1.51,.20),.091,.018,m['iron'],'Y')
# Small opposed spray/steam lances aim into the actual mineral bed.
for sign in (-1,1):
 circuit('mineral bed lance',[(.28,.43,1.14),(.08,.58,1.27),(-.30+sign*.47,.48,1.34),(-.30+sign*.42,.34,1.20)],.022,.013)
ring('inlet stop valve gland',(.34,.52,.88),.071,.049,.05,m['bronze'])
C('inlet valve spindle',(.34,.52,.99),.016,.17,m['bronze']);B('inlet cross handle',(.34,.52,1.08),(.17,.025,.025),m['iron'])
# Geared paddle assembly uses a bored shaft and real attached mixing blades.
mix=E('mineral paddle gear and shaft',(-.30,.05,1.78));pinion=E('vertical 31 tooth pinion',(.63,.05,1.78))
C('main turning paddle shaft',(0,0,-.35),.035,1.40,m['iron'],parent=mix)
for i in range(4):
 a=i*math.pi/2
 beam('mixing sweep arm',(.10*math.cos(a),.10*math.sin(a),-.66),(.47*math.cos(a),.47*math.sin(a),-.66),.045,m['iron'],mix)
 blade=B('mineral stirring blade',(.41*math.cos(a),.41*math.sin(a),-.735),(.22,.045,.15),m['iron'],mix);blade.rotation_euler.z=a+math.pi/2
 C('paddle fastening pin',(.41*math.cos(a),.41*math.sin(a),-.64),.019,.08,m['bronze'],parent=mix)
def conical_teeth(n,parent,axis,teeth=18):
 points=[];N=teeth*5
 for z in (-.17,-.10):
  for tooth in range(teeth):
   for frac,tip in [(-.5,False),(-.30,False),(-.18,True),(.18,True),(.30,False)]:
    a=math.tau*(tooth+frac)/teeth;rad=-z+(.010 if tip else -.009);points.append((rad*math.cos(a),rad*math.sin(a),z))
 faces=[(i,(i+1)%N,(i+1)%N+N,i+N) for i in range(N)]
 for z,reverse in ((-.17,True),(-.10,False)):
  start=len(points);points.extend((.033*math.cos(i*math.tau/N),.033*math.sin(i*math.tau/N),z) for i in range(N));outer=0 if reverse else N
  for i in range(N):
   j=(i+1)%N;face=(outer+i,outer+j,start+j,start+i);faces.append(tuple(reversed(face)) if reverse else face)
  other=start-N if not reverse else None
 for i in range(N):j=(i+1)%N;faces.append((2*N+i,3*N+i,3*N+j,2*N+j))
 o=mesh('CALCIFIER | '+n,points,faces,m['bronze'],col,parent);o.rotation_euler.y=math.pi/2 if axis=='X' else 0;o.rotation_euler.x=-math.pi/2 if axis=='Y' else 0;surfaces.apply(o,m['bronze']);return o

def spur(n,parent,pitch,teeth,inner,material):
 N=teeth*5;verts=[]
 for y in (-.035,.035):
  for tooth in range(teeth):
   for frac,tip in [(-.5,False),(-.30,False),(-.18,True),(.18,True),(.30,False)]:
    a=math.tau*(tooth+frac)/teeth;rr=pitch+(.0115 if tip else -.0115);verts.append((rr*math.cos(a),y,rr*math.sin(a)))
 for y in (-.035,.035):verts.extend((inner*math.cos(i*math.tau/N),y,inner*math.sin(i*math.tau/N)) for i in range(N))
 faces=[]
 for i in range(N):
  j=(i+1)%N;faces.extend([(i,j,N+j,N+i),(2*N+j,2*N+i,3*N+i,3*N+j),(i,2*N+i,2*N+j,j),(N+j,3*N+j,3*N+i,N+i)])
 o=mesh('CALCIFIER | '+n,verts,faces,material,col,parent);surfaces.apply(o,material);return o

# Fore-facing piston engine and closed belt feed the right-angle pinion transmission.
LOW=Vector((1.00,-.55,1.05));UP=Vector((.63,-.55,1.55));DIST=(UP-LOW).length;PULLEY=DIST/math.pi;PERIM=2*DIST+math.tau*PULLEY
fly=E('engine crank flywheel',LOW);pulley=E('upper belt pulley',UP)
for actor in (fly,pulley):
 ring('drive pulley rim',(0,0,0),PULLEY+.014,PULLEY-.025,.075,m['iron'],'Y',actor);C('pulley central hub',(0,0,0),.055,.10,m['bronze'],'Y',actor)
 for i in range(6):
  a=i*math.tau/6;beam('pulley spoke',(.045*math.cos(a),0,.045*math.sin(a)),((PULLEY-.015)*math.cos(a),0,(PULLEY-.015)*math.sin(a)),.025,m['iron'],actor)
crank=C('retained engine crank pin',(.06,-.085,0),.018,.12,m['bronze'],'Y',fly)
slider=E('guided engine crosshead',(1.00,-.635,.76));shoe=B('bored engine crosshead',(0,0,0),(.31,.08,.09),m['bronze'],slider)
for x in (-.13,.13):bore(shoe,C('temporary crosshead rail bore',(x,0,0),.017,.16,m['iron'],parent=slider))
for x in (.87,1.13):C('fixed engine crosshead rail',(x,-.635,.78),.012,.40,m['iron'])
piston=C('engine rigid piston',(1.00,-.635,.585),.022,.35,m['iron']);rod=C('engine rigid connecting arm',(1.00,-.635,.90),.016,.29,m['iron'])
ring('bored engine cylinder',(1.00,-.635,.50),.085,.040,.30,m['iron']);ring('packed engine piston gland',(1.00,-.635,.656),.10,.026,.045,m['bronze'])
B('engine stone load block',(1.00,-.635,.24),(.29,.28,.32),m['worked-stone'])
for z in (.30,.58,.98):
 bar=B('engine guide crossmember',(1.00,-.57,z),(.37,.18,.045),m['wood'])
 if z==.58:bore(bar,C('temporary cylinder clearance',(1.00,-.635,z),.095,.15,m['iron']))
for x in (.82,1.18):B('engine guide upright',(x,-.48,.52),(.055,.07,.88),m['wood'])
for y in (-.43,-.23):
 pier=B('upper pulley journal pier',(.63,y,1.05),(.14,.13,.98),m['wood']);bore(pier,C('temporary upper pulley shaft slot',(.63,y,1.55),.036,.30,m['iron'],'Y'));ring('upper pulley bored journal',(.63,y,1.55),.067,.032,.15,m['bronze'],'Y')
C('upper turning shaft',(0,.34,0),.028,.88,m['iron'],'Y',pulley)
miter_y=E('driving 18 tooth miter',(.63,.05,1.55));miter_z=E('driven 18 tooth miter',(.63,.05,1.55))
conical_teeth('driving right angle bevel',miter_y,'Y');conical_teeth('driven vertical bevel',miter_z,'Z')
C('turning pinion shaft',(0,0,-.45),.030,1.44,m['iron'],parent=pinion)
B('lower pinion stone pedestal',(.63,.05,.56),(.27,.27,.16),m['worked-stone']);ring('lower pinion shaft journal',(.63,.05,.66),.075,.035,.10,m['bronze'])
large=spur('62 tooth paddle crown',mix,.62,62,.49,m['iron']);large.rotation_euler.x=math.pi/2
small=spur('31 tooth drive pinion',pinion,.31,31,.20,m['bronze']);small.rotation_euler.x=math.pi/2
for actor,r,count in ((mix,.62,4),(pinion,.31,3)):
 C('gear shaft keyed hub',(0,0,0),.066,.10,m['bronze'],parent=actor)
 for i in range(count):
  a=i*math.tau/count;beam('gear supporting spoke',(.05*math.cos(a),.05*math.sin(a),0),((r-.03)*math.cos(a),(r-.03)*math.sin(a),0),.040,m['iron'],actor)
direction=(UP-LOW).normalized();normal=Vector((-direction.z,0,direction.x))
def belt_at(s):
 s%=PERIM
 if s<DIST:return LOW+normal*PULLEY+direction*s,direction
 s-=DIST
 if s<math.pi*PULLEY:
  a=s/PULLEY;return UP+PULLEY*(normal*math.cos(a)+direction*math.sin(a)),-normal*math.sin(a)+direction*math.cos(a)
 s-=math.pi*PULLEY
 if s<DIST:return UP-normal*PULLEY-direction*s,-direction
 s-=DIST;a=s/PULLEY;return LOW+PULLEY*(-normal*math.cos(a)-direction*math.sin(a)),normal*math.sin(a)-direction*math.cos(a)
points=[belt_at(PERIM*i/144)[0] for i in range(145)];beltverts=[tuple(p+Vector((0,y,0))) for p in points for y in (-.018,.018)]
belt=mesh('CALCIFIER | continuous closed hemp belt',beltverts,[(2*i,2*i+1,2*i+3,2*i+2) for i in range(144)],m['reinforced-lagging'],col,root);surfaces.physical_box_uv(belt);solid=belt.modifiers.new('Real belt thickness','SOLIDIFY');solid.thickness=.012
splices=[B('travelling belt splice',(0,0,0),(.025,.045,.012),m['bronze']) for _ in range(3)]
# Contained thermal circuit and a visibly lagged engine feed loop.
circuit('heated bowl engine supply',[(.28,.43,1.14),(.50,.55,1.32),(.88,.34,1.20),(1.13,-.08,.91),(1.00,-.55,.58)],.031,.019,m['reinforced-lagging'])
circuit('engine return to jacket',[(1.00,-.55,.43),(.82,-.39,.38),(.56,-.12,.55),(.32,.28,.74)],.026,.016)
# Solids leave on a supported slatted draining rack, not through the unused fluid port.
circuit('closed solids discharge',[(-.61,-.39,1.13),(-.68,-.60,.85),(-.66,-.77,.50)],.105,.081,m['copper'])
for x in (-.91,-.41):B('draining rack side rail',(x,-1.03,.35),(.055,.56,.13),m['wood'])
for i in range(6):B('draining rack slat',(-.66,-1.25+i*.09,.31),(.48,.055,.045),m['wood'])
for x in (-.87,-.45):
 for y in (-1.23,-.83):B('rack load bearing leg',(x,y,.18),(.065,.065,.20),m['wood'])
for i in range(9):
 bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1,radius=1);ore=bpy.context.object
 for collection in tuple(ore.users_collection):collection.objects.unlink(ore)
 col.objects.link(ore);ore.parent=root;ore.name='CALCIFIER | mineral growth product'
 for pt in ore.data.vertices:pt.co*=float(rng.uniform(.85,1.12))
 ore.scale=(.045,.048,.04);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);ore.location=(-.81+(i%3)*.14,-1.18+(i//3)*.14,.34-min(v.co.z for v in ore.data.vertices));surfaces.apply(ore,m['chalky-crystal-growth'])
for x in (-1.30,-1.00):B('coal tray retaining rail',(x,-1.15,.25),(.03,.30,.09),m['wood'])
beam('stoke rake handle',(-1.20,-1.31,.09),(-.98,-1.31,.09),.022,m['wood']);B('stoke rake iron head',(-.96,-1.31,.09),(.07,.08,.025),m['iron'])
# Every moving mechanism is constrained by the same phase; there are no free-floating links.
for frame in range(1,194):
 phase=math.tau*(frame-1)/192;theta=phase*2
 fly.rotation_euler.y=theta;pulley.rotation_euler.y=theta;miter_y.rotation_euler.y=theta;miter_z.rotation_euler.z=-theta+math.pi/18;pinion.rotation_euler.z=miter_z.rotation_euler.z;mix.rotation_euler.z=-pinion.rotation_euler.z/2
 pin=Vector((1.00+.06*math.cos(theta),-.635,1.05-.06*math.sin(theta)));slide=Vector((1.00,-.635,pin.z-math.sqrt(.29**2-(pin.x-1.00)**2)))
 slider.location=slide;piston.location=slide-Vector((0,0,.175));rod.location=(pin+slide)/2;rod.rotation_euler=(pin-slide).to_track_quat('Z','Y').to_euler()
 for actor in (fly,pulley,miter_y,miter_z,pinion,mix):actor.keyframe_insert(data_path='rotation_euler',frame=frame)
 for actor in (slider,piston,rod):actor.keyframe_insert(data_path='location',frame=frame)
 rod.keyframe_insert(data_path='rotation_euler',frame=frame)
 for i,actor in enumerate(splices):
  p,t=belt_at(PERIM*((frame-1)/192+i/3));actor.location=p;actor.rotation_euler=t.to_track_quat('X','Y').to_euler();actor.keyframe_insert(data_path='location',frame=frame);actor.keyframe_insert(data_path='rotation_euler',frame=frame)
repairs={}
for obj in root.children_recursive:
 if obj.type!='MESH':continue
 if obj.modifiers:data=bpy.data.meshes.new_from_object(obj.evaluated_get(bpy.context.evaluated_depsgraph_get()));obj.modifiers.clear();obj.data=data
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
profile={'camera_policy':'fmpl.factorio45.v1','capture_kind':'entity','orientation_policy':'rotatable','directions':[0,90,180,270],'states':{'idle':[0],'working':list(range(1,193,12))},'source_size':256,'fps':4,'camera_override':{'type':'ORTHO','elevation_deg':45,'azimuth_deg':0,'distance':math.sqrt(72),'ortho_scale':5.6,'target':[0,0,1.08]}}
scene.frame_start=1;scene.frame_end=193;scene.render.fps=48;scene.render.resolution_x=scene.render.resolution_y=256;scene.render.resolution_percentage=100;install_canonical_camera(scene,profile,bpy);scene.frame_set(1);assert_clean(scene,profile,bpy);bpy.ops.file.pack_all()
native=O/'calcifier-v1.blend';bpy.ops.wm.save_as_mainfile(filepath=str(native),compress=True);bpy.ops.wm.open_mainfile(filepath=str(native));scene=bpy.context.scene;root=bpy.data.objects['EXPORT | Calcifier all authored parts'];bpy.ops.object.select_all(action='DESELECT')
for obj in [root,*root.children_recursive]:obj.select_set(True)
bpy.ops.export_scene.gltf(filepath=str(O/'calcifier-v1.glb'),export_format='GLB',use_selection=True,export_cameras=False,export_lights=False,export_animations=True,export_animation_mode='SCENE',export_anim_scene_split_object=False,export_frame_range=True,export_force_sampling=True,export_frame_step=1,export_apply=True,export_extras=True)
(O/'capture-profile.json').write_text(json.dumps(profile,indent=2)+'\n');(O/'construction-receipt.json').write_text(json.dumps(dict(source_sha256=sha(native),glb_sha256=sha(O/'calcifier-v1.glb'),starter_sha256=sha(starter),reused_groups=reused,gear_teeth=[18,18,31,62],belt=dict(radius=PULLEY,center_distance=DIST,perimeter=PERIM,turns_per_loop=2),fixed_sockets=contract['ports'],owner_visual_approved=False,native_integrated=False,degenerate_repairs=repairs),indent=2)+'\n')
projection=bpy.data.objects.new('SPRITE ONLY | square ground grid',None);scene.collection.objects.link(projection);projection.scale.y=math.sqrt(2);root.parent=projection;scene.render.resolution_x=scene.render.resolution_y=512
for name,yaw in [('front',0),('east',270),('rear',180),('west',90)]:
 root.rotation_euler.z=math.radians(yaw);scene.frame_set(49);scene.render.filepath=str(O/(name+'-review512.png'));bpy.ops.render.render(write_still=True)
print('CALCIFIER_SOURCE_SAVED',native,flush=True)
