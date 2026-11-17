"""Replace slab-like geology with weathered fractured outcrop and explicit worked seats."""
import bpy,bmesh,json,math,sys,tempfile,hashlib
import numpy as np
from pathlib import Path
from mathutils import Vector
H=Path(__file__).resolve().parent;R=H.parents[3];P=R/'models/island-survival/quarry/candidates/v2-detail02';O=R/'models/island-survival/quarry/candidates/v3-geology02'
if O.exists():raise FileExistsError(O)
O.mkdir(parents=True);tempfile.tempdir=str(R/'build/quarry-export-temp')
sys.path.insert(0,str(R/'models/island-survival/primitive-steam-powered-pump/v3'))
from mesh_util import mesh,box,cylinder
import surfaces
sys.path.insert(0,str(R.parent/'model-production/tools/fmpl'))
from blender_camera_guard import assert_clean,temporary_inspection_camera
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
source=P/'quarry-v2.blend';parent=json.loads((P/'refinement-receipt.json').read_text());assert sha(source)==parent['source_sha256']
bpy.ops.wm.open_mainfile(filepath=str(source));scene=bpy.context.scene;scene.frame_set(1);root=bpy.data.objects['EXPORT | Quarry all authored parts']
col=bpy.data.collections.new('QUARRY V3 | natural fracture and worn stone');scene.collection.children.link(col)
def mat(s):return next(m for m in bpy.data.materials if m.name.endswith(' | '+s))
wood=mat('long-grain-oak');end=mat('cut-oak-growth-rings');iron=mat('cast-iron-housing');bronze=mat('worn-bronze-fittings');bed=mat('quarry-v2-weathered-strata');fresh=mat('quarry-v2-fresh-cleavage')
def M(n,v,f,m,parent=root):
 o=mesh('QUARRY V3 | '+n,v,f,m,col,parent);surfaces.apply(o,m,end if m==wood else None);return o
def B(n,p,d,m,parent=root,bevel=.008):
 o=box('QUARRY V3 | '+n,p,d,m,col,parent,bevel);surfaces.apply(o,m,end if m==wood else None);return o
def C(n,p,r,d,m,axis='Z',segments=16):
 o=cylinder('QUARRY V3 | '+n,p,r,d,m,col,root,axis,segments);surfaces.apply(o,m);return o
def erase(o):bpy.data.objects.remove(o,do_unlink=True)
def apply(o):
 bpy.context.view_layer.objects.active=o
 for modifier in list(o.modifiers):bpy.ops.object.modifier_apply(modifier=modifier.name)
def boolean(a,b,op):
 bpy.context.view_layer.objects.active=a;mod=a.modifiers.new('Worked quarry cut','BOOLEAN');mod.object=b;mod.operation=op;mod.solver='EXACT';bpy.ops.object.modifier_apply(modifier=mod.name)
def rock(n,p,radii,seed):
 bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2,radius=1);o=bpy.context.object
 for c in tuple(o.users_collection):c.objects.unlink(o)
 col.objects.link(o);o.parent=root;o.name='QUARRY V3 | '+n
 planes=[(Vector((1,.3,-.5)).normalized(),.86),(Vector((-.25,1,.45)).normalized(),.89),(Vector((-.4,-.5,1)).normalized(),.88)]
 for i,v in enumerate(o.data.vertices):
  q=v.co*(.98+.025*math.sin(i*2.43+seed))
  for normal,d in planes:
   if q.dot(normal)>d:q-=normal*(q.dot(normal)-d)
  v.co=(q.x*radii[0],q.y*radii[1],q.z*radii[2])
 o.location=p;o.data.materials.append(bed);surfaces.physical_box_uv(o)
 mod=o.modifiers.new('Weathered fracture arris','BEVEL');mod.width=.035;mod.segments=3;mod.limit_method='ANGLE';mod.angle_limit=.28
 apply(o);return o
# A rounded irregular bedrock edge replaces the vertical rectangular plinth.
outline=[(-1.45,-1.28),(-1.34,-1.44),(-.76,-1.40),(-.34,-1.45),(.32,-1.41),(1.20,-1.44),(1.44,-1.24),(1.40,-.72),(1.45,-.17),(1.41,.50),(1.44,1.20),(1.27,1.43),(.55,1.39),(-.15,1.45),(-.80,1.41),(-1.42,1.26),(-1.40,.65),(-1.45,.04),(-1.40,-.55)]
vs=[];count=len(outline)
for ring,(scale,z) in enumerate(((.94,0),(1,.115),(.975,.245),(.91,.32))):
 for i,(x,y) in enumerate(outline):vs.append((x*scale,y*scale,z+(.014*math.sin(i*2.3) if ring in (1,2) else 0)))
faces=[tuple(reversed(range(count))),tuple(range(3*count,4*count))]
for k in range(3):
 for i in range(count):j=(i+1)%count;faces.append((k*count+i,k*count+j,(k+1)*count+j,(k+1)*count+i))
base=M('weathered continuous bedrock edge',vs,faces,bed)
banks=[]
for i,(p,r) in enumerate([
 ((-1.03,1.05,.69),(.43,.43,.55)),((-.54,1.06,.70),(.43,.43,.53)),((.04,1.12,.76),(.51,.37,.55)),((.59,1.10,.70),(.48,.39,.54)),((1.09,1.07,.67),(.38,.39,.53)),
 ((1.11,-.91,.51),(.37,.38,.48)),((1.12,-.35,.54),(.36,.40,.48)),((1.12,.23,.52),(.35,.42,.48)),((1.10,.79,.56),(.36,.48,.49))]):
 banks.append(rock('fractured outcrop '+str(i),p,r,i*.73))
north=banks[0]
for o in banks[1:5]:boolean(north,o,'UNION');erase(o)
# Extraction cuts affect the north working face, never the engine's supporting bank.
for n,p,d in [
 ('front extraction face',(0,-.20,.84),(2.70,1.89,.92)),
 ('upper worked bench',(0,.33,1.135),(2.70,1.11,.81))]:
 cutter=B('temporary '+n,p,d,fresh,bevel=0);boolean(north,cutter,'DIFFERENCE');erase(cutter)
boolean(base,north,'UNION');erase(north)
for o in banks[5:]:boolean(base,o,'UNION');erase(o)
cutter=B('temporary engine bench',(1.04,-.20,1.20),(1.00,2.20,.64),fresh,bevel=0);boolean(base,cutter,'DIFFERENCE');erase(cutter)
for x in (-.95,.95):
 cutter=B('temporary thrust seat',(x,1.14,1.40),(.31,.29,.58),fresh,bevel=0);boolean(base,cutter,'DIFFERENCE');erase(cutter)
for i in range(10):
 x=-1.10+i*.24
 cutter=B('temporary splitting kerf',(x,.765,.58),(.026,.13,.22),fresh,bevel=0);boolean(base,cutter,'DIFFERENCE');erase(cutter)
# Two shallow crosscuts and outer fracture notches break the continuous slab silhouette.
for x in (-.59,.53):
 cutter=B('temporary separated extraction cut',(x,1.01,.82),(.037,.53,.78),fresh,bevel=0);boolean(base,cutter,'DIFFERENCE');erase(cutter)
for i,(x,y,z) in enumerate([(-1.34,1.23,.82),(-.82,1.39,1.13),(.33,1.41,1.20),(1.29,1.18,.79),(1.40,-.94,.45),(1.42,.18,.45)]):
 cutter=B('temporary broken corner',(x,y,z),(.16,.18,.23),fresh,bevel=0);cutter.rotation_euler=(.18,-.25,.35+i*.4);boolean(base,cutter,'DIFFERENCE');erase(cutter)
old=bpy.data.objects['QUARRY | REUSED quarry_base_stone'];old.data=base.data;erase(base)
# Small, broad arrises soften worked edges; fracture faces retain their geological facets.
bev=old.modifiers.new('Worn exposed stone transitions','BEVEL');bev.width=.022;bev.segments=3;bev.limit_method='ANGLE';bev.angle_limit=.35
# Explicit hewn bearing stones support the detailed machinery on the rough bank.
for p,d in [
 ((1.10,-.320366,.83),(.49,.51,.10)),
 ((.94,-.820366,.83),(.54,.46,.10)),
 ((.90,.50,.83),(.28,.28,.10))]:
 B('seated machinery foundation stone',p,d,fresh,bevel=.018)
# Soften and visually blend the former rectangular floor patch into the workings.
floor=bpy.data.objects['QUARRY | REUSED quarry_excavation_floor']
rng=np.random.default_rng(171131);shape=(512,512);f=surfaces.field(rng,shape,.026);g=surfaces.field(rng,shape,.16)
tone=np.clip(.23+.04*f+.014*g,.10,.40);dust=np.clip(.5+.34*f,0,1)
color=np.stack([tone*(1+.09*dust),tone*(1-.07*dust),tone*(1-.20*dust)],axis=-1)
ground=surfaces.material('quarry-v3-rock-dust-and-floor',color,.94+.015*g,.5+.05*f+.02*g,0,O);ground.name=ground.name.replace('PUMP V3','QUARRY V3')
surfaces.apply(floor,ground)
bev=floor.modifiers.new('Loose worn floor edge','BEVEL');bev.width=.040;bev.segments=3
# Front right leg now seats on the engine bench rather than disappearing through it.
leg=bpy.data.objects['QUARRY | REUSED quarry_a_frame_right'];a=Vector((.9,.5,.88));b=Vector((.43,.6,2.4));length=(b-a).length
v=[(x,y,z) for z in (-length/2,length/2) for y in (-.085,.085) for x in (-.085,.085)]
data=bpy.data.meshes.new('Seated right A-frame timber');data.from_pydata(v,[],[(0,2,3,1),(4,5,7,6),(0,1,5,4),(1,3,7,5),(3,2,6,7),(2,0,4,6)]);data.update();leg.data=data;leg.location=(a+b)/2;leg.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler();surfaces.apply(leg,wood,end)
for o in root.children_recursive:
 if o.name.startswith('QUARRY | front heel shoe'):o.location.z=(.88 if o.location.x>0 else .32)+.025
for o in list(root.children_recursive):
 if 'heel anchoring spike' in o.name or 'heel anchor head' in o.name:erase(o)
for sign,height in [(-1,.32),(1,.88)]:
 for dx in (-.065,.065):
  x=sign*.9+dx;C('seated heel anchor stud',(x,.5,height-.005),.014,.14,iron)
  C('seated heel square nut',(x,.5,height+.0665),.026,.018,bronze,segments=4)
# Keep the brick supplies on a supported low working shelf, away from the broken bank.
for o in root.children_recursive:
 if 'bonded spare retaining brick' in o.name:o.location.y=.11;o.location.z-=.68
for i,x in enumerate((-1.12,-.93)):
 B('brick stock timber bearer',(x,.11,.445),(.18,.24,.03),wood,bevel=.003)
# Genuine broken output stone and chipped load edges replace perfect cubes.
block=bpy.data.objects['QUARRY | REUSED quarry_quarried_block_b']
plan=[(-.115,-1.01),(.265,-1.01),(.315,-.955),(.315,-.655),(.265,-.59),(-.065,-.59),(-.115,-.65)]
v=[(x,y,z) for z in (.46,.80) for x,y in plan];n=len(plan);faces=[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
data=bpy.data.meshes.new('Cleaved output chunk');data.from_pydata(v,[],faces);data.update();block.data=data;surfaces.apply(block,fresh)
for o in (block,bpy.data.objects['QUARRY | reused lifted stone']):
 mod=o.modifiers.new('Worn cleaved stone corners','BEVEL');mod.width=.018;mod.segments=3
# Re-seat mineral fracture inlays and splitting pegs only where the worked rock exists.
for o in list(root.children_recursive):
 if 'mineral fracture' in o.name:erase(o)
for o in list(root.children_recursive):
 if 'seated splitting wedge' in o.name:
  x=sum(v.co.x for v in o.data.vertices)/len(o.data.vertices)
  hit,point,normal,index=old.ray_cast(Vector((x,.60,.585)),Vector((0,1,0)),distance=.32)
  if not hit:erase(o)
# Inspection and export cleanup; the winch/piston/basket animation remains intact.
repairs={}
for o in root.children_recursive:
 if o.type!='MESH':continue
 apply(o)
 if not o.data.uv_layers:surfaces.physical_box_uv(o)
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.triangulate(bm,faces=list(bm.faces));bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-7);bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=1e-7);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free()
 o.data.calc_loop_triangles();bad={t.polygon_index for t in o.data.loop_triangles if t.area<1e-12}
 if bad:
  bm=bmesh.new();bm.from_mesh(o.data);bm.faces.ensure_lookup_table();bmesh.ops.delete(bm,geom=[bm.faces[i] for i in bad],context='FACES');bm.to_mesh(o.data);bm.free();repairs[o.name]=len(bad)
profile=json.loads((P/'capture-profile.json').read_text());scene.frame_set(1);assert_clean(scene,profile,bpy);bpy.ops.file.pack_all()
native=O/'quarry-v3.blend';bpy.ops.wm.save_as_mainfile(filepath=str(native),compress=True)
bpy.ops.wm.open_mainfile(filepath=str(native));scene=bpy.context.scene;root=bpy.data.objects['EXPORT | Quarry all authored parts']
bpy.ops.object.select_all(action='DESELECT')
for o in [root,*root.children_recursive]:o.select_set(True)
bpy.ops.export_scene.gltf(filepath=str(O/'quarry-v3.glb'),export_format='GLB',use_selection=True,export_cameras=False,export_lights=False,export_animations=True,export_animation_mode='SCENE',export_anim_scene_split_object=False,export_frame_range=True,export_force_sampling=True,export_frame_step=1,export_apply=True,export_extras=True)
(O/'capture-profile.json').write_text(json.dumps(profile,indent=2)+'\n')
(O/'geology-receipt.json').write_text(json.dumps({'parent_sha256':sha(source),'source_sha256':sha(native),'runtime_sha256':sha(O/'quarry-v3.glb'),'owner_feedback':'Natural stone edges are too sharp; held V1 also needs complex construction detail','natural_stone':'Joined fractured outcrop with rounded weathering/chipped transitions; straight faces restricted to extraction kerfs and worked machinery seats','mechanism_preserved':True,'right_timber_heel_seated_on_bank':True,'zero_area_repairs':repairs,'visual_approved':False,'native_integrated':False},indent=2)+'\n')
projection=bpy.data.objects.new('SPRITE ONLY | quarry square ground grid',None);scene.collection.objects.link(projection);projection.scale.y=math.sqrt(2);root.parent=projection
scene.cycles.samples=48;scene.render.resolution_x=scene.render.resolution_y=512
for name,yaw in [('front',0),('east',270),('rear',180),('west',90)]:
 root.rotation_euler.z=math.radians(yaw);scene.frame_set(49);scene.render.filepath=str(O/(name+'-review512.png'));bpy.ops.render.render(write_still=True)
print('QUARRY_NATURAL_STONE_SOURCE',native,flush=True)
