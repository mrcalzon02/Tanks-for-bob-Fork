"""Recipe-specific scum/sediment separator, wet preform die and properly fitted process plumbing."""
import bpy,bmesh,json,math,hashlib,sys,tempfile
import numpy as np
from pathlib import Path
from mathutils import Vector
H=Path(__file__).resolve().parent;R=H.parents[3];P=R/'models/island-survival/calcifier/candidates/v2-stations02';O=P.parent/'v2-sockets08'
if O.exists():raise FileExistsError(O)
O.mkdir(parents=True);tempfile.tempdir=str(R/'build/quarry-export-temp')
sys.path.insert(0,str(R/'models/island-survival/primitive-steam-powered-pump/v3'))
from mesh_util import mesh,box,cylinder,tube
import surfaces
sys.path.insert(0,str(R.parent/'model-production/tools/fmpl'))
from blender_camera_guard import install_canonical_camera,assert_clean,temporary_inspection_camera
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
source=P/'calcifier-v2.blend';assert sha(source)==json.loads((P/'stations-receipt.json').read_text())['source_sha256']
bpy.ops.wm.open_mainfile(filepath=str(source));scene=bpy.context.scene;scene.frame_set(1);root=bpy.data.objects['EXPORT | Calcifier all authored parts'];col=bpy.data.collections.new('CALCIFIER V2 | clearance corrections');scene.collection.children.link(col)
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

obj=bpy.data.objects
def remove(o):bpy.data.objects.remove(o,do_unlink=True)
oldpipes=['north water steam inlet','mineral bed lance','heated bowl engine supply','engine return to jacket','closed solids discharge']
newpipes=['wet die conditioning feed','water steam distribution valve chest','bolted valve chest cover','valve cover retained stud','distribution valve','distribution hand lever','distribution chest mounting strap','bored hex process union','union stepped pipe ferrule','union dark packing ring']
for o in tuple(root.children_recursive):
 if any(o.name.startswith('CALCIFIER | '+n) for n in oldpipes) or any(o.name.startswith('CALCIFIER V2 | '+n) for n in newpipes):remove(o)
for n in ('inlet valve spindle','inlet cross handle','inlet stop valve gland'):
 if 'CALCIFIER | '+n in obj:remove(obj['CALCIFIER | '+n])
# Shorter gland clears the crosshead at the very bottom of its stroke.
gland=obj['CALCIFIER | packed engine piston gland'];gland.location.z=.615;gland.scale.z=.65
obj['CALCIFIER | outer guide standoff.001'].location.z=.92
B('upper guide rail offset bracket',(.75,-.665,.95),(.06,.04,.065),m['iron'])
# Bearings below the bed, shortened guide rods and a forward offset clear the fire door.
sieve=obj['CALCIFIER V2 | guided scum sediment sieve carriage']
for o in tuple(root.children_recursive):
 if o.name.startswith('CALCIFIER V2 | sieve guide bearing block'):o.location.y-=.07;o.location.z=.245
 elif o.name.startswith('CALCIFIER V2 | sieve sliding guide rod'):o.location.z=-.185;o.scale.z=.50/.62
 elif o.name.startswith('CALCIFIER V2 | sieve moving edge'):o.location.z=-.075
 elif o.name.startswith('CALCIFIER V2 | graded sieve wire'):o.location.z=-.091
 elif o.name.startswith('CALCIFIER V2 | settling chest') or o.name.startswith('CALCIFIER V2 | settling sump floor'):o.location.y-=.07
 elif o.name.startswith('CALCIFIER | rack load bearing leg'):
  o.location.y-=.07;bore(o,C('temporary separator support guide bore',(-.84 if o.location.x<-.66 else -.48,-1.10,.245),.020,.90,m['iron'],'Y'))
 elif o.name.startswith('CALCIFIER | draining rack side rail'):o.location.y-=.07
for o in tuple(sieve.children):
 if o.name.startswith('CALCIFIER | mineral growth product'):o.location.y*=.85
# Take off from the UPPER pulley, away from the lower engine connecting rod.
# A rigid offset link stays in front of both the wheel plane and the forming station.
for n in ('sieve retained eccentric','extended eccentric support boss','rigid sieve drive arm','sieve crosshead socket'):
 target=obj.get('CALCIFIER V2 | '+n)
 if target:
  for child in tuple(target.children):remove(child)
  remove(target)
upper=next(o for o in root.children_recursive if o.type=='EMPTY' and 'pulley' in o.name.lower() and abs(o.location.z-1.55)<.01)
eccentric=C('sieve retained eccentric',(.002,-.31,0),.018,.66,m['bronze'],'Y',upper)
C('extended eccentric support boss',(.002,-.16,0),.031,.28,m['bronze'],'Y',upper)
arm=E('rigid offset separator arm');LR=math.sqrt(1.29**2+.51**2+1.18**2)
pin=Vector((.632,-.86,1.55));end=Vector((-.66,pin.y-math.sqrt(LR**2-(pin.x+.66)**2-(pin.z-.37)**2),.37))
arm.location=(pin+end)/2;arm.rotation_euler=(pin-end).to_track_quat('Z','Y').to_euler();bpy.context.view_layer.update()
path=[pin,Vector((.632,-1.44,1.55)),Vector((-.66,-1.44,.37)),end];local=[arm.matrix_world.inverted()@p for p in path]
for i in range(3):beam('offset separator rigid arm segment',local[i],local[i+1],.025,m['iron'],arm)
for p in (local[0],local[-1]):ball('separator spherical retained end',p,arm)
ring('sieve crosshead socket',(0,-.27,-.06),.040,.021,.045,m['bronze'],'X',sieve)
for frame in range(1,194):
 scene.frame_set(frame);theta=math.tau*2*(frame-1)/192;pin=Vector((.63+.002*math.cos(theta),-.86,1.55-.002*math.sin(theta)))
 end=Vector((-.66,pin.y-math.sqrt(LR**2-(pin.x+.66)**2-(pin.z-.37)**2),.37));sieve.location=(end.x,end.y+.27,.43);sieve.keyframe_insert(data_path='location',frame=frame)
 arm.location=(pin+end)/2;arm.rotation_euler=(pin-end).to_track_quat('Z','Y').to_euler()
 for prop in ('location','rotation_euler'):arm.keyframe_insert(data_path=prop,frame=frame)
scene.frame_set(1);bpy.context.view_layer.update()
B('load bearing die pad',(.29,-1.04,.365),(.30,.26,.07),m['stone'])
shaft=obj['CALCIFIER V2 | forming guided piston shaft'];shaft.location.z=.29;shaft.scale.z=.52/.70
for n in ('bioceramic preform feed box','preform transfer lip','visible bioceramic preform','visible bioceramic preform.001'):remove(obj['CALCIFIER V2 | '+n])
B('supported preform loading tray',(.29,-1.28,.50),(.24,.10,.08),m['wood'])
B('preform transfer lip',(.29,-1.18,.55),(.22,.16,.025),m['bronze'])
for x in (.23,.35):
 C('visible bioceramic preform',(x,-1.28,.565),.039,.05,m['mineral'])
 beam('preform tray brace',(x,-1.19,.36),(x,-1.28,.46),.022)
axle=obj['CALCIFIER | turning lower engine axle'];axle.location.y=.17;axle.scale.z=.35/.45
bore(obj['CALCIFIER | engine stone load block'],C('temporary piston bottom clearance',(1,-.635,.39),.029,.15,m['iron']))
bore(obj['CALCIFIER | lower axle load bridge'],C('temporary lower hub swept clearance',(1,-.55,1.05),.064,.23,m['iron'],'Y'))
obj['CALCIFIER | upper pulley bored journal'].location.y+=.012
bore(obj['CALCIFIER | lower pinion stone pedestal'],C('temporary pinion pedestal bearing recess',(.63,.05,.63),.036,.18,m['iron']))
upper_shaft=obj['CALCIFIER | upper turning shaft'];upper_shaft.location.y=.1925;upper_shaft.scale.z=.585/.88
ring('driving bevel keyed hub',(0,-.135,0),.059,.027,.07,m['bronze'],'Y',obj['CALCIFIER | driving 18 tooth miter'])
# The wet-die cock sits on the right, below and outside the platen sweep.
obj['CALCIFIER V2 | local isolation cock.001'].location.x=.51
for n in ('local stopcock stem.001','local stopcock handle.001'):
 o=obj['CALCIFIER V2 | '+n];o.location=(.58 if 'stem' in n else .645,-1.04,.46);o.rotation_euler.y=math.pi/2
for n in ('local stopcock stem','local stopcock handle'):
 o=obj['CALCIFIER V2 | '+n];o.location=(-1.02 if 'stem' in n else -1.085,-.94,.17);o.rotation_euler.y=math.pi/2
for n in ('local isolation cock','sump bolted bulkhead','settling sump internal return'):obj['CALCIFIER V2 | '+n].location.y-=.07
obj['CALCIFIER V2 | local isolation cock'].location.y=-.94
obj['CALCIFIER V2 | sump bolted bulkhead'].location.y=-.94
sumpwall=obj['CALCIFIER V2 | settling chest low side wall'];bore(sumpwall,C('temporary fitted sump valve bore',(-.90,-.94,.17),.028,.20,m['iron'],'X'))

def fit(n,p,t,r,inner):
 t=Vector(t).normalized();p=Vector(p);o=C(n+' hex union',p,r+.013,.040,m['bronze'],segments=6);o.rotation_euler=t.to_track_quat('Z','Y').to_euler()
 cut=C('temporary fitted union bore',p,inner,.15,m['iron']);cut.rotation_euler=o.rotation_euler;bore(o,cut)
 for sign in (-1,1):
  a=ring(n+' ferrule',p+t*sign*.032,r+.007,inner,.020,m['copper']);a.rotation_euler=o.rotation_euler
  a=ring(n+' packing',p+t*sign*.022,r+.010,inner,.005,m['iron']);a.rotation_euler=o.rotation_euler
 return o
def pipe(n,points,r=.027,inner=.017,fitted=True):
 controls=[Vector(p) for p in points];route=[controls[0]]
 # Circular-style elbow fillets avoid spline overshoot into adjacent mechanisms.
 for i in range(1,len(controls)-1):
  a,b,c=controls[i-1:i+2];d=min(.08,(a-b).length*.25,(c-b).length*.25);start=b+(a-b).normalized()*d;end=b+(c-b).normalized()*d;route.append(start)
  for j in range(1,9):
   t=j/8;route.append((1-t)**2*start+2*(1-t)*t*b+t*t*end)
 route.append(controls[-1]);samples=[(p,(route[min(i+1,len(route)-1)]-route[max(0,i-1)]).normalized(),r,inner) for i,p in enumerate(route)]
 o=tube('CALCIFIER V2 | '+n,samples,m['copper'],col,root,32)
 if fitted:
  for i in (0,-1):
   p,t,_,_=samples[i];fit(n,p+t*(.10 if i==0 else -.10),t,r,inner)
 return o
node=Vector((.55,.60,1.30));chest=B('external distribution valve chest',node,(.24,.24,.24),m['bronze'])
pipe('fixed north inlet',[(0,1.50,.20),(0,1.30,.20),(.35,1.30,.24),(.55,1.30,.55),(.60,.95,1.0),(.55,.60,1.18)],.075,.051)
pipe('left mineral wetting lance',[(.50,.60,1.42),(.50,.60,1.57),(.10,.72,1.59),(-.10,.50,1.59),(-.10,.37,1.31)],.022,.013)
pipe('right mineral wetting lance',[(.60,.60,1.42),(.60,.83,1.62),(-.40,.82,1.62),(-.70,.30,1.62),(-.62,.18,1.31)],.022,.013)
pipe('supported engine supply',[(.67,.60,1.30),(.80,.40,1.30),(1.38,.40,1.30),(1.38,-1.02,.55),(1,-1.02,.55),(1,-.675,.55)],.031,.019)
pipe('external engine return',[(1,-.675,.45),(1,-1.10,.45),(.90,-1.10,.45),(.90,-1.10,1.0),(.70,-.90,1.30),(.40,-.40,1.30),(.27,-.30,1.30)],.026,.016)
pipe('front mineral discharge',[(-.66,-.53,1.22),(-.72,-.75,.92),(-.72,-.97,.47)],.090,.071,False);fit('discharge outlet',(-.72,-.92,.53),(0,-.22,-.45),.090,.071)
pipe('conditioned die feed',[(.43,.60,1.30),(.30,.60,1.30),(.30,.95,1.30),(.30,.95,1.69),(-.15,.95,1.69),(-.15,-.70,1.69),(-.15,-1.30,.86),(.54,-1.30,.86),(.54,-1.04,.46)],.026,.016)
wall=obj['CALCIFIER V2 | forming chest side.001'];bore(wall,C('temporary right wet inlet',(.475,-1.04,.46),.028,.30,m['iron'],'X'))
pipe('die side inlet',[(.54,-1.04,.46),(.405,-1.04,.46)],.026,.016,False)
bore(obj['CALCIFIER V2 | two cavity bioceramic forming die'],C('temporary die conditioning gallery',(.45,-1.04,.46),.028,.12,m['iron'],'X'))
for center,radius in [((1,-.635,.55),.033),((1,-.635,.45),.028)]:bore(obj['CALCIFIER | bored engine cylinder'],C('temporary real engine port',center,radius,.30,m['iron'],'Y'))
for center,tangent,radius in [((.27,-.30,1.30),(-.13,.10,0),.032),((-.66,-.53,1.22),(-.06,-.22,-.30),.098)]:
 cut=C('temporary aligned vessel bulkhead',center,radius,.42,m['iron']);cut.rotation_euler=Vector(tangent).to_track_quat('Z','Y').to_euler();bore(obj['CALCIFIER | REUSED calcifier_kiln_drum'],cut)
for p,tangent,r in [((.55,.60,1.18),(-.05,-.35,.18),.077),((.50,.60,1.42),(0,0,1),.024),((.60,.60,1.42),(0,.23,.20),.024),((.67,.60,1.30),(.13,-.20,0),.033),((.43,.60,1.30),(-1,0,0),.028)]:
 cut=C('temporary aligned manifold port',p,r,.30,m['iron']);cut.rotation_euler=Vector(tangent).to_track_quat('Z','Y').to_euler();bore(chest,cut)
# Rebuild the sump return with a fixed wall tap, rather than translating its vessel end.
remove(obj['CALCIFIER V2 | settling sump internal return'])
pipe('settling sump fitted return',[(-.66,-.94,.17),(-.96,-.94,.17),(-1.08,-.72,.26),(-1.10,-.40,.52),(-1.08,-.09,.91),(-1.08,.12,1.18),(-.96,.12,1.18)],.025,.015,False)
bore(obj['CALCIFIER | REUSED calcifier_kiln_drum'],C('temporary restored sump wall tap',(-.975,.12,1.18),.031,.30,m['iron'],'X'))
B('distribution valve bracket',(.55,.45,1.19),(.10,.08,.10),m['iron']);beam('valve chest support strut',(.55,.45,1.14),(1.14,.65,1.14),.035)
ring('blanked original die tap',(.075,-1.04,.46),.035,.006,.035,m['bronze'],'X')
# Full-bore native pipe couplings. Mouth planes stay at +/-1.5 tiles; the old
# 0.15-tile process tube was never large enough to be a player pipe interface.
for o in tuple(root.children_recursive):
 if any(o.name.startswith('CALCIFIER | '+n) for n in ('fixed player pipe flange','pipe flange stud','blanked unused process outlet','capped spare south outlet')) or any(o.name.startswith('CALCIFIER V2 | '+n) for n in ('exterior flange packing gasket','flange stud washer','flange hex retaining nut','fixed north inlet hex union','fixed north inlet ferrule','fixed north inlet packing')):remove(o)
inlet=obj['CALCIFIER V2 | fixed north inlet']
# Raise the first straight section to meet the new seated throat, then blend
# into the retained small process line rather than moving the native socket.
for v in inlet.data.vertices:
 if v.co.y>1.29 and abs(v.co.x)<.12:v.co.z+=.16
for sign,role in [(1,'north inlet'),(-1,'capped unused south outlet')]:
 t=Vector((0,sign,0));z=.36
 stations=[(Vector((0,sign*1.10,z)),t,.075,.051),(Vector((0,sign*1.29,z)),t,.075,.051),(Vector((0,sign*1.39,z)),t,.300,.280),(Vector((0,sign*1.46,z)),t,.300,.280),(Vector((0,sign*1.50,z)),t,.300,.280)]
 throat=tube('CALCIFIER V2 | full bore '+role+' reducer',stations,m['iron'],col,root,64)
 flange=ring('full size '+role+' flange',(0,sign*1.465,z),.420,.280,.070,m['bronze'],'Y')
 # A cast flat foot seats the flange on the paving while the circular bore
 # stays above it. No exposed connector geometry extends below the ground.
 for v in flange.data.vertices:
  if v.co.z+z<.072:v.co.z=.072-z
 gasket=ring('full size '+role+' packing',(0,sign*1.503,z),.365,.280,.008,m['iron'],'Y')
 for angle in (0,45,90,135,180,225,315):
  a=math.radians(angle);p=(.350*math.cos(a),sign*1.515,z+.350*math.sin(a))
  ring(role+' bolt washer',p,.032,.014,.012,m['iron'],'Y');C(role+' retained hex bolt',p,.024,.035,m['bronze'],'Y',segments=6)
 B(role+' cast mounting foot',(0,sign*1.445,.092),(.52,.11,.04),m['iron'])
 if sign<0:C('removable unused outlet blanking plate',(0,-1.507,z),.277,.018,m['iron'],'Y',segments=64)
 # Only the south internal line is otherwise unused; its sealed reducer is
 # the honest visual representation of the current recipe's inactive outlet.
# Freeze changed geometry, reopen the editable source, and export the same assembly.
for o in tuple(root.children_recursive):
 if o.type!='MESH':continue
 if o.modifiers:o.data=bpy.data.meshes.new_from_object(o.evaluated_get(bpy.context.evaluated_depsgraph_get()));o.modifiers.clear()
 if not o.data.uv_layers:surfaces.physical_box_uv(o)
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.triangulate(bm,faces=list(bm.faces));bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-7);bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=1e-7);bmesh.ops.delete(bm,geom=[v for v in bm.verts if not v.link_faces],context='VERTS');bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free()
for o in (sieve,arm):
 for layer in o.animation_data.action.layers:
  for strip in layer.strips:
   for bag in strip.channelbags:
    for curve in bag.fcurves:
     for key in curve.keyframe_points:key.interpolation='LINEAR'
profile=json.loads((P/'capture-profile.json').read_text());install_canonical_camera(scene,profile,bpy);scene.frame_set(1);assert_clean(scene,profile,bpy);bpy.ops.file.pack_all();native=O/'calcifier-v2.blend';bpy.ops.wm.save_as_mainfile(filepath=str(native),compress=True)
bpy.ops.wm.open_mainfile(filepath=str(native));scene=bpy.context.scene;root=bpy.data.objects['EXPORT | Calcifier all authored parts'];bpy.ops.object.select_all(action='DESELECT')
for o in [root,*root.children_recursive]:o.select_set(True)
bpy.ops.export_scene.gltf(filepath=str(O/'calcifier-v2.glb'),export_format='GLB',use_selection=True,export_cameras=False,export_lights=False,export_animations=True,export_animation_mode='SCENE',export_anim_scene_split_object=False,export_frame_range=True,export_force_sampling=True,export_frame_step=1,export_apply=True,export_extras=True)
(O/'capture-profile.json').write_text(json.dumps(profile,indent=2)+'\n');(O/'clearance-repair-receipt.json').write_text(json.dumps({'parent_sha256':sha(source),'source_sha256':sha(native),'glb_sha256':sha(O/'calcifier-v2.glb'),'clearance_approved':False,'native_verified':False,'separator_endpoint_distance':LR},indent=2)+'\n')
with temporary_inspection_camera(scene,bpy,'Actual clearance repair review') as camera:
 camera.data.type='ORTHO';camera.data.ortho_scale=3.2;camera.location=(2,-4,2.8);camera.rotation_euler=(Vector((0,-.50,.85))-camera.location).to_track_quat('-Z','Y').to_euler();scene.camera=camera;scene.render.resolution_x=scene.render.resolution_y=768;scene.render.filepath=str(O/'mechanisms-review768.png');bpy.ops.render.render(write_still=True)
print('CLEARANCE_REPAIR_SAVED',native,flush=True)
