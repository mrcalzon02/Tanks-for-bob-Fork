"""Refine the tracked square cistern starter into a supported native storage tank."""
import bpy,bmesh,json,math,sys,tempfile,hashlib
from pathlib import Path
from mathutils import Vector
import numpy as np
HERE=Path(__file__).resolve().parent;R=HERE.parents[3];O=R/'models/island-survival/wood-basin/candidates/v1-pilot03'
if O.exists():raise FileExistsError(O)
O.mkdir(parents=True);temp=R/'build/basin-export-temp';temp.mkdir(exist_ok=True);tempfile.tempdir=str(temp)
sys.path.insert(0,str(R/'models/island-survival/primitive-steam-powered-pump/v3'))
from mesh_util import box,cylinder,tube,mesh
import surfaces
sys.path.insert(0,str(R.parent/'model-production/tools/fmpl'))
from blender_camera_guard import install_canonical_camera,assert_clean
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
contract=json.loads((HERE/'contract.json').read_text());starter=HERE/'starter-wood-basin.obj';assert sha(starter)==contract['source']['sha256']
bpy.ops.wm.read_factory_settings(use_empty=True);scene=bpy.context.scene
scene.render.engine='CYCLES';scene.cycles.samples=32;scene.cycles.use_denoising=False
scene.render.film_transparent=True;scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA'
scene.world=bpy.data.worlds.new('Basin neutral environment');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.22,.22,.22,1)
for loc,power,size in [((4,-3,6),650,5),((-3,2,5),450,4),((0,1,7),300,3)]:
 l=bpy.data.lights.new('Basin area','AREA');l.energy=power;l.size=size;o=bpy.data.objects.new('Basin area',l);scene.collection.objects.link(o);o.location=loc;o.rotation_euler=(Vector((0,0,.6))-o.location).to_track_quat('-Z','Y').to_euler()
root=bpy.data.objects.new('EXPORT | Wood Basin all authored parts',None);scene.collection.objects.link(root)
collection=bpy.data.collections.new('BASIN | timber cistern and full-bore fittings');scene.collection.children.link(collection)
m=surfaces.create(O)
rng=np.random.default_rng(171126);stone=surfaces.field(rng,(512,512),.04);tone=np.clip(.23+.018*stone,.15,.33);color=np.stack([tone*.96,tone,tone*.98],axis=-1)
m['stone']=surfaces.material('basin-rough-stone-piers',color,.91+.015*stone,.5+.04*stone,0,O)
for mat in m.values():
 mat.name=mat.name.replace('PUMP V3','WOOD BASIN');mat['surface_authorship']='Basin stave/floor grain, cut end rings, iron bands and native port roles'
def B(n,p,d,mat,parent=root):
 o=box('BASIN | '+n,p,d,mat,collection,parent);surfaces.apply(o,mat,m['endgrain'] if mat==m['wood'] else None);return o
def C(n,p,r,d,mat,axis='Z',parent=root):
 o=cylinder('BASIN | '+n,p,r,d,mat,collection,parent,axis);surfaces.apply(o,mat);return o
def T(n,pts,outer,inner):
 samples=[]
 for i,p in enumerate(pts):samples.append((p,(Vector(pts[min(i+1,len(pts)-1)])-Vector(pts[max(i-1,0)])).normalized(),outer,inner))
 return tube('BASIN | '+n,samples,m['iron'],collection,root)
# Parse only starter groups used in production; preserve original source on disk.
vertices=[];groups={};current=None
for line in starter.read_text().splitlines():
 p=line.split()
 if not p:continue
 if p[0]=='v':vertices.append(Vector(map(float,p[1:])))
 elif p[0]=='g':current=p[1];groups[current]=[]
 elif p[0]=='f':groups[current].append([int(v)-1 for v in p[1:]])
reused=[]
for name,faces in groups.items():
 if not ('floor' in name or 'stave_' in name):continue
 ids=sorted({i for f in faces for i in f});remap={idx:i for i,idx in enumerate(ids)}
 pts=[vertices[i].copy() for i in ids]
 if 'floor' in name:
  pts=[(v.x*1.30,v.y*1.30,v.z*.5+.1) for v in pts]
 else:
  center=sum(pts,Vector())/len(pts);x=math.copysign(1.17,center.x);y=math.copysign(1.17,center.y)
  pts=[(x+(v.x-center.x),y+(v.y-center.y),.15+(v.z-.05)*1.35) for v in pts]
 o=mesh('BASIN | REUSED '+name,pts,[tuple(remap[i] for i in f) for f in faces],m['wood'],collection,root,.006);surfaces.apply(o,m['wood'],m['endgrain']);reused.append(o.name)
for x in (-1.16,1.16):
 for y in (-1.16,1.16):B('rough stone pier',(x,y,.075),(.34,.34,.15),m['stone'])
# Four walls: separate watertight timber staves and an actual central sight aperture.
wallparts=[]
for facing,yaw in [('south',0),('east',90),('north',180),('west',270)]:
 local=bpy.data.objects.new('BASIN | '+facing+' wall frame',None);scene.collection.objects.link(local);local.parent=root;local.rotation_euler.z=math.radians(yaw)
 for i in range(12):
  x=-1.1+(i+.5)*2.2/12
  if abs(x)<.20:
   for z,depth in [(.32,.14),(1.32,.16)]:
    wallparts.append(B(facing+' window sill stave '+str(i),(x,-1.145,z),(.182,.13,depth),m['wood'],local))
  else:wallparts.append(B(facing+' individual stave '+str(i),(x,-1.145,.84),(.182,.13,1.18),m['wood'],local))
 for x in (-.245,.245):B(facing+' glass frame upright',(x,-1.225,.84),(.065,.065,.84),m['bronze'],local)
 for z in (.405,1.275):B(facing+' glass frame crosspiece',(0,-1.225,z),(.55,.065,.065),m['bronze'],local)
 # Preview fill volume represents the native window. Production body excludes it.
 fluid=B(facing+' PREVIEW fluid fill',(0,-1.154,.45),(.38,.035,.02),m['copper'],local)
 fluid['native_fluid_preview']=True
 for f in range(1,98):
  level=.5-.5*math.cos((f-1)*math.tau/96);h=.04+.74*level
  fluid.scale.z=h/.02;fluid.location.z=.44+h/2
  fluid.keyframe_insert(data_path='scale',frame=f);fluid.keyframe_insert(data_path='location',frame=f)
 # Restraint bands continue over corner posts; central windows remain open.
 for z in (.34,1.36):
  B(facing+' iron restraint band',(0,-1.23,z),(2.45,.035,.055),m['iron'],local)
 for x in (-1.13,1.13):
  for z in (.34,1.36):C(facing+' square-headed band fastener',(x,-1.255,z),.035,.035,m['bronze'],'Y',local)
# Board lid and supported service hatch keep unknown fluid contents unpainted.
for i in range(10):
 x=-1.12+(i+.5)*2.24/10
 B('removable lid plank '+str(i),(x,0,1.455),(.219,2.24,.075),m['wood'])
for y in (-.72,.72):B('lid brace',(0,y,1.515),(2.28,.10,.05),m['iron'])
B('service hatch',(0,-.15,1.53),(.62,.64,.045),m['wood'])
for x in (-.20,.20):B('hatch hinge',(x,.13,1.56),(.085,.19,.025),m['bronze'])
B('hatch lifting bar',(0,-.34,1.59),(.29,.05,.045),m['iron'])
# A true hollow union at each paired corner avoids intersecting capped pipe bores.
def boolean_apply(a,b,operation):
 bpy.context.view_layer.objects.active=a;mod=a.modifiers.new('True full-bore corner joint','BOOLEAN');mod.object=b;mod.operation=operation;mod.solver='EXACT';bpy.ops.object.modifier_apply(modifier=mod.name)
def rawpipe(n,start,end,r):
 a,b=Vector(start),Vector(end);o=C(n,(a+b)/2,r,(b-a).length,m['iron']);o.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler();return o
cutters=[]
for sign in (-1,1):
 # sign=-1: NW (-1,+1); sign=+1: SE (+1,-1).
 x=sign;y=-sign
 segments=[((x,y*1.5,.36),(x,y*.72,.36)),((x*1.5,y,.36),(x*.72,y,.36))]
 outer=[rawpipe('manifold outer',a,b,.285) for a,b in segments]
 boolean_apply(outer[0],outer[1],'UNION');bpy.data.objects.remove(outer[1],do_unlink=True)
 inner=[rawpipe('manifold bore',Vector(a)+(Vector(a)-Vector(b)).normalized()*.01,Vector(b)+(Vector(b)-Vector(a)).normalized()*.01,.245) for a,b in segments]
 boolean_apply(inner[0],inner[1],'UNION');bpy.data.objects.remove(inner[1],do_unlink=True)
 boolean_apply(outer[0],inner[0],'DIFFERENCE');bpy.data.objects.remove(inner[0],do_unlink=True)
 outer[0].name='BASIN | hollow connected corner manifold '+str(sign);surfaces.apply(outer[0],m['iron'])
 for a,b in segments:
  direction=(Vector(b)-Vector(a)).normalized()
  T('fixed collar '+str(a),[a,tuple(Vector(a)+direction*.075)],.34,.245)
  cutter=rawpipe('temporary timber bore',Vector(a)-direction*.01,Vector(b)+direction*.01,.287);cutters.append(cutter)
# Cut the real openings in adjacent wood, including the reused floor/posts.
for o in [*wallparts,*[bpy.data.objects[n] for n in reused]]:
 for cutter in cutters:
  # Bounding-box overlap filter is only an optimization; exact booleans do the cut.
  bpy.context.view_layer.update();pts=[cutter.matrix_world@Vector(c) for c in cutter.bound_box];q=[o.matrix_world@Vector(c) for c in o.bound_box]
  if all(min(v[i] for v in pts)<=max(v[i] for v in q) and max(v[i] for v in pts)>=min(v[i] for v in q) for i in range(3)):boolean_apply(o,cutter,'DIFFERENCE')
for o in cutters:bpy.data.objects.remove(o,do_unlink=True)
for o in root.children_recursive:
 if o.type!='MESH':continue
 if not o.data.uv_layers:surfaces.physical_box_uv(o)
 if o.modifiers:
  evaluated=o.evaluated_get(bpy.context.evaluated_depsgraph_get());finished=bpy.data.meshes.new_from_object(evaluated);o.modifiers.clear();o.data=finished
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.triangulate(bm,faces=list(bm.faces));bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-7);bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=1e-7);bmesh.ops.delete(bm,geom=[f for f in bm.faces if f.calc_area()<1e-12],context='FACES');bm.to_mesh(o.data);bm.free()
 o.data.calc_loop_triangles();bad={t.polygon_index for t in o.data.loop_triangles if t.area<1e-12}
 if bad:
  bm=bmesh.new();bm.from_mesh(o.data);bm.faces.ensure_lookup_table();bmesh.ops.delete(bm,geom=[bm.faces[i] for i in bad],context='FACES');bm.to_mesh(o.data);bm.free()
 if o.animation_data:
  for layer in o.animation_data.action.layers:
   for strip in layer.strips:
    for bag in strip.channelbags:
     for curve in bag.fcurves:
      for k in curve.keyframe_points:k.interpolation='LINEAR'
profile={'camera_policy':'fmpl.factorio45.v1','capture_kind':'entity','orientation_policy':'rotatable','directions':[0,90,180,270],'states':{'idle':[0],'working':list(range(1,92,6))},'source_size':256,'fps':8,'camera_override':{'type':'ORTHO','elevation_deg':45,'azimuth_deg':0,'distance':math.sqrt(72),'ortho_scale':4.8,'target':[0,0,.75]}}
install_canonical_camera(scene,profile,bpy);scene.render.fps=48;scene.frame_start=1;scene.frame_end=97;scene.frame_set(1);bpy.ops.file.pack_all();assert_clean(scene,profile,bpy)
native=O/'wood-basin-v1.blend';bpy.ops.wm.save_as_mainfile(filepath=str(native),compress=True)
bpy.ops.wm.open_mainfile(filepath=str(native));scene=bpy.context.scene;root=bpy.data.objects['EXPORT | Wood Basin all authored parts']
bpy.ops.object.select_all(action='DESELECT')
for o in [root,*root.children_recursive]:o.select_set(True)
bpy.ops.export_scene.gltf(filepath=str(O/'wood-basin-v1.glb'),export_format='GLB',use_selection=True,export_cameras=False,export_lights=False,export_animations=True,export_animation_mode='SCENE',export_anim_scene_split_object=False,export_frame_range=True,export_force_sampling=True,export_frame_step=1,export_apply=True,export_extras=True)
(O/'capture-profile.json').write_text(json.dumps(profile,indent=2)+'\n')
(O/'reuse-receipt.json').write_text(json.dumps(dict(starter_sha256=sha(starter),reused_groups=reused,reused_geometry_refined_to_native_3x3=True,source_sha256=sha(native),runtime_sha256=sha(O/'wood-basin-v1.glb'),liquid_preview='Editable fill/drain demonstrator only; native body captures exclude it and actual game window uses tank contents'),indent=2)+'\n')
projection=bpy.data.objects.new('SPRITE ONLY | square ground grid',None);scene.collection.objects.link(projection);projection.scale.y=math.sqrt(2);root.parent=projection
for o in root.children_recursive:
 if o.get('native_fluid_preview'):o.hide_render=True
for facing,yaw in [('north',0),('east',270),('south',180),('west',90)]:
 root.rotation_euler.z=math.radians(yaw);scene.frame_set(25);assert_clean(scene,profile,bpy);scene.render.filepath=str(O/(facing+'-pilot.png'));bpy.ops.render.render(write_still=True)
print('BASIN_EDITABLE_AND_GLB_SAVED',native,flush=True)
