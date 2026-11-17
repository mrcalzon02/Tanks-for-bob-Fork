"""Preserve eight saved OBJ groups as a supported primitive electric component works."""
import bpy,bmesh,json,math,sys,tempfile,hashlib,argparse
from pathlib import Path
from mathutils import Vector
import numpy as np
H=Path(__file__).resolve().parent;R=H.parents[3];parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path,required=True);args=parser.parse_args(sys.argv[sys.argv.index('--')+1:]);O=args.out.resolve()
if O.exists():raise FileExistsError(O)
O.mkdir(parents=True);tempfile.tempdir=str(R/'build/quarry-export-temp');sys.path.insert(0,str(R/'models/island-survival/primitive-steam-powered-pump/v3'));sys.path.insert(0,str(R.parent/'model-production/tools/fmpl'))
from mesh_util import box,cylinder,tube,lathe,mesh
import surfaces
from blender_camera_guard import install_canonical_camera,assert_clean,temporary_inspection_camera
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();starter=H/'starter-tank-ammo-assembling-machine.obj';assert sha(starter)=='f4b4c74c275ad8df520c18a7d11f5f2bee101966e367272c7ba254e7d61a1a39'
contract=json.loads((H/'contract.json').read_text());assert len(contract['processing_recipes'])==46 and contract['entity']['electric']
bpy.ops.wm.read_factory_settings(use_empty=True);s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=32;s.cycles.use_denoising=False;s.render.film_transparent=True;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGBA';s.render.threads_mode='FIXED';s.render.threads=6;s.view_settings.view_transform='AgX'
s.world=bpy.data.worlds.new('Neutral component workshop');s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs[0].default_value=(.32,.32,.32,1)
for p,power in [((4,-4,7),800),((-4,2,5),450)]:
 l=bpy.data.lights.new('Workshop area','AREA');l.energy=power;l.size=5;o=bpy.data.objects.new(l.name,l);s.collection.objects.link(o);o.location=p;o.rotation_euler=(Vector((0,0,1))-o.location).to_track_quat('-Z','Y').to_euler()
root=bpy.data.objects.new('EXPORT | Tanks ammunition component works',None);s.collection.objects.link(root);col=bpy.data.collections.new('AMMO WORKS | supported electric process machinery');s.collection.children.link(col);m=surfaces.create(O)
rng=np.random.default_rng(171846);u,v=np.meshgrid(np.linspace(0,1,512),np.linspace(0,1,512));coarse=surfaces.field(rng,(512,512),.015);fine=surfaces.field(rng,(512,512),.24);fiber=np.sin(u*270+2*np.sin(v*8))
for name,color,rough,metal,detail in [('bedded-limestone',(.31,.30,.265),.94,0,.014*coarse+.004*fine),('fired-retort-clay',(.32,.19,.115),.89,0,.017*coarse+.004*fine),('sooted-resistance-jacket',(.08,.065,.05),.92,0,.012*coarse+.003*fine),('oiled-leather-belt',(.13,.075,.035),.90,0,.012*fiber+.007*coarse),('crude-oil',(.030,.023,.014),.25,.02,.003*coarse),('insulated-winding-cloth',(.25,.19,.115),.95,0,.010*np.sin(u*190)*np.sin(v*210)+.006*coarse)]:
 m[name]=surfaces.material('tank-ammo-'+name,np.stack([c+detail for c in color],axis=-1),rough+.015*fine,.5+.015*coarse+.008*fine,metal,O)
for mat in m.values():mat.name=mat.name.replace('PUMP V3','TANK AMMO');mat['surface_authorship']='Tank ammunition assembler: physical oak grain/end cuts for bins/frame, bedded limestone and fired retort brick/clay, cloth-wrapped electric windings, copper case/oil circuit, forged guides/cranks, leather drive belts. Per-part physical UVs; actual electric 46-recipe component/munition/wood-oil operations.'
# Common fittings use real hollow bores; all link endpoints are authored explicitly.
def E(n,p=(0,0,0),parent=root):
 o=bpy.data.objects.new('AMMO | '+n,None);col.objects.link(o);o.parent=parent;o.location=p;return o
def B(n,p,d,mat=None,parent=root,bevel=.005):
 mat=mat or m['wood'];o=box('AMMO | '+n,p,d,mat,col,parent,bevel);surfaces.apply(o,mat,m['endgrain'] if mat==m['wood'] else None);return o
def C(n,p,r,d,mat=None,axis='Z',parent=root,segments=40):
 mat=mat or m['iron'];o=cylinder('AMMO | '+n,p,r,d,mat,col,parent,axis,segments);surfaces.apply(o,mat);return o
def ring(n,p,outer,inner,depth,mat=None,axis='Z',parent=root):
 mat=mat or m['bronze'];t=Vector({'X':(1,0,0),'Y':(0,1,0),'Z':(0,0,1)}[axis]);o=tube('AMMO | '+n,[(-t*depth/2,t,outer,inner),(t*depth/2,t,outer,inner)],mat,col,parent,48);o.location=p;return o
def beam(n,a,b,w,mat=None,parent=root):
 a,b=Vector(a),Vector(b);o=B(n,(a+b)/2,(w,w,(b-a).length),mat,parent);o.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler();return o
def bore(o,c):
 bpy.context.view_layer.update();bpy.context.view_layer.objects.active=o;mod=o.modifiers.new('Real fitted bore or open chamber','BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=c;bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(c,do_unlink=True)
def pipe(n,points,r=.045,mat=None):
 pts=[Vector(p) for p in points];smooth=[pts[0]]
 for i in range(1,len(pts)-1):
  incoming=(pts[i]-pts[i-1]).normalized();outgoing=(pts[i+1]-pts[i]).normalized();cut=min(.08,(pts[i]-pts[i-1]).length*.3,(pts[i+1]-pts[i]).length*.3);a=pts[i]-incoming*cut;b=pts[i]+outgoing*cut
  for k in range(9):t=k/8;smooth.append((1-t)**2*a+2*(1-t)*t*pts[i]+t*t*b)
 smooth.append(pts[-1]);samples=[(p,(smooth[min(i+1,len(smooth)-1)]-smooth[max(0,i-1)]).normalized(),r,r*.68) for i,p in enumerate(smooth)];return tube('AMMO | '+n,samples,mat or m['copper'],col,root,24)
def linear(o):
 if o.animation_data and o.animation_data.action:
  for l in o.animation_data.action.layers:
   for strip in l.strips:
    for bag in strip.channelbags:
     for curve in bag.fcurves:
      for key in curve.keyframe_points:key.interpolation='LINEAR'
# Import the actual eight starter groups rather than replacing the source.
verts=[];groups={};name=None
for line in starter.read_text().splitlines():
 t=line.split()
 if not t:continue
 if t[0]=='v':verts.append(Vector(map(float,t[1:])))
 elif t[0]=='g':name=t[1];groups[name]=[]
 elif t[0]=='f':groups[name].append(tuple(int(i)-1 for i in t[1:]))
reused={}
for name,faces in groups.items():
 ids=sorted({i for f in faces for i in f});lookup={i:j for j,i in enumerate(ids)};pts=[verts[i].copy() for i in ids];fs=[tuple(lookup[i] for i in f) for f in faces];lo=[min(p[a] for p in pts) for a in range(3)];hi=[max(p[a] for p in pts) for a in range(3)];kind=name.removeprefix('tank-ammo-assembling-machine_');mat=m['wood'];solid=None
 def remap(p,center,size):return tuple(center[a]+((p[a]-(lo[a]+hi[a])/2)/(hi[a]-lo[a]))*size[a] for a in range(3))
 if kind=='factory_base':pts=[(p.x,p.y,p.z*.28) for p in pts];mat=m['bedded-limestone']
 elif kind=='munitions_feeder':
  fs=fs[:2]+fs[4:];new=[]
  for p in pts:
   z=(p.z-lo[2])/(hi[2]-lo[2]);new.append((-.70+(p.x-(lo[0]+hi[0])/2)/(hi[0]-lo[0])*(.40+.30*z),-.93+(p.y-(lo[1]+hi[1])/2)/(hi[1]-lo[1])*(.25+.20*z),.43+.38*z))
  pts=new;solid=.025
 elif kind=='case_former':pts=[(.70+(p.x-.58)*.60,.30+p.y*.95/1.5,1.02+(p.z-1)*.60) for p in pts];mat=m['fired-retort-clay']
 elif kind=='loading_hopper':
  fs=fs[4:];new=[]
  for p in pts:
   z=(p.z-lo[2])/(hi[2]-lo[2]);new.append((.70+(p.x-(lo[0]+hi[0])/2)/(hi[0]-lo[0])*(.14+.44*z),.30+(p.y-(lo[1]+hi[1])/2)/(hi[1]-lo[1])*(.14+.40*z),1.41+.35*z))
  pts=new;solid=.020
 elif kind in ('north_oil_inlet','south_oil_outlet'):
  # Retain the saved cylindrical body as the outer native-size throat; replace
  # solid caps by real annular ends before fitting reducers and clamping saddles.
  sign=1 if kind.startswith('north') else -1;new=[]
  for p in pts:
   radial=Vector((p.x,p.z-.42));radius=radial.length
   new.append((p.x*.285/.18,sign*(1.20+(abs(p.y)-1.04)/.62*.30),.36+(p.z-.42)*.285/.18))
  pts=new;mat=m['iron']
 elif kind=='output_cases':pts=[remap(p,(.72,-.99,.35),(.80,.60,.20)) for p in pts];fs=fs[:2]+fs[4:];solid=.025
 elif kind=='safety_cage':pts=[remap(p,(-.70,-.62,1.08),(.90,.035,.035)) for p in pts];mat=m['iron']
 o=mesh('AMMO | REUSED '+name,pts,fs,mat,col,root);surfaces.apply(o,mat,m['endgrain'] if mat==m['wood'] else None);o['retained_starter_group']=name;reused[kind]=o
 if solid:mod=o.modifiers.new('Actual plank/liner thickness','SOLIDIFY');mod.thickness=solid;mod.offset=0
# Real clearance slots keep the full-size sockets independent of the floor.
base=reused['factory_base']
for sign in (-1,1):bore(base,B('temporary base pipe clearance',(0,sign*1.27,.10),(.72,.66,.44),m['iron']))
for i in range(9):
 x=-1.20+i*.30;B('separate timber deck board',(x,0,.145),(.285,1.90 if abs(x)<.40 else 2.60,.065))
for x in (-1.22,1.22):
 for y in (-1.16,1.16):B('seated floor corner pin',(x,y,.19),(.045,.045,.045),m['bronze'])
# Main fixed pipe bodies are bored; annular collars and large-to-small reducers
# fit the actual 3x3 machine faces at +/-1.5, height .36.
for sign,kind in ((1,'north_oil_inlet'),(-1,'south_oil_outlet')):
 o=reused[kind];bore(o,C('temporary full-bore outlet',(0,sign*1.35,.36),.245,.90,m['iron'],'Y'));o['role']='stationary_socket'
 ring('full-size fixed pipe collar',(0,sign*1.4625,.36),.34,.245,.075,m['iron'],'Y')
 for i in range(6):
  a=i*math.tau/6;C('collar retained bolt',(.308*math.cos(a),sign*1.472,.36+.308*math.sin(a)),.018,.075,m['bronze'],'Y',segments=6)
 samples=[(Vector((0,sign*y,.36)),Vector((0,-sign,0)),outer,inner) for y,outer,inner in [(1.20,.285,.245),(1.12,.24,.195),(.98,.12,.08),(.88,.070,.045)]];o=tube('AMMO | fixed reducing pipe tail',samples,m['iron'],col,root,48);o['role']='stationary_socket'
 saddle=B('grounded pipe saddle',(0,sign*1.28,.095),(.62,.18,.19),m['bedded-limestone']);bore(saddle,C('temporary saddle seat',(0,sign*1.28,.36),.286,.40,m['iron'],'Y'))
 for x in (-.28,.28):C('saddle anchor bolt',(x,sign*1.28,.19),.014,.055,m['bronze'])
bore(reused['munitions_feeder'],B('temporary actual feeder slot',(-.70,-.78,.46),(.24,.24,.10),m['iron']))
# Press frame and fitted, bored linear guides.
for x in (-1.15,-.25):
 for y in (-.20,.82):
  B('press timber load post',(x,y,.875),(.12,.14,1.42));B('post seated iron foot',(x,y,.24),(.18,.20,.08),m['iron'])
 for y in (-.20,.82):beam('post knee brace',(x,y,.35),(x+.08,y+.12,.70),.045)
B('press bearing crosshead',(-.70,-.20,1.53),(1.04,.20,.10));B('rear shaft bearing crosshead',(-.70,.82,1.75),(1.04,.20,.10))
B('fixed die bolster',(-.70,-.20,.47),(.76,.55,.12),m['iron']);ring('bored fixed case die',(-.70,-.20,.60),.16,.101,.14,m['bronze'])
# Copper stock has an actual cavity for the drawing mandrel.
stock=lathe('AMMO | hollow copper case in die',[(0,.530),(.087,.530),(.092,.56),(.092,.88),(.075,.88),(.075,.563),(0,.563)],(-.70,-.20),m['copper'],col,root,48);surfaces.physical_box_uv(stock)
for x in (-.99,-.41):
 C('fixed polished press guide',(x,-.20,1.13),.024,.94,m['iron'])
 for z in (.67,1.53):
  ring('fixed guide support collar',(x,-.20,z),.052,.025,.06,m['bronze'])
ram=E('guided moving press ram');ram_bar=B('moving ram crossbar',(0,0,0),(.69,.30,.12),m['iron'],ram)
for x in (-.29,.29):bore(ram_bar,C('temporary real ram guide bore',(x,0,0),.0265,.30,m['iron'],parent=ram))
for x in (-.29,.29):ring('bored moving ram guide eye',(x,0,0),.052,.0265,.16,m['bronze'],parent=ram)
C('drawing mandrel',(0,0,-.225),.060,.33,m['bronze'],parent=ram);C('ram lower pin',(0,-.18,.06),.013,.16,m['iron'],'Y',ram);lower_seat=E('press lower pin seat',(0,-.20,.06),ram)
crank=E('press crank and shaft',(-.70,-.20,1.82));C('press through shaft',(0,.52,0),.026,1.18,m['iron'],'Y',crank);ring('press crank rim',(0,0,0),.20,.154,.05,m['iron'],'Y',crank)
for i in range(6):
 a=i*math.tau/6;beam('crank seated spoke',(0,0,0),(.17*math.cos(a),0,.17*math.sin(a)),.035,m['iron'],crank)
C('eccentric upper pin',(0,-.115,.12),.013,.25,m['bronze'],'Y',crank);upper_seat=E('press upper pin seat',(0,-.20,.12),crank)
rod=E('rigid press connecting rod');B('rigid link web',(0,0,0),(.026,.026,.46),m['iron'],rod)
for z in (-.26,.26):ring('real connecting rod eye',(0,0,z),.034,.015,.034,m['bronze'],'Y',rod)
# Fixed bearings support the full press shaft without crossing the eccentric arm.
B('front upper bearing grounded post',(-.70,.30,.96),(.14,.14,1.48))
bore(bpy.data.objects['AMMO | rear shaft bearing crosshead'],C('temporary rear timber shaft clearance',(-.70,.82,1.82),.029,.40,m['iron'],'Y'))
for y in (.30,.82):
 ring('fixed upper shaft bush',(-.70,y,1.82),.053,.028,.10,m['bronze'],'Y');B('bearing seated cleat',(-.70,y,1.735),(.18,.18,.07),m['iron'])
# Open wound electric motor: no burner/fuel substitution.
motor=E('wound motor rotor',(-.70,.94,.65));C('electric armature iron core',(0,0,0),.145,.34,m['iron'],'Y',motor)
C('motor through shaft',(0,-.12,0),.025,.90,m['iron'],'Y',motor)
for i in range(10):
 a=i*math.tau/10;B('armature copper bar',(.15*math.cos(a),0,.15*math.sin(a)),(.026,.31,.024),m['copper'],motor)
for y in (.73,1.15):
 ring('stationary open motor housing',(-.70,y,.65),.225,.172,.055,m['iron'],'Y');ring('motor bored shaft bearing',(-.70,y,.65),.047,.027,.08,m['bronze'],'Y');seat=B('motor grounded wooden saddle',(-.70,y,.3375),(.47,.15,.32));bore(seat,C('temporary actual motor saddle seat',(-.70,y,.65),.226,.30,m['iron'],'Y'))
for sign in (-1,1):
 B('cloth insulated stator pole',(-.70+sign*.26,.94,.65),(.10,.30,.16),m['insulated-winding-cloth'])
 for j in range(10):
  y=.80+j*.028;ring('visible copper field winding',(-.70+sign*.26,y,.65),.085,.065,.009,m['copper'],'Y')
for sign in (-1,1):B('stator pole grounded timber foot',(-.70+sign*.26,.94,.37375),(.10,.18,.3925))
# Retained cylindrical group becomes the lined closed forming/mixing/retort body.
vessel=reused['case_former'];bore(vessel,C('temporary hollow process chamber',(.70,.30,1.02),.27,.86,m['iron'],'Y'));bore(vessel,C('temporary shaft bore',(.70,.30,1.02),.031,1.25,m['iron'],'Y'));bore(vessel,C('temporary charge neck bore',(.70,.30,1.30),.067,.22,m['iron']))
for y in (-.12,.72):
 seat=B('retort brick bearing saddle',(.70,y,.5375),(.72,.22,.72),m['brick']);bore(seat,C('temporary retort curved seat',(.70,y,1.02),.318,.40,m['iron'],'Y'));ring('retort hoop and support clamp',(.70,y,1.02),.317,.301,.045,m['iron'],'Y')
for y in (-.205,.805):ring('fixed agitator sealed bearing',(.70,y,1.02),.060,.027,.07,m['bronze'],'Y')
for y in (-.19,.79):
 for z in (1.02,1.22):bore(vessel,C('temporary process cap port',(.70,y,z),.046,.15,m['iron'],'Y')) if z==1.22 else None
ring('actual charge neck',(.70,.30,1.365),.083,.062,.11,m['bronze'])
for yy in (.12,.48):
 beam('hopper grounded upright',(.34,yy,.1775),(.34,yy,1.30),.045)
 beam('hopper diagonal cradle',(.34,yy,1.30),(.48,yy,1.64),.045)
# Closed end caps/straps expose the pressure-vessel construction and electric heat.
for y in (-.15,.75):ring('retort bolted end ring',(.70,y,1.02),.326,.285,.040,m['iron'],'Y')
for i in range(8):
 a=i*math.tau/8
 for y in (-.17,.77):C('retort ring fastener',(.70+.312*math.cos(a),y,1.02+.312*math.sin(a)),.014,.040,m['bronze'],'Y',segments=6)
for y in (.02,.22,.42,.62):ring('electric retort heating band',(.70,y,1.02),.307,.301,.028,m['copper'],'Y')
agitator=E('driven sealed agitator shaft',(.70,.30,1.02));C('sealed process through shaft',(0,.065,0),.025,1.43,m['iron'],'Y',agitator)
for y in (-.22,.05,.28):
 for i in range(3):
  a=i*math.tau/3;beam('contained mixing paddle',(0,y,0),(.20*math.cos(a),y,.20*math.sin(a)),.035,m['iron'],agitator)
for i in range(4):
 a=i*math.tau/4;beam('front agitator indicator spoke',(0,-.61,0),(.105*math.cos(a),-.61,.105*math.sin(a)),.025,m['bronze'],agitator)
# Upper transfer arbor and its timber load path stay clear of the charge hopper.
arbor=E('upper mixing transfer shaft',(.70,.66,1.82));C('upper transfer through shaft',(0,.22,0),.025,.75,m['iron'],'Y',arbor)
for x in (.35,1.08):B('rear transmission timber upright',(x,1.12,.94875),(.11,.12,1.5425))
B('rear transfer bearing beam',(.70,1.12,1.735),(.90,.08,.09));ring('fixed transfer bored bush',(.70,1.12,1.82),.052,.028,.08,m['bronze'],'Y')
# Leather belts use exact common external tangents; their geometry is the fixed
# running path. Pulleys/shafts rotate at matching radius ratios.
def pulley(n,parent,y,r):

 for edge in (-1,1):ring(n+' flange',(0,y+edge*.032,0),r+.014,r-.025,.010,m['iron'],'Y',parent)
 ring(n+' leather contact',(0,y,0),r-.005,r-.022,.050,m['bronze'],'Y',parent)
 for i in range(4):
  a=i*math.tau/4;beam(n+' spoke',(0,y,0),((r-.02)*math.cos(a),y,(r-.02)*math.sin(a)),.022,m['iron'],parent)
def belt(n,c1,r1,c2,r2,y):
 a,b=np.array(c1),np.array(c2);d=b-a;dist=np.linalg.norm(d);direction=d/dist;perp=np.array([direction[1],-direction[0]]);k=(r1-r2)/dist;nr=k*direction+math.sqrt(1-k*k)*perp;nl=k*direction-math.sqrt(1-k*k)*perp;ar=math.atan2(nr[1],nr[0]);al=math.atan2(nl[1],nl[0]);
 while al<ar:al+=math.tau
 pts=[b+r2*np.array([math.cos(t),math.sin(t)]) for t in np.linspace(ar,al,40)];pts += [a+r1*nl];end=ar+math.tau
 while end<al:end+=math.tau
 pts += [a+r1*np.array([math.cos(t),math.sin(t)]) for t in np.linspace(al,end,40)];verts=[]
 for i,p in enumerate(pts):
  tangent=pts[(i+1)%len(pts)]-pts[(i-1)%len(pts)];normal=np.array([-tangent[1],tangent[0]])/np.linalg.norm(tangent)
  for side,thick in ((-1,-1),(1,-1),(1,1),(-1,1)):q=p+normal*.005*thick;verts.append((float(q[0]),y+side*.024,float(q[1])))
 faces=[]
 for i in range(len(pts)):
  j=(i+1)%len(pts)
  for k in range(4):faces.append((4*i+k,4*j+k,4*j+(k+1)%4,4*i+(k+1)%4))
 o=mesh('AMMO | '+n,verts,faces,m['oiled-leather-belt'],col,root);surfaces.physical_box_uv(o)
pulley('motor drive pulley',motor,-.36,.10);pulley('press reduction pulley',crank,.78,.20);belt('motor to press leather belt',(-.70,.65),.10,(-.70,1.82),.20,.58)
pulley('press transfer pulley',crank,.86,.18);pulley('mixing upper transfer pulley',arbor,0,.18);belt('upper cross-shaft leather belt',(-.70,1.82),.18,(.70,1.82),.18,.66)
pulley('mixing upper drop pulley',arbor,.37,.12);pulley('agitator driven pulley',agitator,.73,.12);belt('rear agitator leather belt',(.70,1.02),.12,(.70,1.82),.12,1.03)
# Fixed large native ports reduce into the actual closed wood/oil circuit.
pipe('north crude oil input line',[(0,.88,.36),(.20,.88,.36),(.20,.88,1.42),(.20,1.25,1.42),(.70,1.25,1.42),(.70,1.25,1.22),(.70,.79,1.22)])
pipe('hot condensate line',[(.70,-.19,1.22),(.70,-.34,1.22),(1.17,-.34,1.26),(1.27,-.25,1.26)],.022)
coil=[]
for i in range(161):
 a=i*math.tau*4/160;coil.append((1.17+.10*math.cos(a),-.25+.10*math.sin(a),1.26-.56*i/160))
pipe('four turn oil cooling coil',coil,.018);pipe('coil tail into closed collector',[(1.27,-.25,.70),(1.17,-.25,.70),(1.17,-.25,.61)],.018)
cup=lathe('AMMO | clay oil collector',[(0,.46),(.10,.46),(.125,.49),(.125,.70),(.105,.72),(.10,.50),(0,.50)],(1.17,-.25),m['fired-retort-clay'],col,root,48);surfaces.physical_box_uv(cup);bore(cup,C('temporary collector outlet',(1.17,-.36,.55),.046,.17,m['iron'],'Y'))
C('collected crude oil surface',(1.17,-.25,.58),.098,.008,m['crude-oil']);B('collector seated stone stand',(1.17,-.25,.315),(.31,.31,.29),m['bedded-limestone'])
pipe('south recovered crude oil outlet',[(1.17,-.36,.55),(1.17,-.52,.55),(.25,-.52,.55),(.25,-.78,.55),(.25,-.78,.36),(0,-.88,.36)])
for x in (1.025,1.315):
 B('cooler grounded upright',(x,-.25,.75),(.035,.05,1.16),m['iron']);B('cooler foot',(x,-.25,.19),(.09,.12,.045),m['iron'])
# Planked feed/packing stands, shields and accessible containment. No invented
# recipe output is added: displayed shells are representative empty cases.
for x in (-1.02,-.38):
 for y in (-1.08,-.78):beam('feed hopper splayed leg',(x,y,.1775),(-.70+(x+.70)*.20/.32,-.93+(y+.93)*.125/.15,.418),.055)
for j in range(5):B('guided feed tray board',(-.98+j*.14,-.55,.42),(.135,.65,.035))
for x in (-1.15,-.25):B('grounded front guard upright',(x,-.62,.64),(.035,.035,.90),m['iron'])
for x in (.38,1.06):
 for y in (-1.24,-.74):B('packing tray seated leg',(x,y,.2075),(.07,.07,.060))
for i in range(3):
 for j in range(4):
  x=.45+j*.18;y=-1.16+i*.18;case=lathe('AMMO | retained finished hollow case',[(0,.2625),(.039,.2625),(.043,.28),(.043,.49),(.032,.49),(.032,.2825),(0,.2825)],(x,y),m['copper'],col,root,24);surfaces.physical_box_uv(case)
B('timber electrical isolator board',(-1.20,1.11,.48),(.18,.31,.44))
for yy in (1.02,1.20):
 ring('clay insulated power terminal',(-1.20,yy,.75),.033,.012,.065,m['fired-retort-clay']);C('power terminal pin',(-1.20,yy,.77),.009,.09,m['copper'])
pipe('cloth insulated motor supply',[(-1.20,1.02,.78),(-1.02,1.02,.78),(-.95,.94,.65)],.014,m['insulated-winding-cloth'])
# Single authored kinematic cycle, with explicit idle key and rigid endpoint solve.
for f in range(0,194):
 theta=0 if f==0 else math.tau*(f-1)/192;crank.rotation_euler.y=theta;motor.rotation_euler.y=2*theta;arbor.rotation_euler.y=theta;agitator.rotation_euler.y=theta
 pin=Vector((-.70+.12*math.sin(theta),-.40,1.82+.12*math.cos(theta)));bottom=Vector((-.70,-.40,pin.z-math.sqrt(.52**2-(pin.x+.70)**2)));ram.location=(-.70,-.20,bottom.z-.06);rod.location=(pin+bottom)/2;rod.rotation_euler.y=math.atan2(pin.x-bottom.x,pin.z-bottom.z)
 for o in (crank,motor,arbor,agitator,ram,rod):o.keyframe_insert(data_path='rotation_euler',frame=f);o.keyframe_insert(data_path='location',frame=f)
for o in (crank,motor,arbor,agitator,ram,rod):linear(o)
# Bake real modifiers and remove zero-area remnants before saving/exporting.
for o in root.children_recursive:
 if o.type!='MESH':continue
 if o.modifiers:o.data=bpy.data.meshes.new_from_object(o.evaluated_get(bpy.context.evaluated_depsgraph_get()));o.modifiers.clear()
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.triangulate(bm,faces=list(bm.faces));bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-7);bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=1e-7);bmesh.ops.delete(bm,geom=[v for v in bm.verts if not v.link_faces],context='VERTS');bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free();o.data.calc_loop_triangles();bad={t.polygon_index for t in o.data.loop_triangles if t.area<1e-12}
 if bad:
  bm=bmesh.new();bm.from_mesh(o.data);bm.faces.ensure_lookup_table();bmesh.ops.delete(bm,geom=[bm.faces[i] for i in bad],context='FACES');bm.to_mesh(o.data);bm.free()
 if not o.data.uv_layers:surfaces.physical_box_uv(o)
s.frame_start=1;s.frame_end=193;s.render.fps=48;s.frame_set(1);profile=dict(camera_policy='fmpl.factorio45.v1',capture_kind='entity',orientation_policy='rotatable',directions=[0,90,180,270],states={'idle':[0],'working':list(range(1,193,6))},source_size=256,camera_override=dict(type='ORTHO',elevation_deg=45,azimuth_deg=0,distance=8,ortho_scale=5.8,target=[0,0,1.0]));install_canonical_camera(s,profile,bpy);s.render.resolution_x=s.render.resolution_y=256;assert_clean(s,profile,bpy);root['prototype']='assembling-machine/tank-ammo-assembling-machine';root['units_per_tile']=1.;root['native_power']='Electric 175 kW, no burner';root['purpose']='46 actual tank-ammo-component recipes; press/form/pack, sealed mixing, wood/coal/oil circuit; fixed native input/output sockets'
bpy.ops.file.pack_all();source=O/'tank-ammo-assembler-v1.blend';bpy.ops.wm.save_as_mainfile(filepath=str(source),compress=True);bpy.ops.wm.open_mainfile(filepath=str(source));s=bpy.context.scene;root=bpy.data.objects['EXPORT | Tanks ammunition component works'];bpy.ops.object.select_all(action='DESELECT')
for o in [root,*root.children_recursive]:o.select_set(True)
bpy.ops.export_scene.gltf(filepath=str(O/'tank-ammo-assembler-v1.glb'),export_format='GLB',use_selection=True,export_cameras=False,export_lights=False,export_animations=True,export_animation_mode='SCENE',export_anim_scene_split_object=False,export_frame_range=True,export_force_sampling=True,export_frame_step=1,export_apply=True,export_extras=True)
(O/'capture-profile.json').write_text(json.dumps(profile,indent=2)+'\n');(O/'construction-receipt.json').write_text(json.dumps(dict(starter_sha256=sha(starter),preserved_starter_groups=list(groups),source_sha256=sha(source),runtime_sha256=sha(O/'tank-ammo-assembler-v1.glb'),native_power='electric 175kW',actual_recipe_contracts=46,owner_visual_approved=False,native_integrated=False),indent=2)+'\n')
projection=bpy.data.objects.new('SPRITE ONLY | square ground correction',None);s.collection.objects.link(projection);projection.scale.y=math.sqrt(2);root.parent=projection;s.render.resolution_x=s.render.resolution_y=512
for name,yaw in [('front',0),('rear',180),('side',90)]:
 root.rotation_euler.z=math.radians(yaw);s.render.filepath=str(O/(name+'-review512.png'));bpy.ops.render.render(write_still=True)
root.rotation_euler.z=0
with temporary_inspection_camera(s,bpy,'Press rigid link and primitive electric processing') as camera:
 target=Vector((0,0,1.1));camera.data.type='ORTHO';camera.data.ortho_scale=3.8;camera.location=target+Vector((-3,-4,2.4));camera.rotation_euler=(target-camera.location).to_track_quat('-Z','Y').to_euler();s.camera=camera;s.render.filepath=str(O/'mechanism-close512.png');bpy.ops.render.render(write_still=True)
print('AMMUNITION_ASSEMBLER_SAVED_REOPENED_EXPORTED',sha(source),flush=True)
