"""Masonry upgrade of the real Tanks lab, preserving its starter and useful study fittings."""
import bpy,bmesh,json,math,hashlib,sys,tempfile
import numpy as np
from pathlib import Path
from mathutils import Vector
H=Path(__file__).resolve().parent;R=H.parents[3];P=R/'models/island-survival/thinking-hut/candidates/v1-lantern08';O=H.parent/'candidates/v1-production03'
if O.exists():raise FileExistsError(O)
O.mkdir(parents=True);tempfile.tempdir=str(R/'build/quarry-export-temp');sys.path.insert(0,str(R/'models/island-survival/primitive-steam-powered-pump/v3'))
from mesh_util import mesh,box,cylinder,tube
import surfaces
sys.path.insert(0,str(R.parent/'model-production/tools/fmpl'))
from blender_camera_guard import install_canonical_camera,assert_clean,temporary_inspection_camera
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
source=P/'thinking-hut-v1.blend';assert sha(source)=='4c7dee2ad5124ea1c078b0f4f997c994b8d971d9395f86b083254f3bc9e75b13'
bpy.ops.wm.open_mainfile(filepath=str(source));s=bpy.context.scene;s.frame_set(1);root=bpy.data.objects['EXPORT | Thinking Hut authored shelter'];root.name='EXPORT | Pondering Hovel authored shelter';col=bpy.data.collections.new('HOVEL | masonry shingle roof and folio research');s.collection.children.link(col)
mat=lambda suffix:next(m for m in bpy.data.materials if m.name.endswith(' | '+suffix))
m=dict(wood=mat('long-grain-oak'),endgrain=mat('cut-oak-growth-rings'),iron=mat('cast-iron-housing'),bronze=mat('worn-bronze-fittings'),clay=mat('thinking-hut-clay-flue'),stone=mat('thinking-hut-rounded-hearth-stone'),paper=mat('thinking-hut-handwritten-records'))
rng=np.random.default_rng(171801);u,v=np.meshgrid(np.linspace(0,1,512),np.linspace(0,1,512));broad=surfaces.field(rng,(512,512),.018);fine=surfaces.field(rng,(512,512),.22)
grain=np.sin(v*240+1.3*np.sin(u*9)+.2*broad)+.25*np.sin(v*710+np.sin(u*17))
for name,color,rough,detail in [('porous-fired-brick',(.37,.205,.13),.88,.018*broad+.005*fine),('lime-clay-mortar',(.31,.30,.265),.95,.010*broad+.003*fine),('split-cedar-shingles',(.25,.205,.145),.89,.021*grain+.014*broad),('translucent-horn-pane',(.39,.30,.16),.40,.013*broad+.005*np.sin(u*120+v*20))]:
 m[name]=surfaces.material('pondering-hovel-'+name,np.stack([x+detail for x in color],axis=-1),rough+.02*fine,.5+.020*broad+.010*fine,0,O)
m['translucent-horn-pane'].node_tree.nodes['Principled BSDF'].inputs['Alpha'].default_value=.38
for material in bpy.data.materials:
 material.name=material.name.replace('THINKING HUT','PONDERING HOVEL');material['surface_authorship']='Pondering Hovel: retained fitted research/lantern components from its Thinking Hut upgrade, new model-specific fired-brick/mortar/cedar-shingle/horn-pane maps and per-part physical UVs. No new gameplay function.'
def B(n,p,d,material,parent=root,bevel=.006):
 o=box('HOVEL | '+n,p,d,material,col,parent,bevel);surfaces.apply(o,material,m['endgrain'] if material in (m['wood'],m['split-cedar-shingles']) else None);return o
def C(n,p,r,d,material,axis='Z',parent=root,segments=40):
 o=cylinder('HOVEL | '+n,p,r,d,material,col,parent,axis,segments);surfaces.apply(o,material);return o
def E(n,p=(0,0,0)):
 o=bpy.data.objects.new('HOVEL | '+n,None);col.objects.link(o);o.parent=root;o.location=p;return o
def beam(n,a,b,w,material=m['wood']):
 a,b=Vector(a),Vector(b);o=B(n,(a+b)/2,(w,w,(b-a).length),material);o.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler();return o
def bore(o,cut):
 bpy.context.view_layer.update();bpy.context.view_layer.objects.active=o;mod=o.modifiers.new('Actual masonry/roof/bearing opening','BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=cut;bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cut,do_unlink=True)
def ring(n,p,outer,inner,depth,material,axis='Z',parent=root):
 t=Vector({'X':(1,0,0),'Y':(0,1,0),'Z':(0,0,1)}[axis]);o=tube('HOVEL | '+n,[(-t*depth/2,t,outer,inner),(t*depth/2,t,outer,inner)],material,col,parent,40);o.location=p;surfaces.physical_box_uv(o);return o
def remove(o):bpy.data.objects.remove(o,do_unlink=True)
# Preserve the fitted balance, lantern, desk structure and braced porch. Replace
# the timber/thatch hut envelope with this machine's actual masonry starter.
for o in tuple(root.children_recursive):
 name=o.name
 if name.startswith('HUT | REUSED thinking-hut_') and 'wall_lantern' not in name:remove(o);continue
 if any(name.startswith('HUT | '+n) for n in ['separate floor board','individual staggered roof reed','ridge saddle binding','roof rafter','rear rafter bearing seat','supported ridge purlin','wall exposed stave','window ','continuous clay flue','roof heat clearance curb']):remove(o);continue
 if name.startswith(('HUT | load carrying post','HUT | post stone pad','HUT | post knee brace')) and o.location.y>.5:remove(o)
verts=[];groups={};group=None;starter=H/'starter-pondering-hovel.obj';contract=json.loads((H/'contract.json').read_text());assert sha(starter)==contract['source']['sha256']
for line in starter.read_text().splitlines():
 t=line.split()
 if not t:continue
 if t[0]=='v':verts.append(Vector(map(float,t[1:])))
 elif t[0]=='g':group=t[1];groups[group]=[]
 elif t[0]=='f':groups[group].append(tuple(int(x)-1 for x in t[1:]))
reused=[]
for name,faces in groups.items():
 ids=sorted({i for face in faces for i in face});lookup={i:j for j,i in enumerate(ids)};pts=[verts[i].copy() for i in ids];fs=[tuple(lookup[i] for i in face) for face in faces];material=m['wood'];solid=None
 if name.endswith('_floor'):pts=[(p.x,p.y,p.z*.4) for p in pts];material=m['stone']
 elif name.endswith('_masonry_walls'):
  fs=fs[6:];pts=[(p.x*.97,-.55+(p.y+1.23)*(1.68/2.46),.18+(p.z-.335)*(1.80/1.69)) for p in pts];material=m['lime-clay-mortar'];solid=.12
 elif name.endswith('_shingle_roof'):
  fs=fs[:4];pts=[(p.x,p.y,2.10+(p.z-1.82)*(.90/1.04)) for p in pts];material=m['split-cedar-shingles'];solid=.075
 elif name.endswith('_front_entry'):pts=[(-.70+p.x*.72,-.48+(p.y+1.25)*.6,.18+(p.z-.365)*1.075) for p in pts]
 elif name.endswith('_chimney'):
  fs=[f for f in fs if max(pts[i].z for i in f)-min(pts[i].z for i in f)>.1];pts=[(.82+(p.x-.78)*.5,.50+(p.y-.61)*.5,1.08+(p.z-2.20)*(2.48/1.10)) for p in pts];material=m['clay'];solid=.025
 elif name.endswith('_research_window'):
  pts=[(.65+(p.x+.86)*(.62/.41),-.55+(p.y+1.26)*(.008/.09),1.35+(p.z-1.46)*(.50/.48)) for p in pts];material=m['translucent-horn-pane']
 elif name.endswith('_desk_visible'):pts=[(.18+(p.x-.13),-.99+(p.y+1.05)*1.5,.745+(p.z-.93)*(.055/.23)) for p in pts]
 o=mesh('HOVEL | REUSED '+name,pts,fs,material,col,root);surfaces.apply(o,material,m['endgrain'] if material==m['wood'] else None);reused.append(o.name)
 if solid:
  mod=o.modifiers.new('Actual construction wall thickness','SOLIDIFY');mod.thickness=solid;mod.offset=-1;bpy.context.view_layer.objects.active=o;bpy.ops.object.modifier_apply(modifier=mod.name)
 if name.endswith('_masonry_walls'):
  for x in (-1.1737,1.1737):bore(o,B('temporary side window',(x,.10,1.17),(.40,.72,.54),m['iron']))
 if name.endswith('_shingle_roof'):bore(o,B('temporary square chimney clearance',(.82,.50,2.70),(.54,.54,2),m['iron']))
# New stone paving carries both the masonry and retained porch/desk.
for ix in range(8):
 for iy in range(8):B('seated worked stone paving',(-1.25125+ix*.3575,-1.23375+iy*.3525,.162),(.350,.345,.036),m['stone'])
def row_bricks(n,a,b,step,make):
 x=a
 while x<b-.02:
  width=min(step,b-x);make(x+width/2,width-.008);x+=width
for row in range(10):
 z=.27+row*.18
 for sign in (-1,1):
  spans=[(-.55,1.13)]
  if 4<=row<=6:spans=[(-.55,-.26),(.46,1.13)]
  for a,b in spans:row_bricks('side',a,b,.31 if row%2==0 else .28,lambda y,w:B('bonded side wall brick',(sign*1.15,y,z),(.12,w,.17),m['porous-fired-brick']))
 row_bricks('rear',-1.21,1.21,.31 if row%2==0 else .28,lambda x,w:B('bonded rear wall brick',(x,1.10,z),(w,.12,.17),m['porous-fired-brick']))
 spans=[(-.20,1.17)] if row not in (5,6,7) else [(-.20,.32),(.98,1.17)]
 for a,b in spans:row_bricks('front',a,b,.29 if row%2==0 else .32,lambda x,w:B('bonded front reading wall brick',(x,-.55,z),(w,.12,.17),m['porous-fired-brick']))
# Side windows and a supported translucent horn reading window.
for x in (-1.17,1.17):
 for z in (.90,1.44):B('side window lintel sill',(x,.10,z),(.17,.80,.055),m['wood'])
 for y in (-.26,.46):B('side window jamb',(x,y,1.17),(.17,.055,.59),m['wood'])
 for y in (-.08,.24):B('side window vertical lattice',(x,y,1.17),(.04,.025,.50),m['wood'])
for x in (.32,.98):B('front reading window jamb',(x,-.56,1.35),(.04,.15,.58),m['wood'])
for z in (1.08,1.62):B('front reading window sill lintel',(.65,-.56,z),(.70,.15,.04),m['wood'])
B('horn pane centre mullion',(.65,-.565,1.35),(.025,.04,.50),m['wood']);B('horn pane cross rail',(.65,-.565,1.35),(.62,.04,.025),m['wood'])
C('drawer pull retained pin',(.18,-1.155,.745),.014,.04,m['bronze'],'Y');B('wooden drawer handle',(.18,-1.17,.745),(.12,.025,.02),m['wood'])
# Rafters follow the new starter roof, with real seats on the retained beams.
slope=.90/1.48
for x in (-1.30,-.65,0,.65,1.30):
 for sign in (-1,1):beam('roof rafter',(x,sign*1.43,3.0-1.43*slope-.112),(x,0,2.888),.07)
 for y in (-1.20,1.07):
  bottom=3.0-abs(y)*slope-.112-.048;h=max(.015,bottom-2.0875);B('rafter seated bearing pad',(x,y,2.0875+h/2),(.09,.12,h),m['wood'])
beam('supported ridge timber',(-1.38,0,2.888),(1.38,0,2.888),.08)
angle=math.atan(slope)
for sign in (-1,1):
 for row in range(6):
  y=.13+row*.25;offset=.105 if row%2 else 0
  for i in range(15):
   raw_left=-1.57+i*.21+offset;left=max(-1.46,raw_left);right=min(1.46,raw_left+.204)
   if right-left<.04:continue
   x=(left+right)/2;points=[]
   # Tapered, slightly lifted butt meets the next course rather than putting
   # overlapping flat boards in the same plane. Upper .004, lower .024 thick.
   for top in (False,True):
    for xx,frac in [(left,0),(right,0),(right,1),(left,1)]:
     run=y-.16+frac*.32;z=3.0-run*slope+.006+frac*.01072+(0 if not top else .004+.020*frac);points.append((xx,sign*run,z))
   o=mesh('HOVEL | separate split cedar roof shingle',points,[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],m['split-cedar-shingles'],col,root,bevel=.0015);surfaces.apply(o,m['split-cedar-shingles'],m['endgrain'])
   if abs(x-.82)<.40 and sign>0 and .04<y<.96:bore(o,B('temporary shingle chimney clearance',(.82,.50,2.70),(.54,.54,2),m['iron']))
# A continuous brick firebox and bonded stack support the chimney from the base.
B('hearth masonry load pad',(.82,.50,.21),(.72,.72,.06),m['stone'])
for row in range(18):
 z=.33+row*.18;wide=.66 if row<5 else .48;thick=.12 if row<5 else .10;half=wide/2;side=half-thick/2
 for sign in (-1,1):
  if row%2==0:
   B('bonded chimney side course',(.82+sign*side,.50,z),(thick,wide,.17),m['porous-fired-brick'])
   if not (sign<0 and row in (1,2)):B('bonded chimney cross course',(.82,.50+sign*side,z),(wide-2*thick,thick,.17),m['porous-fired-brick'])
  else:
   B('bonded chimney cross course',(.82,.50+sign*side,z),(wide,thick,.17),m['porous-fired-brick'])
   B('bonded chimney side course',(.82+sign*side,.50,z),(thick,wide-2*thick,.17),m['porous-fired-brick'])
cap=B('full bearing chimney stone cap',(.82,.50,3.49),(.56,.56,.08),m['stone']);bore(cap,C('temporary open cap bore',(.82,.50,3.49),.14,.30,m['iron']))
for dx,dy,dims in [(-.285,0,(.08,.64,.04)),(.285,0,(.08,.64,.04)),(0,-.285,(.49,.08,.04)),(0,.285,(.49,.08,.04))]:
 o=B('fitted sloping clay roof flashing',(.82+dx,.50+dy,3.0-(.50+dy)*slope+.055),dims,m['clay'])
 for vtx in o.data.vertices:vtx.co.z-=slope*vtx.co.y
# Hinged research folio. The original paper supplies remain on the bench; this
# is visible research handling, not a new manufacturing recipe or output.
for name in ['HUT | food support bowl','HUT | meal ration in bowl']:bpy.data.objects[name].location+=Vector((.01,-.26,0))
bpy.data.objects['HUT | sorted dossier bundle.002'].location.x=.52
folio=E('hinged research folio',(.16,-.85,.95));cover=B('bound folio cover',(0,-.13,0),(.28,.26,.012),m['wood'],folio);bore(cover,C('temporary folio rotating seat',(0,0,0),.013,.50,m['iron'],'X',folio));B('attached handwritten folio leaf',(0,-.14,.008),(.26,.22,.003),m['paper'],folio,bevel=.001)
for x in (-.10,.10):ring('folio rotating hinge knuckle',(x,0,0),.022,.013,.03,m['bronze'],'X',folio)
C('folio fixed hinge pin',(.16,-.85,.95),.012,.43,m['iron'],'X')
for x in (-.025,.345):
 o=B('folio hinge pedestal',(x,-.85,.91),(.04,.05,.09),m['wood']);bore(o,C('temporary folio pedestal bore',(x,-.85,.95),.013,.10,m['iron'],'X'))
for frame in range(0,194):
 phase=math.tau*(frame-1)/192;folio.rotation_euler.x=-.02 if frame==0 else -.23-.08*math.sin(phase);folio.keyframe_insert(data_path='rotation_euler',frame=frame)
for layer in folio.animation_data.action.layers:
 for strip in layer.strips:
  for bag in strip.channelbags:
   for curve in bag.fcurves:
    for key in curve.keyframe_points:key.interpolation='LINEAR'
# Freeze and triangulate all new physical construction, keeping the inherited
# editable study fittings and their proven kinematics intact.
for o in col.objects:
 if o.type!='MESH':continue
 if o.modifiers:o.data=bpy.data.meshes.new_from_object(o.evaluated_get(bpy.context.evaluated_depsgraph_get()));o.modifiers.clear()
 if not o.data.uv_layers:surfaces.physical_box_uv(o)
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.triangulate(bm,faces=list(bm.faces));bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-7);bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=1e-7);bmesh.ops.delete(bm,geom=[v for v in bm.verts if not v.link_faces],context='VERTS');bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free()
 o.data.calc_loop_triangles();bad={t.polygon_index for t in o.data.loop_triangles if t.area<1e-12}
 if bad:
  bm=bmesh.new();bm.from_mesh(o.data);bm.faces.ensure_lookup_table();bmesh.ops.delete(bm,geom=[bm.faces[i] for i in bad],context='FACES');bm.to_mesh(o.data);bm.free()
profile=json.loads((P/'capture-profile.json').read_text());profile['camera_override']['target']=[0,0,1.35];install_canonical_camera(s,profile,bpy);s.frame_set(1);assert_clean(s,profile,bpy);bpy.ops.file.pack_all();native=O/'pondering-hovel-v1.blend';bpy.ops.wm.save_as_mainfile(filepath=str(native),compress=True)
bpy.ops.wm.open_mainfile(filepath=str(native));s=bpy.context.scene;root=bpy.data.objects['EXPORT | Pondering Hovel authored shelter'];bpy.ops.object.select_all(action='DESELECT')
for o in [root,*root.children_recursive]:o.select_set(True)
bpy.ops.export_scene.gltf(filepath=str(O/'pondering-hovel-v1.glb'),export_format='GLB',use_selection=True,export_cameras=False,export_lights=False,export_animations=True,export_animation_mode='SCENE',export_anim_scene_split_object=False,export_frame_range=True,export_force_sampling=True,export_frame_step=1,export_apply=True,export_extras=True)
(O/'capture-profile.json').write_text(json.dumps(profile,indent=2)+'\n');(O/'construction-receipt.json').write_text(json.dumps(dict(parent_thinking_hut_source_sha256=sha(source),starter_sha256=sha(starter),reused_starter_groups=reused,source_sha256=sha(native),glb_sha256=sha(O/'pondering-hovel-v1.glb'),native_orientation='fixed north',smoke_outlet_source=[.82,.50,3.56],gameplay_changed=False,owner_visual_approved=False,native_integrated=False),indent=2)+'\n')
projection=bpy.data.objects.new('SPRITE ONLY | square ground projection',None);s.collection.objects.link(projection);projection.scale.y=math.sqrt(2);root.parent=projection;s.render.resolution_x=s.render.resolution_y=512;s.render.filepath=str(O/'front-review512.png');bpy.ops.render.render(write_still=True)
with temporary_inspection_camera(s,bpy,'Masonry upgraded research porch') as camera:
 target=root.matrix_world@Vector((.30,-.65,1.10));camera.data.type='ORTHO';camera.data.ortho_scale=2.9;camera.location=target+Vector((2,-4,1.8));camera.rotation_euler=(target-camera.location).to_track_quat('-Z','Y').to_euler();s.camera=camera;s.render.filepath=str(O/'research-porch-close512.png');bpy.ops.render.render(write_still=True)
print('PONDERING_HOVEL_SOURCE_SAVED',native,flush=True)
