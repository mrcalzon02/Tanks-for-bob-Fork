"""Owner-requested visible machinery, connected process circuits and supported masonry flue."""
import bpy,bmesh,json,math,hashlib,sys,tempfile
import numpy as np
from pathlib import Path
from mathutils import Vector
H=Path(__file__).resolve().parent;R=H.parents[3];P=R/'models/island-survival/shaler/candidates/v1-production04';O=P.parent/'v2-mechanisms02'
if O.exists():raise FileExistsError(O)
O.mkdir(parents=True);tempfile.tempdir=str(R/'build/quarry-export-temp')
sys.path.insert(0,str(R/'models/island-survival/primitive-steam-powered-pump/v3'))
from mesh_util import mesh,box,cylinder,tube,lathe
import surfaces
sys.path.insert(0,str(R.parent/'model-production/tools/fmpl'))
from blender_camera_guard import install_canonical_camera,assert_clean,temporary_inspection_camera
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
source=P/'shaler-v1.blend';assert sha(source)==json.loads((P/'construction-receipt.json').read_text())['source_sha256']
bpy.ops.wm.open_mainfile(filepath=str(source));scene=bpy.context.scene;scene.frame_set(1);root=bpy.data.objects['EXPORT | Shaler all authored parts']
col=bpy.data.collections.new('SHALER V2 | exposed transmission process pump and grounded flue');scene.collection.children.link(col)
def mat(s):return next(m for m in bpy.data.materials if m.name.endswith(' | '+s))
m={k:mat(v) for k,v in {'wood':'long-grain-oak','endgrain':'cut-oak-growth-rings','iron':'cast-iron-housing','bronze':'worn-bronze-fittings','copper':'aged-copper-jacket','brick':'fired-clay-lining','stone':'shaler-worked-sandstone','clay':'shaler-salt-glazed-stoneware','belt':'shaler-hemp-drive-belt'}.items()}
rng=np.random.default_rng(171143);u,v=np.meshgrid(np.linspace(0,1,512),np.linspace(0,1,512));noise=surfaces.field(rng,(512,512),.05);weave=.012*np.sin(u*360+v*40)*np.sin(v*340-u*30)
m['lagging']=surfaces.material('shaler-hand-wound-hemp-hose-lagging',np.stack([.135+weave+.008*noise,.095+weave+.006*noise,.055+weave+.004*noise],axis=-1),.90+.02*noise,.5+weave+.02*noise,0,O);m['lagging']['surface_authorship']='Hemp-lagged annealed copper flexure loops, with close-wound reinforcing wire and rigid end unions'
def B(n,p,d,material,parent=root,bevel=.006):
 o=box('SHALER V2 | '+n,p,d,material,col,parent,bevel);surfaces.apply(o,material,m['endgrain'] if material==m['wood'] else None);return o
def C(n,p,r,d,material,axis='Z',parent=root,segments=40):
 o=cylinder('SHALER V2 | '+n,p,r,d,material,col,parent,axis,segments);surfaces.apply(o,material);return o
def E(n,p=(0,0,0),parent=root):
 o=bpy.data.objects.new('SHALER V2 | '+n,None);col.objects.link(o);o.parent=parent;o.location=p;return o
def beam(n,a,b,w,material=m['wood'],parent=root):
 a,b=Vector(a),Vector(b);o=B(n,(a+b)/2,(w,w,(b-a).length),material,parent);o.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler();return o
def bore(obj,cutter):
 bpy.context.view_layer.update();bpy.context.view_layer.objects.active=obj;mod=obj.modifiers.new('Actual fitted bore','BOOLEAN');mod.operation='DIFFERENCE';mod.object=cutter;mod.solver='EXACT';bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cutter,do_unlink=True)
def ring(n,p,outer,inner,depth,material,axis='Z',parent=root):
 tangent={'X':Vector((1,0,0)),'Y':Vector((0,1,0)),'Z':Vector((0,0,1))}[axis];p=Vector(p)
 o=tube('SHALER V2 | '+n,[(-tangent*depth/2,tangent,outer,inner),(tangent*depth/2,tangent,outer,inner)],material,col,parent,40);o.location=p;return o
def bolt(n,p,axis='Z',parent=root):return C(n,p,.019,.032,m['bronze'],axis,parent,6)
# The formerly hanging brick chimney now bears continuously on a broad worked footing.
B('chimney continuous foundation',(-1.02,.76,.146),(.53,.54,.14),m['stone'],bevel=.018)
foundation=[]
for course in range(4):
 z=.18+course*.12
 for dx,dy,wx,wy in [(-.13,0,.10,.36),(.13,0,.10,.36),(0,-.13,.16,.10),(0,.13,.16,.10)]:
  block=B('chimney lower bonded course',(-1.02+dx,.76+dy,z),(wx,wy,.114),m['brick']);foundation.append(block.name)
  if dx>0:bore(block,C('temporary firebox flue entry',(-.90,.76,.39),.093,.38,m['iron'],'X'))
# Bonded corbels tie the stack into the hearth while leaving its combustion passage open.
for z,x,width in ((.24,-.77,.30),(.36,-.78,.28),(.48,-.81,.22)):
 for y in (.52,.98):B('bonded hearth flue corbel',(x,y,z),(width,.12,.114),m['brick'])
# A keyed rotating shaft extends the existing upper drive to a new visible gear train.
old=bpy.data.objects.get('SHALER | fixed cam axle')
if old:bpy.data.objects.remove(old,do_unlink=True)
shaft=E('keyed main transmission shaft',(.08,-.65,1.85));C('continuous turning shaft',(0,0,0),.030,2.64,m['iron'],'X',shaft)
for x in (-1.25,):
 post=B('transmission pier',(x,-.65,1.01),(.16,.21,1.86),m['wood']);bore(post,C('temporary transmission pier bore',(x,-.65,1.85),.038,.30,m['iron'],'X'))
 B('transmission pier shoe',(x,-.65,.12),(.27,.29,.08),m['iron']);ring('transmission pier bronze bush',(x,-.65,1.85),.066,.034,.23,m['bronze'],'X')
 for y in (-.75,-.55):bolt('transmission pier anchor',(x,y,.175))
 beam('transmission pier forward brace',(x,-.65,1.10),(-1.25,-1.19,.10),.09)
for x in (-1.07,-.45,.25,1.18):
 ring('keyed shaft collar',(x-.08,0,0),.048,.029,.045,m['bronze'],'X',shaft);B('shaft collar visible key',(x-.08,0,.049),(.045,.024,.018),m['iron'],shaft)
# Front timber gantry supports both gear shafts and the new wet-process pump.
for x in (-.70,.15):
 B('front gear gantry leg',(x,-.25,1.01),(.16,.17,1.86),m['wood']);B('front gantry foot',(x,-.25,.12),(.25,.27,.08),m['iron'])
 for y in (-.34,-.16):bolt('gantry heel anchor',(x,y,.175))
 beam('gantry rear thrust stay',(x,-.25,1.45),(x,-.84,.09),.085)
header=B('front gear bearing beam',(-.38,-.25,1.85),(1.17,.18,.18),m['wood'])
for x in (-.78,-.30):
 bore(header,C('temporary front gear shaft bore',(x,-.25,1.85),.037,.35,m['iron'],'Y'))
 ring('front gear shaft bronze bush',(x,-.25,1.85),.068,.033,.20,m['bronze'],'Y')
for x in (-.70,.15):
 B('gantry iron joint strap',(x,-.355,1.85),(.14,.027,.25),m['iron'])
 for z in (1.76,1.94):bolt('gantry cheek fastener',(x,-.384,z),'Y')
# Equal miter gears turn the horizontal press shaft into a forward-facing gear drive.
I=Vector((-.78,-.65,1.85));miter_x=E('driving miter gear',I);miter_y=E('driven miter gear',I)
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
 o=mesh('SHALER V2 | '+n,points,faces,m['bronze'],col,parent);o.rotation_euler.y=math.pi/2 if axis=='X' else 0;o.rotation_euler.x=-math.pi/2 if axis=='Y' else 0;surfaces.apply(o,m['bronze']);return o
conical_teeth('18 tooth driving bevel',miter_x,'X');conical_teeth('18 tooth driven bevel',miter_y,'Y')
C('forward gear input shaft',(0,.02,0),.030,.98,m['iron'],'Y',miter_y)
# Two open-faced cog wheels: 18:54 teeth means the large crank closes once per loop.
small=E('18 tooth front pinion',(-.78,-1.02,1.85));large=E('54 tooth process crank gear',(-.30,-1.02,1.85))
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
 o=mesh('SHALER V2 | '+n,verts,faces,material,col,parent);surfaces.apply(o,material);return o
spur('iron pinion teeth',small,.12,18,.052,m['iron']);spur('hardwood process gear teeth',large,.36,54,.225,m['wood'])
for actor,r,count in ((small,.12,3),(large,.36,6)):
 C('gear keyed central hub',(0,0,0),.065,.12,m['bronze'],'Y',actor)
 for i in range(count):
  a=math.tau*i/count;beam('gear radial spoke',(.042*math.cos(a),0,.042*math.sin(a)),((r-.035)*math.cos(a),0,(r-.035)*math.sin(a)),.040,m['wood'] if actor==large else m['iron'],actor)
  if actor==large:
   beam('gear spoke iron facing',(.065*math.cos(a),-.028,.065*math.sin(a)),(.30*math.cos(a),-.028,.30*math.sin(a)),.018,m['iron'],actor)
C('process gear supported axle',(0,.38,0),.030,.90,m['iron'],'Y',large)
crank=C('process gear retained crank pin',(.11,-.14,0),.022,.22,m['bronze'],'Y',large)
# A second visible piston/arm operates a genuine internal recirculation circuit.
for z in (.54,.95,1.52):
 B('pump guide front crossmember',(-.34,-1.16,z),(1.12,.070,.065),m['wood'])
 for x in (-.70,.15):B('pump guide cantilever bracket',(x,-.705,z),(.10,1.05,.07),m['iron'])
for x in (-.70,.15):
 beam('pump cantilever lower brace',(x,-.25,.20),(x-.06 if x<0 else x,-1.16,.54),.055,m['iron'])
 beam('pump cantilever upper brace',(x,-.25,1.72),(x,-1.16,1.52),.045,m['iron'])
for x in (-.42,-.18):C('vertical pump crosshead guide',(x,-1.16,1.235),.013,.57,m['iron'])
crosshead=E('guided process pump crosshead',(-.30,-1.16,1.33));shoe=B('bored pump crosshead',(0,0,0),(.30,.09,.10),m['bronze'],crosshead)
for x in (-.12,.12):bore(shoe,C('temporary process pump guide bore',(x,0,0),.018,.20,m['iron'],parent=crosshead))
piston=C('process pump rigid piston',(-.30,-1.16,1.07),.023,.52,m['iron'])
rod=C('process pump rigid connecting arm',(-.30,-1.16,1.59),.017,.52,m['iron'])
ring('wet process pump cylinder',(-.30,-1.16,.80),.112,.061,.44,m['copper'])
ring('wet pump packed gland',(-.30,-1.16,1.028),.13,.027,.06,m['bronze'])
C('wet pump sealed foot',(-.30,-1.16,.572),.13,.03,m['bronze'])
B('wet pump load saddle',(-.30,-1.16,.568),(.30,.16,.035),m['iron'])
for x in (-.39,-.21):bolt('wet cylinder foot fixing',(x,-1.16,.596))
# Rounded, supported circuits use only the real two exterior sockets; all branches are internal.
def smooth_path(controls,steps=8):
 pts=[Vector(p) for p in controls];samples=[]
 for i in range(len(pts)-1):
  p0=pts[max(0,i-1)];p1=pts[i];p2=pts[i+1];p3=pts[min(len(pts)-1,i+2)]
  for k in range(steps):
   t=k/steps;p=.5*((2*p1)+(-p0+p2)*t+(2*p0-5*p1+4*p2-p3)*t*t+(-p0+3*p1-3*p2+p3)*t*t*t);samples.append(p)
 samples.append(pts[-1]);return samples
def circuit(n,points,outer=.035,inner=.023,material=m['copper'],wrapped=False):
 pts=smooth_path(points);samples=[]
 for i,p in enumerate(pts):samples.append((p,(pts[min(i+1,len(pts)-1)]-pts[max(0,i-1)]).normalized(),outer,inner))
 o=tube('SHALER V2 | '+n,samples,material,col,root,24)
 for endpoint in (0,-1):
  p,tangent,_,_=samples[endpoint];f=ring(n+' compression union',p,outer+.020,inner,.06,m['bronze']);f.rotation_euler=Vector(tangent).to_track_quat('Z','Y').to_euler()
 if wrapped:
  spiral=[]
  for i,(p,tangent,_,_) in enumerate(samples):
   side=tangent.cross(Vector((0,0,1)))
   if side.length<.1:side=tangent.cross(Vector((1,0,0)))
   side.normalize();other=tangent.cross(side).normalized();angle=i*math.tau*.70
   q=p+(outer+.004)*(side*math.cos(angle)+other*math.sin(angle));spiral.append(q)
  wire=[(p,(spiral[min(i+1,len(spiral)-1)]-spiral[max(0,i-1)]).normalized(),.0035,.001) for i,p in enumerate(spiral)]
  tube('SHALER V2 | '+n+' hand wound retaining wire',wire,m['iron'],col,root,8)
 return o
circuit('retort slurry suction',[(-.55,0,.85),(-.82,.04,.85),(-.96,-.15,.85),(-.99,-.55,.80),(-.89,-.92,.71),(-.48,-1.16,.71),(-.41,-1.16,.71)],.041,.027,m['clay'])
circuit('looped process return hose',[(-.19,-1.16,.92),(.06,-1.20,1.01),(.30,-1.18,1.20),(.34,-.85,1.38),(.28,-.52,1.45),(-.05,-.28,1.44),(-.18,-.19,1.40)],.035,.023,m['lagging'],True)
circuit('steam distribution riser',[(.32,.68,1.03),(.43,.73,1.20),(.42,.57,1.34),(.36,.50,1.35)],.029,.018)
circuit('insulated engine pressure loop',[(.36,.50,1.35),(.64,.80,1.55),(1.00,.98,1.45),(1.13,1.04,1.05),(1.12,1.03,.737)],.029,.017,m['lagging'],True)
circuit('engine return loop',[(1.12,.85,.65),(.99,.74,.61),(.74,.73,.69),(.59,.67,.85),(.34,.55,.82)],.027,.016)
# Pipe cleats anchor long runs to the actual timber or masonry surfaces.
for post_x,pipe_x,y,pipe_z in [(-1.10,-.99,-.55,.80),(-1.08,-.89,-.92,.71)]:
 top=pipe_z-.041-.025
 B('pipe supporting timber post',(post_x,y,(.076+top)/2),(.08,.10,top-.076),m['wood'])
 B('pipe post anchored shoe',(post_x,y,.105),(.16,.18,.058),m['iron'])
 B('pipe bearing cantilever cleat',((post_x+pipe_x)/2,y,pipe_z-.041-.0125),(abs(post_x-pipe_x)+.10,.12,.025),m['wood'])
 ring('split slurry pipe saddle',(pipe_x,y,pipe_z),.056,.041,.04,m['iron'],'Y')
beam('riser bracket from retort hoop',(.30,.65,1.04),(.43,.73,1.20),.025,m['iron'])
clamp=ring('riser fixed retaining clamp',(.43,.73,1.20),.046,.029,.04,m['iron']);clamp.rotation_euler=Vector((.10,-.11,.31)).to_track_quat('Z','Y').to_euler()
# Weighted relief arm and an analogue pressure dial explain the pressure circuit.
C('relief valve body',(.36,.50,1.45),.045,.16,m['bronze']);beam('weighted relief arm',(.36,.50,1.54),(.58,.50,1.57),.025,m['iron']);C('relief counterweight',(.58,.50,1.57),.046,.045,m['iron'],'Y')
C('pressure dial impulse neck',(.36,.46,1.46),.024,.095,m['bronze'],'Y')
C('pressure dial brass bezel',(.36,.42,1.46),.072,.035,m['bronze'],'Y');C('pressure dial pale face',(.36,.399,1.46),.061,.009,m['stone'],'Y')
beam('pressure dial needle',(.36,.392,1.46),(.389,.392,1.49),.006,m['iron'])
# Synchronised drive: 1:1 miter pair, then 18:54 spur pair; one large-crank turn per loop.
for frame in range(1,194):
 phase=math.tau*(frame-1)/192;theta=phase*3;alpha=-theta;phi=theta/3+math.pi/54
 shaft.rotation_euler.x=theta;miter_x.rotation_euler.x=theta;miter_y.rotation_euler.y=alpha;small.rotation_euler.y=alpha;large.rotation_euler.y=phi
 pin=Vector((-.30+.11*math.cos(phi),-1.16,1.85-.11*math.sin(phi)));slide=Vector((-.30,-1.16,pin.z-math.sqrt(.52**2-(pin.x+.30)**2)))
 crosshead.location=slide;piston.location=slide-Vector((0,0,.26));rod.location=(pin+slide)/2;rod.rotation_euler=(pin-slide).to_track_quat('Z','Y').to_euler()
 for actor in (shaft,miter_x,miter_y,small,large):actor.keyframe_insert(data_path='rotation_euler',frame=frame)
 for actor in (crosshead,piston,rod):actor.keyframe_insert(data_path='location',frame=frame)
 rod.keyframe_insert(data_path='rotation_euler',frame=frame)
# Freeze only new geometry; leave existing accepted kinematic relationships intact.
repairs={}
for obj in col.objects:
 if obj.type!='MESH':continue
 if obj.modifiers:
  data=bpy.data.meshes.new_from_object(obj.evaluated_get(bpy.context.evaluated_depsgraph_get()));obj.modifiers.clear();obj.data=data
 if not obj.data.uv_layers:surfaces.physical_box_uv(obj)
 bm=bmesh.new();bm.from_mesh(obj.data);bmesh.ops.triangulate(bm,faces=list(bm.faces));bmesh.ops.delete(bm,geom=[v for v in bm.verts if not v.link_faces],context='VERTS');bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-7);bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=1e-7);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(obj.data);bm.free()
 obj.data.calc_loop_triangles();bad={t.polygon_index for t in obj.data.loop_triangles if t.area<1e-12}
 if bad:
  bm=bmesh.new();bm.from_mesh(obj.data);bm.faces.ensure_lookup_table();bmesh.ops.delete(bm,geom=[bm.faces[i] for i in bad],context='FACES');bm.to_mesh(obj.data);bm.free();repairs[obj.name]=len(bad)
for obj in col.objects:
 if not obj.animation_data:continue
 for layer in obj.animation_data.action.layers:
  for strip in layer.strips:
   for bag in strip.channelbags:
    for curve in bag.fcurves:
     for key in curve.keyframe_points:key.interpolation='LINEAR'
profile=json.loads((P/'capture-profile.json').read_text());install_canonical_camera(scene,profile,bpy);scene.frame_set(1);assert_clean(scene,profile,bpy);bpy.ops.file.pack_all()
native=O/'shaler-v2.blend';bpy.ops.wm.save_as_mainfile(filepath=str(native),compress=True);bpy.ops.wm.open_mainfile(filepath=str(native));scene=bpy.context.scene;root=bpy.data.objects['EXPORT | Shaler all authored parts']
bpy.ops.object.select_all(action='DESELECT')
for obj in [root,*root.children_recursive]:obj.select_set(True)
bpy.ops.export_scene.gltf(filepath=str(O/'shaler-v2.glb'),export_format='GLB',use_selection=True,export_cameras=False,export_lights=False,export_animations=True,export_animation_mode='SCENE',export_anim_scene_split_object=False,export_frame_range=True,export_force_sampling=True,export_frame_step=1,export_apply=True,export_extras=True)
(O/'capture-profile.json').write_text(json.dumps(profile,indent=2)+'\n');(O/'refinement-receipt.json').write_text(json.dumps(dict(parent_source_sha256=sha(source),source_sha256=sha(native),runtime_sha256=sha(O/'shaler-v2.glb'),owner_feedback=['Good rough structure; needs much more pipes, hoses, gears and working piston arms','Brick chimney needs visible support to ground'],chimney_foundation_courses=foundation,gear_teeth=[18,18,18,54],additional_piston_rod_length=.52,exterior_fluid_sockets_unchanged=True,owner_visual_approved=False,native_integrated=False,degenerate_repairs=repairs),indent=2)+'\n')
projection=bpy.data.objects.new('SPRITE ONLY | square ground grid',None);scene.collection.objects.link(projection);projection.scale.y=math.sqrt(2);root.parent=projection;scene.render.resolution_x=scene.render.resolution_y=512
for name,yaw in [('front',0),('east',270),('rear',180),('west',90)]:
 root.rotation_euler.z=math.radians(yaw);scene.frame_set(49);scene.render.filepath=str(O/(name+'-review512.png'));bpy.ops.render.render(write_still=True)
root.rotation_euler.z=0
with temporary_inspection_camera(scene,bpy,'Shaler V2 foundation and gear drive') as camera:
 camera.data.type='ORTHO';camera.data.ortho_scale=3.3;camera.location=(-3,-5,3);camera.rotation_euler=(Vector((-.48,-.40,1.1))-camera.location).to_track_quat('-Z','Y').to_euler();scene.camera=camera;scene.render.filepath=str(O/'machinery-close512.png');bpy.ops.render.render(write_still=True)
print('SHALER_V2_MECHANISMS_SOURCE',native,flush=True)
