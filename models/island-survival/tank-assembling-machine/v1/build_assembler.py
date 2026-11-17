"""Refine the exact saved nine-group gantry into a primitive electric vehicle works."""
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
starter=H/'starter-tank-assembling-machine.obj';assert sha(starter)=='cc89317f7b92cec81cb63d33921a5d5029d1eddde3a50fffa333ed092f41f119'
contract=json.loads((H/'contract.json').read_text());assert len(contract['processing_recipes'])==13 and contract['entity']['electric']
bpy.ops.wm.read_factory_settings(use_empty=True);s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=32;s.cycles.use_denoising=False;s.render.film_transparent=True;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGBA';s.render.threads_mode='FIXED';s.render.threads=6;s.view_settings.view_transform='AgX'
s.world=bpy.data.worlds.new('Neutral primitive vehicle works');s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs[0].default_value=(.32,.32,.32,1)
for pos,power in [((4,-4,7),800),((-4,2,5),450)]:
 l=bpy.data.lights.new('Vehicle works area','AREA');l.energy=power;l.size=5;o=bpy.data.objects.new(l.name,l);s.collection.objects.link(o);o.location=pos;o.rotation_euler=(Vector((0,0,1))-o.location).to_track_quat('-Z','Y').to_euler()
root=bpy.data.objects.new('EXPORT | Tanks vehicle conversion gantry',None);s.collection.objects.link(root);col=bpy.data.collections.new('VEHICLE WORKS | supported conversion bed and electric tooling');s.collection.children.link(col);m=surfaces.create(O)
rng=np.random.default_rng(171913);u,v=np.meshgrid(np.linspace(0,1,512),np.linspace(0,1,512));coarse=surfaces.field(rng,(512,512),.016);fine=surfaces.field(rng,(512,512),.24)
scuff=np.exp(-((v-.52)/.30)**2)*np.sin(u*220+coarse)**2
for name,color,rough,metal,detail in [('bedded-limestone',(.31,.30,.265),.94,0,.014*coarse+.004*fine),('oiled-hemp-rope',(.24,.175,.10),.93,0,.016*np.sin(u*180+v*35)+.005*fine),('insulated-winding-cloth',(.25,.19,.115),.95,0,.010*np.sin(u*190)*np.sin(v*210)+.006*coarse),('oxide-green-hull',(.12,.16,.095),.68,.5,.012*coarse+.025*scuff),('glazed-ceramic-insulator',(.48,.40,.29),.35,0,.012*coarse+.003*fine),('joint-arc',(.63,.40,.13),.38,.1,.006*fine)]:
 m[name]=surfaces.material('tank-assembler-'+name,np.stack([c+detail for c in color],axis=-1),rough+.015*fine,.5+.018*coarse+.008*fine,metal,O)
arc=m['joint-arc'].node_tree.nodes['Principled BSDF'];arc.inputs['Emission Color'].default_value=(1,.62,.22,1);arc.inputs['Emission Strength'].default_value=5
for mat in m.values():mat.name=mat.name.replace('PUMP V3','TANK ASSEMBLER');mat['surface_authorship']='Tank conversion gantry: oak fibres/end cuts on braced load paths, bedded limestone, forged joint plates, winding cloth and glazed clay terminals, twisted hemp lifting rope, scuffed oxide-green vehicle plate. Physical per-part UVs; useful common base metal/wood images explicitly reused.'
def E(n,pos=(0,0,0),parent=root):
 o=bpy.data.objects.new('VEHICLE | '+n,None);col.objects.link(o);o.parent=parent;o.location=pos;return o
def B(n,pos,dims,mat=None,parent=root,bevel=.005):
 mat=mat or m['wood'];o=box('VEHICLE | '+n,pos,dims,mat,col,parent,bevel);surfaces.apply(o,mat,m['endgrain'] if mat==m['wood'] else None);return o
def C(n,pos,r,depth,mat=None,axis='Z',parent=root,segments=32):
 mat=mat or m['iron'];o=cylinder('VEHICLE | '+n,pos,r,depth,mat,col,parent,axis,segments);surfaces.apply(o,mat);return o
def ring(n,pos,outer,inner,depth,mat=None,axis='Z',parent=root):
 mat=mat or m['bronze'];t=Vector({'X':(1,0,0),'Y':(0,1,0),'Z':(0,0,1)}[axis]);o=tube('VEHICLE | '+n,[(-t*depth/2,t,outer,inner),(t*depth/2,t,outer,inner)],mat,col,parent,40);o.location=pos;return o
def beam(n,a,b,width,mat=None,parent=root):
 a,b=Vector(a),Vector(b);o=B(n,(a+b)/2,(width,width,(b-a).length),mat,parent);o.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler();return o
def bore(o,c):
 bpy.context.view_layer.update();bpy.context.view_layer.objects.active=o
 for pre in list(o.modifiers):bpy.ops.object.modifier_apply(modifier=pre.name)
 mod=o.modifiers.new('Actual fitted through bore','BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=c;bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(c,do_unlink=True)
def wire(n,points,r,mat=None,parent=root):
 pts=[Vector(p) for p in points];o=tube('VEHICLE | '+n,[(pt,(pts[min(i+1,len(pts)-1)]-pts[max(0,i-1)]).normalized(),r,r*.35) for i,pt in enumerate(pts)],mat or m['insulated-winding-cloth'],col,parent,16);surfaces.physical_box_uv(o);return o
def linear(o):
 for layer in o.animation_data.action.layers:
  for strip in layer.strips:
   for bag in strip.channelbags:
    for curve in bag.fcurves:
     for key in curve.keyframe_points:key.interpolation='LINEAR'
# Preserve each saved group as editable geometry with explicit refinement.
verts=[];groups={};name=None
for line in starter.read_text().splitlines():
 t=line.split()
 if not t:continue
 if t[0]=='v':verts.append(Vector(map(float,t[1:])))
 elif t[0]=='g':name=t[1];groups[name]=[]
 elif t[0]=='f':groups[name].append(tuple(int(i)-1 for i in t[1:]))
assert len(groups)==9
reused={}
for name,faces in groups.items():
 ids=sorted({i for f in faces for i in f});lookup={i:j for j,i in enumerate(ids)};pts=[verts[i].copy() for i in ids];fs=[tuple(lookup[i] for i in f) for f in faces];kind=name.removeprefix('tank-assembling-machine_');mat=m['wood'];parent=root
 if kind=='factory_foundation':pts=[(p.x,p.y,p.z*.36) for p in pts];mat=m['bedded-limestone']
 elif kind.startswith('assembly_rail'):pts=[(p.x,p.y,.24+(p.z-.30)*.55) for p in pts];mat=m['iron']
 elif kind.startswith('gantry_support'):pts=[(p.x,p.y,.18+(p.z-.40)*1.10) for p in pts]
 elif kind=='overhead_gantry':pts=[(p.x,p.y,p.z+.10) for p in pts]
 elif kind=='empty_hull_jig':
  fs=fs[:2]+fs[4:];pts=[(p.x*(.68 if p.z<.6 else .82),p.y,.56+(p.z-.425)*.76) for p in pts];mat=m['oxide-green-hull']
 elif kind=='welding_head':pts=[((p.x-.65)*.42,(p.y+.46)*.42,(p.z-1.38)*.34) for p in pts];mat=m['copper']
 elif kind=='sparks_marker':pts=[((p.x-.65)*.08,(p.y+.46)*.08,(p.z-1.02)*.10) for p in pts];mat=m['joint-arc']
 o=mesh('VEHICLE | REUSED '+name,pts,fs,mat,col,parent);surfaces.apply(o,mat,m['endgrain'] if mat==m['wood'] else None);o['retained_starter_group']=name;reused[kind]=o
 if kind=='empty_hull_jig':mod=o.modifiers.new('Real open vehicle plate thickness','SOLIDIFY');mod.thickness=.035;mod.offset=0
for i in range(10):B('separate timber bed plank',(-1.26+i*.28,0,.155),(.265,2.70,.05))
for y in (-1.10,-.35,.45,1.15):
 B('rail grounded transverse sleeper',(0,y,.225),(2.65,.15,.10))
 for x in (-1.02,1.02):C('rail retained clamp bolt',(x,y,.40),.022,.07,m['bronze'],segments=6)
for x in (-1.12,1.12):
 B('gantry seated forged foot',(x,.9,.255),(.36,.40,.15),m['iron'])
 for y in (.76,1.04):
  C('foot through anchor',(x,y,.35),.025,.10,m['bronze'],segments=6)
 beam('gantry fore and aft knee',(x,.03,.18),(x,.83,1.17),.105)
 beam('gantry upper knee',(x,.9,1.98),(x-math.copysign(.43,x),.9,2.43),.11)
 for z in (.50,1.94,2.39):B('post retaining hoop',(x,.9,z),(.25,.33,.05),m['iron'])
 for yy in (.70,1.02):B('winch cantilever foot',(x*.46,yy,2.60),(.22,.14,.06),m['iron'])
# Two transverse skid bolsters support the representative input hull above rails.
for y in (-.72,.40):B('hull jig supported cross-bolster',(0,y,.44),(2.26,.18,.16),m['wood'])
for x in (-.50,.50):
 for y in (-.72,.40):B('hull locator and clamp',(x,y,.56),(.14,.19,.10),m['bronze'])
# Recognisable input vehicle tracks: fixed capsule bands and pinned road wheels.
for x in (-.84,.84):
 path=[]
 for center,start in [(.48,-math.pi/2),(-.78,math.pi/2)]:
  path += [(center+.17*math.cos(a),.74+.17*math.sin(a)) for a in np.linspace(start,start+math.pi,17)]
 # capsule axis follows Y; outer tread plates face radially from the track centre.
 pts=[]
 for yc,zc in path:
  yy=yc-(.48 if yc>-.15 else -.78);zz=zc-.74;normal=Vector((0,yy,zz)).normalized()
  for side,rad in [(-1,-1),(1,-1),(1,1),(-1,1)]:pts.append((x+side*.105,yc+normal.y*rad*.025,zc+normal.z*rad*.025))
 fs=[]
 for i in range(len(path)):
  j=(i+1)%len(path)
  for k in range(4):fs.append((4*i+k,4*j+k,4*j+(k+1)%4,4*i+(k+1)%4))
 o=mesh('VEHICLE | continuous retained input vehicle track',pts,fs,m['iron'],col,root);surfaces.physical_box_uv(o)
 for y in (-.78,-.36,.06,.48):
  C('vehicle road wheel',(x,y,.74),.147,.18,m['iron'],'X');C('road wheel retained hub',(x+math.copysign(.11,x),y,.74),.045,.045,m['bronze'],'X')
 for y in np.linspace(-.74,.44,10):
  for z in (.545,.935):B('individual track tread shoe',(x,float(y),z),(.25,.095,.035),m['iron'])
for y in (-.78,-.36,.06,.48):
 bore(reused['empty_hull_jig'],C('temporary actual hull axle bore',(0,y,.74),.029,1.90,m['iron'],'X'))
 C('retained vehicle through axle',(0,y,.74),.025,1.70,m['iron'],'X')
for x in (-.63,.63):
 for y in np.linspace(-.80,.50,8):C('hull plate visible rivet',(x,float(y),1.065),.014,.035,m['bronze'])
 B('hull top rail',(x,-.15,1.08),(.075,1.60,.04),m['oxide-green-hull'])
B('open hull central bulkhead',(0,-.10,.82),(1.08,.06,.39),m['oxide-green-hull'])
for x in (-.33,.33):
 B('existing vehicle crew seat',(x,-.57,.75),(.27,.25,.08),m['wood']);B('existing seat back',(x,-.43,.87),(.27,.06,.25),m['wood'])
# Rear engine module stays upright; the gantry carries its complete load path.
load=E('upright suspended engine module',(0,.42,1.32));B('lifted replacement engine block',(0,0,0),(.56,.38,.27),m['iron'],load)
for x in (-.18,0,.18):C('engine cylinder head',(x,0,.17),.065,.13,m['bronze'],parent=load)
for x in (-.30,.30):B('engine mounting lug',(x,0,-.08),(.08,.22,.06),m['iron'],load)
B('upright load spreader',(0,0,.57),(.66,.10,.07),m['wood'],load)
for x in (-.26,.26):
 ring('load spreader suspension eye',(x,0,.64),.028,.014,.035,m['iron'],'Y',load)
 for y in (-.15,.15):beam('attached fixed length load sling',(x,0,.54),(math.copysign(.27,x),y,.14),.012,m['oiled-hemp-rope'],load)
 B('engine sling seated retaining strap',(math.copysign(.27,x),0,.13),(.035,.35,.025),m['iron'],load)
for x in (-.52,.52):
 B('forward winch cantilever',(x,.66,2.70),(.14,.91,.16));beam('cantilever underside knee',(x,.96,2.38),(x,.30,2.62),.065)
 B('winch bearing seated block',(x,.42,2.785),(.17,.19,.05),m['iron']);ring('fixed winch shaft bush',(x,.42,2.86),.054,.027,.10,m['bronze'],'X')
drum=E('reversing supported hoist drum',(0,.42,2.86));C('winch supported through shaft',(.0325,0,0),.025,1.295,m['iron'],'X',drum)
for x in (-.26,.26):
 C('rope winding drum',(x,0,0),.075,.15,m['wood'],'X',drum)
 for end in (-1,1):ring('drum retaining flange',(x+end*.083,0,0),.092,.03,.014,m['iron'],'X',drum)
 for i in range(7):ring('visible rope winding',(x-.06+i*.02,0,0),.081,.075,.012,m['oiled-hemp-rope'],'X',drum)
ropes=[]
for x in (-.26,.26):
 rope=C('variable hanging rope',(x,.42,2.30),.008,1,m['oiled-hemp-rope']);ropes.append(rope)
 # Rope exits the front tangent and runs over an anchored fairlead at its real X.
 ring('fixed hoist fairlead',(x,.42,2.72),.021,.010,.040,m['bronze'])
 beam('fairlead bearing support',(x,.445,2.72),(x,.73,2.72),.025,m['iron'])
# Compact overhead electric motor with copper windings and real seated bearings.
motor=E('reversing hoist electric armature',(-.84,.42,2.86));C('electric motor armature',(0,0,0),.108,.23,m['iron'],'X',motor)
C('motor supported through shaft',(.02,0,0),.025,.41,m['iron'],'X',motor)
for i in range(8):
 a=i*math.tau/8;beam('armature copper conductor',(-.11,.114*math.cos(a),.114*math.sin(a)),(.11,.114*math.cos(a),.114*math.sin(a)),.018,m['copper'],motor)
for x in (-1.0,-.68):
 ring('open motor housing',(x,.42,2.86),.155,.124,.045,m['iron'],'X');ring('motor bored shaft bush',(x,.42,2.86),.041,.027,.07,m['bronze'],'X');B('motor grounded bracket',(x,.69,2.80),(.08,.38,.065),m['iron'])
for x in (-1.0,-.68):
 for i in range(3):
  a=math.tau*i/3;beam('fixed motor bearing radial support',(x,.42+.040*math.cos(a),2.86+.040*math.sin(a)),(x,.42+.140*math.cos(a),2.86+.140*math.sin(a)),.018,m['iron'])
for z in (2.655,3.065):
 B('cloth wrapped fixed motor field',(-.84,.42,z),(.25,.10,.06),m['insulated-winding-cloth'])
 for x in np.linspace(-.94,-.74,8):ring('motor field copper turn',(float(x),.42,z),.060,.043,.009,m['copper'],'X')
ring('shaft rigid motor coupling',(-.615,0,0),.045,.025,.06,m['bronze'],'X',drum)
for x in (-.99,-.69):
 for sign in (-1,1):B('fixed field housing tie',(x,.42,2.86+sign*.18),(.035,.08,.12),m['iron'])
# Guided joining head refines the saved source instead of floating above the bed.
for y in (-.95,-.10):
 B('tool grounded outboard mast',(1.27,y,.91),(.11,.11,1.46));reach=beam('tool overhead reach',(1.27,y,1.69),(.65,y,1.69),.075);bore(reach,C('temporary actual rail through timber',(.65,y,1.69),.021,.24,m['iron'],'Y'))
 ring('tool rail grounded bearing',(.65,y,1.69),.045,.021,.07,m['bronze'],'Y')
C('fixed guided tool rail',(.65,-.525,1.69),.018,.94,m['iron'],'Y')
tool=E('guided joining head',(.65,-.46,1.37));reused['welding_head'].parent=tool
ring('bored tool sliding carriage',(0,0,.32),.040,.021,.14,m['bronze'],'Y',tool)
B('carriage stem',(0,0,.17),(.035,.075,.225),m['iron'],tool)
C('ceramic electrode collar',(0,0,-.15),.045,.065,m['glazed-ceramic-insulator'],parent=tool)
C('real joining electrode',(0,0,-.225),.012,.09,m['copper'],parent=tool)
effect=E('rooted intermittent joining arc',(0,0,-.273),tool);reused['sparks_marker'].parent=effect
# Articulated rigid electrical arms are solved from their endpoints each pose.
fixed_power=Vector((1.13,-.12,1.57));bus1=E('first rigid insulated electrical arm');bus2=E('second rigid insulated electrical arm')
for bus in (bus1,bus2):
 B('rigid insulated conductor',(0,0,0),(.022,.025,.34),m['insulated-winding-cloth'],bus)
 for z in (-.185,.185):ring('electrical arm pivot eye',(0,0,z),.026,.010,.025,m['bronze'],'Y',bus)
for bus in (bus1,bus2):C('seated articulated electrical pin',(0,.02 if bus==bus1 else 0,.185),.009,.10 if bus==bus1 else .06,m['copper'],'Y',bus)
# Parallel hinge leaves have actual axial clearance; the shared vertical pin spans both.
for leaf in bus2.children:leaf.location.y+=.04
C('fixed electrical arm seated pin',fixed_power,.009,.10,m['copper'])
beam('electrical arm support',(1.27,-.12,1.53),(1.13,-.12,1.53),.035,m['iron'])
B('grounded electrical terminal board',(1.27,-.20,1.70),(.14,.34,.08))
for y in (-.12,-.28):
 C('clay supply insulator',(1.27,y,1.765),.032,.075,m['glazed-ceramic-insulator']);C('real supply terminal',(1.27,y,1.82),.009,.10,m['copper'])
wire('fixed joining power lead',[(1.27,-.12,1.82),(1.17,-.20,1.85),(1.13,-.20,1.76),(1.13,-.20,1.53),(1.13,-.12,1.53)],.013)
wire('grounded motor supply lead',[(1.27,-.28,1.82),(1.35,-.28,1.90),(1.35,1.20,1.90),(1.35,1.20,2.85),(-.84,1.20,2.85),(-.84,1.20,3.065),(-.84,.48,3.065)],.013)
for x in (-.9,.9):
 B('rear cable bracket',(x,1.10,2.65),(.08,.28,.06),m['iron']);C('gantry cable clay standoff',(x,1.20,2.74),.035,.12,m['glazed-ceramic-insulator']);C('cable retained pin',(x,1.20,2.82),.009,.08,m['copper'])
# Spare arms/engine parts on a separate supported timber rack explain the upgrades.
for x in (-1.32,-1.18):
 for y in (-1.10,-.45):B('component rack grounded leg',(x,y,.41),(.06,.06,.48))
B('component rack plank',(-1.25,-.775,.67),(.22,.85,.065))
for y in (-1.02,-.80,-.58):
 ring('spare upgrade arm pivot',(-1.25,y,.73),.063,.032,.06,m['bronze'])
 B('spare upgrade arm',(-1.25,y,.78),(.07,.06,.17),m['iron'])
animated=[load,drum,motor,tool,bus1,bus2,effect,*ropes]
for frame in range(194):
 theta=0 if frame==0 else math.tau*(frame-1)/192;lift=.055*(1-math.cos(theta));load.location.z=1.32+lift;drum.rotation_euler.x=lift/.081;motor.rotation_euler.x=drum.rotation_euler.x
 tool.location.y=-.46+.12*math.sin(theta);target=Vector((.65,tool.location.y,1.57));mid=(fixed_power+target)/2;d=target-fixed_power;perp=Vector((-d.y,d.x,0)).normalized();elbow=mid-perp*math.sqrt(.37**2-d.length_squared/4)
 for bus,a,b in [(bus1,fixed_power,elbow),(bus2,elbow,target)]:bus.location=(a+b)/2;bus.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler()
 for rope in ropes:
  bottom=load.location.z+.66;top=2.779;rope.location.z=(bottom+top)/2;rope.scale.z=top-bottom
 effect.scale=(.001,)*3 if frame==0 else (1,1,.6+.4*math.sin(theta*8)**2)
 for o in animated:o.keyframe_insert(data_path='location',frame=frame);o.keyframe_insert(data_path='rotation_euler',frame=frame);o.keyframe_insert(data_path='scale',frame=frame)
for o in animated:linear(o)
for o in root.children_recursive:
 if o.type!='MESH':continue
 if o.modifiers:o.data=bpy.data.meshes.new_from_object(o.evaluated_get(bpy.context.evaluated_depsgraph_get()));o.modifiers.clear()
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.triangulate(bm,faces=list(bm.faces));bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-7);bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=1e-7);bmesh.ops.delete(bm,geom=[v for v in bm.verts if not v.link_faces],context='VERTS');bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free();o.data.calc_loop_triangles();bad={t.polygon_index for t in o.data.loop_triangles if t.area<1e-12}
 if bad:
  bm=bmesh.new();bm.from_mesh(o.data);bm.faces.ensure_lookup_table();bmesh.ops.delete(bm,geom=[bm.faces[i] for i in bad],context='FACES');bm.to_mesh(o.data);bm.free()
 if not o.data.uv_layers:surfaces.physical_box_uv(o)
s.frame_start=1;s.frame_end=193;s.render.fps=48;s.frame_set(1)
profile=dict(camera_policy='fmpl.factorio45.v1',capture_kind='entity',orientation_policy='fixed',directions=[0],states={'idle':[0],'working':list(range(1,193,6))},source_size=256,camera_override=dict(type='ORTHO',elevation_deg=45,azimuth_deg=0,distance=8,ortho_scale=6.4,target=[0,0,1.25]));install_canonical_camera(s,profile,bpy);s.render.resolution_x=s.render.resolution_y=256;assert_clean(s,profile,bpy)
root['prototype']='assembling-machine/tank-assembling-machine';root['units_per_tile']=1.;root['native_power']='Electric 250 kW, no fuel or fluid storage';root['purpose']='13 actual vehicle upgrade/light chassis recipes; retained input hull, upright replacement engine lift, guided electric joining tool'
bpy.ops.file.pack_all();source=O/'tank-assembler-v1.blend';bpy.ops.wm.save_as_mainfile(filepath=str(source),compress=True);bpy.ops.wm.open_mainfile(filepath=str(source));s=bpy.context.scene;root=bpy.data.objects['EXPORT | Tanks vehicle conversion gantry'];bpy.ops.object.select_all(action='DESELECT')
for o in [root,*root.children_recursive]:o.select_set(True)
bpy.ops.export_scene.gltf(filepath=str(O/'tank-assembler-v1.glb'),export_format='GLB',use_selection=True,export_cameras=False,export_lights=False,export_animations=True,export_animation_mode='SCENE',export_anim_scene_split_object=False,export_frame_range=True,export_force_sampling=True,export_frame_step=1,export_apply=True,export_extras=True)
(O/'capture-profile.json').write_text(json.dumps(profile,indent=2)+'\n');(O/'construction-receipt.json').write_text(json.dumps(dict(starter_sha256=sha(starter),preserved_starter_groups=list(groups),source_sha256=sha(source),runtime_sha256=sha(O/'tank-assembler-v1.glb'),native_power='electric 250kW',actual_recipe_contracts=13,owner_visual_approved=False,native_integrated=False,review_status='held_pending_actual_artifact_and_clearance_review'),indent=2)+'\n')
projection=bpy.data.objects.new('SPRITE ONLY | square ground correction',None);s.collection.objects.link(projection);projection.scale.y=math.sqrt(2);root.parent=projection;s.render.resolution_x=s.render.resolution_y=512
for name,yaw in [('front',0),('rear',180),('side',90)]:
 root.rotation_euler.z=math.radians(yaw);s.render.filepath=str(O/(name+'-review512.png'));bpy.ops.render.render(write_still=True)
root.rotation_euler.z=0
with temporary_inspection_camera(s,bpy,'Supported upright engine lift and guided joining electrode') as camera:
 target=Vector((0,.25,1.60));camera.data.type='ORTHO';camera.data.ortho_scale=3.6;camera.location=target+Vector((-3,-4,2.3));camera.rotation_euler=(target-camera.location).to_track_quat('-Z','Y').to_euler();s.camera=camera;s.render.filepath=str(O/'mechanism-close512.png');bpy.ops.render.render(write_still=True)
print('TANK_ASSEMBLER_SOURCE_SAVED_REOPENED_EXPORTED',sha(source),flush=True)

