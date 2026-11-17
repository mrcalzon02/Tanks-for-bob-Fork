"""Refine the exact saved ten-group condenser starter for the actual wood/steam recipe."""
import bpy,bmesh,json,math,sys,tempfile,hashlib,argparse
from pathlib import Path
from mathutils import Vector
import numpy as np
H=Path(__file__).resolve().parent;R=H.parents[3]
p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);args=p.parse_args(sys.argv[sys.argv.index('--')+1:]);O=args.out.resolve()
if O.exists():raise FileExistsError(O)
O.mkdir(parents=True);tempfile.tempdir=str(R/'build/quarry-export-temp')
sys.path.insert(0,str(R/'models/island-survival/primitive-steam-powered-pump/v3'));sys.path.insert(0,str(R.parent/'model-production/tools/fmpl'))
from mesh_util import box,cylinder,tube,lathe,mesh
import surfaces
from blender_camera_guard import install_canonical_camera,assert_clean,temporary_inspection_camera
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
starter=H/'starter-steam-condenser.obj';assert sha(starter)=='c5459a1d00ee9aae2acb325e4b3dfcc25d9794a6d61ecacc1873471577986177'
contract=json.loads((H/'contract.json').read_text());assert len(contract['processing_recipes'])==1 and contract['entity']['burner']
bpy.ops.wm.read_factory_settings(use_empty=True);s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=32;s.cycles.use_denoising=True;s.render.film_transparent=True;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGBA';s.render.threads_mode='FIXED';s.render.threads=6;s.view_settings.view_transform='AgX'
s.world=bpy.data.worlds.new('Neutral low-tech steam treatment');s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs[0].default_value=(.32,.32,.32,1)
for pos,power in [((4,-4,7),800),((-4,2,5),450)]:
 l=bpy.data.lights.new('Treatment works area','AREA');l.energy=power;l.size=5;o=bpy.data.objects.new(l.name,l);s.collection.objects.link(o);o.location=pos;o.rotation_euler=(Vector((0,0,1))-o.location).to_track_quat('-Z','Y').to_euler()
root=bpy.data.objects.new('EXPORT | Tanks wood steam treatment condenser',None);s.collection.objects.link(root);col=bpy.data.collections.new('CONDENSER | wood steam treatment construction');s.collection.children.link(col);m=surfaces.create(O)
rng=np.random.default_rng(171913);u,v=np.meshgrid(np.linspace(0,1,512),np.linspace(0,1,512));coarse=surfaces.field(rng,(512,512),.016);fine=surfaces.field(rng,(512,512),.24)
for name,color,rough,metal,detail in [('bedded-limestone',(.32,.305,.27),.94,0,.014*coarse+.004*fine),('clay-pressure-lining',(.33,.20,.12),.88,0,.013*coarse+.004*fine),('crude-inspection-glass',(.32,.36,.30),.23,0,.003*coarse+.001*fine),('charcoal-bed',(.035,.028,.023),.96,0,.012*coarse+.003*fine),('small-burner-flame',(.48,.18,.035),.42,0,.008*fine),('oiled-leather-belt',(.12,.067,.029),.90,0,.013*np.sin(u*280+v*11)+.005*coarse),('mineral-stone-output',(.34,.34,.30),.94,0,.024*coarse+.006*fine)]:
 m[name]=surfaces.material('condenser-v2-'+name,np.stack([c+detail for c in color],axis=-1),rough+.015*fine,.5+.018*coarse+.008*fine,metal,O)
glass=m['crude-inspection-glass'].node_tree.nodes['Principled BSDF'];glass.inputs['Transmission Weight'].default_value=.70;glass.inputs['Alpha'].default_value=.10
for node in m['crude-inspection-glass'].node_tree.nodes:
 if node.type=='NORMAL_MAP':node.inputs['Strength'].default_value=.025;m['crude-inspection-glass'].surface_render_method='DITHERED'
fire=m['small-burner-flame'].node_tree.nodes['Principled BSDF'];fire.inputs['Emission Color'].default_value=(1,.24,.035,1);fire.inputs['Emission Strength'].default_value=3
for mat in m.values():mat.name=mat.name.replace('PUMP V3','TANKS CONDENSER');mat['surface_authorship']='Actual Tanks wood/steam-to-stone process: fitted brick/clay hot chamber, physical oak fibres/end cuts for charge/rack/frame, forged guides and copper steam jacket, rough crude-glass inspection pane, mineral product and charcoal. Useful common base maps explicitly reused; domain-specific images/placement authored for this machine.'
def E(n,pos=(0,0,0),parent=root):
 o=bpy.data.objects.new('CONDENSER | '+n,None);col.objects.link(o);o.parent=parent;o.location=pos;return o
def B(n,pos,dims,mat=None,parent=root,bevel=.005):
 mat=mat or m['wood'];o=box('CONDENSER | '+n,pos,dims,mat,col,parent,bevel);surfaces.apply(o,mat,m['endgrain'] if mat==m['wood'] else None);return o
def C(n,pos,r,depth,mat=None,axis='Z',parent=root,segments=32):
 mat=mat or m['iron'];o=cylinder('CONDENSER | '+n,pos,r,depth,mat,col,parent,axis,segments);surfaces.apply(o,mat);return o
def ring(n,pos,outer,inner,depth,mat=None,axis='Z',parent=root):
 mat=mat or m['bronze'];t=Vector({'X':(1,0,0),'Y':(0,1,0),'Z':(0,0,1)}[axis]);o=tube('CONDENSER | '+n,[(-t*depth/2,t,outer,inner),(t*depth/2,t,outer,inner)],mat,col,parent,40);o.location=pos;return o
def beam(n,a,b,width,mat=None,parent=root):
 a,b=Vector(a),Vector(b);o=B(n,(a+b)/2,(width,width,(b-a).length),mat,parent);o.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler();return o
def bore(o,c):
 bpy.context.view_layer.update();bpy.context.view_layer.objects.active=o
 for pre in list(o.modifiers):bpy.ops.object.modifier_apply(modifier=pre.name)
 mod=o.modifiers.new('Actual fitted through bore','BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=c;bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(c,do_unlink=True)
def wire(n,points,r,mat=None,parent=root):
 pts=[Vector(p) for p in points];o=tube('CONDENSER | '+n,[(pt,(pts[min(i+1,len(pts)-1)]-pts[max(0,i-1)]).normalized(),r,r*.35) for i,pt in enumerate(pts)],mat or m['insulated-winding-cloth'],col,parent,16);surfaces.physical_box_uv(o);return o
def linear(o):
 for layer in o.animation_data.action.layers:
  for strip in layer.strips:
   for bag in strip.channelbags:
    for curve in bag.fcurves:
     for key in curve.keyframe_points:key.interpolation='LINEAR'
# Exact starter groups remain distinct, with their useful geometry reworked.
verts=[];groups={};name=None
for line in starter.read_text(encoding='utf-8').splitlines():
 t=line.split()
 if not t:continue
 if t[0]=='v':verts.append(Vector(map(float,t[1:])))
 elif t[0]=='g':name=t[1];groups[name]=[]
 elif t[0]=='f':groups[name].append(tuple(int(i)-1 for i in t[1:]))
assert len(groups)==10
reused={}
for name,faces in groups.items():
 ids=sorted({i for f in faces for i in f});lookup={i:j for j,i in enumerate(ids)};pts=[verts[i].copy() for i in ids];fs=[tuple(lookup[i] for i in f) for f in faces];kind=name.removeprefix('steam-condenser_');mat=m['copper'];solid=None
 lo=[min(p[a] for p in pts) for a in range(3)];hi=[max(p[a] for p in pts) for a in range(3)]
 if kind=='base':pts=[(p.x,p.y,p.z*.40) for p in pts];mat=m['bedded-limestone']
 elif kind=='cooling_tower':pts=[(p.x*.57/.67,p.y*.57/.67,.72+(p.z-.22)*1.23/1.60) for p in pts];mat=m['clay-pressure-lining']
 elif kind=='funnel':
  fs=[f for f in fs if not all(abs(pts[i].z-pts[f[0]].z)<1e-6 for i in f)];pts=[(p.x*.62/.82,p.y*.62/.82,1.92+(p.z-1.73)*.27/.42) for p in pts];solid=.025
 elif kind=='upper_steam_pipe':pts=[(p.y*.285/.15,.90+(p.x-.27)*.60/.90,.36+(p.z-1.70)*.285/.15) for p in pts];mat=m['iron']
 elif kind=='condensate_outlet':
  fs=[f for f in fs if not all(abs(pts[i].x-pts[f[0]].x)<1e-6 for i in f) and sum(pts[i].z for i in f)/len(f)<=.43001]
  pts=[(-.34+p.y/.15*.13,-.57-(p.x-lo[0])/(hi[0]-lo[0])*.42,.94-(p.x-lo[0])/(hi[0]-lo[0])*.37+(p.z-.43)/.15*.13) for p in pts];solid=.018
 elif kind.startswith('coil_'):
  a=math.pi/4+int(kind[-1])*math.pi/2;pts=[(.76*math.cos(a)+(p.y+.65)*.045/.07,.76*math.sin(a)+(p.z-1.03)*.045/.07,1.02+(p.x-lo[0])/(hi[0]-lo[0])*.63) for p in pts]
 elif kind=='collection_tray':
  fs=fs[:2]+fs[4:];pts=[(p.x,-1.05+(p.y-.88)*.92,.22+(p.z-.21)) for p in pts];solid=.025;mat=m['wood']
 o=mesh('CONDENSER | REUSED '+name,pts,fs,mat,col,root);surfaces.apply(o,mat,m['endgrain'] if mat==m['wood'] else None);o['retained_starter_group']=name;reused[kind]=o
 if solid:mod=o.modifiers.new('Actual supported plate thickness','SOLIDIFY');mod.thickness=solid;mod.offset=0
# Shared curved routing: explicit connected endpoints and soft elbows.
def pipe(n,points,r=.035,mat=None):
 pts=[Vector(p) for p in points];smooth=[pts[0]]
 for i in range(1,len(pts)-1):
  incoming=(pts[i]-pts[i-1]).normalized();outgoing=(pts[i+1]-pts[i]).normalized();cut=min(.065,(pts[i]-pts[i-1]).length*.30,(pts[i+1]-pts[i]).length*.30);a=pts[i]-incoming*cut;b=pts[i]+outgoing*cut
  for k in range(9):t=k/8;smooth.append((1-t)**2*a+2*(1-t)*t*pts[i]+t*t*b)
 smooth.append(pts[-1]);return tube('CONDENSER | '+n,[(p,(smooth[min(i+1,len(smooth)-1)]-smooth[max(0,i-1)]).normalized(),r,r*.65) for i,p in enumerate(smooth)],mat or m['copper'],col,root,24)
def torus(n,pos,major,minor,mat):
 bpy.ops.mesh.primitive_torus_add(major_segments=96,minor_segments=20,location=pos,major_radius=major,minor_radius=minor);o=bpy.context.object
 for c in tuple(o.users_collection):c.objects.unlink(o)
 col.objects.link(o);o.name='CONDENSER | '+n;o.parent=root;surfaces.apply(o,mat);return o
bore(reused['base'],C('temporary real inlet foundation clearance',(0,1.23,.36),.30,.85,m['iron'],'Y'))
bore(reused['upper_steam_pipe'],C('temporary fixed full-bore throat',(0,1.20,.36),.245,.95,m['iron'],'Y'));reused['upper_steam_pipe']['role']='stationary_socket'
ring('full-size fixed inlet collar',(0,1.4625,.36),.34,.245,.075,m['iron'],'Y')
for i in range(8):
 a=math.tau*i/8;C('collar retained bolt',(.308*math.cos(a),1.47,.36+.308*math.sin(a)),.016,.07,m['bronze'],'Y',segments=6)
tail=tube('CONDENSER | fixed inlet reducing tail',[(Vector((0,y,.36)),Vector((0,-1,0)),outside,inside) for y,outside,inside in [(.90,.285,.245),(.83,.20,.16),(.75,.065,.042)]],m['iron'],col,root,48);tail['role']='stationary_socket'
saddle=B('grounded inlet pipe saddle',(0,1.18,.13),(.64,.20,.26),m['bedded-limestone']);bore(saddle,C('temporary saddle seat',(0,1.18,.36),.286,.40,m['iron'],'Y'))
for x in (-.28,.28):C('saddle anchor',(x,1.18,.25),.017,.065,m['bronze'])
# A genuinely hollow chamber, front inspection opening and process discharge.
bore(reused['cooling_tower'],C('temporary actual treatment cavity',(0,0,1.365),.515,1.21,m['iron']))
bore(reused['cooling_tower'],B('temporary actual inspection opening',(0,-.55,1.365),(.44,.36,.57),m['iron']))
bore(reused['cooling_tower'],C('temporary stone discharge opening',(-.34,-.50,.94),.12,.36,m['iron'],'Y'))
for z in (1.065,1.665):B('window seated horizontal frame',(0,-.55,z),(.55,.20,.055),m['iron'])
for x in (-.25,.25):B('window seated vertical frame',(x,-.55,1.365),(.055,.20,.65),m['iron'])
B('real crude-glass inspection pane',(0,-.651,1.365),(.47,.014,.60),m['crude-inspection-glass'],bevel=.002)
for x in (-.25,.25):
 for z in (1.12,1.61):C('window frame retained fastener',(x,-.63,z),.014,.045,m['bronze'],'Y',segments=6)
for z in (.82,1.88):ring('chamber retaining hoop',(0,0,z),.591,.565,.045,m['iron'])
# Brick firebox and stone heat plate carry the chamber; the stack is founded.
C('chamber supported heat plate',(0,0,.70),.65,.06,m['bedded-limestone'])
B('firebox clay floor',(0,0,.20),(1.28,1.18,.16),m['brick'])
for z in (.315,.425,.535,.645):
 for x in (-.58,.58):B('fired brick side wall',(x,0,z),(.15,1.12,.10),m['brick'])
 B('fired brick rear wall',(0,.50,z),(1.16,.15,.10),m['brick'])
 for x in (-.47,.47):B('front fire door brick jamb',(x,-.50,z),(.27,.15,.10),m['brick'])
B('fire door lintel',(0,-.51,.645),(1.10,.17,.10),m['bedded-limestone'])
for x in (-.24,.24):B('founded fire door iron jamb',(x,-.597,.42),(.035,.035,.31),m['iron'])
B('fire door iron lintel',(0,-.597,.57),(.51,.035,.035),m['iron'])
for x in (-.18,-.09,0,.09,.18):C('fitted hearth grate bar',(x,-.35,.292),.012,.40,m['iron'],'Y')
for i in range(9):
 x=(i%3-1)*.105;y=-.35+(i//3-1)*.09;B('charcoal in grounded hearth',(x,y,.315),(.095,.07,.045),m['charcoal-bed'])
flame=E('working chemical hearth flame',(0,-.35,.34))
for x in (-.105,0,.105):
 o=lathe('CONDENSER | small rooted burner flame',[(0,0),(.026,.01),(.032,.045),(.018,.085),(0,.145)],(x,0),m['small-burner-flame'],col,flame,24);surfaces.physical_box_uv(o)
B('stack continuous foundation',(.98,.50,.20),(.40,.40,.16),m['bedded-limestone'])
B('founded connecting firebox flue',(.77,.50,.40),(.44,.29,.30),m['brick'])
for row in range(22):
 z=.335+row*.105
 for x in (.87,1.09):B('stack individual side brick',(x,.50,z),(.08,.30,.10),m['brick'])
 for y in (.39,.61):B('stack individual end brick',(.98,y,z),(.14,.08,.10),m['brick'])
for x in (.85,1.11):B('supported stack cap side',(x,.50,2.64),(.10,.36,.09),m['bedded-limestone'])
for y in (.37,.63):B('supported stack cap end',(.98,y,2.64),(.16,.10,.09),m['bedded-limestone'])
# Four retained coil groups become steam-distribution risers, not invented coolant.
for z in (1.02,1.65):torus('closed steam jacket header',(0,0,z),.76,.045,m['copper'])
for i in range(4):
 a=math.pi/4+i*math.pi/2;pt=Vector((.76*math.cos(a),.76*math.sin(a),1.25));bore(reused['coil_'+str(i)],C('temporary actual riser bore',pt,.029,1.05,m['iron']))
 for z in (1.10,1.57):
  pipe('jacket seated chamber connection',[(.76*math.cos(a),.76*math.sin(a),z),(.545*math.cos(a),.545*math.sin(a),z)],.035)
  beam('jacket grounded support',(.84*math.cos(a),.84*math.sin(a),.12),(.76*math.cos(a),.76*math.sin(a),1.02),.035,m['iron']) if z==1.10 else None
  cutter=C('temporary jacket chamber port',(.58*math.cos(a),.58*math.sin(a),z),.025,.20,m['iron']);cutter.rotation_euler=Vector((math.cos(a),math.sin(a),0)).to_track_quat('Z','Y').to_euler();bore(reused['cooling_tower'],cutter)
pipe('fixed incoming steam riser',[(0,.75,.36),(0,.91,.36),(0,.91,1.65),(0,.76,1.65)],.055)
# Open loading neck preserves the saved conical lid; a side wood charge rack.
neck=ring('lid central shaft gland',(0,0,2.20),.083,.028,.18,m['bronze'])
for x in (.71,.98):
 for y in (-.25,.20):B('wood charge rack grounded leg',(x,y,.46),(.065,.065,.68))
B('wood charge rack plank',(.82,-.03,.82),(.43,.64,.07))
for i in range(4):
 o=B('actual wood charge billet',(.82,-.25+i*.145,.905),(.36,.11,.10));o.rotation_euler.z=.12*(i%2-.5)
for z in (1.02,1.18):B('seated charge hatch strap',(.556,.08,z),(.06,.32,.04),m['iron'])
for z in (1.02,1.18):C('charge hatch latch',(.61,.08,z),.025,.09,m['bronze'],'X')
# Internal rake stays within the chamber and is visible through the real window.
shaft=E('slow treatment rake',(0,0,1.60));C('actual rake through shaft',(0,0,0),.025,1.64,m['iron'],parent=shaft)
for z in (-.43,-.06):
 for i in range(3):
  a=i*math.tau/3;beam('contained mineral rake arm',(.04*math.cos(a),.04*math.sin(a),z),(.35*math.cos(a),.35*math.sin(a),z),.035,m['wood'],shaft)
  o=B('wood charge turning in rake',(.25*math.cos(a),.25*math.sin(a),z+.055),(.15,.075,.07),m['wood'],shaft);o.rotation_euler.z=a
ring('fixed rake lower bored bearing',(0,0,.82),.065,.028,.09,m['bronze']);pedestal=C('lower bearing grounded pedestal',(0,0,.79),.075,.08,m['bedded-limestone']);bore(pedestal,C('temporary pedestal shaft bore',(0,0,.79),.028,.20,m['iron']))
# Steam-driven piston and exposed, fitted rigid slider-crank power the slow rake.
crank=E('steam engine crank and vertical shaft',(-.96,.55,1.30));C('crank vertical through shaft',(0,0,-.175),.025,.37,m['iron'],parent=crank);ring('exposed steam crank rim',(0,0,0),.16,.122,.045,m['iron'],parent=crank)
for i in range(5):
 a=i*math.tau/5;beam('crank rim seated spoke',(0,0,0),(.14*math.cos(a),.14*math.sin(a),0),.027,m['iron'],crank)
C('crank retained upper pin',(.10,0,.075),.012,.15,m['bronze'],parent=crank);upper=E('crank pin seat',(.10,0,.09),crank)
ram=E('guided steam piston');C('actual piston rod',(0,-.18,0),.018,.45,m['bronze'],'Y',ram);C('fitted steam piston',(0,-.42,0),.089,.08,m['iron'],'Y',ram);B('piston lower fork seat',(0,0,.025),(.10,.07,.025),m['iron'],ram);B('piston upper fork seat',(0,0,.15),(.10,.07,.025),m['iron'],ram)
for x in (-.04,.04):B('clevis separated fork cheek',(x,0,.075),(.018,.09,.15),m['iron'],ram)
C('lower retained crank pin',(0,0,.09),.012,.11,m['bronze'],parent=ram);lower=E('piston pin seat',(0,0,.09),ram)
rod=E('rigid half-tile steam connecting rod');B('rigid connecting web',(0,0,0),(.024,.024,.45),m['iron'],rod)
for z in (-.25,.25):ring('bored connecting rod eye',(0,0,z),.031,.014,.029,m['bronze'],'Y',rod)
transfer=E('offset belt transfer shaft',(-.96,.96,1.30));C('offset supported transfer shaft',(0,0,.35),.025,1.39,m['iron'],parent=transfer)
rod.rotation_mode='QUATERNION'
# Bored eyes have local Y normal to the XY linkage plane after track-Z/up-Y solve.
body=ring('actual hollow steam cylinder',(-.96,-.40,1.30),.13,.095,.56,m['copper'],'Y')
for y in (-.68,-.12):
 cap=C('steam cylinder end cap',(-.96,y,1.30),.145,.035,m['iron'],'Y')
 if y>-.2:bore(cap,C('temporary real rod guide',(-.96,y,1.30),.0205,.15,m['iron'],'Y'))
 for x in (-1.08,-.84):B('cylinder grounded mounting leg',(x,y,.69),(.065,.09,1.14));B('cylinder seated foot',(x,y,.17),(.13,.18,.08),m['iron'])
 for i in range(4):
  a=math.pi/4+i*math.pi/2;C('cylinder cap retained tie',(-.96+.135*math.cos(a),y,1.30+.135*math.sin(a)),.012,.06,m['bronze'],'Y',segments=6)
for x in (-1.20,-.72):
 B('engine bearing grounded timber post',(x,.55,1.17),(.10,.13,2.10));B('engine post seated foot',(x,.55,.18),(.17,.20,.12),m['iron'])
 for z in (1.05,):
  beam('engine post short bearing knee',(x,.55,z-.30),(-.96+math.copysign(.11,x+.96),.55,z-.03),.05)
for x in (-1.20,-.72):
 B('transfer bearing grounded rear post',(x,.96,1.17),(.10,.13,2.10));B('transfer rear post seated foot',(x,.96,.18),(.17,.20,.12),m['iron'])
 B('front to rear bearing tie',(x,.755,2.20),(.10,.55,.10))
for xx,yy,z in [(-.96,.55,1.00),(-.96,.96,1.00),(-.96,.96,2.20)]:
 cross=B('engine shaft bearing beam',(xx,yy,z),(.58,.16,.10));bore(cross,C('temporary timber shaft clearance',(xx,yy,z),.030,.30,m['iron']));ring('fixed bored engine shaft bearing',(xx,yy,z+(.035 if z<1.1 else .075)),.055,.028,.06 if z<1.1 else .10,m['bronze'])
pipe('steam admission to cylinder',[(0,.91,.70),(0,1.19,.70),(-1.30,1.19,.70),(-1.30,1.19,1.30),(-1.30,-.56,1.30),(-1.085,-.56,1.30)],.023)
bore(body,C('temporary actual steam admission',(-1.085,-.56,1.30),.018,.17,m['iron'],'X'))
pipe('steam return into treatment chamber',[(-.835,-.56,1.30),(-.68,-.56,1.30),(-.68,-.28,1.30),(-.49,-.28,1.30)],.023)
bore(body,C('temporary actual steam return',(-.835,-.56,1.30),.018,.17,m['iron'],'X'));bore(reused['cooling_tower'],C('temporary chamber steam return opening',(-.49,-.28,1.30),.018,.20,m['iron'],'X'))
# Equal-radius pulleys and exact common tangents, safely above the lid.
def pulley(n,parent,localz,r=.14):
 for sign in (-1,1):ring(n+' retaining flange',(0,0,localz+sign*.030),r+.016,r-.035,.012,m['iron'],parent=parent)
 ring(n+' running rim',(0,0,localz),r,r-.035,.046,m['bronze'],parent=parent)
 for i in range(4):
  a=math.tau*i/4;beam(n+' seated spoke',(0,0,localz),((r-.02)*math.cos(a),(r-.02)*math.sin(a),localz),.025,m['iron'],parent)
pulley('offset transfer upper pulley',transfer,1.05);pulley('rake driven pulley',shaft,.75)
pulley('crank lower takeoff pulley',crank,-.18,.10);pulley('offset transfer lower pulley',transfer,-.18,.10)
for label,c1,c2,r,z in [('upper rake belt',(-.96,.96),(0.,0.),.14,2.35),('lower offset transfer belt',(-.96,.55),(-.96,.96),.10,1.12)]:
 a=np.array(c1);b=np.array(c2);direction=(b-a)/np.linalg.norm(b-a);perp=np.array([direction[1],-direction[0]]);angle=math.atan2(perp[1],perp[0]);points=[b+r*np.array([math.cos(t),math.sin(t)]) for t in np.linspace(angle,angle+math.pi,40)]+[a-r*perp]+[a+r*np.array([math.cos(t),math.sin(t)]) for t in np.linspace(angle+math.pi,angle+math.tau,40)];pts=[];fs=[]
 for i,pt in enumerate(points):
  tangent=points[(i+1)%len(points)]-points[(i-1)%len(points)];normal=np.array([-tangent[1],tangent[0]])/np.linalg.norm(tangent)
  for side,thick in [(-1,-1),(1,-1),(1,1),(-1,1)]:q=pt+normal*.004*thick;pts.append((float(q[0]),float(q[1]),z+side*.021))
 for i in range(len(points)):
  j=(i+1)%len(points)
  for k in range(4):fs.append((4*i+k,4*j+k,4*j+(k+1)%4,4*i+(k+1)%4))
 belt=mesh('CONDENSER | exact tangent '+label,pts,fs,m['oiled-leather-belt'],col,root);surfaces.physical_box_uv(belt)
# Grounded separate stone and waste compartments; no water-output mouth.
for x in (-.78,.78):
 for y in (-1.24,-.84):B('collection tray grounded foot',(x,y,.17),(.09,.09,.10))
B('stone waste tray divider',(.34,-1.05,.35),(.035,.50,.23))
for i in range(10):
 x=-.70+(i%5)*.20;y=-1.17+(i//5)*.22;bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2,radius=.10,location=(x,y,.32));o=bpy.context.object
 for c in tuple(o.users_collection):c.objects.unlink(o)
 col.objects.link(o);o.parent=root;o.name='CONDENSER | actual stone output cobble';o.scale=(1,.8,.7);surfaces.apply(o,m['mineral-stone-output'])
for i in range(3):B('industrial waste collected separately',(.52+i*.12,-1.05,.30),(.09,.16,.08),m['charcoal-bed'])
for i in range(3):
 a=i*math.tau/3;B('mineral forming in contained rake',(.23*math.cos(a),.23*math.sin(a),-.33),(.11,.09,.07),m['mineral-stone-output'],shaft)
previous=None
for frame in range(194):
 theta=0 if frame==0 else math.tau*(frame-1)/192;crank.rotation_euler.z=theta;transfer.rotation_euler.z=theta;shaft.rotation_euler.z=theta;pin=Vector((-.96+.10*math.cos(theta),.55+.10*math.sin(theta),1.39));bottom=Vector((-.96,pin.y-math.sqrt(.50**2-(pin.x+.96)**2),1.39));ram.location=(-.96,bottom.y,1.30);rod.location=(pin+bottom)/2;q=(pin-bottom).to_track_quat('Z','Y')
 if previous and q.dot(previous)<0:q.negate()
 rod.rotation_quaternion=q;previous=q.copy();flame.scale=(.001,)*3 if frame==0 else (1,1,.9+.12*math.sin(theta*5)+.06*math.cos(theta*3))
 for o in (crank,transfer,shaft,ram,rod,flame):o.keyframe_insert(data_path='location',frame=frame);o.keyframe_insert(data_path='rotation_quaternion' if o==rod else 'rotation_euler',frame=frame);o.keyframe_insert(data_path='scale',frame=frame)
for o in (crank,transfer,shaft,ram,rod,flame):linear(o)
for o in root.children_recursive:
 if o.type!='MESH':continue
 if o.modifiers:o.data=bpy.data.meshes.new_from_object(o.evaluated_get(bpy.context.evaluated_depsgraph_get()));o.modifiers.clear()
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.triangulate(bm,faces=list(bm.faces));bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-7);bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=1e-7);bmesh.ops.delete(bm,geom=[v for v in bm.verts if not v.link_faces],context='VERTS');bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free();o.data.calc_loop_triangles();bad={t.polygon_index for t in o.data.loop_triangles if t.area<1e-12}
 if bad:
  bm=bmesh.new();bm.from_mesh(o.data);bm.faces.ensure_lookup_table();bmesh.ops.delete(bm,geom=[bm.faces[i] for i in bad],context='FACES');bm.to_mesh(o.data);bm.free()
 if not o.data.uv_layers:surfaces.physical_box_uv(o)
s.frame_start=1;s.frame_end=193;s.render.fps=48;s.frame_set(1);profile=dict(camera_policy='fmpl.factorio45.v1',capture_kind='entity',orientation_policy='rotatable',directions=[0,90,180,270],states={'idle':[0],'working':list(range(1,193,6))},source_size=256,camera_override=dict(type='ORTHO',elevation_deg=45,azimuth_deg=0,distance=8,ortho_scale=6.2,target=[0,0,1.1]));install_canonical_camera(s,profile,bpy);s.render.resolution_x=s.render.resolution_y=256;assert_clean(s,profile,bpy)
root['prototype']='assembling-machine/steam-condenser';root['units_per_tile']=1.;root['native_power']='Chemical burner 1kW';root['purpose']='Actual wood5+steam200 -> stone10+industrialwaste1; no water output. Four actual directions, one fixed inlet per facing.'
bpy.ops.file.pack_all();source=O/'steam-condenser-v2.blend';bpy.ops.wm.save_as_mainfile(filepath=str(source),compress=True);bpy.ops.wm.open_mainfile(filepath=str(source));s=bpy.context.scene;root=bpy.data.objects['EXPORT | Tanks wood steam treatment condenser'];bpy.ops.object.select_all(action='DESELECT')
for o in [root,*root.children_recursive]:o.select_set(True)
bpy.ops.export_scene.gltf(filepath=str(O/'steam-condenser-v2.glb'),export_format='GLB',use_selection=True,export_cameras=False,export_lights=False,export_animations=True,export_animation_mode='SCENE',export_anim_scene_split_object=False,export_frame_range=True,export_force_sampling=True,export_frame_step=1,export_apply=True,export_extras=True)
(O/'capture-profile.json').write_text(json.dumps(profile,indent=2)+'\n');(O/'construction-receipt.json').write_text(json.dumps(dict(starter_sha256=sha(starter),preserved_starter_groups=list(groups),source_sha256=sha(source),runtime_sha256=sha(O/'steam-condenser-v2.glb'),native_power='chemical burner1kW',actual_recipe_contracts=1,owner_visual_approved=False,native_integrated=False,review_status='held-pending-source-export-and-native-review'),indent=2)+'\n')
projection=bpy.data.objects.new('SPRITE ONLY | square ground correction',None);s.collection.objects.link(projection);projection.scale.y=math.sqrt(2);root.parent=projection;s.render.resolution_x=s.render.resolution_y=512
for name,yaw in [('front',0),('rear',180),('side',90)]:
 root.rotation_euler.z=math.radians(yaw);s.render.filepath=str(O/(name+'-review512.png'));bpy.ops.render.render(write_still=True)
root.rotation_euler.z=0
with temporary_inspection_camera(s,bpy,'Fitted steam piston drive and real treatment window') as camera:
 target=Vector((-.30,-.15,1.40));camera.data.type='ORTHO';camera.data.ortho_scale=3.3;camera.location=target+Vector((-3,-4,1.9));camera.rotation_euler=(target-camera.location).to_track_quat('-Z','Y').to_euler();s.camera=camera;s.render.filepath=str(O/'mechanism-close512.png');bpy.ops.render.render(write_still=True)
print('TANKS_CONDENSER_SAVED_REOPENED_EXPORTED',sha(source),flush=True)
