"""Develop the held quarry's construction and geology while retaining its useful motions."""
import bpy,bmesh,json,math,sys,tempfile,hashlib
import numpy as np
from pathlib import Path
from mathutils import Vector
H=Path(__file__).resolve().parent;R=H.parents[3];P=R/'models/island-survival/quarry/candidates/v1-pilot01';O=R/'models/island-survival/quarry/candidates/v2-detail02'
if O.exists():raise FileExistsError(O)
O.mkdir(parents=True);tempfile.tempdir=str(R/'build/quarry-export-temp')
sys.path.insert(0,str(R/'models/island-survival/primitive-steam-powered-pump/v3'))
from mesh_util import mesh,box,cylinder,tube,lathe
import surfaces
sys.path.insert(0,str(R.parent/'model-production/tools/fmpl'))
from blender_camera_guard import assert_clean,temporary_inspection_camera
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
source=P/'quarry-v1.blend';assert sha(source)=='1876df147328fc5a49be6cb0206693ddb986c97b648c049c3fe5b64104264030'
bpy.ops.wm.open_mainfile(filepath=str(source));scene=bpy.context.scene;scene.frame_set(1)
root=bpy.data.objects['EXPORT | Quarry all authored parts']
col=bpy.data.collections.new('QUARRY V2 | authored joints geology and machinery');scene.collection.children.link(col)
def oldmat(suffix):return next(m for m in bpy.data.materials if m.name.endswith(' | '+suffix))
wood=oldmat('long-grain-oak');endgrain=oldmat('cut-oak-growth-rings');iron=oldmat('cast-iron-housing');bronze=oldmat('worn-bronze-fittings');copper=oldmat('aged-copper-jacket');brick=oldmat('fired-clay-lining');rope=oldmat('quarry-twisted-hemp')
oldstone=oldmat('quarry-stone-face');oldbed=oldmat('quarry-stone-bed')
rng=np.random.default_rng(171130);shape=(512,512);u,v=np.meshgrid(np.linspace(0,1,512),np.linspace(0,1,512))
coarse=surfaces.field(rng,shape,.017);fine=surfaces.field(rng,shape,.19)
layers=np.sin(v*4*math.pi+.28*np.sin(u*math.tau)+.10*coarse)
fresh_tone=np.clip(.34+.038*coarse+.024*layers+.006*fine,.17,.55)
fresh=surfaces.material('quarry-v2-fresh-cleavage',np.stack([fresh_tone*1.02,fresh_tone,fresh_tone*.93],axis=-1),.82+.04*fine,.5+.065*layers+.018*fine,0,O)
bed_tone=np.clip(.23+.035*coarse+.008*fine,.10,.42)
bed=surfaces.material('quarry-v2-weathered-strata',np.stack([bed_tone*1.03,bed_tone,bed_tone*.91],axis=-1),.92+.02*fine,.5+.04*coarse+.02*fine,0,O)
dirt=np.stack([.19+.025*coarse,.137+.02*coarse,.082+.014*coarse],axis=-1)
pebbles=np.zeros(shape)
for _ in range(110):
 x,y=rng.uniform(0,1,2);rx,ry=rng.uniform(.005,.018,2);distance=((u-x)/rx)**2+((v-y)/ry)**2;pebbles=np.maximum(pebbles,np.clip(1-distance,0,1))
dirt=dirt*(1-pebbles[:,:,None]*.65)+np.stack([.34+.01*fine,.32+.01*fine,.27+.01*fine],axis=-1)*pebbles[:,:,None]*.65
soil=surfaces.material('quarry-v2-ground-chips-and-earth',dirt,.96+.008*fine,.5+.065*coarse+.14*pebbles,0,O)
coal_tone=np.clip(.025+.009*coarse+.003*fine,.008,.06)
coal=surfaces.material('quarry-v2-fuel-and-ash',np.stack([coal_tone*.94,coal_tone,coal_tone*.95],axis=-1),.96+.008*fine,.5+.07*coarse,0,O)
for m in (fresh,bed,soil,coal):m.name=m.name.replace('PUMP V3','QUARRY V2');m['surface_authorship']='Fresh cut strata, weathered bank, chipped floor and fuel each have physical placement and independent image surfaces'
def B(n,p,d,m,parent=root,bevel=.004):
 o=box('QUARRY V2 | '+n,p,d,m,col,parent,bevel);surfaces.apply(o,m,endgrain if m==wood else None);return o
def C(n,p,r,depth,m,axis='Z',parent=root,segments=32):
 o=cylinder('QUARRY V2 | '+n,p,r,depth,m,col,parent,axis,segments);surfaces.apply(o,m);return o
def M(n,verts,faces,m,parent=root,bevel=0):
 o=mesh('QUARRY V2 | '+n,verts,faces,m,col,parent,bevel);surfaces.apply(o,m,endgrain if m==wood else None);return o
def beam(n,a,b,w,m=wood,parent=root):
 a,b=Vector(a),Vector(b);o=B(n,(a+b)/2,(w,w,(b-a).length),m,parent);o.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler();return o
def erase(o):
 if o and bpy.data.objects.get(o.name):bpy.data.objects.remove(o,do_unlink=True)
def boolean(a,b,operation):
 bpy.context.view_layer.objects.active=a;mod=a.modifiers.new('Authored fitted opening','BOOLEAN');mod.operation=operation;mod.object=b;mod.solver='EXACT';bpy.ops.object.modifier_apply(modifier=mod.name)
def torus(n,p,major,minor,m,parent=root,axis='Z'):
 bpy.ops.mesh.primitive_torus_add(major_segments=48,minor_segments=8,major_radius=major,minor_radius=minor)
 o=bpy.context.object
 for c in tuple(o.users_collection):c.objects.unlink(o)
 col.objects.link(o);o.parent=parent;o.name='QUARRY V2 | '+n;o.location=p
 if axis=='X':o.rotation_euler.y=math.pi/2
 elif axis=='Y':o.rotation_euler.x=math.pi/2
 surfaces.apply(o,m);return o
def pipe(n,start,end,outer,inner,m=bronze,parent=root):
 a,b=Vector(start),Vector(end);t=(b-a).normalized()
 return tube('QUARRY V2 | '+n,[(tuple(a),tuple(t),outer,inner),(tuple(b),tuple(t),outer,inner)],m,col,parent)
def prism(n,outline,z0,z1,m):
 v=[(x,y,z) for z in (z0,z1) for x,y in outline];count=len(outline)
 f=[tuple(reversed(range(count))),tuple(range(count,2*count))]
 f.extend((i,(i+1)%count,(i+1)%count+count,i+count) for i in range(count))
 return M(n,v,f,m)
def profiled_bank(n,sections,profile,m,axis='X'):
 v=[];k=len(profile)
 for i,coordinate in enumerate(sections):
  for j,(a,z) in enumerate(profile):
   if axis=='X':
    b=a+(.012*math.sin(i*2.1) if j>=4 else 0);zz=z+(.008*math.cos(i*1.7) if j==4 else 0);v.append((coordinate,b,zz))
   else:
    b=a+(.012*math.sin(i*1.9) if j>=2 else 0);v.append((b,coordinate,z))
 f=[]
 for i in range(len(sections)-1):
  for j in range(k):f.append((i*k+j,i*k+(j+1)%k,(i+1)*k+(j+1)%k,(i+1)*k+j))
 f.extend([tuple(reversed(range(k))),tuple(range((len(sections)-1)*k,len(sections)*k))])
 o=M(n,v,f,m);bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free();return o
# Connected, irregular bedrock with a genuine stepped extraction bench.
outline=[(-1.45,-1.28),(-1.34,-1.44),(-.76,-1.40),(-.34,-1.45),(.32,-1.41),(1.20,-1.44),(1.44,-1.24),(1.40,-.72),(1.45,-.17),(1.41,.50),(1.44,1.20),(1.27,1.43),(.55,1.39),(-.15,1.45),(-.80,1.41),(-1.42,1.26),(-1.40,.65),(-1.45,.04),(-1.40,-.55)]
newbase=prism('irregular continuous bedrock',outline,0,.32,bed)
north=profiled_bank('hewn north benches',[-1.275,-1.0,-.72,-.42,-.12,.18,.48,.78,1.02,1.275],[(.745,.20),(.745,.73),(.885,.73),(.885,1.135),(1.415,1.135),(1.415,.20)],fresh)
east=profiled_bank('engine-side rock bench',[-1.18,-.92,-.64,-.36,0,.35,.68,.94,1.18],[(.765,.16),(.765,.88),(1.435,.88),(1.435,.16)],bed,'Y')
for o in (north,east):boolean(newbase,o,'UNION');erase(o)
for i in range(10):
 x=-1.10+i*.24
 cutter=B('temporary feather wedge kerf',(x,.765,.58),(.026,.13,.22),fresh,bevel=0);boolean(newbase,cutter,'DIFFERENCE');erase(cutter)
 # Wet wooden wedges sit inside the cut kerfs rather than hovering on a face.
 p=[(x+dx,y,z) for y,s in ((.713,1),(.81,.38)) for dx,z in [(-.010*s,.55),(.010*s,.55),(.010*s,.62),(-.010*s,.62)]]
 wedge=M('seated splitting wedge',p,[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],wood,bevel=.001)
oldbase=bpy.data.objects['QUARRY | REUSED quarry_base_stone'];oldbase.data=newbase.data;erase(newbase);oldbase.data.name='Refined connected quarry bedrock'
mod=oldbase.modifiers.new('Hewn edge arris','BEVEL');mod.width=.009;mod.segments=2
floor=prism('irregular chipped pit floor',[(-1.30,-1.27),(.62,-1.26),(.63,-.20),(.60,.25),(.45,.30),(.39,.71),(-.40,.71),(-.46,.36),(-1.27,.39)],.29,.43,soil)
oldfloor=bpy.data.objects['QUARRY | REUSED quarry_excavation_floor'];oldfloor.data=floor.data;erase(floor)
# Fine mineral-bearing fracture paths follow the exposed cutting surfaces.
for o in list(root.children_recursive):
 if o.name.startswith('QUARRY | exposed '):erase(o)
for label,y,z,material in [('iron',.743,.65,oldmat('quarry-iron-seam')),('copper',.883,.97,oldmat('quarry-copper-seam'))]:
 for branch in range(3):
  xs=np.linspace(-1.15+branch*.08,1.12-branch*.10,8);zs=z+.022*np.sin(xs*8+branch)+branch*.013
  v=[(float(x),y,float(zz+offset)) for offset in (-.004,.004) for x,zz in zip(xs,zs)]
  M(label+' mineral fracture',v,[(i,i+1,i+9,i+8) for i in range(7)],material)
# Split bearing blocks, actual bored bushes, cap bolts and shaft collars.
for o in list(root.children_recursive):
 if 'shaft bearing housing' in o.name or 'outboard bearing housing' in o.name:erase(o)
for o in root.children_recursive:
 if o.name.startswith('QUARRY | shaft bearing seat'):o.location.z=1.95
pier=bpy.data.objects['QUARRY | outboard bearing pier']
for vtx in pier.data.vertices:vtx.co.z*=1.14/1.30
pier.location.z=1.45
def pillow(x,label):
 B(label+' sole plate',(x,.59,2.0325),(.24,.27,.025),iron)
 for z,part in ((2.065,'lower saddle'),(2.135,'split cap')):
  block=B(label+' '+part,(x,.59,z),(.18,.22,.07),iron,bevel=0)
  cutter=C('temporary bearing bore',(x,.59,2.1),.052,.23,iron,'X');boolean(block,cutter,'DIFFERENCE');erase(cutter)
  bevel=block.modifiers.new('Bearing cap edge','BEVEL');bevel.width=.003;bevel.segments=2
 pipe(label+' bronze plain bush',(x-.095,.59,2.1),(x+.095,.59,2.1),.050,.0325)
 for xx in (x-.055,x+.055):
  for yy in (.51,.67):
   C(label+' cap stud',(xx,yy,2.105),.010,.17,iron,segments=16)
   torus(label+' cap washer',(xx,yy,2.174),.018,.004,bronze)
   C(label+' six-flat cap nut',(xx,yy,2.187),.023,.018,bronze,segments=6)
for x,label in [(-.47,'left windlass bearing'),(.47,'right windlass bearing'),(1.16,'outboard drive bearing')]:pillow(x,label)
for x in (-.65,1.235):
 pipe('fixed shaft stop collar',(x-.018,.59,2.1),(x+.018,.59,2.1),.049,.031,iron)
 C('collar retaining screw',(x,.59,2.153),.013,.015,bronze,segments=6)
# Bolted straps secure actual A-frame junctions; heel and thrust braces carry loads.
for sign in (-1,1):
 for y in (.493,.707):
  pts=[(sign*x,y,z) for x,z in [(.34,2.225),(.52,2.225),(.56,2.445),(.35,2.445)]]
  plate=M('head joint cheek strap',pts,[(0,1,2,3)],iron)
  solid=plate.modifiers.new('Iron strap thickness','SOLIDIFY');solid.thickness=.012
 for x,z in [(sign*.43,2.26),(sign*.43,2.40)]:
  C('head through-bolt',(x,.6,z),.013,.24,iron,'Y',segments=16)
  for y in (.477,.723):C('head square nut',(x,y,z),.026,.023,bronze,'Y',segments=4)
 B('rear brace stone seat',(sign*.95,1.14,1.095),(.26,.24,.08),fresh)
 for x in (sign*.95-.07,sign*.95+.07):
  C('heel anchoring spike',(x,.5,.37),.014,.11,iron,segments=12)
  C('heel anchor head',(x,.5,.43),.026,.018,bronze,segments=4)
beam('outboard diagonal brace',(1.16,.59,1.02),(.50,.59,2.20),.10)
for y,z in [(.59,1.02),(.59,2.20)]:pass
# Windlass has a real axial bore and a continuously laid rope coil.
drum=bpy.data.objects['QUARRY | winding drum']
for o in list(drum.children):
 if 'wound hemp turn' in o.name:erase(o);continue
 if any(s in o.name for s in ('refined original hoist roller','retaining flange','clutch counterplate')):
  cutter=C('temporary drum spindle bore',(0,0,0),.033,1.5,iron,'X',parent=drum)
  boolean(o,cutter,'DIFFERENCE');erase(cutter)
for x in (-.30,.30):pipe('drum bronze sleeve',(x-.018,0,0),(x+.018,0,0),.048,.031,bronze,drum)
coil=[]
for i in range(1601):
 t=i/1600;a=(t-.5)*20*math.tau+math.pi;p=Vector((.48*(t-.5),.188*math.cos(a),.188*math.sin(a)))
 tangent=Vector((.48,-.188*20*math.tau*math.sin(a),.188*20*math.tau*math.cos(a))).normalized()
 coil.append((p,tangent))
def solid_cord(name,path,radius,material,parent=root):
 vs=[];count=8
 for p,t in path:
  test=Vector((1,0,0)) if abs(t.x)<.9 else Vector((0,1,0));a=(test-t*test.dot(t)).normalized();b=t.cross(a)
  for j in range(count):vs.append(tuple(p+radius*(math.cos(j*math.tau/count)*a+math.sin(j*math.tau/count)*b)))
 fs=[]
 for i in range(len(path)-1):
  for j in range(count):fs.append((i*count+j,i*count+(j+1)%count,(i+1)*count+(j+1)%count,(i+1)*count+j))
 fs.extend([tuple(reversed(range(count))),tuple(range((len(path)-1)*count,len(path)*count))])
 return M(name,vs,fs,material,parent)
solid_cord('laid hemp windlass coil',coil,.0105,rope,drum)
torus('fixed cable guide eye',(0,.402,1.97),.024,.007,bronze)
beam('guide eye support',(-.47,.59,1.97),(-.031,.402,1.97),.022,iron)
# Cargo and bucket fittings preserve the upright bucket's animation and rope endpoint.
bucket=bpy.data.objects['QUARRY | upright lifting bucket'];load=bpy.data.objects['QUARRY | reused lifted stone']
points=[(-.19,-.20,-.17),(.16,-.22,-.17),(.22,-.03,-.17),(.15,.20,-.17),(-.18,.20,-.17),(-.23,-.04,-.02),(.21,-.12,.01),(.20,.17,.04),(-.17,.23,.02),(-.14,-.17,.15),(.12,-.14,.17),(.16,.12,.13),(-.12,.16,.16)]
data=bpy.data.meshes.new('Hand-cleaved lifted stone');bm=bmesh.new()
for p in points:bm.verts.new(p)
bmesh.ops.convex_hull(bm,input=list(bm.verts),use_existing_faces=False)
loose=[v for v in bm.verts if not v.link_faces]
if loose:bmesh.ops.delete(bm,geom=loose,context='VERTS')
bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(data);bm.free();load.data=data;surfaces.apply(load,fresh)
for sign in (-1,1):
 for a in (-.22,.22):
  for z in (.12,.31):
   C('bucket side strap rivet',(sign*.331,a,z),.012,.017,bronze,'X',bucket,segments=8)
   C('bucket end strap rivet',(a,sign*.329,z),.012,.017,bronze,'Y',bucket,segments=8)
 C('handle attachment pin',(sign*.29,0,.31),.027,.065,bronze,'X',bucket,segments=12)
# A properly supported brick fire chamber, grate, ash pan and pressure-jacket seat.
spec=json.loads((P/'construction-receipt.json').read_text());EY=spec['engine_center'][1]
for o in list(root.children_recursive):
 if any(s in o.name for s in ('fuel firebox brick','firebox side brick','iron stoke door','stoke door latch')):erase(o)
B('refractory hearth slab',(1.10,EY,.90),(.46,.46,.04),brick)
for course in range(3):
 z=.93+course*.10
 for j in range(3):
  B('back wall individual fired brick',(.94+j*.16,EY+.20,z),(.156,.10,.096),brick)
 for side in (-1,1):
  for j in range(2):B('side wall fired brick',(1.10+side*.19,EY-.10+j*.20,z),(.10,.196,.096),brick)
 for side in (-1,1):
  if course<2:B('stoke opening jamb',(1.10+side*.15,EY-.20,z),(.10,.10,.096),brick)
# Voussoirs are separate real wedge-shaped masonry, surrounding a clear mouth.
for i in range(9):
 a0=i*math.pi/9+.012;a1=(i+1)*math.pi/9-.012
 points=[]
 for yy in (EY-.255,EY-.15):
  for r,a in ((.12,a0),(.18,a0),(.18,a1),(.12,a1)):points.append((1.10+r*math.cos(a),yy,.99+r*math.sin(a)))
 M('fitted arch voussoir',points,[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],brick,bevel=.0015)
B('load-bearing firebox cap',(1.10,EY,1.18),(.46,.46,.025),iron)
for y in np.linspace(EY-.12,EY+.12,5):C('supported fire grate bar',(1.1,float(y),.926),.009,.29,iron,'X',segments=12)
for i in range(7):
 bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1,radius=1);o=bpy.context.object
 for c in tuple(o.users_collection):c.objects.unlink(o)
 col.objects.link(o);o.parent=root;o.name='QUARRY V2 | fuel lump';o.scale=(.035,.025,.022);o.location=(1.02+(i%3)*.075,EY-.09+(i//3)*.08,.954);o.data.materials.append(coal);surfaces.physical_box_uv(o)
hinge=bpy.data.objects.new('QUARRY V2 | mounted open stoke door hinge',None);col.objects.link(hinge);hinge.parent=root;hinge.location=(.95,EY-.275,1.03);hinge.rotation_euler.z=math.radians(-32)
B('hinged riveted iron stoke door',(.15,0,0),(.30,.035,.21),iron,hinge)
for x in (.035,.265):
 for z in (-.075,.075):C('stoke door rivet',(x,-.024,z),.009,.015,bronze,'Y',hinge,segments=8)
B('door handle',(.245,-.044,0),(.055,.03,.018),bronze,hinge)
for z in (.96,1.10):
 C('door hinge pin',(.95,EY-.277,z),.014,.065,iron)
 B('door hinge strap',(.98,EY-.277,z),(.10,.025,.035),iron)
B('ash catch tray',(1.1,EY-.40,.898),(.39,.27,.026),iron)
for x in (.91,1.29):B('ash pan rim',(x,EY-.40,.922),(.018,.27,.04),iron)
B('ash pan front rim',(1.1,EY-.532,.922),(.39,.018,.04),iron)
for i in range(7):
 B('cooled ash and slag',(1.0+(i%4)*.055,EY-.45+(i//4)*.055,.922),(.025,.035,.015),soil,bevel=.003)
# Riveted pressure-vessel seams, crown, relief and readable mechanical gauge.
crown=bpy.data.objects['QUARRY | heat jacket crown'];erase(crown)
lathe('QUARRY V2 | dished copper pressure crown',[(0,1.555),(.08,1.553),(.145,1.540),(.19,1.515),(.205,1.505),(.205,1.490),(.18,1.490),(0,1.49)],(1.10,EY),copper,col,root,64)
torus('rolled jacket bottom seam',(1.1,EY,1.205),.192,.010,bronze)
torus('rolled jacket crown seam',(1.1,EY,1.50),.195,.008,bronze)
for k in range(8):
 a=k*math.tau/8;x=1.1+.203*math.cos(a);y=EY+.203*math.sin(a)
 C('pressure-jacket flange stud',(x,y,1.205),.009,.05,iron,segments=12)
 C('pressure-jacket flange nut',(x,y,1.233),.015,.013,bronze,segments=6)
C('relief valve stem',(1.1,EY,1.585),.015,.065,bronze)
C('relief valve seat',(1.1,EY,1.555),.028,.025,bronze)
beam('weighted relief lever',(1.03,EY,1.625),(1.20,EY,1.625),.016,iron)
C('relief lever weight',(1.205,EY,1.615),.021,.035,iron)
C('gauge receiving neck',(1.10,EY-.195,1.40),.025,.06,bronze,'Y')
C('gauge rim',(1.10,EY-.235,1.40),.058,.025,bronze,'Y')
paper=bpy.data.materials.new('QUARRY V2 | aged pressure dial');paper.use_nodes=True;shader=paper.node_tree.nodes.get('Principled BSDF');shader.inputs['Base Color'].default_value=(.62,.57,.43,1);shader.inputs['Roughness'].default_value=.83
C('pressure dial face',(1.10,EY-.250,1.40),.046,.006,paper,'Y')
for k in range(11):
 a=math.radians(30+k*24);x=1.1+.037*math.cos(a);z=1.4+.037*math.sin(a)
 tick=B('engraved pressure tick',(x,EY-.254,z),(.010,.002,.0025),iron,bevel=0);tick.rotation_euler.y=-a
needle=bpy.data.objects.new('QUARRY V2 | pressure needle pivot',None);col.objects.link(needle);needle.parent=root;needle.location=(1.10,EY-.258,1.40)
B('pressure needle',(.010,0,.011),(.041,.003,.004),iron,needle,bevel=0)
for f in range(1,194):
 needle.rotation_euler.y=.18*math.sin((f-1)*math.tau/192);needle.keyframe_insert(data_path='rotation_euler',frame=f)
# Bored cylinder, fitted gland, bolted caps and supported guide end blocks.
body=bpy.data.objects['QUARRY | pressure cylinder'];gland=bpy.data.objects['QUARRY | cylinder front gland']
for o,r in ((body,.056),(gland,.0225)):
 cutter=C('temporary cylinder bore',(.75,EY-.54,1.28),r,.40,iron,'Y');boolean(o,cutter,'DIFFERENCE');erase(cutter)
C('closed cylinder rear head',(.75,EY-.694,1.28),.080,.025,bronze,'Y')
for y in (EY-.694,EY-.386):
 for k in range(6):
  a=k*math.tau/6
  C('cylinder head six-flat bolt',(.75+.064*math.cos(a),y,1.28+.064*math.sin(a)),.010,.018,iron,'Y',segments=6)
for y in (EY-.42,EY-.12):
 B('crosshead guide pedestal',(.75,y,1.10),(.14,.05,.28),iron)
 block=B('bolted crosshead guide stop',(.75,y,1.26),(.16,.055,.05),bronze,bevel=0)
 for x in (.70,.80):
  cutter=C('temporary guide receiver bore',(x,y,1.26),.0135,.09,iron,'Y');boolean(block,cutter,'DIFFERENCE');erase(cutter)
 for x in (.70,.80):C('guide pedestal foot bolt',(x,y,.975),.012,.022,bronze,segments=6)
# Brick stock, lashed stone tools and supported output/rubble replace loose blockout props.
for o in list(root.children_recursive):
 if any(s in o.name for s in ('retaining brick stock','stone-tool handle','stone-tool head')):erase(o)
for layer in range(3):
 for j in range(2):B('bonded spare retaining brick',(-1.12+j*.19,1.29,1.19+layer*.105),(.182,.20,.10),brick)
def rough_rock(n,position,radii,material,support,parent=root,seed=0):
 bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1,radius=1)
 o=bpy.context.object
 for c in tuple(o.users_collection):c.objects.unlink(o)
 col.objects.link(o);o.name='QUARRY V2 | '+n;o.parent=parent
 for i,vtx in enumerate(o.data.vertices):
  p=vtx.co;factor=.91+.11*math.sin(i*2.31+seed);vtx.co=(p.x*radii[0]*factor,p.y*radii[1]*factor,p.z*radii[2]*factor)
 low=min(v.co.z for v in o.data.vertices);o.location=(position[0],position[1],support-low)
 o.data.materials.append(material);surfaces.physical_box_uv(o);return o
for x in (-.94,-.63):
 beam('laid stone-tool handle',(x,-.87,.445),(x,-.43,.478),.028)
 head=rough_rock('cleaved stone tool head',(x,-.42,0),(.085,.050,.048),fresh,.43,seed=x)
 for dx in (-.028,.028):
  torus('stone-tool hemp lashing',(x+dx,-.42,.478),.044,.0055,rope,axis='X')
# A shallow timber skid receives the split block; small chips accumulate at real ground height.
for x in (-.15,.0,.15):B('output skid plank',(x+.10,-.80,.445),(.14,.52,.03),wood)
block=bpy.data.objects['QUARRY | REUSED quarry_quarried_block_b']
for vtx in block.data.vertices:
 vtx.co.x+=.0;vtx.co.z+=.03
surfaces.apply(block,fresh)
for i,(x,y,support) in enumerate([(-1.30,-.38,.32),(-.74,-1.32,.32),(.49,-1.12,.43),(-.87,.67,.32),(-.56,.65,.32),(.56,.61,.32),(-1.2,-.92,.43)]):
 rough_rock('quarry chips',(x,y,0),(.04+.01*(i%3),.05,.027+.008*(i%2)),fresh,support,seed=i)
# Apply finishes without changing the retained animation transforms.
repairs={}
for o in root.children_recursive:
 if o.type!='MESH':continue
 if o.modifiers:
  ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());data=bpy.data.meshes.new_from_object(ev);o.modifiers.clear();o.data=data
 if not o.data.uv_layers:surfaces.physical_box_uv(o)
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.triangulate(bm,faces=list(bm.faces));bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-7);bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=1e-7);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free()
 o.data.calc_loop_triangles();bad={t.polygon_index for t in o.data.loop_triangles if t.area<1e-12}
 if bad:
  bm=bmesh.new();bm.from_mesh(o.data);bm.faces.ensure_lookup_table();bmesh.ops.delete(bm,geom=[bm.faces[i] for i in bad],context='FACES');bm.to_mesh(o.data);bm.free();repairs[o.name]=len(bad)
 if o.animation_data:
  for layer in o.animation_data.action.layers:
   for strip in layer.strips:
    for bag in strip.channelbags:
     for curve in bag.fcurves:
      for key in curve.keyframe_points:key.interpolation='LINEAR'
profile=json.loads((P/'capture-profile.json').read_text());scene.frame_set(1);assert_clean(scene,profile,bpy);bpy.ops.file.pack_all()
target=O/'quarry-v2.blend';bpy.ops.wm.save_as_mainfile(filepath=str(target),compress=True)
bpy.ops.wm.open_mainfile(filepath=str(target));scene=bpy.context.scene;root=bpy.data.objects['EXPORT | Quarry all authored parts']
bpy.ops.object.select_all(action='DESELECT')
for o in [root,*root.children_recursive]:o.select_set(True)
bpy.ops.export_scene.gltf(filepath=str(O/'quarry-v2.glb'),export_format='GLB',use_selection=True,export_cameras=False,export_lights=False,export_animations=True,export_animation_mode='SCENE',export_anim_scene_split_object=False,export_frame_range=True,export_force_sampling=True,export_frame_step=1,export_apply=True,export_extras=True)
(O/'capture-profile.json').write_text(json.dumps(profile,indent=2)+'\n')
(O/'refinement-receipt.json').write_text(json.dumps({'parent_sha256':sha(source),'source_sha256':sha(target),'runtime_sha256':sha(O/'quarry-v2.glb'),'owner_request':'Complex quarry requires detail; V1 held as ultra rough','mechanism_retained':True,'details':['Connected hewn bedrock and stepped benches with actual wedge kerfs','Irregular chipped floor, mineral fractures and seated splitting wedges','Split bored bearing blocks, bronze bushes, studs, washers and nuts','Bolted timber cheek straps, heel anchors and diagonal bracing','Spindle bores, laid rope coil and fixed cable guide','Cleaved cargo, bucket strap rivets and handle pins','Individual brick courses and fitted arch, grate, ash pan and mounted door','Seated riveted heat jacket, dished crown, relief and mechanical gauge','Bored drive cylinder, sealed heads, guide stops and their supports','Bonded brick stock, lashed laid tools and receiving skid'],'zero_area_repairs':repairs,'visual_approved':False,'native_integrated':False},indent=2)+'\n')
projection=bpy.data.objects.new('SPRITE ONLY | quarry square ground grid',None);scene.collection.objects.link(projection);projection.scale.y=math.sqrt(2);root.parent=projection
# Review images are larger inspection output; the saved production camera stays unchanged.
scene.cycles.samples=48;scene.render.resolution_x=scene.render.resolution_y=512
for name,yaw in [('front',0),('east',270),('rear',180),('west',90)]:
 root.rotation_euler.z=math.radians(yaw);scene.frame_set(49);scene.render.filepath=str(O/(name+'-review512.png'));bpy.ops.render.render(write_still=True)
print('QUARRY_DETAILED_SOURCE_SAVED',target,flush=True)
