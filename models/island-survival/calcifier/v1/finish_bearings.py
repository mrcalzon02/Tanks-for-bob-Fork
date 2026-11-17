"""Finish observed rod clearance and explicit axial/radial shaft support before delivery."""
import bpy,bmesh,json,hashlib,sys,tempfile,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[4];P=R/'models/island-survival/calcifier/candidates/v1-production01';O=P.parent/'v1-production03'
if O.exists():raise FileExistsError(O)
O.mkdir(parents=True);tempfile.tempdir=str(R/'build/quarry-export-temp')
sys.path.insert(0,str(R/'models/island-survival/primitive-steam-powered-pump/v3'))
from mesh_util import box,cylinder,tube
import surfaces
sys.path.insert(0,str(R.parent/'model-production/tools/fmpl'))
from blender_camera_guard import install_canonical_camera,assert_clean,temporary_inspection_camera
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
source=P/'calcifier-v1.blend';assert sha(source)==json.loads((P/'construction-receipt.json').read_text())['source_sha256']
bpy.ops.wm.open_mainfile(filepath=str(source));scene=bpy.context.scene;scene.frame_set(1);root=bpy.data.objects['EXPORT | Calcifier all authored parts'];col=bpy.data.collections.new('CALCIFIER | final fitted shaft supports');scene.collection.children.link(col)
material=lambda s:next(m for m in bpy.data.materials if m.name.endswith(' | '+s))
wood=material('long-grain-oak');endgrain=material('cut-oak-growth-rings');iron=material('cast-iron-housing');bronze=material('worn-bronze-fittings')
def B(n,p,d,mat,parent=root):
 o=box('CALCIFIER | '+n,p,d,mat,col,parent);surfaces.apply(o,mat,endgrain if mat==wood else None);return o
def C(n,p,r,d,mat,axis='Z',parent=root):
 o=cylinder('CALCIFIER | '+n,p,r,d,mat,col,parent,axis,40);surfaces.apply(o,mat);return o
def ring(n,p,outer,inner,depth,mat,axis='Z',parent=root):
 t=Vector({'X':(1,0,0),'Y':(0,1,0),'Z':(0,0,1)}[axis]);o=tube('CALCIFIER | '+n,[(-t*depth/2,t,outer,inner),(t*depth/2,t,outer,inner)],mat,col,parent,40);o.location=p;return o
def cut(obj,cutter):
 bpy.context.view_layer.update();bpy.context.view_layer.objects.active=obj;mod=obj.modifiers.new('Actual operating clearance','BOOLEAN');mod.operation='DIFFERENCE';mod.object=cutter;mod.solver='EXACT';bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cutter,do_unlink=True)
guide=next(o for o in root.children_recursive if o.name.startswith('CALCIFIER | engine guide crossmember') and abs(o.location.z-.98)<.0001)
cut(guide,B('temporary connecting rod travel opening',(1.00,-.635,.98),(.18,.18,.15),iron))
# Keep all stationary guide framing behind the flywheel's swept plane.
old_frames=[]
for obj in tuple(root.children_recursive):
 if obj.name.startswith('CALCIFIER | engine guide crossmember'):
  obj.location.y=-.40
  for vertex in obj.data.vertices:vertex.co.x*=.62/.37
  surfaces.physical_box_uv(obj,wood=True);old_frames.append(obj)
 elif obj.name.startswith('CALCIFIER | engine guide upright'):obj.location.y=-.40
 elif obj.name.startswith('CALCIFIER | fixed engine crosshead rail'):obj.location.x=.75 if obj.location.x<1 else 1.25
slider=bpy.data.objects['CALCIFIER | guided engine crosshead'];old_shoe=bpy.data.objects['CALCIFIER | bored engine crosshead'];bpy.data.objects.remove(old_shoe,do_unlink=True)
new_shoe=B('bored engine crosshead',(0,0,0),(.60,.08,.09),bronze,slider)
for x in (-.25,.25):cut(new_shoe,C('temporary wide crosshead rail bore',(x,0,0),.017,.20,iron,parent=slider))
for x in (.75,1.25):
 for z in (.58,.98):B('outer guide standoff',(x,-.5225,z),(.06,.325,.055),iron)
mix=bpy.data.objects['CALCIFIER | mineral paddle gear and shaft'];pinion=bpy.data.objects['CALCIFIER | vertical 31 tooth pinion'];fly=bpy.data.objects['CALCIFIER | engine crank flywheel']
ring('mixer load carrying thrust collar',(0,0,.3225),.066,.034,.045,bronze,parent=mix)
C('mixer thrust collar retained cross pin',(0,0,.33),.007,.12,iron,'X',mix)
ring('pinion lower thrust collar',(0,0,-1.0475),.060,.029,.045,bronze,parent=pinion)
# A bored, grounded cradle supports the lower flywheel axle behind its moving face.
B('lower axle load bridge',(1.00,-.39,.97),(.40,.24,.07),wood)
block=B('lower axle bearing block',(1.00,-.38,1.05),(.20,.16,.20),wood)
cut(block,C('temporary lower axle bore',(1.00,-.38,1.05),.036,.32,iron,'Y'))
ring('lower axle fitted bronze bush',(1.00,-.38,1.05),.067,.032,.18,bronze,'Y')
C('turning lower engine axle',(0,.12,0),.028,.45,iron,'Y',fly)
ring('retained lower axle collar',(0,.28,0),.045,.027,.035,bronze,'Y',fly)
for x in (.84,1.16):C('bearing bridge fastener',(x,-.39,1.02),.018,.055,bronze)
# Freeze new support geometry and recheck the actually cut guide as editable triangles.
objects=[*old_frames,*[o for o in col.objects if o.type=='MESH']]
for obj in objects:
 if obj.modifiers:data=bpy.data.meshes.new_from_object(obj.evaluated_get(bpy.context.evaluated_depsgraph_get()));obj.modifiers.clear();obj.data=data
 if not obj.data.uv_layers:surfaces.physical_box_uv(obj)
 bm=bmesh.new();bm.from_mesh(obj.data);bmesh.ops.triangulate(bm,faces=list(bm.faces));bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-7);bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=1e-7);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(obj.data);bm.free()
 obj.data.calc_loop_triangles();bad={t.polygon_index for t in obj.data.loop_triangles if t.area<1e-12}
 if bad:
  bm=bmesh.new();bm.from_mesh(obj.data);bm.faces.ensure_lookup_table();bmesh.ops.delete(bm,geom=[bm.faces[i] for i in bad],context='FACES');bm.to_mesh(obj.data);bm.free()
profile=json.loads((P/'capture-profile.json').read_text());install_canonical_camera(scene,profile,bpy);scene.frame_set(1);assert_clean(scene,profile,bpy);bpy.ops.file.pack_all();native=O/'calcifier-v1.blend';bpy.ops.wm.save_as_mainfile(filepath=str(native),compress=True)
bpy.ops.wm.open_mainfile(filepath=str(native));scene=bpy.context.scene;root=bpy.data.objects['EXPORT | Calcifier all authored parts'];bpy.ops.object.select_all(action='DESELECT')
for obj in [root,*root.children_recursive]:obj.select_set(True)
bpy.ops.export_scene.gltf(filepath=str(O/'calcifier-v1.glb'),export_format='GLB',use_selection=True,export_cameras=False,export_lights=False,export_animations=True,export_animation_mode='SCENE',export_anim_scene_split_object=False,export_frame_range=True,export_force_sampling=True,export_frame_step=1,export_apply=True,export_extras=True)
(O/'capture-profile.json').write_text(json.dumps(profile,indent=2)+'\n');receipt=json.loads((P/'construction-receipt.json').read_text());receipt.update(parent_source_sha256=sha(source),source_sha256=sha(native),glb_sha256=sha(O/'calcifier-v1.glb'),final_repairs=['Open guide yoke clears rigid connecting arm','Mixer thrust collar bears on upper bronze journal','Pinion thrust collar bears on lower journal','Bored lower engine axle cradle carries flywheel','Rear guide framing and outer standoffs clear flywheel and rod swept volumes'],native_integrated=False)
(O/'construction-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
projection=bpy.data.objects.new('SPRITE ONLY | square ground grid',None);scene.collection.objects.link(projection);projection.scale.y=math.sqrt(2);root.parent=projection;scene.render.resolution_x=scene.render.resolution_y=512
for name,yaw in [('front',0),('east',270),('rear',180),('west',90)]:
 root.rotation_euler.z=math.radians(yaw);scene.frame_set(49);scene.render.filepath=str(O/(name+'-review512.png'));bpy.ops.render.render(write_still=True)
print('CALCIFIER_FITTED_SUPPORTS_SAVED',native,flush=True)
