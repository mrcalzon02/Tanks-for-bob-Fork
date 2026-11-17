"""Recipe-specific scum/sediment separator, wet preform die and properly fitted process plumbing."""
import bpy,bmesh,json,math,hashlib,sys,tempfile
import numpy as np
from pathlib import Path
from mathutils import Vector
H=Path(__file__).resolve().parent;R=H.parents[3];P=R/'models/island-survival/calcifier/candidates/v1-production03';O=P.parent/'v2-stations02'
if O.exists():raise FileExistsError(O)
O.mkdir(parents=True);tempfile.tempdir=str(R/'build/quarry-export-temp')
sys.path.insert(0,str(R/'models/island-survival/primitive-steam-powered-pump/v3'))
from mesh_util import mesh,box,cylinder,tube
import surfaces
sys.path.insert(0,str(R.parent/'model-production/tools/fmpl'))
from blender_camera_guard import install_canonical_camera,assert_clean,temporary_inspection_camera
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
source=P/'calcifier-v1.blend';assert sha(source)==json.loads((P/'construction-receipt.json').read_text())['source_sha256']
bpy.ops.wm.open_mainfile(filepath=str(source));scene=bpy.context.scene;scene.frame_set(1);root=bpy.data.objects['EXPORT | Calcifier all authored parts'];col=bpy.data.collections.new('CALCIFIER V2 | separation forming and fitted circuits');scene.collection.children.link(col)
mat=lambda s:next(m for m in bpy.data.materials if m.name.endswith(' | '+s))
m={k:mat(v) for k,v in {'wood':'long-grain-oak','endgrain':'cut-oak-growth-rings','iron':'cast-iron-housing','bronze':'worn-bronze-fittings','copper':'aged-copper-jacket','clay':'calcifier-refractory-liner','mineral':'calcifier-chalky-crystal-growth','stone':'calcifier-worked-stone','hose':'calcifier-reinforced-lagging'}.items()}
rng=np.random.default_rng(171163);coarse=surfaces.field(rng,(512,512),.04);fine=surfaces.field(rng,(512,512),.22)
m['die']=surfaces.material('calcifier-porous-bioceramic-die',np.stack([.42+.017*coarse,.40+.015*coarse,.31+.012*coarse],axis=-1),.76+.03*fine,.5+.027*coarse+.01*fine,0,O);m['die']['surface_authorship']='Porous fired forming die for the actual hydrocoptic precursor/bioceramic preform/water recipe; two physical cavities and attached wet conditioning circuit'
def B(n,p,d,material,parent=root):
 o=box('CALCIFIER V2 | '+n,p,d,material,col,parent);surfaces.apply(o,material,m['endgrain'] if material==m['wood'] else None);return o
def C(n,p,r,d,material,axis='Z',parent=root,segments=40):
 o=cylinder('CALCIFIER V2 | '+n,p,r,d,material,col,parent,axis,segments);surfaces.apply(o,material);return o
def E(n,p=(0,0,0),parent=root):
 o=bpy.data.objects.new('CALCIFIER V2 | '+n,None);col.objects.link(o);o.parent=parent;o.location=p;return o
def ring(n,p,outer,inner,depth,material,axis='Z',parent=root):
 t=Vector({'X':(1,0,0),'Y':(0,1,0),'Z':(0,0,1)}[axis]);o=tube('CALCIFIER V2 | '+n,[(-t*depth/2,t,outer,inner),(t*depth/2,t,outer,inner)],material,col,parent,40);o.location=p;return o
def beam(n,a,b,w,material=m['iron'],parent=root):
 a,b=Vector(a),Vector(b);o=B(n,(a+b)/2,(w,w,(b-a).length),material,parent);o.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler();return o
def bore(obj,cutter):
 bpy.context.view_layer.update();bpy.context.view_layer.objects.active=obj;mod=obj.modifiers.new('True fitted process opening','BOOLEAN');mod.object=cutter;mod.operation='DIFFERENCE';mod.solver='EXACT';bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cutter,do_unlink=True)
def bolt(n,p,axis='Z',parent=root):return C(n,p,.016,.032,m['bronze'],axis,parent,6)
def ball(n,p,parent):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=16,ring_count=8,radius=.026);o=bpy.context.object
 for collection in tuple(o.users_collection):collection.objects.unlink(o)
 col.objects.link(o);o.name='CALCIFIER V2 | '+n;o.parent=parent;o.location=p;surfaces.apply(o,m['bronze']);return o
# The original draining rack becomes a guided, actuated separation/sieving chest.
sieve=E('guided scum sediment sieve carriage',(-.66,-1.03,.43));bpy.context.view_layer.update()
for obj in tuple(root.children_recursive):
 if obj.name.startswith('CALCIFIER | draining rack slat') or obj.name.startswith('CALCIFIER | mineral growth product'):
  if 'slat' in obj.name:
   for vertex in obj.data.vertices:vertex.co.x*=.42/.48
  old=obj.matrix_world.copy();obj.parent=sieve;obj.matrix_parent_inverse.identity();obj.matrix_basis=sieve.matrix_world.inverted()@old
for x in (-.84,-.48):
 for y in (-1.22,-.82):
  block=B('sieve guide bearing block',(x,y,.26),(.06,.09,.07),m['bronze']);bore(block,C('temporary sieve guide bore',(x,y,.26),.015,.18,m['iron'],'Y'))
 C('sieve sliding guide rod',(x+.66,0,-.17),.011,.62,m['iron'],'Y',sieve)
for x in (-.20,.20):B('sieve moving edge',(x,0,-.11),(.035,.50,.055),m['wood'],sieve)
for i in range(11):B('graded sieve wire',(-.185+i*.037,0,-.105),(.007,.46,.012),m['iron'],sieve)
for y in (-1.26,-.80):B('settling chest low end wall',(-.66,y,.17),(.48,.035,.10),m['wood'])
for x in (-.90,-.42):B('settling chest low side wall',(x,-1.03,.17),(.035,.48,.10),m['wood'])
B('settling sump floor',(-.66,-1.03,.1225),(.48,.48,.025),m['clay'])
# Small eccentric and ball-ended rigid arm let the long spatial link drive the sieve.
upper=bpy.data.objects['CALCIFIER | engine crank flywheel']
eccentric=C('sieve retained eccentric',(.004,-.31,0),.020,.66,m['bronze'],'Y',upper)
C('extended eccentric support boss',(.004,-.16,0),.035,.28,m['bronze'],'Y',upper)
LR=math.sqrt(1.66**2+.62**2+.17**2)
sieve_rod=C('rigid sieve drive arm',(0,0,0),.015,LR,m['iron'])
for z in (-LR/2,LR/2):ball('sieve drive universal ball end',(0,0,z),sieve_rod)
ring('sieve crosshead socket',(0,0,0),.046,.020,.045,m['bronze'],'X',sieve)
# The actual hydrocoptic recipe has a precursor and bioceramic preform: give it a wet die.
for x in (.10,.50):
 B('forming station upright',(x,-.80,.66),(.055,.075,1.176),m['wood']);B('forming upright shoe',(x,-.80,.12),(.14,.16,.09),m['iron'])
 for y in (-.84,-.76):bolt('forming foot anchor',(x,y,.18))
 beam('forming bed support',(x,-.80,.25),(x,-1.20,.33),.045)
B('wet forming chest base',(.29,-1.04,.30),(.40,.36,.06),m['wood'])
for x in (.105,.475):B('forming chest side',(x,-1.04,.39),(.035,.36,.18),m['wood'])
for y in (-1.205,-.875):B('forming chest end',(.29,y,.39),(.37,.03,.18),m['wood'])
die=B('two cavity bioceramic forming die',(.29,-1.04,.48),(.30,.26,.16),m['die'])
for x in (.23,.35):bore(die,C('temporary real forming cavity',(x,-1.04,.48),.045,.24,m['iron']))
header=B('forming piston guide beam',(.29,-.91,1.15),(.54,.35,.10),m['wood']);bore(header,C('temporary forming guide bore',(.29,-1.04,1.15),.035,.25,m['iron']))
ring('forming ram packed bronze guide',(.29,-1.04,1.15),.054,.030,.12,m['bronze'])
for x in (.10,.50):
 B('forming guide cheek strap',(x,-.91,1.205),(.09,.24,.018),m['iron'])
 for y in (-1.00,-.82):bolt('forming guide fixing',(x,y,1.23))
engine_slide=bpy.data.objects['CALCIFIER | guided engine crosshead']
forming=E('forming ram coupled to engine',(-.71,-.405,0),engine_slide)
beam('rigid forming crosshead extension',(0,0,0),(-.71,-.405,0),.035,m['iron'],engine_slide)
for p in ((0,0,0),(-.71,-.405,0)):C('forming linkage retained pin',p,.022,.10,m['bronze'],'Z',engine_slide)
B('forming pressure platen',(0,0,-.10),(.32,.28,.04),m['iron'],forming)
C('forming guided piston shaft',(0,0,.20),.026,.70,m['iron'],parent=forming)
for x in (-.06,.06):C('forming die punch',(x,0,-.20),.038,.20,m['bronze'],parent=forming)
# Preforms enter between the columns and are conditioned by the fitted water/steam circuit.
B('bioceramic preform feed box',(.29,-.68,.33),(.24,.19,.18),m['wood'])
B('preform transfer lip',(.29,-.82,.42),(.22,.20,.045),m['bronze'])
for x in (.23,.35):C('visible bioceramic preform',(x,-.68,.445),.039,.05,m['mineral'])
def circuit(n,points,outer=.035,inner=.023,material=m['copper']):
 controls=[Vector(p) for p in points];pts=[]
 for i in range(len(controls)-1):
  p0,p1,p2,p3=controls[max(0,i-1)],controls[i],controls[i+1],controls[min(len(controls)-1,i+2)]
  for k in range(10):
   t=k/10;pts.append(.5*(2*p1+(-p0+p2)*t+(2*p0-5*p1+4*p2-p3)*t*t+(-p0+3*p1-3*p2+p3)*t*t*t))
 pts.append(controls[-1]);samples=[(p,(pts[min(i+1,len(pts)-1)]-pts[max(0,i-1)]).normalized(),outer,inner) for i,p in enumerate(pts)]
 o=tube('CALCIFIER V2 | '+n,samples,material,col,root,32)
 for index in (0,-1):
  p,t,_,_=samples[index];f=ring(n+' end union',p,outer+.018,inner,.05,m['bronze']);f.rotation_euler=t.to_track_quat('Z','Y').to_euler()
 return o

# A machined multiport chest makes the existing common inlet branches understandable.
node=Vector((.28,.43,1.14));chest=B('water steam distribution valve chest',node,(.22,.20,.20),m['bronze'])
for tangent,radius in ((Vector((-.06,-.09,.26)),.052),(Vector((-.20,.15,.13)),.014),(Vector((.22,.12,.18)),.020),(Vector((.15,-.25,-.06)),.017)):
 tangent.normalize();cut=C('temporary manifold channel',node,radius,.48,m['iron']);cut.rotation_euler=tangent.to_track_quat('Z','Y').to_euler();bore(chest,cut)
B('bolted valve chest cover',(.28,.319,1.14),(.20,.022,.18),m['iron'])
for x in (.215,.345):
 for z in (1.085,1.195):bolt('valve cover retained stud',(x,.30,z),'Y')
ring('distribution valve packed gland',(.28,.43,1.25),.036,.018,.05,m['bronze'])
C('distribution valve spindle',(.28,.43,1.30),.015,.16,m['iron']);B('distribution hand lever',(.28,.43,1.385),(.16,.028,.025),m['wood'])
circuit('wet die conditioning feed',[(.28,.43,1.14),(.43,.18,1.08),(.36,-.20,1.01),(.06,-.55,.94),(-.04,-.80,.74),(-.02,-1.02,.50),(.09,-1.04,.46)],.026,.016,m['copper'])
circuit('settling sump internal return',[(-.66,-.94,.17),(-.96,-.94,.17),(-1.08,-.72,.26),(-1.10,-.40,.52),(-1.06,-.09,.91),(-1.08,.12,1.18),(-.975,.12,1.18)],.025,.015,m['hose'])
# Actual bulkhead bores connect the new fitted circuits through the casing/chest walls.
liner=bpy.data.objects['CALCIFIER | REUSED calcifier_kiln_drum'];bore(liner,C('temporary return tap through refractory wall',(-.975,.12,1.18),.027,.36,m['iron'],'X'))
sump_wall=next(o for o in col.objects if o.name.startswith('CALCIFIER V2 | settling chest low side wall') and o.location.x<-.8)
bore(sump_wall,C('temporary sump bulkhead bore',(-.90,-.94,.17),.027,.16,m['iron'],'X'))
ring('sump bolted bulkhead',(-.92,-.94,.17),.050,.015,.03,m['bronze'],'X')
chest_wall=next(o for o in col.objects if o.name.startswith('CALCIFIER V2 | forming chest side') and o.location.x<.2)
bore(chest_wall,C('temporary forming chest wet inlet bore',(.105,-1.04,.46),.028,.16,m['iron'],'X'))
# Supported valve bodies, hand controls and legible plumbing glands are functional greebles.
for p in ((-.96,-.94,.17),(.09,-1.04,.46)):
 C('local isolation cock',p,.042,.10,m['bronze'],'X');C('local stopcock stem',(p[0],p[1],p[2]+.07),.012,.12,m['iron']);B('local stopcock handle',(p[0],p[1],p[2]+.135),(.11,.02,.02),m['iron'])
beam('distribution chest mounting strap',(.15,.43,1.02),(.28,.43,1.14),.025)
for x,y,z in ((-1.10,-.40,.52),(-1.06,-.09,.91)):
 beam('return tube masonry saddle',(x+.13,y,z-.04),(x,y,z-.04),.025);ring('return tube retaining band',(x,y,z),.038,.025,.035,m['iron'],'Y')
# Replace circular end lumps with true bored hex unions, ferrules and packing rings.
bpy.context.view_layer.update()
unions=[o for o in root.children_recursive if o.type=='MESH' and 'end union' in o.name]
fittings=[]
for old in unions:
 p=old.matrix_world.translation.copy();axis=(old.matrix_world.to_quaternion()@Vector((0,0,1))).normalized()
 radii=[math.hypot(v.co.x,v.co.y) for v in old.data.vertices];outer=max(radii);inner=min(radii)
 if (p-node).length<.002:p+=axis*(-.14 if 'north water steam inlet' in old.name else .14)
 old_name=old.name;bpy.data.objects.remove(old,do_unlink=True)
 union=C('bored hex process union',p,outer*1.08,.065,m['bronze'],segments=6);union.rotation_euler=axis.to_track_quat('Z','Y').to_euler()
 cutter=C('temporary circular union bore',p,inner,.18,m['iron']);cutter.rotation_euler=union.rotation_euler;bore(union,cutter)
 for sign in (-1,1):
  ferrule=ring('union stepped pipe ferrule',p+axis*sign*.048,outer*.92,inner,.023,m['copper']);ferrule.rotation_euler=axis.to_track_quat('Z','Y').to_euler()
  gasket=ring('union dark packing ring',p+axis*sign*.034,outer*.99,inner,.010,m['iron']);gasket.rotation_euler=axis.to_track_quat('Z','Y').to_euler()
 fittings.append(dict(replaces=old_name,center=list(p),bore=inner))
# Four bolts and an actual gasket back each preserved exterior joint, without moving sockets.
for y in (-1.48,1.48):
 ring('exterior flange packing gasket',(0,y,.20),.171,.090,.012,m['clay'],'Y')
 for a in (0,math.pi/2,math.pi,math.pi*1.5):
  x=.132*math.cos(a);z=.20+.132*math.sin(a);ring('flange stud washer',(x,y+.035,z),.024,.011,.009,m['iron'],'Y');bolt('flange hex retaining nut',(x,y+.045,z),'Y')
# The same crank phase drives wet forming and the small-throw separator eccentric.
for frame in range(1,194):
 scene.frame_set(frame);bpy.context.view_layer.update();theta=math.tau*2*(frame-1)/192
 pin=Vector((1.00+.004*math.cos(theta),-.86,1.05-.004*math.sin(theta)))
 travel=math.sqrt(LR**2-(pin.x+.66)**2-(pin.z-.43)**2);slide=Vector((-.66,pin.y-travel,.43))
 sieve.location=slide;sieve_rod.location=(pin+slide)/2;sieve_rod.rotation_euler=(pin-slide).to_track_quat('Z','Y').to_euler()
 for actor in (sieve,sieve_rod):actor.keyframe_insert(data_path='location',frame=frame)
 sieve_rod.keyframe_insert(data_path='rotation_euler',frame=frame)
for obj in col.objects:
 if obj.type!='MESH':continue
 if obj.modifiers:data=bpy.data.meshes.new_from_object(obj.evaluated_get(bpy.context.evaluated_depsgraph_get()));obj.modifiers.clear();obj.data=data
 if not obj.data.uv_layers:surfaces.physical_box_uv(obj)
 bm=bmesh.new();bm.from_mesh(obj.data);bmesh.ops.triangulate(bm,faces=list(bm.faces));bmesh.ops.delete(bm,geom=[v for v in bm.verts if not v.link_faces],context='VERTS');bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-7);bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=1e-7);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(obj.data);bm.free()
 obj.data.calc_loop_triangles();bad={t.polygon_index for t in obj.data.loop_triangles if t.area<1e-12}
 if bad:
  bm=bmesh.new();bm.from_mesh(obj.data);bm.faces.ensure_lookup_table();bmesh.ops.delete(bm,geom=[bm.faces[i] for i in bad],context='FACES');bm.to_mesh(obj.data);bm.free()
for obj in col.objects:
 if not obj.animation_data:continue
 for layer in obj.animation_data.action.layers:
  for strip in layer.strips:
   for bag in strip.channelbags:
    for curve in bag.fcurves:
     for key in curve.keyframe_points:key.interpolation='LINEAR'
profile=json.loads((P/'capture-profile.json').read_text());install_canonical_camera(scene,profile,bpy);scene.frame_set(1);assert_clean(scene,profile,bpy);bpy.ops.file.pack_all();native=O/'calcifier-v2.blend';bpy.ops.wm.save_as_mainfile(filepath=str(native),compress=True)
bpy.ops.wm.open_mainfile(filepath=str(native));scene=bpy.context.scene;root=bpy.data.objects['EXPORT | Calcifier all authored parts'];bpy.ops.object.select_all(action='DESELECT')
for obj in [root,*root.children_recursive]:obj.select_set(True)
bpy.ops.export_scene.gltf(filepath=str(O/'calcifier-v2.glb'),export_format='GLB',use_selection=True,export_cameras=False,export_lights=False,export_animations=True,export_animation_mode='SCENE',export_anim_scene_split_object=False,export_frame_range=True,export_force_sampling=True,export_frame_step=1,export_apply=True,export_extras=True)
(O/'capture-profile.json').write_text(json.dumps(profile,indent=2)+'\n');(O/'stations-receipt.json').write_text(json.dumps(dict(parent_source_sha256=sha(source),source_sha256=sha(native),runtime_sha256=sha(O/'calcifier-v2.glb'),recipe_modules={'Calcifier-pro through pro-5':'Heated wetted mineral bed and geared paddles','ionic-scum':'Settling sump, guided separation screen and internal return','microcrystal-sediment':'Driven grading sieve and draining bed','hydrocoptic-crystal':'Wet bioceramic preform feed and two-cavity piston die'},hex_union_records=fittings,sieve_rod_length=LR,external_ports_unchanged=True,gameplay_changed=False,owner_visual_approved=False,native_integrated=False),indent=2)+'\n')
projection=bpy.data.objects.new('SPRITE ONLY | square ground grid',None);scene.collection.objects.link(projection);projection.scale.y=math.sqrt(2);root.parent=projection;scene.render.resolution_x=scene.render.resolution_y=512
for name,yaw in [('front',0),('east',270),('rear',180),('west',90)]:
 root.rotation_euler.z=math.radians(yaw);scene.frame_set(49);scene.render.filepath=str(O/(name+'-review512.png'));bpy.ops.render.render(write_still=True)
root.rotation_euler.z=0
with temporary_inspection_camera(scene,bpy,'Calcifier process stations and fittings') as camera:
 camera.data.type='ORTHO';camera.data.ortho_scale=2.8;camera.location=(2,-4,2.8);camera.rotation_euler=(Vector((-.08,-.57,.75))-camera.location).to_track_quat('-Z','Y').to_euler();scene.camera=camera;scene.render.filepath=str(O/'stations-close512.png');bpy.ops.render.render(write_still=True)
print('CALCIFIER_RECIPE_STATIONS_SAVED',native,flush=True)
