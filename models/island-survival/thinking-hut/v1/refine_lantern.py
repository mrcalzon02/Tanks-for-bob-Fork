"""Owner correction: a supported, readable oil lantern instead of a dark box on the post."""
import bpy,bmesh,math,json,sys,hashlib,tempfile
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[4];P=R/'models/island-survival/thinking-hut/candidates/v1-production04';O=P.parent/'v1-lantern08'
if O.exists():raise FileExistsError(O)
O.mkdir(parents=True);tempfile.tempdir=str(R/'build/quarry-export-temp');sys.path.insert(0,str(R/'models/island-survival/primitive-steam-powered-pump/v3'))
from mesh_util import box,cylinder,tube,lathe
import surfaces
sys.path.insert(0,str(R.parent/'model-production/tools/fmpl'))
from blender_camera_guard import assert_clean,temporary_inspection_camera
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
source=P/'thinking-hut-v1.blend';assert sha(source)==json.loads((P/'construction-receipt.json').read_text())['source_sha256']
bpy.ops.wm.open_mainfile(filepath=str(source));s=bpy.context.scene;s.frame_set(1);root=bpy.data.objects['EXPORT | Thinking Hut authored shelter'];obj=bpy.data.objects;col=bpy.data.collections.new('HUT | owner-refined sheltered oil lantern');s.collection.children.link(col)
material=lambda suffix:next(m for m in bpy.data.materials if m.name.endswith(' | '+suffix))
iron=material('cast-iron-housing');bronze=material('worn-bronze-fittings');clay=material('thinking-hut-clay-flue');ember=material('thinking-hut-hot-lamp-wick')
outer=ember.copy();outer.name='THINKING HUT | sheltered-lantern-outer-flame';shader=outer.node_tree.nodes['Principled BSDF'];shader.inputs['Emission Color'].default_value=(1,.20,.015,1);shader.inputs['Emission Strength'].default_value=2;shader.inputs['Alpha'].default_value=.55
core=ember.copy();core.name='THINKING HUT | sheltered-lantern-hot-core';shader=core.node_tree.nodes['Principled BSDF'];shader.inputs['Emission Color'].default_value=(1,.56,.14,1);shader.inputs['Emission Strength'].default_value=5
for m in (outer,core):m['surface_authorship']='Thinking Hut wick flame: existing packed model-specific albedo/roughness/normal images with distinct warm outer flame and hot core emission, inspected in source and actual GLB'
def B(n,p,d,m,parent=root):
 o=box('HUT LANTERN | '+n,p,d,m,col,parent,.003);surfaces.apply(o,m);return o
def C(n,p,r,d,m,axis='Z',parent=root,segments=40):
 o=cylinder('HUT LANTERN | '+n,p,r,d,m,col,parent,axis,segments);surfaces.apply(o,m);return o
def wire(n,points,r,m,parent=root):
 pts=[Vector(p) for p in points];o=tube('HUT LANTERN | '+n,[(p,(pts[min(i+1,len(pts)-1)]-pts[max(0,i-1)]).normalized(),r,0) for i,p in enumerate(pts)],m,col,parent,12);surfaces.physical_box_uv(o);return o
def ring(n,p,outer_r,inner,depth,m):
 o=tube('HUT LANTERN | '+n,[(Vector((0,0,-depth/2)),Vector((0,0,1)),outer_r,inner),(Vector((0,0,depth/2)),Vector((0,0,1)),outer_r,inner)],m,col,root,48);o.location=p;surfaces.physical_box_uv(o);return o
for o in tuple(root.children_recursive):
 if o.name.startswith(('HUT | lantern cage','HUT | lantern post bracket','HUT | lamp oil cup','HUT | actual wick flame')):bpy.data.objects.remove(o,do_unlink=True)
# Keep useful original backing geometry as a curved, warm metal reflector,
# now seated between the rear guards rather than wrapped around the timber post.
back=obj['HUT | REUSED thinking-hut_wall_lantern'];pts=[v.co.copy() for v in back.data.vertices];lo=[min(v[a] for v in pts) for a in range(3)];hi=[max(v[a] for v in pts) for a in range(3)]
for v in back.data.vertices:
 x=(v.co.x-(lo[0]+hi[0])/2)/(hi[0]-lo[0])*.14
 v.co=Vector((-.98+x,-1.25-.010*(x/.07)**2+(v.co.y-(lo[1]+hi[1])/2)*.4,1.44+(v.co.z-(lo[2]+hi[2])/2)/(hi[2]-lo[2])*.27))
surfaces.apply(back,bronze)
# Actual anchored hook and bail: the hanging body clears the post by 1 cm.
B('post mounting strap',(-1.18,-1.268,1.72),(.085,.016,.39),iron)
for z in (1.56,1.88):C('strap retained fastener',(-1.18,-1.275,z),.018,.08,bronze,'Y',segments=6)
wire('projecting curved iron bracket',[(-1.18,-1.268,1.90),(-1.14,-1.29,1.92),(-1.06,-1.32,1.92),(-1.00,-1.32,1.91),(-.98,-1.32,1.88),(-.98,-1.32,1.81),(-.995,-1.32,1.79)],.009,iron)
bail=[(-.98+.07*math.cos(i*math.pi/24),-1.32,1.72+.07*math.sin(i*math.pi/24)) for i in range(25)];wire('riveted hanging bail',bail,.006,iron)
for x in (-1.05,-.91):
 wire('bail load carrying leg',[(x,-1.32,1.72),(x,-1.32,1.68)],.006,iron);C('bail shoulder pivot',(x,-1.32,1.68),.014,.04,bronze,'Y')
# Bellied reservoir, raised wick and a vented conical rain hood.
cup=lathe('HUT LANTERN | bellied oil reservoir',[(0,1.245),(.065,1.245),(.082,1.265),(.083,1.290),(.067,1.315),(.030,1.322),(0,1.322)],(-.98,-1.32),bronze,col,root,48);surfaces.physical_box_uv(cup)
ring('reservoir retaining foot',(-.98,-1.32,1.255),.105,.067,.018,iron)
C('threaded wick holder',(-.98,-1.32,1.326),.020,.018,bronze);C('real exposed wick',(-.98,-1.32,1.336),.006,.012,iron)
hood=lathe('HUT LANTERN | conical rain and heat hood',[(r,z+.12) for r,z in [(.126,1.505),(.126,1.518),(.056,1.585),(.035,1.590),(.035,1.605),(.024,1.605),(.024,1.585),(.048,1.574),(.115,1.512)]],(-.98,-1.32),bronze,col,root,48);surfaces.physical_box_uv(hood)
ring('hood rolled rim',(-.98,-1.32,1.629),.133,.116,.014,iron)
for i in range(4):
 a=math.pi/4+i*math.pi/2;x=-.98+.101*math.cos(a);y=-1.32+.101*math.sin(a);C('thin seated vertical guard',(x,y,1.453),.0048,.358,iron)
# Rooted teardrops give a visible warm flame with a distinct hot core, without
# painting a glow onto the sprite or adding an unexported model light.
flame=obj['HUT | working lamp flame'];flame.location=(-.98,-1.32,1.342)
for n,profile,mat in [('warm teardrop',[(0,0),(.012,.005),(.022,.018),(.028,.034),(.026,.050),(.019,.071),(.009,.092),(.004,.108),(0,.120)],outer),('hot rooted core',[(0,0),(.008,.006),(.014,.020),(.013,.032),(.008,.047),(.003,.060),(0,.069)],core)]:
 o=lathe('HUT LANTERN | '+n,profile,(0,0),mat,col,flame,32)
 for v in o.data.vertices:v.co.x+=.008*(v.co.z/.12)**2
 surfaces.physical_box_uv(o)
for frame in range(0,194):
 phase=math.tau*(frame-1)/192;flame.scale=(.001,.001,.001) if frame==0 else (1,1,.92+.14*math.sin(phase*3)+.055*math.sin(phase*7)+.035*math.cos(phase));flame.keyframe_insert(data_path='scale',frame=frame)
for layer in flame.animation_data.action.layers:
 for strip in layer.strips:
  for bag in strip.channelbags:
   for curve in bag.fcurves:
    for key in curve.keyframe_points:key.interpolation='LINEAR'
for o in [back,*[o for o in col.objects if o.type=='MESH']]:
 if o.modifiers:o.data=bpy.data.meshes.new_from_object(o.evaluated_get(bpy.context.evaluated_depsgraph_get()));o.modifiers.clear()
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.triangulate(bm,faces=list(bm.faces));bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-7);bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=1e-7);bmesh.ops.delete(bm,geom=[v for v in bm.verts if not v.link_faces],context='VERTS');bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free()
 o.data.calc_loop_triangles();bad={t.polygon_index for t in o.data.loop_triangles if t.area<1e-12}
 if bad:
  bm=bmesh.new();bm.from_mesh(o.data);bm.faces.ensure_lookup_table();bmesh.ops.delete(bm,geom=[bm.faces[i] for i in bad],context='FACES');bm.to_mesh(o.data);bm.free()
profile=json.loads((P/'capture-profile.json').read_text());s.frame_set(1);assert_clean(s,profile,bpy);bpy.ops.file.pack_all();native=O/'thinking-hut-v1.blend';bpy.ops.wm.save_as_mainfile(filepath=str(native),compress=True)
bpy.ops.wm.open_mainfile(filepath=str(native));s=bpy.context.scene;root=bpy.data.objects['EXPORT | Thinking Hut authored shelter'];bpy.ops.object.select_all(action='DESELECT')
for o in [root,*root.children_recursive]:o.select_set(True)
bpy.ops.export_scene.gltf(filepath=str(O/'thinking-hut-v1.glb'),export_format='GLB',use_selection=True,export_cameras=False,export_lights=False,export_animations=True,export_animation_mode='SCENE',export_anim_scene_split_object=False,export_frame_range=True,export_force_sampling=True,export_frame_step=1,export_apply=True,export_extras=True)
(O/'capture-profile.json').write_text(json.dumps(profile,indent=2)+'\n');receipt=json.loads((P/'construction-receipt.json').read_text());receipt.update(parent_source_sha256=sha(source),source_sha256=sha(native),glb_sha256=sha(O/'thinking-hut-v1.glb'),owner_lantern_correction='Open guarded oil lantern, distinct reservoir/wick/rooted flame/hood/reflector, and anchored bracket/bail clear of the post',native_integrated=False);(O/'construction-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
projection=bpy.data.objects.new('SPRITE ONLY | square ground projection',None);s.collection.objects.link(projection);projection.scale.y=math.sqrt(2);root.parent=projection
s.render.resolution_x=s.render.resolution_y=512;s.render.filepath=str(O/'front-review512.png');bpy.ops.render.render(write_still=True)
with temporary_inspection_camera(s,bpy,'Lantern bracket reservoir wick and hood') as camera:
 target=root.matrix_world@Vector((-.99,-1.30,1.58));camera.data.type='ORTHO';camera.data.ortho_scale=.80;camera.location=target+Vector((.40,-1.8,.35));camera.rotation_euler=(target-camera.location).to_track_quat('-Z','Y').to_euler();s.camera=camera;s.render.filepath=str(O/'lantern-close512.png');bpy.ops.render.render(write_still=True)
s.render.resolution_x=s.render.resolution_y=256
for frame,state in [(0,'idle'),(1,'working')]:
 s.frame_set(frame);s.render.filepath=str(O/('north-'+state+'-00.png'));bpy.ops.render.render(write_still=True)
print('OWNER_LANTERN_REFINEMENT_SAVED',native,flush=True)
