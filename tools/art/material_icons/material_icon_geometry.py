"""Purpose-specific industrial, mineral, biological and administrative prop geometry."""
import math,random
import bpy
from mathutils import Vector
import build_hydrogen_resource_models as p
COLORS={'stone':(.24,.25,.22),'ivory':(.65,.62,.48),'silver':(.36,.40,.40),'red':(.36,.035,.018),
 'ochre':(.42,.29,.09),'brown':(.25,.13,.05),'steel':(.22,.26,.25),'cyan':(.03,.34,.48),
 'magenta':(.35,.055,.22),'green':(.075,.26,.04),'blue':(.035,.15,.37),'amber':(.48,.21,.025),
 'pink':(.39,.18,.14),'cream':(.65,.58,.37),'pale-green':(.34,.43,.19),'violet':(.22,.07,.38),
 'rust':(.27,.08,.025),'olive':(.16,.20,.055),'yellow':(.58,.40,.045),'ash':(.08,.09,.08),
 'teal':(.035,.32,.24),'orange':(.58,.16,.018),'brass':(.34,.22,.06)}
def cx(name,pos,r,depth,mat):
 ob=p.cylinder(name,r,depth,0,mat);ob.rotation_euler.y=math.pi/2;ob.location=pos;return ob
def cy(name,pos,r,depth,mat,vertices=48):
 ob=p.cylinder(name,r,depth,0,mat,vertices=vertices);ob.rotation_euler.x=math.pi/2;ob.location=pos;return ob
def ry(name,pos,r,minor,mat):
 ob=p.ring(name,r,minor,0,mat);ob.rotation_euler.x=math.pi/2;ob.location=pos;return ob
def cone(name,pos,r1,r2,depth,mat,vertices=32):
 bpy.ops.mesh.primitive_cone_add(vertices=vertices,radius1=r1,radius2=r2,depth=depth,location=pos)
 return p.finish(bpy.context.object,name,mat,.008)
def mesh_object(name,vertices,faces,mat,bevel=0):
 mesh=bpy.data.meshes.new(name);mesh.from_pydata(vertices,[],faces);mesh.update()
 ob=bpy.data.objects.new(name,mesh);bpy.context.collection.objects.link(ob);return p.finish(ob,name,mat,bevel)
def chip(name,pos,scale,mat,phase=0):
 x,y,z=pos;a,b,c=scale
 points=[(-.5,-.28),(-.1,-.48),(.47,-.14),(.35,.38),(-.34,.46)]
 verts=[(x+px*a,y+py*b,z+sign*c/2) for sign in [-1,1] for px,py in points]
 n=len(points);faces=[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 ob=mesh_object(name,verts,faces,mat,.004);ob.rotation_euler.y=phase;return ob
def lump(name,pos,scale,mat,seed=2):
 ob=p.sphere(name,pos,scale,mat,2);rng=random.Random(seed)
 for v in ob.data.vertices:v.co*=.87+rng.random()*.22
 return ob
def carve(ob,pos,size):
 bpy.ops.mesh.primitive_cube_add(size=1,location=pos);cut=bpy.context.object;cut.scale=size
 bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);bpy.context.view_layer.objects.active=ob
 mod=ob.modifiers.new('Actual open recess','BOOLEAN');mod.object=cut;mod.operation='DIFFERENCE'
 bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cut,do_unlink=True)
def bowl(m,q):
 r=.48
 if q.get('hopper'):
  cone('Conical assay hopper',(0,0,-.16),.27,.5,.38,m['steel'])
  for x in [-.31,.31]:p.box('Hopper support foot',(x,0,-.36),(.12,.38,.15),m['steel'],.02)
 else:p.cylinder('Thick-walled sample vessel',r,.2,-.12,m['ceramic'] if q.get('ceramic') else m['steel'])
 p.ring('Supported vessel retaining rim',r,.035,0,m['brass'] if q.get('hazard') else m['ceramic'])
 p.cylinder('Contained sample surface',.44,.035,-.015,m['product'])
 if q.get('grains'):
  for i in range(14):
   a=i*2.39996;radius=.07*math.sqrt(i)
   p.sphere('Visible surface inclusion',(radius*math.cos(a),radius*math.sin(a),.02),(.05,.05,.035),m['secondary'] if q.get('ceramic') else m['product'],2)
 if q.get('gel'):lump('Single stabilized gel portion',(0,0,.07),(.35,.31,.12),m['product'])
def granules(m,q):
 for layer,(radius,z) in enumerate([(.46,-.15),(.32,.0),(.18,.15)]):
  count=[16,10,4][layer]
  for i in range(count):
   a=i*math.tau/count+.35*layer;r=radius*(.72+.2*(i%2));pos=(r*math.cos(a),r*math.sin(a)*.72,z)
   size=.095 if not q.get('coarse') else .12
   if q.get('angular'):
    ob=p.box('Angular material grain',pos,(size*1.4,size*1.3,size*1.5),m['product'],.012);ob.rotation_euler=(i*.2,i*.15,i*.55)
   else:p.sphere('Round reactive granule',pos,(size,size*.85,size),m['product'],2)
def flakes(m,q):
 for i in range(12):
  a=i*2.39996;r=.1*math.sqrt(i)
  ob=chip('Broken phase fragment' if q.get('thick') else 'Thin mica-like flake',
   (r*math.cos(a),r*math.sin(a)*.7,-.12+i*.023),(.48,.33,.12 if q.get('thick') else .022),m['product'])
  ob.rotation_euler.z=a;ob.rotation_euler.x=(i%3-1)*.13
def mound(m,q):
 lump('Coagulated material mass',(0,0,-.1),(.62,.40,.25),m['product'])
 for i in range(9):
  a=i*2.4;r=.12*math.sqrt(i)
  lump('Coarse surface aggregate',(r*math.cos(a),r*math.sin(a)*.65,.04),(.14,.10,.08),m['product'],i+20)
def bone_dust(m,q):
 mound(m,q);mat=m['dark'] if q.get('bone_color')=='dark' else m['ceramic']
 ob=p.box('Exposed bone shaft',(.05,-.22,.13),(.65,.07,.07),mat,.025);ob.rotation_euler.y=-.14
 for x in [-.3,.36]:
  for z in [.12,.18]:p.sphere('Calcified bone joint',(x,-.22,z),(.075,.07,.065),mat,2)
def porous(m,q):
 ob=lump('Irregular porous ionic crust',(0,0,0),(.61,.30,.34),m['product'],8)
 for x,z,r in [(-.36,-.08,.12),(-.14,.15,.13),(.13,-.12,.14),(.38,.09,.115),(.06,.22,.085)]:
  bpy.ops.mesh.primitive_uv_sphere_add(segments=20,ring_count=12,radius=r,location=(x,-.24,z))
  cut=bpy.context.object;cut.scale.y=1.7;bpy.context.view_layer.objects.active=ob
  mod=ob.modifiers.new('Actual rounded surface pore','BOOLEAN');mod.object=cut;mod.operation='DIFFERENCE'
  bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cut,do_unlink=True)
 if q.get('cage'):
  p.box('Perforated support sole',(0,0,-.24),(1.1,.62,.08),m['steel'],.025)
  for x in [-.53,.53]:p.box('Supported cage side',(x,0,-.06),(.06,.60,.37),m['steel'],.015)
def crystal(m,q):
 from mathutils import Vector
 lump('Mineral growth base',(0,0,-.25),(.52,.35,.13),m['stone'])
 n=q.get('crystals',7)
 for i in range(n):
  a=i*2.4;r=.115*math.sqrt(i);height=(.90 if q.get('broad') else .74)-.085*(i%4)
  radius=.16 if q.get('broad') else .095
  root=Vector((r*math.cos(a),r*math.sin(a)*.7,-.18));direction=Vector((.32*math.cos(a),.25*math.sin(a),1)).normalized()
  stem=p.cylinder('Large planar crystal faces',radius,height,0,m['product'],vertices=5 if q.get('broad') else 6)
  stem.location=root+direction*height/2;stem.rotation_euler=direction.to_track_quat('Z','Y').to_euler()
  tip=cone('Faceted crystal termination',root+direction*(height+.09),radius,0,.18,m['product'],5 if q.get('broad') else 6)
  tip.rotation_euler=stem.rotation_euler
def vessel(m,q):
 style=q.get('vessel','squat')
 height,r={'tall':(1.05,.28),'sediment':(1.14,.22),'baffled':(.94,.28),'cup':(.32,.48),
  'insulated':(.78,.28),'drum':(.63,.42)}.get(style,(.52,.42))
 if style=='pear':
  p.sphere('Bulbous emulsion flask',(0,0,-.02),(.42,.42,.43),m['glass'],4);height=.60;r=.38
 else:p.cylinder('Closed sample vessel',r,height,0,m['steel'])
 for z in [-height/2+.035,height/2-.035]:p.ring('Supported structural retaining band',r+.007,.022,z,m['dark'])
 if style in ['flask','pear']:
  cone('Sloping vessel shoulder',(0,0,height/2+.1),r,.13,.20,m['steel'])
  p.cylinder('Long sealed flask neck',.13,.25,height/2+.28,m['glass'])
  p.cylinder('Ceramic stopper',.16,.08,height/2+.44,m['ceramic'])
 elif style=='cup':
  p.cylinder('Contained gel surface',r-.035,.018,height/2+.025,m['product'])
  p.ring('Thick open ceramic cup rim',r,.035,height/2+.025,m['ceramic'])
 else:
  p.cylinder('Vessel cap',r+.025,.08,height/2+.025,m['ceramic'] if style=='insulated' else m['steel'])
  p.ring('Cap retaining lip',r+.02,.02,height/2+.07,m['brass'])
 width=min(.43,r*1.52)
 p.box('Welded inset sample port boss',(0,-r+.015,0),(width,.13,height*.64),m['dark'],.035)
 p.box('Supported metal port bezel',(0,-r-.045,0),(width-.035,.025,height*.57),m['brass'],.025)
 p.box('Recessed sample glass',(0,-r-.061,0),(width-.105,.012,height*.45),m['product'],.024)
 for x in [-width*.36,width*.36]:
  for z in [-height*.23,height*.23]:p.sphere('Port fastener on welded boss',(x,-r-.067,z),(.018,.011,.018),m['steel'],2)
 if style not in ['pear','flask','cup']:
  for a in range(6):
   angle=a*math.tau/6;p.cylinder('Cap retaining fastener',.021,.025,height/2+.08,m['brass'],xy=(r*.73*math.cos(angle),r*.73*math.sin(angle)))
 if q.get('two_phase'):
  p.box('Lower separated phase',(0,-r-.070,-height*.13),(width-.12,.012,height*.20),m['secondary'],.015)
 if style in ['sediment','tall']:
  p.box('Visible sediment band',(0,-r-.070,-height*.15),(width-.12,.012,.09),m['secondary'],.008)
 if style=='baffled':
  for z in [-.16,0,.16]:p.box('Internal baffle silhouette',(0,-r-.072,z),(width-.12,.01,.025),m['brass'],.004)
 if style=='open':
  p.cylinder('Open dark neck',r*.78,.08,height/2+.12,m['dark'])
  p.cylinder('Glossy sample meniscus',r*.72,.015,height/2+.155,m['product'])
 if style=='insulated':
  for x in [-.16,.16]:p.cylinder('Guarded electrical contact',.045,.16,height/2+.15,m['brass'],xy=(x,0))
def slabs(m,q):
 for i in range(3):
  ob=p.box('Soft edged rendered block',(i*.075-.075,.08-i*.13,-.16+i*.20),(.95,.31,.2),m['product'],.045)
  ob.rotation_euler.z=(i-1)*.06
def glass_sheets(m,q):
 for i in range(3):
  ob=p.box('Thick warped glass pane',(i*.07,.12-i*.10,i*.07),(.96,.045,.66),m['product'],.012)
  for v in ob.data.vertices:
   v.co.y+=.012*math.sin(v.co.x*9+i)
  ob.rotation_euler.y=(i-1)*.08
  for x in [-.48,.48]:p.box('Exposed pale fracture edge',(x+i*.07,.093-i*.10,i*.07),(.012,.012,.64),m['ceramic'],.002)
def cartridge(m,q):
 cx('Cartridge body',(0,0,0),.28,1.05,m['ceramic'])
 for x in [-.54,.54]:cx('Retaining end cap',(x,0,0),.30,.08,m['steel'])
 for z in [-.14,0,.14] if q.get('strips') else [0]:
  p.box('Recessed product sight strip',(0,-.277,z),(.73,.025,.065),m['product'],.012)
 cx('Recessed dispensing nozzle',(.67,0,0),.085,.18,m['dark'])
def twin_vials(m,q):
 p.box('Common vial carrier',(0,0,-.29),(1.12,.64,.12),m['steel'],.025)
 for x in [-.28,.28]:
  p.cylinder('Sealed precursor vial',.19,.67,.10,m['product'],xy=(x,0))
  for z in [-.23,.44]:p.cylinder('Individual insulating cap',.21,.08,z,m['ceramic'],xy=(x,0))
def filter_(m,q):
 p.box('Filter carrier',(0,0,0),(1.1,.20,.85),m['steel'],.035)
 p.box('Folded residue membrane',(0,-.12,.0),(.88,.03,.64),m['product'],.025)
 for x in [-.35,-.18,0,.18,.35]:
  p.tube('Supported filter reinforcement',[(x,-.15,-.31),(x+.02,-.15,.31)],.008,m['ceramic'])
 for x in [-.36,.23]:lump('Crystalline membrane deposit',(x,-.18,.11),(.10,.04,.13),m['secondary'])
def matrix(m,q):
 style=q.get('matrix','gradient')
 for x in [-.42,0,.42]:
  for z in [-.36,0,.36]:
   p.box('Open matrix horizontal beam',(0,x*.6,z),(1.0,.05,.045),m['steel'] if style=='nested' else m['product'],.008)
   p.box('Open matrix vertical web',(x,-.25,z*.1),(.05,.56,.78),m['product'],.008)
 if style=='nested':
  for z in [-.16,.16]:p.box('Nested inner phase support',(0,-.04,z),(.42,.08,.04),m['brass'],.006)
 if style=='charged':
  for x in [-.2,.2]:p.sphere('Contained ionic insert',(x,-.22,0),(.085,.08,.10),m['secondary'],2)
def broken_matrix(m,q):
 matrix(m,{'matrix':'nested'})
 for i in range(4):chip('Broken open cell fragment',(.28+i*.07,-.29,-.4),(.16,.14,.05),m['product'])
def honeycomb(m,q):
 for x,z in [(0,0),(.31,0),(-.31,0),(.15,.27),(-.15,.27),(.15,-.27),(-.15,-.27)]:
  verts=[];n=6
  for y in [-.23,.23]:
   for r in [.18,.125]:
    verts.extend((x+r*math.cos(i*math.tau/n),y,z+r*math.sin(i*math.tau/n)) for i in range(n))
  faces=[]
  for i in range(n):
   j=(i+1)%n
   faces.extend([(i,j,12+j,12+i),(6+i,18+i,18+j,6+j),(i,6+i,6+j,j),(12+i,12+j,18+j,18+i)])
  mesh_object('True open ceramic hexagonal cell',verts,faces,m['product'],.006)
 ry('Outside retaining band',(0,0,0),.55,.025,m['steel'])
def slab_frame(m,q):
 p.box('Compressed mineral slab',(0,0,0),(1.05,.31,.63),m['product'],.015)
 for x in [-.52,.52]:p.box('Side compression shoe',(x,0,0),(.12,.39,.76),m['steel'],.02)
 for z in [-.32,.32]:p.box('Compression carrier rail',(0,-.18,z),(.98,.07,.09),m['brass'],.012)
def preform(m,q):
 ob=p.box('Shaped bioceramic preform',(0,0,0),(1.08,.41,.75),m['product'],.09)
 carve(ob,(0,0,.06),(.60,.55,.4))
 for x in [-.38,.38]:p.box('Integral mounting foot',(x,0,-.43),(.22,.55,.14),m['product'],.03)
def conductive(m,q):
 mound(m,q)
 for i in range(7):
  x=-.4+i*.13;p.tube('Copper filament in residue',[(x,-.23,.08),(x+.04,-.25,.19),(x+.11,-.21,.22)],.014,m['copper'])
def split_vessel(m,q):
 bowl(m,{})
 p.box('Central reaction divider',(0,0,.05),(.04,.84,.14),m['ceramic'],.01)
 for x in [-.22,.22]:lump('Separated reaction medium',(x,0,.04),(.19,.33,.08),m['product'] if x<0 else m['secondary'])
def puck(m,q):
 cy('Keyed carrier puck',(0,0,0),.46,.28,m['steel'])
 ry('Supported retaining collar',(0,-.16,0),.36,.045,m['brass'])
 cy('Recessed active center',(0,-.17,0),.29,.025,m['product'])
 if q.get('contacts'):
  for a in range(4):
   angle=a*math.pi/2;cy('Supported contact stud',(.4*math.cos(angle),-.2,.4*math.sin(angle)),.065,.1,m['brass'])
def wafers(m,q):
 for i in range(3):
  ob=chip('Triangular precursor wafer',(.07*i,.02-i*.06,.07*i),(.93,.57,.065),m['product']);ob.rotation_euler.z=.2*i
 p.box('Conductive wafer retaining clip',(-.37,-.13,-.04),(.14,.30,.30),m['brass'],.02)
def mixer(m,q):
 bowl(m,{})
 p.cylinder('Supported impeller shaft',.045,.65,.27,m['steel'])
 for z in [.15,.30]:
  for a in [0,math.pi/2]:
   ob=p.box('Real mixing paddle',(0,0,z),(.57,.07,.04),m['brass'],.012);ob.rotation_euler.z=a
 for a in [0,math.tau/3,2*math.tau/3]:
  x,y=.43*math.cos(a),.43*math.sin(a);p.box('Protective impeller rib',(x,y,.18),(.055,.055,.55),m['steel'],.012)
 p.ring('Shaft support bridge ring',.43,.025,.46,m['steel'])
def froth(m,q):
 bowl(m,{'ceramic':True})
 for i in range(20):
  a=i*2.4;r=.075*math.sqrt(i);size=.07+(i%3)*.014
  p.sphere('Supported viscoelastic foam bubble',(r*math.cos(a),r*math.sin(a),.07),
   (size,size,size*.8),m['product'],2)
def resin(m,q):
 p.box('Executive-grade support shoe',(0,0,-.28),(.97,.66,.13),m['steel'],.025)
 ob=lump('Faceted resin body',(0,0,0),(.48,.31,.35),m['product'])
 for face in ob.data.polygons:face.use_smooth=False
 for i in range(3):cone('Embedded visible mineral aggregate',(-.13+i*.13,-.28,.04),.07,0,.26,m['secondary'],5)
def ingot(m,q):
 verts=[(-.58,-.30,-.2),(.58,-.30,-.2),(.58,.30,-.2),(-.58,.30,-.2),
  (-.48,-.23,.2),(.48,-.23,.2),(.48,.23,.2),(-.48,.23,.2)]
 mesh_object('Tapered machined alloy ingot',verts,[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],m['product'],.018)
 p.box('Supported identification band',(0,-.307,-.04),(.35,.015,.15),m['brass'],.01)
def roll(m,q):
 steps=150;verts=[]
 for x in [-.50,.50]:
  for side in [0,.014]:
   for i in range(steps):
    a=i/(steps-1)*math.pi*5;r=.09+.015*a+side
    verts.append((x,r*math.cos(a),r*math.sin(a)))
 faces=[]
 for i in range(steps-1):
  faces.extend([(i,i+1,2*steps+i+1,2*steps+i),(steps+i,3*steps+i,3*steps+i+1,steps+i+1),
   (i,steps+i,steps+i+1,i+1),(2*steps+i,2*steps+i+1,3*steps+i+1,3*steps+i)])
 faces.extend([(0,2*steps,3*steps,steps),(steps-1,2*steps-1,4*steps-1,3*steps-1)])
 mesh_object('Actual layered polymer spiral',verts,faces,m['product'])
 p.box('Loose flat leading sheet',(0,-.24,-.30),(1.0,.38,.025),m['product'],.009)
def substrate(m,q):
 for i in range(2):
  p.box('Duplex insulating substrate',(i*.11,.10-i*.18,i*.13),(.98,.08,.70),m['ceramic'],.014)
  p.box('Etched substrate face',(i*.11,.052-i*.18,i*.13),(.9,.018,.62),m['product'],.007)
  for x in [-.30,-.1,.1,.30]:p.box('Copper circuit trace',(x+i*.11,.038-i*.18,i*.13),(.025,.009,.45),m['copper'],.003)
  for x in [-.34,-.17,0,.17,.34]:p.box('Edge contact',(x+i*.11,.03-i*.18,-.34+i*.13),(.07,.035,.14),m['brass'],.004)
def perforated(m,q):
 for i in range(2):
  x=.07*i;y=.09-i*.15;z=.08*i
  ob=p.box('Perforated alloy sheet',(x,y,z),(1.13,.07,.81),m['product'],.012)
  for xx in [-.38,-.13,.13,.38]:
   for zz in [-.24,0,.24]:carve(ob,(x+xx,y,z+zz),(.105,.12,.105))
def canister(m,q):
 state=q.get('state','empty');r=.38
 p.cylinder('Pressure shell',r,.85,0,m['steel'])
 for z in [-.39,.39]:p.sphere('Dished pressure-vessel end',(0,0,z),(r,r,.13),m['steel'],3)
 for z in [-.44,.44]:p.cylinder('Thick rolled end cap',r+.04,.09,z,m['dark'])
 p.ring('Retaining neck collar',.29,.04,.51,m['brass'])
 p.cylinder('Closed service neck',.27,.12,.55,m['steel'])
 p.box('Flush front inspection bezel',(0,-r-.005,0),(.37,.035,.34),m['dark'],.03)
 p.box('Contained state window',(0,-r-.026,0),(.26,.012,.23),m['product'] if state!='empty' else m['glass'],.025)
 for x in [-.14,.14]:
  for z in [-.12,.12]:p.sphere('Flush window-retaining screw',(x,-r-.03,z),(.016,.012,.016),m['brass'],2)
 for x in [-.10,0,.10]:p.box('Recessed state indicator',(x,-r-.03,-.25),(.05,.014,.035),m['product'] if state=='charged' else m['dark'],.005)
 for a in range(6):
  angle=a*math.tau/6;p.cylinder('Service cap retaining bolt',.023,.025,.625,m['brass'],xy=(.21*math.cos(angle),.21*math.sin(angle)))
 if state in ['waste','radioactive']:
  for x in [-.28,.28]:p.box('Supported return lock tab',(x,-.24,.49),(.1,.14,.15),m['brass'],.012)
 if state=='radioactive':p.ring('Thick shielding collar',r+.03,.055,.23,m['dark'])
def waste_drum(m,q):
 r=.42;style=q.get('waste','industrial')
 p.cylinder('Waste containment drum',r,.8,0,m['product'],vertices=32)
 for z in [-.38,.12,.4]:p.ring('Supported rolled drum hoop',r,.03,z,m['steel'])
 p.cylinder('Fitted sealed waste lid',r+.015,.09,.43,m['dark'])
 p.box('Hazard identification backing',(0,-r-.008,-.05),(.42,.02,.36),m['yellow'] if style=='radioactive' else m['ceramic'],.018)
 if style=='radioactive':
  cy('Radiation trefoil central disk',(0,-r-.025,-.05),.026,.006,m['dark'])
  for j in range(3):
   a0=j*math.tau/3+.25;verts=[]
   for radius in [.047,.145]:
    verts.extend((radius*math.cos(a0+i*math.pi/3/8),-r-.029,-.05+radius*math.sin(a0+i*math.pi/3/8)) for i in range(9))
   mesh_object('Radiation trefoil sector',verts,[(i,i+1,10+i,9+i) for i in range(8)],m['dark'])
 elif style=='biohazard':
  for j in range(3):
   a=j*math.tau/3;xx,zz=.072*math.cos(a),-.05+.072*math.sin(a)
   points=[(xx+.078*math.cos(a+.55+i*5.2/24),-r-.029,zz+.078*math.sin(a+.55+i*5.2/24)) for i in range(25)]
   p.tube('Biohazard lobe marking',points,.011,m['dark'])
  ry('Biohazard center ring',(0,-r-.028,-.05),.035,.009,m['dark'])
 else:
  for angle in [-.65,.65]:
   ob=p.box('Industrial waste crossed hazard mark',(0,-r-.025,-.05),(.032,.009,.25),m['dark'],.003);ob.rotation_euler.y=angle
 if style=='radioactive':
  p.cylinder('Heavy shielding cap',r+.06,.14,.52,m['steel'])
  for x in [-.32,.32]:p.box('Cap locking lug',(x,-.23,.56),(.1,.16,.15),m['brass'],.015)
 if style=='biohazard':
  for x in [-.33,.33]:p.box('Briquette compression rail',(x,-.3,0),(.07,.1,.70),m['dark'],.015)
def shell_case(m,q):
 r=.27 if q.get('reinforced') else .23
 cx('Drawn case body',(0,0,0),r,1.05,m['product'])
 cx('Extractor base',(-.57,0,0),r+.045,.09,m['brass'])
 cx('Dark hollow case mouth',(.54,0,0),r*.82,.025,m['dark'])
 ob=p.ring('Open case mouth rim',r,.025,0,m['product']);ob.rotation_euler.y=math.pi/2;ob.location=(.56,0,0)
 if q.get('reinforced'):
  for x in [-.25,.24]:
   ob=p.ring('Structural case collar',r+.015,.028,0,m['steel']);ob.rotation_euler.y=math.pi/2;ob.location=(x,0,0)
def explosive(m,q):
 p.box('Protective explosive carrier',(0,0,-.26),(1.12,.6,.13),m['steel'],.025)
 for x in [-.32,0,.32]:p.box('Solid explosive block',(x,0,0),(.29,.50,.48),m['product'],.04)
 p.box('Broad restraint band',(0,-.27,0),(.16,.05,.56),m['dark'],.015)
def chassis(m,q):
 p.box('Unarmed chassis hull',(0,0,0),(1.14,.68,.34),m['steel'],.07)
 p.box('Empty turret well',(0,0,.19),(.57,.45,.035),m['dark'],.10)
 p.ring('Turret mounting rim',.26,.026,.22,m['brass'])
 for y in [-.46,.46]:
  p.box('Continuous track backbone',(0,y,-.14),(1.38,.21,.38),m['dark'],.11)
  for x in [-.48,-.24,0,.24,.48]:cy('Supported road wheel',(x,y-.12 if y<0 else y+.12,-.14),.13,.04,m['steel'])
  for x in [-.54,-.36,-.18,0,.18,.36,.54]:p.box('Track tread shoe',(x,y,.04),(.13,.25,.05),m['dark'],.008)
def fish(m,q):
 body=lump('Cooked fish body',(0,0,0),(.57,.23,.23),m['product'])
 for x in [-.32,-.15,.02,.19,.36]:p.tube('Seared skin groove',[(x,-.19,-.08),(x+.04,-.235,.08)],.012,m['dark'])
 for z in [-.11,.11]:chip('Fish tail fin',(-.63,0,z),(.28,.13,.065),m['product'])
 p.sphere('Seared fish eye',(.44,-.20,.04),(.025,.012,.025),m['dark'],2)
 p.tube('Wooden serving skewer',[(-.87,.04,-.07),(.78,.04,-.07)],.025,m['wood'])
def meal(m,q):
 p.box('Open metal mess tin',(0,0,-.14),(1.05,.64,.29),m['steel'],.14)
 p.box('Food-filled tin interior',(0,0,.02),(.88,.48,.025),m['dark'],.1)
 for x in [-.25,.05,.28]:lump('Cooked meal portion',(x,-.02,.09),(.16,.18,.09),m['product'] if x<.1 else m['secondary'])
 lid=p.box('Attached open hinged lid',(0,.33,.24),(1.04,.06,.60),m['steel'],.10);lid.rotation_euler.x=-.18
def tools(m,q):
 for i in range(2):
  y=i*.2-.1;z=i*.18-.12
  p.box('Wooden stone-tool handle',(0,y,z),(.94,.10,.09),m['wood'],.03)
  chip('Knapped stone tool head',(.44,y,z+.10),(.36,.31,.20),m['stone'])
  for x in [.3,.34,.38]:
   ob=p.ring('Binding cord wrap',.075,.012,0,m['stitch']);ob.rotation_euler.y=math.pi/2;ob.location=(x,y,z)
def pulp(m,q):
 p.box('Shallow pulping tray',(0,0,-.21),(1.06,.66,.11),m['wood'],.04)
 lump('Wet pulped fiber mass',(0,0,-.06),(.47,.27,.12),m['product'],6)
 rng=random.Random(9)
 for i in range(26):
  x=rng.uniform(-.38,.38);y=rng.uniform(-.20,.20);a=rng.uniform(0,math.tau)
  dx,dy=.09*math.cos(a),.09*math.sin(a)
  p.tube('Loose wet shredded wood fiber',[(x-dx,y-dy,-.02),(x,y,.02),(x+dx,y+dy,-.015)],.017,m['product'])
def staples(m,q):
 for i in range(12):
  x=-.38+i*.055;p.tube('Collated U-shaped staple',[(x,-.17,-.13),(x,-.17,.14),(x,.18,.14),(x,.18,-.13)],.018,m['steel'])
 for x in [-.2,.15,.42]:p.tube('Loose formed staple',[(x,-.33,-.17),(x,-.33,.05),(x+.20,-.33,.05),(x+.20,-.33,-.17)],.018,m['steel'])
def stamp(m,q):
 p.box('Recessed ink pad tray',(.33,0,-.24),(.52,.5,.11),m['steel'],.04)
 p.box('Red ink pad surface',(.33,0,-.173),(.43,.41,.025),m['product'],.035)
 p.box('Engraved stamp foot',(-.25,0,-.12),(.50,.36,.10),m['dark'],.025)
 p.cylinder('Supported stamp handle stem',.08,.30,.08,m['brass'],xy=(-.25,0))
 p.sphere('Wooden hand stamp grip',(-.25,0,.29),(.23,.16,.13),m['wood'],3)
def document(m,q):
 style=q.get('document','folder');hard=style in ['clipboard','risk-work','contained','docket','board-risk']
 if style=='summary':
  for i in range(3):
   ob=p.box('Fanned summary folder',(i*.09-.1,.10-i*.09,i*.05),(.98,.055,.77),m['product'],.012);ob.rotation_euler.y=(i-1)*.18
 else:p.box('Rigid report cover' if hard else 'Folded document backing',(0,.05,0),(1.15,.11 if hard else .035,.89),m['product'],.018)
 pages=4 if style in ['packet','deliverable','contained','docket','board-risk'] else 2
 for i in range(pages):p.box('Bound report sheet',(i*.015,.00-i*.022,0),(.99,.018,.76),m['paper'],.007)
 front=-.03-pages*.022
 p.box('Printed document header',(0,front,.24),(.72,.004,.07),m['dark'],.002)
 for i in range(4):p.box('Printed report rule',(-.06,front,-.03-i*.075),(.59-i*.035,.004,.009),m['ink'],.001)
 if style in ['folder','folio','summary','board-risk','docket']:
  p.box('Supported indexed folder tab',(.30,.04,.49),(.31,.08,.16),m['product'],.012)
 if style in ['clipboard','risk-work','work','folio']:
  p.tube('Spring steel retaining clip',[(-.19,front-.02,.44),(-.19,front-.04,.30),(.19,front-.04,.30),(.19,front-.02,.44)],.024,m['steel'])
 if style=='certified':
  cy('Raised wax certification seal',(.25,front-.025,-.22),.14,.035,m['product'])
  for x in [.2,.3]:p.box('Tied certification ribbon',(x,front-.015,-.34),(.06,.018,.29),m['red'],.005)
 if style in ['risk','risk-work','board-risk']:
  x=-.27 if style=='board-risk' else .23
  mesh_object('Raised warning plate',[(x-.16,front-.015,-.04),(x+.16,front-.015,-.04),(x,front-.015,.23)],[(0,1,2)],m['yellow'])
  p.box('Warning exclamation',(x,front-.024,.09),(.023,.009,.09),m['dark'],.002)
 if style in ['packet','docket','board-risk']:
  for z in [-.24,.24]:
   ob=p.ring('Actual ring binder loop',.07,.018,0,m['steel']);ob.rotation_euler.y=math.pi/2;ob.location=(-.48,front+.035,z)
 if style in ['contained','deliverable']:
  for x in [-.34,.34]:
   p.box('Document containment strap',(x,front-.022,0),(.13,.04,.89),m['leather'],.012)
   p.box('Supported report latch',(x,front-.05,-.15),(.20,.06,.16),m['brass'],.015)
 if style=='deliverable':
  p.box('Brown paper parcel wrapping',(0,front-.06,.03),(.96,.035,.34),m['wood'],.012)
  p.box('Small attached delivery manifest',(.16,front-.082,.04),(.42,.012,.24),m['paper'],.005)
  for z in [-.02,.04,.10]:p.box('Delivery manifest rule',(.16,front-.092,z),(.29,.004,.009),m['ink'],.001)
 if style=='contained':
  p.box('Closed protective report-case lid',(0,front-.07,.0),(.71,.06,.66),m['dark'],.04)
  p.box('Recessed case identification plate',(0,front-.108,.0),(.38,.012,.17),m['steel'],.014)
 if style=='board-risk':
  for z in [-.24,0,.24]:p.box('Three separate advisory index tabs',(.61,.03,z),(.16,.08,.13),m['product'],.012)
  p.box('Secondary advisory warning plate',(.28,front-.023,.0),(.19,.012,.21),m['yellow'],.01)
 if style=='slip':
  for z in [-.28,-.14,0,.14,.28]:cy('Perforated request-sheet edge recess',(-.43,front-.013,z),.025,.007,m['dark'])
def paper_waste(m,q):
 for i in range(7):
  a=i*2.4;r=.12*math.sqrt(i);ob=lump('Crumpled rejected paper',(r*math.cos(a),r*math.sin(a)*.7,-.05+i*.025),(.23,.17,.14),m['paper'],i+2)
  for face in ob.data.polygons:face.use_smooth=False
 for i in range(3):chip('Torn folder fragment',(-.3+i*.25,-.21,-.20),(.40,.25,.018),m['product'])
def mechanism(m,q):
 style=q.get('mechanism','coils');p.box('Bolted mechanical base',(0,0,-.43),(1.15,.58,.13),m['steel'],.025)
 for x in [-.45,.45]:
  p.box('Supported rotor upright',(x,0,-.02),(.10,.16,.76),m['dark'],.02)
 if style=='vanes':
  ry('Rigid vane containment rim',(0,0,.03),.47,.04,m['steel']);cy('Supported rotor hub',(0,-.06,.03),.12,.28,m['brass'])
  for i in range(6):
   a=i*math.tau/6;ob=p.box('Hydrocoptic rotor vane',(.27*math.cos(a),-.04,.03+.27*math.sin(a)),(.34,.05,.10),m['product'],.018);ob.rotation_euler.y=-a
 elif style in ['column','retro']:
  for i,r in enumerate([.3,.23,.17]):p.cylinder('Indexed upright rotor disc',r,.12,-.2+i*.22,m['product'])
  p.cylinder('Supported central shaft',.055,.88,.04,m['brass'])
 elif style=='discs':
  for x in [-.24,.24]:
   cy('Parallel coaxial grametter disc',(x,-.04,.05),.25,.17,m['product']);ry('Disc retaining ring',(x,-.15,.05),.18,.018,m['brass'])
 else:
  count=q.get('coils',1)
  for i in range(count):
   x=(i-(count-1)/2)*.32;z=.04+(i%2)*.15
   cy('Supported encabulator core',(x,-.04,z),.17,.3,m['product'])
   for y in [-.18,-.1,-.02,.06]:ry('Actual conductive winding',(x,y,z),.185,.018,m['copper'])
  if q.get('frame'):p.box('Framulated top bridge',(0,0,.49),(1.12,.23,.10),m['steel'],.015)
def arm(m,q):
 p.box('Arm installation foot',(0,0,-.41),(1.07,.52,.13),m['steel'],.025)
 for i in range(q.get('arms',1)):
  y=-.12+i*.26
  points=[(-.41,y,-.31),(-.35,y,.22),(.23,y,.29),(.47,y,.06)]
  for start,end in zip(points,points[1:]):
   a,b=Vector(start),Vector(end);delta=b-a
   for side in [-.055,.055]:
    ob=p.box('Paired structural arm fork plate',(a+b)/2+Vector((0,side,0)),(.115,.035,delta.length),m['steel'],.018)
    ob.rotation_euler=delta.to_track_quat('Z','Y').to_euler()
  for x,_,z in points:
   cy('Supported articulation bearing',(x,y-.05,z),.105,.16,m['brass'])
   cy('Recessed bearing pin',(x,y-.145,z),.042,.025,m['dark'])
  p.tube('Arm hydraulic cylinder support',[(-.36,y-.09,-.18),(-.14,y-.09,.24)],.045,m['dark'])
  p.tube('Supported bright piston rod',[(-.14,y-.09,.24),(.12,y-.09,.28)],.023,m['steel'])
  if q.get('duct'):p.tube('Rigid protective arm duct',[(-.25,y,.27),(-.14,y,.43),(.28,y,.43),(.52,y,.19)],.08,m['dark'])
def waterwheel(m,q):
 for x in [-.48,.48]:
  p.box('Stone wheel support pier',(x,.15,-.30),(.25,.55,.72),m['stone'],.05)
 cy('Supported wooden wheel axle',(0,0,.1),.09,.8,m['wood'])
 for y in [-.25,.25]:
  ry('Circular wooden wheel rim',(0,y,.1),.58,.055,m['wood'])
  for i in range(8):
   a=i*math.tau/8
   p.tube('Load-bearing wheel spoke',[(0,y,.1),(.57*math.cos(a),y,.1+.57*math.sin(a))],.035,m['wood'])
 for i in range(12):
  a=i*math.tau/12;ob=p.box('Broad wooden paddle',(.62*math.cos(a),0,.1+.62*math.sin(a)),(.23,.6,.065),m['wood'],.012);ob.rotation_euler.y=-a
def droplet(m,q):
 verts=[];faces=[];rings=20;segments=48
 for j in range(rings):
  z=-.5+j/(rings-1)*1.25;t=j/(rings-1);r=max(.005,.48*math.sin(math.pi*t)**.55*(1-.60*t))
  for i in range(segments):a=i*math.tau/segments;verts.append((r*math.cos(a),r*math.sin(a),z))
 for j in range(rings-1):
  for i in range(segments):k=j*segments+i;n=j*segments+(i+1)%segments;faces.append((k,n,n+segments,k+segments))
 faces.extend([tuple(reversed(range(segments))),tuple(range((rings-1)*segments,rings*segments))])
 mesh_object('Dense toxic sludge droplet',verts,faces,m['product'])
def calcifier(m,q):
 p.box('Masonry calcifier plinth',(0,0,-.38),(1.27,.85,.21),m['stone'],.035)
 body=p.box('Refractory heat chamber',(-.17,0,.0),(.88,.65,.65),m['stone'],.055)
 carve(body,(-.17,-.30,-.08),(.45,.17,.30))
 p.box('Recessed chamber interior',(-.17,-.23,-.08),(.42,.025,.27),m['dark'],.014)
 p.box('Supported furnace grate',(-.17,-.37,-.21),(.5,.22,.05),m['steel'],.012)
 p.cylinder('Supported calcination pan',.36,.11,.40,m['steel'],xy=(-.17,0))
 p.ring('Thick pan retaining rim',.36,.026,.46,m['brass'],center=(-.17,0))
 p.cylinder('Calcined material surface',.31,.02,.455,m['product'],xy=(-.17,0))
 p.cylinder('Braced furnace flue',.11,.80,.20,m['dark'],xy=(.47,.17))
 p.cylinder('Supported flue cap',.17,.08,.62,m['steel'],xy=(.47,.17))
 p.box('Flue retaining bracket',(.42,.12,-.12),(.32,.35,.10),m['steel'],.02)
BUILDERS={'bowl':bowl,'granules':granules,'flakes':flakes,'mound':mound,'bone-dust':bone_dust,'porous':porous,
 'crystal':crystal,'vessel':vessel,'slabs':slabs,'glass-sheets':glass_sheets,'cartridge':cartridge,'twin-vials':twin_vials,'filter':filter_,
 'matrix':matrix,'broken-matrix':broken_matrix,'honeycomb':honeycomb,'slab-frame':slab_frame,'preform':preform,
 'conductive':conductive,'split-vessel':split_vessel,'puck':puck,'wafers':wafers,'mixer':mixer,'froth':froth,
 'resin':resin,'ingot':ingot,'roll':roll,'substrate':substrate,'perforated':perforated,'canister':canister,
 'waste-drum':waste_drum,'shell-case':shell_case,'explosive':explosive,'chassis':chassis,'fish':fish,'meal':meal,
 'tools':tools,'pulp':pulp,'staples':staples,'stamp':stamp,'document':document,'paper-waste':paper_waste,
 'mechanism':mechanism,'arm':arm,'waterwheel':waterwheel,'droplet':droplet,'calcifier':calcifier}
